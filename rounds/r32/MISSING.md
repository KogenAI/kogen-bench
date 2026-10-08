# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 20,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Boundary telemetry not retained": 20
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Boundary telemetry not retained": 5
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 5
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Boundary telemetry not retained": 20
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "No matching controller samples retained": 5
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
      "count": 20,
      "reasons": {
        "Complete per-model billable vector unavailable": 15,
        "Not available for ungraded delivery": 5
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not recorded in available public metadata": 5
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "No dated account-class receipt": 5
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "No per-cell CPU allocation receipt": 15,
        "Not available for ungraded delivery": 5
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "No per-cell CPU receipt": 15,
        "Not available for ungraded delivery": 5
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "No per-cell kernel receipt": 10,
        "Not available for ungraded delivery": 5
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "No per-cell RAM receipt": 15,
        "Not available for ungraded delivery": 5
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 15
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 15
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 15
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 15
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 15
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 15
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
      "count": 6,
      "reasons": {
        "Boolean receipt not recorded": 1,
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
      "count": 20,
      "reasons": {
        "No per-cell CPU receipt": 15,
        "Not available for ungraded delivery": 5
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 15,
      "reasons": {
        "No per-cell kernel receipt": 10,
        "Not available for ungraded delivery": 5
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 20,
      "reasons": {
        "No per-cell RAM receipt": 15,
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
      "count": 20,
      "reasons": {
        "No per-cell CPU allocation receipt": 15,
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
      "count": 5,
      "reasons": {
        "Not recorded in available public metadata": 5
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
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Not recorded in available public metadata": 15
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Dependency source not pinned per cell": 20
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 10
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Original base revision type not recorded per cell": 10
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 5,
      "reasons": {
        "No normalized stop receipt": 4,
        "Runner status does not establish normalized stop cause": 1
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
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 10
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Original base revision type not recorded per cell": 10
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Attempt boundary receipts unavailable": 20
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Absolute phase boundary not retained": 20
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Absolute phase boundary not retained": 20
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Absolute phase boundary not retained": 20
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Absolute phase boundary not retained": 20
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Absolute phase boundary not retained": 20
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Absolute phase boundary not retained": 20
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Absolute phase boundary not retained": 20
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Absolute phase boundary not retained": 20
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Absolute phase boundary not retained": 20
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Absolute phase boundary not retained": 20
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Absolute phase boundary not retained": 20
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Absolute phase boundary not retained": 20
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Absolute phase boundary not retained": 20
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Absolute phase boundary not retained": 20
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Phase wall not emitted or not separable": 15
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Phase wall not emitted or not separable": 15
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Phase wall not emitted or not separable": 1
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Phase wall not emitted or not separable": 15
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Phase wall not emitted or not separable": 15
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Phase wall not emitted or not separable": 15
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Phase wall not emitted or not separable": 15
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 15
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 15
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 15
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 15
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 15
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 15
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 15
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 15
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
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 15
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 15
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 15
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 15
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 15
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 15
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 15
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 15
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 15
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 15
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 15
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 15
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 15
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 15
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 15
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 15
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 19,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 15,
        "Usage counter unavailable": 4
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 19,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 15,
        "Usage counter unavailable": 4
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 19,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 15,
        "Usage counter unavailable": 4
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 19,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 15,
        "Usage counter unavailable": 4
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 15,
        "Not available for ungraded delivery": 5
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 15,
        "Not available for ungraded delivery": 5
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 15,
        "Not available for ungraded delivery": 5
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 15
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 15
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 15
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 15
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 15
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 15
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 20
      },
      "circumstances.concurrent_cells_end": {
        "none": 5
      },
      "circumstances.concurrent_cells_start": {
        "none": 5
      },
      "circumstances.load1_end": {
        "none": 20
      },
      "circumstances.load_samples": {
        "none": 5
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
        "none": 20
      },
      "effort.effective": {
        "none": 5
      },
      "environment.account_class": {
        "none": 5
      },
      "environment.cores": {
        "none": 20
      },
      "environment.cpu_model": {
        "none": 20
      },
      "environment.kernel": {
        "none": 15
      },
      "environment.ram_gib": {
        "none": 20
      },
      "environment.toolchains.elixir": {
        "none": 20
      },
      "environment.toolchains.erlang": {
        "none": 20
      },
      "environment.toolchains.node": {
        "none": 20
      },
      "environment.toolchains.other_inventory": {
        "none": 20
      },
      "environment.toolchains.ruby": {
        "none": 20
      },
      "environment.toolchains.rust": {
        "none": 20
      },
      "grade.grader": {
        "not re-derivable from the public record": 5
      },
      "grade.tests_ran": {
        "none": 1,
        "not re-derivable from the public record": 5
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 5
      },
      "host.cpu": {
        "none": 20
      },
      "host.kernel": {
        "none": 15
      },
      "host.ram_gib": {
        "none": 20
      },
      "host.spec_ref": {
        "none": 5
      },
      "host.vcpu": {
        "none": 20
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
        "none": 5
      },
      "outcome": {
        "not re-derivable from the public record": 5
      },
      "recipe": {
        "none": 20
      },
      "setup.deps_source": {
        "none": 20
      },
      "setup.task_base.hash": {
        "none": 15
      },
      "setup.task_base.kind": {
        "none": 15
      },
      "stop_reason": {
        "none": 5
      },
      "task.base_repo": {
        "none": 5
      },
      "task.base_revision.hash": {
        "none": 15
      },
      "task.base_revision.kind": {
        "none": 15
      },
      "timestamps.attempts": {
        "none": 20
      },
      "timestamps.phases.develop.end_utc": {
        "none": 20
      },
      "timestamps.phases.develop.start_utc": {
        "none": 20
      },
      "timestamps.phases.gate.end_utc": {
        "none": 20
      },
      "timestamps.phases.gate.start_utc": {
        "none": 20
      },
      "timestamps.phases.grade.end_utc": {
        "none": 20
      },
      "timestamps.phases.grade.start_utc": {
        "none": 20
      },
      "timestamps.phases.plan.end_utc": {
        "none": 20
      },
      "timestamps.phases.plan.start_utc": {
        "none": 20
      },
      "timestamps.phases.review.end_utc": {
        "none": 20
      },
      "timestamps.phases.review.start_utc": {
        "none": 20
      },
      "timestamps.phases.setup.end_utc": {
        "none": 20
      },
      "timestamps.phases.setup.start_utc": {
        "none": 20
      },
      "timestamps.phases.shape.end_utc": {
        "none": 20
      },
      "timestamps.phases.shape.start_utc": {
        "none": 20
      },
      "timing.phases_s.develop": {
        "none": 20
      },
      "timing.phases_s.gate": {
        "none": 20
      },
      "timing.phases_s.grade": {
        "none": 6
      },
      "timing.phases_s.plan": {
        "none": 20
      },
      "timing.phases_s.review": {
        "none": 20
      },
      "timing.phases_s.setup": {
        "none": 20
      },
      "timing.phases_s.shape": {
        "none": 20
      },
      "tokens.phases.develop.cached_input": {
        "none": 20
      },
      "tokens.phases.develop.input": {
        "none": 20
      },
      "tokens.phases.develop.output": {
        "none": 20
      },
      "tokens.phases.develop.reasoning": {
        "none": 20
      },
      "tokens.phases.gate.cached_input": {
        "none": 20
      },
      "tokens.phases.gate.input": {
        "none": 20
      },
      "tokens.phases.gate.output": {
        "none": 20
      },
      "tokens.phases.gate.reasoning": {
        "none": 20
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
        "none": 20
      },
      "tokens.phases.plan.input": {
        "none": 20
      },
      "tokens.phases.plan.output": {
        "none": 20
      },
      "tokens.phases.plan.reasoning": {
        "none": 20
      },
      "tokens.phases.review.cached_input": {
        "none": 20
      },
      "tokens.phases.review.input": {
        "none": 20
      },
      "tokens.phases.review.output": {
        "none": 20
      },
      "tokens.phases.review.reasoning": {
        "none": 20
      },
      "tokens.phases.setup.cached_input": {
        "none": 20
      },
      "tokens.phases.setup.input": {
        "none": 20
      },
      "tokens.phases.setup.output": {
        "none": 20
      },
      "tokens.phases.setup.reasoning": {
        "none": 20
      },
      "tokens.phases.shape.cached_input": {
        "none": 20
      },
      "tokens.phases.shape.input": {
        "none": 20
      },
      "tokens.phases.shape.output": {
        "none": 20
      },
      "tokens.phases.shape.reasoning": {
        "none": 20
      },
      "tokens.total.cached_input": {
        "none": 19
      },
      "tokens.total.input": {
        "none": 19
      },
      "tokens.total.output": {
        "none": 19
      },
      "tokens.total.reasoning": {
        "none": 19
      },
      "tools.codex_cli": {
        "none": 20
      },
      "tools.grader": {
        "none": 20
      },
      "tools.runner": {
        "none": 20
      },
      "tools.toolchains.elixir": {
        "none": 20
      },
      "tools.toolchains.erlang": {
        "none": 20
      },
      "tools.toolchains.node": {
        "none": 20
      },
      "tools.toolchains.other_inventory": {
        "none": 20
      },
      "tools.toolchains.ruby": {
        "none": 20
      },
      "tools.toolchains.rust": {
        "none": 20
      }
    },
    "reconstructable": {}
  },
  "round": "r32"
}
```
