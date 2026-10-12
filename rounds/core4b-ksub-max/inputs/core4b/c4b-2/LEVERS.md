# Difficulty and adjustments

Target: 40–60% pilot pass rate; a strong implementation should take 45–75 minutes.
Hardness comes from several interacting modules: canonical object hashing and
DAG traversal; per-ref ABA fencing and tombstones; atomic multi-ref CAS; permanent
idempotent receipts that outrank clock/object checks; retained reflog; grace
interval reset on graph reachability transitions; closure-preserving GC; and
cross-process serialization with precisely placed crash hooks. Tests connect
these rules rather than merely checking each command in isolation.

If pilots pass everything, choose one change and update spec/suite/references:
1. Add bounded reflog retention and explicit history pins that participate in GC.
2. Add read-snapshot tokens that permit optimistic transactions over unedited refs.
3. Require separate object files and resumable physical GC with a per-object hook.
4. Add batch object insertion with forward references and cycle rejection.

If too hard: remove young-orphan ancestry protection and require only age-based
collection with dangling parents explicitly allowed; or remove replay receipts
and their precedence; or collapse versions to OID-only CAS (drops ABA coverage).
Prefer reducing one interacting invariant over shortening concurrency runs.
No difficulty claim is a measured pass rate; pilot measurement remains pending.
