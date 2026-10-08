import sys
ws=sys.argv[1]
# Wrong: preloads in one query but still counts comments per ticket.
p=ws+"/lib/trackline/support.ex"
s=open(p).read()
s=s.replace("    |> put_comment_counts()\n","    |> Enum.map(&%{&1 | comment_count: comment_count(&1)})\n")
open(p,"w").write(s)
