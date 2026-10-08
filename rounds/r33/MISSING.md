# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 81,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Boundary telemetry not retained": 81
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Boundary telemetry not retained": 54
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 54
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Boundary telemetry not retained": 81
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "No matching controller samples retained": 54
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
      "count": 27,
      "reasons": {
        "Complete per-model billable vector unavailable": 21,
        "Not available for ungraded delivery": 6
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 4,
      "reasons": {
        "Not recorded in available public metadata": 4
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "No dated account-class receipt": 54
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "No per-cell CPU allocation receipt": 75,
        "Not available for ungraded delivery": 6
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "No per-cell CPU receipt": 75,
        "Not available for ungraded delivery": 6
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 27,
      "reasons": {
        "No per-cell kernel receipt": 21,
        "Not available for ungraded delivery": 6
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "No per-cell RAM receipt": 75,
        "Not available for ungraded delivery": 6
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 75
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 75
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 75
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 75
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 75
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 75
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
      "count": 6,
      "reasons": {
        "No official grade in the public snapshot": 6
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 6,
      "reasons": {
        "No official grade in the public snapshot": 6
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 81,
      "reasons": {
        "No per-cell CPU receipt": 75,
        "Not available for ungraded delivery": 6
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 27,
      "reasons": {
        "No per-cell kernel receipt": 21,
        "Not available for ungraded delivery": 6
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 81,
      "reasons": {
        "No per-cell RAM receipt": 75,
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
      "count": 81,
      "reasons": {
        "No per-cell CPU allocation receipt": 75,
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
      "count": 6,
      "reasons": {
        "No captured cohort launch receipt": 6
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 6,
      "reasons": {
        "No audited ITT receipt": 6
      }
    },
    "model.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 4,
      "reasons": {
        "Not recorded in available public metadata": 4
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
      "count": 27,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Not recorded in available public metadata": 21
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Dependency source not pinned per cell": 81
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 75
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Original base revision type not recorded per cell": 75
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 4,
      "reasons": {
        "No normalized stop receipt": 4
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
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 75
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Original base revision type not recorded per cell": 75
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Attempt boundary receipts unavailable": 81
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 27,
      "reasons": {
        "Absolute phase boundary not retained": 27
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 27,
      "reasons": {
        "Absolute phase boundary not retained": 27
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Absolute phase boundary not retained": 81
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Absolute phase boundary not retained": 81
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Absolute phase boundary not retained": 81
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Absolute phase boundary not retained": 81
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Absolute phase boundary not retained": 81
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Absolute phase boundary not retained": 81
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Absolute phase boundary not retained": 81
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Absolute phase boundary not retained": 81
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Absolute phase boundary not retained": 81
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Absolute phase boundary not retained": 81
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Absolute phase boundary not retained": 81
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Absolute phase boundary not retained": 81
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Phase wall not emitted or not separable": 75
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Phase wall not emitted or not separable": 75
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Phase wall not emitted or not separable": 75
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Phase wall not emitted or not separable": 75
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Phase wall not emitted or not separable": 75
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Phase wall not emitted or not separable": 75
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 75
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 75
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 75
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 75
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 75
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 75
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 75
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 75
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
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 75
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 75
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 75
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 75
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 75
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 75
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 75
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 75
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 75
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 75
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 75
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 75
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 75
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 75
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 75
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 75
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 21,
        "Usage counter unavailable": 4
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 21,
        "Usage counter unavailable": 4
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 21,
        "Usage counter unavailable": 4
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 21,
        "Usage counter unavailable": 4
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 27,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 21,
        "Not available for ungraded delivery": 6
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 75,
        "Not available for ungraded delivery": 6
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 75,
        "Not available for ungraded delivery": 6
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 75
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 75
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 75
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 75
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 75
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 81,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 75
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 81
      },
      "circumstances.concurrent_cells_end": {
        "none": 54
      },
      "circumstances.concurrent_cells_start": {
        "none": 54
      },
      "circumstances.load1_end": {
        "none": 81
      },
      "circumstances.load_samples": {
        "none": 54
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
        "none": 27
      },
      "effort.effective": {
        "none": 4
      },
      "environment.account_class": {
        "none": 54
      },
      "environment.cores": {
        "none": 81
      },
      "environment.cpu_model": {
        "none": 81
      },
      "environment.kernel": {
        "none": 27
      },
      "environment.ram_gib": {
        "none": 81
      },
      "environment.toolchains.elixir": {
        "none": 81
      },
      "environment.toolchains.erlang": {
        "none": 81
      },
      "environment.toolchains.node": {
        "none": 81
      },
      "environment.toolchains.other_inventory": {
        "none": 81
      },
      "environment.toolchains.ruby": {
        "none": 81
      },
      "environment.toolchains.rust": {
        "none": 81
      },
      "grade.grader": {
        "not re-derivable from the public record": 6
      },
      "grade.tests_ran": {
        "not re-derivable from the public record": 6
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 6
      },
      "host.cpu": {
        "none": 81
      },
      "host.kernel": {
        "none": 27
      },
      "host.ram_gib": {
        "none": 81
      },
      "host.spec_ref": {
        "none": 6
      },
      "host.vcpu": {
        "none": 81
      },
      "itt.class": {
        "none": 6
      },
      "itt.cohort": {
        "none": 6
      },
      "itt.evidence_ref": {
        "none": 6
      },
      "model.effective": {
        "none": 4
      },
      "outcome": {
        "not re-derivable from the public record": 6
      },
      "recipe": {
        "none": 27
      },
      "setup.deps_source": {
        "none": 81
      },
      "setup.task_base.hash": {
        "none": 81
      },
      "setup.task_base.kind": {
        "none": 81
      },
      "stop_reason": {
        "none": 4
      },
      "task.base_repo": {
        "none": 6
      },
      "task.base_revision.hash": {
        "none": 81
      },
      "task.base_revision.kind": {
        "none": 81
      },
      "timestamps.attempts": {
        "none": 81
      },
      "timestamps.phases.develop.end_utc": {
        "none": 27
      },
      "timestamps.phases.develop.start_utc": {
        "none": 27
      },
      "timestamps.phases.gate.end_utc": {
        "none": 81
      },
      "timestamps.phases.gate.start_utc": {
        "none": 81
      },
      "timestamps.phases.grade.end_utc": {
        "none": 81
      },
      "timestamps.phases.grade.start_utc": {
        "none": 81
      },
      "timestamps.phases.plan.end_utc": {
        "none": 81
      },
      "timestamps.phases.plan.start_utc": {
        "none": 81
      },
      "timestamps.phases.review.end_utc": {
        "none": 81
      },
      "timestamps.phases.review.start_utc": {
        "none": 81
      },
      "timestamps.phases.setup.end_utc": {
        "none": 81
      },
      "timestamps.phases.setup.start_utc": {
        "none": 81
      },
      "timestamps.phases.shape.end_utc": {
        "none": 81
      },
      "timestamps.phases.shape.start_utc": {
        "none": 81
      },
      "timing.phases_s.develop": {
        "none": 81
      },
      "timing.phases_s.gate": {
        "none": 81
      },
      "timing.phases_s.grade": {
        "none": 6
      },
      "timing.phases_s.plan": {
        "none": 81
      },
      "timing.phases_s.review": {
        "none": 81
      },
      "timing.phases_s.setup": {
        "none": 81
      },
      "timing.phases_s.shape": {
        "none": 81
      },
      "tokens.phases.develop.cached_input": {
        "none": 81
      },
      "tokens.phases.develop.input": {
        "none": 81
      },
      "tokens.phases.develop.output": {
        "none": 81
      },
      "tokens.phases.develop.reasoning": {
        "none": 81
      },
      "tokens.phases.gate.cached_input": {
        "none": 81
      },
      "tokens.phases.gate.input": {
        "none": 81
      },
      "tokens.phases.gate.output": {
        "none": 81
      },
      "tokens.phases.gate.reasoning": {
        "none": 81
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
        "none": 81
      },
      "tokens.phases.plan.input": {
        "none": 81
      },
      "tokens.phases.plan.output": {
        "none": 81
      },
      "tokens.phases.plan.reasoning": {
        "none": 81
      },
      "tokens.phases.review.cached_input": {
        "none": 81
      },
      "tokens.phases.review.input": {
        "none": 81
      },
      "tokens.phases.review.output": {
        "none": 81
      },
      "tokens.phases.review.reasoning": {
        "none": 81
      },
      "tokens.phases.setup.cached_input": {
        "none": 81
      },
      "tokens.phases.setup.input": {
        "none": 81
      },
      "tokens.phases.setup.output": {
        "none": 81
      },
      "tokens.phases.setup.reasoning": {
        "none": 81
      },
      "tokens.phases.shape.cached_input": {
        "none": 81
      },
      "tokens.phases.shape.input": {
        "none": 81
      },
      "tokens.phases.shape.output": {
        "none": 81
      },
      "tokens.phases.shape.reasoning": {
        "none": 81
      },
      "tokens.total.cached_input": {
        "none": 25
      },
      "tokens.total.input": {
        "none": 25
      },
      "tokens.total.output": {
        "none": 25
      },
      "tokens.total.reasoning": {
        "none": 25
      },
      "tools.codex_cli": {
        "none": 27
      },
      "tools.grader": {
        "none": 81
      },
      "tools.runner": {
        "none": 81
      },
      "tools.toolchains.elixir": {
        "none": 81
      },
      "tools.toolchains.erlang": {
        "none": 81
      },
      "tools.toolchains.node": {
        "none": 81
      },
      "tools.toolchains.other_inventory": {
        "none": 81
      },
      "tools.toolchains.ruby": {
        "none": 81
      },
      "tools.toolchains.rust": {
        "none": 81
      }
    },
    "reconstructable": {}
  },
  "round": "r33"
}
```
