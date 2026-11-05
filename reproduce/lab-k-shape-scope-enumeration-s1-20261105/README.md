# A model-free scope inventory names every owner-keyed store the hidden checks touch, but the counted shaper cells were not run

Finding `lab-k-shape-scope-enumeration-s1-20261105`. Stage 1 of Lab `k-shape-scope-enumeration` (5 Nov 2026): the judge step is model-free; three one-cell dry runs used a model seat; the 18 counted Stage 1a cells did not start, so no arm is proven or refuted.

## Question

A request quantified over a set ("delete everything belonging to a cancelled account") is shaped from the model associations only, and stores keyed by the owner id are missed. Stage 0 showed a deterministic scan finds those stores in 0.1 s and 2.8 KB. Stage 1 asks (1) whether the stored inventories name every table that the hidden checks of the 13 application tasks touch, scored by a judge who did not write the scanner, and (2) whether three ways of getting the inventory to the shaper without a tool call (E1 prefetched into the first message, E2 the same text framed as an answered tool call, E3 review-side only) get the two known stores named in at least 4 of 6 valid Intents on the target task.

## Method

- Judge (model-free, no seat): for each task the judge list is the set of tables that exist in the task's start schema and that the hidden verification test touches (model constants resolved to tables, plus literal table names); the owner root table `accounts` is excluded. Each stored inventory is scored by the names it contains. Recall is reported over all hidden-touched tables and over the owner-keyed subset (the scanner's declared scope). The 26 Go kits have no schema, a 0-byte inventory and no list.
- Arms: one patch of kogen-shaping at the pin of release 41d70052, selected at link time; E1, E2, E3 as in the Lab design. The Go port of the scanner gives byte-identical inventories on all 13 trees.
- Dry cells (one per arm, target task, shape only, claude-sonnet-5-5 high, one Mac runner): run once each before the counted cells, never counted.
- Registered decision rule (unchanged): an arm is proven if stores are named in at least 4 of 6 valid Intents on the target and the hidden mean is at least the control plus 1/8 with sign p <= 0.0625, and on guards at most 1 of 12 valid-Intent pairs is lost with no new refusal class.

## Result

Judge (`data/judge-recall.tsv`, one row per task):

| Quantity | Value |
|---|---|
| Trees with an inventory | 13 |
| Hidden-touched tables / owner-keyed among them | 121 / 106 |
| Owner-keyed tables missed | 0 (recall 1.00 on 13 of 13 trees) |
| Recall over all hidden-touched tables | mean 0.94, min 0.75 |
| Missed tables, none owner-keyed | 14 (identity and session tables; on the target five filter join tables keyed one hop below `filters`) |
| Median inventory size | 2,781 bytes |

The judge gate passes: no owner-keyed store of a hidden list is missed, including the two known stores of the target task. The documented gap is that the scanner does not follow one-hop keys, so a package that must be complete over join tables could still miss them.

Dry cells (`data/dry-cells.tsv`), target task, one cell per arm:

| Arm | Outcome | Rounds | Wall | Requests | Client cost | Stores named |
|---|---|---|---|---|---|---|
| E1 | Intent saved | 7 | 2130 s | 66 | 2.15 USD | search records, storage entries, storage_totals |
| E2 | Intent saved | 4 | 1591 s | 52 | 1.79 USD | search_records, storage_entries, storage_totals |
| E3 | refused at round 3, draft saved | 3 | 1785 s | 64 | 1.82 USD | search_records, storage_entries |

E3's refusal listed 8 owner-keyed places the Intent neither named nor excluded; that is the scope review working, and it is also a refusal class the guards must watch. One cell per arm says nothing about rates.

Counted Stage 1a: 0 of 18 cells ran. The only account open to new work (the kogen seat) was refused by the admission gate from 16:20Z to 17:10Z (5h use 0.47 to 0.56 against a pace cap of 0.43 to 0.52, almost entirely delivery jobs), and the gap was not closing before the helper's time limit, so the three arms were not started. No other account was used.

## Verdict

**Unresolved.** The Stage 1 judge gate passes, and all three arms put both known stores into a saved Intent or draft in one dry cell each. The target gate (stores named in 4 of 6 valid Intents) and the guard bar are unmeasured, so no arm is proven and no REQUEST is filed.

## Limits

- The judge list is derived from hidden verification tests by a Rails naming heuristic; unresolved constants are ignored, so recall over all tables is an estimate. The 13 trees come from 2 base applications.
- Dry cells are single runs on a loaded host (27 to 36 minutes each); wall times include shaper retries.
- Model-free evidence does not show how often the shaper uses an inventory; that is the counted Stage 1a.

## Rerun

Offline, from the published data, with no model call and no checkout:

```
python3 -I report.py data
```

It recounts the judge table and the dry-cell table and checks every count against `replay.json`. The inventories, scanner and kogen-shaping patch pin are named by sha in `replay.json`; kogen sources are public in the KogenAI GitHub organization at commit 41d70052bf0ff932a0424df86a0fb388021428fc.
