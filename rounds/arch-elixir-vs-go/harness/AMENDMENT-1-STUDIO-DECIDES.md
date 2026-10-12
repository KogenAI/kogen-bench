# ARCH-20261011 amendment 1: the Studio decides; the MacBook is optional (11 Oct 2026)

Authority: coordinator (main) ruling under RULES 2 and the operator's standing rule of 11 Oct ("the Mac Studio is the source of truth; the MacBook is optional, intermittent, and nothing may depend on it"). This amends an UNLAUNCHED plan; the frozen DECISION-RULE-ARCH.md (4bab1146…) stays byte-identical, and this file is the dated, hashed amendment read alongside it. Writer: benchmarks (Opus). Reviewer: Astra (targeted recheck).

1. Deciding runs. All eight deciding runs execute on the Mac Studio as two sequential waves of four, so each wave keeps the frozen per-arm soft-core budget (2.5 cores × 4 arms = the Studio's 10 cores; eight concurrent arms would oversubscribe it twice over and change the wall-cap conditions):
   - Wave A: E1, E2, G1, G2 (pairs E1/G1, E2/G2).
   - Wave B: E3, E4, G3, G4 (pairs E3/G3, E4/G4).
   Pairs are preassigned within a wave. A wave plays the role the rule's "host" played (rule lines 12 and 28): each wave holds two E and two G runs, so E and G keep identical wave representation. No rematching or replacement runs after outcomes.
2. Decision. The rule's medians, conditions and pair-inclusion rule (a pair counts only if both runs are valid with complete F and T) apply unchanged to these eight Studio runs. Four runs per architecture, as frozen.
3. MacBook (optional). If the MacBook is reachable and admitted, it MAY run one extra wave of four (E5, E6, G5, G6). These runs are DESCRIPTIVE ONLY: reported beside the decision, never included in the deciding medians, and never waited for. If the MacBook drops, its cells are marked "interrupted: optional host unavailable" and the round stays decidable.
4. Disclosures added to DESIGN §8:
   (a) one physical host, so no cross-host replication claim;
   (b) waves are sequential, so time-of-day/provider drift between waves is possible, and the wave is reported as a factor;
   (c) per-wave CPU contention equals the frozen per-host contention.
5. Harness. arch_run gains a wave schedule for host studio (A then B; B starts after A's maintenance phase ends and A's scoring has a reserved, non-overlapping slot or has finished), plus the optional MacBook wave. The harness change is sealed with the manifest after a passing Studio dry cell. The dry cell is ONE wave-shaped cell (two arms, E and G) on the Studio; MacBook dry cells are no longer required. This amendment also supersedes the both-Mac passability requirements in DESIGN §3 and §7 gate 2: require analysis plus stub-mechanics evidence on the Studio alone, or, if witnesses are ordered, both Elixir/OTP and Go witnesses passing 3/3 clean repetitions on the Studio alone. MacBook validation is optional and cannot gate the Studio launch or verdict. Include this amended gate and its evidence in the re-sealed prelaunch hash manifest.
6. Future rounds: every round rule states what happens if the MacBook drops: its cells are interrupted, and the round stays decidable without them.


Recheck (Astra medium, ARCH-AMEND1-RECHECK): 1 finding (MacBook passability gates) — ADOPTED verbatim above.
