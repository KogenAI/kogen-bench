# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 35,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Boundary telemetry not retained": 35
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Boundary telemetry not retained": 15
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 15
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Boundary telemetry not retained": 35
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "No matching controller samples retained": 15
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Complete per-model billable vector unavailable": 35
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "No per-cell CPU allocation receipt": 35
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "No per-cell CPU receipt": 35
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
      "count": 35,
      "reasons": {
        "No per-cell RAM receipt": 35
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Toolchain version/inventory not recorded": 35
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Toolchain version/inventory not recorded": 35
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Toolchain version/inventory not recorded": 35
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Toolchain version/inventory not recorded": 35
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Toolchain version/inventory not recorded": 35
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Toolchain version/inventory not recorded": 35
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 35,
      "reasons": {
        "No per-cell CPU receipt": 35
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
      "count": 35,
      "reasons": {
        "No per-cell RAM receipt": 35
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 35,
      "reasons": {
        "No per-cell CPU allocation receipt": 35
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Not recorded in available public metadata": 35
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Dependency source not pinned per cell": 35
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 35
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Original base revision type not recorded per cell": 35
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 35
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Original base revision type not recorded per cell": 35
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Attempt boundary receipts unavailable": 35
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Absolute phase boundary not retained": 35
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Absolute phase boundary not retained": 35
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Absolute phase boundary not retained": 35
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Absolute phase boundary not retained": 35
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Absolute phase boundary not retained": 35
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Absolute phase boundary not retained": 35
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Absolute phase boundary not retained": 35
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Absolute phase boundary not retained": 35
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Absolute phase boundary not retained": 35
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Absolute phase boundary not retained": 35
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Absolute phase boundary not retained": 35
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Absolute phase boundary not retained": 35
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Absolute phase boundary not retained": 35
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Absolute phase boundary not retained": 35
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 35,
      "reasons": {
        "Phase wall not emitted or not separable": 35
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 35,
      "reasons": {
        "Phase wall not emitted or not separable": 35
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 35,
      "reasons": {
        "Phase wall not emitted or not separable": 35
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 35,
      "reasons": {
        "Phase wall not emitted or not separable": 35
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 35,
      "reasons": {
        "Phase wall not emitted or not separable": 35
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 35,
      "reasons": {
        "Phase wall not emitted or not separable": 35
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Per-phase token counter not emitted": 35
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Per-phase token counter not emitted": 35
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Per-phase token counter not emitted": 35
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Per-phase token counter not emitted": 35
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Per-phase token counter not emitted": 35
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Per-phase token counter not emitted": 35
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Per-phase token counter not emitted": 35
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Per-phase token counter not emitted": 35
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Per-phase token counter not emitted": 35
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Per-phase token counter not emitted": 35
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Per-phase token counter not emitted": 35
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Per-phase token counter not emitted": 35
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Per-phase token counter not emitted": 35
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Per-phase token counter not emitted": 35
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Per-phase token counter not emitted": 35
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Per-phase token counter not emitted": 35
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Per-phase token counter not emitted": 35
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Per-phase token counter not emitted": 35
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Per-phase token counter not emitted": 35
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Per-phase token counter not emitted": 35
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Per-phase token counter not emitted": 35
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Per-phase token counter not emitted": 35
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Per-phase token counter not emitted": 35
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Per-phase token counter not emitted": 35
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 35
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 35
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 35
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 35,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 35
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 35
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 35
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 35
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Toolchain version/inventory not recorded": 35
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Toolchain version/inventory not recorded": 35
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Toolchain version/inventory not recorded": 35
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Toolchain version/inventory not recorded": 35
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Toolchain version/inventory not recorded": 35
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "Toolchain version/inventory not recorded": 35
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 35
      },
      "circumstances.concurrent_cells_end": {
        "none": 15
      },
      "circumstances.concurrent_cells_start": {
        "none": 15
      },
      "circumstances.load1_end": {
        "none": 35
      },
      "circumstances.load_samples": {
        "none": 15
      },
      "cost.usd": {
        "none": 35
      },
      "environment.cores": {
        "none": 35
      },
      "environment.cpu_model": {
        "none": 35
      },
      "environment.kernel": {
        "none": 20
      },
      "environment.ram_gib": {
        "none": 35
      },
      "environment.toolchains.elixir": {
        "none": 35
      },
      "environment.toolchains.erlang": {
        "none": 35
      },
      "environment.toolchains.node": {
        "none": 35
      },
      "environment.toolchains.other_inventory": {
        "none": 35
      },
      "environment.toolchains.ruby": {
        "none": 35
      },
      "environment.toolchains.rust": {
        "none": 35
      },
      "host.cpu": {
        "none": 35
      },
      "host.kernel": {
        "none": 20
      },
      "host.ram_gib": {
        "none": 35
      },
      "host.vcpu": {
        "none": 35
      },
      "recipe": {
        "none": 35
      },
      "setup.deps_source": {
        "none": 35
      },
      "setup.task_base.hash": {
        "none": 35
      },
      "setup.task_base.kind": {
        "none": 35
      },
      "task.base_revision.hash": {
        "none": 35
      },
      "task.base_revision.kind": {
        "none": 35
      },
      "timestamps.attempts": {
        "none": 35
      },
      "timestamps.phases.develop.end_utc": {
        "none": 35
      },
      "timestamps.phases.develop.start_utc": {
        "none": 35
      },
      "timestamps.phases.gate.end_utc": {
        "none": 35
      },
      "timestamps.phases.gate.start_utc": {
        "none": 35
      },
      "timestamps.phases.grade.end_utc": {
        "none": 35
      },
      "timestamps.phases.grade.start_utc": {
        "none": 35
      },
      "timestamps.phases.plan.end_utc": {
        "none": 35
      },
      "timestamps.phases.plan.start_utc": {
        "none": 35
      },
      "timestamps.phases.review.end_utc": {
        "none": 35
      },
      "timestamps.phases.review.start_utc": {
        "none": 35
      },
      "timestamps.phases.setup.end_utc": {
        "none": 35
      },
      "timestamps.phases.setup.start_utc": {
        "none": 35
      },
      "timestamps.phases.shape.end_utc": {
        "none": 35
      },
      "timestamps.phases.shape.start_utc": {
        "none": 35
      },
      "timing.phases_s.develop": {
        "none": 35
      },
      "timing.phases_s.gate": {
        "none": 35
      },
      "timing.phases_s.plan": {
        "none": 35
      },
      "timing.phases_s.review": {
        "none": 35
      },
      "timing.phases_s.setup": {
        "none": 35
      },
      "timing.phases_s.shape": {
        "none": 35
      },
      "tokens.phases.develop.cached_input": {
        "none": 35
      },
      "tokens.phases.develop.input": {
        "none": 35
      },
      "tokens.phases.develop.output": {
        "none": 35
      },
      "tokens.phases.develop.reasoning": {
        "none": 35
      },
      "tokens.phases.gate.cached_input": {
        "none": 35
      },
      "tokens.phases.gate.input": {
        "none": 35
      },
      "tokens.phases.gate.output": {
        "none": 35
      },
      "tokens.phases.gate.reasoning": {
        "none": 35
      },
      "tokens.phases.plan.cached_input": {
        "none": 35
      },
      "tokens.phases.plan.input": {
        "none": 35
      },
      "tokens.phases.plan.output": {
        "none": 35
      },
      "tokens.phases.plan.reasoning": {
        "none": 35
      },
      "tokens.phases.review.cached_input": {
        "none": 35
      },
      "tokens.phases.review.input": {
        "none": 35
      },
      "tokens.phases.review.output": {
        "none": 35
      },
      "tokens.phases.review.reasoning": {
        "none": 35
      },
      "tokens.phases.setup.cached_input": {
        "none": 35
      },
      "tokens.phases.setup.input": {
        "none": 35
      },
      "tokens.phases.setup.output": {
        "none": 35
      },
      "tokens.phases.setup.reasoning": {
        "none": 35
      },
      "tokens.phases.shape.cached_input": {
        "none": 35
      },
      "tokens.phases.shape.input": {
        "none": 35
      },
      "tokens.phases.shape.output": {
        "none": 35
      },
      "tokens.phases.shape.reasoning": {
        "none": 35
      },
      "tokens.total.cached_input": {
        "none": 35
      },
      "tokens.total.input": {
        "none": 35
      },
      "tokens.total.output": {
        "none": 35
      },
      "tokens.total.reasoning": {
        "none": 35
      },
      "tools.codex_cli": {
        "none": 35
      },
      "tools.grader": {
        "none": 35
      },
      "tools.runner": {
        "none": 35
      },
      "tools.toolchains.elixir": {
        "none": 35
      },
      "tools.toolchains.erlang": {
        "none": 35
      },
      "tools.toolchains.node": {
        "none": 35
      },
      "tools.toolchains.other_inventory": {
        "none": 35
      },
      "tools.toolchains.ruby": {
        "none": 35
      },
      "tools.toolchains.rust": {
        "none": 35
      }
    },
    "reconstructable": {}
  },
  "round": "r8"
}
```
