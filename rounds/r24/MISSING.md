# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 40,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Boundary telemetry not retained": 40
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Boundary telemetry not retained": 20
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 20
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Boundary telemetry not retained": 40
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "No matching controller samples retained": 20
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Complete per-model billable vector unavailable": 40
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "No dated account-class receipt": 20
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "No per-cell CPU allocation receipt": 40
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "No per-cell CPU receipt": 40
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "No per-cell kernel receipt": 20
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "No per-cell RAM receipt": 40
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Toolchain version/inventory not recorded": 40
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Toolchain version/inventory not recorded": 40
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Toolchain version/inventory not recorded": 40
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Toolchain version/inventory not recorded": 40
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Toolchain version/inventory not recorded": 40
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Toolchain version/inventory not recorded": 40
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 40,
      "reasons": {
        "No per-cell CPU receipt": 40
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 20,
      "reasons": {
        "No per-cell kernel receipt": 20
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 40,
      "reasons": {
        "No per-cell RAM receipt": 40
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 40,
      "reasons": {
        "No per-cell CPU allocation receipt": 40
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Not recorded in available public metadata": 40
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Dependency source not pinned per cell": 40
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Attempt boundary receipts unavailable": 40
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Absolute phase boundary not retained": 40
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 40,
      "reasons": {
        "Phase wall not emitted or not separable": 40
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 40,
      "reasons": {
        "Phase wall not emitted or not separable": 40
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 40,
      "reasons": {
        "Phase wall not emitted or not separable": 40
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 40,
      "reasons": {
        "Phase wall not emitted or not separable": 40
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 40,
      "reasons": {
        "Phase wall not emitted or not separable": 40
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 40,
      "reasons": {
        "Phase wall not emitted or not separable": 40
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Per-phase token counter not emitted": 40
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Per-phase token counter not emitted": 40
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Per-phase token counter not emitted": 40
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Per-phase token counter not emitted": 40
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Per-phase token counter not emitted": 40
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Per-phase token counter not emitted": 40
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Per-phase token counter not emitted": 40
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Per-phase token counter not emitted": 40
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Per-phase token counter not emitted": 40
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Per-phase token counter not emitted": 40
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Per-phase token counter not emitted": 40
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Per-phase token counter not emitted": 40
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Per-phase token counter not emitted": 40
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Per-phase token counter not emitted": 40
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Per-phase token counter not emitted": 40
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Per-phase token counter not emitted": 40
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Per-phase token counter not emitted": 40
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Per-phase token counter not emitted": 40
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Per-phase token counter not emitted": 40
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Per-phase token counter not emitted": 40
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Per-phase token counter not emitted": 40
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Per-phase token counter not emitted": 40
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Per-phase token counter not emitted": 40
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Per-phase token counter not emitted": 40
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 40
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 40
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 40
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 40,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 40
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 40
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 40
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 40
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Toolchain version/inventory not recorded": 40
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Toolchain version/inventory not recorded": 40
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Toolchain version/inventory not recorded": 40
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Toolchain version/inventory not recorded": 40
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Toolchain version/inventory not recorded": 40
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 40,
      "reasons": {
        "Toolchain version/inventory not recorded": 40
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 40
      },
      "circumstances.concurrent_cells_end": {
        "none": 20
      },
      "circumstances.concurrent_cells_start": {
        "none": 20
      },
      "circumstances.load1_end": {
        "none": 40
      },
      "circumstances.load_samples": {
        "none": 20
      },
      "cost.usd": {
        "none": 40
      },
      "environment.account_class": {
        "none": 20
      },
      "environment.cores": {
        "none": 40
      },
      "environment.cpu_model": {
        "none": 40
      },
      "environment.kernel": {
        "none": 20
      },
      "environment.ram_gib": {
        "none": 40
      },
      "environment.toolchains.elixir": {
        "none": 40
      },
      "environment.toolchains.erlang": {
        "none": 40
      },
      "environment.toolchains.node": {
        "none": 40
      },
      "environment.toolchains.other_inventory": {
        "none": 40
      },
      "environment.toolchains.ruby": {
        "none": 40
      },
      "environment.toolchains.rust": {
        "none": 40
      },
      "host.cpu": {
        "none": 40
      },
      "host.kernel": {
        "none": 20
      },
      "host.ram_gib": {
        "none": 40
      },
      "host.vcpu": {
        "none": 40
      },
      "recipe": {
        "none": 40
      },
      "setup.deps_source": {
        "none": 40
      },
      "timestamps.attempts": {
        "none": 40
      },
      "timestamps.phases.develop.end_utc": {
        "none": 40
      },
      "timestamps.phases.develop.start_utc": {
        "none": 40
      },
      "timestamps.phases.gate.end_utc": {
        "none": 40
      },
      "timestamps.phases.gate.start_utc": {
        "none": 40
      },
      "timestamps.phases.grade.end_utc": {
        "none": 40
      },
      "timestamps.phases.grade.start_utc": {
        "none": 40
      },
      "timestamps.phases.plan.end_utc": {
        "none": 40
      },
      "timestamps.phases.plan.start_utc": {
        "none": 40
      },
      "timestamps.phases.review.end_utc": {
        "none": 40
      },
      "timestamps.phases.review.start_utc": {
        "none": 40
      },
      "timestamps.phases.setup.end_utc": {
        "none": 40
      },
      "timestamps.phases.setup.start_utc": {
        "none": 40
      },
      "timestamps.phases.shape.end_utc": {
        "none": 40
      },
      "timestamps.phases.shape.start_utc": {
        "none": 40
      },
      "timing.phases_s.develop": {
        "none": 40
      },
      "timing.phases_s.gate": {
        "none": 40
      },
      "timing.phases_s.plan": {
        "none": 40
      },
      "timing.phases_s.review": {
        "none": 40
      },
      "timing.phases_s.setup": {
        "none": 40
      },
      "timing.phases_s.shape": {
        "none": 40
      },
      "tokens.phases.develop.cached_input": {
        "none": 40
      },
      "tokens.phases.develop.input": {
        "none": 40
      },
      "tokens.phases.develop.output": {
        "none": 40
      },
      "tokens.phases.develop.reasoning": {
        "none": 40
      },
      "tokens.phases.gate.cached_input": {
        "none": 40
      },
      "tokens.phases.gate.input": {
        "none": 40
      },
      "tokens.phases.gate.output": {
        "none": 40
      },
      "tokens.phases.gate.reasoning": {
        "none": 40
      },
      "tokens.phases.plan.cached_input": {
        "none": 40
      },
      "tokens.phases.plan.input": {
        "none": 40
      },
      "tokens.phases.plan.output": {
        "none": 40
      },
      "tokens.phases.plan.reasoning": {
        "none": 40
      },
      "tokens.phases.review.cached_input": {
        "none": 40
      },
      "tokens.phases.review.input": {
        "none": 40
      },
      "tokens.phases.review.output": {
        "none": 40
      },
      "tokens.phases.review.reasoning": {
        "none": 40
      },
      "tokens.phases.setup.cached_input": {
        "none": 40
      },
      "tokens.phases.setup.input": {
        "none": 40
      },
      "tokens.phases.setup.output": {
        "none": 40
      },
      "tokens.phases.setup.reasoning": {
        "none": 40
      },
      "tokens.phases.shape.cached_input": {
        "none": 40
      },
      "tokens.phases.shape.input": {
        "none": 40
      },
      "tokens.phases.shape.output": {
        "none": 40
      },
      "tokens.phases.shape.reasoning": {
        "none": 40
      },
      "tokens.total.cached_input": {
        "none": 40
      },
      "tokens.total.input": {
        "none": 40
      },
      "tokens.total.output": {
        "none": 40
      },
      "tokens.total.reasoning": {
        "none": 40
      },
      "tools.codex_cli": {
        "none": 40
      },
      "tools.grader": {
        "none": 40
      },
      "tools.runner": {
        "none": 40
      },
      "tools.toolchains.elixir": {
        "none": 40
      },
      "tools.toolchains.erlang": {
        "none": 40
      },
      "tools.toolchains.node": {
        "none": 40
      },
      "tools.toolchains.other_inventory": {
        "none": 40
      },
      "tools.toolchains.ruby": {
        "none": 40
      },
      "tools.toolchains.rust": {
        "none": 40
      }
    },
    "reconstructable": {}
  },
  "round": "r24"
}
```
