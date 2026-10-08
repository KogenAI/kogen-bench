# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 34,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Boundary telemetry not retained": 34
      }
    },
    "circumstances.cap_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Boundary telemetry not retained": 20
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Boundary telemetry not retained": 34
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 34
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Boundary telemetry not retained": 34
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "No matching controller samples retained": 34
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 20,
      "reasons": {
        "Complete per-model billable vector unavailable": 20
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "No dated account-class receipt": 34
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "No per-cell CPU allocation receipt": 34
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "No per-cell CPU receipt": 34
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "No per-cell RAM receipt": 34
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Toolchain version/inventory not recorded": 34
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Toolchain version/inventory not recorded": 34
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Toolchain version/inventory not recorded": 34
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Toolchain version/inventory not recorded": 34
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Toolchain version/inventory not recorded": 34
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Toolchain version/inventory not recorded": 34
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 6,
      "reasons": {
        "Boolean receipt not recorded": 6
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 34,
      "reasons": {
        "No per-cell CPU receipt": 34
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 34,
      "reasons": {
        "No per-cell RAM receipt": 34
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 34,
      "reasons": {
        "No per-cell CPU allocation receipt": 34
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 6,
      "reasons": {
        "Invalid/environment cause requires evidence audit": 6
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 6,
      "reasons": {
        "No evidence-backed ITT classification": 6
      }
    },
    "kogen.best_candidate": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Not recorded in available public metadata": 6
      }
    },
    "kogen.landed": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 4,
      "reasons": {
        "Kogen report status absent": 4
      }
    },
    "setup.adapter_harness_sha": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 19,
      "reasons": {
        "Not recorded in available public metadata": 19
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Dependency source not pinned per cell": 34
      }
    },
    "setup.kogen_sha": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 20
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 6,
      "reasons": {
        "Runner status does not establish normalized stop cause": 6
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Value withheld by PRIVATE.md": 10
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Attempt boundary receipts unavailable": 34
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Absolute phase boundary not retained": 20
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Absolute phase boundary not retained": 20
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Absolute phase boundary not retained": 18
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Absolute phase boundary not retained": 18
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Absolute phase boundary not retained": 34
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Absolute phase boundary not retained": 34
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Absolute phase boundary not retained": 34
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Absolute phase boundary not retained": 34
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Absolute phase boundary not retained": 34
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Absolute phase boundary not retained": 34
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 14,
      "reasons": {
        "Absolute phase boundary not retained": 14
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 14,
      "reasons": {
        "Absolute phase boundary not retained": 14
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Absolute phase boundary not retained": 34
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Absolute phase boundary not retained": 34
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 18,
      "reasons": {
        "Phase wall not emitted or not separable": 18
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 18,
      "reasons": {
        "Phase wall not emitted or not separable": 18
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "Phase wall not emitted or not separable": 6
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 33,
      "reasons": {
        "Phase wall not emitted or not separable": 33
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 33,
      "reasons": {
        "Phase wall not emitted or not separable": 33
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 14,
      "reasons": {
        "Phase wall not emitted or not separable": 14
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 30,
      "reasons": {
        "Phase wall not emitted or not separable": 30
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 18,
      "reasons": {
        "Per-phase token counter not emitted": 18
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 18,
      "reasons": {
        "Per-phase token counter not emitted": 18
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 18,
      "reasons": {
        "Per-phase token counter not emitted": 18
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 18,
      "reasons": {
        "Per-phase token counter not emitted": 18
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Per-phase token counter not emitted": 34
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Per-phase token counter not emitted": 34
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Per-phase token counter not emitted": 34
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Per-phase token counter not emitted": 34
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 33,
      "reasons": {
        "Per-phase token counter not emitted": 33
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 33,
      "reasons": {
        "Per-phase token counter not emitted": 33
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 33,
      "reasons": {
        "Per-phase token counter not emitted": 33
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 33,
      "reasons": {
        "Per-phase token counter not emitted": 33
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 33,
      "reasons": {
        "Per-phase token counter not emitted": 33
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 33,
      "reasons": {
        "Per-phase token counter not emitted": 33
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 33,
      "reasons": {
        "Per-phase token counter not emitted": 33
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 33,
      "reasons": {
        "Per-phase token counter not emitted": 33
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Per-phase token counter not emitted": 34
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Per-phase token counter not emitted": 34
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Per-phase token counter not emitted": 34
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 34,
      "reasons": {
        "Per-phase token counter not emitted": 34
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Per-phase token counter not emitted": 30
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Per-phase token counter not emitted": 30
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Per-phase token counter not emitted": 30
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Per-phase token counter not emitted": 30
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 20
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 34
      }
    },
    "tools.harness": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 19,
      "reasons": {
        "Not recorded in available public metadata": 19
      }
    },
    "tools.kogen": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 20
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 34
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Toolchain version/inventory not recorded": 34
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Toolchain version/inventory not recorded": 34
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Toolchain version/inventory not recorded": 34
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Toolchain version/inventory not recorded": 34
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Toolchain version/inventory not recorded": 34
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 34,
      "reasons": {
        "Toolchain version/inventory not recorded": 34
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 34
      },
      "circumstances.cap_start": {
        "none": 20
      },
      "circumstances.concurrent_cells_end": {
        "none": 34
      },
      "circumstances.concurrent_cells_start": {
        "none": 34
      },
      "circumstances.load1_end": {
        "none": 34
      },
      "circumstances.load_samples": {
        "none": 34
      },
      "cost.usd": {
        "none": 20
      },
      "environment.account_class": {
        "none": 34
      },
      "environment.cores": {
        "none": 34
      },
      "environment.cpu_model": {
        "none": 34
      },
      "environment.ram_gib": {
        "none": 34
      },
      "environment.toolchains.elixir": {
        "none": 34
      },
      "environment.toolchains.erlang": {
        "none": 34
      },
      "environment.toolchains.node": {
        "none": 34
      },
      "environment.toolchains.other_inventory": {
        "none": 34
      },
      "environment.toolchains.ruby": {
        "none": 34
      },
      "environment.toolchains.rust": {
        "none": 34
      },
      "grade.tests_ran": {
        "none": 6
      },
      "host.cpu": {
        "none": 34
      },
      "host.ram_gib": {
        "none": 34
      },
      "host.vcpu": {
        "none": 34
      },
      "itt.class": {
        "none": 6
      },
      "itt.evidence_ref": {
        "none": 6
      },
      "kogen.best_candidate": {
        "none": 6
      },
      "kogen.landed": {
        "none": 4
      },
      "setup.adapter_harness_sha": {
        "none": 19
      },
      "setup.deps_source": {
        "none": 34
      },
      "setup.kogen_sha": {
        "none": 20
      },
      "stop_reason": {
        "none": 6
      },
      "task.base_repo": {
        "none": 10
      },
      "timestamps.attempts": {
        "none": 34
      },
      "timestamps.phases.develop.end_utc": {
        "none": 20
      },
      "timestamps.phases.develop.start_utc": {
        "none": 20
      },
      "timestamps.phases.gate.end_utc": {
        "none": 18
      },
      "timestamps.phases.gate.start_utc": {
        "none": 18
      },
      "timestamps.phases.grade.end_utc": {
        "none": 34
      },
      "timestamps.phases.grade.start_utc": {
        "none": 34
      },
      "timestamps.phases.plan.end_utc": {
        "none": 34
      },
      "timestamps.phases.plan.start_utc": {
        "none": 34
      },
      "timestamps.phases.review.end_utc": {
        "none": 34
      },
      "timestamps.phases.review.start_utc": {
        "none": 34
      },
      "timestamps.phases.setup.end_utc": {
        "none": 14
      },
      "timestamps.phases.setup.start_utc": {
        "none": 14
      },
      "timestamps.phases.shape.end_utc": {
        "none": 34
      },
      "timestamps.phases.shape.start_utc": {
        "none": 34
      },
      "timing.phases_s.develop": {
        "none": 18
      },
      "timing.phases_s.gate": {
        "none": 18
      },
      "timing.phases_s.grade": {
        "none": 6
      },
      "timing.phases_s.plan": {
        "none": 33
      },
      "timing.phases_s.review": {
        "none": 33
      },
      "timing.phases_s.setup": {
        "none": 14
      },
      "timing.phases_s.shape": {
        "none": 30
      },
      "tokens.phases.develop.cached_input": {
        "none": 18
      },
      "tokens.phases.develop.input": {
        "none": 18
      },
      "tokens.phases.develop.output": {
        "none": 18
      },
      "tokens.phases.develop.reasoning": {
        "none": 18
      },
      "tokens.phases.gate.cached_input": {
        "none": 34
      },
      "tokens.phases.gate.input": {
        "none": 34
      },
      "tokens.phases.gate.output": {
        "none": 34
      },
      "tokens.phases.gate.reasoning": {
        "none": 34
      },
      "tokens.phases.plan.cached_input": {
        "none": 33
      },
      "tokens.phases.plan.input": {
        "none": 33
      },
      "tokens.phases.plan.output": {
        "none": 33
      },
      "tokens.phases.plan.reasoning": {
        "none": 33
      },
      "tokens.phases.review.cached_input": {
        "none": 33
      },
      "tokens.phases.review.input": {
        "none": 33
      },
      "tokens.phases.review.output": {
        "none": 33
      },
      "tokens.phases.review.reasoning": {
        "none": 33
      },
      "tokens.phases.setup.cached_input": {
        "none": 34
      },
      "tokens.phases.setup.input": {
        "none": 34
      },
      "tokens.phases.setup.output": {
        "none": 34
      },
      "tokens.phases.setup.reasoning": {
        "none": 34
      },
      "tokens.phases.shape.cached_input": {
        "none": 30
      },
      "tokens.phases.shape.input": {
        "none": 30
      },
      "tokens.phases.shape.output": {
        "none": 30
      },
      "tokens.phases.shape.reasoning": {
        "none": 30
      },
      "tools.codex_cli": {
        "none": 20
      },
      "tools.grader": {
        "none": 34
      },
      "tools.harness": {
        "none": 19
      },
      "tools.kogen": {
        "none": 20
      },
      "tools.runner": {
        "none": 34
      },
      "tools.toolchains.elixir": {
        "none": 34
      },
      "tools.toolchains.erlang": {
        "none": 34
      },
      "tools.toolchains.node": {
        "none": 34
      },
      "tools.toolchains.other_inventory": {
        "none": 34
      },
      "tools.toolchains.ruby": {
        "none": 34
      },
      "tools.toolchains.rust": {
        "none": 34
      }
    },
    "reconstructable": {}
  },
  "round": "r61"
}
```
