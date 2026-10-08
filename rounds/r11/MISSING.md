# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 25,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Boundary telemetry not retained": 25
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Boundary telemetry not retained": 25
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
      "count": 25,
      "reasons": {
        "Complete per-model billable vector unavailable": 25
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "No per-cell CPU allocation receipt": 25
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "No per-cell CPU receipt": 25
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "No per-cell kernel receipt": 25
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "No per-cell RAM receipt": 25
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Toolchain version/inventory not recorded": 25
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Toolchain version/inventory not recorded": 25
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Toolchain version/inventory not recorded": 25
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Toolchain version/inventory not recorded": 25
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Toolchain version/inventory not recorded": 25
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Toolchain version/inventory not recorded": 25
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 25,
      "reasons": {
        "No per-cell CPU receipt": 25
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 25,
      "reasons": {
        "No per-cell kernel receipt": 25
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 25,
      "reasons": {
        "No per-cell RAM receipt": 25
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 25,
      "reasons": {
        "No per-cell CPU allocation receipt": 25
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 7,
      "reasons": {
        "Official result outside standard outcome classes": 7
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Not recorded in available public metadata": 25
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Dependency source not pinned per cell": 25
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 25
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Original base revision type not recorded per cell": 25
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 25
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Original base revision type not recorded per cell": 25
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Attempt boundary receipts unavailable": 25
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Absolute phase boundary not retained": 25
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Absolute phase boundary not retained": 25
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Absolute phase boundary not retained": 25
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Absolute phase boundary not retained": 25
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Absolute phase boundary not retained": 25
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Absolute phase boundary not retained": 25
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Absolute phase boundary not retained": 25
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Absolute phase boundary not retained": 25
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Absolute phase boundary not retained": 25
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Absolute phase boundary not retained": 25
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Absolute phase boundary not retained": 25
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Absolute phase boundary not retained": 25
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Absolute phase boundary not retained": 25
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Absolute phase boundary not retained": 25
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 25,
      "reasons": {
        "Phase wall not emitted or not separable": 25
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 25,
      "reasons": {
        "Phase wall not emitted or not separable": 25
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 25,
      "reasons": {
        "Phase wall not emitted or not separable": 25
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 25,
      "reasons": {
        "Phase wall not emitted or not separable": 25
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 25,
      "reasons": {
        "Phase wall not emitted or not separable": 25
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 25,
      "reasons": {
        "Phase wall not emitted or not separable": 25
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Per-phase token counter not emitted": 25
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 25
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 25
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 25
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 25
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 25
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 25
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 25
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Toolchain version/inventory not recorded": 25
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Toolchain version/inventory not recorded": 25
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Toolchain version/inventory not recorded": 25
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Toolchain version/inventory not recorded": 25
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Toolchain version/inventory not recorded": 25
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 25,
      "reasons": {
        "Toolchain version/inventory not recorded": 25
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 25
      },
      "circumstances.load1_end": {
        "none": 25
      },
      "circumstances.load_samples": {
        "none": 20
      },
      "cost.usd": {
        "none": 25
      },
      "environment.cores": {
        "none": 25
      },
      "environment.cpu_model": {
        "none": 25
      },
      "environment.kernel": {
        "none": 25
      },
      "environment.ram_gib": {
        "none": 25
      },
      "environment.toolchains.elixir": {
        "none": 25
      },
      "environment.toolchains.erlang": {
        "none": 25
      },
      "environment.toolchains.node": {
        "none": 25
      },
      "environment.toolchains.other_inventory": {
        "none": 25
      },
      "environment.toolchains.ruby": {
        "none": 25
      },
      "environment.toolchains.rust": {
        "none": 25
      },
      "host.cpu": {
        "none": 25
      },
      "host.kernel": {
        "none": 25
      },
      "host.ram_gib": {
        "none": 25
      },
      "host.vcpu": {
        "none": 25
      },
      "outcome": {
        "none": 7
      },
      "recipe": {
        "none": 25
      },
      "setup.deps_source": {
        "none": 25
      },
      "setup.task_base.hash": {
        "none": 25
      },
      "setup.task_base.kind": {
        "none": 25
      },
      "task.base_revision.hash": {
        "none": 25
      },
      "task.base_revision.kind": {
        "none": 25
      },
      "timestamps.attempts": {
        "none": 25
      },
      "timestamps.phases.develop.end_utc": {
        "none": 25
      },
      "timestamps.phases.develop.start_utc": {
        "none": 25
      },
      "timestamps.phases.gate.end_utc": {
        "none": 25
      },
      "timestamps.phases.gate.start_utc": {
        "none": 25
      },
      "timestamps.phases.grade.end_utc": {
        "none": 25
      },
      "timestamps.phases.grade.start_utc": {
        "none": 25
      },
      "timestamps.phases.plan.end_utc": {
        "none": 25
      },
      "timestamps.phases.plan.start_utc": {
        "none": 25
      },
      "timestamps.phases.review.end_utc": {
        "none": 25
      },
      "timestamps.phases.review.start_utc": {
        "none": 25
      },
      "timestamps.phases.setup.end_utc": {
        "none": 25
      },
      "timestamps.phases.setup.start_utc": {
        "none": 25
      },
      "timestamps.phases.shape.end_utc": {
        "none": 25
      },
      "timestamps.phases.shape.start_utc": {
        "none": 25
      },
      "timing.phases_s.develop": {
        "none": 25
      },
      "timing.phases_s.gate": {
        "none": 25
      },
      "timing.phases_s.plan": {
        "none": 25
      },
      "timing.phases_s.review": {
        "none": 25
      },
      "timing.phases_s.setup": {
        "none": 25
      },
      "timing.phases_s.shape": {
        "none": 25
      },
      "tokens.phases.develop.cached_input": {
        "none": 25
      },
      "tokens.phases.develop.input": {
        "none": 25
      },
      "tokens.phases.develop.output": {
        "none": 25
      },
      "tokens.phases.develop.reasoning": {
        "none": 25
      },
      "tokens.phases.gate.cached_input": {
        "none": 25
      },
      "tokens.phases.gate.input": {
        "none": 25
      },
      "tokens.phases.gate.output": {
        "none": 25
      },
      "tokens.phases.gate.reasoning": {
        "none": 25
      },
      "tokens.phases.plan.cached_input": {
        "none": 25
      },
      "tokens.phases.plan.input": {
        "none": 25
      },
      "tokens.phases.plan.output": {
        "none": 25
      },
      "tokens.phases.plan.reasoning": {
        "none": 25
      },
      "tokens.phases.review.cached_input": {
        "none": 25
      },
      "tokens.phases.review.input": {
        "none": 25
      },
      "tokens.phases.review.output": {
        "none": 25
      },
      "tokens.phases.review.reasoning": {
        "none": 25
      },
      "tokens.phases.setup.cached_input": {
        "none": 25
      },
      "tokens.phases.setup.input": {
        "none": 25
      },
      "tokens.phases.setup.output": {
        "none": 25
      },
      "tokens.phases.setup.reasoning": {
        "none": 25
      },
      "tokens.phases.shape.cached_input": {
        "none": 25
      },
      "tokens.phases.shape.input": {
        "none": 25
      },
      "tokens.phases.shape.output": {
        "none": 25
      },
      "tokens.phases.shape.reasoning": {
        "none": 25
      },
      "tokens.total.cached_input": {
        "none": 25
      },
      "tokens.total.input": {
        "none": 25
      },
      "tokens.total.output": {
        "none": 25
      },
      "tokens.total.reasoning": {
        "none": 25
      },
      "tools.codex_cli": {
        "none": 25
      },
      "tools.grader": {
        "none": 25
      },
      "tools.runner": {
        "none": 25
      },
      "tools.toolchains.elixir": {
        "none": 25
      },
      "tools.toolchains.erlang": {
        "none": 25
      },
      "tools.toolchains.node": {
        "none": 25
      },
      "tools.toolchains.other_inventory": {
        "none": 25
      },
      "tools.toolchains.ruby": {
        "none": 25
      },
      "tools.toolchains.rust": {
        "none": 25
      }
    },
    "reconstructable": {}
  },
  "round": "r11"
}
```
