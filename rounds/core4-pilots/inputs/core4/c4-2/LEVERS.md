# Difficulty levers

1. Add batched claims and all-or-nothing batch acknowledgments, with crash hooks
   spanning the batch, to expose partial transaction writes.
2. Add bounded retention and key tombstones; require key idempotency after job
   pruning and crash-safe compaction of the storage log or snapshots.
3. Add queue namespaces and a global concurrency limit enforced across workers,
   including atomic slot release on expiry and acknowledgment.
4. Add a client operation ID for claim/heartbeat/ack so retries after lost
   responses return the original result without a second transition.
5. Raise the job count and impose a runtime bound that makes rewriting the whole
   queue impractical, requiring indexed storage and bounded recovery.
