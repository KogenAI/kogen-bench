# Scored release checklist

Use this checklist before releasing scored cells. See the [public glossary](../rounds/GLOSSARY.md) for terms.

1. **Real sandbox smoke for every arm.** Use the exact arm configuration and deployed inputs through the production-equivalent sandbox. Obtain an official grade for each smoke cell before bulk release.
2. **Smoke each harness separately.** A successful smoke on one harness does not verify another harness, even on the same venue.
3. **Credential handling.** Check access through an approved status-only method. Do not copy or refresh shared credentials on benchmark workers; cells must not depend on worker access to authentication services.
4. **Base gates.** Run format, lint, and acceptance checks on the untouched base and record the expected results before release.
5. **Pinned source.** Build from a fresh checkout at the named revision. Isolate each arm and keep its source revision pinned while cells are running.
6. **Input validation.** Validate and record task inputs and harness configuration before launch.
7. **Capacity controls.** Apply host-wide concurrency and worker-storage limits across every active study. Use one admission controller per venue and verify active-cell counts before launch.
8. **Predeclared analysis.** Record the decision rule before release. Exclude a cell from intention-to-treat analysis only when a documented environment or adapter fault proves the exclusion.
9. **Frozen launch materials.** Keep the reviewed launch specification and scripts versioned and unchanged during execution. Launch only from a complete, nonempty specification.
10. **Standard records.** Emit one standard run record per cell. Strict validation must pass on officially graded real-sandbox smoke cells for every arm before release, and on all cells before analysis.

Scored release requires all ten checks and a public receipt for the smoke records and validation results.
