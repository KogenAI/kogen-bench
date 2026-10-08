# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 132,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Boundary telemetry not retained": 132
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
      "count": 132,
      "reasons": {
        "Boundary telemetry not retained": 132
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
      "count": 70,
      "reasons": {
        "Not available for ungraded delivery": 70
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 70,
      "reasons": {
        "Not available for ungraded delivery": 70
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 70,
      "reasons": {
        "Not available for ungraded delivery": 70
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 70,
      "reasons": {
        "Not available for ungraded delivery": 70
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 132,
      "reasons": {
        "Complete per-model billable vector unavailable": 62,
        "Not available for ungraded delivery": 70
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
      "count": 132,
      "reasons": {
        "No per-cell CPU allocation receipt": 62,
        "Not available for ungraded delivery": 70
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "No per-cell CPU receipt": 62,
        "Not available for ungraded delivery": 70
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "No per-cell kernel receipt": 32,
        "Not available for ungraded delivery": 70
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "No per-cell RAM receipt": 62,
        "Not available for ungraded delivery": 70
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Toolchain version/inventory not recorded": 62
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Toolchain version/inventory not recorded": 62
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Toolchain version/inventory not recorded": 62
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Toolchain version/inventory not recorded": 62
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Toolchain version/inventory not recorded": 62
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Toolchain version/inventory not recorded": 62
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 70,
      "reasons": {
        "No official grade in the public snapshot": 70
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 93,
      "reasons": {
        "Boolean receipt not recorded": 23,
        "No official grade in the public snapshot": 70
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 70,
      "reasons": {
        "No official grade in the public snapshot": 70
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 132,
      "reasons": {
        "No per-cell CPU receipt": 62,
        "Not available for ungraded delivery": 70
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 102,
      "reasons": {
        "No per-cell kernel receipt": 32,
        "Not available for ungraded delivery": 70
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 132,
      "reasons": {
        "No per-cell RAM receipt": 62,
        "Not available for ungraded delivery": 70
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 70,
      "reasons": {
        "Not available for ungraded delivery": 70
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 132,
      "reasons": {
        "No per-cell CPU allocation receipt": 62,
        "Not available for ungraded delivery": 70
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 93,
      "reasons": {
        "Invalid/environment cause requires evidence audit": 23,
        "Ungraded delivery needs evidence audit": 70
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 70,
      "reasons": {
        "No captured cohort launch receipt": 70
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 93,
      "reasons": {
        "No audited ITT receipt": 70,
        "No evidence-backed ITT classification": 23
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 70,
      "reasons": {
        "No official grade in the public snapshot": 70
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Not recorded in available public metadata": 62
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Dependency source not pinned per cell": 132
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 32
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Original base revision type not recorded per cell": 32
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 57,
      "reasons": {
        "No normalized stop receipt": 34,
        "Runner status does not establish normalized stop cause": 23
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 70,
      "reasons": {
        "Not available for ungraded delivery": 70
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 32
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Original base revision type not recorded per cell": 32
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Attempt boundary receipts unavailable": 132
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Absolute phase boundary not retained": 132
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Absolute phase boundary not retained": 132
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Absolute phase boundary not retained": 132
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Absolute phase boundary not retained": 132
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Absolute phase boundary not retained": 132
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Absolute phase boundary not retained": 132
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Absolute phase boundary not retained": 132
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Absolute phase boundary not retained": 132
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Absolute phase boundary not retained": 132
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Absolute phase boundary not retained": 132
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Absolute phase boundary not retained": 132
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Absolute phase boundary not retained": 132
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Absolute phase boundary not retained": 132
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Absolute phase boundary not retained": 132
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Phase wall not emitted or not separable": 62
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Phase wall not emitted or not separable": 62
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 93,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Phase wall not emitted or not separable": 23
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Phase wall not emitted or not separable": 62
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Phase wall not emitted or not separable": 62
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Phase wall not emitted or not separable": 62
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Phase wall not emitted or not separable": 62
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 70,
      "reasons": {
        "Not available for ungraded delivery": 70
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 70,
      "reasons": {
        "Not available for ungraded delivery": 70
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 70,
      "reasons": {
        "Not available for ungraded delivery": 70
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 70,
      "reasons": {
        "Not available for ungraded delivery": 70
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 62,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 62
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 62,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 62
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 62,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 62
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 62,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 62
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 62,
        "Not available for ungraded delivery": 70
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 62,
        "Not available for ungraded delivery": 70
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 62,
        "Not available for ungraded delivery": 70
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Toolchain version/inventory not recorded": 62
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Toolchain version/inventory not recorded": 62
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Toolchain version/inventory not recorded": 62
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Toolchain version/inventory not recorded": 62
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Toolchain version/inventory not recorded": 62
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "Not available for ungraded delivery": 70,
        "Toolchain version/inventory not recorded": 62
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 132
      },
      "circumstances.concurrent_cells_end": {
        "none": 30
      },
      "circumstances.concurrent_cells_start": {
        "none": 30
      },
      "circumstances.load1_end": {
        "none": 132
      },
      "circumstances.load_samples": {
        "none": 30
      },
      "cost.accounting": {
        "none": 70
      },
      "cost.calculator_version": {
        "none": 70
      },
      "cost.long_context_reconciled": {
        "none": 70
      },
      "cost.price_table_version": {
        "none": 70
      },
      "cost.usd": {
        "none": 132
      },
      "environment.account_class": {
        "none": 30
      },
      "environment.cores": {
        "none": 132
      },
      "environment.cpu_model": {
        "none": 132
      },
      "environment.kernel": {
        "none": 102
      },
      "environment.ram_gib": {
        "none": 132
      },
      "environment.toolchains.elixir": {
        "none": 132
      },
      "environment.toolchains.erlang": {
        "none": 132
      },
      "environment.toolchains.node": {
        "none": 132
      },
      "environment.toolchains.other_inventory": {
        "none": 132
      },
      "environment.toolchains.ruby": {
        "none": 132
      },
      "environment.toolchains.rust": {
        "none": 132
      },
      "grade.grader": {
        "not re-derivable from the public record": 70
      },
      "grade.tests_ran": {
        "none": 23,
        "not re-derivable from the public record": 70
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 70
      },
      "host.cpu": {
        "none": 132
      },
      "host.kernel": {
        "none": 102
      },
      "host.ram_gib": {
        "none": 132
      },
      "host.spec_ref": {
        "none": 70
      },
      "host.vcpu": {
        "none": 132
      },
      "itt.class": {
        "none": 93
      },
      "itt.cohort": {
        "none": 70
      },
      "itt.evidence_ref": {
        "none": 93
      },
      "outcome": {
        "not re-derivable from the public record": 70
      },
      "recipe": {
        "none": 132
      },
      "setup.deps_source": {
        "none": 132
      },
      "setup.task_base.hash": {
        "none": 102
      },
      "setup.task_base.kind": {
        "none": 102
      },
      "stop_reason": {
        "none": 57
      },
      "task.base_repo": {
        "none": 70
      },
      "task.base_revision.hash": {
        "none": 102
      },
      "task.base_revision.kind": {
        "none": 102
      },
      "timestamps.attempts": {
        "none": 132
      },
      "timestamps.phases.develop.end_utc": {
        "none": 132
      },
      "timestamps.phases.develop.start_utc": {
        "none": 132
      },
      "timestamps.phases.gate.end_utc": {
        "none": 132
      },
      "timestamps.phases.gate.start_utc": {
        "none": 132
      },
      "timestamps.phases.grade.end_utc": {
        "none": 132
      },
      "timestamps.phases.grade.start_utc": {
        "none": 132
      },
      "timestamps.phases.plan.end_utc": {
        "none": 132
      },
      "timestamps.phases.plan.start_utc": {
        "none": 132
      },
      "timestamps.phases.review.end_utc": {
        "none": 132
      },
      "timestamps.phases.review.start_utc": {
        "none": 132
      },
      "timestamps.phases.setup.end_utc": {
        "none": 132
      },
      "timestamps.phases.setup.start_utc": {
        "none": 132
      },
      "timestamps.phases.shape.end_utc": {
        "none": 132
      },
      "timestamps.phases.shape.start_utc": {
        "none": 132
      },
      "timing.phases_s.develop": {
        "none": 132
      },
      "timing.phases_s.gate": {
        "none": 132
      },
      "timing.phases_s.grade": {
        "none": 93
      },
      "timing.phases_s.plan": {
        "none": 132
      },
      "timing.phases_s.review": {
        "none": 132
      },
      "timing.phases_s.setup": {
        "none": 132
      },
      "timing.phases_s.shape": {
        "none": 132
      },
      "tokens.phases.develop.cached_input": {
        "none": 132
      },
      "tokens.phases.develop.input": {
        "none": 132
      },
      "tokens.phases.develop.output": {
        "none": 132
      },
      "tokens.phases.develop.reasoning": {
        "none": 132
      },
      "tokens.phases.gate.cached_input": {
        "none": 132
      },
      "tokens.phases.gate.input": {
        "none": 132
      },
      "tokens.phases.gate.output": {
        "none": 132
      },
      "tokens.phases.gate.reasoning": {
        "none": 132
      },
      "tokens.phases.grade.cached_input": {
        "none": 70
      },
      "tokens.phases.grade.input": {
        "none": 70
      },
      "tokens.phases.grade.output": {
        "none": 70
      },
      "tokens.phases.grade.reasoning": {
        "none": 70
      },
      "tokens.phases.plan.cached_input": {
        "none": 132
      },
      "tokens.phases.plan.input": {
        "none": 132
      },
      "tokens.phases.plan.output": {
        "none": 132
      },
      "tokens.phases.plan.reasoning": {
        "none": 132
      },
      "tokens.phases.review.cached_input": {
        "none": 132
      },
      "tokens.phases.review.input": {
        "none": 132
      },
      "tokens.phases.review.output": {
        "none": 132
      },
      "tokens.phases.review.reasoning": {
        "none": 132
      },
      "tokens.phases.setup.cached_input": {
        "none": 132
      },
      "tokens.phases.setup.input": {
        "none": 132
      },
      "tokens.phases.setup.output": {
        "none": 132
      },
      "tokens.phases.setup.reasoning": {
        "none": 132
      },
      "tokens.phases.shape.cached_input": {
        "none": 132
      },
      "tokens.phases.shape.input": {
        "none": 132
      },
      "tokens.phases.shape.output": {
        "none": 132
      },
      "tokens.phases.shape.reasoning": {
        "none": 132
      },
      "tokens.total.cached_input": {
        "none": 62
      },
      "tokens.total.input": {
        "none": 62
      },
      "tokens.total.output": {
        "none": 62
      },
      "tokens.total.reasoning": {
        "none": 62
      },
      "tools.codex_cli": {
        "none": 132
      },
      "tools.grader": {
        "none": 132
      },
      "tools.runner": {
        "none": 132
      },
      "tools.toolchains.elixir": {
        "none": 132
      },
      "tools.toolchains.erlang": {
        "none": 132
      },
      "tools.toolchains.node": {
        "none": 132
      },
      "tools.toolchains.other_inventory": {
        "none": 132
      },
      "tools.toolchains.ruby": {
        "none": 132
      },
      "tools.toolchains.rust": {
        "none": 132
      }
    },
    "reconstructable": {}
  },
  "round": "r49"
}
```
