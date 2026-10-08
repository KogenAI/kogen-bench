# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 198,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Boundary telemetry not retained": 198
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Boundary telemetry not retained": 45
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 45
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Boundary telemetry not retained": 198
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "No matching controller samples retained": 45
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 24
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 24
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 24
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 24
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 198,
      "reasons": {
        "Complete per-model billable vector unavailable": 174,
        "Not available for ungraded delivery": 24
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "No dated account-class receipt": 45
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "No per-cell CPU allocation receipt": 174,
        "Not available for ungraded delivery": 24
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "No per-cell CPU receipt": 174,
        "Not available for ungraded delivery": 24
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 153,
      "reasons": {
        "No per-cell kernel receipt": 129,
        "Not available for ungraded delivery": 24
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "No per-cell RAM receipt": 174,
        "Not available for ungraded delivery": 24
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Toolchain version/inventory not recorded": 174
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Toolchain version/inventory not recorded": 174
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Toolchain version/inventory not recorded": 174
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Toolchain version/inventory not recorded": 174
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Toolchain version/inventory not recorded": 174
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Toolchain version/inventory not recorded": 174
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 24,
      "reasons": {
        "No official grade in the public snapshot": 24
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 24,
      "reasons": {
        "No official grade in the public snapshot": 24
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 24,
      "reasons": {
        "No official grade in the public snapshot": 24
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 198,
      "reasons": {
        "No per-cell CPU receipt": 174,
        "Not available for ungraded delivery": 24
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 153,
      "reasons": {
        "No per-cell kernel receipt": 129,
        "Not available for ungraded delivery": 24
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 198,
      "reasons": {
        "No per-cell RAM receipt": 174,
        "Not available for ungraded delivery": 24
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 24
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 198,
      "reasons": {
        "No per-cell CPU allocation receipt": 174,
        "Not available for ungraded delivery": 24
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 25,
      "reasons": {
        "Invalid/environment cause requires evidence audit": 1,
        "Ungraded delivery needs evidence audit": 24
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 24,
      "reasons": {
        "No captured cohort launch receipt": 24
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 25,
      "reasons": {
        "No audited ITT receipt": 24,
        "No evidence-backed ITT classification": 1
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 24,
      "reasons": {
        "No official grade in the public snapshot": 24
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Not recorded in available public metadata": 174
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Dependency source not pinned per cell": 198
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 153,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 129
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 153,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Original base revision type not recorded per cell": 129
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 14,
      "reasons": {
        "No normalized stop receipt": 14
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 24
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 153,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 129
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 153,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Original base revision type not recorded per cell": 129
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Attempt boundary receipts unavailable": 198
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Absolute phase boundary not retained": 198
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Absolute phase boundary not retained": 198
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Absolute phase boundary not retained": 198
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Absolute phase boundary not retained": 198
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Absolute phase boundary not retained": 198
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Absolute phase boundary not retained": 198
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Absolute phase boundary not retained": 198
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Absolute phase boundary not retained": 198
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Absolute phase boundary not retained": 198
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Absolute phase boundary not retained": 198
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Absolute phase boundary not retained": 198
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Absolute phase boundary not retained": 198
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Absolute phase boundary not retained": 198
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Absolute phase boundary not retained": 198
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Phase wall not emitted or not separable": 174
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Phase wall not emitted or not separable": 174
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 24
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Phase wall not emitted or not separable": 174
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Phase wall not emitted or not separable": 174
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Phase wall not emitted or not separable": 174
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Phase wall not emitted or not separable": 174
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Per-phase token counter not emitted": 174
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Per-phase token counter not emitted": 174
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Per-phase token counter not emitted": 174
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Per-phase token counter not emitted": 174
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Per-phase token counter not emitted": 174
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Per-phase token counter not emitted": 174
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Per-phase token counter not emitted": 174
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Per-phase token counter not emitted": 174
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 24
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 24
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 24
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 24
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Per-phase token counter not emitted": 174
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Per-phase token counter not emitted": 174
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Per-phase token counter not emitted": 174
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Per-phase token counter not emitted": 174
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Per-phase token counter not emitted": 174
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Per-phase token counter not emitted": 174
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Per-phase token counter not emitted": 174
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Per-phase token counter not emitted": 174
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Per-phase token counter not emitted": 174
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Per-phase token counter not emitted": 174
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Per-phase token counter not emitted": 174
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Per-phase token counter not emitted": 174
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Per-phase token counter not emitted": 174
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Per-phase token counter not emitted": 174
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Per-phase token counter not emitted": 174
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Per-phase token counter not emitted": 174
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 174,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 174
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 174,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 174
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 174,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 174
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 174,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 174
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 174,
        "Not available for ungraded delivery": 24
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 174,
        "Not available for ungraded delivery": 24
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 174,
        "Not available for ungraded delivery": 24
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Toolchain version/inventory not recorded": 174
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Toolchain version/inventory not recorded": 174
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Toolchain version/inventory not recorded": 174
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Toolchain version/inventory not recorded": 174
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Toolchain version/inventory not recorded": 174
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 198,
      "reasons": {
        "Not available for ungraded delivery": 24,
        "Toolchain version/inventory not recorded": 174
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 198
      },
      "circumstances.concurrent_cells_end": {
        "none": 45
      },
      "circumstances.concurrent_cells_start": {
        "none": 45
      },
      "circumstances.load1_end": {
        "none": 198
      },
      "circumstances.load_samples": {
        "none": 45
      },
      "cost.accounting": {
        "none": 24
      },
      "cost.calculator_version": {
        "none": 24
      },
      "cost.long_context_reconciled": {
        "none": 24
      },
      "cost.price_table_version": {
        "none": 24
      },
      "cost.usd": {
        "none": 198
      },
      "environment.account_class": {
        "none": 45
      },
      "environment.cores": {
        "none": 198
      },
      "environment.cpu_model": {
        "none": 198
      },
      "environment.kernel": {
        "none": 153
      },
      "environment.ram_gib": {
        "none": 198
      },
      "environment.toolchains.elixir": {
        "none": 198
      },
      "environment.toolchains.erlang": {
        "none": 198
      },
      "environment.toolchains.node": {
        "none": 198
      },
      "environment.toolchains.other_inventory": {
        "none": 198
      },
      "environment.toolchains.ruby": {
        "none": 198
      },
      "environment.toolchains.rust": {
        "none": 198
      },
      "grade.grader": {
        "not re-derivable from the public record": 24
      },
      "grade.tests_ran": {
        "not re-derivable from the public record": 24
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 24
      },
      "host.cpu": {
        "none": 198
      },
      "host.kernel": {
        "none": 153
      },
      "host.ram_gib": {
        "none": 198
      },
      "host.spec_ref": {
        "none": 24
      },
      "host.vcpu": {
        "none": 198
      },
      "itt.class": {
        "none": 25
      },
      "itt.cohort": {
        "none": 24
      },
      "itt.evidence_ref": {
        "none": 25
      },
      "outcome": {
        "not re-derivable from the public record": 24
      },
      "recipe": {
        "none": 198
      },
      "setup.deps_source": {
        "none": 198
      },
      "setup.task_base.hash": {
        "none": 153
      },
      "setup.task_base.kind": {
        "none": 153
      },
      "stop_reason": {
        "none": 14
      },
      "task.base_repo": {
        "none": 24
      },
      "task.base_revision.hash": {
        "none": 153
      },
      "task.base_revision.kind": {
        "none": 153
      },
      "timestamps.attempts": {
        "none": 198
      },
      "timestamps.phases.develop.end_utc": {
        "none": 198
      },
      "timestamps.phases.develop.start_utc": {
        "none": 198
      },
      "timestamps.phases.gate.end_utc": {
        "none": 198
      },
      "timestamps.phases.gate.start_utc": {
        "none": 198
      },
      "timestamps.phases.grade.end_utc": {
        "none": 198
      },
      "timestamps.phases.grade.start_utc": {
        "none": 198
      },
      "timestamps.phases.plan.end_utc": {
        "none": 198
      },
      "timestamps.phases.plan.start_utc": {
        "none": 198
      },
      "timestamps.phases.review.end_utc": {
        "none": 198
      },
      "timestamps.phases.review.start_utc": {
        "none": 198
      },
      "timestamps.phases.setup.end_utc": {
        "none": 198
      },
      "timestamps.phases.setup.start_utc": {
        "none": 198
      },
      "timestamps.phases.shape.end_utc": {
        "none": 198
      },
      "timestamps.phases.shape.start_utc": {
        "none": 198
      },
      "timing.phases_s.develop": {
        "none": 198
      },
      "timing.phases_s.gate": {
        "none": 198
      },
      "timing.phases_s.grade": {
        "none": 24
      },
      "timing.phases_s.plan": {
        "none": 198
      },
      "timing.phases_s.review": {
        "none": 198
      },
      "timing.phases_s.setup": {
        "none": 198
      },
      "timing.phases_s.shape": {
        "none": 198
      },
      "tokens.phases.develop.cached_input": {
        "none": 198
      },
      "tokens.phases.develop.input": {
        "none": 198
      },
      "tokens.phases.develop.output": {
        "none": 198
      },
      "tokens.phases.develop.reasoning": {
        "none": 198
      },
      "tokens.phases.gate.cached_input": {
        "none": 198
      },
      "tokens.phases.gate.input": {
        "none": 198
      },
      "tokens.phases.gate.output": {
        "none": 198
      },
      "tokens.phases.gate.reasoning": {
        "none": 198
      },
      "tokens.phases.grade.cached_input": {
        "none": 24
      },
      "tokens.phases.grade.input": {
        "none": 24
      },
      "tokens.phases.grade.output": {
        "none": 24
      },
      "tokens.phases.grade.reasoning": {
        "none": 24
      },
      "tokens.phases.plan.cached_input": {
        "none": 198
      },
      "tokens.phases.plan.input": {
        "none": 198
      },
      "tokens.phases.plan.output": {
        "none": 198
      },
      "tokens.phases.plan.reasoning": {
        "none": 198
      },
      "tokens.phases.review.cached_input": {
        "none": 198
      },
      "tokens.phases.review.input": {
        "none": 198
      },
      "tokens.phases.review.output": {
        "none": 198
      },
      "tokens.phases.review.reasoning": {
        "none": 198
      },
      "tokens.phases.setup.cached_input": {
        "none": 198
      },
      "tokens.phases.setup.input": {
        "none": 198
      },
      "tokens.phases.setup.output": {
        "none": 198
      },
      "tokens.phases.setup.reasoning": {
        "none": 198
      },
      "tokens.phases.shape.cached_input": {
        "none": 198
      },
      "tokens.phases.shape.input": {
        "none": 198
      },
      "tokens.phases.shape.output": {
        "none": 198
      },
      "tokens.phases.shape.reasoning": {
        "none": 198
      },
      "tokens.total.cached_input": {
        "none": 174
      },
      "tokens.total.input": {
        "none": 174
      },
      "tokens.total.output": {
        "none": 174
      },
      "tokens.total.reasoning": {
        "none": 174
      },
      "tools.codex_cli": {
        "none": 198
      },
      "tools.grader": {
        "none": 198
      },
      "tools.runner": {
        "none": 198
      },
      "tools.toolchains.elixir": {
        "none": 198
      },
      "tools.toolchains.erlang": {
        "none": 198
      },
      "tools.toolchains.node": {
        "none": 198
      },
      "tools.toolchains.other_inventory": {
        "none": 198
      },
      "tools.toolchains.ruby": {
        "none": 198
      },
      "tools.toolchains.rust": {
        "none": 198
      }
    },
    "reconstructable": {}
  },
  "round": "r50"
}
```
