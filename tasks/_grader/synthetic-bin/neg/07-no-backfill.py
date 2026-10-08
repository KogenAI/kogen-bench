import sys,glob
ws=sys.argv[1]
p=glob.glob(ws+"/priv/repo/migrations/*closed_at*.exs")[0]
s=open(p).read()
s=s.replace('    execute "UPDATE tickets SET closed_at = updated_at WHERE status = \'closed\'"\n',"")
open(p,"w").write(s)
