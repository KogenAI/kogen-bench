# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 5,
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
      "count": 5,
      "reasons": {
        "Boundary telemetry not retained": 5
      }
    },
    "circumstances.cap_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Boundary telemetry not retained": 5
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Boundary telemetry not retained": 5
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Boundary telemetry not retained": 5
      }
    },
    "circumstances.dispatcher_id": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Dispatcher receipt unavailable": 5
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Boundary telemetry not retained": 5
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "No matching controller samples retained": 5
      }
    },
    "circumstances.queue": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Queue receipt unavailable": 5
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Complete per-model billable vector unavailable": 4,
        "Not available for ungraded delivery": 1
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not recorded in available public metadata": 1
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "No dated account-class receipt": 5
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "No per-cell CPU allocation receipt": 4,
        "Not available for ungraded delivery": 1
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "No per-cell CPU receipt": 4,
        "Not available for ungraded delivery": 1
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
      "count": 5,
      "reasons": {
        "No per-cell RAM receipt": 4,
        "Not available for ungraded delivery": 1
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 4
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 4
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 4
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 4
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 4
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 4
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 1,
      "reasons": {
        "No official grade in the public snapshot": 1
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 4,
      "reasons": {
        "Boolean receipt not recorded": 3,
        "No official grade in the public snapshot": 1
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 1,
      "reasons": {
        "No official grade in the public snapshot": 1
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 5,
      "reasons": {
        "No per-cell CPU receipt": 4,
        "Not available for ungraded delivery": 1
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 5,
      "reasons": {
        "No per-cell RAM receipt": 4,
        "Not available for ungraded delivery": 1
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 5,
      "reasons": {
        "No per-cell CPU allocation receipt": 4,
        "Not available for ungraded delivery": 1
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 4,
      "reasons": {
        "Invalid/environment cause requires evidence audit": 3,
        "Ungraded delivery needs evidence audit": 1
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 4,
      "reasons": {
        "No audited ITT receipt": 1,
        "No evidence-backed ITT classification": 3
      }
    },
    "kogen.best_candidate": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Not recorded in available public metadata": 4
      }
    },
    "kogen.landed": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Kogen report status absent": 4,
        "Not available for ungraded delivery": 1
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
      "count": 1,
      "reasons": {
        "No official grade in the public snapshot": 1
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Not recorded in available public metadata": 4
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
      "count": 5,
      "reasons": {
        "Dependency source not pinned per cell": 5
      }
    },
    "setup.kogen_sha": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 4,
        "Not available for ungraded delivery": 1
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
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 5,
      "reasons": {
        "No normalized stop receipt": 1,
        "Runner status does not establish normalized stop cause": 4
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Attempt boundary receipts unavailable": 5
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
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Phase wall not emitted or not separable": 4
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Phase wall not emitted or not separable": 4
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Phase wall not emitted or not separable": 3
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Phase wall not emitted or not separable": 4
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Phase wall not emitted or not separable": 4
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Phase wall not emitted or not separable": 4
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Phase wall not emitted or not separable": 3
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
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 4
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 4
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 4
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 4
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 4
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 4
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 4
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 4
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 4
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 4
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 4
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 4
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 4
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 4
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 4
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 4
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 4
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 4
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 4
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 4
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Usage counter unavailable": 1
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Usage counter unavailable": 1
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Usage counter unavailable": 1
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Usage counter unavailable": 1
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 4,
        "Not available for ungraded delivery": 1
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 4,
        "Not available for ungraded delivery": 1
      }
    },
    "tools.kogen": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 4,
        "Not available for ungraded delivery": 1
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 4,
        "Not available for ungraded delivery": 1
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 4
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 4
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 4
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 4
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 4
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 4
      }
    }
  },
  "gap_sources": {
    "lost": {
      "arm": {
        "none": 1
      },
      "circumstances.cap_end": {
        "none": 5
      },
      "circumstances.cap_start": {
        "none": 5
      },
      "circumstances.concurrent_cells_end": {
        "none": 5
      },
      "circumstances.concurrent_cells_start": {
        "none": 5
      },
      "circumstances.dispatcher_id": {
        "none": 5
      },
      "circumstances.load1_end": {
        "none": 5
      },
      "circumstances.load_samples": {
        "none": 5
      },
      "circumstances.queue": {
        "none": 5
      },
      "cost.accounting": {
        "none": 1
      },
      "cost.calculator_version": {
        "none": 1
      },
      "cost.long_context_reconciled": {
        "none": 1
      },
      "cost.price_table_version": {
        "none": 1
      },
      "cost.usd": {
        "none": 5
      },
      "effort.effective": {
        "none": 1
      },
      "environment.account_class": {
        "none": 5
      },
      "environment.cores": {
        "none": 5
      },
      "environment.cpu_model": {
        "none": 5
      },
      "environment.network.allowlist_hosts": {
        "none": 1
      },
      "environment.network.profile": {
        "none": 1
      },
      "environment.ram_gib": {
        "none": 5
      },
      "environment.toolchains.elixir": {
        "none": 5
      },
      "environment.toolchains.erlang": {
        "none": 5
      },
      "environment.toolchains.node": {
        "none": 5
      },
      "environment.toolchains.other_inventory": {
        "none": 5
      },
      "environment.toolchains.ruby": {
        "none": 5
      },
      "environment.toolchains.rust": {
        "none": 5
      },
      "grade.grader": {
        "not re-derivable from the public record": 1
      },
      "grade.tests_ran": {
        "none": 3,
        "not re-derivable from the public record": 1
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 1
      },
      "host.cpu": {
        "none": 5
      },
      "host.ram_gib": {
        "none": 5
      },
      "host.spec_ref": {
        "none": 1
      },
      "host.vcpu": {
        "none": 5
      },
      "itt.class": {
        "none": 4
      },
      "itt.evidence_ref": {
        "none": 4
      },
      "kogen.best_candidate": {
        "none": 5
      },
      "kogen.landed": {
        "none": 5
      },
      "model.effective": {
        "none": 4
      },
      "outcome": {
        "not re-derivable from the public record": 1
      },
      "recipe": {
        "none": 5
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
        "none": 5
      },
      "setup.kogen_sha": {
        "none": 5
      },
      "setup.sandbox_mode": {
        "none": 1
      },
      "setup.task_base.hash": {
        "none": 1
      },
      "setup.task_base.kind": {
        "none": 1
      },
      "stop_reason": {
        "none": 5
      },
      "task.base_repo": {
        "none": 1
      },
      "task.base_revision.hash": {
        "none": 1
      },
      "task.base_revision.kind": {
        "none": 1
      },
      "timestamps.attempts": {
        "none": 5
      },
      "timestamps.phases.develop.end_utc": {
        "none": 5
      },
      "timestamps.phases.develop.start_utc": {
        "none": 5
      },
      "timestamps.phases.gate.end_utc": {
        "none": 5
      },
      "timestamps.phases.gate.start_utc": {
        "none": 5
      },
      "timestamps.phases.grade.end_utc": {
        "none": 5
      },
      "timestamps.phases.grade.start_utc": {
        "none": 5
      },
      "timestamps.phases.plan.end_utc": {
        "none": 5
      },
      "timestamps.phases.plan.start_utc": {
        "none": 5
      },
      "timestamps.phases.review.end_utc": {
        "none": 5
      },
      "timestamps.phases.review.start_utc": {
        "none": 5
      },
      "timestamps.phases.setup.end_utc": {
        "none": 5
      },
      "timestamps.phases.setup.start_utc": {
        "none": 5
      },
      "timestamps.phases.shape.end_utc": {
        "none": 5
      },
      "timestamps.phases.shape.start_utc": {
        "none": 5
      },
      "timing.phases_s.develop": {
        "none": 5
      },
      "timing.phases_s.gate": {
        "none": 5
      },
      "timing.phases_s.grade": {
        "none": 4
      },
      "timing.phases_s.plan": {
        "none": 5
      },
      "timing.phases_s.review": {
        "none": 5
      },
      "timing.phases_s.setup": {
        "none": 5
      },
      "timing.phases_s.shape": {
        "none": 4
      },
      "timing.total_wall_s": {
        "none": 1
      },
      "tokens.phases.develop.cached_input": {
        "none": 5
      },
      "tokens.phases.develop.input": {
        "none": 5
      },
      "tokens.phases.develop.output": {
        "none": 5
      },
      "tokens.phases.develop.reasoning": {
        "none": 5
      },
      "tokens.phases.gate.cached_input": {
        "none": 5
      },
      "tokens.phases.gate.input": {
        "none": 5
      },
      "tokens.phases.gate.output": {
        "none": 5
      },
      "tokens.phases.gate.reasoning": {
        "none": 5
      },
      "tokens.phases.grade.cached_input": {
        "none": 1
      },
      "tokens.phases.grade.input": {
        "none": 1
      },
      "tokens.phases.grade.output": {
        "none": 1
      },
      "tokens.phases.grade.reasoning": {
        "none": 1
      },
      "tokens.phases.plan.cached_input": {
        "none": 5
      },
      "tokens.phases.plan.input": {
        "none": 5
      },
      "tokens.phases.plan.output": {
        "none": 5
      },
      "tokens.phases.plan.reasoning": {
        "none": 5
      },
      "tokens.phases.review.cached_input": {
        "none": 5
      },
      "tokens.phases.review.input": {
        "none": 5
      },
      "tokens.phases.review.output": {
        "none": 5
      },
      "tokens.phases.review.reasoning": {
        "none": 5
      },
      "tokens.phases.setup.cached_input": {
        "none": 5
      },
      "tokens.phases.setup.input": {
        "none": 5
      },
      "tokens.phases.setup.output": {
        "none": 5
      },
      "tokens.phases.setup.reasoning": {
        "none": 5
      },
      "tokens.phases.shape.cached_input": {
        "none": 4
      },
      "tokens.phases.shape.input": {
        "none": 4
      },
      "tokens.phases.shape.output": {
        "none": 4
      },
      "tokens.phases.shape.reasoning": {
        "none": 4
      },
      "tokens.total.cached_input": {
        "none": 1
      },
      "tokens.total.input": {
        "none": 1
      },
      "tokens.total.output": {
        "none": 1
      },
      "tokens.total.reasoning": {
        "none": 1
      },
      "tools.codex_cli": {
        "none": 5
      },
      "tools.grader": {
        "none": 5
      },
      "tools.kogen": {
        "none": 5
      },
      "tools.runner": {
        "none": 5
      },
      "tools.toolchains.elixir": {
        "none": 5
      },
      "tools.toolchains.erlang": {
        "none": 5
      },
      "tools.toolchains.node": {
        "none": 5
      },
      "tools.toolchains.other_inventory": {
        "none": 5
      },
      "tools.toolchains.ruby": {
        "none": 5
      },
      "tools.toolchains.rust": {
        "none": 5
      }
    },
    "reconstructable": {
      "timestamps.cell.end_utc": {
        "Completion manifest or dispatcher END": 1
      }
    }
  },
  "round": "r58b"
}
```
