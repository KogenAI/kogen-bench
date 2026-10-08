# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 68,
  "fields": {
    "arm": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 2,
      "reasons": {
        "Arm label not retained": 2
      }
    },
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Boundary telemetry not retained": 68
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 17,
      "reasons": {
        "Boundary telemetry not retained": 17
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 17,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 17
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Boundary telemetry not retained": 68
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 17,
      "reasons": {
        "No matching controller samples retained": 17
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Complete per-model billable vector unavailable": 63,
        "Not available for ungraded delivery": 5
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 4,
      "reasons": {
        "Not recorded in available public metadata": 4
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 17,
      "reasons": {
        "No dated account-class receipt": 17
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "No per-cell CPU allocation receipt": 63,
        "Not available for ungraded delivery": 5
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "No per-cell CPU receipt": 63,
        "Not available for ungraded delivery": 5
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 51,
      "reasons": {
        "No per-cell kernel receipt": 48,
        "Not available for ungraded delivery": 3
      }
    },
    "environment.network.allowlist_hosts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 4,
      "reasons": {
        "Allowlist unavailable": 4
      }
    },
    "environment.network.profile": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 4,
      "reasons": {
        "Not recorded in available public metadata": 4
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "No per-cell RAM receipt": 63,
        "Not available for ungraded delivery": 5
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 63
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 63
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 63
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 63
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 63
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 63
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 5,
      "reasons": {
        "No official grade in the public snapshot": 5
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 5,
      "reasons": {
        "No official grade in the public snapshot": 5
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 5,
      "reasons": {
        "No official grade in the public snapshot": 5
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 68,
      "reasons": {
        "No per-cell CPU receipt": 63,
        "Not available for ungraded delivery": 5
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 51,
      "reasons": {
        "No per-cell kernel receipt": 48,
        "Not available for ungraded delivery": 3
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 68,
      "reasons": {
        "No per-cell RAM receipt": 63,
        "Not available for ungraded delivery": 5
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 68,
      "reasons": {
        "No per-cell CPU allocation receipt": 63,
        "Not available for ungraded delivery": 5
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 5,
      "reasons": {
        "Ungraded delivery needs evidence audit": 5
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 5,
      "reasons": {
        "No captured cohort launch receipt": 5
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 5,
      "reasons": {
        "No audited ITT receipt": 5
      }
    },
    "model.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 4,
      "reasons": {
        "Not recorded in available public metadata": 4
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 6,
      "reasons": {
        "No official grade in the public snapshot": 5,
        "Official result outside standard outcome classes": 1
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Not recorded in available public metadata": 63
      }
    },
    "sandbox.egress_allow": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 4,
      "reasons": {
        "Allowlist unavailable": 4
      }
    },
    "sandbox.egress_profile": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 4,
      "reasons": {
        "Not recorded in available public metadata": 4
      }
    },
    "sandbox.profile": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 4,
      "reasons": {
        "Not recorded in available public metadata": 4
      }
    },
    "sandbox.profile_sha256": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 2,
      "reasons": {
        "Public sandbox profile fingerprint not yet captured": 2
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Dependency source not pinned per cell": 68
      }
    },
    "setup.sandbox_mode": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 4,
      "reasons": {
        "Not recorded in available public metadata": 4
      }
    },
    "setup.sandbox_profile_sha256": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 2,
      "reasons": {
        "Public sandbox profile fingerprint not yet captured": 2
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 53,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 48
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 53,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Original base revision type not recorded per cell": 48
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 4,
      "reasons": {
        "No normalized stop receipt": 4
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 53,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 48
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 53,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Original base revision type not recorded per cell": 48
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Attempt boundary receipts unavailable": 68
      }
    },
    "timestamps.cell.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 4,
      "reasons": {
        "End boundary absent; delivery may be active or receipt lost": 4
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Absolute phase boundary not retained": 68
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Absolute phase boundary not retained": 68
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Absolute phase boundary not retained": 68
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Absolute phase boundary not retained": 68
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Absolute phase boundary not retained": 68
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Absolute phase boundary not retained": 68
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Absolute phase boundary not retained": 68
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Absolute phase boundary not retained": 68
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Absolute phase boundary not retained": 68
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Absolute phase boundary not retained": 68
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Absolute phase boundary not retained": 68
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Absolute phase boundary not retained": 68
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Absolute phase boundary not retained": 68
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Absolute phase boundary not retained": 68
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Phase wall not emitted or not separable": 63
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Phase wall not emitted or not separable": 63
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Phase wall not emitted or not separable": 63
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Phase wall not emitted or not separable": 63
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Phase wall not emitted or not separable": 63
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Phase wall not emitted or not separable": 63
      }
    },
    "timing.total_wall_s": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 4,
      "reasons": {
        "Wall counter unavailable": 4
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 63
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 63
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 63
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 63
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 63
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 63
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 63
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 63
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 63
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 63
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 63
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 63
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 63
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 63
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 63
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 63
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 63
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 63
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 63
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 63
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 63
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 63
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 63
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-phase token counter not emitted": 63
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 67,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 63,
        "Usage counter unavailable": 4
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 67,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 63,
        "Usage counter unavailable": 4
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 67,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 63,
        "Usage counter unavailable": 4
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 67,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 63,
        "Usage counter unavailable": 4
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 63,
        "Not available for ungraded delivery": 5
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 63,
        "Not available for ungraded delivery": 5
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 63,
        "Not available for ungraded delivery": 5
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 63
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 63
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 63
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 63
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 63
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 68,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Toolchain version/inventory not recorded": 63
      }
    }
  },
  "gap_sources": {
    "lost": {
      "arm": {
        "none": 2
      },
      "circumstances.cap_end": {
        "none": 68
      },
      "circumstances.concurrent_cells_end": {
        "none": 17
      },
      "circumstances.concurrent_cells_start": {
        "none": 17
      },
      "circumstances.load1_end": {
        "none": 68
      },
      "circumstances.load_samples": {
        "none": 17
      },
      "cost.accounting": {
        "none": 5
      },
      "cost.calculator_version": {
        "none": 5
      },
      "cost.long_context_reconciled": {
        "none": 5
      },
      "cost.price_table_version": {
        "none": 5
      },
      "cost.usd": {
        "none": 68
      },
      "effort.effective": {
        "none": 4
      },
      "environment.account_class": {
        "none": 17
      },
      "environment.cores": {
        "none": 68
      },
      "environment.cpu_model": {
        "none": 68
      },
      "environment.kernel": {
        "none": 51
      },
      "environment.network.allowlist_hosts": {
        "none": 4
      },
      "environment.network.profile": {
        "none": 4
      },
      "environment.ram_gib": {
        "none": 68
      },
      "environment.toolchains.elixir": {
        "none": 68
      },
      "environment.toolchains.erlang": {
        "none": 68
      },
      "environment.toolchains.node": {
        "none": 68
      },
      "environment.toolchains.other_inventory": {
        "none": 68
      },
      "environment.toolchains.ruby": {
        "none": 68
      },
      "environment.toolchains.rust": {
        "none": 68
      },
      "grade.grader": {
        "not re-derivable from the public record": 5
      },
      "grade.tests_ran": {
        "not re-derivable from the public record": 5
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 5
      },
      "host.cpu": {
        "none": 68
      },
      "host.kernel": {
        "none": 51
      },
      "host.ram_gib": {
        "none": 68
      },
      "host.spec_ref": {
        "none": 5
      },
      "host.vcpu": {
        "none": 68
      },
      "itt.class": {
        "none": 5
      },
      "itt.cohort": {
        "none": 5
      },
      "itt.evidence_ref": {
        "none": 5
      },
      "model.effective": {
        "none": 4
      },
      "outcome": {
        "none": 1,
        "not re-derivable from the public record": 5
      },
      "recipe": {
        "none": 68
      },
      "sandbox.egress_allow": {
        "none": 4
      },
      "sandbox.egress_profile": {
        "none": 4
      },
      "sandbox.profile": {
        "none": 4
      },
      "setup.deps_source": {
        "none": 68
      },
      "setup.sandbox_mode": {
        "none": 4
      },
      "setup.task_base.hash": {
        "none": 53
      },
      "setup.task_base.kind": {
        "none": 53
      },
      "stop_reason": {
        "none": 4
      },
      "task.base_repo": {
        "none": 5
      },
      "task.base_revision.hash": {
        "none": 53
      },
      "task.base_revision.kind": {
        "none": 53
      },
      "timestamps.attempts": {
        "none": 68
      },
      "timestamps.phases.develop.end_utc": {
        "none": 68
      },
      "timestamps.phases.develop.start_utc": {
        "none": 68
      },
      "timestamps.phases.gate.end_utc": {
        "none": 68
      },
      "timestamps.phases.gate.start_utc": {
        "none": 68
      },
      "timestamps.phases.grade.end_utc": {
        "none": 68
      },
      "timestamps.phases.grade.start_utc": {
        "none": 68
      },
      "timestamps.phases.plan.end_utc": {
        "none": 68
      },
      "timestamps.phases.plan.start_utc": {
        "none": 68
      },
      "timestamps.phases.review.end_utc": {
        "none": 68
      },
      "timestamps.phases.review.start_utc": {
        "none": 68
      },
      "timestamps.phases.setup.end_utc": {
        "none": 68
      },
      "timestamps.phases.setup.start_utc": {
        "none": 68
      },
      "timestamps.phases.shape.end_utc": {
        "none": 68
      },
      "timestamps.phases.shape.start_utc": {
        "none": 68
      },
      "timing.phases_s.develop": {
        "none": 68
      },
      "timing.phases_s.gate": {
        "none": 68
      },
      "timing.phases_s.grade": {
        "none": 5
      },
      "timing.phases_s.plan": {
        "none": 68
      },
      "timing.phases_s.review": {
        "none": 68
      },
      "timing.phases_s.setup": {
        "none": 68
      },
      "timing.phases_s.shape": {
        "none": 68
      },
      "timing.total_wall_s": {
        "none": 4
      },
      "tokens.phases.develop.cached_input": {
        "none": 68
      },
      "tokens.phases.develop.input": {
        "none": 68
      },
      "tokens.phases.develop.output": {
        "none": 68
      },
      "tokens.phases.develop.reasoning": {
        "none": 68
      },
      "tokens.phases.gate.cached_input": {
        "none": 68
      },
      "tokens.phases.gate.input": {
        "none": 68
      },
      "tokens.phases.gate.output": {
        "none": 68
      },
      "tokens.phases.gate.reasoning": {
        "none": 68
      },
      "tokens.phases.grade.cached_input": {
        "none": 5
      },
      "tokens.phases.grade.input": {
        "none": 5
      },
      "tokens.phases.grade.output": {
        "none": 5
      },
      "tokens.phases.grade.reasoning": {
        "none": 5
      },
      "tokens.phases.plan.cached_input": {
        "none": 68
      },
      "tokens.phases.plan.input": {
        "none": 68
      },
      "tokens.phases.plan.output": {
        "none": 68
      },
      "tokens.phases.plan.reasoning": {
        "none": 68
      },
      "tokens.phases.review.cached_input": {
        "none": 68
      },
      "tokens.phases.review.input": {
        "none": 68
      },
      "tokens.phases.review.output": {
        "none": 68
      },
      "tokens.phases.review.reasoning": {
        "none": 68
      },
      "tokens.phases.setup.cached_input": {
        "none": 68
      },
      "tokens.phases.setup.input": {
        "none": 68
      },
      "tokens.phases.setup.output": {
        "none": 68
      },
      "tokens.phases.setup.reasoning": {
        "none": 68
      },
      "tokens.phases.shape.cached_input": {
        "none": 68
      },
      "tokens.phases.shape.input": {
        "none": 68
      },
      "tokens.phases.shape.output": {
        "none": 68
      },
      "tokens.phases.shape.reasoning": {
        "none": 68
      },
      "tokens.total.cached_input": {
        "none": 67
      },
      "tokens.total.input": {
        "none": 67
      },
      "tokens.total.output": {
        "none": 67
      },
      "tokens.total.reasoning": {
        "none": 67
      },
      "tools.codex_cli": {
        "none": 68
      },
      "tools.grader": {
        "none": 68
      },
      "tools.runner": {
        "none": 68
      },
      "tools.toolchains.elixir": {
        "none": 68
      },
      "tools.toolchains.erlang": {
        "none": 68
      },
      "tools.toolchains.node": {
        "none": 68
      },
      "tools.toolchains.other_inventory": {
        "none": 68
      },
      "tools.toolchains.ruby": {
        "none": 68
      },
      "tools.toolchains.rust": {
        "none": 68
      }
    },
    "reconstructable": {
      "sandbox.profile_sha256": {
        "Delivery attempt sandbox.sb on eu-worker": 2
      },
      "setup.sandbox_profile_sha256": {
        "Delivery attempt sandbox.sb on eu-worker": 2
      },
      "timestamps.cell.end_utc": {
        "Completion manifest or dispatcher END": 4
      }
    }
  },
  "round": "r45"
}
```
