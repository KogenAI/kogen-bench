# Safety model

`arch.qnt` models four finite job identities, two repositories, two worker slots, durable acceptance sequence and normalized priority, high-first FIFO queue assignment, eight logical seconds per lease, successful/failed build, ready lane waiting, landing intent, Git ref application, terminal recording, cancellation, expiration, shutdown, and independent coordinator/worker crashes and restarts. Maintenance M01–M06 are represented by directed tests and the priority/landing invariants.

The acceptance set and terminal map are ghost history. Git history and per-job landing counts are separate from job state. This separation lets the simulator crash between intent persistence, Git movement, and terminal persistence. Recovery uses `applyRef` only while the old head remains and `finishLand` when the recorded candidate already appears; it cannot apply the same job twice.

`safety` combines `noLoss`, `noDoubleLand`, `serializedLanding`, `landingOrder`, `oneJobPerWorker`, `containmentDeadline`, `immutableTerminal`, `landedHasCommit`, `commitHasDurableIntent`, `gitHistoryConsistent`, `intentProtectsLane`, and `sequenceUnique`. Accepted jobs remain represented even during downtime; terminal records never change; the landing lane includes protected recovery intents; Git history/counts agree and every applied commit has durable recovery evidence.

The implementation refines this abstraction: `prepare` includes a successful landing rerun and durable artifact intent; `finishFailure`/`cleanupCancel` include confirmed whole-tree cleanup; `tick` includes an independent supervisor killing trees before hard lease expiry. The model **assumes**, rather than proves, OS tree tracking and fsync/atomic-rename correctness. Logical deadline cleanup is atomic; the one-second retry availability bound and real-time fairness are exercised by F scenarios, not this safety simulation. Arbitrary stuttering/crashes mean the model makes no unconditional liveness claim. Invalid messages and exact duplicate replay are abstracted as `ignoredMessage`; token/session encoding, JSON parsing, shell execution, and Git conflict detection are not modeled.

Run from `spec/` with the supplied local tool:

```
<scratch-dir>/race6-kit/quint/quint typecheck quint/arch.qnt
<scratch-dir>/race6-kit/quint/quint test quint/arch.qnt --match '.*Test' --seed 20261011
<scratch-dir>/race6-kit/quint/quint run quint/arch.qnt --invariant safety --max-samples 1000 --max-steps 100 --seed 20261011 --verbosity 1
```

The commands above use the provided wrapper, which selects the TypeScript backend for `run` and `test`; do not add `--backend typescript`. Six base directed tests exercise recovery before/after the ref update, FIFO landing, both-process death and expiration, cancellation before intent, and lane release after a failed predecessor. Eight maintenance tests cover normalization/validation, priority dispatch and nonpreemption, FIFO lease retry, priority-independent landing, and restart/replay. Typechecking, directed tests, and randomized invariant checking are self-checks, not an exhaustive proof. SELF-CHECKS.md records the actual run and witness coverage. No formal verifier installation is required.
