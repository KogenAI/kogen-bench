# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 34,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Boundary telemetry not retained": 34
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Boundary telemetry not retained": 34
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
      "count": 34,
      "reasons": {
        "Complete per-model billable vector unavailable": 27,
        "Not available for ungraded delivery": 7
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Account transition approximate; corrected ops entry cannot pin this cell": 34
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "No per-cell CPU allocation receipt": 27,
        "Not available for ungraded delivery": 7
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "No per-cell CPU receipt": 27,
        "Not available for ungraded delivery": 7
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "No per-cell kernel receipt": 27,
        "Not available for ungraded delivery": 7
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "No per-cell RAM receipt": 27,
        "Not available for ungraded delivery": 7
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 27
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 27
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 27
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 27
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 27
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 27
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
      "count": 34,
      "reasons": {
        "No per-cell CPU receipt": 27,
        "Not available for ungraded delivery": 7
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 34,
      "reasons": {
        "No per-cell kernel receipt": 27,
        "Not available for ungraded delivery": 7
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 34,
      "reasons": {
        "No per-cell RAM receipt": 27,
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
      "count": 34,
      "reasons": {
        "No per-cell CPU allocation receipt": 27,
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
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 8,
      "reasons": {
        "No official grade in the public snapshot": 7,
        "Official result outside standard outcome classes": 1
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Not recorded in available public metadata": 27
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Dependency source not pinned per cell": 34
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 27
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Original base revision type not recorded per cell": 27
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
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 27
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Original base revision type not recorded per cell": 27
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Attempt boundary receipts unavailable": 34
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Absolute phase boundary not retained": 34
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Absolute phase boundary not retained": 34
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Absolute phase boundary not retained": 34
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Absolute phase boundary not retained": 34
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Absolute phase boundary not retained": 34
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Absolute phase boundary not retained": 34
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Absolute phase boundary not retained": 34
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Absolute phase boundary not retained": 34
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Absolute phase boundary not retained": 34
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Absolute phase boundary not retained": 34
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Absolute phase boundary not retained": 34
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Absolute phase boundary not retained": 34
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Absolute phase boundary not retained": 34
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Absolute phase boundary not retained": 34
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Phase wall not emitted or not separable": 27
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Phase wall not emitted or not separable": 27
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
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Phase wall not emitted or not separable": 27
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Phase wall not emitted or not separable": 27
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Phase wall not emitted or not separable": 27
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Phase wall not emitted or not separable": 27
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 27
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 27
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 27
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 27
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 27
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 27
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 27
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 27
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
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 27
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 27
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 27
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 27
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 27
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 27
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 27
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 27
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 27
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 27
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 27
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 27
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 27
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 27
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 27
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 27
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 27,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 27
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 27,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 27
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 27,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 27
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 27,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 27
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 27,
        "Not available for ungraded delivery": 7
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 27,
        "Not available for ungraded delivery": 7
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 27,
        "Not available for ungraded delivery": 7
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 27
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 27
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 27
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 27
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 27
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 27
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 34
      },
      "circumstances.load1_end": {
        "none": 34
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
        "none": 34
      },
      "environment.account_class": {
        "not re-derivable from the public record": 34
      },
      "environment.cores": {
        "none": 34
      },
      "environment.cpu_model": {
        "none": 34
      },
      "environment.kernel": {
        "none": 34
      },
      "environment.ram_gib": {
        "none": 34
      },
      "environment.toolchains.elixir": {
        "none": 34
      },
      "environment.toolchains.erlang": {
        "none": 34
      },
      "environment.toolchains.node": {
        "none": 34
      },
      "environment.toolchains.other_inventory": {
        "none": 34
      },
      "environment.toolchains.ruby": {
        "none": 34
      },
      "environment.toolchains.rust": {
        "none": 34
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
        "none": 34
      },
      "host.kernel": {
        "none": 34
      },
      "host.ram_gib": {
        "none": 34
      },
      "host.spec_ref": {
        "none": 7
      },
      "host.vcpu": {
        "none": 34
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
      "outcome": {
        "none": 1,
        "not re-derivable from the public record": 7
      },
      "recipe": {
        "none": 34
      },
      "setup.deps_source": {
        "none": 34
      },
      "setup.task_base.hash": {
        "none": 34
      },
      "setup.task_base.kind": {
        "none": 34
      },
      "stop_reason": {
        "none": 7
      },
      "task.base_repo": {
        "none": 7
      },
      "task.base_revision.hash": {
        "none": 34
      },
      "task.base_revision.kind": {
        "none": 34
      },
      "timestamps.attempts": {
        "none": 34
      },
      "timestamps.phases.develop.end_utc": {
        "none": 34
      },
      "timestamps.phases.develop.start_utc": {
        "none": 34
      },
      "timestamps.phases.gate.end_utc": {
        "none": 34
      },
      "timestamps.phases.gate.start_utc": {
        "none": 34
      },
      "timestamps.phases.grade.end_utc": {
        "none": 34
      },
      "timestamps.phases.grade.start_utc": {
        "none": 34
      },
      "timestamps.phases.plan.end_utc": {
        "none": 34
      },
      "timestamps.phases.plan.start_utc": {
        "none": 34
      },
      "timestamps.phases.review.end_utc": {
        "none": 34
      },
      "timestamps.phases.review.start_utc": {
        "none": 34
      },
      "timestamps.phases.setup.end_utc": {
        "none": 34
      },
      "timestamps.phases.setup.start_utc": {
        "none": 34
      },
      "timestamps.phases.shape.end_utc": {
        "none": 34
      },
      "timestamps.phases.shape.start_utc": {
        "none": 34
      },
      "timing.phases_s.develop": {
        "none": 34
      },
      "timing.phases_s.gate": {
        "none": 34
      },
      "timing.phases_s.grade": {
        "none": 7
      },
      "timing.phases_s.plan": {
        "none": 34
      },
      "timing.phases_s.review": {
        "none": 34
      },
      "timing.phases_s.setup": {
        "none": 34
      },
      "timing.phases_s.shape": {
        "none": 34
      },
      "tokens.phases.develop.cached_input": {
        "none": 34
      },
      "tokens.phases.develop.input": {
        "none": 34
      },
      "tokens.phases.develop.output": {
        "none": 34
      },
      "tokens.phases.develop.reasoning": {
        "none": 34
      },
      "tokens.phases.gate.cached_input": {
        "none": 34
      },
      "tokens.phases.gate.input": {
        "none": 34
      },
      "tokens.phases.gate.output": {
        "none": 34
      },
      "tokens.phases.gate.reasoning": {
        "none": 34
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
        "none": 34
      },
      "tokens.phases.plan.input": {
        "none": 34
      },
      "tokens.phases.plan.output": {
        "none": 34
      },
      "tokens.phases.plan.reasoning": {
        "none": 34
      },
      "tokens.phases.review.cached_input": {
        "none": 34
      },
      "tokens.phases.review.input": {
        "none": 34
      },
      "tokens.phases.review.output": {
        "none": 34
      },
      "tokens.phases.review.reasoning": {
        "none": 34
      },
      "tokens.phases.setup.cached_input": {
        "none": 34
      },
      "tokens.phases.setup.input": {
        "none": 34
      },
      "tokens.phases.setup.output": {
        "none": 34
      },
      "tokens.phases.setup.reasoning": {
        "none": 34
      },
      "tokens.phases.shape.cached_input": {
        "none": 34
      },
      "tokens.phases.shape.input": {
        "none": 34
      },
      "tokens.phases.shape.output": {
        "none": 34
      },
      "tokens.phases.shape.reasoning": {
        "none": 34
      },
      "tokens.total.cached_input": {
        "none": 27
      },
      "tokens.total.input": {
        "none": 27
      },
      "tokens.total.output": {
        "none": 27
      },
      "tokens.total.reasoning": {
        "none": 27
      },
      "tools.codex_cli": {
        "none": 34
      },
      "tools.grader": {
        "none": 34
      },
      "tools.runner": {
        "none": 34
      },
      "tools.toolchains.elixir": {
        "none": 34
      },
      "tools.toolchains.erlang": {
        "none": 34
      },
      "tools.toolchains.node": {
        "none": 34
      },
      "tools.toolchains.other_inventory": {
        "none": 34
      },
      "tools.toolchains.ruby": {
        "none": 34
      },
      "tools.toolchains.rust": {
        "none": 34
      }
    },
    "reconstructable": {}
  },
  "publication_reconciliation": {
    "disposition": "Keep this capture separate from r64/r64b/r64c/r64d. Public delivery summaries do not reproduce the historical complete Rails cohort or cost analysis.",
    "original_execution_command": "not recorded in the public snapshot",
    "harness_source_commit": "absent; tools.harness values are wrapper fingerprints",
    "kogen_source_commit": "Public records mark the Kogen product commit not applicable for these harness records.",
    "raw_public_records": [
      "results/run-records/r64e.jsonl",
      "results/cells.jsonl"
    ],
    "public_record_rebuild": "python3 reproduce/export_results.py; python3 reproduce/build_records.py; python3 reproduce/validate_round.py --round r64e"
  },
  "round": "r64e"
}
```
