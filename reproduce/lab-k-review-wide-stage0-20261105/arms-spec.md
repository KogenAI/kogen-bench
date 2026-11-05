# Arms as modelled in replay.py (request text of each arm)

Common: stable text 103,824 B (authority, task, constraints; fitted), check results 2,500 B (assumed), part header of `reviewPartHeader`, ceiling 524,288 B inclusive, `MaterialPartBytes` 6,000 B.

- R0 (kogen-review b33665f): every part carries `# Every changed path` with the complete catalog line (`json.Marshal(m.Files)`), the checks, and its slice; changed files' full text is not in the source (7a9fac6). Stops if the mandatory prompt leaves less than 6,000 B for source.
- R1: R0 plus `# Digest of earlier parts`, 3,000 B, in every part after the first.
- R2 (on_demand as a lane patch): one session; first prompt = stable + checks + catalog + hunk manifest + required part list; then one ranged read per 6,000 B pinned part (or per 64 KB for R2-b64k), each re-sending the context; 300 B envelope per read (assumed).
- R3: R0 with the catalog replaced by the slice's entries in full and every other path as `{"path","status"}`.
- R0' (4c421b7, unlanded): a catalog longer than 6,000 B is not repeated: the slice's entries in full, then a line giving the number of other paths and the retained catalog file; a catalog of 6,000 B or less is as R0.
