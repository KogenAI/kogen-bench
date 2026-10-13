# Deviations and operational notes

## Measurement gate sequence

The no-model apparatus check passed for the selected z,b configuration. c2 was withheld after its live allowed_rw positive control failed to produce the expected marker. A manual nono run in the same scope did produce the marker; the cause is unresolved and no explanation is guessed here.

The one-repetition z,b rehearsal completed its report as REHEARSAL / DISCARDED. Its teardown gate passed. It is not part of the measured result. The retained measurement then ran three repetitions for z and b under the same frozen manifest and plan.

## Apparatus development history

The source history records three live-check failures that were later fixed. A separate observer-order regression was also identified and corrected. The final selected-arm check passed before rehearsal and measurement. These repairs explain the gate history but do not add outcomes or alter the published per-cell matrix.

The matrix records b file_read_outside, secret_file_read and net_loopback as INVALID(launch ok), not blocked or passed. The complete c2 arm is NOT-RUN. z cap cells are UNSUPPORTED(no mechanism).

## Host exclusivity and scheduled activity

The measurement window was reserved for this harness and had no concurrent benchmark experiment. A scheduled egress-refresh cron job remained active and generated periodic ticks during the run. It was disclosed, left untouched and was not classified as a host-exclusivity violation. It did not run benchmark fixtures. No host firewall changes are claimed.

## Scope of the observed mechanisms

b is bubblewrap inside a systemd scope, including configured scope resource limits and its PID namespace/die-with-parent behavior. The results do not isolate bubblewrap from those surrounding controls or compare native nono resource enforcement. The survivor observation was made 200 ms after runner SIGKILL while the scope remained active; it is not a scope-stop result.

## Publication sanitization

The public harness mirror resolves account-home paths through account metadata and uses a renamed fixture-value variable. The deployed source hashes and apparatus fingerprint identify the measured source. The public mirror is intentionally not byte-identical; no result was recomputed from the mirror.
