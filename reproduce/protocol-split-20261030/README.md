# protocol-split-20261030

A protocol rule, not a measurement. There are no runs, no `runs.csv` and no analysis script in this pack. 30 October 2026, study revision 28.

## The rule

> Loop-versus-Codex wall time and cost are measured only on the two Linux benchmark hosts, one run at a time, with the tools interleaved per task. The two Macs measure Kogen against the other tool used alone, on hard tasks, by success rate. No wall-time claim is made from the Macs.

Source: the finding's ledger entry (`protocol-split-20261030`, "study rev 28"), made by the research owner relaying the repository owner's rulings of 30 October. The text of revision 28 itself was not available when this pack was written, so the wording above is the ledger entry's, with internal host and run names replaced by plain terms; the two follow-on rulings quoted below come from the research notes of the rounds that implemented it.

## Why the rule exists

On the morning of 30 October the loop-versus-Codex wall comparisons on the Macs could not be interpreted:

- loop's measured output rate on the Macs' subscription route fell from about 110 to about 48 tokens/s at about 04:00 UTC with the same loop binary, tasks and output tokens, while Codex's wall on the same tasks moved about 1–10% ([`reproduce/loop-sub-route-throughput/`](../loop-sub-route-throughput/)). The cause was not found; a later same-host test saw all three routes at 40–43 tokens/s in the afternoon, so the earlier gap is a time-of-day or provider-state effect that cannot be separated from the tools on the Macs ([`reproduce/loop-sub-route-throughput/superseding-same-host-test/`](../loop-sub-route-throughput/superseding-same-host-test/)).
- the Macs also run other benchmark and delivery work on the same machine, with logged overlap windows (29 October 19:31–20:12 UTC and 21:26–21:28 UTC, 30 October 04:28–04:31 UTC) and two reboots that cut runs short.
- the tonight-only subscription rounds were therefore labelled route-confounded and their wall gaps were not to be read as loop-versus-Codex differences ([`reproduce/morning-report-20261030/`](../morning-report-20261030/), section on the provider throughput regime change).

Wall time compared across tools needs both tools to see the same host load and provider state. Interleaving per task on a host that runs nothing else gives that; the Macs cannot.

## What it changes in later rounds

1. **Wall and cost comparisons** go on the Linux hosts only, with `--slots 1` (strictly one run at a time) and an interleaved order. The Claude Code round that followed (Kogen driving Claude Code against Claude Code alone, same model and effort in both) registered exactly this: one batch per round, `"order": "alternate"` so that for each task both tools run back to back and the tool that goes first alternates by task index, one repetition, 24 tasks, a stalled-npm fault test before launch, and the host reserved for the round.
2. **Mac rounds** report success rate on hard tasks only. The Mac programme that followed ran the same Kogen-driving-Claude-Code against Claude Code-alone comparison on a hard-task set at the same model and effort in both tools (Sonnet 5.5 medium first, then Opus 5.5 high), one repetition per task and tool, with "no wall-time claim" written into the registration.
3. **Findings from before the split** (the 29–30 October loop-versus-Codex subscription rounds) keep their route and time labels; they are not pooled across the 04:00 UTC change and their wall gaps are not quoted as tool differences.
4. Same-tool comparisons inside one period on one host (patch against baseline) are unaffected, because both sides share the host and route.

## What it does not change

It does not say the Macs' timings are wrong, and it does not stop Mac rounds from measuring success rate, or from comparing a patch against its own baseline on the same Mac (item 4). It limits which machines may support loop-versus-Codex claims about wall time and cost.

## Rerun

Nothing to run. To check a later round against the rule, confirm for its registration that: the host is one of the two Linux hosts for any wall or cost claim; the order is interleaved per task with one run at a time; and that Mac rounds publish success rates only.
