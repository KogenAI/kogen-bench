defmodule Trackline.PortErasureTest do
  use Trackline.DataCase, async: false
  alias Trackline.{Repo, Accounts, Support}
  alias Trackline.Accounts.User
  alias Trackline.Support.{Ticket, Comment, Membership}
  alias Trackline.Ports.{Erasure, KnowledgeBook, KnowledgePage, KnowledgeAsset, KnowledgeGrant, KnowledgeSearch, PersonalNotice, SignIn}
  import Trackline.AccountsFixtures
  import Trackline.SupportFixtures
  defp book(user, public) do
    b = Repo.insert!(%KnowledgeBook{title: "Book #{System.unique_integer([:positive])}", author_id: user.id, byline: user.email, public: public})
    p = Repo.insert!(%KnowledgePage{book_id: b.id, body: "Still useful"})
    a = Repo.insert!(%KnowledgeAsset{page_id: p.id, bytes: <<1, 2, 3>>})
    Repo.insert!(%KnowledgeSearch{book_id: b.id, user_id: user.id, content: b.title <> " Still useful", author_label: user.email})
    {b, p, a}
  end
  test "active user's row memberships tokens and notices disappear" do
    u = user_fixture()
    organization_fixture(u)
    token = Accounts.generate_user_session_token(u)
    Repo.insert!(%PersonalNotice{user_id: u.id, body: "Private"})
    Repo.insert!(%KnowledgeSearch{user_id: u.id, content: "Private profile"})
    assert :ok = Erasure.erase(u)
    assert Repo.get(User, u.id) == nil
    assert Repo.aggregate(Membership, :count) == 0
    assert Accounts.get_user_by_session_token(token) == nil
    assert Repo.aggregate(PersonalNotice, :count) == 0
    assert Repo.aggregate(KnowledgeSearch, :count) == 0
  end
  test "private books pages assets and their indexes are deleted" do
    u = user_fixture()
    {b, p, a} = book(u, false)
    assert :ok = Erasure.erase(u)
    assert Repo.get(KnowledgeBook, b.id) == nil
    assert Repo.get(KnowledgePage, p.id) == nil
    assert Repo.get(KnowledgeAsset, a.id) == nil
    assert Repo.aggregate(KnowledgeSearch, :count) == 0
  end
  test "public books keep content and become Deleted author" do
    u = user_fixture()
    {b, p, a} = book(u, true)
    Erasure.erase(u)
    kept = Repo.get!(KnowledgeBook, b.id)
    assert kept.public
    assert kept.author_id == nil
    assert kept.byline == "Deleted author"
    assert Repo.get!(KnowledgePage, p.id).body == "Still useful"
    assert Repo.get!(KnowledgeAsset, a.id).bytes == <<1, 2, 3>>
  end
  test "public search remains usable without erased author identity" do
    u = user_fixture()
    {b, _, _} = book(u, true)
    Erasure.erase(u)
    hit = Repo.get_by!(KnowledgeSearch, book_id: b.id)
    assert hit.content =~ b.title
    assert hit.user_id == nil
    assert hit.author_label == "Deleted author"
  end
  test "authored tickets and comments disappear and others' assignments detach" do
    u = user_fixture()
    other = user_fixture()
    org = organization_fixture(other)
    Support.add_member(org, u, "agent")
    owned = ticket_fixture(org, u)
    kept = ticket_fixture(org, other)
    {:ok, kept} = Support.assign_ticket(kept, u)
    authored = comment_fixture(kept, u)
    theirs = comment_fixture(kept, other)
    Erasure.erase(u)
    assert Repo.get(Ticket, owned.id) == nil
    assert Repo.get(Comment, authored.id) == nil
    assert Repo.get(Comment, theirs.id)
    assert Repo.get!(Ticket, kept.id).assignee_id == nil
  end
  test "old deactivated user's original and rewritten address logs disappear" do
    u = user_fixture()
    original = u.email
    {:ok, removed} = Erasure.deactivate(u)
    Repo.insert!(%SignIn{email: original})
    Repo.insert!(%SignIn{email: String.upcase(original)})
    Repo.insert!(%SignIn{email: removed.email})
    Repo.insert!(%SignIn{user_id: removed.id, email: "past-address@example.com"})
    Erasure.erase(removed)
    assert Repo.get(User, removed.id) == nil
    assert Repo.aggregate(SignIn, :count) == 0
  end
  test "email lookalikes and unrelated users survive" do
    u = user_fixture(%{email: "alice@example.com"})
    other = user_fixture(%{email: "alice-other@example.com"})
    {:ok, removed} = Erasure.deactivate(u)
    log = Repo.insert!(%SignIn{email: other.email})
    {b, p, _} = book(other, false)
    Erasure.erase(removed)
    assert Repo.get(User, other.id)
    assert Repo.get(SignIn, log.id)
    assert Repo.get(KnowledgeBook, b.id)
    assert Repo.get(KnowledgePage, p.id)
  end
  test "access grants are cleaned without denying surviving public-book readers" do
    u = user_fixture()
    reader = user_fixture()
    {public, _, _} = book(u, true)
    {private, _, _} = book(u, false)
    {other, _, _} = book(reader, false)
    kept = Repo.insert!(%KnowledgeGrant{book_id: public.id, user_id: reader.id})
    Repo.insert!(%KnowledgeGrant{book_id: private.id, user_id: reader.id})
    Repo.insert!(%KnowledgeGrant{book_id: other.id, user_id: u.id})
    Erasure.erase(u)
    assert Repo.get(KnowledgeGrant, kept.id)
    assert Repo.aggregate(KnowledgeGrant, :count) == 1
  end
  test "stale pre-deactivation struct and repeated erasure are safe" do
    u = user_fixture()
    {b, _, _} = book(u, false)
    Erasure.deactivate(u)
    assert :ok = Erasure.erase(u)
    assert :ok = Erasure.erase(u)
    assert Repo.get(User, u.id) == nil
    assert Repo.get(KnowledgeBook, b.id) == nil
  end
  test "active address containing deactivated is treated as a real address" do
    original = "person@example.com"
    natural = "person-deactivated-12345678-1234-1234-1234-123456789abc@example.com"
    u = user_fixture(%{email: natural})
    log = Repo.insert!(%SignIn{email: original})
    Repo.insert!(%SignIn{email: natural})
    Erasure.erase(u)
    assert Repo.get(SignIn, log.id)
    assert Repo.aggregate(SignIn, :count) == 1
  end
end
