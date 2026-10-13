# Repair-turn coding rubric (frozen)

Code the attempt's Codex event log after the run. Use `parse_events.py`'s edit event IDs to identify edits; inspect the adjacent command/check events only to establish chronology and what failure was visible to the agent.

Count one repair turn when all of these are true:

1. A completed execution or checker event exposed a concrete failure.
2. In a later agent turn, the agent made at least one source/configuration edit that addresses that previously observed failure.
3. The edit is supported by an edit event ID and the failure by its execution/check event ID.

Count a turn at most once even when it contains several corrective edits or addresses several failures. An agent turn containing edits that address failures from earlier turns counts once. A turn that only reruns verification, changes presentation without addressing a failure, or edits before any failure was observed does not count. A missing or ambiguous event link is coded `uncertain` and excluded from the primary count, with the event IDs retained.

Record `repair_turns`, the counted agent turn IDs, each linked failure event ID, each supporting edit event ID, and any uncertainty note. Do not infer a repair from a nonzero shell count alone; inspect the command result and subsequent edit chronology.
