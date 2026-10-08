# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 15,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Boundary telemetry not retained": 15
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Boundary telemetry not retained": 10
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 10
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Boundary telemetry not retained": 15
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "No matching controller samples retained": 10
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Complete per-model billable vector unavailable": 10,
        "Not available for ungraded delivery": 5
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 13,
      "reasons": {
        "Not recorded in available public metadata": 13
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "No dated account-class receipt": 10
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "No per-cell CPU allocation receipt": 10,
        "Not available for ungraded delivery": 5
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "No per-cell CPU receipt": 10,
        "Not available for ungraded delivery": 5
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "No per-cell RAM receipt": 10,
        "Not available for ungraded delivery": 5
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 10
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 10
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 10
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 10
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 10
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 10
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 5,
      "reasons": {
        "No official grade in the public snapshot": 5
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 13,
      "reasons": {
        "Boolean receipt not recorded": 8,
        "No official grade in the public snapshot": 5
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 5,
      "reasons": {
        "No official grade in the public snapshot": 5
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 15,
      "reasons": {
        "No per-cell CPU receipt": 10,
        "Not available for ungraded delivery": 5
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 15,
      "reasons": {
        "No per-cell RAM receipt": 10,
        "Not available for ungraded delivery": 5
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 15,
      "reasons": {
        "No per-cell CPU allocation receipt": 10,
        "Not available for ungraded delivery": 5
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 5,
      "reasons": {
        "Ungraded delivery needs evidence audit": 5
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 5,
      "reasons": {
        "No captured cohort launch receipt": 5
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 5,
      "reasons": {
        "No audited ITT receipt": 5
      }
    },
    "model.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 13,
      "reasons": {
        "Not recorded in available public metadata": 13
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 5,
      "reasons": {
        "No official grade in the public snapshot": 5
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Not recorded in available public metadata": 10
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Dependency source not pinned per cell": 15
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 13,
      "reasons": {
        "No normalized stop receipt": 5,
        "Runner status does not establish normalized stop cause": 8
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Attempt boundary receipts unavailable": 15
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Absolute phase boundary not retained": 15
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Absolute phase boundary not retained": 15
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Absolute phase boundary not retained": 15
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Absolute phase boundary not retained": 15
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Absolute phase boundary not retained": 15
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Absolute phase boundary not retained": 15
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Absolute phase boundary not retained": 15
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Absolute phase boundary not retained": 15
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Absolute phase boundary not retained": 15
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Absolute phase boundary not retained": 15
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Absolute phase boundary not retained": 15
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Absolute phase boundary not retained": 15
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Absolute phase boundary not retained": 15
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Absolute phase boundary not retained": 15
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Phase wall not emitted or not separable": 10
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Phase wall not emitted or not separable": 10
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 13,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Phase wall not emitted or not separable": 8
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Phase wall not emitted or not separable": 10
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Phase wall not emitted or not separable": 10
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Phase wall not emitted or not separable": 10
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Phase wall not emitted or not separable": 10
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 10,
        "Usage counter unavailable": 5
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 10,
        "Usage counter unavailable": 5
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 10,
        "Usage counter unavailable": 5
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 10,
        "Usage counter unavailable": 5
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 10,
        "Not available for ungraded delivery": 5
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 10,
        "Not available for ungraded delivery": 5
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 10,
        "Not available for ungraded delivery": 5
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 10
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 10
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 10
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 10
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 10
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 10
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 15
      },
      "circumstances.concurrent_cells_end": {
        "none": 10
      },
      "circumstances.concurrent_cells_start": {
        "none": 10
      },
      "circumstances.load1_end": {
        "none": 15
      },
      "circumstances.load_samples": {
        "none": 10
      },
      "cost.accounting": {
        "none": 5
      },
      "cost.calculator_version": {
        "none": 5
      },
      "cost.long_context_reconciled": {
        "none": 5
      },
      "cost.price_table_version": {
        "none": 5
      },
      "cost.usd": {
        "none": 15
      },
      "effort.effective": {
        "none": 13
      },
      "environment.account_class": {
        "none": 10
      },
      "environment.cores": {
        "none": 15
      },
      "environment.cpu_model": {
        "none": 15
      },
      "environment.kernel": {
        "none": 5
      },
      "environment.ram_gib": {
        "none": 15
      },
      "environment.toolchains.elixir": {
        "none": 15
      },
      "environment.toolchains.erlang": {
        "none": 15
      },
      "environment.toolchains.node": {
        "none": 15
      },
      "environment.toolchains.other_inventory": {
        "none": 15
      },
      "environment.toolchains.ruby": {
        "none": 15
      },
      "environment.toolchains.rust": {
        "none": 15
      },
      "grade.grader": {
        "not re-derivable from the public record": 5
      },
      "grade.tests_ran": {
        "none": 8,
        "not re-derivable from the public record": 5
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 5
      },
      "host.cpu": {
        "none": 15
      },
      "host.kernel": {
        "none": 5
      },
      "host.ram_gib": {
        "none": 15
      },
      "host.spec_ref": {
        "none": 5
      },
      "host.vcpu": {
        "none": 15
      },
      "itt.class": {
        "none": 5
      },
      "itt.cohort": {
        "none": 5
      },
      "itt.evidence_ref": {
        "none": 5
      },
      "model.effective": {
        "none": 13
      },
      "outcome": {
        "not re-derivable from the public record": 5
      },
      "recipe": {
        "none": 15
      },
      "setup.deps_source": {
        "none": 15
      },
      "setup.task_base.hash": {
        "none": 5
      },
      "setup.task_base.kind": {
        "none": 5
      },
      "stop_reason": {
        "none": 13
      },
      "task.base_repo": {
        "none": 5
      },
      "task.base_revision.hash": {
        "none": 5
      },
      "task.base_revision.kind": {
        "none": 5
      },
      "timestamps.attempts": {
        "none": 15
      },
      "timestamps.phases.develop.end_utc": {
        "none": 15
      },
      "timestamps.phases.develop.start_utc": {
        "none": 15
      },
      "timestamps.phases.gate.end_utc": {
        "none": 15
      },
      "timestamps.phases.gate.start_utc": {
        "none": 15
      },
      "timestamps.phases.grade.end_utc": {
        "none": 15
      },
      "timestamps.phases.grade.start_utc": {
        "none": 15
      },
      "timestamps.phases.plan.end_utc": {
        "none": 15
      },
      "timestamps.phases.plan.start_utc": {
        "none": 15
      },
      "timestamps.phases.review.end_utc": {
        "none": 15
      },
      "timestamps.phases.review.start_utc": {
        "none": 15
      },
      "timestamps.phases.setup.end_utc": {
        "none": 15
      },
      "timestamps.phases.setup.start_utc": {
        "none": 15
      },
      "timestamps.phases.shape.end_utc": {
        "none": 15
      },
      "timestamps.phases.shape.start_utc": {
        "none": 15
      },
      "timing.phases_s.develop": {
        "none": 15
      },
      "timing.phases_s.gate": {
        "none": 15
      },
      "timing.phases_s.grade": {
        "none": 13
      },
      "timing.phases_s.plan": {
        "none": 15
      },
      "timing.phases_s.review": {
        "none": 15
      },
      "timing.phases_s.setup": {
        "none": 15
      },
      "timing.phases_s.shape": {
        "none": 15
      },
      "tokens.phases.develop.cached_input": {
        "none": 15
      },
      "tokens.phases.develop.input": {
        "none": 15
      },
      "tokens.phases.develop.output": {
        "none": 15
      },
      "tokens.phases.develop.reasoning": {
        "none": 15
      },
      "tokens.phases.gate.cached_input": {
        "none": 15
      },
      "tokens.phases.gate.input": {
        "none": 15
      },
      "tokens.phases.gate.output": {
        "none": 15
      },
      "tokens.phases.gate.reasoning": {
        "none": 15
      },
      "tokens.phases.grade.cached_input": {
        "none": 5
      },
      "tokens.phases.grade.input": {
        "none": 5
      },
      "tokens.phases.grade.output": {
        "none": 5
      },
      "tokens.phases.grade.reasoning": {
        "none": 5
      },
      "tokens.phases.plan.cached_input": {
        "none": 15
      },
      "tokens.phases.plan.input": {
        "none": 15
      },
      "tokens.phases.plan.output": {
        "none": 15
      },
      "tokens.phases.plan.reasoning": {
        "none": 15
      },
      "tokens.phases.review.cached_input": {
        "none": 15
      },
      "tokens.phases.review.input": {
        "none": 15
      },
      "tokens.phases.review.output": {
        "none": 15
      },
      "tokens.phases.review.reasoning": {
        "none": 15
      },
      "tokens.phases.setup.cached_input": {
        "none": 15
      },
      "tokens.phases.setup.input": {
        "none": 15
      },
      "tokens.phases.setup.output": {
        "none": 15
      },
      "tokens.phases.setup.reasoning": {
        "none": 15
      },
      "tokens.phases.shape.cached_input": {
        "none": 15
      },
      "tokens.phases.shape.input": {
        "none": 15
      },
      "tokens.phases.shape.output": {
        "none": 15
      },
      "tokens.phases.shape.reasoning": {
        "none": 15
      },
      "tokens.total.cached_input": {
        "none": 15
      },
      "tokens.total.input": {
        "none": 15
      },
      "tokens.total.output": {
        "none": 15
      },
      "tokens.total.reasoning": {
        "none": 15
      },
      "tools.codex_cli": {
        "none": 15
      },
      "tools.grader": {
        "none": 15
      },
      "tools.runner": {
        "none": 15
      },
      "tools.toolchains.elixir": {
        "none": 15
      },
      "tools.toolchains.erlang": {
        "none": 15
      },
      "tools.toolchains.node": {
        "none": 15
      },
      "tools.toolchains.other_inventory": {
        "none": 15
      },
      "tools.toolchains.ruby": {
        "none": 15
      },
      "tools.toolchains.rust": {
        "none": 15
      }
    },
    "reconstructable": {}
  },
  "round": "r34"
}
```
