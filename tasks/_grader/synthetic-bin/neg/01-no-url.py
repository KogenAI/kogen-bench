import sys
ws=sys.argv[1]
# Wrong: filters via assigns only; the URL never changes.
p=ws+"/lib/trackline_web/live/ticket_live/index.ex"
s=open(p).read()
s=s.replace("{:noreply, push_patch(socket, to: path)}","""f = %{status: valid(params["status"], Ticket.statuses()), priority: valid(params["priority"], Ticket.priorities())}
    {:noreply, socket |> assign(:filters, f) |> assign(:tickets, Support.list_tickets(socket.assigns.org, f))}""")
open(p,"w").write(s)
