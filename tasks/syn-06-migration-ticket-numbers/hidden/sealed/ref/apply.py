import sys
ws = sys.argv[1]
def edit(path, old, new):
    p = f"{ws}/{path}"; s = open(p).read()
    assert old in s, f"missing in {path}: {old[:60]!r}"
    open(p, "w").write(s.replace(old, new, 1))

edit("lib/trackline/support/ticket.ex", """    field :priority, :string, default: "normal"
""", """    field :priority, :string, default: "normal"
    field :number, :integer
""")
edit("lib/trackline/support.ex", """    %Ticket{organization_id: org_id, author_id: author_id}
    |> Ticket.changeset(attrs)
    |> Repo.insert()
  end
""", """    changeset = Ticket.changeset(%Ticket{organization_id: org_id, author_id: author_id}, attrs)

    Repo.transact(fn ->
      if changeset.valid? do
        next =
          Repo.one(from t in Ticket, where: t.organization_id == ^org_id, select: max(t.number)) || 0

        changeset |> Ecto.Changeset.put_change(:number, next + 1) |> Repo.insert()
      else
        {:error, %{changeset | action: :insert}}
      end
    end)
  end
""")
edit("lib/trackline_web/live/ticket_live/index.ex", """                {ticket.title}
""", """                #{ticket.number} {ticket.title}
""")
edit("lib/trackline_web/live/ticket_live/show.ex", """        {@ticket.title}
        <:subtitle>""", """        #{@ticket.number} {@ticket.title}
        <:subtitle>""")
edit("lib/trackline_web/controllers/ticket_export_controller.ex", """      id: ticket.id,
""", """      id: ticket.id,
      number: ticket.number,
""")
