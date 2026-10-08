# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 110,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Boundary telemetry not retained": 110
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
      "count": 74,
      "reasons": {
        "Boundary telemetry not retained": 74
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 74,
      "reasons": {
        "Boundary telemetry not retained": 6,
        "Launch running/active counter is block-scoped; host concurrency not emitted": 68
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
      "count": 110,
      "reasons": {
        "Boundary telemetry not retained": 110
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 74,
      "reasons": {
        "No matching controller samples retained": 74
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
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 4
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 4
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 4
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 4
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 4
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 74,
      "reasons": {
        "No dated account-class receipt": 74
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "No per-cell CPU allocation receipt": 106,
        "Not available for ungraded delivery": 4
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "No per-cell CPU receipt": 106,
        "Not available for ungraded delivery": 4
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "No per-cell kernel receipt": 32,
        "Not available for ungraded delivery": 4
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "No per-cell RAM receipt": 106,
        "Not available for ungraded delivery": 4
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Toolchain version/inventory not recorded": 106
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Toolchain version/inventory not recorded": 106
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Toolchain version/inventory not recorded": 106
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Toolchain version/inventory not recorded": 106
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Toolchain version/inventory not recorded": 106
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Toolchain version/inventory not recorded": 106
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 4,
      "reasons": {
        "No official grade in the public snapshot": 4
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 4,
      "reasons": {
        "No official grade in the public snapshot": 4
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 4,
      "reasons": {
        "No official grade in the public snapshot": 4
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 110,
      "reasons": {
        "No per-cell CPU receipt": 106,
        "Not available for ungraded delivery": 4
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 36,
      "reasons": {
        "No per-cell kernel receipt": 32,
        "Not available for ungraded delivery": 4
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 110,
      "reasons": {
        "No per-cell RAM receipt": 106,
        "Not available for ungraded delivery": 4
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 4
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 110,
      "reasons": {
        "No per-cell CPU allocation receipt": 106,
        "Not available for ungraded delivery": 4
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 4,
      "reasons": {
        "Ungraded delivery needs evidence audit": 4
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
      "count": 4,
      "reasons": {
        "No audited ITT receipt": 4
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 4,
      "reasons": {
        "No official grade in the public snapshot": 4
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Not recorded in available public metadata": 32
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Dependency source not pinned per cell": 110
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 32
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Original base revision type not recorded per cell": 32
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 2,
      "reasons": {
        "No normalized stop receipt": 1,
        "Runner status does not establish normalized stop cause": 1
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 4
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 32
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Original base revision type not recorded per cell": 32
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Attempt boundary receipts unavailable": 110
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Absolute phase boundary not retained": 36
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Absolute phase boundary not retained": 36
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Absolute phase boundary not retained": 110
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Absolute phase boundary not retained": 110
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Absolute phase boundary not retained": 110
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Absolute phase boundary not retained": 110
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Absolute phase boundary not retained": 110
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Absolute phase boundary not retained": 110
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Absolute phase boundary not retained": 110
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Absolute phase boundary not retained": 110
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Absolute phase boundary not retained": 110
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Absolute phase boundary not retained": 110
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Absolute phase boundary not retained": 110
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Absolute phase boundary not retained": 110
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Phase wall not emitted or not separable": 106
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Phase wall not emitted or not separable": 106
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 4
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Phase wall not emitted or not separable": 106
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Phase wall not emitted or not separable": 106
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Phase wall not emitted or not separable": 106
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Phase wall not emitted or not separable": 106
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 106
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 106
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 106
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 106
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 106
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 106
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 106
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 106
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 4
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 4
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 4
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 4
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 106
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 106
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 106
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 106
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 106
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 106
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 106
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 106
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 106
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 106
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 106
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 106
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 106
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 106
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 106
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 106
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 32,
        "Not available for ungraded delivery": 4
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 106,
        "Not available for ungraded delivery": 4
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 106,
        "Not available for ungraded delivery": 4
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Toolchain version/inventory not recorded": 106
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Toolchain version/inventory not recorded": 106
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Toolchain version/inventory not recorded": 106
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Toolchain version/inventory not recorded": 106
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Toolchain version/inventory not recorded": 106
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 110,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Toolchain version/inventory not recorded": 106
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 110
      },
      "circumstances.cap_start": {
        "none": 6
      },
      "circumstances.concurrent_cells_end": {
        "none": 74
      },
      "circumstances.concurrent_cells_start": {
        "none": 74
      },
      "circumstances.dispatcher_id": {
        "none": 6
      },
      "circumstances.load1_end": {
        "none": 110
      },
      "circumstances.load_samples": {
        "none": 74
      },
      "circumstances.queue": {
        "none": 6
      },
      "cost.accounting": {
        "none": 4
      },
      "cost.calculator_version": {
        "none": 4
      },
      "cost.long_context_reconciled": {
        "none": 4
      },
      "cost.price_table_version": {
        "none": 4
      },
      "cost.usd": {
        "none": 4
      },
      "environment.account_class": {
        "none": 74
      },
      "environment.cores": {
        "none": 110
      },
      "environment.cpu_model": {
        "none": 110
      },
      "environment.kernel": {
        "none": 36
      },
      "environment.ram_gib": {
        "none": 110
      },
      "environment.toolchains.elixir": {
        "none": 110
      },
      "environment.toolchains.erlang": {
        "none": 110
      },
      "environment.toolchains.node": {
        "none": 110
      },
      "environment.toolchains.other_inventory": {
        "none": 110
      },
      "environment.toolchains.ruby": {
        "none": 110
      },
      "environment.toolchains.rust": {
        "none": 110
      },
      "grade.grader": {
        "not re-derivable from the public record": 4
      },
      "grade.tests_ran": {
        "not re-derivable from the public record": 4
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 4
      },
      "host.cpu": {
        "none": 110
      },
      "host.kernel": {
        "none": 36
      },
      "host.ram_gib": {
        "none": 110
      },
      "host.spec_ref": {
        "none": 4
      },
      "host.vcpu": {
        "none": 110
      },
      "itt.class": {
        "none": 4
      },
      "itt.cohort": {
        "none": 4
      },
      "itt.evidence_ref": {
        "none": 4
      },
      "outcome": {
        "not re-derivable from the public record": 4
      },
      "recipe": {
        "none": 36
      },
      "setup.deps_source": {
        "none": 110
      },
      "setup.task_base.hash": {
        "none": 36
      },
      "setup.task_base.kind": {
        "none": 36
      },
      "stop_reason": {
        "none": 2
      },
      "task.base_repo": {
        "none": 4
      },
      "task.base_revision.hash": {
        "none": 36
      },
      "task.base_revision.kind": {
        "none": 36
      },
      "timestamps.attempts": {
        "none": 110
      },
      "timestamps.phases.develop.end_utc": {
        "none": 36
      },
      "timestamps.phases.develop.start_utc": {
        "none": 36
      },
      "timestamps.phases.gate.end_utc": {
        "none": 110
      },
      "timestamps.phases.gate.start_utc": {
        "none": 110
      },
      "timestamps.phases.grade.end_utc": {
        "none": 110
      },
      "timestamps.phases.grade.start_utc": {
        "none": 110
      },
      "timestamps.phases.plan.end_utc": {
        "none": 110
      },
      "timestamps.phases.plan.start_utc": {
        "none": 110
      },
      "timestamps.phases.review.end_utc": {
        "none": 110
      },
      "timestamps.phases.review.start_utc": {
        "none": 110
      },
      "timestamps.phases.setup.end_utc": {
        "none": 110
      },
      "timestamps.phases.setup.start_utc": {
        "none": 110
      },
      "timestamps.phases.shape.end_utc": {
        "none": 110
      },
      "timestamps.phases.shape.start_utc": {
        "none": 110
      },
      "timing.phases_s.develop": {
        "none": 110
      },
      "timing.phases_s.gate": {
        "none": 110
      },
      "timing.phases_s.grade": {
        "none": 4
      },
      "timing.phases_s.plan": {
        "none": 110
      },
      "timing.phases_s.review": {
        "none": 110
      },
      "timing.phases_s.setup": {
        "none": 110
      },
      "timing.phases_s.shape": {
        "none": 110
      },
      "tokens.phases.develop.cached_input": {
        "none": 110
      },
      "tokens.phases.develop.input": {
        "none": 110
      },
      "tokens.phases.develop.output": {
        "none": 110
      },
      "tokens.phases.develop.reasoning": {
        "none": 110
      },
      "tokens.phases.gate.cached_input": {
        "none": 110
      },
      "tokens.phases.gate.input": {
        "none": 110
      },
      "tokens.phases.gate.output": {
        "none": 110
      },
      "tokens.phases.gate.reasoning": {
        "none": 110
      },
      "tokens.phases.grade.cached_input": {
        "none": 4
      },
      "tokens.phases.grade.input": {
        "none": 4
      },
      "tokens.phases.grade.output": {
        "none": 4
      },
      "tokens.phases.grade.reasoning": {
        "none": 4
      },
      "tokens.phases.plan.cached_input": {
        "none": 110
      },
      "tokens.phases.plan.input": {
        "none": 110
      },
      "tokens.phases.plan.output": {
        "none": 110
      },
      "tokens.phases.plan.reasoning": {
        "none": 110
      },
      "tokens.phases.review.cached_input": {
        "none": 110
      },
      "tokens.phases.review.input": {
        "none": 110
      },
      "tokens.phases.review.output": {
        "none": 110
      },
      "tokens.phases.review.reasoning": {
        "none": 110
      },
      "tokens.phases.setup.cached_input": {
        "none": 110
      },
      "tokens.phases.setup.input": {
        "none": 110
      },
      "tokens.phases.setup.output": {
        "none": 110
      },
      "tokens.phases.setup.reasoning": {
        "none": 110
      },
      "tokens.phases.shape.cached_input": {
        "none": 110
      },
      "tokens.phases.shape.input": {
        "none": 110
      },
      "tokens.phases.shape.output": {
        "none": 110
      },
      "tokens.phases.shape.reasoning": {
        "none": 110
      },
      "tools.codex_cli": {
        "none": 36
      },
      "tools.grader": {
        "none": 110
      },
      "tools.runner": {
        "none": 110
      },
      "tools.toolchains.elixir": {
        "none": 110
      },
      "tools.toolchains.erlang": {
        "none": 110
      },
      "tools.toolchains.node": {
        "none": 110
      },
      "tools.toolchains.other_inventory": {
        "none": 110
      },
      "tools.toolchains.ruby": {
        "none": 110
      },
      "tools.toolchains.rust": {
        "none": 110
      }
    },
    "reconstructable": {}
  },
  "publication_reconciliation": {
    "disposition": "A one-cell classification conflict is recorded in the current status, but its exact cell is not established by the public aggregate rows. That conflict is source-reported, not reproducible from public data. Preserve INTERIM and do not restore the historical comparison or its p-value.",
    "original_execution_command": "not recorded in the public snapshot",
    "harness_source_commit": "absent; tools.harness values are wrapper fingerprints",
    "kogen_source_commit": "Public records mark the Kogen product commit not applicable for these harness records.",
    "raw_public_records": [
      "results/run-records/r53.jsonl",
      "results/cells.jsonl"
    ],
    "public_record_rebuild": "python3 reproduce/export_results.py; python3 reproduce/build_records.py; python3 reproduce/validate_round.py --round r53"
  },
  "round": "r53"
}
```
