import csv,sys
with open(sys.argv[1],newline='') as f:
 rows=list(csv.DictReader(f,delimiter='\t'))
assert len(rows)==8
for r in rows:
 print('{task}\t{cohort}\t{outcome}\t{intent}\t{hidden_all_pass}\t{wall_s}'.format(**r))
