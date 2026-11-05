# Approve: batched step-binding check and a single approve call (Lab E1)

Since Kogen release 41d70052, `kogen intent approve` checks step-binding ownership before readiness. For every other Intent, every pair of own and other step file, and every step text of both Intents, it starts one Node + Cucumber loader process. The delivery launcher calls approve twice per Build. This model-free Lab experiment compared four arms on frozen copies of real shaped trees on the Studio Mac (kogen-runner), with no model calls:

- **A**: release [d98cfe01](https://github.com/KogenAI/kogen/tree/d98cfe018ef5717de8e67d91fb39f91f997bea9e) approve as the launcher runs it (preview for the digest, then approve).
- **B**: the same release with the check batched, one loader per (own file, other file) pair returning per-text matches. Pairs, order and the collision rule are unchanged. The patch is `patches/e1-batch-bindingcollision.diff` against [kogen-shaping f04edce](https://github.com/KogenAI/kogen-shaping/tree/f04edcea9896) `shape/stepownership.go`.
- **C**: A with one approve call.
- **B+C**: both.

**Result: B passes; C does not.**

- **B, speed:** batching cut approve wall time by 91.9–96.3% on all 7 shaped trees that ran both A and B: 3 Studio, 1 kogen, loop, setup, shaping. Pooled over those trees it fell from 16,360 s to 1,093 s (−93.3%). Examples:
  - Studio trees: 2,772–3,330 s down to 199–242 s.
  - The kogen tree with 147 Intents: 3,563 s down to 203 s.
  - The two-worktree pair: −91.6% and −95.9%.
  - Negative controls: −96.7% to −98.6%.
- **B, verdicts:** the step-binding verdict was identical to A on 12/12 fixtures, and all 3 synthetic collisions were refused with byte-identical `intent/step_ownership_collision` text in A, B and B+C.
- **B, final verdicts:** identical on 9/12 fixtures. The 3 differences are the Studio trees, where readiness's acceptance step timed out after 120 s (`environment/step_timeout`) at host load 60–170. It timed out in A on all 3 and in B on 2 of 3. That stage is readiness, which the patch does not change.
- **C:** one call cut approve by −10% to 57% (median 39%, ≥45% on 1 of 4 trees). It saves nothing when the first call already refuses (collisions, readiness timeouts). It also needs a digest the launcher does not have: d98cfe01's shape prints no SHA-256 line, and shape's package record is stale by approval time (on these trees it lacked `.kogen/models.yaml`, and the launcher rewrites `.kogen/project.yaml` after shaping). C here used a Lab helper that computes the release's own package digest. On top of B, a single call saved a further 15–40% (for example 25 → 18 s and 203 → 174 s).

Per fixture (A n=1; B, C, B+C up to 3 reps; wall seconds; cut against A):

| fixture | kind | A s (n=1) | B median s (n) | C median s (n) | B+C median s (n) | cut B / C / B+C | outcome A / B / C / B+C | binding verdict identical B/C/B+C | final identical B/C/B+C |
|---|---|---|---|---|---|---|---|---|---|
| s-bulk-import | studio | 3330.4 | 237.9 (3) | None (0) | 229.3 (3) | 92.9% / None% / 93.1% | environment/step_timeout / environment/step_timeout / - / environment/step_timeout | yes/-/yes | **NO**/-/**NO** |
| s-long-reports | studio | 2771.5 | 225.1 (1) | 3057.4 (1) | 148.9 (1) | 91.9% / -10.3% / 94.6% | environment/step_timeout / approved / approved / approved | yes/yes/yes | **NO**/**NO**/**NO** |
| s-record-relations | studio | 3004.6 | 237.5 (3) | None (0) | 239.7 (3) | 92.1% / None% / 92.0% | environment/step_timeout / environment/step_timeout / - / environment/step_timeout | yes/-/yes | **NO**/-/**NO** |
| k-integrate-pins-20261105t082752z | kogen | 3563.2 | 202.8 (3) | None (0) | 174.3 (3) | 94.3% / None% / 95.1% | approved / approved / - / approved | yes/-/yes | yes/-/yes |
| k-setup-initialized-reports-bootstrap-setup | kogen-setup | 679.0 | 25.4 (3) | 430.2 (2) | 18.2 (3) | 96.3% / 36.6% / 97.3% | approved / approved / approved / approved | yes/yes/yes | yes/yes/yes |
| neg1-setup | negative | 181.9 | 5.2 (3) | 197.3 (3) | 5.4 (3) | 97.1% / -8.5% / 97.0% | intent/step_ownership_collision / intent/step_ownership_collision / intent/step_ownership_collision / intent/step_ownership_collision | yes/yes/yes | yes/yes/yes |
| k-shape-scope-enumeration | kogen-shaping | 1659.9 | 62.9 (2) | 707.1 (1) | 37.8 (3) | 96.2% / 57.4% / 97.7% | approved / approved / approved / approved | yes/yes/yes | yes/yes/yes |
| neg2-review | negative | 374.7 | 5.2 (1) | None (0) | 5.3 (1) | 98.6% / None% / 98.6% | intent/step_ownership_collision / intent/step_ownership_collision / - / intent/step_ownership_collision | yes/-/yes | yes/-/yes |
| neg3-verification | negative | 85.2 | 2.8 (1) | None (0) | 2.9 (1) | 96.7% / None% / 96.6% | intent/step_ownership_collision / intent/step_ownership_collision / - / intent/step_ownership_collision | yes/-/yes | yes/-/yes |
| wt1-verification | worktree | 1777.3 | 72.6 (1) | None (0) | 44.4 (1) | 95.9% / None% / 97.5% | approved / approved / - / approved | yes/-/yes | yes/-/yes |
| wt2-verification | worktree | 916.0 | 77.2 (1) | 426.8 (1) | 62.5 (1) | 91.6% / 53.4% / 93.2% | approved / approved / approved / approved | yes/yes/yes | yes/yes/yes |
| l-credential-lock-wait-backoff | loop | 1351.1 | 101.7 (1) | 793.3 (1) | 73.2 (1) | 92.5% / 41.3% / 94.6% | approved / approved / approved / approved | yes/yes/yes | yes/yes/yes |

## Deviations from the registered design
- **Fewer runs than registered:** the 2.5-hour cap, a host shared with delivery Builds (load 20–170 on 10 cores) and one C call on a Studio tree costing about 50 minutes cut the reps. C ran on 6 fixtures, mostly n=1. The kogen-build and kogen-verification trees got arm A only (kept as A timings). The rebuilt second kogen tree was dropped, because without a readiness cache its approve would have run the kogen acceptance outside the host test lock.
- **Stopped runs:** two Studio C runs were stopped by me when the host was saturated; they are excluded (marked `killed`).
- **Reconstructed runs:** I overwrote the measuring script while three Studio A runs were reading it. Those shells died after approve finished, so their wall time is reconstructed from file times (to the second); their verdict text is complete. One C run died the same way and is excluded.
- **Uneven load:** A ran once at the load it met; arms were interleaved per tree.

## Rerun
Data: `data/results.json` (every run: arm, rep, wall, per-call time, load, normalized verdict text). `python3 report.py` recomputes the summary.

To rerun on a Mac with Kogen d98cfe01 installed:
1. Clone kogen at d98cfe01 and kogen-shaping at f04edce, and apply `patches/e1-batch-bindingcollision.diff` to kogen-shaping.
2. In `kogen/cli`, run `go mod edit -replace github.com/KogenAI/kogen-shaping=<patched dir>`, then `CGO_ENABLED=0 go build -trimpath -buildvcs=false`. The same build without the replace reproduces the release binary byte for byte (sha256 7dc55c5b…); the patched binary is f5c6f858….
3. Copy any shaped Intent tree and time `kogen intent approve <slug>` (preview, then with the digest) with each binary. `data/run1.sh` is the per-run script and `data/mkneg.py` makes a negative control.

Fixtures were delivery's kept shaped trees from 4–5 Nov (repositories public at those commits).
