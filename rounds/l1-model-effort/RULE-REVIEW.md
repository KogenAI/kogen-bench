Frozen rule review — sanitized publication copy

The independent review found five blocking issues before execution:

1. Arm isolation needed an explicit fresh-session and clean-state rule.
2. Sequential runs on separate hosts could still compete for a shared
   account; this risk needed to be stated.
3. Snapshot and clock boundaries needed precise definitions.
4. Token, timing, command-based activity estimates and failure counting needed fixed rules.
5. Infrastructure replacement limits and inclusion rules needed to be
   specified.

The adopted rule addressed arm isolation, snapshot boundaries, metrics
and the one-replacement limit. Shared-account contention remained
possible because the hosts ran in parallel. The final report discloses
this limitation. The review found the descriptive-pilot and
no-significance wording appropriately restrained.

This copy omits account labels, host identifiers and private paths.
