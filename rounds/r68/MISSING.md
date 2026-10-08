# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 12,
  "fields": {
    "arm": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 4,
      "reasons": {
        "Arm label not retained": 4
      }
    },
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Boundary telemetry not retained": 12
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Boundary telemetry not retained": 12
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 12
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Boundary telemetry not retained": 12
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "No matching controller samples retained": 12
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 4
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 4
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 4
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 4
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Complete per-model billable vector unavailable": 8,
        "Not available for ungraded delivery": 4
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
      "count": 12,
      "reasons": {
        "No dated account-class receipt": 12
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "No per-cell CPU allocation receipt": 8,
        "Not available for ungraded delivery": 4
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "No per-cell CPU receipt": 8,
        "Not available for ungraded delivery": 4
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
      "count": 12,
      "reasons": {
        "No per-cell RAM receipt": 8,
        "Not available for ungraded delivery": 4
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Toolchain version/inventory not recorded": 8
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Toolchain version/inventory not recorded": 8
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Toolchain version/inventory not recorded": 8
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Toolchain version/inventory not recorded": 8
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Toolchain version/inventory not recorded": 8
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Toolchain version/inventory not recorded": 8
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 4,
      "reasons": {
        "No official grade in the public snapshot": 4
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 12,
      "reasons": {
        "Boolean receipt not recorded": 8,
        "No official grade in the public snapshot": 4
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 4,
      "reasons": {
        "No official grade in the public snapshot": 4
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 12,
      "reasons": {
        "No per-cell CPU receipt": 8,
        "Not available for ungraded delivery": 4
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 12,
      "reasons": {
        "No per-cell RAM receipt": 8,
        "Not available for ungraded delivery": 4
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 4
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 12,
      "reasons": {
        "No per-cell CPU allocation receipt": 8,
        "Not available for ungraded delivery": 4
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 12,
      "reasons": {
        "Invalid/environment cause requires evidence audit": 8,
        "Ungraded delivery needs evidence audit": 4
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 4,
      "reasons": {
        "No captured cohort launch receipt": 4
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 12,
      "reasons": {
        "No audited ITT receipt": 4,
        "No evidence-backed ITT classification": 8
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
      "count": 4,
      "reasons": {
        "No official grade in the public snapshot": 4
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Not recorded in available public metadata": 8
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
      "count": 3,
      "reasons": {
        "Public sandbox profile fingerprint not yet captured": 3
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Dependency source not pinned per cell": 12
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
      "count": 3,
      "reasons": {
        "Public sandbox profile fingerprint not yet captured": 3
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 4
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 4
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 12,
      "reasons": {
        "No normalized stop receipt": 4,
        "Runner status does not establish normalized stop cause": 8
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 4
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 4
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 4
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Attempt boundary receipts unavailable": 12
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
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Phase wall not emitted or not separable": 8
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Phase wall not emitted or not separable": 8
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Phase wall not emitted or not separable": 8
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Phase wall not emitted or not separable": 8
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Phase wall not emitted or not separable": 8
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Phase wall not emitted or not separable": 8
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Phase wall not emitted or not separable": 8
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
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 4
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 4
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 4
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 4
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 8,
        "Usage counter unavailable": 4
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 8,
        "Usage counter unavailable": 4
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 8,
        "Usage counter unavailable": 4
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 8,
        "Usage counter unavailable": 4
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 8,
        "Not available for ungraded delivery": 4
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 8,
        "Not available for ungraded delivery": 4
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 8,
        "Not available for ungraded delivery": 4
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Toolchain version/inventory not recorded": 8
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Toolchain version/inventory not recorded": 8
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Toolchain version/inventory not recorded": 8
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Toolchain version/inventory not recorded": 8
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Toolchain version/inventory not recorded": 8
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Toolchain version/inventory not recorded": 8
      }
    }
  },
  "gap_sources": {
    "lost": {
      "arm": {
        "none": 4
      },
      "circumstances.cap_end": {
        "none": 12
      },
      "circumstances.concurrent_cells_end": {
        "none": 12
      },
      "circumstances.concurrent_cells_start": {
        "none": 12
      },
      "circumstances.load1_end": {
        "none": 12
      },
      "circumstances.load_samples": {
        "none": 12
      },
      "cost.accounting": {
        "none": 4
      },
      "cost.calculator_version": {
        "none": 4
      },
      "cost.long_context_reconciled": {
        "none": 4
      },
      "cost.price_table_version": {
        "none": 4
      },
      "cost.usd": {
        "none": 12
      },
      "effort.effective": {
        "none": 4
      },
      "environment.account_class": {
        "none": 12
      },
      "environment.cores": {
        "none": 12
      },
      "environment.cpu_model": {
        "none": 12
      },
      "environment.network.allowlist_hosts": {
        "none": 4
      },
      "environment.network.profile": {
        "none": 4
      },
      "environment.ram_gib": {
        "none": 12
      },
      "environment.toolchains.elixir": {
        "none": 12
      },
      "environment.toolchains.erlang": {
        "none": 12
      },
      "environment.toolchains.node": {
        "none": 12
      },
      "environment.toolchains.other_inventory": {
        "none": 12
      },
      "environment.toolchains.ruby": {
        "none": 12
      },
      "environment.toolchains.rust": {
        "none": 12
      },
      "grade.grader": {
        "not re-derivable from the public record": 4
      },
      "grade.tests_ran": {
        "none": 8,
        "not re-derivable from the public record": 4
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 4
      },
      "host.cpu": {
        "none": 12
      },
      "host.ram_gib": {
        "none": 12
      },
      "host.spec_ref": {
        "none": 4
      },
      "host.vcpu": {
        "none": 12
      },
      "itt.class": {
        "none": 12
      },
      "itt.cohort": {
        "none": 4
      },
      "itt.evidence_ref": {
        "none": 12
      },
      "model.effective": {
        "none": 4
      },
      "outcome": {
        "not re-derivable from the public record": 4
      },
      "recipe": {
        "none": 12
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
        "none": 12
      },
      "setup.sandbox_mode": {
        "none": 4
      },
      "setup.task_base.hash": {
        "none": 4
      },
      "setup.task_base.kind": {
        "none": 4
      },
      "stop_reason": {
        "none": 12
      },
      "task.base_repo": {
        "none": 4
      },
      "task.base_revision.hash": {
        "none": 4
      },
      "task.base_revision.kind": {
        "none": 4
      },
      "timestamps.attempts": {
        "none": 12
      },
      "timestamps.phases.develop.end_utc": {
        "none": 12
      },
      "timestamps.phases.develop.start_utc": {
        "none": 12
      },
      "timestamps.phases.gate.end_utc": {
        "none": 12
      },
      "timestamps.phases.gate.start_utc": {
        "none": 12
      },
      "timestamps.phases.grade.end_utc": {
        "none": 12
      },
      "timestamps.phases.grade.start_utc": {
        "none": 12
      },
      "timestamps.phases.plan.end_utc": {
        "none": 12
      },
      "timestamps.phases.plan.start_utc": {
        "none": 12
      },
      "timestamps.phases.review.end_utc": {
        "none": 12
      },
      "timestamps.phases.review.start_utc": {
        "none": 12
      },
      "timestamps.phases.setup.end_utc": {
        "none": 12
      },
      "timestamps.phases.setup.start_utc": {
        "none": 12
      },
      "timestamps.phases.shape.end_utc": {
        "none": 12
      },
      "timestamps.phases.shape.start_utc": {
        "none": 12
      },
      "timing.phases_s.develop": {
        "none": 12
      },
      "timing.phases_s.gate": {
        "none": 12
      },
      "timing.phases_s.grade": {
        "none": 12
      },
      "timing.phases_s.plan": {
        "none": 12
      },
      "timing.phases_s.review": {
        "none": 12
      },
      "timing.phases_s.setup": {
        "none": 12
      },
      "timing.phases_s.shape": {
        "none": 12
      },
      "timing.total_wall_s": {
        "none": 4
      },
      "tokens.phases.develop.cached_input": {
        "none": 12
      },
      "tokens.phases.develop.input": {
        "none": 12
      },
      "tokens.phases.develop.output": {
        "none": 12
      },
      "tokens.phases.develop.reasoning": {
        "none": 12
      },
      "tokens.phases.gate.cached_input": {
        "none": 12
      },
      "tokens.phases.gate.input": {
        "none": 12
      },
      "tokens.phases.gate.output": {
        "none": 12
      },
      "tokens.phases.gate.reasoning": {
        "none": 12
      },
      "tokens.phases.grade.cached_input": {
        "none": 4
      },
      "tokens.phases.grade.input": {
        "none": 4
      },
      "tokens.phases.grade.output": {
        "none": 4
      },
      "tokens.phases.grade.reasoning": {
        "none": 4
      },
      "tokens.phases.plan.cached_input": {
        "none": 12
      },
      "tokens.phases.plan.input": {
        "none": 12
      },
      "tokens.phases.plan.output": {
        "none": 12
      },
      "tokens.phases.plan.reasoning": {
        "none": 12
      },
      "tokens.phases.review.cached_input": {
        "none": 12
      },
      "tokens.phases.review.input": {
        "none": 12
      },
      "tokens.phases.review.output": {
        "none": 12
      },
      "tokens.phases.review.reasoning": {
        "none": 12
      },
      "tokens.phases.setup.cached_input": {
        "none": 12
      },
      "tokens.phases.setup.input": {
        "none": 12
      },
      "tokens.phases.setup.output": {
        "none": 12
      },
      "tokens.phases.setup.reasoning": {
        "none": 12
      },
      "tokens.phases.shape.cached_input": {
        "none": 12
      },
      "tokens.phases.shape.input": {
        "none": 12
      },
      "tokens.phases.shape.output": {
        "none": 12
      },
      "tokens.phases.shape.reasoning": {
        "none": 12
      },
      "tokens.total.cached_input": {
        "none": 12
      },
      "tokens.total.input": {
        "none": 12
      },
      "tokens.total.output": {
        "none": 12
      },
      "tokens.total.reasoning": {
        "none": 12
      },
      "tools.codex_cli": {
        "none": 12
      },
      "tools.grader": {
        "none": 12
      },
      "tools.runner": {
        "none": 12
      },
      "tools.toolchains.elixir": {
        "none": 12
      },
      "tools.toolchains.erlang": {
        "none": 12
      },
      "tools.toolchains.node": {
        "none": 12
      },
      "tools.toolchains.other_inventory": {
        "none": 12
      },
      "tools.toolchains.ruby": {
        "none": 12
      },
      "tools.toolchains.rust": {
        "none": 12
      }
    },
    "reconstructable": {
      "sandbox.profile_sha256": {
        "Delivery attempt sandbox.sb on eu-worker": 3
      },
      "setup.sandbox_profile_sha256": {
        "Delivery attempt sandbox.sb on eu-worker": 3
      },
      "timestamps.cell.end_utc": {
        "Completion manifest or dispatcher END": 4
      }
    }
  },
  "round": "r68"
}
```
