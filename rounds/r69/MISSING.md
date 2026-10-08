# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 459,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Boundary telemetry not retained": 459
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Boundary telemetry not retained": 12,
        "Dispatcher termination may leave stale state; finalization counts are not live concurrency": 13
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Boundary telemetry not retained": 459
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 192,
      "reasons": {
        "No matching controller samples retained": 192
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 309,
      "reasons": {
        "Not available for ungraded delivery": 309
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 309,
      "reasons": {
        "Not available for ungraded delivery": 309
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 309,
      "reasons": {
        "Not available for ungraded delivery": 309
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 309,
      "reasons": {
        "Not available for ungraded delivery": 309
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 459,
      "reasons": {
        "Complete per-model billable vector unavailable": 150,
        "Not available for ungraded delivery": 309
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 262,
      "reasons": {
        "Not recorded in available public metadata": 262
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "No per-cell CPU allocation receipt": 150,
        "Not available for ungraded delivery": 309
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "No per-cell CPU receipt": 150,
        "Not available for ungraded delivery": 309
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "No per-cell kernel receipt": 150,
        "Not available for ungraded delivery": 309
      }
    },
    "environment.network.allowlist_hosts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 13,
      "reasons": {
        "Allowlist unavailable": 13
      }
    },
    "environment.network.profile": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 13,
      "reasons": {
        "Not recorded in available public metadata": 13
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "No per-cell RAM receipt": 150,
        "Not available for ungraded delivery": 309
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Toolchain version/inventory not recorded": 150
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Toolchain version/inventory not recorded": 150
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Toolchain version/inventory not recorded": 150
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Toolchain version/inventory not recorded": 150
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Toolchain version/inventory not recorded": 150
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Toolchain version/inventory not recorded": 150
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 309,
      "reasons": {
        "No official grade in the public snapshot": 309
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 309,
      "reasons": {
        "No official grade in the public snapshot": 309
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 309,
      "reasons": {
        "No official grade in the public snapshot": 309
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 459,
      "reasons": {
        "No per-cell CPU receipt": 150,
        "Not available for ungraded delivery": 309
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 459,
      "reasons": {
        "No per-cell kernel receipt": 150,
        "Not available for ungraded delivery": 309
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 459,
      "reasons": {
        "No per-cell RAM receipt": 150,
        "Not available for ungraded delivery": 309
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 309,
      "reasons": {
        "Not available for ungraded delivery": 309
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 459,
      "reasons": {
        "No per-cell CPU allocation receipt": 150,
        "Not available for ungraded delivery": 309
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 309,
      "reasons": {
        "Ungraded delivery needs evidence audit": 309
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 309,
      "reasons": {
        "No captured cohort launch receipt": 309
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 309,
      "reasons": {
        "No audited ITT receipt": 309
      }
    },
    "model.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 262,
      "reasons": {
        "Not recorded in available public metadata": 262
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 309,
      "reasons": {
        "No official grade in the public snapshot": 309
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Not recorded in available public metadata": 150
      }
    },
    "sandbox.egress_allow": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 13,
      "reasons": {
        "Allowlist unavailable": 13
      }
    },
    "sandbox.egress_profile": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 13,
      "reasons": {
        "Not recorded in available public metadata": 13
      }
    },
    "sandbox.profile": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 13,
      "reasons": {
        "Not recorded in available public metadata": 13
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Dependency source not pinned per cell": 459
      }
    },
    "setup.sandbox_mode": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 13,
      "reasons": {
        "Not recorded in available public metadata": 13
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 307,
      "reasons": {
        "Not available for ungraded delivery": 211,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 96
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 307,
      "reasons": {
        "Not available for ungraded delivery": 211,
        "Original base revision type not recorded per cell": 96
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 292,
      "reasons": {
        "No normalized stop receipt": 292
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 309,
      "reasons": {
        "Not available for ungraded delivery": 309
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 307,
      "reasons": {
        "Not available for ungraded delivery": 211,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 96
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 307,
      "reasons": {
        "Not available for ungraded delivery": 211,
        "Original base revision type not recorded per cell": 96
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Attempt boundary receipts unavailable": 459
      }
    },
    "timestamps.cell.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "End boundary absent; delivery may be active or receipt lost": 12
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Absolute phase boundary not retained": 459
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Absolute phase boundary not retained": 459
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Absolute phase boundary not retained": 459
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Absolute phase boundary not retained": 459
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Absolute phase boundary not retained": 459
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Absolute phase boundary not retained": 459
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Absolute phase boundary not retained": 459
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Absolute phase boundary not retained": 459
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Absolute phase boundary not retained": 459
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Absolute phase boundary not retained": 459
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Absolute phase boundary not retained": 459
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Absolute phase boundary not retained": 459
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Absolute phase boundary not retained": 459
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Absolute phase boundary not retained": 459
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Phase wall not emitted or not separable": 150
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Phase wall not emitted or not separable": 150
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 309,
      "reasons": {
        "Not available for ungraded delivery": 309
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Phase wall not emitted or not separable": 150
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Phase wall not emitted or not separable": 150
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Phase wall not emitted or not separable": 150
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Phase wall not emitted or not separable": 150
      }
    },
    "timing.total_wall_s": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 13,
      "reasons": {
        "Wall counter unavailable": 13
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Per-phase token counter not emitted": 150
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Per-phase token counter not emitted": 150
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Per-phase token counter not emitted": 150
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Per-phase token counter not emitted": 150
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Per-phase token counter not emitted": 150
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Per-phase token counter not emitted": 150
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Per-phase token counter not emitted": 150
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Per-phase token counter not emitted": 150
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 309,
      "reasons": {
        "Not available for ungraded delivery": 309
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 309,
      "reasons": {
        "Not available for ungraded delivery": 309
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 309,
      "reasons": {
        "Not available for ungraded delivery": 309
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 309,
      "reasons": {
        "Not available for ungraded delivery": 309
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Per-phase token counter not emitted": 150
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Per-phase token counter not emitted": 150
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Per-phase token counter not emitted": 150
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Per-phase token counter not emitted": 150
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Per-phase token counter not emitted": 150
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Per-phase token counter not emitted": 150
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Per-phase token counter not emitted": 150
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Per-phase token counter not emitted": 150
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Per-phase token counter not emitted": 150
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Per-phase token counter not emitted": 150
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Per-phase token counter not emitted": 150
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Per-phase token counter not emitted": 150
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Per-phase token counter not emitted": 150
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Per-phase token counter not emitted": 150
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Per-phase token counter not emitted": 150
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Per-phase token counter not emitted": 150
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 412,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 150,
        "Usage counter unavailable": 262
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 412,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 150,
        "Usage counter unavailable": 262
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 412,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 150,
        "Usage counter unavailable": 262
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 412,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 150,
        "Usage counter unavailable": 262
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 150,
        "Not available for ungraded delivery": 309
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 150,
        "Not available for ungraded delivery": 309
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 150,
        "Not available for ungraded delivery": 309
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Toolchain version/inventory not recorded": 150
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Toolchain version/inventory not recorded": 150
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Toolchain version/inventory not recorded": 150
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Toolchain version/inventory not recorded": 150
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Toolchain version/inventory not recorded": 150
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 459,
      "reasons": {
        "Not available for ungraded delivery": 309,
        "Toolchain version/inventory not recorded": 150
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 459
      },
      "circumstances.concurrent_cells_end": {
        "none": 25
      },
      "circumstances.load1_end": {
        "none": 459
      },
      "circumstances.load_samples": {
        "none": 192
      },
      "cost.accounting": {
        "none": 309
      },
      "cost.calculator_version": {
        "none": 309
      },
      "cost.long_context_reconciled": {
        "none": 309
      },
      "cost.price_table_version": {
        "none": 309
      },
      "cost.usd": {
        "none": 459
      },
      "effort.effective": {
        "none": 262
      },
      "environment.cores": {
        "none": 459
      },
      "environment.cpu_model": {
        "none": 459
      },
      "environment.kernel": {
        "none": 459
      },
      "environment.network.allowlist_hosts": {
        "none": 13
      },
      "environment.network.profile": {
        "none": 13
      },
      "environment.ram_gib": {
        "none": 459
      },
      "environment.toolchains.elixir": {
        "none": 459
      },
      "environment.toolchains.erlang": {
        "none": 459
      },
      "environment.toolchains.node": {
        "none": 459
      },
      "environment.toolchains.other_inventory": {
        "none": 459
      },
      "environment.toolchains.ruby": {
        "none": 459
      },
      "environment.toolchains.rust": {
        "none": 459
      },
      "grade.grader": {
        "not re-derivable from the public record": 309
      },
      "grade.tests_ran": {
        "not re-derivable from the public record": 309
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 309
      },
      "host.cpu": {
        "none": 459
      },
      "host.kernel": {
        "none": 459
      },
      "host.ram_gib": {
        "none": 459
      },
      "host.spec_ref": {
        "none": 309
      },
      "host.vcpu": {
        "none": 459
      },
      "itt.class": {
        "none": 309
      },
      "itt.cohort": {
        "none": 309
      },
      "itt.evidence_ref": {
        "none": 309
      },
      "model.effective": {
        "none": 262
      },
      "outcome": {
        "not re-derivable from the public record": 309
      },
      "recipe": {
        "none": 459
      },
      "sandbox.egress_allow": {
        "none": 13
      },
      "sandbox.egress_profile": {
        "none": 13
      },
      "sandbox.profile": {
        "none": 13
      },
      "setup.deps_source": {
        "none": 459
      },
      "setup.sandbox_mode": {
        "none": 13
      },
      "setup.task_base.hash": {
        "none": 307
      },
      "setup.task_base.kind": {
        "none": 307
      },
      "stop_reason": {
        "none": 292
      },
      "task.base_repo": {
        "none": 309
      },
      "task.base_revision.hash": {
        "none": 307
      },
      "task.base_revision.kind": {
        "none": 307
      },
      "timestamps.attempts": {
        "none": 459
      },
      "timestamps.phases.develop.end_utc": {
        "none": 459
      },
      "timestamps.phases.develop.start_utc": {
        "none": 459
      },
      "timestamps.phases.gate.end_utc": {
        "none": 459
      },
      "timestamps.phases.gate.start_utc": {
        "none": 459
      },
      "timestamps.phases.grade.end_utc": {
        "none": 459
      },
      "timestamps.phases.grade.start_utc": {
        "none": 459
      },
      "timestamps.phases.plan.end_utc": {
        "none": 459
      },
      "timestamps.phases.plan.start_utc": {
        "none": 459
      },
      "timestamps.phases.review.end_utc": {
        "none": 459
      },
      "timestamps.phases.review.start_utc": {
        "none": 459
      },
      "timestamps.phases.setup.end_utc": {
        "none": 459
      },
      "timestamps.phases.setup.start_utc": {
        "none": 459
      },
      "timestamps.phases.shape.end_utc": {
        "none": 459
      },
      "timestamps.phases.shape.start_utc": {
        "none": 459
      },
      "timing.phases_s.develop": {
        "none": 459
      },
      "timing.phases_s.gate": {
        "none": 459
      },
      "timing.phases_s.grade": {
        "none": 309
      },
      "timing.phases_s.plan": {
        "none": 459
      },
      "timing.phases_s.review": {
        "none": 459
      },
      "timing.phases_s.setup": {
        "none": 459
      },
      "timing.phases_s.shape": {
        "none": 459
      },
      "timing.total_wall_s": {
        "none": 13
      },
      "tokens.phases.develop.cached_input": {
        "none": 459
      },
      "tokens.phases.develop.input": {
        "none": 459
      },
      "tokens.phases.develop.output": {
        "none": 459
      },
      "tokens.phases.develop.reasoning": {
        "none": 459
      },
      "tokens.phases.gate.cached_input": {
        "none": 459
      },
      "tokens.phases.gate.input": {
        "none": 459
      },
      "tokens.phases.gate.output": {
        "none": 459
      },
      "tokens.phases.gate.reasoning": {
        "none": 459
      },
      "tokens.phases.grade.cached_input": {
        "none": 309
      },
      "tokens.phases.grade.input": {
        "none": 309
      },
      "tokens.phases.grade.output": {
        "none": 309
      },
      "tokens.phases.grade.reasoning": {
        "none": 309
      },
      "tokens.phases.plan.cached_input": {
        "none": 459
      },
      "tokens.phases.plan.input": {
        "none": 459
      },
      "tokens.phases.plan.output": {
        "none": 459
      },
      "tokens.phases.plan.reasoning": {
        "none": 459
      },
      "tokens.phases.review.cached_input": {
        "none": 459
      },
      "tokens.phases.review.input": {
        "none": 459
      },
      "tokens.phases.review.output": {
        "none": 459
      },
      "tokens.phases.review.reasoning": {
        "none": 459
      },
      "tokens.phases.setup.cached_input": {
        "none": 459
      },
      "tokens.phases.setup.input": {
        "none": 459
      },
      "tokens.phases.setup.output": {
        "none": 459
      },
      "tokens.phases.setup.reasoning": {
        "none": 459
      },
      "tokens.phases.shape.cached_input": {
        "none": 459
      },
      "tokens.phases.shape.input": {
        "none": 459
      },
      "tokens.phases.shape.output": {
        "none": 459
      },
      "tokens.phases.shape.reasoning": {
        "none": 459
      },
      "tokens.total.cached_input": {
        "none": 412
      },
      "tokens.total.input": {
        "none": 412
      },
      "tokens.total.output": {
        "none": 412
      },
      "tokens.total.reasoning": {
        "none": 412
      },
      "tools.codex_cli": {
        "none": 459
      },
      "tools.grader": {
        "none": 459
      },
      "tools.runner": {
        "none": 459
      },
      "tools.toolchains.elixir": {
        "none": 459
      },
      "tools.toolchains.erlang": {
        "none": 459
      },
      "tools.toolchains.node": {
        "none": 459
      },
      "tools.toolchains.other_inventory": {
        "none": 459
      },
      "tools.toolchains.ruby": {
        "none": 459
      },
      "tools.toolchains.rust": {
        "none": 459
      }
    },
    "reconstructable": {
      "timestamps.cell.end_utc": {
        "Completion manifest or dispatcher END": 12
      }
    }
  },
  "publication_reconciliation": {
    "disposition": "The public delivery ledger and official outcome export have materially different coverage. The historical adjudicated four-arm intention-to-treat results and replacement analysis are source-reported, not reproducible from the public data; keep INTERIM and do not restore the headline table.",
    "original_execution_command": "not recorded in the public snapshot",
    "harness_source_commit": "absent; tools.harness values are wrapper fingerprints",
    "kogen_source_commit": "Public records mark the Kogen product commit not applicable for these harness records.",
    "raw_public_records": [
      "results/run-records/r69.jsonl",
      "results/cells.jsonl"
    ],
    "public_record_rebuild": "python3 reproduce/export_results.py; python3 reproduce/build_records.py; python3 reproduce/validate_round.py --round r69"
  },
  "round": "r69"
}
```
