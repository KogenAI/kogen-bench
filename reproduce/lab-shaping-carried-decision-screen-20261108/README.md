# Guidance for carrying shaping decisions

On ten small requests, the stored release reached 6 ready Intents and a candidate reached 7. Three cases changed from not ready to ready and two from ready to not ready. Two unpatched repetitions reached 6 and 7, with two and three paired flips respectively. The candidate was dropped because its regressions fail the registered rule. No questions were asked. This is a screen, not a qualified delivery change.

All five discordances occurred in shaping; their cause remains unclear because run-to-run variation is also observed. One regression ended at an evidence-format refusal before the carried-decision check; the other ended at an acceptance-step self-check. One gain recovered after decision and readiness refusals; the other two recovered after decision checks where the stored release had ended at evidence checks. No carried-decision line was observed in the candidate terminal Intent files, so instruction firing is unproven. The decision, evidence and readiness gates were unchanged.

The candidate instructed the shaper how to carry each newly recorded decision into the Intent of the same submission, preserving the exact fields required by the existing check. Both arms used the same model, low effort and no answerer; the control was stored. Times include failed attempts. The shared credit balance did not move visibly; attributable spend is unknown. No held-out or complex requests, Build stage or hidden checks ran; landing and hidden outcomes are unmeasured. Small Go and Node workspaces were reconstructed; byte identity with the earlier study is unverified.

The release uses [Kogen source](https://github.com/KogenAI/kogen/tree/47236bbb93385bc960fd2ac353c9b000bd6ed571) and [shaping source](https://github.com/KogenAI/kogen-shaping/tree/0484edf817f6dc74f691f44d5234cf7f6ae0435e). The candidate adds only the instruction described above.

## Rerun

Run `python3 report.py` to reproduce paired counts. To repeat the model screen, use the [small-request setup](../lab-shaping-small-requests-20261107/README.md), pinned release and same ten requests; add the described carried-decision instruction, keep all gates, and shape each request with the same model, low effort and no answerer. Record readiness, questions, refusal causes and elapsed time.
