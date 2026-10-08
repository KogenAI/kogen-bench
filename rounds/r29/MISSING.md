# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 75,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Boundary telemetry not retained": 75
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
        "Launch running/active counter is block-scoped; host concurrency not emitted": 30
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Boundary telemetry not retained": 75
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "No matching controller samples retained": 30
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 2,
      "reasons": {
        "Not available for ungraded delivery": 2
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 2,
      "reasons": {
        "Not available for ungraded delivery": 2
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 2,
      "reasons": {
        "Not available for ungraded delivery": 2
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 2,
      "reasons": {
        "Not available for ungraded delivery": 2
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Complete per-model billable vector unavailable": 73,
        "Not available for ungraded delivery": 2
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 2,
      "reasons": {
        "Not recorded in available public metadata": 2
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "No dated account-class receipt": 30
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "No per-cell CPU allocation receipt": 73,
        "Not available for ungraded delivery": 2
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "No per-cell CPU receipt": 73,
        "Not available for ungraded delivery": 2
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "No per-cell kernel receipt": 43,
        "Not available for ungraded delivery": 2
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "No per-cell RAM receipt": 73,
        "Not available for ungraded delivery": 2
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Toolchain version/inventory not recorded": 73
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Toolchain version/inventory not recorded": 73
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Toolchain version/inventory not recorded": 73
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Toolchain version/inventory not recorded": 73
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Toolchain version/inventory not recorded": 73
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Toolchain version/inventory not recorded": 73
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 2,
      "reasons": {
        "No official grade in the public snapshot": 2
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 2,
      "reasons": {
        "No official grade in the public snapshot": 2
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 2,
      "reasons": {
        "No official grade in the public snapshot": 2
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 75,
      "reasons": {
        "No per-cell CPU receipt": 73,
        "Not available for ungraded delivery": 2
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 45,
      "reasons": {
        "No per-cell kernel receipt": 43,
        "Not available for ungraded delivery": 2
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 75,
      "reasons": {
        "No per-cell RAM receipt": 73,
        "Not available for ungraded delivery": 2
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 2,
      "reasons": {
        "Not available for ungraded delivery": 2
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 75,
      "reasons": {
        "No per-cell CPU allocation receipt": 73,
        "Not available for ungraded delivery": 2
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 2,
      "reasons": {
        "Ungraded delivery needs evidence audit": 2
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 2,
      "reasons": {
        "No captured cohort launch receipt": 2
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 2,
      "reasons": {
        "No audited ITT receipt": 2
      }
    },
    "model.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 2,
      "reasons": {
        "Not recorded in available public metadata": 2
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 2,
      "reasons": {
        "No official grade in the public snapshot": 2
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Not recorded in available public metadata": 73
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Dependency source not pinned per cell": 75
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 43
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Original base revision type not recorded per cell": 43
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 2,
      "reasons": {
        "No normalized stop receipt": 2
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 2,
      "reasons": {
        "Not available for ungraded delivery": 2
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 43
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Original base revision type not recorded per cell": 43
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Attempt boundary receipts unavailable": 75
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Absolute phase boundary not retained": 75
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Absolute phase boundary not retained": 75
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Absolute phase boundary not retained": 75
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Absolute phase boundary not retained": 75
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Absolute phase boundary not retained": 75
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Absolute phase boundary not retained": 75
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Absolute phase boundary not retained": 75
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Absolute phase boundary not retained": 75
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Absolute phase boundary not retained": 75
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Absolute phase boundary not retained": 75
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Absolute phase boundary not retained": 75
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Absolute phase boundary not retained": 75
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Absolute phase boundary not retained": 75
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Absolute phase boundary not retained": 75
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Phase wall not emitted or not separable": 73
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Phase wall not emitted or not separable": 73
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 2,
      "reasons": {
        "Not available for ungraded delivery": 2
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Phase wall not emitted or not separable": 73
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Phase wall not emitted or not separable": 73
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Phase wall not emitted or not separable": 73
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Phase wall not emitted or not separable": 73
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Per-phase token counter not emitted": 73
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Per-phase token counter not emitted": 73
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Per-phase token counter not emitted": 73
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Per-phase token counter not emitted": 73
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Per-phase token counter not emitted": 73
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Per-phase token counter not emitted": 73
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Per-phase token counter not emitted": 73
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Per-phase token counter not emitted": 73
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 2,
      "reasons": {
        "Not available for ungraded delivery": 2
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 2,
      "reasons": {
        "Not available for ungraded delivery": 2
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 2,
      "reasons": {
        "Not available for ungraded delivery": 2
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 2,
      "reasons": {
        "Not available for ungraded delivery": 2
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Per-phase token counter not emitted": 73
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Per-phase token counter not emitted": 73
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Per-phase token counter not emitted": 73
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Per-phase token counter not emitted": 73
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Per-phase token counter not emitted": 73
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Per-phase token counter not emitted": 73
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Per-phase token counter not emitted": 73
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Per-phase token counter not emitted": 73
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Per-phase token counter not emitted": 73
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Per-phase token counter not emitted": 73
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Per-phase token counter not emitted": 73
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Per-phase token counter not emitted": 73
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Per-phase token counter not emitted": 73
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Per-phase token counter not emitted": 73
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Per-phase token counter not emitted": 73
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Per-phase token counter not emitted": 73
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 73,
        "Usage counter unavailable": 2
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 73,
        "Usage counter unavailable": 2
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 73,
        "Usage counter unavailable": 2
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 75,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 73,
        "Usage counter unavailable": 2
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 73,
        "Not available for ungraded delivery": 2
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 73,
        "Not available for ungraded delivery": 2
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 73,
        "Not available for ungraded delivery": 2
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Toolchain version/inventory not recorded": 73
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Toolchain version/inventory not recorded": 73
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Toolchain version/inventory not recorded": 73
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Toolchain version/inventory not recorded": 73
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Toolchain version/inventory not recorded": 73
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 75,
      "reasons": {
        "Not available for ungraded delivery": 2,
        "Toolchain version/inventory not recorded": 73
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 75
      },
      "circumstances.concurrent_cells_end": {
        "none": 30
      },
      "circumstances.concurrent_cells_start": {
        "none": 30
      },
      "circumstances.load1_end": {
        "none": 75
      },
      "circumstances.load_samples": {
        "none": 30
      },
      "cost.accounting": {
        "none": 2
      },
      "cost.calculator_version": {
        "none": 2
      },
      "cost.long_context_reconciled": {
        "none": 2
      },
      "cost.price_table_version": {
        "none": 2
      },
      "cost.usd": {
        "none": 75
      },
      "effort.effective": {
        "none": 2
      },
      "environment.account_class": {
        "none": 30
      },
      "environment.cores": {
        "none": 75
      },
      "environment.cpu_model": {
        "none": 75
      },
      "environment.kernel": {
        "none": 45
      },
      "environment.ram_gib": {
        "none": 75
      },
      "environment.toolchains.elixir": {
        "none": 75
      },
      "environment.toolchains.erlang": {
        "none": 75
      },
      "environment.toolchains.node": {
        "none": 75
      },
      "environment.toolchains.other_inventory": {
        "none": 75
      },
      "environment.toolchains.ruby": {
        "none": 75
      },
      "environment.toolchains.rust": {
        "none": 75
      },
      "grade.grader": {
        "not re-derivable from the public record": 2
      },
      "grade.tests_ran": {
        "not re-derivable from the public record": 2
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 2
      },
      "host.cpu": {
        "none": 75
      },
      "host.kernel": {
        "none": 45
      },
      "host.ram_gib": {
        "none": 75
      },
      "host.spec_ref": {
        "none": 2
      },
      "host.vcpu": {
        "none": 75
      },
      "itt.class": {
        "none": 2
      },
      "itt.cohort": {
        "none": 2
      },
      "itt.evidence_ref": {
        "none": 2
      },
      "model.effective": {
        "none": 2
      },
      "outcome": {
        "not re-derivable from the public record": 2
      },
      "recipe": {
        "none": 75
      },
      "setup.deps_source": {
        "none": 75
      },
      "setup.task_base.hash": {
        "none": 45
      },
      "setup.task_base.kind": {
        "none": 45
      },
      "stop_reason": {
        "none": 2
      },
      "task.base_repo": {
        "none": 2
      },
      "task.base_revision.hash": {
        "none": 45
      },
      "task.base_revision.kind": {
        "none": 45
      },
      "timestamps.attempts": {
        "none": 75
      },
      "timestamps.phases.develop.end_utc": {
        "none": 75
      },
      "timestamps.phases.develop.start_utc": {
        "none": 75
      },
      "timestamps.phases.gate.end_utc": {
        "none": 75
      },
      "timestamps.phases.gate.start_utc": {
        "none": 75
      },
      "timestamps.phases.grade.end_utc": {
        "none": 75
      },
      "timestamps.phases.grade.start_utc": {
        "none": 75
      },
      "timestamps.phases.plan.end_utc": {
        "none": 75
      },
      "timestamps.phases.plan.start_utc": {
        "none": 75
      },
      "timestamps.phases.review.end_utc": {
        "none": 75
      },
      "timestamps.phases.review.start_utc": {
        "none": 75
      },
      "timestamps.phases.setup.end_utc": {
        "none": 75
      },
      "timestamps.phases.setup.start_utc": {
        "none": 75
      },
      "timestamps.phases.shape.end_utc": {
        "none": 75
      },
      "timestamps.phases.shape.start_utc": {
        "none": 75
      },
      "timing.phases_s.develop": {
        "none": 75
      },
      "timing.phases_s.gate": {
        "none": 75
      },
      "timing.phases_s.grade": {
        "none": 2
      },
      "timing.phases_s.plan": {
        "none": 75
      },
      "timing.phases_s.review": {
        "none": 75
      },
      "timing.phases_s.setup": {
        "none": 75
      },
      "timing.phases_s.shape": {
        "none": 75
      },
      "tokens.phases.develop.cached_input": {
        "none": 75
      },
      "tokens.phases.develop.input": {
        "none": 75
      },
      "tokens.phases.develop.output": {
        "none": 75
      },
      "tokens.phases.develop.reasoning": {
        "none": 75
      },
      "tokens.phases.gate.cached_input": {
        "none": 75
      },
      "tokens.phases.gate.input": {
        "none": 75
      },
      "tokens.phases.gate.output": {
        "none": 75
      },
      "tokens.phases.gate.reasoning": {
        "none": 75
      },
      "tokens.phases.grade.cached_input": {
        "none": 2
      },
      "tokens.phases.grade.input": {
        "none": 2
      },
      "tokens.phases.grade.output": {
        "none": 2
      },
      "tokens.phases.grade.reasoning": {
        "none": 2
      },
      "tokens.phases.plan.cached_input": {
        "none": 75
      },
      "tokens.phases.plan.input": {
        "none": 75
      },
      "tokens.phases.plan.output": {
        "none": 75
      },
      "tokens.phases.plan.reasoning": {
        "none": 75
      },
      "tokens.phases.review.cached_input": {
        "none": 75
      },
      "tokens.phases.review.input": {
        "none": 75
      },
      "tokens.phases.review.output": {
        "none": 75
      },
      "tokens.phases.review.reasoning": {
        "none": 75
      },
      "tokens.phases.setup.cached_input": {
        "none": 75
      },
      "tokens.phases.setup.input": {
        "none": 75
      },
      "tokens.phases.setup.output": {
        "none": 75
      },
      "tokens.phases.setup.reasoning": {
        "none": 75
      },
      "tokens.phases.shape.cached_input": {
        "none": 75
      },
      "tokens.phases.shape.input": {
        "none": 75
      },
      "tokens.phases.shape.output": {
        "none": 75
      },
      "tokens.phases.shape.reasoning": {
        "none": 75
      },
      "tokens.total.cached_input": {
        "none": 75
      },
      "tokens.total.input": {
        "none": 75
      },
      "tokens.total.output": {
        "none": 75
      },
      "tokens.total.reasoning": {
        "none": 75
      },
      "tools.codex_cli": {
        "none": 75
      },
      "tools.grader": {
        "none": 75
      },
      "tools.runner": {
        "none": 75
      },
      "tools.toolchains.elixir": {
        "none": 75
      },
      "tools.toolchains.erlang": {
        "none": 75
      },
      "tools.toolchains.node": {
        "none": 75
      },
      "tools.toolchains.other_inventory": {
        "none": 75
      },
      "tools.toolchains.ruby": {
        "none": 75
      },
      "tools.toolchains.rust": {
        "none": 75
      }
    },
    "reconstructable": {}
  },
  "round": "r29"
}
```
