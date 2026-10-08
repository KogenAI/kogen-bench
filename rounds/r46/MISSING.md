# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 66,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Boundary telemetry not retained": 66
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Boundary telemetry not retained": 15
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 15
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Boundary telemetry not retained": 66
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "No matching controller samples retained": 16
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Complete per-model billable vector unavailable": 65,
        "Not available for ungraded delivery": 1
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "No dated account-class receipt": 15
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "No per-cell CPU allocation receipt": 65,
        "Not available for ungraded delivery": 1
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "No per-cell CPU receipt": 65,
        "Not available for ungraded delivery": 1
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 51,
      "reasons": {
        "No per-cell kernel receipt": 50,
        "Not available for ungraded delivery": 1
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "No per-cell RAM receipt": 65,
        "Not available for ungraded delivery": 1
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 65
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 65
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 65
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 65
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 65
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 65
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 1,
      "reasons": {
        "No official grade in the public snapshot": 1
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 3,
      "reasons": {
        "Boolean receipt not recorded": 2,
        "No official grade in the public snapshot": 1
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 1,
      "reasons": {
        "No official grade in the public snapshot": 1
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 66,
      "reasons": {
        "No per-cell CPU receipt": 65,
        "Not available for ungraded delivery": 1
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 51,
      "reasons": {
        "No per-cell kernel receipt": 50,
        "Not available for ungraded delivery": 1
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 66,
      "reasons": {
        "No per-cell RAM receipt": 65,
        "Not available for ungraded delivery": 1
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 66,
      "reasons": {
        "No per-cell CPU allocation receipt": 65,
        "Not available for ungraded delivery": 1
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 1,
      "reasons": {
        "Ungraded delivery needs evidence audit": 1
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 1,
      "reasons": {
        "No captured cohort launch receipt": 1
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 1,
      "reasons": {
        "No audited ITT receipt": 1
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 1,
      "reasons": {
        "No official grade in the public snapshot": 1
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Not recorded in available public metadata": 65
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Dependency source not pinned per cell": 66
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 51,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 50
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 51,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Original base revision type not recorded per cell": 50
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 1,
      "reasons": {
        "No normalized stop receipt": 1
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 51,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 50
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 51,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Original base revision type not recorded per cell": 50
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Attempt boundary receipts unavailable": 66
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Absolute phase boundary not retained": 66
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Absolute phase boundary not retained": 66
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Absolute phase boundary not retained": 66
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Absolute phase boundary not retained": 66
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Absolute phase boundary not retained": 66
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Absolute phase boundary not retained": 66
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Absolute phase boundary not retained": 66
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Absolute phase boundary not retained": 66
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Absolute phase boundary not retained": 66
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Absolute phase boundary not retained": 66
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Absolute phase boundary not retained": 66
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Absolute phase boundary not retained": 66
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Absolute phase boundary not retained": 66
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Absolute phase boundary not retained": 66
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Phase wall not emitted or not separable": 65
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Phase wall not emitted or not separable": 65
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 3,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Phase wall not emitted or not separable": 2
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Phase wall not emitted or not separable": 65
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Phase wall not emitted or not separable": 65
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Phase wall not emitted or not separable": 65
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Phase wall not emitted or not separable": 65
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 65
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 65
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 65
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 65
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 65
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 65
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 65
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 65
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 65
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 65
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 65
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 65
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 65
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 65
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 65
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 65
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 65
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 65
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 65
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 65
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 65
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 65
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 65
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 65
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 65,
        "Usage counter unavailable": 1
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 65,
        "Usage counter unavailable": 1
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 65,
        "Usage counter unavailable": 1
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 66,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 65,
        "Usage counter unavailable": 1
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 65,
        "Not available for ungraded delivery": 1
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 65,
        "Not available for ungraded delivery": 1
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 65,
        "Not available for ungraded delivery": 1
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 65
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 65
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 65
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 65
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 65
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 66,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 65
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 66
      },
      "circumstances.concurrent_cells_end": {
        "none": 15
      },
      "circumstances.concurrent_cells_start": {
        "none": 15
      },
      "circumstances.load1_end": {
        "none": 66
      },
      "circumstances.load_samples": {
        "none": 16
      },
      "cost.accounting": {
        "none": 1
      },
      "cost.calculator_version": {
        "none": 1
      },
      "cost.long_context_reconciled": {
        "none": 1
      },
      "cost.price_table_version": {
        "none": 1
      },
      "cost.usd": {
        "none": 66
      },
      "environment.account_class": {
        "none": 15
      },
      "environment.cores": {
        "none": 66
      },
      "environment.cpu_model": {
        "none": 66
      },
      "environment.kernel": {
        "none": 51
      },
      "environment.ram_gib": {
        "none": 66
      },
      "environment.toolchains.elixir": {
        "none": 66
      },
      "environment.toolchains.erlang": {
        "none": 66
      },
      "environment.toolchains.node": {
        "none": 66
      },
      "environment.toolchains.other_inventory": {
        "none": 66
      },
      "environment.toolchains.ruby": {
        "none": 66
      },
      "environment.toolchains.rust": {
        "none": 66
      },
      "grade.grader": {
        "not re-derivable from the public record": 1
      },
      "grade.tests_ran": {
        "none": 2,
        "not re-derivable from the public record": 1
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 1
      },
      "host.cpu": {
        "none": 66
      },
      "host.kernel": {
        "none": 51
      },
      "host.ram_gib": {
        "none": 66
      },
      "host.spec_ref": {
        "none": 1
      },
      "host.vcpu": {
        "none": 66
      },
      "itt.class": {
        "none": 1
      },
      "itt.cohort": {
        "none": 1
      },
      "itt.evidence_ref": {
        "none": 1
      },
      "outcome": {
        "not re-derivable from the public record": 1
      },
      "recipe": {
        "none": 66
      },
      "setup.deps_source": {
        "none": 66
      },
      "setup.task_base.hash": {
        "none": 51
      },
      "setup.task_base.kind": {
        "none": 51
      },
      "stop_reason": {
        "none": 1
      },
      "task.base_repo": {
        "none": 1
      },
      "task.base_revision.hash": {
        "none": 51
      },
      "task.base_revision.kind": {
        "none": 51
      },
      "timestamps.attempts": {
        "none": 66
      },
      "timestamps.phases.develop.end_utc": {
        "none": 66
      },
      "timestamps.phases.develop.start_utc": {
        "none": 66
      },
      "timestamps.phases.gate.end_utc": {
        "none": 66
      },
      "timestamps.phases.gate.start_utc": {
        "none": 66
      },
      "timestamps.phases.grade.end_utc": {
        "none": 66
      },
      "timestamps.phases.grade.start_utc": {
        "none": 66
      },
      "timestamps.phases.plan.end_utc": {
        "none": 66
      },
      "timestamps.phases.plan.start_utc": {
        "none": 66
      },
      "timestamps.phases.review.end_utc": {
        "none": 66
      },
      "timestamps.phases.review.start_utc": {
        "none": 66
      },
      "timestamps.phases.setup.end_utc": {
        "none": 66
      },
      "timestamps.phases.setup.start_utc": {
        "none": 66
      },
      "timestamps.phases.shape.end_utc": {
        "none": 66
      },
      "timestamps.phases.shape.start_utc": {
        "none": 66
      },
      "timing.phases_s.develop": {
        "none": 66
      },
      "timing.phases_s.gate": {
        "none": 66
      },
      "timing.phases_s.grade": {
        "none": 3
      },
      "timing.phases_s.plan": {
        "none": 66
      },
      "timing.phases_s.review": {
        "none": 66
      },
      "timing.phases_s.setup": {
        "none": 66
      },
      "timing.phases_s.shape": {
        "none": 66
      },
      "tokens.phases.develop.cached_input": {
        "none": 66
      },
      "tokens.phases.develop.input": {
        "none": 66
      },
      "tokens.phases.develop.output": {
        "none": 66
      },
      "tokens.phases.develop.reasoning": {
        "none": 66
      },
      "tokens.phases.gate.cached_input": {
        "none": 66
      },
      "tokens.phases.gate.input": {
        "none": 66
      },
      "tokens.phases.gate.output": {
        "none": 66
      },
      "tokens.phases.gate.reasoning": {
        "none": 66
      },
      "tokens.phases.grade.cached_input": {
        "none": 1
      },
      "tokens.phases.grade.input": {
        "none": 1
      },
      "tokens.phases.grade.output": {
        "none": 1
      },
      "tokens.phases.grade.reasoning": {
        "none": 1
      },
      "tokens.phases.plan.cached_input": {
        "none": 66
      },
      "tokens.phases.plan.input": {
        "none": 66
      },
      "tokens.phases.plan.output": {
        "none": 66
      },
      "tokens.phases.plan.reasoning": {
        "none": 66
      },
      "tokens.phases.review.cached_input": {
        "none": 66
      },
      "tokens.phases.review.input": {
        "none": 66
      },
      "tokens.phases.review.output": {
        "none": 66
      },
      "tokens.phases.review.reasoning": {
        "none": 66
      },
      "tokens.phases.setup.cached_input": {
        "none": 66
      },
      "tokens.phases.setup.input": {
        "none": 66
      },
      "tokens.phases.setup.output": {
        "none": 66
      },
      "tokens.phases.setup.reasoning": {
        "none": 66
      },
      "tokens.phases.shape.cached_input": {
        "none": 66
      },
      "tokens.phases.shape.input": {
        "none": 66
      },
      "tokens.phases.shape.output": {
        "none": 66
      },
      "tokens.phases.shape.reasoning": {
        "none": 66
      },
      "tokens.total.cached_input": {
        "none": 66
      },
      "tokens.total.input": {
        "none": 66
      },
      "tokens.total.output": {
        "none": 66
      },
      "tokens.total.reasoning": {
        "none": 66
      },
      "tools.codex_cli": {
        "none": 66
      },
      "tools.grader": {
        "none": 66
      },
      "tools.runner": {
        "none": 66
      },
      "tools.toolchains.elixir": {
        "none": 66
      },
      "tools.toolchains.erlang": {
        "none": 66
      },
      "tools.toolchains.node": {
        "none": 66
      },
      "tools.toolchains.other_inventory": {
        "none": 66
      },
      "tools.toolchains.ruby": {
        "none": 66
      },
      "tools.toolchains.rust": {
        "none": 66
      }
    },
    "reconstructable": {}
  },
  "round": "r46"
}
```
