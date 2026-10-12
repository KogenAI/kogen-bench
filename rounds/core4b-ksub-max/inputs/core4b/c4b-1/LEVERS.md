# Difficulty notes

Target: 40–60% pilot pass rate, estimated 45–75 minutes for a strong agent.
These are design targets, not measured results. No contestant pilot is authorized
in this author job.

Hardness comes from the interaction of six modules: strict manifest validation,
ordered DAG scheduling, immutable input snapshots, durable state/event receipts,
a surviving process-tree guardian, and generation-based CAS publication. The
same crash boundary must preserve completed output bytes, avoid a duplicate
journal event, and recover a landed generation before rechecking inputs. Session
escape means ordinary process-group cleanup is insufficient. Output prefix
replacement must preserve unrelated target files and leave old views immutable.

Ways to raise difficulty after accepted pilot evidence:

1. Add bounded parallel ready-step execution with a specified deterministic event
   merge order and per-step fences.
2. Introduce cancellation with durable reasons, including cancellation racing the
   target switch and supervisor shutdown.
3. Permit multiple target namespaces and optimistic concurrent landing against
   both input hashes and a generation token.
4. Add recovery from a deliberately truncated journal tail with checksummed
   records, while distinguishing corruption of committed records.
5. Add content-addressed output receipts and verify stored bytes on resume,
   detecting external workspace modification before landing.

If too hard, relax these constraints in sequence: forbid descendants from changing session/group;
remove after_launch and arbitrary mid-worker SIGKILL; remove target path-prefix
replacement; accept process-crash durability without file/directory fsync.
Retain after_step/after_publish recovery and the byte-hash CAS as the core task.
Any change requires a new spec/prompt/suite revision and repeat validation before
registration; do not alter a launched registered plan.

External review reconciliation (AUTHOR-2): the 20–40 minute estimate belongs to
core4. The explicit core4b order targets 45–75 minutes and 40–60% pass; those
unmeasured targets remain unchanged. The all-fail risk at a shorter budget is
real; use the ordered relaxations above if authorized pilots indicate it. No
shorter-budget success claim is made.
