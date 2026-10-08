# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 10,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Boundary telemetry not retained": 10
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Boundary telemetry not retained": 10
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "No matching controller samples retained": 10
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Complete per-model billable vector unavailable": 10
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "No per-cell CPU allocation receipt": 10
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "No per-cell CPU receipt": 10
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "No per-cell kernel receipt": 10
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "No per-cell RAM receipt": 10
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Toolchain version/inventory not recorded": 10
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Toolchain version/inventory not recorded": 10
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Toolchain version/inventory not recorded": 10
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Toolchain version/inventory not recorded": 10
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Toolchain version/inventory not recorded": 10
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Toolchain version/inventory not recorded": 10
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 10,
      "reasons": {
        "No per-cell CPU receipt": 10
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 10,
      "reasons": {
        "No per-cell kernel receipt": 10
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 10,
      "reasons": {
        "No per-cell RAM receipt": 10
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 10,
      "reasons": {
        "No per-cell CPU allocation receipt": 10
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Not recorded in available public metadata": 10
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Dependency source not pinned per cell": 10
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 10
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Original base revision type not recorded per cell": 10
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 10
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Original base revision type not recorded per cell": 10
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Attempt boundary receipts unavailable": 10
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Absolute phase boundary not retained": 10
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Absolute phase boundary not retained": 10
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Absolute phase boundary not retained": 10
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Absolute phase boundary not retained": 10
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Absolute phase boundary not retained": 10
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Absolute phase boundary not retained": 10
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Absolute phase boundary not retained": 10
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Absolute phase boundary not retained": 10
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Absolute phase boundary not retained": 10
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Absolute phase boundary not retained": 10
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Absolute phase boundary not retained": 10
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Absolute phase boundary not retained": 10
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Absolute phase boundary not retained": 10
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Absolute phase boundary not retained": 10
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 10,
      "reasons": {
        "Phase wall not emitted or not separable": 10
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 10,
      "reasons": {
        "Phase wall not emitted or not separable": 10
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 10,
      "reasons": {
        "Phase wall not emitted or not separable": 10
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 10,
      "reasons": {
        "Phase wall not emitted or not separable": 10
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 10,
      "reasons": {
        "Phase wall not emitted or not separable": 10
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 10,
      "reasons": {
        "Phase wall not emitted or not separable": 10
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Per-phase token counter not emitted": 10
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 10
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 10
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 10
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 10,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 10
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 10
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 10
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 10
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Toolchain version/inventory not recorded": 10
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Toolchain version/inventory not recorded": 10
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Toolchain version/inventory not recorded": 10
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Toolchain version/inventory not recorded": 10
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Toolchain version/inventory not recorded": 10
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Toolchain version/inventory not recorded": 10
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 10
      },
      "circumstances.load1_end": {
        "none": 10
      },
      "circumstances.load_samples": {
        "none": 10
      },
      "cost.usd": {
        "none": 10
      },
      "environment.cores": {
        "none": 10
      },
      "environment.cpu_model": {
        "none": 10
      },
      "environment.kernel": {
        "none": 10
      },
      "environment.ram_gib": {
        "none": 10
      },
      "environment.toolchains.elixir": {
        "none": 10
      },
      "environment.toolchains.erlang": {
        "none": 10
      },
      "environment.toolchains.node": {
        "none": 10
      },
      "environment.toolchains.other_inventory": {
        "none": 10
      },
      "environment.toolchains.ruby": {
        "none": 10
      },
      "environment.toolchains.rust": {
        "none": 10
      },
      "host.cpu": {
        "none": 10
      },
      "host.kernel": {
        "none": 10
      },
      "host.ram_gib": {
        "none": 10
      },
      "host.vcpu": {
        "none": 10
      },
      "recipe": {
        "none": 10
      },
      "setup.deps_source": {
        "none": 10
      },
      "setup.task_base.hash": {
        "none": 10
      },
      "setup.task_base.kind": {
        "none": 10
      },
      "task.base_revision.hash": {
        "none": 10
      },
      "task.base_revision.kind": {
        "none": 10
      },
      "timestamps.attempts": {
        "none": 10
      },
      "timestamps.phases.develop.end_utc": {
        "none": 10
      },
      "timestamps.phases.develop.start_utc": {
        "none": 10
      },
      "timestamps.phases.gate.end_utc": {
        "none": 10
      },
      "timestamps.phases.gate.start_utc": {
        "none": 10
      },
      "timestamps.phases.grade.end_utc": {
        "none": 10
      },
      "timestamps.phases.grade.start_utc": {
        "none": 10
      },
      "timestamps.phases.plan.end_utc": {
        "none": 10
      },
      "timestamps.phases.plan.start_utc": {
        "none": 10
      },
      "timestamps.phases.review.end_utc": {
        "none": 10
      },
      "timestamps.phases.review.start_utc": {
        "none": 10
      },
      "timestamps.phases.setup.end_utc": {
        "none": 10
      },
      "timestamps.phases.setup.start_utc": {
        "none": 10
      },
      "timestamps.phases.shape.end_utc": {
        "none": 10
      },
      "timestamps.phases.shape.start_utc": {
        "none": 10
      },
      "timing.phases_s.develop": {
        "none": 10
      },
      "timing.phases_s.gate": {
        "none": 10
      },
      "timing.phases_s.plan": {
        "none": 10
      },
      "timing.phases_s.review": {
        "none": 10
      },
      "timing.phases_s.setup": {
        "none": 10
      },
      "timing.phases_s.shape": {
        "none": 10
      },
      "tokens.phases.develop.cached_input": {
        "none": 10
      },
      "tokens.phases.develop.input": {
        "none": 10
      },
      "tokens.phases.develop.output": {
        "none": 10
      },
      "tokens.phases.develop.reasoning": {
        "none": 10
      },
      "tokens.phases.gate.cached_input": {
        "none": 10
      },
      "tokens.phases.gate.input": {
        "none": 10
      },
      "tokens.phases.gate.output": {
        "none": 10
      },
      "tokens.phases.gate.reasoning": {
        "none": 10
      },
      "tokens.phases.plan.cached_input": {
        "none": 10
      },
      "tokens.phases.plan.input": {
        "none": 10
      },
      "tokens.phases.plan.output": {
        "none": 10
      },
      "tokens.phases.plan.reasoning": {
        "none": 10
      },
      "tokens.phases.review.cached_input": {
        "none": 10
      },
      "tokens.phases.review.input": {
        "none": 10
      },
      "tokens.phases.review.output": {
        "none": 10
      },
      "tokens.phases.review.reasoning": {
        "none": 10
      },
      "tokens.phases.setup.cached_input": {
        "none": 10
      },
      "tokens.phases.setup.input": {
        "none": 10
      },
      "tokens.phases.setup.output": {
        "none": 10
      },
      "tokens.phases.setup.reasoning": {
        "none": 10
      },
      "tokens.phases.shape.cached_input": {
        "none": 10
      },
      "tokens.phases.shape.input": {
        "none": 10
      },
      "tokens.phases.shape.output": {
        "none": 10
      },
      "tokens.phases.shape.reasoning": {
        "none": 10
      },
      "tokens.total.cached_input": {
        "none": 10
      },
      "tokens.total.input": {
        "none": 10
      },
      "tokens.total.output": {
        "none": 10
      },
      "tokens.total.reasoning": {
        "none": 10
      },
      "tools.codex_cli": {
        "none": 10
      },
      "tools.grader": {
        "none": 10
      },
      "tools.runner": {
        "none": 10
      },
      "tools.toolchains.elixir": {
        "none": 10
      },
      "tools.toolchains.erlang": {
        "none": 10
      },
      "tools.toolchains.node": {
        "none": 10
      },
      "tools.toolchains.other_inventory": {
        "none": 10
      },
      "tools.toolchains.ruby": {
        "none": 10
      },
      "tools.toolchains.rust": {
        "none": 10
      }
    },
    "reconstructable": {}
  },
  "round": "r14"
}
```
