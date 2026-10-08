# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 40,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Boundary telemetry not retained": 40
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Boundary telemetry not retained": 40
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "Not available for ungraded delivery": 8
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "Not available for ungraded delivery": 8
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "Not available for ungraded delivery": 8
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "Not available for ungraded delivery": 8
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Complete per-model billable vector unavailable": 32,
        "Not available for ungraded delivery": 8
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 3,
      "reasons": {
        "Not recorded in available public metadata": 3
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "No per-cell CPU allocation receipt": 32,
        "Not available for ungraded delivery": 8
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "No per-cell CPU receipt": 32,
        "Not available for ungraded delivery": 8
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "No per-cell kernel receipt": 32,
        "Not available for ungraded delivery": 8
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "No per-cell RAM receipt": 32,
        "Not available for ungraded delivery": 8
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Toolchain version/inventory not recorded": 32
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Toolchain version/inventory not recorded": 32
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Toolchain version/inventory not recorded": 32
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Toolchain version/inventory not recorded": 32
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Toolchain version/inventory not recorded": 32
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Toolchain version/inventory not recorded": 32
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 8,
      "reasons": {
        "No official grade in the public snapshot": 8
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 8,
      "reasons": {
        "No official grade in the public snapshot": 8
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 8,
      "reasons": {
        "No official grade in the public snapshot": 8
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 40,
      "reasons": {
        "No per-cell CPU receipt": 32,
        "Not available for ungraded delivery": 8
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 40,
      "reasons": {
        "No per-cell kernel receipt": 32,
        "Not available for ungraded delivery": 8
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 40,
      "reasons": {
        "No per-cell RAM receipt": 32,
        "Not available for ungraded delivery": 8
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 8,
      "reasons": {
        "Not available for ungraded delivery": 8
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 40,
      "reasons": {
        "No per-cell CPU allocation receipt": 32,
        "Not available for ungraded delivery": 8
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 9,
      "reasons": {
        "Invalid/environment cause requires evidence audit": 1,
        "Ungraded delivery needs evidence audit": 8
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 8,
      "reasons": {
        "No captured cohort launch receipt": 8
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 9,
      "reasons": {
        "No audited ITT receipt": 8,
        "No evidence-backed ITT classification": 1
      }
    },
    "model.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 3,
      "reasons": {
        "Not recorded in available public metadata": 3
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 9,
      "reasons": {
        "No official grade in the public snapshot": 8,
        "Official result outside standard outcome classes": 1
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Not recorded in available public metadata": 32
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Dependency source not pinned per cell": 40
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 32
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Original base revision type not recorded per cell": 32
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 8,
      "reasons": {
        "No normalized stop receipt": 8
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Not available for ungraded delivery": 8
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 32
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Original base revision type not recorded per cell": 32
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Attempt boundary receipts unavailable": 40
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Phase wall not emitted or not separable": 32
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Phase wall not emitted or not separable": 32
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 8,
      "reasons": {
        "Not available for ungraded delivery": 8
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Phase wall not emitted or not separable": 32
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Phase wall not emitted or not separable": 32
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Phase wall not emitted or not separable": 32
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Phase wall not emitted or not separable": 32
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Per-phase token counter not emitted": 32
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Per-phase token counter not emitted": 32
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Per-phase token counter not emitted": 32
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Per-phase token counter not emitted": 32
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Per-phase token counter not emitted": 32
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Per-phase token counter not emitted": 32
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Per-phase token counter not emitted": 32
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Per-phase token counter not emitted": 32
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "Not available for ungraded delivery": 8
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "Not available for ungraded delivery": 8
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "Not available for ungraded delivery": 8
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "Not available for ungraded delivery": 8
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Per-phase token counter not emitted": 32
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Per-phase token counter not emitted": 32
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Per-phase token counter not emitted": 32
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Per-phase token counter not emitted": 32
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Per-phase token counter not emitted": 32
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Per-phase token counter not emitted": 32
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Per-phase token counter not emitted": 32
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Per-phase token counter not emitted": 32
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Per-phase token counter not emitted": 32
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Per-phase token counter not emitted": 32
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Per-phase token counter not emitted": 32
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Per-phase token counter not emitted": 32
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Per-phase token counter not emitted": 32
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Per-phase token counter not emitted": 32
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Per-phase token counter not emitted": 32
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Per-phase token counter not emitted": 32
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 32,
        "Usage counter unavailable": 3
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 32,
        "Usage counter unavailable": 3
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 32,
        "Usage counter unavailable": 3
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 32,
        "Usage counter unavailable": 3
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 32,
        "Not available for ungraded delivery": 8
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 32,
        "Not available for ungraded delivery": 8
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 32,
        "Not available for ungraded delivery": 8
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Toolchain version/inventory not recorded": 32
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Toolchain version/inventory not recorded": 32
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Toolchain version/inventory not recorded": 32
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Toolchain version/inventory not recorded": 32
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Toolchain version/inventory not recorded": 32
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Not available for ungraded delivery": 8,
        "Toolchain version/inventory not recorded": 32
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 40
      },
      "circumstances.load1_end": {
        "none": 40
      },
      "cost.accounting": {
        "none": 8
      },
      "cost.calculator_version": {
        "none": 8
      },
      "cost.long_context_reconciled": {
        "none": 8
      },
      "cost.price_table_version": {
        "none": 8
      },
      "cost.usd": {
        "none": 40
      },
      "effort.effective": {
        "none": 3
      },
      "environment.cores": {
        "none": 40
      },
      "environment.cpu_model": {
        "none": 40
      },
      "environment.kernel": {
        "none": 40
      },
      "environment.ram_gib": {
        "none": 40
      },
      "environment.toolchains.elixir": {
        "none": 40
      },
      "environment.toolchains.erlang": {
        "none": 40
      },
      "environment.toolchains.node": {
        "none": 40
      },
      "environment.toolchains.other_inventory": {
        "none": 40
      },
      "environment.toolchains.ruby": {
        "none": 40
      },
      "environment.toolchains.rust": {
        "none": 40
      },
      "grade.grader": {
        "not re-derivable from the public record": 8
      },
      "grade.tests_ran": {
        "not re-derivable from the public record": 8
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 8
      },
      "host.cpu": {
        "none": 40
      },
      "host.kernel": {
        "none": 40
      },
      "host.ram_gib": {
        "none": 40
      },
      "host.spec_ref": {
        "none": 8
      },
      "host.vcpu": {
        "none": 40
      },
      "itt.class": {
        "none": 9
      },
      "itt.cohort": {
        "none": 8
      },
      "itt.evidence_ref": {
        "none": 9
      },
      "model.effective": {
        "none": 3
      },
      "outcome": {
        "none": 1,
        "not re-derivable from the public record": 8
      },
      "recipe": {
        "none": 40
      },
      "setup.deps_source": {
        "none": 40
      },
      "setup.task_base.hash": {
        "none": 40
      },
      "setup.task_base.kind": {
        "none": 40
      },
      "stop_reason": {
        "none": 8
      },
      "task.base_repo": {
        "none": 8
      },
      "task.base_revision.hash": {
        "none": 40
      },
      "task.base_revision.kind": {
        "none": 40
      },
      "timestamps.attempts": {
        "none": 40
      },
      "timestamps.phases.develop.end_utc": {
        "none": 40
      },
      "timestamps.phases.develop.start_utc": {
        "none": 40
      },
      "timestamps.phases.gate.end_utc": {
        "none": 40
      },
      "timestamps.phases.gate.start_utc": {
        "none": 40
      },
      "timestamps.phases.grade.end_utc": {
        "none": 40
      },
      "timestamps.phases.grade.start_utc": {
        "none": 40
      },
      "timestamps.phases.plan.end_utc": {
        "none": 40
      },
      "timestamps.phases.plan.start_utc": {
        "none": 40
      },
      "timestamps.phases.review.end_utc": {
        "none": 40
      },
      "timestamps.phases.review.start_utc": {
        "none": 40
      },
      "timestamps.phases.setup.end_utc": {
        "none": 40
      },
      "timestamps.phases.setup.start_utc": {
        "none": 40
      },
      "timestamps.phases.shape.end_utc": {
        "none": 40
      },
      "timestamps.phases.shape.start_utc": {
        "none": 40
      },
      "timing.phases_s.develop": {
        "none": 40
      },
      "timing.phases_s.gate": {
        "none": 40
      },
      "timing.phases_s.grade": {
        "none": 8
      },
      "timing.phases_s.plan": {
        "none": 40
      },
      "timing.phases_s.review": {
        "none": 40
      },
      "timing.phases_s.setup": {
        "none": 40
      },
      "timing.phases_s.shape": {
        "none": 40
      },
      "tokens.phases.develop.cached_input": {
        "none": 40
      },
      "tokens.phases.develop.input": {
        "none": 40
      },
      "tokens.phases.develop.output": {
        "none": 40
      },
      "tokens.phases.develop.reasoning": {
        "none": 40
      },
      "tokens.phases.gate.cached_input": {
        "none": 40
      },
      "tokens.phases.gate.input": {
        "none": 40
      },
      "tokens.phases.gate.output": {
        "none": 40
      },
      "tokens.phases.gate.reasoning": {
        "none": 40
      },
      "tokens.phases.grade.cached_input": {
        "none": 8
      },
      "tokens.phases.grade.input": {
        "none": 8
      },
      "tokens.phases.grade.output": {
        "none": 8
      },
      "tokens.phases.grade.reasoning": {
        "none": 8
      },
      "tokens.phases.plan.cached_input": {
        "none": 40
      },
      "tokens.phases.plan.input": {
        "none": 40
      },
      "tokens.phases.plan.output": {
        "none": 40
      },
      "tokens.phases.plan.reasoning": {
        "none": 40
      },
      "tokens.phases.review.cached_input": {
        "none": 40
      },
      "tokens.phases.review.input": {
        "none": 40
      },
      "tokens.phases.review.output": {
        "none": 40
      },
      "tokens.phases.review.reasoning": {
        "none": 40
      },
      "tokens.phases.setup.cached_input": {
        "none": 40
      },
      "tokens.phases.setup.input": {
        "none": 40
      },
      "tokens.phases.setup.output": {
        "none": 40
      },
      "tokens.phases.setup.reasoning": {
        "none": 40
      },
      "tokens.phases.shape.cached_input": {
        "none": 40
      },
      "tokens.phases.shape.input": {
        "none": 40
      },
      "tokens.phases.shape.output": {
        "none": 40
      },
      "tokens.phases.shape.reasoning": {
        "none": 40
      },
      "tokens.total.cached_input": {
        "none": 35
      },
      "tokens.total.input": {
        "none": 35
      },
      "tokens.total.output": {
        "none": 35
      },
      "tokens.total.reasoning": {
        "none": 35
      },
      "tools.codex_cli": {
        "none": 40
      },
      "tools.grader": {
        "none": 40
      },
      "tools.runner": {
        "none": 40
      },
      "tools.toolchains.elixir": {
        "none": 40
      },
      "tools.toolchains.erlang": {
        "none": 40
      },
      "tools.toolchains.node": {
        "none": 40
      },
      "tools.toolchains.other_inventory": {
        "none": 40
      },
      "tools.toolchains.ruby": {
        "none": 40
      },
      "tools.toolchains.rust": {
        "none": 40
      }
    },
    "reconstructable": {}
  },
  "round": "r35"
}
```
