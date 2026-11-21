# Measurements — h23-release-bbf56fdc-vs-891c91b3

Question: See [README.md](README.md). The scored unit is an exact slot (arm, task, repetition) of the h23 retained execution diagnostic. The records use only the retained [cells.json](cells.json).

Required measures: retained slot outcome and numeric score where one exists, terminal state, wall seconds, venue alias, and the resolved role models where captured.

Coverage: 15 Standard 1.2 records, one per new attempt; 10 carry a numeric score and 5 do not. The three reused baseline slots remain in the source study `h14-release-891c91b3-vs-30cf6619` and are not duplicated here. Every record uses the same Standard fields; the all-planned denominator beyond these slots is not inferred from them.

Coverage counts: 15 Standard records; 1725 explicitly missing scalar capture slots across the records. Exact paths, reasons and impact are in [MISSING.md](MISSING.md).

Verdict impact: Explicit receipt gaps limit protocol compliance and measurement completeness. The retained scores, denominators and wall values are unchanged. Raw transcripts, token totals, account meters, credentials and real host identities are not published.
