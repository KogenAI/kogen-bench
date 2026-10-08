# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 55,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Boundary telemetry not retained": 55
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
      "count": 55,
      "reasons": {
        "Boundary telemetry not retained": 55
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "No matching controller samples retained": 15
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
      "count": 55,
      "reasons": {
        "Complete per-model billable vector unavailable": 49,
        "Not available for ungraded delivery": 6
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Not recorded in available public metadata": 6
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
      "count": 55,
      "reasons": {
        "No per-cell CPU allocation receipt": 49,
        "Not available for ungraded delivery": 6
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "No per-cell CPU receipt": 49,
        "Not available for ungraded delivery": 6
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "No per-cell kernel receipt": 34,
        "Not available for ungraded delivery": 6
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "No per-cell RAM receipt": 49,
        "Not available for ungraded delivery": 6
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 49
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 49
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 49
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 49
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 49
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 49
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
      "count": 55,
      "reasons": {
        "No per-cell CPU receipt": 49,
        "Not available for ungraded delivery": 6
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 40,
      "reasons": {
        "No per-cell kernel receipt": 34,
        "Not available for ungraded delivery": 6
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 55,
      "reasons": {
        "No per-cell RAM receipt": 49,
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
      "count": 55,
      "reasons": {
        "No per-cell CPU allocation receipt": 49,
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
      "count": 6,
      "reasons": {
        "Not recorded in available public metadata": 6
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
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Not recorded in available public metadata": 49
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Dependency source not pinned per cell": 55
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 34
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Original base revision type not recorded per cell": 34
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 6,
      "reasons": {
        "No normalized stop receipt": 6
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
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 34
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Original base revision type not recorded per cell": 34
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Attempt boundary receipts unavailable": 55
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Absolute phase boundary not retained": 55
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Absolute phase boundary not retained": 55
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Absolute phase boundary not retained": 55
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Absolute phase boundary not retained": 55
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Absolute phase boundary not retained": 55
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Absolute phase boundary not retained": 55
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Absolute phase boundary not retained": 55
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Absolute phase boundary not retained": 55
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Absolute phase boundary not retained": 55
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Absolute phase boundary not retained": 55
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Absolute phase boundary not retained": 55
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Absolute phase boundary not retained": 55
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Absolute phase boundary not retained": 55
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Absolute phase boundary not retained": 55
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Phase wall not emitted or not separable": 49
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Phase wall not emitted or not separable": 49
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
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Phase wall not emitted or not separable": 49
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Phase wall not emitted or not separable": 49
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Phase wall not emitted or not separable": 49
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Phase wall not emitted or not separable": 49
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 49
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
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 49,
        "Usage counter unavailable": 6
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 49,
        "Usage counter unavailable": 6
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 49,
        "Usage counter unavailable": 6
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 49,
        "Usage counter unavailable": 6
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 49,
        "Not available for ungraded delivery": 6
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 49,
        "Not available for ungraded delivery": 6
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 49,
        "Not available for ungraded delivery": 6
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 49
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 49
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 49
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 49
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 49
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 6,
        "Toolchain version/inventory not recorded": 49
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 55
      },
      "circumstances.concurrent_cells_end": {
        "none": 15
      },
      "circumstances.concurrent_cells_start": {
        "none": 15
      },
      "circumstances.load1_end": {
        "none": 55
      },
      "circumstances.load_samples": {
        "none": 15
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
        "none": 55
      },
      "effort.effective": {
        "none": 6
      },
      "environment.account_class": {
        "none": 15
      },
      "environment.cores": {
        "none": 55
      },
      "environment.cpu_model": {
        "none": 55
      },
      "environment.kernel": {
        "none": 40
      },
      "environment.ram_gib": {
        "none": 55
      },
      "environment.toolchains.elixir": {
        "none": 55
      },
      "environment.toolchains.erlang": {
        "none": 55
      },
      "environment.toolchains.node": {
        "none": 55
      },
      "environment.toolchains.other_inventory": {
        "none": 55
      },
      "environment.toolchains.ruby": {
        "none": 55
      },
      "environment.toolchains.rust": {
        "none": 55
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
        "none": 55
      },
      "host.kernel": {
        "none": 40
      },
      "host.ram_gib": {
        "none": 55
      },
      "host.spec_ref": {
        "none": 6
      },
      "host.vcpu": {
        "none": 55
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
        "none": 6
      },
      "outcome": {
        "not re-derivable from the public record": 6
      },
      "recipe": {
        "none": 55
      },
      "setup.deps_source": {
        "none": 55
      },
      "setup.task_base.hash": {
        "none": 40
      },
      "setup.task_base.kind": {
        "none": 40
      },
      "stop_reason": {
        "none": 6
      },
      "task.base_repo": {
        "none": 6
      },
      "task.base_revision.hash": {
        "none": 40
      },
      "task.base_revision.kind": {
        "none": 40
      },
      "timestamps.attempts": {
        "none": 55
      },
      "timestamps.phases.develop.end_utc": {
        "none": 55
      },
      "timestamps.phases.develop.start_utc": {
        "none": 55
      },
      "timestamps.phases.gate.end_utc": {
        "none": 55
      },
      "timestamps.phases.gate.start_utc": {
        "none": 55
      },
      "timestamps.phases.grade.end_utc": {
        "none": 55
      },
      "timestamps.phases.grade.start_utc": {
        "none": 55
      },
      "timestamps.phases.plan.end_utc": {
        "none": 55
      },
      "timestamps.phases.plan.start_utc": {
        "none": 55
      },
      "timestamps.phases.review.end_utc": {
        "none": 55
      },
      "timestamps.phases.review.start_utc": {
        "none": 55
      },
      "timestamps.phases.setup.end_utc": {
        "none": 55
      },
      "timestamps.phases.setup.start_utc": {
        "none": 55
      },
      "timestamps.phases.shape.end_utc": {
        "none": 55
      },
      "timestamps.phases.shape.start_utc": {
        "none": 55
      },
      "timing.phases_s.develop": {
        "none": 55
      },
      "timing.phases_s.gate": {
        "none": 55
      },
      "timing.phases_s.grade": {
        "none": 6
      },
      "timing.phases_s.plan": {
        "none": 55
      },
      "timing.phases_s.review": {
        "none": 55
      },
      "timing.phases_s.setup": {
        "none": 55
      },
      "timing.phases_s.shape": {
        "none": 55
      },
      "tokens.phases.develop.cached_input": {
        "none": 55
      },
      "tokens.phases.develop.input": {
        "none": 55
      },
      "tokens.phases.develop.output": {
        "none": 55
      },
      "tokens.phases.develop.reasoning": {
        "none": 55
      },
      "tokens.phases.gate.cached_input": {
        "none": 55
      },
      "tokens.phases.gate.input": {
        "none": 55
      },
      "tokens.phases.gate.output": {
        "none": 55
      },
      "tokens.phases.gate.reasoning": {
        "none": 55
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
        "none": 55
      },
      "tokens.phases.plan.input": {
        "none": 55
      },
      "tokens.phases.plan.output": {
        "none": 55
      },
      "tokens.phases.plan.reasoning": {
        "none": 55
      },
      "tokens.phases.review.cached_input": {
        "none": 55
      },
      "tokens.phases.review.input": {
        "none": 55
      },
      "tokens.phases.review.output": {
        "none": 55
      },
      "tokens.phases.review.reasoning": {
        "none": 55
      },
      "tokens.phases.setup.cached_input": {
        "none": 55
      },
      "tokens.phases.setup.input": {
        "none": 55
      },
      "tokens.phases.setup.output": {
        "none": 55
      },
      "tokens.phases.setup.reasoning": {
        "none": 55
      },
      "tokens.phases.shape.cached_input": {
        "none": 55
      },
      "tokens.phases.shape.input": {
        "none": 55
      },
      "tokens.phases.shape.output": {
        "none": 55
      },
      "tokens.phases.shape.reasoning": {
        "none": 55
      },
      "tokens.total.cached_input": {
        "none": 55
      },
      "tokens.total.input": {
        "none": 55
      },
      "tokens.total.output": {
        "none": 55
      },
      "tokens.total.reasoning": {
        "none": 55
      },
      "tools.codex_cli": {
        "none": 55
      },
      "tools.grader": {
        "none": 55
      },
      "tools.runner": {
        "none": 55
      },
      "tools.toolchains.elixir": {
        "none": 55
      },
      "tools.toolchains.erlang": {
        "none": 55
      },
      "tools.toolchains.node": {
        "none": 55
      },
      "tools.toolchains.other_inventory": {
        "none": 55
      },
      "tools.toolchains.ruby": {
        "none": 55
      },
      "tools.toolchains.rust": {
        "none": 55
      }
    },
    "reconstructable": {}
  },
  "round": "r26"
}
```
