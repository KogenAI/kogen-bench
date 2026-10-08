# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 36,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Boundary telemetry not retained": 36
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Boundary telemetry not retained": 6
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 6
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Boundary telemetry not retained": 36
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "No matching controller samples retained": 6
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 7,
      "reasons": {
        "Not available for ungraded delivery": 7
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 7,
      "reasons": {
        "Not available for ungraded delivery": 7
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 7,
      "reasons": {
        "Not available for ungraded delivery": 7
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 7,
      "reasons": {
        "Not available for ungraded delivery": 7
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Complete per-model billable vector unavailable": 29,
        "Not available for ungraded delivery": 7
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 7,
      "reasons": {
        "Not recorded in available public metadata": 7
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "No dated account-class receipt": 6
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "No per-cell CPU allocation receipt": 29,
        "Not available for ungraded delivery": 7
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "No per-cell CPU receipt": 29,
        "Not available for ungraded delivery": 7
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "No per-cell kernel receipt": 23,
        "Not available for ungraded delivery": 7
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "No per-cell RAM receipt": 29,
        "Not available for ungraded delivery": 7
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 29
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 29
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 29
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 29
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 29
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 29
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 7,
      "reasons": {
        "No official grade in the public snapshot": 7
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 7,
      "reasons": {
        "No official grade in the public snapshot": 7
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 7,
      "reasons": {
        "No official grade in the public snapshot": 7
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 36,
      "reasons": {
        "No per-cell CPU receipt": 29,
        "Not available for ungraded delivery": 7
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 30,
      "reasons": {
        "No per-cell kernel receipt": 23,
        "Not available for ungraded delivery": 7
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 36,
      "reasons": {
        "No per-cell RAM receipt": 29,
        "Not available for ungraded delivery": 7
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 7,
      "reasons": {
        "Not available for ungraded delivery": 7
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 36,
      "reasons": {
        "No per-cell CPU allocation receipt": 29,
        "Not available for ungraded delivery": 7
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 7,
      "reasons": {
        "Ungraded delivery needs evidence audit": 7
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 7,
      "reasons": {
        "No captured cohort launch receipt": 7
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 7,
      "reasons": {
        "No audited ITT receipt": 7
      }
    },
    "model.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 7,
      "reasons": {
        "Not recorded in available public metadata": 7
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 7,
      "reasons": {
        "No official grade in the public snapshot": 7
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Not recorded in available public metadata": 29
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Dependency source not pinned per cell": 36
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 17
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Original base revision type not recorded per cell": 17
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 7,
      "reasons": {
        "No normalized stop receipt": 7
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 7,
      "reasons": {
        "Not available for ungraded delivery": 7
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 17
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Original base revision type not recorded per cell": 17
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Attempt boundary receipts unavailable": 36
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Absolute phase boundary not retained": 36
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Absolute phase boundary not retained": 36
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Absolute phase boundary not retained": 36
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Absolute phase boundary not retained": 36
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Absolute phase boundary not retained": 36
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Absolute phase boundary not retained": 36
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Absolute phase boundary not retained": 36
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Absolute phase boundary not retained": 36
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Absolute phase boundary not retained": 36
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Absolute phase boundary not retained": 36
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Absolute phase boundary not retained": 36
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Absolute phase boundary not retained": 36
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Absolute phase boundary not retained": 36
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Absolute phase boundary not retained": 36
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Phase wall not emitted or not separable": 29
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Phase wall not emitted or not separable": 29
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 7,
      "reasons": {
        "Not available for ungraded delivery": 7
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Phase wall not emitted or not separable": 29
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Phase wall not emitted or not separable": 29
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Phase wall not emitted or not separable": 29
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Phase wall not emitted or not separable": 29
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 29
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 29
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 29
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 29
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 29
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 29
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 29
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 29
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 7,
      "reasons": {
        "Not available for ungraded delivery": 7
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 7,
      "reasons": {
        "Not available for ungraded delivery": 7
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 7,
      "reasons": {
        "Not available for ungraded delivery": 7
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 7,
      "reasons": {
        "Not available for ungraded delivery": 7
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 29
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 29
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 29
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 29
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 29
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 29
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 29
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 29
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 29
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 29
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 29
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 29
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 29
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 29
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 29
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 29
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 29,
        "Usage counter unavailable": 7
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 29,
        "Usage counter unavailable": 7
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 29,
        "Usage counter unavailable": 7
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 36,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 29,
        "Usage counter unavailable": 7
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 29,
        "Not available for ungraded delivery": 7
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 29,
        "Not available for ungraded delivery": 7
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 29,
        "Not available for ungraded delivery": 7
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 29
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 29
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 29
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 29
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 29
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 29
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 36
      },
      "circumstances.concurrent_cells_end": {
        "none": 6
      },
      "circumstances.concurrent_cells_start": {
        "none": 6
      },
      "circumstances.load1_end": {
        "none": 36
      },
      "circumstances.load_samples": {
        "none": 6
      },
      "cost.accounting": {
        "none": 7
      },
      "cost.calculator_version": {
        "none": 7
      },
      "cost.long_context_reconciled": {
        "none": 7
      },
      "cost.price_table_version": {
        "none": 7
      },
      "cost.usd": {
        "none": 36
      },
      "effort.effective": {
        "none": 7
      },
      "environment.account_class": {
        "none": 6
      },
      "environment.cores": {
        "none": 36
      },
      "environment.cpu_model": {
        "none": 36
      },
      "environment.kernel": {
        "none": 30
      },
      "environment.ram_gib": {
        "none": 36
      },
      "environment.toolchains.elixir": {
        "none": 36
      },
      "environment.toolchains.erlang": {
        "none": 36
      },
      "environment.toolchains.node": {
        "none": 36
      },
      "environment.toolchains.other_inventory": {
        "none": 36
      },
      "environment.toolchains.ruby": {
        "none": 36
      },
      "environment.toolchains.rust": {
        "none": 36
      },
      "grade.grader": {
        "not re-derivable from the public record": 7
      },
      "grade.tests_ran": {
        "not re-derivable from the public record": 7
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 7
      },
      "host.cpu": {
        "none": 36
      },
      "host.kernel": {
        "none": 30
      },
      "host.ram_gib": {
        "none": 36
      },
      "host.spec_ref": {
        "none": 7
      },
      "host.vcpu": {
        "none": 36
      },
      "itt.class": {
        "none": 7
      },
      "itt.cohort": {
        "none": 7
      },
      "itt.evidence_ref": {
        "none": 7
      },
      "model.effective": {
        "none": 7
      },
      "outcome": {
        "not re-derivable from the public record": 7
      },
      "recipe": {
        "none": 36
      },
      "setup.deps_source": {
        "none": 36
      },
      "setup.task_base.hash": {
        "none": 24
      },
      "setup.task_base.kind": {
        "none": 24
      },
      "stop_reason": {
        "none": 7
      },
      "task.base_repo": {
        "none": 7
      },
      "task.base_revision.hash": {
        "none": 24
      },
      "task.base_revision.kind": {
        "none": 24
      },
      "timestamps.attempts": {
        "none": 36
      },
      "timestamps.phases.develop.end_utc": {
        "none": 36
      },
      "timestamps.phases.develop.start_utc": {
        "none": 36
      },
      "timestamps.phases.gate.end_utc": {
        "none": 36
      },
      "timestamps.phases.gate.start_utc": {
        "none": 36
      },
      "timestamps.phases.grade.end_utc": {
        "none": 36
      },
      "timestamps.phases.grade.start_utc": {
        "none": 36
      },
      "timestamps.phases.plan.end_utc": {
        "none": 36
      },
      "timestamps.phases.plan.start_utc": {
        "none": 36
      },
      "timestamps.phases.review.end_utc": {
        "none": 36
      },
      "timestamps.phases.review.start_utc": {
        "none": 36
      },
      "timestamps.phases.setup.end_utc": {
        "none": 36
      },
      "timestamps.phases.setup.start_utc": {
        "none": 36
      },
      "timestamps.phases.shape.end_utc": {
        "none": 36
      },
      "timestamps.phases.shape.start_utc": {
        "none": 36
      },
      "timing.phases_s.develop": {
        "none": 36
      },
      "timing.phases_s.gate": {
        "none": 36
      },
      "timing.phases_s.grade": {
        "none": 7
      },
      "timing.phases_s.plan": {
        "none": 36
      },
      "timing.phases_s.review": {
        "none": 36
      },
      "timing.phases_s.setup": {
        "none": 36
      },
      "timing.phases_s.shape": {
        "none": 36
      },
      "tokens.phases.develop.cached_input": {
        "none": 36
      },
      "tokens.phases.develop.input": {
        "none": 36
      },
      "tokens.phases.develop.output": {
        "none": 36
      },
      "tokens.phases.develop.reasoning": {
        "none": 36
      },
      "tokens.phases.gate.cached_input": {
        "none": 36
      },
      "tokens.phases.gate.input": {
        "none": 36
      },
      "tokens.phases.gate.output": {
        "none": 36
      },
      "tokens.phases.gate.reasoning": {
        "none": 36
      },
      "tokens.phases.grade.cached_input": {
        "none": 7
      },
      "tokens.phases.grade.input": {
        "none": 7
      },
      "tokens.phases.grade.output": {
        "none": 7
      },
      "tokens.phases.grade.reasoning": {
        "none": 7
      },
      "tokens.phases.plan.cached_input": {
        "none": 36
      },
      "tokens.phases.plan.input": {
        "none": 36
      },
      "tokens.phases.plan.output": {
        "none": 36
      },
      "tokens.phases.plan.reasoning": {
        "none": 36
      },
      "tokens.phases.review.cached_input": {
        "none": 36
      },
      "tokens.phases.review.input": {
        "none": 36
      },
      "tokens.phases.review.output": {
        "none": 36
      },
      "tokens.phases.review.reasoning": {
        "none": 36
      },
      "tokens.phases.setup.cached_input": {
        "none": 36
      },
      "tokens.phases.setup.input": {
        "none": 36
      },
      "tokens.phases.setup.output": {
        "none": 36
      },
      "tokens.phases.setup.reasoning": {
        "none": 36
      },
      "tokens.phases.shape.cached_input": {
        "none": 36
      },
      "tokens.phases.shape.input": {
        "none": 36
      },
      "tokens.phases.shape.output": {
        "none": 36
      },
      "tokens.phases.shape.reasoning": {
        "none": 36
      },
      "tokens.total.cached_input": {
        "none": 36
      },
      "tokens.total.input": {
        "none": 36
      },
      "tokens.total.output": {
        "none": 36
      },
      "tokens.total.reasoning": {
        "none": 36
      },
      "tools.codex_cli": {
        "none": 36
      },
      "tools.grader": {
        "none": 36
      },
      "tools.runner": {
        "none": 36
      },
      "tools.toolchains.elixir": {
        "none": 36
      },
      "tools.toolchains.erlang": {
        "none": 36
      },
      "tools.toolchains.node": {
        "none": 36
      },
      "tools.toolchains.other_inventory": {
        "none": 36
      },
      "tools.toolchains.ruby": {
        "none": 36
      },
      "tools.toolchains.rust": {
        "none": 36
      }
    },
    "reconstructable": {}
  },
  "round": "r23"
}
```
