# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 55,
  "fields": {
    "arm": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Arm label not retained": 12
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
      "count": 55,
      "reasons": {
        "Boundary telemetry not retained": 55
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 43,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 43
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Boundary telemetry not retained": 55
      }
    },
    "circumstances.load1_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Manifest start load unavailable": 1
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "No matching controller samples retained": 55
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 12
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 12
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 12
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 12
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Complete per-model billable vector unavailable": 43,
        "Not available for ungraded delivery": 12
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 4,
      "reasons": {
        "Not recorded in available public metadata": 4
      }
    },
    "effort.requested": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not recorded in available public metadata": 1
      }
    },
    "effort.runner_requested": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not recorded in available public metadata": 1
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "No dated account-class receipt": 54
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "No per-cell CPU allocation receipt": 43,
        "Not available for ungraded delivery": 12
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "No per-cell CPU receipt": 43,
        "Not available for ungraded delivery": 12
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
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
    "environment.os": {
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
        "No per-cell RAM receipt": 43,
        "Not available for ungraded delivery": 12
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Toolchain version/inventory not recorded": 43
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Toolchain version/inventory not recorded": 43
      }
    },
    "environment.toolchains.python": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not recorded in available public metadata": 1
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Toolchain version/inventory not recorded": 43
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Toolchain version/inventory not recorded": 43
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 12,
      "reasons": {
        "No official grade in the public snapshot": 12
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 30,
      "reasons": {
        "Boolean receipt not recorded": 18,
        "No official grade in the public snapshot": 12
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 12,
      "reasons": {
        "No official grade in the public snapshot": 12
      }
    },
    "harness": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Harness not retained": 1
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 55,
      "reasons": {
        "No per-cell CPU receipt": 43,
        "Not available for ungraded delivery": 12
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "host.os": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 1,
      "reasons": {
        "Not recorded in available public metadata": 1
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 55,
      "reasons": {
        "No per-cell RAM receipt": 43,
        "Not available for ungraded delivery": 12
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 12
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 55,
      "reasons": {
        "No per-cell CPU allocation receipt": 43,
        "Not available for ungraded delivery": 12
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 30,
      "reasons": {
        "Invalid/environment cause requires evidence audit": 18,
        "Ungraded delivery needs evidence audit": 12
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 12,
      "reasons": {
        "No captured cohort launch receipt": 12
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 30,
      "reasons": {
        "No audited ITT receipt": 12,
        "No evidence-backed ITT classification": 18
      }
    },
    "kogen.best_candidate": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 29,
      "reasons": {
        "Not available for ungraded delivery": 11,
        "Not recorded in available public metadata": 18
      }
    },
    "kogen.landed": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 19,
      "reasons": {
        "Kogen report status absent": 8,
        "Not available for ungraded delivery": 11
      }
    },
    "model.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 4,
      "reasons": {
        "Not recorded in available public metadata": 4
      }
    },
    "model.requested": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not recorded in available public metadata": 1
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 12,
      "reasons": {
        "No official grade in the public snapshot": 12
      }
    },
    "provenance.manifest_sha256": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Manifest unavailable": 1
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 12
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
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "setup.adapter_harness_sha": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not recorded in available public metadata": 55
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Dependency source not pinned per cell": 1
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
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
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
      "count": 23,
      "reasons": {
        "No normalized stop receipt": 5,
        "Runner status does not establish normalized stop cause": 18
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Value withheld by PRIVATE.md": 12
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
    "task.id": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Task identity not retained": 1
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
      "count": 4,
      "reasons": {
        "End boundary absent; delivery may be active or receipt lost": 4
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
      "count": 17,
      "reasons": {
        "Absolute phase boundary not retained": 17
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 17,
      "reasons": {
        "Absolute phase boundary not retained": 17
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
      "count": 4,
      "reasons": {
        "Absolute phase boundary not retained": 4
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 4,
      "reasons": {
        "Absolute phase boundary not retained": 4
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
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Phase wall not emitted or not separable": 12
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 25,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Phase wall not emitted or not separable": 13
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 30,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Phase wall not emitted or not separable": 18
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Phase wall not emitted or not separable": 25
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Phase wall not emitted or not separable": 43
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 12
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 12
      }
    },
    "timing.timeout_cap_s": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 1,
      "reasons": {
        "Timeout receipt unavailable": 1
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
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 43
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 43
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 43
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 43
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 12
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 12
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 12
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 12
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 43
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 43
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 43
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 43
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 43
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 43
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 43
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 43
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 46,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 34
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 46,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 34
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 46,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 34
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 46,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Per-phase token counter not emitted": 34
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Usage counter unavailable": 4
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Usage counter unavailable": 4
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Usage counter unavailable": 4
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Usage counter unavailable": 4
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 43,
        "Not available for ungraded delivery": 12
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 43,
        "Not available for ungraded delivery": 12
      }
    },
    "tools.harness": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not recorded in available public metadata": 55
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 43,
        "Not available for ungraded delivery": 12
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Toolchain version/inventory not recorded": 43
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Toolchain version/inventory not recorded": 43
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Toolchain version/inventory not recorded": 43
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Toolchain version/inventory not recorded": 43
      }
    },
    "tools.toolchains.python": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not recorded in available public metadata": 1
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Toolchain version/inventory not recorded": 43
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 55,
      "reasons": {
        "Not available for ungraded delivery": 12,
        "Toolchain version/inventory not recorded": 43
      }
    }
  },
  "gap_sources": {
    "lost": {
      "arm": {
        "none": 12
      },
      "circumstances.cap_end": {
        "none": 55
      },
      "circumstances.concurrent_cells_end": {
        "none": 55
      },
      "circumstances.concurrent_cells_start": {
        "none": 43
      },
      "circumstances.load1_end": {
        "none": 55
      },
      "circumstances.load1_start": {
        "none": 1
      },
      "circumstances.load_samples": {
        "none": 55
      },
      "cost.accounting": {
        "none": 12
      },
      "cost.calculator_version": {
        "none": 12
      },
      "cost.long_context_reconciled": {
        "none": 12
      },
      "cost.price_table_version": {
        "none": 12
      },
      "cost.usd": {
        "none": 55
      },
      "effort.effective": {
        "none": 4
      },
      "effort.requested": {
        "none": 1
      },
      "effort.runner_requested": {
        "none": 1
      },
      "environment.account_class": {
        "none": 54
      },
      "environment.cores": {
        "none": 55
      },
      "environment.cpu_model": {
        "none": 55
      },
      "environment.kernel": {
        "none": 1
      },
      "environment.network.allowlist_hosts": {
        "none": 4
      },
      "environment.network.profile": {
        "none": 4
      },
      "environment.os": {
        "none": 1
      },
      "environment.ram_gib": {
        "none": 55
      },
      "environment.toolchains.elixir": {
        "none": 1
      },
      "environment.toolchains.erlang": {
        "none": 1
      },
      "environment.toolchains.node": {
        "none": 55
      },
      "environment.toolchains.other_inventory": {
        "none": 55
      },
      "environment.toolchains.python": {
        "none": 1
      },
      "environment.toolchains.ruby": {
        "none": 55
      },
      "environment.toolchains.rust": {
        "none": 55
      },
      "grade.grader": {
        "not re-derivable from the public record": 12
      },
      "grade.tests_ran": {
        "none": 18,
        "not re-derivable from the public record": 12
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 12
      },
      "harness": {
        "none": 1
      },
      "host.cpu": {
        "none": 55
      },
      "host.kernel": {
        "none": 1
      },
      "host.os": {
        "none": 1
      },
      "host.ram_gib": {
        "none": 55
      },
      "host.spec_ref": {
        "none": 12
      },
      "host.vcpu": {
        "none": 55
      },
      "itt.class": {
        "none": 30
      },
      "itt.cohort": {
        "none": 12
      },
      "itt.evidence_ref": {
        "none": 30
      },
      "kogen.best_candidate": {
        "none": 29
      },
      "kogen.landed": {
        "none": 19
      },
      "model.effective": {
        "none": 4
      },
      "model.requested": {
        "none": 1
      },
      "outcome": {
        "not re-derivable from the public record": 12
      },
      "provenance.manifest_sha256": {
        "none": 1
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
      "sandbox.profile_sha256": {
        "none": 1
      },
      "setup.adapter_harness_sha": {
        "none": 55
      },
      "setup.deps_source": {
        "none": 1
      },
      "setup.sandbox_mode": {
        "none": 4
      },
      "setup.sandbox_profile_sha256": {
        "none": 1
      },
      "setup.task_base.hash": {
        "none": 4
      },
      "setup.task_base.kind": {
        "none": 4
      },
      "stop_reason": {
        "none": 23
      },
      "task.base_repo": {
        "none": 24
      },
      "task.base_revision.hash": {
        "none": 4
      },
      "task.base_revision.kind": {
        "none": 4
      },
      "task.id": {
        "none": 1
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
        "none": 17
      },
      "timestamps.phases.gate.start_utc": {
        "none": 17
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
        "none": 4
      },
      "timestamps.phases.setup.start_utc": {
        "none": 4
      },
      "timestamps.phases.shape.end_utc": {
        "none": 55
      },
      "timestamps.phases.shape.start_utc": {
        "none": 55
      },
      "timing.phases_s.develop": {
        "none": 24
      },
      "timing.phases_s.gate": {
        "none": 25
      },
      "timing.phases_s.grade": {
        "none": 30
      },
      "timing.phases_s.plan": {
        "none": 37
      },
      "timing.phases_s.review": {
        "none": 55
      },
      "timing.phases_s.setup": {
        "none": 12
      },
      "timing.phases_s.shape": {
        "none": 12
      },
      "timing.timeout_cap_s": {
        "none": 1
      },
      "timing.total_wall_s": {
        "none": 4
      },
      "tokens.phases.develop.cached_input": {
        "none": 24
      },
      "tokens.phases.develop.input": {
        "none": 24
      },
      "tokens.phases.develop.output": {
        "none": 24
      },
      "tokens.phases.develop.reasoning": {
        "none": 24
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
        "none": 12
      },
      "tokens.phases.grade.input": {
        "none": 12
      },
      "tokens.phases.grade.output": {
        "none": 12
      },
      "tokens.phases.grade.reasoning": {
        "none": 12
      },
      "tokens.phases.plan.cached_input": {
        "none": 37
      },
      "tokens.phases.plan.input": {
        "none": 37
      },
      "tokens.phases.plan.output": {
        "none": 37
      },
      "tokens.phases.plan.reasoning": {
        "none": 37
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
        "none": 46
      },
      "tokens.phases.shape.input": {
        "none": 46
      },
      "tokens.phases.shape.output": {
        "none": 46
      },
      "tokens.phases.shape.reasoning": {
        "none": 46
      },
      "tokens.total.cached_input": {
        "none": 4
      },
      "tokens.total.input": {
        "none": 4
      },
      "tokens.total.output": {
        "none": 4
      },
      "tokens.total.reasoning": {
        "none": 4
      },
      "tools.codex_cli": {
        "none": 55
      },
      "tools.grader": {
        "none": 55
      },
      "tools.harness": {
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
      "tools.toolchains.python": {
        "none": 1
      },
      "tools.toolchains.ruby": {
        "none": 55
      },
      "tools.toolchains.rust": {
        "none": 55
      }
    },
    "reconstructable": {
      "timestamps.cell.end_utc": {
        "Completion manifest or dispatcher END": 4
      }
    }
  },
  "round": "r67b"
}
```
