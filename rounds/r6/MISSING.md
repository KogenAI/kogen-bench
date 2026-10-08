# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 45,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Boundary telemetry not retained": 45
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
      "count": 45,
      "reasons": {
        "Boundary telemetry not retained": 45
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "No matching controller samples retained": 45
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Complete per-model billable vector unavailable": 45
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "No per-cell CPU allocation receipt": 45
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "No per-cell CPU receipt": 45
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "No per-cell kernel receipt": 15
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "No per-cell RAM receipt": 45
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Toolchain version/inventory not recorded": 45
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Toolchain version/inventory not recorded": 45
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Toolchain version/inventory not recorded": 45
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Toolchain version/inventory not recorded": 45
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Toolchain version/inventory not recorded": 45
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Toolchain version/inventory not recorded": 45
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 45,
      "reasons": {
        "No per-cell CPU receipt": 45
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 15,
      "reasons": {
        "No per-cell kernel receipt": 15
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 45,
      "reasons": {
        "No per-cell RAM receipt": 45
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 45,
      "reasons": {
        "No per-cell CPU allocation receipt": 45
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Not recorded in available public metadata": 45
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Dependency source not pinned per cell": 45
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 45
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Original base revision type not recorded per cell": 45
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 45
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Original base revision type not recorded per cell": 45
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Attempt boundary receipts unavailable": 45
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Absolute phase boundary not retained": 45
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Absolute phase boundary not retained": 45
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Absolute phase boundary not retained": 45
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Absolute phase boundary not retained": 45
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Absolute phase boundary not retained": 45
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Absolute phase boundary not retained": 45
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Absolute phase boundary not retained": 45
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Absolute phase boundary not retained": 45
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Absolute phase boundary not retained": 45
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Absolute phase boundary not retained": 45
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Absolute phase boundary not retained": 45
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Absolute phase boundary not retained": 45
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Absolute phase boundary not retained": 45
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Absolute phase boundary not retained": 45
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 45,
      "reasons": {
        "Phase wall not emitted or not separable": 45
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 45,
      "reasons": {
        "Phase wall not emitted or not separable": 45
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 45,
      "reasons": {
        "Phase wall not emitted or not separable": 45
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 45,
      "reasons": {
        "Phase wall not emitted or not separable": 45
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 45,
      "reasons": {
        "Phase wall not emitted or not separable": 45
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 45,
      "reasons": {
        "Phase wall not emitted or not separable": 45
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Per-phase token counter not emitted": 45
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Per-phase token counter not emitted": 45
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Per-phase token counter not emitted": 45
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Per-phase token counter not emitted": 45
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Per-phase token counter not emitted": 45
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Per-phase token counter not emitted": 45
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Per-phase token counter not emitted": 45
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Per-phase token counter not emitted": 45
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Per-phase token counter not emitted": 45
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Per-phase token counter not emitted": 45
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Per-phase token counter not emitted": 45
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Per-phase token counter not emitted": 45
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Per-phase token counter not emitted": 45
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Per-phase token counter not emitted": 45
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Per-phase token counter not emitted": 45
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Per-phase token counter not emitted": 45
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Per-phase token counter not emitted": 45
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Per-phase token counter not emitted": 45
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Per-phase token counter not emitted": 45
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Per-phase token counter not emitted": 45
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Per-phase token counter not emitted": 45
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Per-phase token counter not emitted": 45
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Per-phase token counter not emitted": 45
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Per-phase token counter not emitted": 45
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 45
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 45
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 45
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 45,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 45
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 45
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 45
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 45
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Toolchain version/inventory not recorded": 45
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Toolchain version/inventory not recorded": 45
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Toolchain version/inventory not recorded": 45
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Toolchain version/inventory not recorded": 45
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Toolchain version/inventory not recorded": 45
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 45,
      "reasons": {
        "Toolchain version/inventory not recorded": 45
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 45
      },
      "circumstances.concurrent_cells_end": {
        "none": 30
      },
      "circumstances.concurrent_cells_start": {
        "none": 30
      },
      "circumstances.load1_end": {
        "none": 45
      },
      "circumstances.load_samples": {
        "none": 45
      },
      "cost.usd": {
        "none": 45
      },
      "environment.cores": {
        "none": 45
      },
      "environment.cpu_model": {
        "none": 45
      },
      "environment.kernel": {
        "none": 15
      },
      "environment.ram_gib": {
        "none": 45
      },
      "environment.toolchains.elixir": {
        "none": 45
      },
      "environment.toolchains.erlang": {
        "none": 45
      },
      "environment.toolchains.node": {
        "none": 45
      },
      "environment.toolchains.other_inventory": {
        "none": 45
      },
      "environment.toolchains.ruby": {
        "none": 45
      },
      "environment.toolchains.rust": {
        "none": 45
      },
      "host.cpu": {
        "none": 45
      },
      "host.kernel": {
        "none": 15
      },
      "host.ram_gib": {
        "none": 45
      },
      "host.vcpu": {
        "none": 45
      },
      "recipe": {
        "none": 45
      },
      "setup.deps_source": {
        "none": 45
      },
      "setup.task_base.hash": {
        "none": 45
      },
      "setup.task_base.kind": {
        "none": 45
      },
      "task.base_revision.hash": {
        "none": 45
      },
      "task.base_revision.kind": {
        "none": 45
      },
      "timestamps.attempts": {
        "none": 45
      },
      "timestamps.phases.develop.end_utc": {
        "none": 45
      },
      "timestamps.phases.develop.start_utc": {
        "none": 45
      },
      "timestamps.phases.gate.end_utc": {
        "none": 45
      },
      "timestamps.phases.gate.start_utc": {
        "none": 45
      },
      "timestamps.phases.grade.end_utc": {
        "none": 45
      },
      "timestamps.phases.grade.start_utc": {
        "none": 45
      },
      "timestamps.phases.plan.end_utc": {
        "none": 45
      },
      "timestamps.phases.plan.start_utc": {
        "none": 45
      },
      "timestamps.phases.review.end_utc": {
        "none": 45
      },
      "timestamps.phases.review.start_utc": {
        "none": 45
      },
      "timestamps.phases.setup.end_utc": {
        "none": 45
      },
      "timestamps.phases.setup.start_utc": {
        "none": 45
      },
      "timestamps.phases.shape.end_utc": {
        "none": 45
      },
      "timestamps.phases.shape.start_utc": {
        "none": 45
      },
      "timing.phases_s.develop": {
        "none": 45
      },
      "timing.phases_s.gate": {
        "none": 45
      },
      "timing.phases_s.plan": {
        "none": 45
      },
      "timing.phases_s.review": {
        "none": 45
      },
      "timing.phases_s.setup": {
        "none": 45
      },
      "timing.phases_s.shape": {
        "none": 45
      },
      "tokens.phases.develop.cached_input": {
        "none": 45
      },
      "tokens.phases.develop.input": {
        "none": 45
      },
      "tokens.phases.develop.output": {
        "none": 45
      },
      "tokens.phases.develop.reasoning": {
        "none": 45
      },
      "tokens.phases.gate.cached_input": {
        "none": 45
      },
      "tokens.phases.gate.input": {
        "none": 45
      },
      "tokens.phases.gate.output": {
        "none": 45
      },
      "tokens.phases.gate.reasoning": {
        "none": 45
      },
      "tokens.phases.plan.cached_input": {
        "none": 45
      },
      "tokens.phases.plan.input": {
        "none": 45
      },
      "tokens.phases.plan.output": {
        "none": 45
      },
      "tokens.phases.plan.reasoning": {
        "none": 45
      },
      "tokens.phases.review.cached_input": {
        "none": 45
      },
      "tokens.phases.review.input": {
        "none": 45
      },
      "tokens.phases.review.output": {
        "none": 45
      },
      "tokens.phases.review.reasoning": {
        "none": 45
      },
      "tokens.phases.setup.cached_input": {
        "none": 45
      },
      "tokens.phases.setup.input": {
        "none": 45
      },
      "tokens.phases.setup.output": {
        "none": 45
      },
      "tokens.phases.setup.reasoning": {
        "none": 45
      },
      "tokens.phases.shape.cached_input": {
        "none": 45
      },
      "tokens.phases.shape.input": {
        "none": 45
      },
      "tokens.phases.shape.output": {
        "none": 45
      },
      "tokens.phases.shape.reasoning": {
        "none": 45
      },
      "tokens.total.cached_input": {
        "none": 45
      },
      "tokens.total.input": {
        "none": 45
      },
      "tokens.total.output": {
        "none": 45
      },
      "tokens.total.reasoning": {
        "none": 45
      },
      "tools.codex_cli": {
        "none": 45
      },
      "tools.grader": {
        "none": 45
      },
      "tools.runner": {
        "none": 45
      },
      "tools.toolchains.elixir": {
        "none": 45
      },
      "tools.toolchains.erlang": {
        "none": 45
      },
      "tools.toolchains.node": {
        "none": 45
      },
      "tools.toolchains.other_inventory": {
        "none": 45
      },
      "tools.toolchains.ruby": {
        "none": 45
      },
      "tools.toolchains.rust": {
        "none": 45
      }
    },
    "reconstructable": {}
  },
  "round": "r6"
}
```
