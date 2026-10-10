# Trial execution source

The runner, counted feedback broker, usage monitor, diagnosis ordering,
source regeneration and public test/API drivers are included. Paths in this
public copy use installation locations under `/opt`; provision these on a
fresh Linux host and supply your own account through the runner parameters.
The publication copy requires explicit account-home and expected-account
parameters and accepts an admission-region key with `--admission-host`.
These are edited publication copies, not the exact admitted runtime hashes.

The final evaluator is a private external dependency. Its implementation,
answer catalog and evaluation inputs are not included. The runner's final
evaluation entry point must be supplied by an operator before execution.
The public bundle can regenerate formal feedback and run starter tests;
it cannot independently repeat the historical final grades or model calls.
Historical outcome receipts in the ledger are source-reported results.
Never give an agent the trial outputs or results while rerunning a task.
