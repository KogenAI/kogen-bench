# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 72,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Boundary telemetry not retained": 72
      }
    },
    "circumstances.cap_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Boundary telemetry not retained": 72
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Boundary telemetry not retained": 72
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 72
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Boundary telemetry not retained": 72
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "No matching controller samples retained": 72
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 72,
      "reasons": {
        "Complete per-model billable vector unavailable": 72
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "No dated account-class receipt": 72
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "No per-cell CPU allocation receipt": 72
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "No per-cell CPU receipt": 72
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "No per-cell RAM receipt": 72
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Toolchain version/inventory not recorded": 72
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Toolchain version/inventory not recorded": 72
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Toolchain version/inventory not recorded": 72
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Toolchain version/inventory not recorded": 72
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Toolchain version/inventory not recorded": 72
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Toolchain version/inventory not recorded": 72
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 13,
      "reasons": {
        "Boolean receipt not recorded": 13
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 72,
      "reasons": {
        "No per-cell CPU receipt": 72
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 72,
      "reasons": {
        "No per-cell RAM receipt": 72
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 72,
      "reasons": {
        "No per-cell CPU allocation receipt": 72
      }
    },
    "kogen.best_candidate": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 13,
      "reasons": {
        "Not recorded in available public metadata": 13
      }
    },
    "kogen.landed": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 3,
      "reasons": {
        "Kogen report status absent": 3
      }
    },
    "setup.adapter_harness_sha": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Not recorded in available public metadata": 60
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Dependency source not pinned per cell": 72
      }
    },
    "setup.kogen_sha": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 72
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 13,
      "reasons": {
        "Runner status does not establish normalized stop cause": 13
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Attempt boundary receipts unavailable": 72
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Absolute phase boundary not retained": 72
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Absolute phase boundary not retained": 72
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 3,
      "reasons": {
        "Absolute phase boundary not retained": 3
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 3,
      "reasons": {
        "Absolute phase boundary not retained": 3
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Absolute phase boundary not retained": 72
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Absolute phase boundary not retained": 72
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Absolute phase boundary not retained": 72
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Absolute phase boundary not retained": 72
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Absolute phase boundary not retained": 72
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Absolute phase boundary not retained": 72
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Absolute phase boundary not retained": 72
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Absolute phase boundary not retained": 72
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 3,
      "reasons": {
        "Phase wall not emitted or not separable": 3
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 3,
      "reasons": {
        "Phase wall not emitted or not separable": 3
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 13,
      "reasons": {
        "Phase wall not emitted or not separable": 13
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 50,
      "reasons": {
        "Phase wall not emitted or not separable": 50
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 51,
      "reasons": {
        "Phase wall not emitted or not separable": 51
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 68,
      "reasons": {
        "Phase wall not emitted or not separable": 68
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 72,
      "reasons": {
        "Per-phase token counter not emitted": 72
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 72,
      "reasons": {
        "Per-phase token counter not emitted": 72
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 72,
      "reasons": {
        "Per-phase token counter not emitted": 72
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 72,
      "reasons": {
        "Per-phase token counter not emitted": 72
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 50,
      "reasons": {
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 50,
      "reasons": {
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 50,
      "reasons": {
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 50,
      "reasons": {
        "Per-phase token counter not emitted": 50
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 51,
      "reasons": {
        "Per-phase token counter not emitted": 51
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 51,
      "reasons": {
        "Per-phase token counter not emitted": 51
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 51,
      "reasons": {
        "Per-phase token counter not emitted": 51
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 51,
      "reasons": {
        "Per-phase token counter not emitted": 51
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 72,
      "reasons": {
        "Per-phase token counter not emitted": 72
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 72,
      "reasons": {
        "Per-phase token counter not emitted": 72
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 72,
      "reasons": {
        "Per-phase token counter not emitted": 72
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 72,
      "reasons": {
        "Per-phase token counter not emitted": 72
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Per-phase token counter not emitted": 68
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Per-phase token counter not emitted": 68
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Per-phase token counter not emitted": 68
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 68,
      "reasons": {
        "Per-phase token counter not emitted": 68
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 72
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 72
      }
    },
    "tools.harness": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Not recorded in available public metadata": 60
      }
    },
    "tools.kogen": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 72
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 72
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Toolchain version/inventory not recorded": 72
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Toolchain version/inventory not recorded": 72
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Toolchain version/inventory not recorded": 72
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Toolchain version/inventory not recorded": 72
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Toolchain version/inventory not recorded": 72
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Toolchain version/inventory not recorded": 72
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 72
      },
      "circumstances.cap_start": {
        "none": 72
      },
      "circumstances.concurrent_cells_end": {
        "none": 72
      },
      "circumstances.concurrent_cells_start": {
        "none": 72
      },
      "circumstances.load1_end": {
        "none": 72
      },
      "circumstances.load_samples": {
        "none": 72
      },
      "cost.usd": {
        "none": 72
      },
      "environment.account_class": {
        "none": 72
      },
      "environment.cores": {
        "none": 72
      },
      "environment.cpu_model": {
        "none": 72
      },
      "environment.ram_gib": {
        "none": 72
      },
      "environment.toolchains.elixir": {
        "none": 72
      },
      "environment.toolchains.erlang": {
        "none": 72
      },
      "environment.toolchains.node": {
        "none": 72
      },
      "environment.toolchains.other_inventory": {
        "none": 72
      },
      "environment.toolchains.ruby": {
        "none": 72
      },
      "environment.toolchains.rust": {
        "none": 72
      },
      "grade.tests_ran": {
        "none": 13
      },
      "host.cpu": {
        "none": 72
      },
      "host.ram_gib": {
        "none": 72
      },
      "host.vcpu": {
        "none": 72
      },
      "kogen.best_candidate": {
        "none": 13
      },
      "kogen.landed": {
        "none": 3
      },
      "setup.adapter_harness_sha": {
        "none": 60
      },
      "setup.deps_source": {
        "none": 72
      },
      "setup.kogen_sha": {
        "none": 72
      },
      "stop_reason": {
        "none": 13
      },
      "timestamps.attempts": {
        "none": 72
      },
      "timestamps.phases.develop.end_utc": {
        "none": 72
      },
      "timestamps.phases.develop.start_utc": {
        "none": 72
      },
      "timestamps.phases.gate.end_utc": {
        "none": 3
      },
      "timestamps.phases.gate.start_utc": {
        "none": 3
      },
      "timestamps.phases.grade.end_utc": {
        "none": 72
      },
      "timestamps.phases.grade.start_utc": {
        "none": 72
      },
      "timestamps.phases.plan.end_utc": {
        "none": 72
      },
      "timestamps.phases.plan.start_utc": {
        "none": 72
      },
      "timestamps.phases.review.end_utc": {
        "none": 72
      },
      "timestamps.phases.review.start_utc": {
        "none": 72
      },
      "timestamps.phases.shape.end_utc": {
        "none": 72
      },
      "timestamps.phases.shape.start_utc": {
        "none": 72
      },
      "timing.phases_s.develop": {
        "none": 3
      },
      "timing.phases_s.gate": {
        "none": 3
      },
      "timing.phases_s.grade": {
        "none": 13
      },
      "timing.phases_s.plan": {
        "none": 50
      },
      "timing.phases_s.review": {
        "none": 51
      },
      "timing.phases_s.shape": {
        "none": 68
      },
      "tokens.phases.develop.cached_input": {
        "none": 3
      },
      "tokens.phases.develop.input": {
        "none": 3
      },
      "tokens.phases.develop.output": {
        "none": 3
      },
      "tokens.phases.develop.reasoning": {
        "none": 3
      },
      "tokens.phases.gate.cached_input": {
        "none": 72
      },
      "tokens.phases.gate.input": {
        "none": 72
      },
      "tokens.phases.gate.output": {
        "none": 72
      },
      "tokens.phases.gate.reasoning": {
        "none": 72
      },
      "tokens.phases.plan.cached_input": {
        "none": 50
      },
      "tokens.phases.plan.input": {
        "none": 50
      },
      "tokens.phases.plan.output": {
        "none": 50
      },
      "tokens.phases.plan.reasoning": {
        "none": 50
      },
      "tokens.phases.review.cached_input": {
        "none": 51
      },
      "tokens.phases.review.input": {
        "none": 51
      },
      "tokens.phases.review.output": {
        "none": 51
      },
      "tokens.phases.review.reasoning": {
        "none": 51
      },
      "tokens.phases.setup.cached_input": {
        "none": 72
      },
      "tokens.phases.setup.input": {
        "none": 72
      },
      "tokens.phases.setup.output": {
        "none": 72
      },
      "tokens.phases.setup.reasoning": {
        "none": 72
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
      "tools.codex_cli": {
        "none": 72
      },
      "tools.grader": {
        "none": 72
      },
      "tools.harness": {
        "none": 60
      },
      "tools.kogen": {
        "none": 72
      },
      "tools.runner": {
        "none": 72
      },
      "tools.toolchains.elixir": {
        "none": 72
      },
      "tools.toolchains.erlang": {
        "none": 72
      },
      "tools.toolchains.node": {
        "none": 72
      },
      "tools.toolchains.other_inventory": {
        "none": 72
      },
      "tools.toolchains.ruby": {
        "none": 72
      },
      "tools.toolchains.rust": {
        "none": 72
      }
    },
    "reconstructable": {}
  },
  "round": "r62b"
}
```
