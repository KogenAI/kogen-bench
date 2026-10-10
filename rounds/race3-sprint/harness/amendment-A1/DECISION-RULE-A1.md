# Race 3 decision rule — amendment A1

This amendment applies together with the frozen DECISION-RULE.md, SHA-256 `b0f2cac829a938c3ce48c7e09f3d9e3d07f6a882f30a24fe9ffd6bcd6d1505d7`.

Wave 1 (original runs A+B, started 10:10Z) is invalid as a registered run because the resume fix changed the harness mid-race (see INCIDENT.md). It will be scored and published as descriptive only, with the incident note. Lost windows are reported only with those descriptive results.

The four registered runs are wave 2 (MacBook + Studio, start 13:20:00Z) and wave 3 (MacBook + Studio, start 16:30:00Z). Both waves use the same fixed arm.sh and arm-cont.sh from turn 0. Run A = wave 2 MacBook; run B = wave 2 Studio; run C = wave 3 MacBook; run D = wave 3 Studio.

Everything else in DECISION-RULE.md is unchanged: target 50/56, median over four runs, the ≥ 3 of 4 winner rule, scoring and invalidation.

Disclosures: the resume bug and stall-regex bug were fixed before wave 2; the false quota alert is retracted; the fast-fail alert guard with exponential backoff was added before the registered waves.
