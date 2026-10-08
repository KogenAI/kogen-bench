defmodule Trackline.PortCleanupTest do
  use Trackline.DataCase, async: false
  alias Trackline.{Repo, Support}
  alias Trackline.Support.{Organization, Ticket, Comment, Membership}
  alias Trackline.Ports.{AccountLifecycle, IncinerateDue, CleanupSchedule, CleanupBoard, CleanupAsset, CleanupInvitation, CleanupEvent, CleanupSearch}
  import Trackline.AccountsFixtures
  import Trackline.SupportFixtures
  @now ~U[2026-10-03 12:00:00Z]
  defp org(age, owner) do
    o = organization_fixture(owner)
    {:ok, o} = AccountLifecycle.cancel(o, DateTime.add(@now, -age, :second))
    o
  end
  defp sweep, do: IncinerateDue.perform(%Oban.Job{args: %{"now" => DateTime.to_iso8601(@now)}})
  defp fill(org, user) do
    ticket = ticket_fixture(org, user)
    comment_fixture(ticket, user)
    b = Repo.insert!(%CleanupBoard{organization_id: org.id, name: "Private"})
    Repo.insert!(%CleanupAsset{organization_id: org.id, board_id: b.id, payload: "secret"})
    Repo.insert!(%CleanupInvitation{organization_id: org.id, email: "invite@example.com"})
    Repo.insert!(%CleanupEvent{organization_id: org.id, ticket_id: ticket.id, body: "history"})
    Repo.insert!(%CleanupSearch{organization_id: org.id, ticket_id: ticket.id, body: "indexed"})
    %{organization_id: org.id} |> IncinerateDue.new() |> Oban.insert!()
    ticket
  end
  test "old cancellation removes organization tickets comments and memberships" do
    user = user_fixture()
    o = org(31 * 86400, user)
    t = fill(o, user)
    assert :ok = sweep()
    assert Repo.get(Organization, o.id) == nil
    assert Repo.get(Ticket, t.id) == nil
    assert Repo.aggregate(Comment, :count) == 0
    assert Repo.aggregate(Membership, :count) == 0
  end
  test "all non cascading organization resources and stale search hits are erased" do
    user = user_fixture()
    o = org(31 * 86400, user)
    fill(o, user)
    sweep()
    for module <- [CleanupBoard, CleanupAsset, CleanupInvitation, CleanupEvent, CleanupSearch] do
      assert Repo.aggregate(module, :count) == 0
    end
  end
  test "exact thirty days recent cancellation and active organizations survive" do
    user = user_fixture()
    for age <- [30 * 86400, 29 * 86400] do
      o = org(age, user)
      t = fill(o, user)
      sweep()
      assert Repo.get(Organization, o.id)
      assert Repo.get(Ticket, t.id)
    end
    active = organization_fixture(user)
    fill(active, user)
    sweep()
    assert Repo.get(Organization, active.id).active
  end
  test "one second beyond deadline is due" do
    user = user_fixture()
    o = org(30 * 86400 + 1, user)
    sweep()
    assert Repo.get(Organization, o.id) == nil
  end
  test "restored organization is judged from current database state" do
    user = user_fixture()
    o = org(40 * 86400, user)
    fill(o, user)
    {:ok, restored} = AccountLifecycle.restore(o)
    sweep()
    assert Repo.get!(Organization, restored.id).active
    assert Repo.aggregate(CleanupSearch, :count) == 1
  end
  test "shared user and surviving tenant retain data and login tokens" do
    user = user_fixture()
    dying = org(31 * 86400, user)
    live = organization_fixture(user)
    fill(dying, user)
    kept = fill(live, user)
    token = Trackline.Accounts.generate_user_session_token(user)
    sweep()
    assert Repo.get(Ticket, kept.id)
    assert Support.get_membership(live, user)
    assert Trackline.Accounts.get_user_by_session_token(token)
    assert Repo.aggregate(CleanupSearch, :count) == 1
  end
  test "queued and completed work for deleted organization is removed only there" do
    user = user_fixture()
    dying = org(31 * 86400, user)
    live = organization_fixture(user)
    fill(dying, user)
    fill(live, user)
    completed = %{organization_id: dying.id} |> IncinerateDue.new() |> Oban.insert!()
    completed |> Ecto.Changeset.change(state: "completed") |> Repo.update!()
    sweep()
    jobs = Repo.all(Oban.Job)
    assert Enum.all?(jobs, &(&1.args["organization_id"] != dying.id))
    assert Enum.any?(jobs, &(&1.args["organization_id"] == live.id))
  end
  test "repeated sweep and empty sweep are harmless" do
    user = user_fixture()
    o = org(31 * 86400, user)
    fill(o, user)
    assert :ok = sweep()
    assert :ok = sweep()
    assert Repo.get(Organization, o.id) == nil
  end
  test "hourly recurring configuration names the worker" do
    # Read deployable configuration, rather than the test mode which disables plugins.
    previous = Application.fetch_env!(:trackline, Oban)
    on_exit(fn -> Application.put_env(:trackline, Oban, previous) end)
    # Evaluate runtime.exs too, using disposable grading values, without booting prod.
    env_keys = ["DATABASE_PATH", "SECRET_KEY_BASE"]
    saved_env = Enum.map(env_keys, &{&1, System.get_env(&1)})
    System.put_env("DATABASE_PATH", System.fetch_env!("TRACKLINE_DB"))
    System.put_env("SECRET_KEY_BASE", String.duplicate("grade-fixture-", 8))
    config = try do
      compile = Config.Reader.read!("config/config.exs", env: :prod, target: :host)
      runtime = Config.Reader.read!("config/runtime.exs", env: :prod, target: :host)
      Config.Reader.merge(compile, runtime)
    after
      for {key, value} <- saved_env do
        if value, do: System.put_env(key, value), else: System.delete_env(key)
      end
    end
    Application.put_env(:trackline, Oban, config[:trackline][Oban])
    effective = CleanupSchedule.oban_options()
      |> Keyword.put(:testing, :disabled)
      |> Oban.Config.new()
    # Oban itself normalizes service keys, legacy crontab and renamed plugins.
    cron = Enum.flat_map(effective.plugins, fn
      {Oban.Cron, options} -> Keyword.get(options, :crontab, [])
      _ -> []
    end)
    assert Enum.any?(cron, fn entry ->
      case entry do
        {expression, IncinerateDue} -> hourly?(expression)
        {expression, IncinerateDue, _options} -> hourly?(expression)
        _ -> false
      end
    end)
  end
  defp hourly?(expression) do
    # Parsed sets accept aliases, ranges/steps and any once-per-hour minute phase.
    case Oban.Cron.parse(expression) do
      {:ok, parsed} ->
        not parsed.reboot? and MapSet.size(parsed.minutes) == 1 and
          parsed.hours == MapSet.new(0..23) and parsed.days == MapSet.new(1..31) and
          parsed.months == MapSet.new(1..12) and parsed.weekdays == MapSet.new(0..6)
      _ -> false
    end
  end
end
