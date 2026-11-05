#!/usr/bin/env python3
"""python3 -I report.py data : recount the judge table and the dry-cell table, check against replay.json."""
import csv, json, os, sys
d = sys.argv[1]; here = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(d, "judge-recall.tsv")), delimiter="\t"))
dry = list(csv.DictReader(open(os.path.join(d, "dry-cells.tsv")), delimiter="\t"))
c = {
 "trees_with_inventory": len(rows),
 "owner_keyed_missed": sum(int(r["missed_owner_keyed"]) for r in rows),
 "trees_owner_keyed_recall_1": sum(1 for r in rows if float(r["recall_owner_keyed"]) == 1.0),
 "hidden_touched_tables": sum(int(r["hidden_touched_tables"]) for r in rows),
 "hidden_touched_owner_keyed": sum(int(r["hidden_touched_owner_keyed"]) for r in rows),
 "missed_not_owner_keyed": sum(int(r["missed_not_owner_keyed"]) for r in rows),
 "inventory_bytes_median": sorted(int(r["inventory_bytes"]) for r in rows)[len(rows) // 2],
 "dry_cells": len(dry),
}
print(json.dumps(c, indent=1))
print("min all-table recall %.3f; mean %.3f" % (min(float(r["recall_all"]) for r in rows), sum(float(r["recall_all"]) for r in rows) / len(rows)))
rp = json.load(open(os.path.join(here, "replay.json")))["arms"]["judge"]["counts"]
bad = [k for k in c if rp.get(k) != c[k]]
print("replay.json counts match" if not bad else "MISMATCH: " + ", ".join(bad)); sys.exit(1 if bad else 0)
