# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 30,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Boundary telemetry not retained": 30
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Boundary telemetry not retained": 30
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 30
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Boundary telemetry not retained": 30
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "No matching controller samples retained": 30
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Complete per-model billable vector unavailable": 30
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "No dated account-class receipt": 30
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "No per-cell CPU allocation receipt": 30
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "No per-cell CPU receipt": 30
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "No per-cell RAM receipt": 30
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Toolchain version/inventory not recorded": 30
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Toolchain version/inventory not recorded": 30
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Toolchain version/inventory not recorded": 30
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Toolchain version/inventory not recorded": 30
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Toolchain version/inventory not recorded": 30
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Toolchain version/inventory not recorded": 30
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 30,
      "reasons": {
        "No per-cell CPU receipt": 30
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 30,
      "reasons": {
        "No per-cell RAM receipt": 30
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 30,
      "reasons": {
        "No per-cell CPU allocation receipt": 30
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Not recorded in available public metadata": 30
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Dependency source not pinned per cell": 30
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Attempt boundary receipts unavailable": 30
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Absolute phase boundary not retained": 30
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Absolute phase boundary not retained": 30
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Absolute phase boundary not retained": 30
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Absolute phase boundary not retained": 30
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Absolute phase boundary not retained": 30
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Absolute phase boundary not retained": 30
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Absolute phase boundary not retained": 30
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Absolute phase boundary not retained": 30
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Absolute phase boundary not retained": 30
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Absolute phase boundary not retained": 30
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Absolute phase boundary not retained": 30
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Absolute phase boundary not retained": 30
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Absolute phase boundary not retained": 30
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Absolute phase boundary not retained": 30
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 30,
      "reasons": {
        "Phase wall not emitted or not separable": 30
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 30,
      "reasons": {
        "Phase wall not emitted or not separable": 30
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 30,
      "reasons": {
        "Phase wall not emitted or not separable": 30
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 30,
      "reasons": {
        "Phase wall not emitted or not separable": 30
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 30,
      "reasons": {
        "Phase wall not emitted or not separable": 30
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
      "count": 30,
      "reasons": {
        "Per-phase token counter not emitted": 30
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Per-phase token counter not emitted": 30
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Per-phase token counter not emitted": 30
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Per-phase token counter not emitted": 30
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Per-phase token counter not emitted": 30
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Per-phase token counter not emitted": 30
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Per-phase token counter not emitted": 30
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Per-phase token counter not emitted": 30
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Per-phase token counter not emitted": 30
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Per-phase token counter not emitted": 30
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Per-phase token counter not emitted": 30
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Per-phase token counter not emitted": 30
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Per-phase token counter not emitted": 30
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Per-phase token counter not emitted": 30
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Per-phase token counter not emitted": 30
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Per-phase token counter not emitted": 30
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Per-phase token counter not emitted": 30
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Per-phase token counter not emitted": 30
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Per-phase token counter not emitted": 30
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Per-phase token counter not emitted": 30
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
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 30
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 30
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 30
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 30,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 30
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 30
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 30
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 30
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Toolchain version/inventory not recorded": 30
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Toolchain version/inventory not recorded": 30
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Toolchain version/inventory not recorded": 30
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Toolchain version/inventory not recorded": 30
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Toolchain version/inventory not recorded": 30
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 30,
      "reasons": {
        "Toolchain version/inventory not recorded": 30
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 30
      },
      "circumstances.concurrent_cells_end": {
        "none": 30
      },
      "circumstances.concurrent_cells_start": {
        "none": 30
      },
      "circumstances.load1_end": {
        "none": 30
      },
      "circumstances.load_samples": {
        "none": 30
      },
      "cost.usd": {
        "none": 30
      },
      "environment.account_class": {
        "none": 30
      },
      "environment.cores": {
        "none": 30
      },
      "environment.cpu_model": {
        "none": 30
      },
      "environment.ram_gib": {
        "none": 30
      },
      "environment.toolchains.elixir": {
        "none": 30
      },
      "environment.toolchains.erlang": {
        "none": 30
      },
      "environment.toolchains.node": {
        "none": 30
      },
      "environment.toolchains.other_inventory": {
        "none": 30
      },
      "environment.toolchains.ruby": {
        "none": 30
      },
      "environment.toolchains.rust": {
        "none": 30
      },
      "host.cpu": {
        "none": 30
      },
      "host.ram_gib": {
        "none": 30
      },
      "host.vcpu": {
        "none": 30
      },
      "recipe": {
        "none": 30
      },
      "setup.deps_source": {
        "none": 30
      },
      "timestamps.attempts": {
        "none": 30
      },
      "timestamps.phases.develop.end_utc": {
        "none": 30
      },
      "timestamps.phases.develop.start_utc": {
        "none": 30
      },
      "timestamps.phases.gate.end_utc": {
        "none": 30
      },
      "timestamps.phases.gate.start_utc": {
        "none": 30
      },
      "timestamps.phases.grade.end_utc": {
        "none": 30
      },
      "timestamps.phases.grade.start_utc": {
        "none": 30
      },
      "timestamps.phases.plan.end_utc": {
        "none": 30
      },
      "timestamps.phases.plan.start_utc": {
        "none": 30
      },
      "timestamps.phases.review.end_utc": {
        "none": 30
      },
      "timestamps.phases.review.start_utc": {
        "none": 30
      },
      "timestamps.phases.setup.end_utc": {
        "none": 30
      },
      "timestamps.phases.setup.start_utc": {
        "none": 30
      },
      "timestamps.phases.shape.end_utc": {
        "none": 30
      },
      "timestamps.phases.shape.start_utc": {
        "none": 30
      },
      "timing.phases_s.develop": {
        "none": 30
      },
      "timing.phases_s.gate": {
        "none": 30
      },
      "timing.phases_s.plan": {
        "none": 30
      },
      "timing.phases_s.review": {
        "none": 30
      },
      "timing.phases_s.setup": {
        "none": 30
      },
      "timing.phases_s.shape": {
        "none": 30
      },
      "tokens.phases.develop.cached_input": {
        "none": 30
      },
      "tokens.phases.develop.input": {
        "none": 30
      },
      "tokens.phases.develop.output": {
        "none": 30
      },
      "tokens.phases.develop.reasoning": {
        "none": 30
      },
      "tokens.phases.gate.cached_input": {
        "none": 30
      },
      "tokens.phases.gate.input": {
        "none": 30
      },
      "tokens.phases.gate.output": {
        "none": 30
      },
      "tokens.phases.gate.reasoning": {
        "none": 30
      },
      "tokens.phases.plan.cached_input": {
        "none": 30
      },
      "tokens.phases.plan.input": {
        "none": 30
      },
      "tokens.phases.plan.output": {
        "none": 30
      },
      "tokens.phases.plan.reasoning": {
        "none": 30
      },
      "tokens.phases.review.cached_input": {
        "none": 30
      },
      "tokens.phases.review.input": {
        "none": 30
      },
      "tokens.phases.review.output": {
        "none": 30
      },
      "tokens.phases.review.reasoning": {
        "none": 30
      },
      "tokens.phases.setup.cached_input": {
        "none": 30
      },
      "tokens.phases.setup.input": {
        "none": 30
      },
      "tokens.phases.setup.output": {
        "none": 30
      },
      "tokens.phases.setup.reasoning": {
        "none": 30
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
      "tokens.total.cached_input": {
        "none": 30
      },
      "tokens.total.input": {
        "none": 30
      },
      "tokens.total.output": {
        "none": 30
      },
      "tokens.total.reasoning": {
        "none": 30
      },
      "tools.codex_cli": {
        "none": 30
      },
      "tools.grader": {
        "none": 30
      },
      "tools.runner": {
        "none": 30
      },
      "tools.toolchains.elixir": {
        "none": 30
      },
      "tools.toolchains.erlang": {
        "none": 30
      },
      "tools.toolchains.node": {
        "none": 30
      },
      "tools.toolchains.other_inventory": {
        "none": 30
      },
      "tools.toolchains.ruby": {
        "none": 30
      },
      "tools.toolchains.rust": {
        "none": 30
      }
    },
    "reconstructable": {}
  },
  "round": "r54"
}
```
