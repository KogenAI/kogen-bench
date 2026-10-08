# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 12,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Boundary telemetry not retained": 12
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Boundary telemetry not retained": 12
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "No matching controller samples retained": 12
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Complete per-model billable vector unavailable": 12
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "No per-cell CPU allocation receipt": 12
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "No per-cell CPU receipt": 12
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "No per-cell kernel receipt": 12
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "No per-cell RAM receipt": 12
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 12,
      "reasons": {
        "No per-cell CPU receipt": 12
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 12,
      "reasons": {
        "No per-cell kernel receipt": 12
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 12,
      "reasons": {
        "No per-cell RAM receipt": 12
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 12,
      "reasons": {
        "No per-cell CPU allocation receipt": 12
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Not recorded in available public metadata": 12
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Dependency source not pinned per cell": 12
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 12
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Original base revision type not recorded per cell": 12
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 12
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Original base revision type not recorded per cell": 12
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Attempt boundary receipts unavailable": 12
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Absolute phase boundary not retained": 12
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 12,
      "reasons": {
        "Phase wall not emitted or not separable": 12
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 12,
      "reasons": {
        "Phase wall not emitted or not separable": 12
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 12,
      "reasons": {
        "Phase wall not emitted or not separable": 12
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 12,
      "reasons": {
        "Phase wall not emitted or not separable": 12
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 12,
      "reasons": {
        "Phase wall not emitted or not separable": 12
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 12,
      "reasons": {
        "Phase wall not emitted or not separable": 12
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 12
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 12
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 12
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 12
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 12
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 12
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 12
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 12
      },
      "circumstances.load1_end": {
        "none": 12
      },
      "circumstances.load_samples": {
        "none": 12
      },
      "cost.usd": {
        "none": 12
      },
      "environment.cores": {
        "none": 12
      },
      "environment.cpu_model": {
        "none": 12
      },
      "environment.kernel": {
        "none": 12
      },
      "environment.ram_gib": {
        "none": 12
      },
      "environment.toolchains.elixir": {
        "none": 12
      },
      "environment.toolchains.erlang": {
        "none": 12
      },
      "environment.toolchains.node": {
        "none": 12
      },
      "environment.toolchains.other_inventory": {
        "none": 12
      },
      "environment.toolchains.ruby": {
        "none": 12
      },
      "environment.toolchains.rust": {
        "none": 12
      },
      "host.cpu": {
        "none": 12
      },
      "host.kernel": {
        "none": 12
      },
      "host.ram_gib": {
        "none": 12
      },
      "host.vcpu": {
        "none": 12
      },
      "recipe": {
        "none": 12
      },
      "setup.deps_source": {
        "none": 12
      },
      "setup.task_base.hash": {
        "none": 12
      },
      "setup.task_base.kind": {
        "none": 12
      },
      "task.base_revision.hash": {
        "none": 12
      },
      "task.base_revision.kind": {
        "none": 12
      },
      "timestamps.attempts": {
        "none": 12
      },
      "timestamps.phases.develop.end_utc": {
        "none": 12
      },
      "timestamps.phases.develop.start_utc": {
        "none": 12
      },
      "timestamps.phases.gate.end_utc": {
        "none": 12
      },
      "timestamps.phases.gate.start_utc": {
        "none": 12
      },
      "timestamps.phases.grade.end_utc": {
        "none": 12
      },
      "timestamps.phases.grade.start_utc": {
        "none": 12
      },
      "timestamps.phases.plan.end_utc": {
        "none": 12
      },
      "timestamps.phases.plan.start_utc": {
        "none": 12
      },
      "timestamps.phases.review.end_utc": {
        "none": 12
      },
      "timestamps.phases.review.start_utc": {
        "none": 12
      },
      "timestamps.phases.setup.end_utc": {
        "none": 12
      },
      "timestamps.phases.setup.start_utc": {
        "none": 12
      },
      "timestamps.phases.shape.end_utc": {
        "none": 12
      },
      "timestamps.phases.shape.start_utc": {
        "none": 12
      },
      "timing.phases_s.develop": {
        "none": 12
      },
      "timing.phases_s.gate": {
        "none": 12
      },
      "timing.phases_s.plan": {
        "none": 12
      },
      "timing.phases_s.review": {
        "none": 12
      },
      "timing.phases_s.setup": {
        "none": 12
      },
      "timing.phases_s.shape": {
        "none": 12
      },
      "tokens.phases.develop.cached_input": {
        "none": 12
      },
      "tokens.phases.develop.input": {
        "none": 12
      },
      "tokens.phases.develop.output": {
        "none": 12
      },
      "tokens.phases.develop.reasoning": {
        "none": 12
      },
      "tokens.phases.gate.cached_input": {
        "none": 12
      },
      "tokens.phases.gate.input": {
        "none": 12
      },
      "tokens.phases.gate.output": {
        "none": 12
      },
      "tokens.phases.gate.reasoning": {
        "none": 12
      },
      "tokens.phases.plan.cached_input": {
        "none": 12
      },
      "tokens.phases.plan.input": {
        "none": 12
      },
      "tokens.phases.plan.output": {
        "none": 12
      },
      "tokens.phases.plan.reasoning": {
        "none": 12
      },
      "tokens.phases.review.cached_input": {
        "none": 12
      },
      "tokens.phases.review.input": {
        "none": 12
      },
      "tokens.phases.review.output": {
        "none": 12
      },
      "tokens.phases.review.reasoning": {
        "none": 12
      },
      "tokens.phases.setup.cached_input": {
        "none": 12
      },
      "tokens.phases.setup.input": {
        "none": 12
      },
      "tokens.phases.setup.output": {
        "none": 12
      },
      "tokens.phases.setup.reasoning": {
        "none": 12
      },
      "tokens.phases.shape.cached_input": {
        "none": 12
      },
      "tokens.phases.shape.input": {
        "none": 12
      },
      "tokens.phases.shape.output": {
        "none": 12
      },
      "tokens.phases.shape.reasoning": {
        "none": 12
      },
      "tokens.total.cached_input": {
        "none": 12
      },
      "tokens.total.input": {
        "none": 12
      },
      "tokens.total.output": {
        "none": 12
      },
      "tokens.total.reasoning": {
        "none": 12
      },
      "tools.codex_cli": {
        "none": 12
      },
      "tools.grader": {
        "none": 12
      },
      "tools.runner": {
        "none": 12
      },
      "tools.toolchains.elixir": {
        "none": 12
      },
      "tools.toolchains.erlang": {
        "none": 12
      },
      "tools.toolchains.node": {
        "none": 12
      },
      "tools.toolchains.other_inventory": {
        "none": 12
      },
      "tools.toolchains.ruby": {
        "none": 12
      },
      "tools.toolchains.rust": {
        "none": 12
      }
    },
    "reconstructable": {}
  },
  "round": "r5"
}
```
