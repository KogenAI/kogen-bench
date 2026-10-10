# Harness archive

The files at this directory's top level come from the frozen harness. `DECISION-RULE-A1.md` comes from the resume-fix package. `amendment-A1/` contains that package's scripts and accelerated scoring helpers. `run-versions/` contains top-level scripts, briefs and configuration from each supplied host/wave copy. It excludes arm repositories, snapshots, templates, toolchain caches, account/auth files and agent logs.

Paths and hostnames are sanitized. A literal `~` in a quoted string does not expand like the original absolute path; these are inspectable historical scripts, not a turnkey runnable installation. Race-time `arm.sh`/`arm-cont.sh` copies match across all four w2/w3 runs. All six scoring-script copies contain the later subset-validation fix. No frozen scorer or input is executed by the bundle builder.

The original rule's three-hour cap, four-run schedule and every-FINAL/band-repeat requirements are preserved for accountability. A1 invalidates w1 and proposed later starts; actual sprint starts/caps and incomplete scoring are documented in the main README and TIMELINE. Original checksum pins describe source bytes; exported checksum pins are in the bundle manifests.

`COUNTS.txt`, `SPEC-BUG-CASES.txt`, `TARGET.md`, `EXCLUDED-V2.txt`, `CASE-INVENTORY.txt` and `SCORED-56.tsv` define the same frozen 144/88/56 inventory and target 50. `score-arm.sh`, `validate-results.py`, `scoring_config.py`, `kg-wrap.py` and `sweep.sh` expose the scoring mechanics. The archived scripts can refer to omitted external kits/trees; those were not authorized public arm artifacts.
