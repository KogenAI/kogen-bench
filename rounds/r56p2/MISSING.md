# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 336,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Boundary telemetry not retained": 336
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 256,
      "reasons": {
        "Boundary telemetry not retained": 256
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 256,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 256
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Boundary telemetry not retained": 336
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 256,
      "reasons": {
        "No matching controller samples retained": 256
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 15
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 15
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 15
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 15
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 47,
      "reasons": {
        "Complete per-model billable vector unavailable": 32,
        "Not available for ungraded delivery": 15
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 42,
      "reasons": {
        "Not recorded in available public metadata": 42
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 256,
      "reasons": {
        "No dated account-class receipt": 256
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "No per-cell CPU allocation receipt": 321,
        "Not available for ungraded delivery": 15
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "No per-cell CPU receipt": 321,
        "Not available for ungraded delivery": 15
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "No per-cell kernel receipt": 65,
        "Not available for ungraded delivery": 15
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "No per-cell RAM receipt": 321,
        "Not available for ungraded delivery": 15
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Toolchain version/inventory not recorded": 321
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Toolchain version/inventory not recorded": 321
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Toolchain version/inventory not recorded": 321
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Toolchain version/inventory not recorded": 321
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Toolchain version/inventory not recorded": 321
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Toolchain version/inventory not recorded": 321
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 15,
      "reasons": {
        "No official grade in the public snapshot": 15
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 47,
      "reasons": {
        "Boolean receipt not recorded": 32,
        "No official grade in the public snapshot": 15
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 15,
      "reasons": {
        "No official grade in the public snapshot": 15
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 336,
      "reasons": {
        "No per-cell CPU receipt": 321,
        "Not available for ungraded delivery": 15
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 80,
      "reasons": {
        "No per-cell kernel receipt": 65,
        "Not available for ungraded delivery": 15
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 336,
      "reasons": {
        "No per-cell RAM receipt": 321,
        "Not available for ungraded delivery": 15
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 15
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 336,
      "reasons": {
        "No per-cell CPU allocation receipt": 321,
        "Not available for ungraded delivery": 15
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 47,
      "reasons": {
        "Invalid/environment cause requires evidence audit": 32,
        "Ungraded delivery needs evidence audit": 15
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 15,
      "reasons": {
        "No captured cohort launch receipt": 15
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 47,
      "reasons": {
        "No audited ITT receipt": 15,
        "No evidence-backed ITT classification": 32
      }
    },
    "model.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 42,
      "reasons": {
        "Not recorded in available public metadata": 42
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 15,
      "reasons": {
        "No official grade in the public snapshot": 15
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Not recorded in available public metadata": 321
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Dependency source not pinned per cell": 336
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 240,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 225
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 240,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Original base revision type not recorded per cell": 225
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 47,
      "reasons": {
        "No normalized stop receipt": 15,
        "Runner status does not establish normalized stop cause": 32
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 15
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 240,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 225
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 240,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Original base revision type not recorded per cell": 225
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Attempt boundary receipts unavailable": 336
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Absolute phase boundary not retained": 336
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Absolute phase boundary not retained": 336
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Absolute phase boundary not retained": 336
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Absolute phase boundary not retained": 336
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Absolute phase boundary not retained": 336
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Absolute phase boundary not retained": 336
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Absolute phase boundary not retained": 336
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Absolute phase boundary not retained": 336
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Absolute phase boundary not retained": 336
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Absolute phase boundary not retained": 336
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Absolute phase boundary not retained": 336
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Absolute phase boundary not retained": 336
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Absolute phase boundary not retained": 336
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Absolute phase boundary not retained": 336
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Phase wall not emitted or not separable": 321
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Phase wall not emitted or not separable": 321
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 47,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Phase wall not emitted or not separable": 32
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Phase wall not emitted or not separable": 321
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Phase wall not emitted or not separable": 321
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Phase wall not emitted or not separable": 321
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Phase wall not emitted or not separable": 321
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Per-phase token counter not emitted": 321
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Per-phase token counter not emitted": 321
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Per-phase token counter not emitted": 321
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Per-phase token counter not emitted": 321
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Per-phase token counter not emitted": 321
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Per-phase token counter not emitted": 321
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Per-phase token counter not emitted": 321
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Per-phase token counter not emitted": 321
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 15
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 15
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 15
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 15
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Per-phase token counter not emitted": 321
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Per-phase token counter not emitted": 321
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Per-phase token counter not emitted": 321
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Per-phase token counter not emitted": 321
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Per-phase token counter not emitted": 321
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Per-phase token counter not emitted": 321
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Per-phase token counter not emitted": 321
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Per-phase token counter not emitted": 321
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Per-phase token counter not emitted": 321
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Per-phase token counter not emitted": 321
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Per-phase token counter not emitted": 321
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Per-phase token counter not emitted": 321
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Per-phase token counter not emitted": 321
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Per-phase token counter not emitted": 321
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Per-phase token counter not emitted": 321
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Per-phase token counter not emitted": 321
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 42,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 32,
        "Usage counter unavailable": 10
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 42,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 32,
        "Usage counter unavailable": 10
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 42,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 32,
        "Usage counter unavailable": 10
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 42,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 32,
        "Usage counter unavailable": 10
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 321,
        "Not available for ungraded delivery": 15
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 321,
        "Not available for ungraded delivery": 15
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 321,
        "Not available for ungraded delivery": 15
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Toolchain version/inventory not recorded": 321
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Toolchain version/inventory not recorded": 321
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Toolchain version/inventory not recorded": 321
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Toolchain version/inventory not recorded": 321
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Toolchain version/inventory not recorded": 321
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 336,
      "reasons": {
        "Not available for ungraded delivery": 15,
        "Toolchain version/inventory not recorded": 321
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 336
      },
      "circumstances.concurrent_cells_end": {
        "none": 256
      },
      "circumstances.concurrent_cells_start": {
        "none": 256
      },
      "circumstances.load1_end": {
        "none": 336
      },
      "circumstances.load_samples": {
        "none": 256
      },
      "cost.accounting": {
        "none": 15
      },
      "cost.calculator_version": {
        "none": 15
      },
      "cost.long_context_reconciled": {
        "none": 15
      },
      "cost.price_table_version": {
        "none": 15
      },
      "cost.usd": {
        "none": 47
      },
      "effort.effective": {
        "none": 42
      },
      "environment.account_class": {
        "none": 256
      },
      "environment.cores": {
        "none": 336
      },
      "environment.cpu_model": {
        "none": 336
      },
      "environment.kernel": {
        "none": 80
      },
      "environment.ram_gib": {
        "none": 336
      },
      "environment.toolchains.elixir": {
        "none": 336
      },
      "environment.toolchains.erlang": {
        "none": 336
      },
      "environment.toolchains.node": {
        "none": 336
      },
      "environment.toolchains.other_inventory": {
        "none": 336
      },
      "environment.toolchains.ruby": {
        "none": 336
      },
      "environment.toolchains.rust": {
        "none": 336
      },
      "grade.grader": {
        "not re-derivable from the public record": 15
      },
      "grade.tests_ran": {
        "none": 32,
        "not re-derivable from the public record": 15
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 15
      },
      "host.cpu": {
        "none": 336
      },
      "host.kernel": {
        "none": 80
      },
      "host.ram_gib": {
        "none": 336
      },
      "host.spec_ref": {
        "none": 15
      },
      "host.vcpu": {
        "none": 336
      },
      "itt.class": {
        "none": 47
      },
      "itt.cohort": {
        "none": 15
      },
      "itt.evidence_ref": {
        "none": 47
      },
      "model.effective": {
        "none": 42
      },
      "outcome": {
        "not re-derivable from the public record": 15
      },
      "recipe": {
        "none": 336
      },
      "setup.deps_source": {
        "none": 336
      },
      "setup.task_base.hash": {
        "none": 240
      },
      "setup.task_base.kind": {
        "none": 240
      },
      "stop_reason": {
        "none": 47
      },
      "task.base_repo": {
        "none": 15
      },
      "task.base_revision.hash": {
        "none": 240
      },
      "task.base_revision.kind": {
        "none": 240
      },
      "timestamps.attempts": {
        "none": 336
      },
      "timestamps.phases.develop.end_utc": {
        "none": 336
      },
      "timestamps.phases.develop.start_utc": {
        "none": 336
      },
      "timestamps.phases.gate.end_utc": {
        "none": 336
      },
      "timestamps.phases.gate.start_utc": {
        "none": 336
      },
      "timestamps.phases.grade.end_utc": {
        "none": 336
      },
      "timestamps.phases.grade.start_utc": {
        "none": 336
      },
      "timestamps.phases.plan.end_utc": {
        "none": 336
      },
      "timestamps.phases.plan.start_utc": {
        "none": 336
      },
      "timestamps.phases.review.end_utc": {
        "none": 336
      },
      "timestamps.phases.review.start_utc": {
        "none": 336
      },
      "timestamps.phases.setup.end_utc": {
        "none": 336
      },
      "timestamps.phases.setup.start_utc": {
        "none": 336
      },
      "timestamps.phases.shape.end_utc": {
        "none": 336
      },
      "timestamps.phases.shape.start_utc": {
        "none": 336
      },
      "timing.phases_s.develop": {
        "none": 336
      },
      "timing.phases_s.gate": {
        "none": 336
      },
      "timing.phases_s.grade": {
        "none": 47
      },
      "timing.phases_s.plan": {
        "none": 336
      },
      "timing.phases_s.review": {
        "none": 336
      },
      "timing.phases_s.setup": {
        "none": 336
      },
      "timing.phases_s.shape": {
        "none": 336
      },
      "tokens.phases.develop.cached_input": {
        "none": 336
      },
      "tokens.phases.develop.input": {
        "none": 336
      },
      "tokens.phases.develop.output": {
        "none": 336
      },
      "tokens.phases.develop.reasoning": {
        "none": 336
      },
      "tokens.phases.gate.cached_input": {
        "none": 336
      },
      "tokens.phases.gate.input": {
        "none": 336
      },
      "tokens.phases.gate.output": {
        "none": 336
      },
      "tokens.phases.gate.reasoning": {
        "none": 336
      },
      "tokens.phases.grade.cached_input": {
        "none": 15
      },
      "tokens.phases.grade.input": {
        "none": 15
      },
      "tokens.phases.grade.output": {
        "none": 15
      },
      "tokens.phases.grade.reasoning": {
        "none": 15
      },
      "tokens.phases.plan.cached_input": {
        "none": 336
      },
      "tokens.phases.plan.input": {
        "none": 336
      },
      "tokens.phases.plan.output": {
        "none": 336
      },
      "tokens.phases.plan.reasoning": {
        "none": 336
      },
      "tokens.phases.review.cached_input": {
        "none": 336
      },
      "tokens.phases.review.input": {
        "none": 336
      },
      "tokens.phases.review.output": {
        "none": 336
      },
      "tokens.phases.review.reasoning": {
        "none": 336
      },
      "tokens.phases.setup.cached_input": {
        "none": 336
      },
      "tokens.phases.setup.input": {
        "none": 336
      },
      "tokens.phases.setup.output": {
        "none": 336
      },
      "tokens.phases.setup.reasoning": {
        "none": 336
      },
      "tokens.phases.shape.cached_input": {
        "none": 336
      },
      "tokens.phases.shape.input": {
        "none": 336
      },
      "tokens.phases.shape.output": {
        "none": 336
      },
      "tokens.phases.shape.reasoning": {
        "none": 336
      },
      "tokens.total.cached_input": {
        "none": 42
      },
      "tokens.total.input": {
        "none": 42
      },
      "tokens.total.output": {
        "none": 42
      },
      "tokens.total.reasoning": {
        "none": 42
      },
      "tools.codex_cli": {
        "none": 336
      },
      "tools.grader": {
        "none": 336
      },
      "tools.runner": {
        "none": 336
      },
      "tools.toolchains.elixir": {
        "none": 336
      },
      "tools.toolchains.erlang": {
        "none": 336
      },
      "tools.toolchains.node": {
        "none": 336
      },
      "tools.toolchains.other_inventory": {
        "none": 336
      },
      "tools.toolchains.ruby": {
        "none": 336
      },
      "tools.toolchains.rust": {
        "none": 336
      }
    },
    "reconstructable": {}
  },
  "publication_reconciliation": {
    "disposition": "This is a separate later capture. Keep it apart from the r56/r56b/r56c/r56d cohorts; the historical pooled decision table is not reproduced by this page.",
    "original_execution_command": "not recorded in the public snapshot",
    "harness_source_commit": "absent; tools.harness values are wrapper fingerprints",
    "kogen_source_commit": "Public records mark the Kogen product commit not applicable for these harness records.",
    "raw_public_records": [
      "results/run-records/r56p2.jsonl",
      "results/cells.jsonl"
    ],
    "public_record_rebuild": "python3 reproduce/export_results.py; python3 reproduce/build_records.py; python3 reproduce/validate_round.py --round r56p2"
  },
  "round": "r56p2"
}
```
