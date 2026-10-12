# Difficulty and pilot levers

Target: 40–60% pilot pass rate, 45–75 minutes for a strong agent. This is an
unmeasured target; no contestant pilot is authorized in this author job.

Hardness comes from interacting scanning, identity matching, debounce, outbox,
clock validation, crash recovery, and locking modules. The baseline differs from
the observed snapshot; acknowledging delivery must not change either. Rename
chains, swaps, hard links, replacement writes and symlink content use distinct
rules. A late poll must scan before deciding whether an old deadline is due.
Persisted pending windows and assigned-but-unreturned batches stress separate
commit boundaries. Content is hashed despite unchanged mtime/size. The suite
checks exact events and rollback, not merely eventual counts.

If too easy after pilots:
1. Add bounded batch paging and an opaque continuation cursor tied to an outbox
   revision; specify behavior under ack and concurrent sealing.
2. Add per-subtree ignore rules with explicit reconfiguration baseline semantics.
3. Add max-wait sealing in addition to trailing quiet time, with exact scan-first
   precedence when both deadlines expire.
4. Add stable-scan retry rules for files mutated during enumeration, with a
   documented retry budget and all-or-nothing observation.

If too hard, relax these constraints in sequence: remove hard-link pairing while retaining
ordinary renames; remove concurrent invocation tests while retaining crash-safe
commits; remove cumulative ack/outbox and explicitly weaken delivery semantics.
Do not relax JSON framing or silently accept loss across successful restarts.
