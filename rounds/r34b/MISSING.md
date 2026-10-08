# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 5,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Boundary telemetry not retained": 5
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Boundary telemetry not retained": 5
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 3,
      "reasons": {
        "Not available for ungraded delivery": 3
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 3,
      "reasons": {
        "Not available for ungraded delivery": 3
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 3,
      "reasons": {
        "Not available for ungraded delivery": 3
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 3,
      "reasons": {
        "Not available for ungraded delivery": 3
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Complete per-model billable vector unavailable": 2,
        "Not available for ungraded delivery": 3
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 3,
      "reasons": {
        "Not recorded in available public metadata": 3
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "No per-cell CPU allocation receipt": 2,
        "Not available for ungraded delivery": 3
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "No per-cell CPU receipt": 2,
        "Not available for ungraded delivery": 3
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "No per-cell kernel receipt": 2,
        "Not available for ungraded delivery": 3
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "No per-cell RAM receipt": 2,
        "Not available for ungraded delivery": 3
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Toolchain version/inventory not recorded": 2
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Toolchain version/inventory not recorded": 2
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Toolchain version/inventory not recorded": 2
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Toolchain version/inventory not recorded": 2
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Toolchain version/inventory not recorded": 2
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Toolchain version/inventory not recorded": 2
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 3,
      "reasons": {
        "No official grade in the public snapshot": 3
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 3,
      "reasons": {
        "No official grade in the public snapshot": 3
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 3,
      "reasons": {
        "No official grade in the public snapshot": 3
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 5,
      "reasons": {
        "No per-cell CPU receipt": 2,
        "Not available for ungraded delivery": 3
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 5,
      "reasons": {
        "No per-cell kernel receipt": 2,
        "Not available for ungraded delivery": 3
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 5,
      "reasons": {
        "No per-cell RAM receipt": 2,
        "Not available for ungraded delivery": 3
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 3,
      "reasons": {
        "Not available for ungraded delivery": 3
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 5,
      "reasons": {
        "No per-cell CPU allocation receipt": 2,
        "Not available for ungraded delivery": 3
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 3,
      "reasons": {
        "Ungraded delivery needs evidence audit": 3
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 3,
      "reasons": {
        "No captured cohort launch receipt": 3
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 3,
      "reasons": {
        "No audited ITT receipt": 3
      }
    },
    "model.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 3,
      "reasons": {
        "Not recorded in available public metadata": 3
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 3,
      "reasons": {
        "No official grade in the public snapshot": 3
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Not recorded in available public metadata": 2
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Dependency source not pinned per cell": 5
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 2
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Original base revision type not recorded per cell": 2
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 3,
      "reasons": {
        "No normalized stop receipt": 3
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 3,
      "reasons": {
        "Not available for ungraded delivery": 3
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 2
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Original base revision type not recorded per cell": 2
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Attempt boundary receipts unavailable": 5
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Phase wall not emitted or not separable": 2
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Phase wall not emitted or not separable": 2
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 3,
      "reasons": {
        "Not available for ungraded delivery": 3
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Phase wall not emitted or not separable": 2
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Phase wall not emitted or not separable": 2
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Phase wall not emitted or not separable": 2
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Phase wall not emitted or not separable": 2
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Per-phase token counter not emitted": 2
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Per-phase token counter not emitted": 2
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Per-phase token counter not emitted": 2
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Per-phase token counter not emitted": 2
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Per-phase token counter not emitted": 2
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Per-phase token counter not emitted": 2
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Per-phase token counter not emitted": 2
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Per-phase token counter not emitted": 2
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 3,
      "reasons": {
        "Not available for ungraded delivery": 3
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 3,
      "reasons": {
        "Not available for ungraded delivery": 3
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 3,
      "reasons": {
        "Not available for ungraded delivery": 3
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 3,
      "reasons": {
        "Not available for ungraded delivery": 3
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Per-phase token counter not emitted": 2
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Per-phase token counter not emitted": 2
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Per-phase token counter not emitted": 2
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Per-phase token counter not emitted": 2
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Per-phase token counter not emitted": 2
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Per-phase token counter not emitted": 2
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Per-phase token counter not emitted": 2
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Per-phase token counter not emitted": 2
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Per-phase token counter not emitted": 2
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Per-phase token counter not emitted": 2
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Per-phase token counter not emitted": 2
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Per-phase token counter not emitted": 2
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Per-phase token counter not emitted": 2
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Per-phase token counter not emitted": 2
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Per-phase token counter not emitted": 2
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Per-phase token counter not emitted": 2
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 2,
        "Usage counter unavailable": 3
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 2,
        "Usage counter unavailable": 3
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 2,
        "Usage counter unavailable": 3
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 2,
        "Usage counter unavailable": 3
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 2,
        "Not available for ungraded delivery": 3
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 2,
        "Not available for ungraded delivery": 3
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 2,
        "Not available for ungraded delivery": 3
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Toolchain version/inventory not recorded": 2
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Toolchain version/inventory not recorded": 2
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Toolchain version/inventory not recorded": 2
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Toolchain version/inventory not recorded": 2
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Toolchain version/inventory not recorded": 2
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 3,
        "Toolchain version/inventory not recorded": 2
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 5
      },
      "circumstances.load1_end": {
        "none": 5
      },
      "cost.accounting": {
        "none": 3
      },
      "cost.calculator_version": {
        "none": 3
      },
      "cost.long_context_reconciled": {
        "none": 3
      },
      "cost.price_table_version": {
        "none": 3
      },
      "cost.usd": {
        "none": 5
      },
      "effort.effective": {
        "none": 3
      },
      "environment.cores": {
        "none": 5
      },
      "environment.cpu_model": {
        "none": 5
      },
      "environment.kernel": {
        "none": 5
      },
      "environment.ram_gib": {
        "none": 5
      },
      "environment.toolchains.elixir": {
        "none": 5
      },
      "environment.toolchains.erlang": {
        "none": 5
      },
      "environment.toolchains.node": {
        "none": 5
      },
      "environment.toolchains.other_inventory": {
        "none": 5
      },
      "environment.toolchains.ruby": {
        "none": 5
      },
      "environment.toolchains.rust": {
        "none": 5
      },
      "grade.grader": {
        "not re-derivable from the public record": 3
      },
      "grade.tests_ran": {
        "not re-derivable from the public record": 3
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 3
      },
      "host.cpu": {
        "none": 5
      },
      "host.kernel": {
        "none": 5
      },
      "host.ram_gib": {
        "none": 5
      },
      "host.spec_ref": {
        "none": 3
      },
      "host.vcpu": {
        "none": 5
      },
      "itt.class": {
        "none": 3
      },
      "itt.cohort": {
        "none": 3
      },
      "itt.evidence_ref": {
        "none": 3
      },
      "model.effective": {
        "none": 3
      },
      "outcome": {
        "not re-derivable from the public record": 3
      },
      "recipe": {
        "none": 5
      },
      "setup.deps_source": {
        "none": 5
      },
      "setup.task_base.hash": {
        "none": 5
      },
      "setup.task_base.kind": {
        "none": 5
      },
      "stop_reason": {
        "none": 3
      },
      "task.base_repo": {
        "none": 3
      },
      "task.base_revision.hash": {
        "none": 5
      },
      "task.base_revision.kind": {
        "none": 5
      },
      "timestamps.attempts": {
        "none": 5
      },
      "timestamps.phases.develop.end_utc": {
        "none": 5
      },
      "timestamps.phases.develop.start_utc": {
        "none": 5
      },
      "timestamps.phases.gate.end_utc": {
        "none": 5
      },
      "timestamps.phases.gate.start_utc": {
        "none": 5
      },
      "timestamps.phases.grade.end_utc": {
        "none": 5
      },
      "timestamps.phases.grade.start_utc": {
        "none": 5
      },
      "timestamps.phases.plan.end_utc": {
        "none": 5
      },
      "timestamps.phases.plan.start_utc": {
        "none": 5
      },
      "timestamps.phases.review.end_utc": {
        "none": 5
      },
      "timestamps.phases.review.start_utc": {
        "none": 5
      },
      "timestamps.phases.setup.end_utc": {
        "none": 5
      },
      "timestamps.phases.setup.start_utc": {
        "none": 5
      },
      "timestamps.phases.shape.end_utc": {
        "none": 5
      },
      "timestamps.phases.shape.start_utc": {
        "none": 5
      },
      "timing.phases_s.develop": {
        "none": 5
      },
      "timing.phases_s.gate": {
        "none": 5
      },
      "timing.phases_s.grade": {
        "none": 3
      },
      "timing.phases_s.plan": {
        "none": 5
      },
      "timing.phases_s.review": {
        "none": 5
      },
      "timing.phases_s.setup": {
        "none": 5
      },
      "timing.phases_s.shape": {
        "none": 5
      },
      "tokens.phases.develop.cached_input": {
        "none": 5
      },
      "tokens.phases.develop.input": {
        "none": 5
      },
      "tokens.phases.develop.output": {
        "none": 5
      },
      "tokens.phases.develop.reasoning": {
        "none": 5
      },
      "tokens.phases.gate.cached_input": {
        "none": 5
      },
      "tokens.phases.gate.input": {
        "none": 5
      },
      "tokens.phases.gate.output": {
        "none": 5
      },
      "tokens.phases.gate.reasoning": {
        "none": 5
      },
      "tokens.phases.grade.cached_input": {
        "none": 3
      },
      "tokens.phases.grade.input": {
        "none": 3
      },
      "tokens.phases.grade.output": {
        "none": 3
      },
      "tokens.phases.grade.reasoning": {
        "none": 3
      },
      "tokens.phases.plan.cached_input": {
        "none": 5
      },
      "tokens.phases.plan.input": {
        "none": 5
      },
      "tokens.phases.plan.output": {
        "none": 5
      },
      "tokens.phases.plan.reasoning": {
        "none": 5
      },
      "tokens.phases.review.cached_input": {
        "none": 5
      },
      "tokens.phases.review.input": {
        "none": 5
      },
      "tokens.phases.review.output": {
        "none": 5
      },
      "tokens.phases.review.reasoning": {
        "none": 5
      },
      "tokens.phases.setup.cached_input": {
        "none": 5
      },
      "tokens.phases.setup.input": {
        "none": 5
      },
      "tokens.phases.setup.output": {
        "none": 5
      },
      "tokens.phases.setup.reasoning": {
        "none": 5
      },
      "tokens.phases.shape.cached_input": {
        "none": 5
      },
      "tokens.phases.shape.input": {
        "none": 5
      },
      "tokens.phases.shape.output": {
        "none": 5
      },
      "tokens.phases.shape.reasoning": {
        "none": 5
      },
      "tokens.total.cached_input": {
        "none": 5
      },
      "tokens.total.input": {
        "none": 5
      },
      "tokens.total.output": {
        "none": 5
      },
      "tokens.total.reasoning": {
        "none": 5
      },
      "tools.codex_cli": {
        "none": 5
      },
      "tools.grader": {
        "none": 5
      },
      "tools.runner": {
        "none": 5
      },
      "tools.toolchains.elixir": {
        "none": 5
      },
      "tools.toolchains.erlang": {
        "none": 5
      },
      "tools.toolchains.node": {
        "none": 5
      },
      "tools.toolchains.other_inventory": {
        "none": 5
      },
      "tools.toolchains.ruby": {
        "none": 5
      },
      "tools.toolchains.rust": {
        "none": 5
      }
    },
    "reconstructable": {}
  },
  "round": "r34b"
}
```
