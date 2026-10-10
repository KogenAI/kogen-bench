# Acceptance specifications for Intents

Every Intent carries Gherkin acceptance scenarios describing the requested behavior in terms a caller can review.
The Shaper preserves the verbatim request and writes the requirements, Acceptance and Verify sections together with
those scenarios. An Intent may also carry Quint properties and models for state transitions, invariants, success
traces and safety failures. Quint is optional; its absence does not prevent shaping or approval.

The review card identifies the scenarios and optional properties, and reports exactly which scenarios and generated
traces were checked, their results, bounds, seeds, tool versions and retained artifacts. Distinguish passed, failed,
unchecked and blocked results. Specification checks are advisory and non-blocking by default. Explicitly configured
project checks or approved executable acceptance may make selected scenarios or properties part of the gate; the
review card must identify that policy before approval. A trace with no observable actions supplies no executable
conformance coverage. A passing model check is separate from replay against the candidate.

Approval is a separate caller action and binds the exact Intent and executable acceptance bytes, including source
presence or absence. Put accepted scenario/property identities and any required gate policy in that approved contract;
changes to bound bytes require approval again. The Shaper cannot approve. The bounded Build preserves the approved
contract, runs required configured checks and executable acceptance against its exact candidate, and records receipts
against that complete tree. Advisory scenario/property results do not grant verification or waive a required check.
After a base rebase, rerun the required checks against the resulting tree; recheck the tree immediately before landing.

Optional Quint checks include typechecking, authored tests, bounded invariant exploration and positive/negative trace
replay. Record actual tools, model/fixture digests, seeds, sample/step bounds, checked scenarios, replay results and
candidate identity. Review can examine generated traces without treating bounded exploration as an unbounded proof.
The integrated system checks use 300 samples and 20 steps; the generated-suite profiles are in
[QUINT-SUITE.md](QUINT-SUITE.md). Check failures, unavailable capabilities and historical gaps remain visible.

## Open questions

- Location: store scenarios and optional models beside the Intent or in a versioned shared specification directory?
- Limits: which state-size, readability and scenario-count limits should apply?
- Effects: which external outcomes should be model inputs, and which observable trace effects are required?
- Properties: which safety properties should be suggested for each Intent, and which can a project require?
- Review: which scenarios and generated traces should the caller inspect before approving?
- Receipts: which serialization and tree identity format should store check and replay results?
- Versions: bind tool versions and model/scenario digests in the approved Intent and candidate receipt?
- Exploration: which default bounds suit advisory checks, and how can projects opt into larger required checks?
