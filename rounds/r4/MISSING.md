# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 48,
  "fields": {
    "arm": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Arm label not retained": 6
      }
    },
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Boundary telemetry not retained": 48
      }
    },
    "circumstances.cap_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Boundary telemetry not retained": 6
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Boundary telemetry not retained": 30
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Boundary telemetry not retained": 6,
        "Launch running/active counter is block-scoped; host concurrency not emitted": 24
      }
    },
    "circumstances.dispatcher_id": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Dispatcher receipt unavailable": 6
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Boundary telemetry not retained": 48
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 33,
      "reasons": {
        "No matching controller samples retained": 33
      }
    },
    "circumstances.queue": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Queue receipt unavailable": 6
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Complete per-model billable vector unavailable": 42,
        "Not available for ungraded delivery": 6
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "No dated account-class receipt": 6
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "No per-cell CPU allocation receipt": 42,
        "Not available for ungraded delivery": 6
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "No per-cell CPU receipt": 42,
        "Not available for ungraded delivery": 6
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "No per-cell kernel receipt": 18
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "No per-cell RAM receipt": 42,
        "Not available for ungraded delivery": 6
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 42
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 42
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 42
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 42
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 42
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 42
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 6,
      "reasons": {
        "No official grade in the public snapshot": 6
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 7,
      "reasons": {
        "Boolean receipt not recorded": 1,
        "No official grade in the public snapshot": 6
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 16,
      "reasons": {
        "No official grade in the public snapshot": 6,
        "Not recorded in available public metadata": 10
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 48,
      "reasons": {
        "No per-cell CPU receipt": 42,
        "Not available for ungraded delivery": 6
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 18,
      "reasons": {
        "No per-cell kernel receipt": 18
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 48,
      "reasons": {
        "No per-cell RAM receipt": 42,
        "Not available for ungraded delivery": 6
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 48,
      "reasons": {
        "No per-cell CPU allocation receipt": 42,
        "Not available for ungraded delivery": 6
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 6,
      "reasons": {
        "Ungraded delivery needs evidence audit": 6
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 4,
      "reasons": {
        "No captured cohort launch receipt": 4
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 6,
      "reasons": {
        "No audited ITT receipt": 6
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 6,
      "reasons": {
        "No official grade in the public snapshot": 6
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Not recorded in available public metadata": 42
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Dependency source not pinned per cell": 48
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 42
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Original base revision type not recorded per cell": 42
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 42
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Original base revision type not recorded per cell": 42
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Attempt boundary receipts unavailable": 48
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Absolute phase boundary not retained": 48
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Absolute phase boundary not retained": 48
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Absolute phase boundary not retained": 48
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Absolute phase boundary not retained": 48
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Absolute phase boundary not retained": 48
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Absolute phase boundary not retained": 48
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Absolute phase boundary not retained": 48
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Absolute phase boundary not retained": 48
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Absolute phase boundary not retained": 48
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Absolute phase boundary not retained": 48
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Absolute phase boundary not retained": 48
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Absolute phase boundary not retained": 48
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Absolute phase boundary not retained": 48
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Absolute phase boundary not retained": 48
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Phase wall not emitted or not separable": 42
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Phase wall not emitted or not separable": 42
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 7,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Phase wall not emitted or not separable": 1
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Phase wall not emitted or not separable": 42
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Phase wall not emitted or not separable": 42
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Phase wall not emitted or not separable": 42
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Phase wall not emitted or not separable": 42
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 42
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 42
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 42
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 42
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 42
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 42
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 42
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 42
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 42
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 42
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 42
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 42
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 42
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 42
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 42
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 42
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 42
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 42
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 42
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 42
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 42
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 42
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 42
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 42
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 42,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 42
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 42,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 42
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 42,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 42
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 42,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 42
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 42,
        "Not available for ungraded delivery": 6
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 42,
        "Not available for ungraded delivery": 6
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 42,
        "Not available for ungraded delivery": 6
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 42
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 42
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 42
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 42
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 42
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 48,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 42
      }
    }
  },
  "gap_sources": {
    "lost": {
      "arm": {
        "none": 6
      },
      "circumstances.cap_end": {
        "none": 48
      },
      "circumstances.cap_start": {
        "none": 6
      },
      "circumstances.concurrent_cells_end": {
        "none": 30
      },
      "circumstances.concurrent_cells_start": {
        "none": 30
      },
      "circumstances.dispatcher_id": {
        "none": 6
      },
      "circumstances.load1_end": {
        "none": 48
      },
      "circumstances.load_samples": {
        "none": 33
      },
      "circumstances.queue": {
        "none": 6
      },
      "cost.accounting": {
        "none": 6
      },
      "cost.calculator_version": {
        "none": 6
      },
      "cost.long_context_reconciled": {
        "none": 6
      },
      "cost.price_table_version": {
        "none": 6
      },
      "cost.usd": {
        "none": 48
      },
      "environment.account_class": {
        "none": 6
      },
      "environment.cores": {
        "none": 48
      },
      "environment.cpu_model": {
        "none": 48
      },
      "environment.kernel": {
        "none": 18
      },
      "environment.ram_gib": {
        "none": 48
      },
      "environment.toolchains.elixir": {
        "none": 48
      },
      "environment.toolchains.erlang": {
        "none": 48
      },
      "environment.toolchains.node": {
        "none": 48
      },
      "environment.toolchains.other_inventory": {
        "none": 48
      },
      "environment.toolchains.ruby": {
        "none": 48
      },
      "environment.toolchains.rust": {
        "none": 48
      },
      "grade.grader": {
        "not re-derivable from the public record": 6
      },
      "grade.tests_ran": {
        "none": 1,
        "not re-derivable from the public record": 6
      },
      "grade.timestamp": {
        "none": 10,
        "not re-derivable from the public record": 6
      },
      "host.cpu": {
        "none": 48
      },
      "host.kernel": {
        "none": 18
      },
      "host.ram_gib": {
        "none": 48
      },
      "host.spec_ref": {
        "none": 6
      },
      "host.vcpu": {
        "none": 48
      },
      "itt.class": {
        "none": 6
      },
      "itt.cohort": {
        "none": 4
      },
      "itt.evidence_ref": {
        "none": 6
      },
      "outcome": {
        "not re-derivable from the public record": 6
      },
      "recipe": {
        "none": 48
      },
      "setup.deps_source": {
        "none": 48
      },
      "setup.task_base.hash": {
        "none": 48
      },
      "setup.task_base.kind": {
        "none": 48
      },
      "task.base_repo": {
        "none": 6
      },
      "task.base_revision.hash": {
        "none": 48
      },
      "task.base_revision.kind": {
        "none": 48
      },
      "timestamps.attempts": {
        "none": 48
      },
      "timestamps.phases.develop.end_utc": {
        "none": 48
      },
      "timestamps.phases.develop.start_utc": {
        "none": 48
      },
      "timestamps.phases.gate.end_utc": {
        "none": 48
      },
      "timestamps.phases.gate.start_utc": {
        "none": 48
      },
      "timestamps.phases.grade.end_utc": {
        "none": 48
      },
      "timestamps.phases.grade.start_utc": {
        "none": 48
      },
      "timestamps.phases.plan.end_utc": {
        "none": 48
      },
      "timestamps.phases.plan.start_utc": {
        "none": 48
      },
      "timestamps.phases.review.end_utc": {
        "none": 48
      },
      "timestamps.phases.review.start_utc": {
        "none": 48
      },
      "timestamps.phases.setup.end_utc": {
        "none": 48
      },
      "timestamps.phases.setup.start_utc": {
        "none": 48
      },
      "timestamps.phases.shape.end_utc": {
        "none": 48
      },
      "timestamps.phases.shape.start_utc": {
        "none": 48
      },
      "timing.phases_s.develop": {
        "none": 48
      },
      "timing.phases_s.gate": {
        "none": 48
      },
      "timing.phases_s.grade": {
        "none": 7
      },
      "timing.phases_s.plan": {
        "none": 48
      },
      "timing.phases_s.review": {
        "none": 48
      },
      "timing.phases_s.setup": {
        "none": 48
      },
      "timing.phases_s.shape": {
        "none": 48
      },
      "tokens.phases.develop.cached_input": {
        "none": 48
      },
      "tokens.phases.develop.input": {
        "none": 48
      },
      "tokens.phases.develop.output": {
        "none": 48
      },
      "tokens.phases.develop.reasoning": {
        "none": 48
      },
      "tokens.phases.gate.cached_input": {
        "none": 48
      },
      "tokens.phases.gate.input": {
        "none": 48
      },
      "tokens.phases.gate.output": {
        "none": 48
      },
      "tokens.phases.gate.reasoning": {
        "none": 48
      },
      "tokens.phases.grade.cached_input": {
        "none": 6
      },
      "tokens.phases.grade.input": {
        "none": 6
      },
      "tokens.phases.grade.output": {
        "none": 6
      },
      "tokens.phases.grade.reasoning": {
        "none": 6
      },
      "tokens.phases.plan.cached_input": {
        "none": 48
      },
      "tokens.phases.plan.input": {
        "none": 48
      },
      "tokens.phases.plan.output": {
        "none": 48
      },
      "tokens.phases.plan.reasoning": {
        "none": 48
      },
      "tokens.phases.review.cached_input": {
        "none": 48
      },
      "tokens.phases.review.input": {
        "none": 48
      },
      "tokens.phases.review.output": {
        "none": 48
      },
      "tokens.phases.review.reasoning": {
        "none": 48
      },
      "tokens.phases.setup.cached_input": {
        "none": 48
      },
      "tokens.phases.setup.input": {
        "none": 48
      },
      "tokens.phases.setup.output": {
        "none": 48
      },
      "tokens.phases.setup.reasoning": {
        "none": 48
      },
      "tokens.phases.shape.cached_input": {
        "none": 48
      },
      "tokens.phases.shape.input": {
        "none": 48
      },
      "tokens.phases.shape.output": {
        "none": 48
      },
      "tokens.phases.shape.reasoning": {
        "none": 48
      },
      "tokens.total.cached_input": {
        "none": 42
      },
      "tokens.total.input": {
        "none": 42
      },
      "tokens.total.output": {
        "none": 42
      },
      "tokens.total.reasoning": {
        "none": 42
      },
      "tools.codex_cli": {
        "none": 48
      },
      "tools.grader": {
        "none": 48
      },
      "tools.runner": {
        "none": 48
      },
      "tools.toolchains.elixir": {
        "none": 48
      },
      "tools.toolchains.erlang": {
        "none": 48
      },
      "tools.toolchains.node": {
        "none": 48
      },
      "tools.toolchains.other_inventory": {
        "none": 48
      },
      "tools.toolchains.ruby": {
        "none": 48
      },
      "tools.toolchains.rust": {
        "none": 48
      }
    },
    "reconstructable": {}
  },
  "round": "r4"
}
```
