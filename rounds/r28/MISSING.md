# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 55,
  "fields": {
    "arm": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Arm label not retained": 1
      }
    },
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
      "count": 14,
      "reasons": {
        "Not available for ungraded delivery": 14
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 14,
      "reasons": {
        "Not available for ungraded delivery": 14
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 14,
      "reasons": {
        "Not available for ungraded delivery": 14
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 14,
      "reasons": {
        "Not available for ungraded delivery": 14
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Complete per-model billable vector unavailable": 41,
        "Not available for ungraded delivery": 14
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 14,
      "reasons": {
        "Not recorded in available public metadata": 14
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
        "No per-cell CPU allocation receipt": 41,
        "Not available for ungraded delivery": 14
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "No per-cell CPU receipt": 41,
        "Not available for ungraded delivery": 14
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "No per-cell kernel receipt": 27,
        "Not available for ungraded delivery": 13
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
      "count": 55,
      "reasons": {
        "No per-cell RAM receipt": 41,
        "Not available for ungraded delivery": 14
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Toolchain version/inventory not recorded": 41
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Toolchain version/inventory not recorded": 41
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Toolchain version/inventory not recorded": 41
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Toolchain version/inventory not recorded": 41
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Toolchain version/inventory not recorded": 41
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Toolchain version/inventory not recorded": 41
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 14,
      "reasons": {
        "No official grade in the public snapshot": 14
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 15,
      "reasons": {
        "Boolean receipt not recorded": 1,
        "No official grade in the public snapshot": 14
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 14,
      "reasons": {
        "No official grade in the public snapshot": 14
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 55,
      "reasons": {
        "No per-cell CPU receipt": 41,
        "Not available for ungraded delivery": 14
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 40,
      "reasons": {
        "No per-cell kernel receipt": 27,
        "Not available for ungraded delivery": 13
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 55,
      "reasons": {
        "No per-cell RAM receipt": 41,
        "Not available for ungraded delivery": 14
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 14,
      "reasons": {
        "Not available for ungraded delivery": 14
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 55,
      "reasons": {
        "No per-cell CPU allocation receipt": 41,
        "Not available for ungraded delivery": 14
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 14,
      "reasons": {
        "Ungraded delivery needs evidence audit": 14
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 14,
      "reasons": {
        "No captured cohort launch receipt": 14
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 14,
      "reasons": {
        "No audited ITT receipt": 14
      }
    },
    "model.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 14,
      "reasons": {
        "Not recorded in available public metadata": 14
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 14,
      "reasons": {
        "No official grade in the public snapshot": 14
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Not recorded in available public metadata": 41
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
    "sandbox.profile_sha256": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Public sandbox profile fingerprint not yet captured": 1
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Dependency source not pinned per cell": 55
      }
    },
    "setup.sandbox_mode": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not recorded in available public metadata": 1
      }
    },
    "setup.sandbox_profile_sha256": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Public sandbox profile fingerprint not yet captured": 1
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 27
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Original base revision type not recorded per cell": 27
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 15,
      "reasons": {
        "No normalized stop receipt": 14,
        "Runner status does not establish normalized stop cause": 1
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 14,
      "reasons": {
        "Not available for ungraded delivery": 14
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 27
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Original base revision type not recorded per cell": 27
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Attempt boundary receipts unavailable": 55
      }
    },
    "timestamps.cell.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "End boundary absent; delivery may be active or receipt lost": 1
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
        "Not available for ungraded delivery": 14,
        "Phase wall not emitted or not separable": 41
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Phase wall not emitted or not separable": 41
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Phase wall not emitted or not separable": 1
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Phase wall not emitted or not separable": 41
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Phase wall not emitted or not separable": 41
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Phase wall not emitted or not separable": 41
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Phase wall not emitted or not separable": 41
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
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 14,
      "reasons": {
        "Not available for ungraded delivery": 14
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 14,
      "reasons": {
        "Not available for ungraded delivery": 14
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 14,
      "reasons": {
        "Not available for ungraded delivery": 14
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 14,
      "reasons": {
        "Not available for ungraded delivery": 14
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 41,
        "Usage counter unavailable": 13
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 41,
        "Usage counter unavailable": 13
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 41,
        "Usage counter unavailable": 13
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 41,
        "Usage counter unavailable": 13
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 41,
        "Not available for ungraded delivery": 14
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 41,
        "Not available for ungraded delivery": 14
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 41,
        "Not available for ungraded delivery": 14
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Toolchain version/inventory not recorded": 41
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Toolchain version/inventory not recorded": 41
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Toolchain version/inventory not recorded": 41
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Toolchain version/inventory not recorded": 41
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Toolchain version/inventory not recorded": 41
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 14,
        "Toolchain version/inventory not recorded": 41
      }
    }
  },
  "gap_sources": {
    "lost": {
      "arm": {
        "none": 1
      },
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
        "none": 14
      },
      "cost.calculator_version": {
        "none": 14
      },
      "cost.long_context_reconciled": {
        "none": 14
      },
      "cost.price_table_version": {
        "none": 14
      },
      "cost.usd": {
        "none": 55
      },
      "effort.effective": {
        "none": 14
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
      "environment.network.allowlist_hosts": {
        "none": 1
      },
      "environment.network.profile": {
        "none": 1
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
        "not re-derivable from the public record": 14
      },
      "grade.tests_ran": {
        "none": 1,
        "not re-derivable from the public record": 14
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 14
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
        "none": 14
      },
      "host.vcpu": {
        "none": 55
      },
      "itt.class": {
        "none": 14
      },
      "itt.cohort": {
        "none": 14
      },
      "itt.evidence_ref": {
        "none": 14
      },
      "model.effective": {
        "none": 14
      },
      "outcome": {
        "not re-derivable from the public record": 14
      },
      "recipe": {
        "none": 55
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
        "none": 55
      },
      "setup.sandbox_mode": {
        "none": 1
      },
      "setup.task_base.hash": {
        "none": 41
      },
      "setup.task_base.kind": {
        "none": 41
      },
      "stop_reason": {
        "none": 15
      },
      "task.base_repo": {
        "none": 14
      },
      "task.base_revision.hash": {
        "none": 41
      },
      "task.base_revision.kind": {
        "none": 41
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
        "none": 15
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
      "timing.total_wall_s": {
        "none": 1
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
        "none": 14
      },
      "tokens.phases.grade.input": {
        "none": 14
      },
      "tokens.phases.grade.output": {
        "none": 14
      },
      "tokens.phases.grade.reasoning": {
        "none": 14
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
        "none": 54
      },
      "tokens.total.input": {
        "none": 54
      },
      "tokens.total.output": {
        "none": 54
      },
      "tokens.total.reasoning": {
        "none": 54
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
    "reconstructable": {
      "sandbox.profile_sha256": {
        "Delivery attempt sandbox.sb on us-worker": 1
      },
      "setup.sandbox_profile_sha256": {
        "Delivery attempt sandbox.sb on us-worker": 1
      },
      "timestamps.cell.end_utc": {
        "Completion manifest or dispatcher END": 1
      }
    }
  },
  "round": "r28"
}
```
