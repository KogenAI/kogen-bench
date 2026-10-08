import sys
ws = sys.argv[1]
def edit(path, old, new):
    p = f"{ws}/{path}"; s = open(p).read()
    assert old in s, f"missing in {path}: {old[:60]!r}"
    open(p, "w").write(s.replace(old, new, 1))

edit("lib/trackline/support.ex", """  def get_ticket!(id),
""", """  @doc "Fetches a ticket by id, but only if it belongs to `org`."
  def get_ticket(%Organization{id: org_id}, id) do
    with {:ok, id} <- Ecto.Type.cast(:id, id),
         %Ticket{} = ticket <- Repo.get_by(Ticket, id: id, organization_id: org_id) do
      Repo.preload(ticket, [:organization, :author, :assignee])
    else
      _ -> nil
    end
  end

  def get_ticket!(id),
""")

edit("lib/trackline_web/live/ticket_live/show.ex", """    with %{} = org <- Support.get_organization_by_slug(slug),
         %{} = membership <- Support.get_membership(org, user) do
      ticket = Support.get_ticket!(id)
""", """    with %{} = org <- Support.get_organization_by_slug(slug),
         %{} = membership <- Support.get_membership(org, user),
         %{} = ticket <- Support.get_ticket(org, id) do
""")

