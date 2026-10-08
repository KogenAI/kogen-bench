# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 84,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Boundary telemetry not retained": 84
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Boundary telemetry not retained": 34
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 34
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Boundary telemetry not retained": 84
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "No matching controller samples retained": 34
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 22,
      "reasons": {
        "Not available for ungraded delivery": 22
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 22,
      "reasons": {
        "Not available for ungraded delivery": 22
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 22,
      "reasons": {
        "Not available for ungraded delivery": 22
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 22,
      "reasons": {
        "Not available for ungraded delivery": 22
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Complete per-model billable vector unavailable": 62,
        "Not available for ungraded delivery": 22
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Not recorded in available public metadata": 41
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "No dated account-class receipt": 34
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "No per-cell CPU allocation receipt": 62,
        "Not available for ungraded delivery": 22
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "No per-cell CPU receipt": 62,
        "Not available for ungraded delivery": 22
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "No per-cell kernel receipt": 28,
        "Not available for ungraded delivery": 22
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "No per-cell RAM receipt": 62,
        "Not available for ungraded delivery": 22
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Toolchain version/inventory not recorded": 62
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Toolchain version/inventory not recorded": 62
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Toolchain version/inventory not recorded": 62
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Toolchain version/inventory not recorded": 62
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Toolchain version/inventory not recorded": 62
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Toolchain version/inventory not recorded": 62
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 22,
      "reasons": {
        "No official grade in the public snapshot": 22
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 41,
      "reasons": {
        "Boolean receipt not recorded": 19,
        "No official grade in the public snapshot": 22
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 22,
      "reasons": {
        "No official grade in the public snapshot": 22
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 84,
      "reasons": {
        "No per-cell CPU receipt": 62,
        "Not available for ungraded delivery": 22
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 50,
      "reasons": {
        "No per-cell kernel receipt": 28,
        "Not available for ungraded delivery": 22
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 84,
      "reasons": {
        "No per-cell RAM receipt": 62,
        "Not available for ungraded delivery": 22
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 22,
      "reasons": {
        "Not available for ungraded delivery": 22
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 84,
      "reasons": {
        "No per-cell CPU allocation receipt": 62,
        "Not available for ungraded delivery": 22
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 22,
      "reasons": {
        "Ungraded delivery needs evidence audit": 22
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 22,
      "reasons": {
        "No captured cohort launch receipt": 22
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 22,
      "reasons": {
        "No audited ITT receipt": 22
      }
    },
    "model.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Not recorded in available public metadata": 41
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 23,
      "reasons": {
        "No official grade in the public snapshot": 22,
        "Official result outside standard outcome classes": 1
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Not recorded in available public metadata": 62
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Dependency source not pinned per cell": 84
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 46
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Original base revision type not recorded per cell": 46
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 41,
      "reasons": {
        "No normalized stop receipt": 22,
        "Runner status does not establish normalized stop cause": 19
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 22,
      "reasons": {
        "Not available for ungraded delivery": 22
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 46
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Original base revision type not recorded per cell": 46
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Attempt boundary receipts unavailable": 84
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Absolute phase boundary not retained": 84
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Absolute phase boundary not retained": 84
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Absolute phase boundary not retained": 84
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Absolute phase boundary not retained": 84
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Absolute phase boundary not retained": 84
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Absolute phase boundary not retained": 84
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Absolute phase boundary not retained": 84
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Absolute phase boundary not retained": 84
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Absolute phase boundary not retained": 84
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Absolute phase boundary not retained": 84
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Absolute phase boundary not retained": 84
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Absolute phase boundary not retained": 84
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Absolute phase boundary not retained": 84
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Absolute phase boundary not retained": 84
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Phase wall not emitted or not separable": 62
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Phase wall not emitted or not separable": 62
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 41,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Phase wall not emitted or not separable": 19
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Phase wall not emitted or not separable": 62
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Phase wall not emitted or not separable": 62
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Phase wall not emitted or not separable": 62
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Phase wall not emitted or not separable": 62
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 22,
      "reasons": {
        "Not available for ungraded delivery": 22
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 22,
      "reasons": {
        "Not available for ungraded delivery": 22
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 22,
      "reasons": {
        "Not available for ungraded delivery": 22
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 22,
      "reasons": {
        "Not available for ungraded delivery": 22
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 62,
        "Usage counter unavailable": 22
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 62,
        "Usage counter unavailable": 22
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 62,
        "Usage counter unavailable": 22
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 84,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 62,
        "Usage counter unavailable": 22
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 62,
        "Not available for ungraded delivery": 22
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 62,
        "Not available for ungraded delivery": 22
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 62,
        "Not available for ungraded delivery": 22
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Toolchain version/inventory not recorded": 62
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Toolchain version/inventory not recorded": 62
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Toolchain version/inventory not recorded": 62
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Toolchain version/inventory not recorded": 62
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Toolchain version/inventory not recorded": 62
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Toolchain version/inventory not recorded": 62
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 84
      },
      "circumstances.concurrent_cells_end": {
        "none": 34
      },
      "circumstances.concurrent_cells_start": {
        "none": 34
      },
      "circumstances.load1_end": {
        "none": 84
      },
      "circumstances.load_samples": {
        "none": 34
      },
      "cost.accounting": {
        "none": 22
      },
      "cost.calculator_version": {
        "none": 22
      },
      "cost.long_context_reconciled": {
        "none": 22
      },
      "cost.price_table_version": {
        "none": 22
      },
      "cost.usd": {
        "none": 84
      },
      "effort.effective": {
        "none": 41
      },
      "environment.account_class": {
        "none": 34
      },
      "environment.cores": {
        "none": 84
      },
      "environment.cpu_model": {
        "none": 84
      },
      "environment.kernel": {
        "none": 50
      },
      "environment.ram_gib": {
        "none": 84
      },
      "environment.toolchains.elixir": {
        "none": 84
      },
      "environment.toolchains.erlang": {
        "none": 84
      },
      "environment.toolchains.node": {
        "none": 84
      },
      "environment.toolchains.other_inventory": {
        "none": 84
      },
      "environment.toolchains.ruby": {
        "none": 84
      },
      "environment.toolchains.rust": {
        "none": 84
      },
      "grade.grader": {
        "not re-derivable from the public record": 22
      },
      "grade.tests_ran": {
        "none": 19,
        "not re-derivable from the public record": 22
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 22
      },
      "host.cpu": {
        "none": 84
      },
      "host.kernel": {
        "none": 50
      },
      "host.ram_gib": {
        "none": 84
      },
      "host.spec_ref": {
        "none": 22
      },
      "host.vcpu": {
        "none": 84
      },
      "itt.class": {
        "none": 22
      },
      "itt.cohort": {
        "none": 22
      },
      "itt.evidence_ref": {
        "none": 22
      },
      "model.effective": {
        "none": 41
      },
      "outcome": {
        "none": 1,
        "not re-derivable from the public record": 22
      },
      "recipe": {
        "none": 84
      },
      "setup.deps_source": {
        "none": 84
      },
      "setup.task_base.hash": {
        "none": 68
      },
      "setup.task_base.kind": {
        "none": 68
      },
      "stop_reason": {
        "none": 41
      },
      "task.base_repo": {
        "none": 22
      },
      "task.base_revision.hash": {
        "none": 68
      },
      "task.base_revision.kind": {
        "none": 68
      },
      "timestamps.attempts": {
        "none": 84
      },
      "timestamps.phases.develop.end_utc": {
        "none": 84
      },
      "timestamps.phases.develop.start_utc": {
        "none": 84
      },
      "timestamps.phases.gate.end_utc": {
        "none": 84
      },
      "timestamps.phases.gate.start_utc": {
        "none": 84
      },
      "timestamps.phases.grade.end_utc": {
        "none": 84
      },
      "timestamps.phases.grade.start_utc": {
        "none": 84
      },
      "timestamps.phases.plan.end_utc": {
        "none": 84
      },
      "timestamps.phases.plan.start_utc": {
        "none": 84
      },
      "timestamps.phases.review.end_utc": {
        "none": 84
      },
      "timestamps.phases.review.start_utc": {
        "none": 84
      },
      "timestamps.phases.setup.end_utc": {
        "none": 84
      },
      "timestamps.phases.setup.start_utc": {
        "none": 84
      },
      "timestamps.phases.shape.end_utc": {
        "none": 84
      },
      "timestamps.phases.shape.start_utc": {
        "none": 84
      },
      "timing.phases_s.develop": {
        "none": 84
      },
      "timing.phases_s.gate": {
        "none": 84
      },
      "timing.phases_s.grade": {
        "none": 41
      },
      "timing.phases_s.plan": {
        "none": 84
      },
      "timing.phases_s.review": {
        "none": 84
      },
      "timing.phases_s.setup": {
        "none": 84
      },
      "timing.phases_s.shape": {
        "none": 84
      },
      "tokens.phases.develop.cached_input": {
        "none": 84
      },
      "tokens.phases.develop.input": {
        "none": 84
      },
      "tokens.phases.develop.output": {
        "none": 84
      },
      "tokens.phases.develop.reasoning": {
        "none": 84
      },
      "tokens.phases.gate.cached_input": {
        "none": 84
      },
      "tokens.phases.gate.input": {
        "none": 84
      },
      "tokens.phases.gate.output": {
        "none": 84
      },
      "tokens.phases.gate.reasoning": {
        "none": 84
      },
      "tokens.phases.grade.cached_input": {
        "none": 22
      },
      "tokens.phases.grade.input": {
        "none": 22
      },
      "tokens.phases.grade.output": {
        "none": 22
      },
      "tokens.phases.grade.reasoning": {
        "none": 22
      },
      "tokens.phases.plan.cached_input": {
        "none": 84
      },
      "tokens.phases.plan.input": {
        "none": 84
      },
      "tokens.phases.plan.output": {
        "none": 84
      },
      "tokens.phases.plan.reasoning": {
        "none": 84
      },
      "tokens.phases.review.cached_input": {
        "none": 84
      },
      "tokens.phases.review.input": {
        "none": 84
      },
      "tokens.phases.review.output": {
        "none": 84
      },
      "tokens.phases.review.reasoning": {
        "none": 84
      },
      "tokens.phases.setup.cached_input": {
        "none": 84
      },
      "tokens.phases.setup.input": {
        "none": 84
      },
      "tokens.phases.setup.output": {
        "none": 84
      },
      "tokens.phases.setup.reasoning": {
        "none": 84
      },
      "tokens.phases.shape.cached_input": {
        "none": 84
      },
      "tokens.phases.shape.input": {
        "none": 84
      },
      "tokens.phases.shape.output": {
        "none": 84
      },
      "tokens.phases.shape.reasoning": {
        "none": 84
      },
      "tokens.total.cached_input": {
        "none": 84
      },
      "tokens.total.input": {
        "none": 84
      },
      "tokens.total.output": {
        "none": 84
      },
      "tokens.total.reasoning": {
        "none": 84
      },
      "tools.codex_cli": {
        "none": 84
      },
      "tools.grader": {
        "none": 84
      },
      "tools.runner": {
        "none": 84
      },
      "tools.toolchains.elixir": {
        "none": 84
      },
      "tools.toolchains.erlang": {
        "none": 84
      },
      "tools.toolchains.node": {
        "none": 84
      },
      "tools.toolchains.other_inventory": {
        "none": 84
      },
      "tools.toolchains.ruby": {
        "none": 84
      },
      "tools.toolchains.rust": {
        "none": 84
      }
    },
    "reconstructable": {}
  },
  "round": "r37"
}
```
