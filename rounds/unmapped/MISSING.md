# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 500,
  "fields": {
    "arm": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 469,
      "reasons": {
        "Arm label not retained": 450,
        "Not recorded in available public metadata": 19
      }
    },
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Boundary telemetry not retained": 500
      }
    },
    "circumstances.cap_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 482,
      "reasons": {
        "Boundary telemetry not retained": 482
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Boundary telemetry not retained": 500
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Boundary telemetry not retained": 482,
        "Launch running/active counter is block-scoped; host concurrency not emitted": 18
      }
    },
    "circumstances.dispatcher_id": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 482,
      "reasons": {
        "Dispatcher receipt unavailable": 482
      }
    },
    "circumstances.incidents": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Cell interval unavailable for incident overlap audit": 10
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Boundary telemetry not retained": 500
      }
    },
    "circumstances.load1_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Boundary telemetry not retained": 10
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 498,
      "reasons": {
        "No matching controller samples retained": 498
      }
    },
    "circumstances.queue": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 482,
      "reasons": {
        "Queue receipt unavailable": 482
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 450,
      "reasons": {
        "Not available for ungraded delivery": 450
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 450,
      "reasons": {
        "Not available for ungraded delivery": 450
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 450,
      "reasons": {
        "Not available for ungraded delivery": 450
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 450,
      "reasons": {
        "Not available for ungraded delivery": 450
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 486,
      "reasons": {
        "Complete per-model billable vector unavailable": 36,
        "Not available for ungraded delivery": 450
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 70,
      "reasons": {
        "Not recorded in available public metadata": 70
      }
    },
    "effort.requested": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 9,
      "reasons": {
        "Not recorded in available public metadata": 9
      }
    },
    "effort.runner_requested": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 9,
      "reasons": {
        "Not recorded in available public metadata": 9
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 454,
      "reasons": {
        "No dated account-class receipt": 454
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "No per-cell CPU allocation receipt": 50,
        "Not available for ungraded delivery": 450
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "No per-cell CPU receipt": 50,
        "Not available for ungraded delivery": 450
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 156,
      "reasons": {
        "No per-cell kernel receipt": 18,
        "Not available for ungraded delivery": 138
      }
    },
    "environment.network.allowlist_hosts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 122,
      "reasons": {
        "Allowlist unavailable": 112,
        "Egress allowlist not recorded": 10
      }
    },
    "environment.network.profile": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 122,
      "reasons": {
        "Not recorded in available public metadata": 122
      }
    },
    "environment.os": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Not recorded in available public metadata": 10
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "No per-cell RAM receipt": 50,
        "Not available for ungraded delivery": 450
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Toolchain version/inventory not recorded": 50
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Toolchain version/inventory not recorded": 50
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Toolchain version/inventory not recorded": 50
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Toolchain version/inventory not recorded": 50
      }
    },
    "environment.toolchains.python": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Not recorded in available public metadata": 10
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Toolchain version/inventory not recorded": 50
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Toolchain version/inventory not recorded": 50
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 482,
      "reasons": {
        "No official grade in the public snapshot": 450,
        "Not recorded in available public metadata": 32
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 452,
      "reasons": {
        "Boolean receipt not recorded": 2,
        "No official grade in the public snapshot": 450
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 500,
      "reasons": {
        "No official grade in the public snapshot": 450,
        "Not recorded in available public metadata": 50
      }
    },
    "harness": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Not recorded in available public metadata": 6
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 500,
      "reasons": {
        "No per-cell CPU receipt": 50,
        "Not available for ungraded delivery": 450
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 156,
      "reasons": {
        "No per-cell kernel receipt": 18,
        "Not available for ungraded delivery": 138
      }
    },
    "host.os": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 10,
      "reasons": {
        "Not recorded in available public metadata": 10
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 500,
      "reasons": {
        "No per-cell RAM receipt": 50,
        "Not available for ungraded delivery": 450
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 458,
      "reasons": {
        "No measured host-spec reference": 8,
        "Not available for ungraded delivery": 450
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 500,
      "reasons": {
        "No per-cell CPU allocation receipt": 50,
        "Not available for ungraded delivery": 450
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 459,
      "reasons": {
        "Invalid/environment cause requires evidence audit": 9,
        "Ungraded delivery needs evidence audit": 450
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 406,
      "reasons": {
        "No captured cohort launch receipt": 406
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 459,
      "reasons": {
        "No audited ITT receipt": 450,
        "No evidence-backed ITT classification": 9
      }
    },
    "kogen.best_candidate": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Not available for ungraded delivery": 4,
        "Not recorded in available public metadata": 14
      }
    },
    "kogen.landed": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Kogen report status absent": 14,
        "Not available for ungraded delivery": 4
      }
    },
    "model.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Not recorded in available public metadata": 54
      }
    },
    "model.requested": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 9,
      "reasons": {
        "Not recorded in available public metadata": 9
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 450,
      "reasons": {
        "No official grade in the public snapshot": 450
      }
    },
    "provenance.manifest_sha256": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Exact pulled manifest unavailable": 10
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 434,
      "reasons": {
        "Not available for ungraded delivery": 402,
        "Not recorded in available public metadata": 32
      }
    },
    "round_id": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "No unambiguous owning round tag": 500
      }
    },
    "sandbox.egress_allow": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 122,
      "reasons": {
        "Allowlist unavailable": 112,
        "Egress allowlist not recorded": 10
      }
    },
    "sandbox.egress_profile": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 122,
      "reasons": {
        "Not recorded in available public metadata": 122
      }
    },
    "sandbox.profile": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 122,
      "reasons": {
        "Not recorded in available public metadata": 122
      }
    },
    "sandbox.profile_sha256": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 78,
      "reasons": {
        "Public sandbox profile fingerprint not yet captured": 68,
        "Sandbox profile hash not exported": 10
      }
    },
    "setup.adapter_harness_sha": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Not recorded in available public metadata": 10
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Dependency source not pinned per cell": 500
      }
    },
    "setup.kogen_sha": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 14,
        "Not available for ungraded delivery": 4
      }
    },
    "setup.sandbox_mode": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 122,
      "reasons": {
        "Not recorded in available public metadata": 122
      }
    },
    "setup.sandbox_profile_sha256": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 78,
      "reasons": {
        "Public sandbox profile fingerprint not yet captured": 68,
        "Sandbox profile hash not exported": 10
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 252,
      "reasons": {
        "Not available for ungraded delivery": 208,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 44
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 252,
      "reasons": {
        "Not available for ungraded delivery": 208,
        "Original base revision type not recorded per cell": 44
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 38,
      "reasons": {
        "No normalized stop receipt": 28,
        "Runner status does not establish normalized stop cause": 10
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 450,
      "reasons": {
        "Not available for ungraded delivery": 450
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 252,
      "reasons": {
        "Not available for ungraded delivery": 208,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 44
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 252,
      "reasons": {
        "Not available for ungraded delivery": 208,
        "Original base revision type not recorded per cell": 44
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Attempt boundary receipts unavailable": 500
      }
    },
    "timestamps.cell.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 10,
        "End boundary absent; delivery may be active or receipt lost": 2
      }
    },
    "timestamps.cell.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Absolute phase boundary not retained": 10
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 439,
      "reasons": {
        "Absolute UTC boundary was not emitted": 1,
        "Absolute phase boundary not retained": 438
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 439,
      "reasons": {
        "Absolute UTC boundary was not emitted": 1,
        "Absolute phase boundary not retained": 438
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Absolute phase boundary not retained": 500
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Absolute phase boundary not retained": 500
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Absolute phase boundary not retained": 500
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Absolute phase boundary not retained": 500
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Absolute phase boundary not retained": 500
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Absolute phase boundary not retained": 500
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Absolute phase boundary not retained": 500
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Absolute phase boundary not retained": 500
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Absolute phase boundary not retained": 500
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Absolute phase boundary not retained": 500
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Absolute phase boundary not retained": 500
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Absolute phase boundary not retained": 500
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Phase wall not emitted or not separable": 50
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Phase wall not emitted or not separable": 50
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 452,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Phase wall not emitted or not separable": 2
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Phase wall not emitted or not separable": 50
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Phase wall not emitted or not separable": 50
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Phase wall not emitted or not separable": 50
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Phase wall not emitted or not separable": 50
      }
    },
    "timing.timeout_cap_s": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 10,
      "reasons": {
        "Numeric counter not recorded": 10
      }
    },
    "timing.total_wall_s": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 12,
      "reasons": {
        "Numeric counter not recorded": 10,
        "Wall counter unavailable": 2
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 450,
      "reasons": {
        "Not available for ungraded delivery": 450
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 450,
      "reasons": {
        "Not available for ungraded delivery": 450
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 450,
      "reasons": {
        "Not available for ungraded delivery": 450
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 450,
      "reasons": {
        "Not available for ungraded delivery": 450
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 50,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 18,
        "Numeric counter not recorded": 10,
        "Usage counter unavailable": 22
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 50,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 18,
        "Numeric counter not recorded": 10,
        "Usage counter unavailable": 22
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 50,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 18,
        "Numeric counter not recorded": 10,
        "Usage counter unavailable": 22
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 71,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 18,
        "Numeric counter not recorded": 10,
        "Usage counter unavailable": 43
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 438,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 32,
        "Not available for ungraded delivery": 402,
        "Not recorded in available public metadata": 4
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 50,
        "Not available for ungraded delivery": 450
      }
    },
    "tools.harness": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Not recorded in available public metadata": 10
      }
    },
    "tools.kogen": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 14,
        "Not available for ungraded delivery": 4
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 50,
        "Not available for ungraded delivery": 450
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Toolchain version/inventory not recorded": 50
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Toolchain version/inventory not recorded": 50
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Toolchain version/inventory not recorded": 50
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Toolchain version/inventory not recorded": 50
      }
    },
    "tools.toolchains.python": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Not recorded in available public metadata": 10
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Toolchain version/inventory not recorded": 50
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 500,
      "reasons": {
        "Not available for ungraded delivery": 450,
        "Toolchain version/inventory not recorded": 50
      }
    }
  },
  "gap_sources": {
    "lost": {
      "arm": {
        "none": 469
      },
      "circumstances.cap_end": {
        "none": 500
      },
      "circumstances.cap_start": {
        "none": 482
      },
      "circumstances.concurrent_cells_end": {
        "none": 500
      },
      "circumstances.concurrent_cells_start": {
        "none": 500
      },
      "circumstances.dispatcher_id": {
        "none": 482
      },
      "circumstances.incidents": {
        "none": 10
      },
      "circumstances.load1_end": {
        "none": 500
      },
      "circumstances.load1_start": {
        "none": 10
      },
      "circumstances.load_samples": {
        "none": 498
      },
      "circumstances.queue": {
        "none": 482
      },
      "cost.accounting": {
        "none": 450
      },
      "cost.calculator_version": {
        "none": 450
      },
      "cost.long_context_reconciled": {
        "none": 450
      },
      "cost.price_table_version": {
        "none": 450
      },
      "cost.usd": {
        "none": 486
      },
      "effort.effective": {
        "none": 70
      },
      "effort.requested": {
        "none": 9
      },
      "effort.runner_requested": {
        "none": 9
      },
      "environment.account_class": {
        "none": 454
      },
      "environment.cores": {
        "none": 500
      },
      "environment.cpu_model": {
        "none": 500
      },
      "environment.kernel": {
        "none": 156
      },
      "environment.network.allowlist_hosts": {
        "none": 122
      },
      "environment.network.profile": {
        "none": 122
      },
      "environment.os": {
        "none": 10
      },
      "environment.ram_gib": {
        "none": 500
      },
      "environment.toolchains.elixir": {
        "none": 500
      },
      "environment.toolchains.erlang": {
        "none": 500
      },
      "environment.toolchains.node": {
        "none": 500
      },
      "environment.toolchains.other_inventory": {
        "none": 500
      },
      "environment.toolchains.python": {
        "none": 10
      },
      "environment.toolchains.ruby": {
        "none": 500
      },
      "environment.toolchains.rust": {
        "none": 500
      },
      "grade.grader": {
        "none": 32,
        "not re-derivable from the public record": 450
      },
      "grade.tests_ran": {
        "none": 2,
        "not re-derivable from the public record": 450
      },
      "grade.timestamp": {
        "none": 50,
        "not re-derivable from the public record": 450
      },
      "harness": {
        "none": 6
      },
      "host.cpu": {
        "none": 500
      },
      "host.kernel": {
        "none": 156
      },
      "host.os": {
        "none": 10
      },
      "host.ram_gib": {
        "none": 500
      },
      "host.spec_ref": {
        "none": 458
      },
      "host.vcpu": {
        "none": 500
      },
      "itt.class": {
        "none": 459
      },
      "itt.cohort": {
        "none": 406
      },
      "itt.evidence_ref": {
        "none": 459
      },
      "kogen.best_candidate": {
        "none": 18
      },
      "kogen.landed": {
        "none": 18
      },
      "model.effective": {
        "none": 54
      },
      "model.requested": {
        "none": 9
      },
      "outcome": {
        "not re-derivable from the public record": 450
      },
      "provenance.manifest_sha256": {
        "none": 10
      },
      "recipe": {
        "none": 434
      },
      "round_id": {
        "none": 500
      },
      "sandbox.egress_allow": {
        "none": 122
      },
      "sandbox.egress_profile": {
        "none": 122
      },
      "sandbox.profile": {
        "none": 122
      },
      "sandbox.profile_sha256": {
        "none": 10
      },
      "setup.adapter_harness_sha": {
        "none": 10
      },
      "setup.deps_source": {
        "none": 500
      },
      "setup.kogen_sha": {
        "none": 18
      },
      "setup.sandbox_mode": {
        "none": 122
      },
      "setup.sandbox_profile_sha256": {
        "none": 10
      },
      "setup.task_base.hash": {
        "none": 252
      },
      "setup.task_base.kind": {
        "none": 252
      },
      "stop_reason": {
        "none": 38
      },
      "task.base_repo": {
        "none": 450
      },
      "task.base_revision.hash": {
        "none": 252
      },
      "task.base_revision.kind": {
        "none": 252
      },
      "timestamps.attempts": {
        "none": 500
      },
      "timestamps.cell.end_utc": {
        "none": 10
      },
      "timestamps.cell.start_utc": {
        "none": 10
      },
      "timestamps.phases.develop.end_utc": {
        "none": 439
      },
      "timestamps.phases.develop.start_utc": {
        "none": 439
      },
      "timestamps.phases.gate.end_utc": {
        "none": 500
      },
      "timestamps.phases.gate.start_utc": {
        "none": 500
      },
      "timestamps.phases.grade.end_utc": {
        "none": 500
      },
      "timestamps.phases.grade.start_utc": {
        "none": 500
      },
      "timestamps.phases.plan.end_utc": {
        "none": 500
      },
      "timestamps.phases.plan.start_utc": {
        "none": 500
      },
      "timestamps.phases.review.end_utc": {
        "none": 500
      },
      "timestamps.phases.review.start_utc": {
        "none": 500
      },
      "timestamps.phases.setup.end_utc": {
        "none": 500
      },
      "timestamps.phases.setup.start_utc": {
        "none": 500
      },
      "timestamps.phases.shape.end_utc": {
        "none": 500
      },
      "timestamps.phases.shape.start_utc": {
        "none": 500
      },
      "timing.phases_s.develop": {
        "none": 500
      },
      "timing.phases_s.gate": {
        "none": 500
      },
      "timing.phases_s.grade": {
        "none": 452
      },
      "timing.phases_s.plan": {
        "none": 500
      },
      "timing.phases_s.review": {
        "none": 500
      },
      "timing.phases_s.setup": {
        "none": 500
      },
      "timing.phases_s.shape": {
        "none": 500
      },
      "timing.timeout_cap_s": {
        "none": 10
      },
      "timing.total_wall_s": {
        "none": 12
      },
      "tokens.phases.develop.cached_input": {
        "none": 500
      },
      "tokens.phases.develop.input": {
        "none": 500
      },
      "tokens.phases.develop.output": {
        "none": 500
      },
      "tokens.phases.develop.reasoning": {
        "none": 500
      },
      "tokens.phases.gate.cached_input": {
        "none": 500
      },
      "tokens.phases.gate.input": {
        "none": 500
      },
      "tokens.phases.gate.output": {
        "none": 500
      },
      "tokens.phases.gate.reasoning": {
        "none": 500
      },
      "tokens.phases.grade.cached_input": {
        "none": 450
      },
      "tokens.phases.grade.input": {
        "none": 450
      },
      "tokens.phases.grade.output": {
        "none": 450
      },
      "tokens.phases.grade.reasoning": {
        "none": 450
      },
      "tokens.phases.plan.cached_input": {
        "none": 500
      },
      "tokens.phases.plan.input": {
        "none": 500
      },
      "tokens.phases.plan.output": {
        "none": 500
      },
      "tokens.phases.plan.reasoning": {
        "none": 500
      },
      "tokens.phases.review.cached_input": {
        "none": 500
      },
      "tokens.phases.review.input": {
        "none": 500
      },
      "tokens.phases.review.output": {
        "none": 500
      },
      "tokens.phases.review.reasoning": {
        "none": 500
      },
      "tokens.phases.setup.cached_input": {
        "none": 500
      },
      "tokens.phases.setup.input": {
        "none": 500
      },
      "tokens.phases.setup.output": {
        "none": 500
      },
      "tokens.phases.setup.reasoning": {
        "none": 500
      },
      "tokens.phases.shape.cached_input": {
        "none": 500
      },
      "tokens.phases.shape.input": {
        "none": 500
      },
      "tokens.phases.shape.output": {
        "none": 500
      },
      "tokens.phases.shape.reasoning": {
        "none": 500
      },
      "tokens.total.cached_input": {
        "none": 50
      },
      "tokens.total.input": {
        "none": 50
      },
      "tokens.total.output": {
        "none": 50
      },
      "tokens.total.reasoning": {
        "none": 71
      },
      "tools.codex_cli": {
        "none": 438
      },
      "tools.grader": {
        "none": 500
      },
      "tools.harness": {
        "none": 10
      },
      "tools.kogen": {
        "none": 18
      },
      "tools.runner": {
        "none": 500
      },
      "tools.toolchains.elixir": {
        "none": 500
      },
      "tools.toolchains.erlang": {
        "none": 500
      },
      "tools.toolchains.node": {
        "none": 500
      },
      "tools.toolchains.other_inventory": {
        "none": 500
      },
      "tools.toolchains.python": {
        "none": 10
      },
      "tools.toolchains.ruby": {
        "none": 500
      },
      "tools.toolchains.rust": {
        "none": 500
      }
    },
    "reconstructable": {
      "sandbox.profile_sha256": {
        "Delivery attempt sandbox.sb on eu-worker": 2,
        "Delivery attempt sandbox.sb on studio": 64,
        "Delivery attempt sandbox.sb on us-worker": 2
      },
      "setup.sandbox_profile_sha256": {
        "Delivery attempt sandbox.sb on eu-worker": 2,
        "Delivery attempt sandbox.sb on studio": 64,
        "Delivery attempt sandbox.sb on us-worker": 2
      },
      "timestamps.cell.end_utc": {
        "Completion manifest or dispatcher END": 2
      }
    }
  },
  "round": "unmapped"
}
```
