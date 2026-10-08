# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 222,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Boundary telemetry not retained": 222
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 120,
      "reasons": {
        "Boundary telemetry not retained": 120
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 120,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 120
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Boundary telemetry not retained": 222
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 132,
      "reasons": {
        "No matching controller samples retained": 132
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
      "count": 51,
      "reasons": {
        "Complete per-model billable vector unavailable": 29,
        "Not available for ungraded delivery": 22
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 43,
      "reasons": {
        "Not recorded in available public metadata": 43
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 120,
      "reasons": {
        "No dated account-class receipt": 120
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "No per-cell CPU allocation receipt": 200,
        "Not available for ungraded delivery": 22
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "No per-cell CPU receipt": 200,
        "Not available for ungraded delivery": 22
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "No per-cell kernel receipt": 80,
        "Not available for ungraded delivery": 22
      }
    },
    "environment.network.allowlist_hosts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Allowlist unavailable": 1
      }
    },
    "environment.network.profile": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not recorded in available public metadata": 1
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "No per-cell RAM receipt": 200,
        "Not available for ungraded delivery": 22
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Toolchain version/inventory not recorded": 200
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Toolchain version/inventory not recorded": 200
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Toolchain version/inventory not recorded": 200
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Toolchain version/inventory not recorded": 200
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Toolchain version/inventory not recorded": 200
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Toolchain version/inventory not recorded": 200
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
      "count": 46,
      "reasons": {
        "Boolean receipt not recorded": 24,
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
      "count": 222,
      "reasons": {
        "No per-cell CPU receipt": 200,
        "Not available for ungraded delivery": 22
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 102,
      "reasons": {
        "No per-cell kernel receipt": 80,
        "Not available for ungraded delivery": 22
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 222,
      "reasons": {
        "No per-cell RAM receipt": 200,
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
      "count": 222,
      "reasons": {
        "No per-cell CPU allocation receipt": 200,
        "Not available for ungraded delivery": 22
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 46,
      "reasons": {
        "Invalid/environment cause requires evidence audit": 24,
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
      "count": 46,
      "reasons": {
        "No audited ITT receipt": 22,
        "No evidence-backed ITT classification": 24
      }
    },
    "model.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 43,
      "reasons": {
        "Not recorded in available public metadata": 43
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 22,
      "reasons": {
        "No official grade in the public snapshot": 22
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Not recorded in available public metadata": 200
      }
    },
    "sandbox.egress_allow": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Allowlist unavailable": 1
      }
    },
    "sandbox.egress_profile": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not recorded in available public metadata": 1
      }
    },
    "sandbox.profile": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not recorded in available public metadata": 1
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Dependency source not pinned per cell": 222
      }
    },
    "setup.sandbox_mode": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not recorded in available public metadata": 1
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 80
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Original base revision type not recorded per cell": 80
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 46,
      "reasons": {
        "No normalized stop receipt": 22,
        "Runner status does not establish normalized stop cause": 24
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
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 80
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 102,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Original base revision type not recorded per cell": 80
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Attempt boundary receipts unavailable": 222
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Absolute phase boundary not retained": 222
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Absolute phase boundary not retained": 222
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Absolute phase boundary not retained": 222
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Absolute phase boundary not retained": 222
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Absolute phase boundary not retained": 222
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Absolute phase boundary not retained": 222
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Absolute phase boundary not retained": 222
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Absolute phase boundary not retained": 222
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Absolute phase boundary not retained": 222
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Absolute phase boundary not retained": 222
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Absolute phase boundary not retained": 222
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Absolute phase boundary not retained": 222
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Absolute phase boundary not retained": 222
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Absolute phase boundary not retained": 222
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Phase wall not emitted or not separable": 200
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Phase wall not emitted or not separable": 200
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 46,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Phase wall not emitted or not separable": 24
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Phase wall not emitted or not separable": 200
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Phase wall not emitted or not separable": 200
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Phase wall not emitted or not separable": 200
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Phase wall not emitted or not separable": 200
      }
    },
    "timing.total_wall_s": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 1,
      "reasons": {
        "Wall counter unavailable": 1
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 200
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 200
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 200
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 200
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 200
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 200
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 200
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 200
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
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 200
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 200
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 200
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 200
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 200
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 200
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 200
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 200
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 200
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 200
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 200
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 200
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 200
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 200
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 200
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Per-phase token counter not emitted": 200
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 29,
        "Usage counter unavailable": 19
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 29,
        "Usage counter unavailable": 19
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 29,
        "Usage counter unavailable": 19
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 29,
        "Usage counter unavailable": 19
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 200,
        "Not available for ungraded delivery": 22
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 200,
        "Not available for ungraded delivery": 22
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 200,
        "Not available for ungraded delivery": 22
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Toolchain version/inventory not recorded": 200
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Toolchain version/inventory not recorded": 200
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Toolchain version/inventory not recorded": 200
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Toolchain version/inventory not recorded": 200
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Toolchain version/inventory not recorded": 200
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 222,
      "reasons": {
        "Not available for ungraded delivery": 22,
        "Toolchain version/inventory not recorded": 200
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 222
      },
      "circumstances.concurrent_cells_end": {
        "none": 120
      },
      "circumstances.concurrent_cells_start": {
        "none": 120
      },
      "circumstances.load1_end": {
        "none": 222
      },
      "circumstances.load_samples": {
        "none": 132
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
        "none": 51
      },
      "effort.effective": {
        "none": 43
      },
      "environment.account_class": {
        "none": 120
      },
      "environment.cores": {
        "none": 222
      },
      "environment.cpu_model": {
        "none": 222
      },
      "environment.kernel": {
        "none": 102
      },
      "environment.network.allowlist_hosts": {
        "none": 1
      },
      "environment.network.profile": {
        "none": 1
      },
      "environment.ram_gib": {
        "none": 222
      },
      "environment.toolchains.elixir": {
        "none": 222
      },
      "environment.toolchains.erlang": {
        "none": 222
      },
      "environment.toolchains.node": {
        "none": 222
      },
      "environment.toolchains.other_inventory": {
        "none": 222
      },
      "environment.toolchains.ruby": {
        "none": 222
      },
      "environment.toolchains.rust": {
        "none": 222
      },
      "grade.grader": {
        "not re-derivable from the public record": 22
      },
      "grade.tests_ran": {
        "none": 24,
        "not re-derivable from the public record": 22
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 22
      },
      "host.cpu": {
        "none": 222
      },
      "host.kernel": {
        "none": 102
      },
      "host.ram_gib": {
        "none": 222
      },
      "host.spec_ref": {
        "none": 22
      },
      "host.vcpu": {
        "none": 222
      },
      "itt.class": {
        "none": 46
      },
      "itt.cohort": {
        "none": 22
      },
      "itt.evidence_ref": {
        "none": 46
      },
      "model.effective": {
        "none": 43
      },
      "outcome": {
        "not re-derivable from the public record": 22
      },
      "recipe": {
        "none": 222
      },
      "sandbox.egress_allow": {
        "none": 1
      },
      "sandbox.egress_profile": {
        "none": 1
      },
      "sandbox.profile": {
        "none": 1
      },
      "setup.deps_source": {
        "none": 222
      },
      "setup.sandbox_mode": {
        "none": 1
      },
      "setup.task_base.hash": {
        "none": 102
      },
      "setup.task_base.kind": {
        "none": 102
      },
      "stop_reason": {
        "none": 46
      },
      "task.base_repo": {
        "none": 22
      },
      "task.base_revision.hash": {
        "none": 102
      },
      "task.base_revision.kind": {
        "none": 102
      },
      "timestamps.attempts": {
        "none": 222
      },
      "timestamps.phases.develop.end_utc": {
        "none": 222
      },
      "timestamps.phases.develop.start_utc": {
        "none": 222
      },
      "timestamps.phases.gate.end_utc": {
        "none": 222
      },
      "timestamps.phases.gate.start_utc": {
        "none": 222
      },
      "timestamps.phases.grade.end_utc": {
        "none": 222
      },
      "timestamps.phases.grade.start_utc": {
        "none": 222
      },
      "timestamps.phases.plan.end_utc": {
        "none": 222
      },
      "timestamps.phases.plan.start_utc": {
        "none": 222
      },
      "timestamps.phases.review.end_utc": {
        "none": 222
      },
      "timestamps.phases.review.start_utc": {
        "none": 222
      },
      "timestamps.phases.setup.end_utc": {
        "none": 222
      },
      "timestamps.phases.setup.start_utc": {
        "none": 222
      },
      "timestamps.phases.shape.end_utc": {
        "none": 222
      },
      "timestamps.phases.shape.start_utc": {
        "none": 222
      },
      "timing.phases_s.develop": {
        "none": 222
      },
      "timing.phases_s.gate": {
        "none": 222
      },
      "timing.phases_s.grade": {
        "none": 46
      },
      "timing.phases_s.plan": {
        "none": 222
      },
      "timing.phases_s.review": {
        "none": 222
      },
      "timing.phases_s.setup": {
        "none": 222
      },
      "timing.phases_s.shape": {
        "none": 222
      },
      "timing.total_wall_s": {
        "none": 1
      },
      "tokens.phases.develop.cached_input": {
        "none": 222
      },
      "tokens.phases.develop.input": {
        "none": 222
      },
      "tokens.phases.develop.output": {
        "none": 222
      },
      "tokens.phases.develop.reasoning": {
        "none": 222
      },
      "tokens.phases.gate.cached_input": {
        "none": 222
      },
      "tokens.phases.gate.input": {
        "none": 222
      },
      "tokens.phases.gate.output": {
        "none": 222
      },
      "tokens.phases.gate.reasoning": {
        "none": 222
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
        "none": 222
      },
      "tokens.phases.plan.input": {
        "none": 222
      },
      "tokens.phases.plan.output": {
        "none": 222
      },
      "tokens.phases.plan.reasoning": {
        "none": 222
      },
      "tokens.phases.review.cached_input": {
        "none": 222
      },
      "tokens.phases.review.input": {
        "none": 222
      },
      "tokens.phases.review.output": {
        "none": 222
      },
      "tokens.phases.review.reasoning": {
        "none": 222
      },
      "tokens.phases.setup.cached_input": {
        "none": 222
      },
      "tokens.phases.setup.input": {
        "none": 222
      },
      "tokens.phases.setup.output": {
        "none": 222
      },
      "tokens.phases.setup.reasoning": {
        "none": 222
      },
      "tokens.phases.shape.cached_input": {
        "none": 222
      },
      "tokens.phases.shape.input": {
        "none": 222
      },
      "tokens.phases.shape.output": {
        "none": 222
      },
      "tokens.phases.shape.reasoning": {
        "none": 222
      },
      "tokens.total.cached_input": {
        "none": 48
      },
      "tokens.total.input": {
        "none": 48
      },
      "tokens.total.output": {
        "none": 48
      },
      "tokens.total.reasoning": {
        "none": 48
      },
      "tools.codex_cli": {
        "none": 222
      },
      "tools.grader": {
        "none": 222
      },
      "tools.runner": {
        "none": 222
      },
      "tools.toolchains.elixir": {
        "none": 222
      },
      "tools.toolchains.erlang": {
        "none": 222
      },
      "tools.toolchains.node": {
        "none": 222
      },
      "tools.toolchains.other_inventory": {
        "none": 222
      },
      "tools.toolchains.ruby": {
        "none": 222
      },
      "tools.toolchains.rust": {
        "none": 222
      }
    },
    "reconstructable": {}
  },
  "publication_reconciliation": {
    "disposition": "Keep this original capture separate from r56b, r56c, r56d and r56p2. The public records do not reproduce the historical validity-filtered analysis or its arm-level adoption tests; retain INTERIM and do not reinstate the old comparison table.",
    "original_execution_command": "not recorded in the public snapshot",
    "harness_source_commit": "absent; tools.harness values are wrapper fingerprints",
    "kogen_source_commit": "Public records mark the Kogen product commit not applicable for these harness records.",
    "raw_public_records": [
      "results/run-records/r56.jsonl",
      "results/cells.jsonl"
    ],
    "public_record_rebuild": "python3 reproduce/export_results.py; python3 reproduce/build_records.py; python3 reproduce/validate_round.py --round r56"
  },
  "round": "r56"
}
```
