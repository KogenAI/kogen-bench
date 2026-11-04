# Bounded shaping recovery confirmation stopped

**Verdict: unresolved; disposition: drop.** The candidate exhausted its invalid-submission allowance in both completed assignments, meeting the registered stop rule. Neither saved a valid Intent. The four remaining assignments, including both held-outs, did not run. One selected task ran out of its registered order because of a staging error. These observations do not establish whether the change improves overall task success.

| Assignment | Release draw 1 | Release draw 2 | Earlier candidate | Confirmation candidate |
|---|---|---|---|---|
| A | refused / no Intent / hidden fail | refused / no Intent / hidden fail | landed / Intent / hidden fail | refused / no Intent / hidden fail |
| B | environment / no Intent / hidden fail | refused / no Intent / hidden fail | refused / no Intent / hidden fail | refused / no Intent / hidden fail |

The same model and effort were used throughout. The release draws are stored comparisons, not concurrent controls. The recovery mechanism fired twice in each confirmation cell; both still exhausted invalid submissions. Both ended with a missing acceptance file, and B also generated an invalid blocked report. The proposed policy questions were rejected; no non-UX question was handed off. Acceptance separation was not measured.

The only changed stop against a release draw is B's environment stop to refusal. It is attributed to the shaping stage, where the patched recovery mechanism fired, but the cause of the difference remains uncertain. A's earlier candidate landing changed to refusal in confirmation; the mechanism fired there too, without proving cause. All other stop outcomes are concordant.

The two confirmation cells used 625,413 input tokens (540,288 cached) and 3,922 output tokens (804 reasoning, included in output). Their summed wall time was 169.902 seconds, including failed attempts. Subscription cost is unpriced and orchestration cost unknown. The earlier screen's costs are reported separately in its finding. The final cell result was written at 2026-11-04T07:03:45.070932087Z.

## Rerun

The release source is [Kogen at 41d70052](https://github.com/KogenAI/kogen/commit/41d70052bf0ff932a0424df86a0fb388021428fc), with [shaping at f04edcea](https://github.com/KogenAI/kogen-shaping/commit/f04edcea9896db525855a810bf6c0429b8494278) plus a bounded refusal-recovery research change. The change's SHA-256 was b14e448991620a5f246bd44eb02975a9712d13fd1556ca4ae575c08be604067a; the candidate archive was 309105f50f506f758427cdeed8469443cb66f644e558f2df8adcc8daaa10199c. The research change was uncommitted and cannot be reconstructed from these public commits alone. The live run used a candidate-only request-to-shape-to-build-to-review lane with one slot and a 3600-second per-cell deadline.

Recompute the published paired table from the retained measurements:

```sh
python3 report.py data/results.tsv
```

This command reproduces the analysis of the recorded cells. Exact live replay additionally requires the original research change, qualified task kits and hidden graders.
