# HC01: stopped by the owner for host maintenance

Recorded 2026-10-08T16:42:09Z.

HC01 was stopped at **25/32 graded**, by the owner, for host maintenance (a Hetzner Rebuild of kogen-bench-us for the new one-command host setup). That is a decision about infrastructure, not outcomes. The round is DESCRIPTIVE, and it could not reach KEEP after AMENDMENT-5. No rule changes and no reanalysis rules were added.

## Stop sequence (UTC)
1. STOP markers set at 16:41:03Z: levers/hc01-lane/STOP and the root STOP-us.
2. The bulk launcher (pgid 2824068) got TERM. Cell 26 (kogen-rs-hc01-on, syn-31 r4), running since 16:24:19Z and in Kogen's Shape stage, ended with it.
   - Its transient unit bench-b65b2ed346 is inactive, and no bench-user processes remain.
   - Its manifest stays at status "running" with no COMPLETE.json.
   - It is kept as an **owner-stopped attempt**: not a model failure, and not in the analysed denominator.
3. Cells 27–32 were never started.
4. The MacBook grade loop and count follower were stopped with no grade in flight.

## Counts
- Graded: 25 cells = 12 complete pairs + 1 orphan (syn-31 OFF r4, whose ON partner is the owner-stopped cell). All official grades come from the night_grade v2 route: cells 1–19 on the Studio, 20–25 on the MacBook (AMENDMENT-6).
- Frozen-rule category: **INCOMPLETE** (stopped by the owner), labelled **DESCRIPTIVE**, with ceiling **NOT CONFIRMED** (AMENDMENT-5).

## Descriptive numbers (frozen rule's descriptive reporting; not a confirmatory test)
- **Per-task full pass:**
  - board: OFF 2/3, ON 2/3;
  - erase: OFF 0/3, ON 0/3;
  - syn-06: OFF 2/3, ON 3/3;
  - syn-31: OFF 0/4, ON 2/3.
- **Over the 12 complete pairs:** rescues R = 3, losses L = 0, D = +0.25 (equal task weights over complete pairs). One-sided exact McNemar p_plus = 0.125 and p_minus = 1.0, reported descriptively only.
- **Official test counts:**
  - for failing withheld-source-artifact-family cells only (board 8/9, 8/9; erase 8/10, 7/10, …; see grades/counts rows);
  - withheld-source-artifact PASS cells and all validation-family cells are "count unavailable" (AMENDMENT-4/5 and the coordinator ruling);
  - no-patch cells count as effective 0 by the ITT convention.
