import sys
ws=sys.argv[1]
# Wrong: fixes the LiveView but leaves the export endpoint trusting any id.
p=ws+"/lib/trackline_web/controllers/ticket_export_controller.ex"
s=open(p).read()
s=s.replace("case Support.get_ticket(org, id) do","case Support.get_ticket!(id) do")
open(p,"w").write(s)
