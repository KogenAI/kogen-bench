import sys, re
ws = sys.argv[1]
def edit(path, old, new, count=1):
    p = f"{ws}/{path}"; s = open(p).read()
    assert old in s, f"missing in {path}: {old[:60]!r}"
    open(p, "w").write(s.replace(old, new, count))

# --- context: filters
edit("lib/trackline/support.ex",
"""  def list_tickets(%Organization{id: org_id}) do
    Ticket
    |> where([t], t.organization_id == ^org_id)
""",
"""  def list_tickets(%Organization{id: org_id}, filters \\\\ %{}) do
    Ticket
    |> where([t], t.organization_id == ^org_id)
    |> filter_by(:status, filters[:status])
    |> filter_by(:priority, filters[:priority])
""")
edit("lib/trackline/support.ex",
"""  defp load_summary(ticket) do""",
"""  defp filter_by(query, _field, nil), do: query
  defp filter_by(query, field, value), do: where(query, [t], field(t, ^field) == ^value)

  defp load_summary(ticket) do""")

# --- live view
idx = "lib/trackline_web/live/ticket_live/index.ex"
edit(idx, """  def handle_params(_params, _uri, socket) do
    {:noreply, assign(socket, :tickets, Support.list_tickets(socket.assigns.org))}
  end
""", """  def handle_params(params, _uri, socket) do
    filters = %{
      status: valid(params["status"], Ticket.statuses()),
      priority: valid(params["priority"], Ticket.priorities())
    }

    {:noreply,
     socket
     |> assign(:filters, filters)
     |> assign(
       :filter_form,
       to_form(%{"status" => filters.status || "", "priority" => filters.priority || ""})
     )
     |> assign(:tickets, Support.list_tickets(socket.assigns.org, filters))}
  end

  defp valid(value, allowed), do: if(value in allowed, do: value)
""")
edit(idx, """  def handle_event("create_ticket", %{"ticket" => params}, socket) do""",
"""  def handle_event("filter", params, socket) do
    query =
      params
      |> Map.take(["status", "priority"])
      |> Enum.reject(fn {_k, v} -> v in [nil, ""] end)

    path = ~p"/orgs/#{socket.assigns.org.slug}/tickets"
    path = if query == [], do: path, else: path <> "?" <> URI.encode_query(query)
    {:noreply, push_patch(socket, to: path)}
  end

  def handle_event("create_ticket", %{"ticket" => params}, socket) do""")
edit(idx, """         |> assign(:tickets, Support.list_tickets(socket.assigns.org))
         |> assign(:form""", """         |> assign(:tickets, Support.list_tickets(socket.assigns.org, socket.assigns.filters))
         |> assign(:form""")
edit(idx, """      <table id="tickets" class="table mt-6">""", """      <.form for={@filter_form} id="ticket-filters" phx-change="filter" class="mt-4 flex gap-4">
        <.input
          field={@filter_form[:status]}
          type="select"
          label="Status"
          prompt="Any"
          options={Ticket.statuses()}
        />
        <.input
          field={@filter_form[:priority]}
          type="select"
          label="Priority"
          prompt="Any"
          options={Ticket.priorities()}
        />
      </.form>

      <table id="tickets" class="table mt-6">""")
