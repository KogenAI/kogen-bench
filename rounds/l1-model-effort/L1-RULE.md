Frozen L1 rule — sanitized publication copy

Question: how much does model and effort choice change what an agent
builds in 60 minutes?

Conditions:

- C1: gpt-6.1-sol, high effort.
- C2: gpt-6.1-sol, medium effort.
- C3: gpt-6-luna, max effort.
- C4: gpt-6-luna, medium effort.

The same frozen Linux harness, task, tool permissions and 60-minute wall
cap were used within each language. Each arm started from a pristine
language-specific template in a fresh agent session. Provider prompt
caching could not be separated from condition effects and is disclosed.
The two hosts ran in parallel, one arm at a time per host, so shared
account contention was possible.

Scoring used the frozen scorer offline. FINAL is the terminal or
3,600-second cap snapshot, regardless of the agent’s last message. T+30
is the 1,800-second snapshot; if a run ends earlier, its terminal
snapshot is used for both. Scores count visible suite cases passed out
of 106. Tokens are counted once per request, with cached input included
in input and reasoning output included in output. Missing token fields
are unavailable, not zero.

This is a descriptive pilot, with one run per condition per language.
Comparisons stay within a language because host and language are
confounded. No significance claim or decision follows from L1 alone.

The original frozen rule’s account labels, host identifiers, commands,
and operational paths are omitted from this publication copy.
