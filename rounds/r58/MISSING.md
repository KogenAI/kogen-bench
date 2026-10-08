# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 93,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Boundary telemetry not retained": 93
      }
    },
    "circumstances.cap_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Boundary telemetry not retained": 93
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Boundary telemetry not retained": 93
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Boundary telemetry not retained": 93
      }
    },
    "circumstances.dispatcher_id": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Dispatcher receipt unavailable": 93
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Boundary telemetry not retained": 93
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "No matching controller samples retained": 93
      }
    },
    "circumstances.queue": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Queue receipt unavailable": 93
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 70,
      "reasons": {
        "Complete per-model billable vector unavailable": 70
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
      "count": 93,
      "reasons": {
        "No dated account-class receipt": 93
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "No per-cell CPU allocation receipt": 93
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "No per-cell CPU receipt": 93
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
      "count": 93,
      "reasons": {
        "No per-cell RAM receipt": 93
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Toolchain version/inventory not recorded": 93
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Toolchain version/inventory not recorded": 93
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Toolchain version/inventory not recorded": 93
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Toolchain version/inventory not recorded": 93
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Toolchain version/inventory not recorded": 93
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Toolchain version/inventory not recorded": 93
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 4,
      "reasons": {
        "Not recorded in available public metadata": 4
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 36,
      "reasons": {
        "Boolean receipt not recorded": 36
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 93,
      "reasons": {
        "No per-cell CPU receipt": 93
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 93,
      "reasons": {
        "No per-cell RAM receipt": 93
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 93,
      "reasons": {
        "No per-cell CPU allocation receipt": 93
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 36,
      "reasons": {
        "Invalid/environment cause requires evidence audit": 36
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 36,
      "reasons": {
        "No evidence-backed ITT classification": 36
      }
    },
    "kogen.best_candidate": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Not recorded in available public metadata": 36
      }
    },
    "kogen.landed": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 36,
      "reasons": {
        "Kogen report status absent": 36
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
        "Official result outside standard outcome classes": 4
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Not recorded in available public metadata": 6
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
      "count": 4,
      "reasons": {
        "Public sandbox profile fingerprint not yet captured": 4
      }
    },
    "setup.adapter_harness_sha": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 26,
      "reasons": {
        "Not recorded in available public metadata": 26
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Dependency source not pinned per cell": 93
      }
    },
    "setup.kogen_sha": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 70,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 70
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
      "count": 4,
      "reasons": {
        "Public sandbox profile fingerprint not yet captured": 4
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 1
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Original base revision type not recorded per cell": 1
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 70,
      "reasons": {
        "Runner status does not establish normalized stop cause": 70
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 21,
      "reasons": {
        "Value withheld by PRIVATE.md": 21
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 1
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Original base revision type not recorded per cell": 1
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Attempt boundary receipts unavailable": 93
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 70,
      "reasons": {
        "Absolute phase boundary not retained": 70
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 70,
      "reasons": {
        "Absolute phase boundary not retained": 70
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Absolute phase boundary not retained": 93
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Absolute phase boundary not retained": 93
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Absolute phase boundary not retained": 93
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Absolute phase boundary not retained": 93
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Absolute phase boundary not retained": 93
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Absolute phase boundary not retained": 93
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Absolute phase boundary not retained": 93
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Absolute phase boundary not retained": 93
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Absolute phase boundary not retained": 93
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Absolute phase boundary not retained": 93
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Absolute phase boundary not retained": 93
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Absolute phase boundary not retained": 93
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 53,
      "reasons": {
        "Phase wall not emitted or not separable": 53
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 93,
      "reasons": {
        "Phase wall not emitted or not separable": 93
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 36,
      "reasons": {
        "Phase wall not emitted or not separable": 36
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 83,
      "reasons": {
        "Phase wall not emitted or not separable": 83
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 83,
      "reasons": {
        "Phase wall not emitted or not separable": 83
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 93,
      "reasons": {
        "Phase wall not emitted or not separable": 93
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 62,
      "reasons": {
        "Phase wall not emitted or not separable": 62
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 53,
      "reasons": {
        "Per-phase token counter not emitted": 53
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 53,
      "reasons": {
        "Per-phase token counter not emitted": 53
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 53,
      "reasons": {
        "Per-phase token counter not emitted": 53
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 53,
      "reasons": {
        "Per-phase token counter not emitted": 53
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 93,
      "reasons": {
        "Per-phase token counter not emitted": 93
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 93,
      "reasons": {
        "Per-phase token counter not emitted": 93
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 93,
      "reasons": {
        "Per-phase token counter not emitted": 93
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 93,
      "reasons": {
        "Per-phase token counter not emitted": 93
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 83,
      "reasons": {
        "Per-phase token counter not emitted": 83
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 83,
      "reasons": {
        "Per-phase token counter not emitted": 83
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 83,
      "reasons": {
        "Per-phase token counter not emitted": 83
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 83,
      "reasons": {
        "Per-phase token counter not emitted": 83
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 83,
      "reasons": {
        "Per-phase token counter not emitted": 83
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 83,
      "reasons": {
        "Per-phase token counter not emitted": 83
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 83,
      "reasons": {
        "Per-phase token counter not emitted": 83
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 83,
      "reasons": {
        "Per-phase token counter not emitted": 83
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 93,
      "reasons": {
        "Per-phase token counter not emitted": 93
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 93,
      "reasons": {
        "Per-phase token counter not emitted": 93
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 93,
      "reasons": {
        "Per-phase token counter not emitted": 93
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 93,
      "reasons": {
        "Per-phase token counter not emitted": 93
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 62,
      "reasons": {
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 62,
      "reasons": {
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 62,
      "reasons": {
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 62,
      "reasons": {
        "Per-phase token counter not emitted": 62
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Numeric counter not recorded": 4
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Numeric counter not recorded": 4
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Numeric counter not recorded": 4
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 4,
      "reasons": {
        "Numeric counter not recorded": 4
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 70,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 70
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 93
      }
    },
    "tools.harness": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 26,
      "reasons": {
        "Not recorded in available public metadata": 26
      }
    },
    "tools.kogen": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 70,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 70
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 93
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Toolchain version/inventory not recorded": 93
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Toolchain version/inventory not recorded": 93
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Toolchain version/inventory not recorded": 93
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Toolchain version/inventory not recorded": 93
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Toolchain version/inventory not recorded": 93
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 93,
      "reasons": {
        "Toolchain version/inventory not recorded": 93
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 93
      },
      "circumstances.cap_start": {
        "none": 93
      },
      "circumstances.concurrent_cells_end": {
        "none": 93
      },
      "circumstances.concurrent_cells_start": {
        "none": 93
      },
      "circumstances.dispatcher_id": {
        "none": 93
      },
      "circumstances.load1_end": {
        "none": 93
      },
      "circumstances.load_samples": {
        "none": 93
      },
      "circumstances.queue": {
        "none": 93
      },
      "cost.usd": {
        "none": 70
      },
      "effort.effective": {
        "none": 4
      },
      "environment.account_class": {
        "none": 93
      },
      "environment.cores": {
        "none": 93
      },
      "environment.cpu_model": {
        "none": 93
      },
      "environment.network.allowlist_hosts": {
        "none": 4
      },
      "environment.network.profile": {
        "none": 4
      },
      "environment.ram_gib": {
        "none": 93
      },
      "environment.toolchains.elixir": {
        "none": 93
      },
      "environment.toolchains.erlang": {
        "none": 93
      },
      "environment.toolchains.node": {
        "none": 93
      },
      "environment.toolchains.other_inventory": {
        "none": 93
      },
      "environment.toolchains.ruby": {
        "none": 93
      },
      "environment.toolchains.rust": {
        "none": 93
      },
      "grade.grader": {
        "none": 4
      },
      "grade.tests_ran": {
        "none": 36
      },
      "host.cpu": {
        "none": 93
      },
      "host.ram_gib": {
        "none": 93
      },
      "host.vcpu": {
        "none": 93
      },
      "itt.class": {
        "none": 36
      },
      "itt.evidence_ref": {
        "none": 36
      },
      "kogen.best_candidate": {
        "none": 36
      },
      "kogen.landed": {
        "none": 36
      },
      "model.effective": {
        "none": 4
      },
      "outcome": {
        "none": 4
      },
      "recipe": {
        "none": 6
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
      "setup.adapter_harness_sha": {
        "none": 26
      },
      "setup.deps_source": {
        "none": 93
      },
      "setup.kogen_sha": {
        "none": 70
      },
      "setup.sandbox_mode": {
        "none": 4
      },
      "setup.task_base.hash": {
        "none": 1
      },
      "setup.task_base.kind": {
        "none": 1
      },
      "stop_reason": {
        "none": 70
      },
      "task.base_repo": {
        "none": 21
      },
      "task.base_revision.hash": {
        "none": 1
      },
      "task.base_revision.kind": {
        "none": 1
      },
      "timestamps.attempts": {
        "none": 93
      },
      "timestamps.phases.develop.end_utc": {
        "none": 70
      },
      "timestamps.phases.develop.start_utc": {
        "none": 70
      },
      "timestamps.phases.gate.end_utc": {
        "none": 93
      },
      "timestamps.phases.gate.start_utc": {
        "none": 93
      },
      "timestamps.phases.grade.end_utc": {
        "none": 93
      },
      "timestamps.phases.grade.start_utc": {
        "none": 93
      },
      "timestamps.phases.plan.end_utc": {
        "none": 93
      },
      "timestamps.phases.plan.start_utc": {
        "none": 93
      },
      "timestamps.phases.review.end_utc": {
        "none": 93
      },
      "timestamps.phases.review.start_utc": {
        "none": 93
      },
      "timestamps.phases.setup.end_utc": {
        "none": 93
      },
      "timestamps.phases.setup.start_utc": {
        "none": 93
      },
      "timestamps.phases.shape.end_utc": {
        "none": 93
      },
      "timestamps.phases.shape.start_utc": {
        "none": 93
      },
      "timing.phases_s.develop": {
        "none": 53
      },
      "timing.phases_s.gate": {
        "none": 93
      },
      "timing.phases_s.grade": {
        "none": 36
      },
      "timing.phases_s.plan": {
        "none": 83
      },
      "timing.phases_s.review": {
        "none": 83
      },
      "timing.phases_s.setup": {
        "none": 93
      },
      "timing.phases_s.shape": {
        "none": 62
      },
      "tokens.phases.develop.cached_input": {
        "none": 53
      },
      "tokens.phases.develop.input": {
        "none": 53
      },
      "tokens.phases.develop.output": {
        "none": 53
      },
      "tokens.phases.develop.reasoning": {
        "none": 53
      },
      "tokens.phases.gate.cached_input": {
        "none": 93
      },
      "tokens.phases.gate.input": {
        "none": 93
      },
      "tokens.phases.gate.output": {
        "none": 93
      },
      "tokens.phases.gate.reasoning": {
        "none": 93
      },
      "tokens.phases.plan.cached_input": {
        "none": 83
      },
      "tokens.phases.plan.input": {
        "none": 83
      },
      "tokens.phases.plan.output": {
        "none": 83
      },
      "tokens.phases.plan.reasoning": {
        "none": 83
      },
      "tokens.phases.review.cached_input": {
        "none": 83
      },
      "tokens.phases.review.input": {
        "none": 83
      },
      "tokens.phases.review.output": {
        "none": 83
      },
      "tokens.phases.review.reasoning": {
        "none": 83
      },
      "tokens.phases.setup.cached_input": {
        "none": 93
      },
      "tokens.phases.setup.input": {
        "none": 93
      },
      "tokens.phases.setup.output": {
        "none": 93
      },
      "tokens.phases.setup.reasoning": {
        "none": 93
      },
      "tokens.phases.shape.cached_input": {
        "none": 62
      },
      "tokens.phases.shape.input": {
        "none": 62
      },
      "tokens.phases.shape.output": {
        "none": 62
      },
      "tokens.phases.shape.reasoning": {
        "none": 62
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
        "none": 70
      },
      "tools.grader": {
        "none": 93
      },
      "tools.harness": {
        "none": 26
      },
      "tools.kogen": {
        "none": 70
      },
      "tools.runner": {
        "none": 93
      },
      "tools.toolchains.elixir": {
        "none": 93
      },
      "tools.toolchains.erlang": {
        "none": 93
      },
      "tools.toolchains.node": {
        "none": 93
      },
      "tools.toolchains.other_inventory": {
        "none": 93
      },
      "tools.toolchains.ruby": {
        "none": 93
      },
      "tools.toolchains.rust": {
        "none": 93
      }
    },
    "reconstructable": {
      "sandbox.profile_sha256": {
        "Delivery attempt sandbox.sb on us-worker": 4
      },
      "setup.sandbox_profile_sha256": {
        "Delivery attempt sandbox.sb on us-worker": 4
      }
    }
  },
  "round": "r58"
}
```
