import sys
ws = sys.argv[1]
def edit(path, old, new):
    p = f"{ws}/{path}"; s = open(p).read()
    assert old in s, f"missing in {path}: {old[:60]!r}"
    open(p, "w").write(s.replace(old, new, 1))

edit("lib/trackline_web/router.ex", """    get "/orgs/:slug/tickets/:id/export.json",""", """    post "/orgs/:slug/tickets/import", TicketImportController, :create
    get "/orgs/:slug/tickets/:id/export.json",""")
edit("lib/trackline/support/ticket.ex", """    field :priority, :string, default: "normal"
""", """    field :priority, :string, default: "normal"
    field :external_id, :string
""")
edit("lib/trackline/support.ex", """  def change_ticket(""", '''  @doc """
  Imports tickets from CSV text (see `Trackline.Support.TicketImport`).
  """
  def import_tickets(%Organization{} = org, %User{} = user, csv),
    do: Trackline.Support.TicketImport.run(org, user, csv)

  def change_ticket(''')
