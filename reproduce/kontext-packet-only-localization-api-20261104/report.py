import json,statistics as st,sys
R=[json.loads(l) for l in open(sys.argv[1])]
for a in "AB":
    X=[r for r in R if r["arm"]==a and "error" not in r]
    print(a,len(X),"recall",round(st.mean(r["recall"] for r in X),3),"precision",round(st.mean(r["precision"] for r in X),3),"first_hit",sum(r["first_hit"] for r in X),"mean_input_tokens",round(st.mean(r["usage"]["input"] for r in X)),"cost",round(sum(r["cost"] for r in X),4))
