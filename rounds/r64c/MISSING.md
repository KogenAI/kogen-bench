# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 102,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Boundary telemetry not retained": 102
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Boundary telemetry not retained": 102
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 12
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 12
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 12
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 12
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 102,
      "reasons": {
        "Complete per-model billable vector unavailable": 90,
        "Not available for ungraded delivery": 12
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "No per-cell CPU allocation receipt": 90,
        "Not available for ungraded delivery": 12
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "No per-cell CPU receipt": 90,
        "Not available for ungraded delivery": 12
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "No per-cell kernel receipt": 90,
        "Not available for ungraded delivery": 12
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "No per-cell RAM receipt": 90,
        "Not available for ungraded delivery": 12
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Toolchain version/inventory not recorded": 90
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Toolchain version/inventory not recorded": 90
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Toolchain version/inventory not recorded": 90
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Toolchain version/inventory not recorded": 90
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Toolchain version/inventory not recorded": 90
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Toolchain version/inventory not recorded": 90
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 12,
      "reasons": {
        "No official grade in the public snapshot": 12
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 13,
      "reasons": {
        "Boolean receipt not recorded": 1,
        "No official grade in the public snapshot": 12
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 12,
      "reasons": {
        "No official grade in the public snapshot": 12
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 102,
      "reasons": {
        "No per-cell CPU receipt": 90,
        "Not available for ungraded delivery": 12
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 102,
      "reasons": {
        "No per-cell kernel receipt": 90,
        "Not available for ungraded delivery": 12
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 102,
      "reasons": {
        "No per-cell RAM receipt": 90,
        "Not available for ungraded delivery": 12
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 12
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 102,
      "reasons": {
        "No per-cell CPU allocation receipt": 90,
        "Not available for ungraded delivery": 12
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 12,
      "reasons": {
        "Ungraded delivery needs evidence audit": 12
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 12,
      "reasons": {
        "No captured cohort launch receipt": 12
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 12,
      "reasons": {
        "No audited ITT receipt": 12
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 16,
      "reasons": {
        "No official grade in the public snapshot": 12,
        "Official result outside standard outcome classes": 4
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Not recorded in available public metadata": 90
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Dependency source not pinned per cell": 102
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 90
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Original base revision type not recorded per cell": 90
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 11,
      "reasons": {
        "No normalized stop receipt": 11
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 12
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 90
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Original base revision type not recorded per cell": 90
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Attempt boundary receipts unavailable": 102
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Absolute phase boundary not retained": 102
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Absolute phase boundary not retained": 102
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Absolute phase boundary not retained": 102
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Absolute phase boundary not retained": 102
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Absolute phase boundary not retained": 102
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Absolute phase boundary not retained": 102
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Absolute phase boundary not retained": 102
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Absolute phase boundary not retained": 102
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Absolute phase boundary not retained": 102
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Absolute phase boundary not retained": 102
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Absolute phase boundary not retained": 102
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Absolute phase boundary not retained": 102
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Absolute phase boundary not retained": 102
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Absolute phase boundary not retained": 102
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Phase wall not emitted or not separable": 90
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Phase wall not emitted or not separable": 90
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 13,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Phase wall not emitted or not separable": 1
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Phase wall not emitted or not separable": 90
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Phase wall not emitted or not separable": 90
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Phase wall not emitted or not separable": 90
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Phase wall not emitted or not separable": 90
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 12
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 12
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 12
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 12
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 90,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 90
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 90,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 90
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 90,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 90
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 90,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 90
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 90,
        "Not available for ungraded delivery": 12
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 90,
        "Not available for ungraded delivery": 12
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 90,
        "Not available for ungraded delivery": 12
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Toolchain version/inventory not recorded": 90
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Toolchain version/inventory not recorded": 90
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Toolchain version/inventory not recorded": 90
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Toolchain version/inventory not recorded": 90
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Toolchain version/inventory not recorded": 90
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Toolchain version/inventory not recorded": 90
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 102
      },
      "circumstances.load1_end": {
        "none": 102
      },
      "cost.accounting": {
        "none": 12
      },
      "cost.calculator_version": {
        "none": 12
      },
      "cost.long_context_reconciled": {
        "none": 12
      },
      "cost.price_table_version": {
        "none": 12
      },
      "cost.usd": {
        "none": 102
      },
      "environment.cores": {
        "none": 102
      },
      "environment.cpu_model": {
        "none": 102
      },
      "environment.kernel": {
        "none": 102
      },
      "environment.ram_gib": {
        "none": 102
      },
      "environment.toolchains.elixir": {
        "none": 102
      },
      "environment.toolchains.erlang": {
        "none": 102
      },
      "environment.toolchains.node": {
        "none": 102
      },
      "environment.toolchains.other_inventory": {
        "none": 102
      },
      "environment.toolchains.ruby": {
        "none": 102
      },
      "environment.toolchains.rust": {
        "none": 102
      },
      "grade.grader": {
        "not re-derivable from the public record": 12
      },
      "grade.tests_ran": {
        "none": 1,
        "not re-derivable from the public record": 12
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 12
      },
      "host.cpu": {
        "none": 102
      },
      "host.kernel": {
        "none": 102
      },
      "host.ram_gib": {
        "none": 102
      },
      "host.spec_ref": {
        "none": 12
      },
      "host.vcpu": {
        "none": 102
      },
      "itt.class": {
        "none": 12
      },
      "itt.cohort": {
        "none": 12
      },
      "itt.evidence_ref": {
        "none": 12
      },
      "outcome": {
        "none": 4,
        "not re-derivable from the public record": 12
      },
      "recipe": {
        "none": 102
      },
      "setup.deps_source": {
        "none": 102
      },
      "setup.task_base.hash": {
        "none": 102
      },
      "setup.task_base.kind": {
        "none": 102
      },
      "stop_reason": {
        "none": 11
      },
      "task.base_repo": {
        "none": 12
      },
      "task.base_revision.hash": {
        "none": 102
      },
      "task.base_revision.kind": {
        "none": 102
      },
      "timestamps.attempts": {
        "none": 102
      },
      "timestamps.phases.develop.end_utc": {
        "none": 102
      },
      "timestamps.phases.develop.start_utc": {
        "none": 102
      },
      "timestamps.phases.gate.end_utc": {
        "none": 102
      },
      "timestamps.phases.gate.start_utc": {
        "none": 102
      },
      "timestamps.phases.grade.end_utc": {
        "none": 102
      },
      "timestamps.phases.grade.start_utc": {
        "none": 102
      },
      "timestamps.phases.plan.end_utc": {
        "none": 102
      },
      "timestamps.phases.plan.start_utc": {
        "none": 102
      },
      "timestamps.phases.review.end_utc": {
        "none": 102
      },
      "timestamps.phases.review.start_utc": {
        "none": 102
      },
      "timestamps.phases.setup.end_utc": {
        "none": 102
      },
      "timestamps.phases.setup.start_utc": {
        "none": 102
      },
      "timestamps.phases.shape.end_utc": {
        "none": 102
      },
      "timestamps.phases.shape.start_utc": {
        "none": 102
      },
      "timing.phases_s.develop": {
        "none": 102
      },
      "timing.phases_s.gate": {
        "none": 102
      },
      "timing.phases_s.grade": {
        "none": 13
      },
      "timing.phases_s.plan": {
        "none": 102
      },
      "timing.phases_s.review": {
        "none": 102
      },
      "timing.phases_s.setup": {
        "none": 102
      },
      "timing.phases_s.shape": {
        "none": 102
      },
      "tokens.phases.develop.cached_input": {
        "none": 102
      },
      "tokens.phases.develop.input": {
        "none": 102
      },
      "tokens.phases.develop.output": {
        "none": 102
      },
      "tokens.phases.develop.reasoning": {
        "none": 102
      },
      "tokens.phases.gate.cached_input": {
        "none": 102
      },
      "tokens.phases.gate.input": {
        "none": 102
      },
      "tokens.phases.gate.output": {
        "none": 102
      },
      "tokens.phases.gate.reasoning": {
        "none": 102
      },
      "tokens.phases.grade.cached_input": {
        "none": 12
      },
      "tokens.phases.grade.input": {
        "none": 12
      },
      "tokens.phases.grade.output": {
        "none": 12
      },
      "tokens.phases.grade.reasoning": {
        "none": 12
      },
      "tokens.phases.plan.cached_input": {
        "none": 102
      },
      "tokens.phases.plan.input": {
        "none": 102
      },
      "tokens.phases.plan.output": {
        "none": 102
      },
      "tokens.phases.plan.reasoning": {
        "none": 102
      },
      "tokens.phases.review.cached_input": {
        "none": 102
      },
      "tokens.phases.review.input": {
        "none": 102
      },
      "tokens.phases.review.output": {
        "none": 102
      },
      "tokens.phases.review.reasoning": {
        "none": 102
      },
      "tokens.phases.setup.cached_input": {
        "none": 102
      },
      "tokens.phases.setup.input": {
        "none": 102
      },
      "tokens.phases.setup.output": {
        "none": 102
      },
      "tokens.phases.setup.reasoning": {
        "none": 102
      },
      "tokens.phases.shape.cached_input": {
        "none": 102
      },
      "tokens.phases.shape.input": {
        "none": 102
      },
      "tokens.phases.shape.output": {
        "none": 102
      },
      "tokens.phases.shape.reasoning": {
        "none": 102
      },
      "tokens.total.cached_input": {
        "none": 90
      },
      "tokens.total.input": {
        "none": 90
      },
      "tokens.total.output": {
        "none": 90
      },
      "tokens.total.reasoning": {
        "none": 90
      },
      "tools.codex_cli": {
        "none": 102
      },
      "tools.grader": {
        "none": 102
      },
      "tools.runner": {
        "none": 102
      },
      "tools.toolchains.elixir": {
        "none": 102
      },
      "tools.toolchains.erlang": {
        "none": 102
      },
      "tools.toolchains.node": {
        "none": 102
      },
      "tools.toolchains.other_inventory": {
        "none": 102
      },
      "tools.toolchains.ruby": {
        "none": 102
      },
      "tools.toolchains.rust": {
        "none": 102
      }
    },
    "reconstructable": {}
  },
  "publication_reconciliation": {
    "disposition": "Keep this cost-tuning capture separate from r64/r64b/r64d/r64e. Public cells support only the page-level export accounting; historical cost and pass-rate claims remain unreconciled.",
    "original_execution_command": "not recorded in the public snapshot",
    "harness_source_commit": "absent; tools.harness values are wrapper fingerprints",
    "kogen_source_commit": "Public records mark the Kogen product commit not applicable for these harness records.",
    "raw_public_records": [
      "results/run-records/r64c.jsonl",
      "results/cells.jsonl"
    ],
    "public_record_rebuild": "python3 reproduce/export_results.py; python3 reproduce/build_records.py; python3 reproduce/validate_round.py --round r64c"
  },
  "round": "r64c"
}
```
