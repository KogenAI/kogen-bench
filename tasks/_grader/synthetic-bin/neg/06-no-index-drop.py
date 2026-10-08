import sys,glob
ws=sys.argv[1]
# Wrong: rollback removes the column without dropping the unique index first (SQLite refuses).
p=glob.glob(ws+"/priv/repo/migrations/*add_ticket_numbers.exs")[0]
s=open(p).read()
s=s.replace("    drop unique_index(:tickets, [:organization_id, :number])\n","")
open(p,"w").write(s)
