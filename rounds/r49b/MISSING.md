# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 23,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Boundary telemetry not retained": 23
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Boundary telemetry not retained": 23
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 23
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Boundary telemetry not retained": 23
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "No matching controller samples retained": 23
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Complete per-model billable vector unavailable": 23
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "No dated account-class receipt": 23
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "No per-cell CPU allocation receipt": 23
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "No per-cell CPU receipt": 23
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "No per-cell RAM receipt": 23
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Toolchain version/inventory not recorded": 23
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Toolchain version/inventory not recorded": 23
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Toolchain version/inventory not recorded": 23
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Toolchain version/inventory not recorded": 23
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Toolchain version/inventory not recorded": 23
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Toolchain version/inventory not recorded": 23
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 23,
      "reasons": {
        "No per-cell CPU receipt": 23
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 23,
      "reasons": {
        "No per-cell RAM receipt": 23
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 23,
      "reasons": {
        "No per-cell CPU allocation receipt": 23
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Not recorded in available public metadata": 23
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Dependency source not pinned per cell": 23
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Attempt boundary receipts unavailable": 23
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Absolute phase boundary not retained": 23
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Absolute phase boundary not retained": 23
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Absolute phase boundary not retained": 23
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Absolute phase boundary not retained": 23
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Absolute phase boundary not retained": 23
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Absolute phase boundary not retained": 23
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Absolute phase boundary not retained": 23
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Absolute phase boundary not retained": 23
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Absolute phase boundary not retained": 23
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Absolute phase boundary not retained": 23
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Absolute phase boundary not retained": 23
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Absolute phase boundary not retained": 23
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Absolute phase boundary not retained": 23
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Absolute phase boundary not retained": 23
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 23,
      "reasons": {
        "Phase wall not emitted or not separable": 23
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 23,
      "reasons": {
        "Phase wall not emitted or not separable": 23
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 23,
      "reasons": {
        "Phase wall not emitted or not separable": 23
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 23,
      "reasons": {
        "Phase wall not emitted or not separable": 23
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 23,
      "reasons": {
        "Phase wall not emitted or not separable": 23
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 23,
      "reasons": {
        "Phase wall not emitted or not separable": 23
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Per-phase token counter not emitted": 23
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Per-phase token counter not emitted": 23
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Per-phase token counter not emitted": 23
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Per-phase token counter not emitted": 23
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Per-phase token counter not emitted": 23
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Per-phase token counter not emitted": 23
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Per-phase token counter not emitted": 23
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Per-phase token counter not emitted": 23
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Per-phase token counter not emitted": 23
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Per-phase token counter not emitted": 23
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Per-phase token counter not emitted": 23
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Per-phase token counter not emitted": 23
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Per-phase token counter not emitted": 23
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Per-phase token counter not emitted": 23
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Per-phase token counter not emitted": 23
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Per-phase token counter not emitted": 23
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Per-phase token counter not emitted": 23
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Per-phase token counter not emitted": 23
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Per-phase token counter not emitted": 23
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Per-phase token counter not emitted": 23
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Per-phase token counter not emitted": 23
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Per-phase token counter not emitted": 23
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Per-phase token counter not emitted": 23
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Per-phase token counter not emitted": 23
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 23
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 23
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 23
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 23
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 23
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 23
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 23
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Toolchain version/inventory not recorded": 23
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Toolchain version/inventory not recorded": 23
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Toolchain version/inventory not recorded": 23
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Toolchain version/inventory not recorded": 23
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Toolchain version/inventory not recorded": 23
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Toolchain version/inventory not recorded": 23
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 23
      },
      "circumstances.concurrent_cells_end": {
        "none": 23
      },
      "circumstances.concurrent_cells_start": {
        "none": 23
      },
      "circumstances.load1_end": {
        "none": 23
      },
      "circumstances.load_samples": {
        "none": 23
      },
      "cost.usd": {
        "none": 23
      },
      "environment.account_class": {
        "none": 23
      },
      "environment.cores": {
        "none": 23
      },
      "environment.cpu_model": {
        "none": 23
      },
      "environment.ram_gib": {
        "none": 23
      },
      "environment.toolchains.elixir": {
        "none": 23
      },
      "environment.toolchains.erlang": {
        "none": 23
      },
      "environment.toolchains.node": {
        "none": 23
      },
      "environment.toolchains.other_inventory": {
        "none": 23
      },
      "environment.toolchains.ruby": {
        "none": 23
      },
      "environment.toolchains.rust": {
        "none": 23
      },
      "host.cpu": {
        "none": 23
      },
      "host.ram_gib": {
        "none": 23
      },
      "host.vcpu": {
        "none": 23
      },
      "recipe": {
        "none": 23
      },
      "setup.deps_source": {
        "none": 23
      },
      "timestamps.attempts": {
        "none": 23
      },
      "timestamps.phases.develop.end_utc": {
        "none": 23
      },
      "timestamps.phases.develop.start_utc": {
        "none": 23
      },
      "timestamps.phases.gate.end_utc": {
        "none": 23
      },
      "timestamps.phases.gate.start_utc": {
        "none": 23
      },
      "timestamps.phases.grade.end_utc": {
        "none": 23
      },
      "timestamps.phases.grade.start_utc": {
        "none": 23
      },
      "timestamps.phases.plan.end_utc": {
        "none": 23
      },
      "timestamps.phases.plan.start_utc": {
        "none": 23
      },
      "timestamps.phases.review.end_utc": {
        "none": 23
      },
      "timestamps.phases.review.start_utc": {
        "none": 23
      },
      "timestamps.phases.setup.end_utc": {
        "none": 23
      },
      "timestamps.phases.setup.start_utc": {
        "none": 23
      },
      "timestamps.phases.shape.end_utc": {
        "none": 23
      },
      "timestamps.phases.shape.start_utc": {
        "none": 23
      },
      "timing.phases_s.develop": {
        "none": 23
      },
      "timing.phases_s.gate": {
        "none": 23
      },
      "timing.phases_s.plan": {
        "none": 23
      },
      "timing.phases_s.review": {
        "none": 23
      },
      "timing.phases_s.setup": {
        "none": 23
      },
      "timing.phases_s.shape": {
        "none": 23
      },
      "tokens.phases.develop.cached_input": {
        "none": 23
      },
      "tokens.phases.develop.input": {
        "none": 23
      },
      "tokens.phases.develop.output": {
        "none": 23
      },
      "tokens.phases.develop.reasoning": {
        "none": 23
      },
      "tokens.phases.gate.cached_input": {
        "none": 23
      },
      "tokens.phases.gate.input": {
        "none": 23
      },
      "tokens.phases.gate.output": {
        "none": 23
      },
      "tokens.phases.gate.reasoning": {
        "none": 23
      },
      "tokens.phases.plan.cached_input": {
        "none": 23
      },
      "tokens.phases.plan.input": {
        "none": 23
      },
      "tokens.phases.plan.output": {
        "none": 23
      },
      "tokens.phases.plan.reasoning": {
        "none": 23
      },
      "tokens.phases.review.cached_input": {
        "none": 23
      },
      "tokens.phases.review.input": {
        "none": 23
      },
      "tokens.phases.review.output": {
        "none": 23
      },
      "tokens.phases.review.reasoning": {
        "none": 23
      },
      "tokens.phases.setup.cached_input": {
        "none": 23
      },
      "tokens.phases.setup.input": {
        "none": 23
      },
      "tokens.phases.setup.output": {
        "none": 23
      },
      "tokens.phases.setup.reasoning": {
        "none": 23
      },
      "tokens.phases.shape.cached_input": {
        "none": 23
      },
      "tokens.phases.shape.input": {
        "none": 23
      },
      "tokens.phases.shape.output": {
        "none": 23
      },
      "tokens.phases.shape.reasoning": {
        "none": 23
      },
      "tokens.total.cached_input": {
        "none": 23
      },
      "tokens.total.input": {
        "none": 23
      },
      "tokens.total.output": {
        "none": 23
      },
      "tokens.total.reasoning": {
        "none": 23
      },
      "tools.codex_cli": {
        "none": 23
      },
      "tools.grader": {
        "none": 23
      },
      "tools.runner": {
        "none": 23
      },
      "tools.toolchains.elixir": {
        "none": 23
      },
      "tools.toolchains.erlang": {
        "none": 23
      },
      "tools.toolchains.node": {
        "none": 23
      },
      "tools.toolchains.other_inventory": {
        "none": 23
      },
      "tools.toolchains.ruby": {
        "none": 23
      },
      "tools.toolchains.rust": {
        "none": 23
      }
    },
    "reconstructable": {}
  },
  "round": "r49b"
}
```
