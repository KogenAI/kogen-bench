import sys,glob
ws=sys.argv[1]
# Wrong: numbers by internal id instead of creation time (ignores inserted_at ordering).
p=glob.glob(ws+"/priv/repo/migrations/*add_ticket_numbers.exs")[0]
s=open(p).read()
s=s.replace("""AND (t2.inserted_at < tickets.inserted_at
             OR (t2.inserted_at = tickets.inserted_at AND t2.id <= tickets.id))""","AND t2.id <= tickets.id")
open(p,"w").write(s)
