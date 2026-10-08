# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 119,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Boundary telemetry not retained": 119
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Boundary telemetry not retained": 90
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 90
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Boundary telemetry not retained": 119
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 105,
      "reasons": {
        "No matching controller samples retained": 105
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 14,
      "reasons": {
        "Not available for ungraded delivery": 14
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 14,
      "reasons": {
        "Not available for ungraded delivery": 14
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 14,
      "reasons": {
        "Not available for ungraded delivery": 14
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 14,
      "reasons": {
        "Not available for ungraded delivery": 14
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Complete per-model billable vector unavailable": 105,
        "Not available for ungraded delivery": 14
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 14,
      "reasons": {
        "Not recorded in available public metadata": 14
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "No per-cell CPU allocation receipt": 105,
        "Not available for ungraded delivery": 14
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "No per-cell CPU receipt": 105,
        "Not available for ungraded delivery": 14
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 29,
      "reasons": {
        "No per-cell kernel receipt": 15,
        "Not available for ungraded delivery": 14
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "No per-cell RAM receipt": 105,
        "Not available for ungraded delivery": 14
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Toolchain version/inventory not recorded": 105
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Toolchain version/inventory not recorded": 105
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Toolchain version/inventory not recorded": 105
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Toolchain version/inventory not recorded": 105
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Toolchain version/inventory not recorded": 105
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Toolchain version/inventory not recorded": 105
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 14,
      "reasons": {
        "No official grade in the public snapshot": 14
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 15,
      "reasons": {
        "Boolean receipt not recorded": 1,
        "No official grade in the public snapshot": 14
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 62,
      "reasons": {
        "No official grade in the public snapshot": 14,
        "Not recorded in available public metadata": 48
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 119,
      "reasons": {
        "No per-cell CPU receipt": 105,
        "Not available for ungraded delivery": 14
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 29,
      "reasons": {
        "No per-cell kernel receipt": 15,
        "Not available for ungraded delivery": 14
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 119,
      "reasons": {
        "No per-cell RAM receipt": 105,
        "Not available for ungraded delivery": 14
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 14,
      "reasons": {
        "Not available for ungraded delivery": 14
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 119,
      "reasons": {
        "No per-cell CPU allocation receipt": 105,
        "Not available for ungraded delivery": 14
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 14,
      "reasons": {
        "Ungraded delivery needs evidence audit": 14
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 14,
      "reasons": {
        "No captured cohort launch receipt": 14
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 14,
      "reasons": {
        "No audited ITT receipt": 14
      }
    },
    "model.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 14,
      "reasons": {
        "Not recorded in available public metadata": 14
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 14,
      "reasons": {
        "No official grade in the public snapshot": 14
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Not recorded in available public metadata": 105
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Dependency source not pinned per cell": 119
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 105
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Original base revision type not recorded per cell": 105
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 14,
      "reasons": {
        "No normalized stop receipt": 14
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 14,
      "reasons": {
        "Not available for ungraded delivery": 14
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 105
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Original base revision type not recorded per cell": 105
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Attempt boundary receipts unavailable": 119
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Absolute phase boundary not retained": 119
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Absolute phase boundary not retained": 119
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Absolute phase boundary not retained": 119
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Absolute phase boundary not retained": 119
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Absolute phase boundary not retained": 119
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Absolute phase boundary not retained": 119
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Absolute phase boundary not retained": 119
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Absolute phase boundary not retained": 119
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Absolute phase boundary not retained": 119
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Absolute phase boundary not retained": 119
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Absolute phase boundary not retained": 119
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Absolute phase boundary not retained": 119
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Absolute phase boundary not retained": 119
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Absolute phase boundary not retained": 119
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Phase wall not emitted or not separable": 105
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Phase wall not emitted or not separable": 105
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Phase wall not emitted or not separable": 1
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Phase wall not emitted or not separable": 105
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Phase wall not emitted or not separable": 105
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Phase wall not emitted or not separable": 105
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Phase wall not emitted or not separable": 105
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 105
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 105
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 105
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 105
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 105
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 105
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 105
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 105
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 14,
      "reasons": {
        "Not available for ungraded delivery": 14
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 14,
      "reasons": {
        "Not available for ungraded delivery": 14
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 14,
      "reasons": {
        "Not available for ungraded delivery": 14
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 14,
      "reasons": {
        "Not available for ungraded delivery": 14
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 105
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 105
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 105
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 105
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 105
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 105
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 105
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 105
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 105
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 105
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 105
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 105
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 105
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 105
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 105
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 105
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 105,
        "Usage counter unavailable": 14
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 105,
        "Usage counter unavailable": 14
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 105,
        "Usage counter unavailable": 14
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 119,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 105,
        "Usage counter unavailable": 14
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 105,
        "Not available for ungraded delivery": 14
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 105,
        "Not available for ungraded delivery": 14
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 105,
        "Not available for ungraded delivery": 14
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Toolchain version/inventory not recorded": 105
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Toolchain version/inventory not recorded": 105
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Toolchain version/inventory not recorded": 105
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Toolchain version/inventory not recorded": 105
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Toolchain version/inventory not recorded": 105
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 119,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Toolchain version/inventory not recorded": 105
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 119
      },
      "circumstances.concurrent_cells_end": {
        "none": 90
      },
      "circumstances.concurrent_cells_start": {
        "none": 90
      },
      "circumstances.load1_end": {
        "none": 119
      },
      "circumstances.load_samples": {
        "none": 105
      },
      "cost.accounting": {
        "none": 14
      },
      "cost.calculator_version": {
        "none": 14
      },
      "cost.long_context_reconciled": {
        "none": 14
      },
      "cost.price_table_version": {
        "none": 14
      },
      "cost.usd": {
        "none": 119
      },
      "effort.effective": {
        "none": 14
      },
      "environment.cores": {
        "none": 119
      },
      "environment.cpu_model": {
        "none": 119
      },
      "environment.kernel": {
        "none": 29
      },
      "environment.ram_gib": {
        "none": 119
      },
      "environment.toolchains.elixir": {
        "none": 119
      },
      "environment.toolchains.erlang": {
        "none": 119
      },
      "environment.toolchains.node": {
        "none": 119
      },
      "environment.toolchains.other_inventory": {
        "none": 119
      },
      "environment.toolchains.ruby": {
        "none": 119
      },
      "environment.toolchains.rust": {
        "none": 119
      },
      "grade.grader": {
        "not re-derivable from the public record": 14
      },
      "grade.tests_ran": {
        "none": 1,
        "not re-derivable from the public record": 14
      },
      "grade.timestamp": {
        "none": 48,
        "not re-derivable from the public record": 14
      },
      "host.cpu": {
        "none": 119
      },
      "host.kernel": {
        "none": 29
      },
      "host.ram_gib": {
        "none": 119
      },
      "host.spec_ref": {
        "none": 14
      },
      "host.vcpu": {
        "none": 119
      },
      "itt.class": {
        "none": 14
      },
      "itt.cohort": {
        "none": 14
      },
      "itt.evidence_ref": {
        "none": 14
      },
      "model.effective": {
        "none": 14
      },
      "outcome": {
        "not re-derivable from the public record": 14
      },
      "recipe": {
        "none": 119
      },
      "setup.deps_source": {
        "none": 119
      },
      "setup.task_base.hash": {
        "none": 119
      },
      "setup.task_base.kind": {
        "none": 119
      },
      "stop_reason": {
        "none": 14
      },
      "task.base_repo": {
        "none": 14
      },
      "task.base_revision.hash": {
        "none": 119
      },
      "task.base_revision.kind": {
        "none": 119
      },
      "timestamps.attempts": {
        "none": 119
      },
      "timestamps.phases.develop.end_utc": {
        "none": 119
      },
      "timestamps.phases.develop.start_utc": {
        "none": 119
      },
      "timestamps.phases.gate.end_utc": {
        "none": 119
      },
      "timestamps.phases.gate.start_utc": {
        "none": 119
      },
      "timestamps.phases.grade.end_utc": {
        "none": 119
      },
      "timestamps.phases.grade.start_utc": {
        "none": 119
      },
      "timestamps.phases.plan.end_utc": {
        "none": 119
      },
      "timestamps.phases.plan.start_utc": {
        "none": 119
      },
      "timestamps.phases.review.end_utc": {
        "none": 119
      },
      "timestamps.phases.review.start_utc": {
        "none": 119
      },
      "timestamps.phases.setup.end_utc": {
        "none": 119
      },
      "timestamps.phases.setup.start_utc": {
        "none": 119
      },
      "timestamps.phases.shape.end_utc": {
        "none": 119
      },
      "timestamps.phases.shape.start_utc": {
        "none": 119
      },
      "timing.phases_s.develop": {
        "none": 119
      },
      "timing.phases_s.gate": {
        "none": 119
      },
      "timing.phases_s.grade": {
        "none": 15
      },
      "timing.phases_s.plan": {
        "none": 119
      },
      "timing.phases_s.review": {
        "none": 119
      },
      "timing.phases_s.setup": {
        "none": 119
      },
      "timing.phases_s.shape": {
        "none": 119
      },
      "tokens.phases.develop.cached_input": {
        "none": 119
      },
      "tokens.phases.develop.input": {
        "none": 119
      },
      "tokens.phases.develop.output": {
        "none": 119
      },
      "tokens.phases.develop.reasoning": {
        "none": 119
      },
      "tokens.phases.gate.cached_input": {
        "none": 119
      },
      "tokens.phases.gate.input": {
        "none": 119
      },
      "tokens.phases.gate.output": {
        "none": 119
      },
      "tokens.phases.gate.reasoning": {
        "none": 119
      },
      "tokens.phases.grade.cached_input": {
        "none": 14
      },
      "tokens.phases.grade.input": {
        "none": 14
      },
      "tokens.phases.grade.output": {
        "none": 14
      },
      "tokens.phases.grade.reasoning": {
        "none": 14
      },
      "tokens.phases.plan.cached_input": {
        "none": 119
      },
      "tokens.phases.plan.input": {
        "none": 119
      },
      "tokens.phases.plan.output": {
        "none": 119
      },
      "tokens.phases.plan.reasoning": {
        "none": 119
      },
      "tokens.phases.review.cached_input": {
        "none": 119
      },
      "tokens.phases.review.input": {
        "none": 119
      },
      "tokens.phases.review.output": {
        "none": 119
      },
      "tokens.phases.review.reasoning": {
        "none": 119
      },
      "tokens.phases.setup.cached_input": {
        "none": 119
      },
      "tokens.phases.setup.input": {
        "none": 119
      },
      "tokens.phases.setup.output": {
        "none": 119
      },
      "tokens.phases.setup.reasoning": {
        "none": 119
      },
      "tokens.phases.shape.cached_input": {
        "none": 119
      },
      "tokens.phases.shape.input": {
        "none": 119
      },
      "tokens.phases.shape.output": {
        "none": 119
      },
      "tokens.phases.shape.reasoning": {
        "none": 119
      },
      "tokens.total.cached_input": {
        "none": 119
      },
      "tokens.total.input": {
        "none": 119
      },
      "tokens.total.output": {
        "none": 119
      },
      "tokens.total.reasoning": {
        "none": 119
      },
      "tools.codex_cli": {
        "none": 119
      },
      "tools.grader": {
        "none": 119
      },
      "tools.runner": {
        "none": 119
      },
      "tools.toolchains.elixir": {
        "none": 119
      },
      "tools.toolchains.erlang": {
        "none": 119
      },
      "tools.toolchains.node": {
        "none": 119
      },
      "tools.toolchains.other_inventory": {
        "none": 119
      },
      "tools.toolchains.ruby": {
        "none": 119
      },
      "tools.toolchains.rust": {
        "none": 119
      }
    },
    "reconstructable": {}
  },
  "round": "r3"
}
```
