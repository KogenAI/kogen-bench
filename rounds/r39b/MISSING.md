# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 24,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Boundary telemetry not retained": 24
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Boundary telemetry not retained": 24
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 13,
      "reasons": {
        "Not available for ungraded delivery": 13
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 13,
      "reasons": {
        "Not available for ungraded delivery": 13
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 13,
      "reasons": {
        "Not available for ungraded delivery": 13
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 13,
      "reasons": {
        "Not available for ungraded delivery": 13
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Complete per-model billable vector unavailable": 11,
        "Not available for ungraded delivery": 13
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not recorded in available public metadata": 1
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "No per-cell CPU allocation receipt": 11,
        "Not available for ungraded delivery": 13
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "No per-cell CPU receipt": 11,
        "Not available for ungraded delivery": 13
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "No per-cell kernel receipt": 11,
        "Not available for ungraded delivery": 13
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "No per-cell RAM receipt": 11,
        "Not available for ungraded delivery": 13
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Toolchain version/inventory not recorded": 11
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Toolchain version/inventory not recorded": 11
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Toolchain version/inventory not recorded": 11
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Toolchain version/inventory not recorded": 11
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Toolchain version/inventory not recorded": 11
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Toolchain version/inventory not recorded": 11
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 13,
      "reasons": {
        "No official grade in the public snapshot": 13
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 13,
      "reasons": {
        "No official grade in the public snapshot": 13
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 13,
      "reasons": {
        "No official grade in the public snapshot": 13
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 24,
      "reasons": {
        "No per-cell CPU receipt": 11,
        "Not available for ungraded delivery": 13
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 24,
      "reasons": {
        "No per-cell kernel receipt": 11,
        "Not available for ungraded delivery": 13
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 24,
      "reasons": {
        "No per-cell RAM receipt": 11,
        "Not available for ungraded delivery": 13
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 13,
      "reasons": {
        "Not available for ungraded delivery": 13
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 24,
      "reasons": {
        "No per-cell CPU allocation receipt": 11,
        "Not available for ungraded delivery": 13
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 13,
      "reasons": {
        "Ungraded delivery needs evidence audit": 13
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 13,
      "reasons": {
        "No captured cohort launch receipt": 13
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 13,
      "reasons": {
        "No audited ITT receipt": 13
      }
    },
    "model.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not recorded in available public metadata": 1
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 13,
      "reasons": {
        "No official grade in the public snapshot": 13
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Not recorded in available public metadata": 11
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Dependency source not pinned per cell": 24
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 11
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Original base revision type not recorded per cell": 11
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 13,
      "reasons": {
        "No normalized stop receipt": 13
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 13,
      "reasons": {
        "Not available for ungraded delivery": 13
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 11
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Original base revision type not recorded per cell": 11
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Attempt boundary receipts unavailable": 24
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Absolute phase boundary not retained": 24
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Absolute phase boundary not retained": 24
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Absolute phase boundary not retained": 24
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Absolute phase boundary not retained": 24
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Absolute phase boundary not retained": 24
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Absolute phase boundary not retained": 24
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Absolute phase boundary not retained": 24
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Absolute phase boundary not retained": 24
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Absolute phase boundary not retained": 24
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Absolute phase boundary not retained": 24
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Absolute phase boundary not retained": 24
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Absolute phase boundary not retained": 24
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Absolute phase boundary not retained": 24
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Absolute phase boundary not retained": 24
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Phase wall not emitted or not separable": 11
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Phase wall not emitted or not separable": 11
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 13,
      "reasons": {
        "Not available for ungraded delivery": 13
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Phase wall not emitted or not separable": 11
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Phase wall not emitted or not separable": 11
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Phase wall not emitted or not separable": 11
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Phase wall not emitted or not separable": 11
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Per-phase token counter not emitted": 11
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Per-phase token counter not emitted": 11
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Per-phase token counter not emitted": 11
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Per-phase token counter not emitted": 11
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Per-phase token counter not emitted": 11
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Per-phase token counter not emitted": 11
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Per-phase token counter not emitted": 11
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Per-phase token counter not emitted": 11
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 13,
      "reasons": {
        "Not available for ungraded delivery": 13
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 13,
      "reasons": {
        "Not available for ungraded delivery": 13
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 13,
      "reasons": {
        "Not available for ungraded delivery": 13
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 13,
      "reasons": {
        "Not available for ungraded delivery": 13
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Per-phase token counter not emitted": 11
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Per-phase token counter not emitted": 11
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Per-phase token counter not emitted": 11
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Per-phase token counter not emitted": 11
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Per-phase token counter not emitted": 11
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Per-phase token counter not emitted": 11
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Per-phase token counter not emitted": 11
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Per-phase token counter not emitted": 11
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Per-phase token counter not emitted": 11
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Per-phase token counter not emitted": 11
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Per-phase token counter not emitted": 11
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Per-phase token counter not emitted": 11
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Per-phase token counter not emitted": 11
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Per-phase token counter not emitted": 11
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Per-phase token counter not emitted": 11
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Per-phase token counter not emitted": 11
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 11,
        "Usage counter unavailable": 1
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 11,
        "Usage counter unavailable": 1
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 11,
        "Usage counter unavailable": 1
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 11,
        "Usage counter unavailable": 1
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 11,
        "Not available for ungraded delivery": 13
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 11,
        "Not available for ungraded delivery": 13
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 11,
        "Not available for ungraded delivery": 13
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Toolchain version/inventory not recorded": 11
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Toolchain version/inventory not recorded": 11
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Toolchain version/inventory not recorded": 11
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Toolchain version/inventory not recorded": 11
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Toolchain version/inventory not recorded": 11
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 13,
        "Toolchain version/inventory not recorded": 11
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 24
      },
      "circumstances.load1_end": {
        "none": 24
      },
      "cost.accounting": {
        "none": 13
      },
      "cost.calculator_version": {
        "none": 13
      },
      "cost.long_context_reconciled": {
        "none": 13
      },
      "cost.price_table_version": {
        "none": 13
      },
      "cost.usd": {
        "none": 24
      },
      "effort.effective": {
        "none": 1
      },
      "environment.cores": {
        "none": 24
      },
      "environment.cpu_model": {
        "none": 24
      },
      "environment.kernel": {
        "none": 24
      },
      "environment.ram_gib": {
        "none": 24
      },
      "environment.toolchains.elixir": {
        "none": 24
      },
      "environment.toolchains.erlang": {
        "none": 24
      },
      "environment.toolchains.node": {
        "none": 24
      },
      "environment.toolchains.other_inventory": {
        "none": 24
      },
      "environment.toolchains.ruby": {
        "none": 24
      },
      "environment.toolchains.rust": {
        "none": 24
      },
      "grade.grader": {
        "not re-derivable from the public record": 13
      },
      "grade.tests_ran": {
        "not re-derivable from the public record": 13
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 13
      },
      "host.cpu": {
        "none": 24
      },
      "host.kernel": {
        "none": 24
      },
      "host.ram_gib": {
        "none": 24
      },
      "host.spec_ref": {
        "none": 13
      },
      "host.vcpu": {
        "none": 24
      },
      "itt.class": {
        "none": 13
      },
      "itt.cohort": {
        "none": 13
      },
      "itt.evidence_ref": {
        "none": 13
      },
      "model.effective": {
        "none": 1
      },
      "outcome": {
        "not re-derivable from the public record": 13
      },
      "recipe": {
        "none": 24
      },
      "setup.deps_source": {
        "none": 24
      },
      "setup.task_base.hash": {
        "none": 24
      },
      "setup.task_base.kind": {
        "none": 24
      },
      "stop_reason": {
        "none": 13
      },
      "task.base_repo": {
        "none": 13
      },
      "task.base_revision.hash": {
        "none": 24
      },
      "task.base_revision.kind": {
        "none": 24
      },
      "timestamps.attempts": {
        "none": 24
      },
      "timestamps.phases.develop.end_utc": {
        "none": 24
      },
      "timestamps.phases.develop.start_utc": {
        "none": 24
      },
      "timestamps.phases.gate.end_utc": {
        "none": 24
      },
      "timestamps.phases.gate.start_utc": {
        "none": 24
      },
      "timestamps.phases.grade.end_utc": {
        "none": 24
      },
      "timestamps.phases.grade.start_utc": {
        "none": 24
      },
      "timestamps.phases.plan.end_utc": {
        "none": 24
      },
      "timestamps.phases.plan.start_utc": {
        "none": 24
      },
      "timestamps.phases.review.end_utc": {
        "none": 24
      },
      "timestamps.phases.review.start_utc": {
        "none": 24
      },
      "timestamps.phases.setup.end_utc": {
        "none": 24
      },
      "timestamps.phases.setup.start_utc": {
        "none": 24
      },
      "timestamps.phases.shape.end_utc": {
        "none": 24
      },
      "timestamps.phases.shape.start_utc": {
        "none": 24
      },
      "timing.phases_s.develop": {
        "none": 24
      },
      "timing.phases_s.gate": {
        "none": 24
      },
      "timing.phases_s.grade": {
        "none": 13
      },
      "timing.phases_s.plan": {
        "none": 24
      },
      "timing.phases_s.review": {
        "none": 24
      },
      "timing.phases_s.setup": {
        "none": 24
      },
      "timing.phases_s.shape": {
        "none": 24
      },
      "tokens.phases.develop.cached_input": {
        "none": 24
      },
      "tokens.phases.develop.input": {
        "none": 24
      },
      "tokens.phases.develop.output": {
        "none": 24
      },
      "tokens.phases.develop.reasoning": {
        "none": 24
      },
      "tokens.phases.gate.cached_input": {
        "none": 24
      },
      "tokens.phases.gate.input": {
        "none": 24
      },
      "tokens.phases.gate.output": {
        "none": 24
      },
      "tokens.phases.gate.reasoning": {
        "none": 24
      },
      "tokens.phases.grade.cached_input": {
        "none": 13
      },
      "tokens.phases.grade.input": {
        "none": 13
      },
      "tokens.phases.grade.output": {
        "none": 13
      },
      "tokens.phases.grade.reasoning": {
        "none": 13
      },
      "tokens.phases.plan.cached_input": {
        "none": 24
      },
      "tokens.phases.plan.input": {
        "none": 24
      },
      "tokens.phases.plan.output": {
        "none": 24
      },
      "tokens.phases.plan.reasoning": {
        "none": 24
      },
      "tokens.phases.review.cached_input": {
        "none": 24
      },
      "tokens.phases.review.input": {
        "none": 24
      },
      "tokens.phases.review.output": {
        "none": 24
      },
      "tokens.phases.review.reasoning": {
        "none": 24
      },
      "tokens.phases.setup.cached_input": {
        "none": 24
      },
      "tokens.phases.setup.input": {
        "none": 24
      },
      "tokens.phases.setup.output": {
        "none": 24
      },
      "tokens.phases.setup.reasoning": {
        "none": 24
      },
      "tokens.phases.shape.cached_input": {
        "none": 24
      },
      "tokens.phases.shape.input": {
        "none": 24
      },
      "tokens.phases.shape.output": {
        "none": 24
      },
      "tokens.phases.shape.reasoning": {
        "none": 24
      },
      "tokens.total.cached_input": {
        "none": 12
      },
      "tokens.total.input": {
        "none": 12
      },
      "tokens.total.output": {
        "none": 12
      },
      "tokens.total.reasoning": {
        "none": 12
      },
      "tools.codex_cli": {
        "none": 24
      },
      "tools.grader": {
        "none": 24
      },
      "tools.runner": {
        "none": 24
      },
      "tools.toolchains.elixir": {
        "none": 24
      },
      "tools.toolchains.erlang": {
        "none": 24
      },
      "tools.toolchains.node": {
        "none": 24
      },
      "tools.toolchains.other_inventory": {
        "none": 24
      },
      "tools.toolchains.ruby": {
        "none": 24
      },
      "tools.toolchains.rust": {
        "none": 24
      }
    },
    "reconstructable": {}
  },
  "round": "r39b"
}
```
