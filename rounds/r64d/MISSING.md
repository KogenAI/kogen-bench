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
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Boundary telemetry not retained": 20
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
      "count": 20,
      "reasons": {
        "Complete per-model billable vector unavailable": 19,
        "Not available for ungraded delivery": 1
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "No per-cell CPU allocation receipt": 19,
        "Not available for ungraded delivery": 1
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "No per-cell CPU receipt": 19,
        "Not available for ungraded delivery": 1
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "No per-cell kernel receipt": 19,
        "Not available for ungraded delivery": 1
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "No per-cell RAM receipt": 19,
        "Not available for ungraded delivery": 1
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 19
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 19
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 19
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 19
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 19
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 19
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
      "count": 1,
      "reasons": {
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
      "count": 20,
      "reasons": {
        "No per-cell CPU receipt": 19,
        "Not available for ungraded delivery": 1
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 20,
      "reasons": {
        "No per-cell kernel receipt": 19,
        "Not available for ungraded delivery": 1
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 20,
      "reasons": {
        "No per-cell RAM receipt": 19,
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
      "count": 20,
      "reasons": {
        "No per-cell CPU allocation receipt": 19,
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
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Not recorded in available public metadata": 19
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
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 19
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Original base revision type not recorded per cell": 19
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
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 19
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Original base revision type not recorded per cell": 19
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
        "Not available for ungraded delivery": 1,
        "Phase wall not emitted or not separable": 19
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Phase wall not emitted or not separable": 19
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Phase wall not emitted or not separable": 19
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Phase wall not emitted or not separable": 19
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Phase wall not emitted or not separable": 19
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Phase wall not emitted or not separable": 19
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 19
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 19
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 19
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 19
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 19
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 19
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 19
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 19
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
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 19
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 19
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 19
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 19
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 19
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 19
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 19
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 19
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 19
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 19
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 19
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 19
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 19
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 19
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 19
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 19
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 19,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 19
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 19,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 19
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 19,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 19
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 19,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 19
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 19,
        "Not available for ungraded delivery": 1
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 19,
        "Not available for ungraded delivery": 1
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 19,
        "Not available for ungraded delivery": 1
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 19
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 19
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 19
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 19
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 19
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 19
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 20
      },
      "circumstances.load1_end": {
        "none": 20
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
        "none": 20
      },
      "environment.cores": {
        "none": 20
      },
      "environment.cpu_model": {
        "none": 20
      },
      "environment.kernel": {
        "none": 20
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
        "not re-derivable from the public record": 1
      },
      "grade.tests_ran": {
        "not re-derivable from the public record": 1
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 1
      },
      "host.cpu": {
        "none": 20
      },
      "host.kernel": {
        "none": 20
      },
      "host.ram_gib": {
        "none": 20
      },
      "host.spec_ref": {
        "none": 1
      },
      "host.vcpu": {
        "none": 20
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
        "none": 20
      },
      "setup.deps_source": {
        "none": 20
      },
      "setup.task_base.hash": {
        "none": 20
      },
      "setup.task_base.kind": {
        "none": 20
      },
      "stop_reason": {
        "none": 1
      },
      "task.base_repo": {
        "none": 1
      },
      "task.base_revision.hash": {
        "none": 20
      },
      "task.base_revision.kind": {
        "none": 20
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
        "none": 1
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
  "publication_reconciliation": {
    "disposition": "This held-out capture remains distinct from r64/r64b/r64c/r64e and historical direct anchors. Do not treat its public delivery table as a cross-round comparison.",
    "original_execution_command": "not recorded in the public snapshot",
    "harness_source_commit": "absent; tools.harness values are wrapper fingerprints",
    "kogen_source_commit": "Public records mark the Kogen product commit not applicable for these harness records.",
    "raw_public_records": [
      "results/run-records/r64d.jsonl",
      "results/cells.jsonl"
    ],
    "public_record_rebuild": "python3 reproduce/export_results.py; python3 reproduce/build_records.py; python3 reproduce/validate_round.py --round r64d"
  },
  "round": "r64d"
}
```
