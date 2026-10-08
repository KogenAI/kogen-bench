# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 54,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Boundary telemetry not retained": 54
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
      "count": 54,
      "reasons": {
        "Boundary telemetry not retained": 54
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
      "count": 54,
      "reasons": {
        "Complete per-model billable vector unavailable": 54
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 15,
      "reasons": {
        "No dated account-class receipt": 15
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "No per-cell CPU allocation receipt": 54
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "No per-cell CPU receipt": 54
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 39,
      "reasons": {
        "No per-cell kernel receipt": 39
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "No per-cell RAM receipt": 54
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 54,
      "reasons": {
        "No per-cell CPU receipt": 54
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 39,
      "reasons": {
        "No per-cell kernel receipt": 39
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 54,
      "reasons": {
        "No per-cell RAM receipt": 54
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 54,
      "reasons": {
        "No per-cell CPU allocation receipt": 54
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 1,
      "reasons": {
        "Official result outside standard outcome classes": 1
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Not recorded in available public metadata": 54
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Dependency source not pinned per cell": 54
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 39,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 39
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 39,
      "reasons": {
        "Original base revision type not recorded per cell": 39
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 39,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 39
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 39,
      "reasons": {
        "Original base revision type not recorded per cell": 39
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Attempt boundary receipts unavailable": 54
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Absolute phase boundary not retained": 54
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Absolute phase boundary not retained": 54
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Absolute phase boundary not retained": 54
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Absolute phase boundary not retained": 54
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Absolute phase boundary not retained": 54
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Absolute phase boundary not retained": 54
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Absolute phase boundary not retained": 54
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Absolute phase boundary not retained": 54
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Absolute phase boundary not retained": 54
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Absolute phase boundary not retained": 54
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Absolute phase boundary not retained": 54
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Absolute phase boundary not retained": 54
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Absolute phase boundary not retained": 54
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Absolute phase boundary not retained": 54
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 54,
      "reasons": {
        "Phase wall not emitted or not separable": 54
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 54,
      "reasons": {
        "Phase wall not emitted or not separable": 54
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 54,
      "reasons": {
        "Phase wall not emitted or not separable": 54
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 54,
      "reasons": {
        "Phase wall not emitted or not separable": 54
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 54,
      "reasons": {
        "Phase wall not emitted or not separable": 54
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 54,
      "reasons": {
        "Phase wall not emitted or not separable": 54
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 54
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 54
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 54
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 54,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 54
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 54
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 54
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 54
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 54
      },
      "circumstances.concurrent_cells_end": {
        "none": 15
      },
      "circumstances.concurrent_cells_start": {
        "none": 15
      },
      "circumstances.load1_end": {
        "none": 54
      },
      "circumstances.load_samples": {
        "none": 15
      },
      "cost.usd": {
        "none": 54
      },
      "environment.account_class": {
        "none": 15
      },
      "environment.cores": {
        "none": 54
      },
      "environment.cpu_model": {
        "none": 54
      },
      "environment.kernel": {
        "none": 39
      },
      "environment.ram_gib": {
        "none": 54
      },
      "environment.toolchains.elixir": {
        "none": 54
      },
      "environment.toolchains.erlang": {
        "none": 54
      },
      "environment.toolchains.node": {
        "none": 54
      },
      "environment.toolchains.other_inventory": {
        "none": 54
      },
      "environment.toolchains.ruby": {
        "none": 54
      },
      "environment.toolchains.rust": {
        "none": 54
      },
      "host.cpu": {
        "none": 54
      },
      "host.kernel": {
        "none": 39
      },
      "host.ram_gib": {
        "none": 54
      },
      "host.vcpu": {
        "none": 54
      },
      "outcome": {
        "none": 1
      },
      "recipe": {
        "none": 54
      },
      "setup.deps_source": {
        "none": 54
      },
      "setup.task_base.hash": {
        "none": 39
      },
      "setup.task_base.kind": {
        "none": 39
      },
      "task.base_revision.hash": {
        "none": 39
      },
      "task.base_revision.kind": {
        "none": 39
      },
      "timestamps.attempts": {
        "none": 54
      },
      "timestamps.phases.develop.end_utc": {
        "none": 54
      },
      "timestamps.phases.develop.start_utc": {
        "none": 54
      },
      "timestamps.phases.gate.end_utc": {
        "none": 54
      },
      "timestamps.phases.gate.start_utc": {
        "none": 54
      },
      "timestamps.phases.grade.end_utc": {
        "none": 54
      },
      "timestamps.phases.grade.start_utc": {
        "none": 54
      },
      "timestamps.phases.plan.end_utc": {
        "none": 54
      },
      "timestamps.phases.plan.start_utc": {
        "none": 54
      },
      "timestamps.phases.review.end_utc": {
        "none": 54
      },
      "timestamps.phases.review.start_utc": {
        "none": 54
      },
      "timestamps.phases.setup.end_utc": {
        "none": 54
      },
      "timestamps.phases.setup.start_utc": {
        "none": 54
      },
      "timestamps.phases.shape.end_utc": {
        "none": 54
      },
      "timestamps.phases.shape.start_utc": {
        "none": 54
      },
      "timing.phases_s.develop": {
        "none": 54
      },
      "timing.phases_s.gate": {
        "none": 54
      },
      "timing.phases_s.plan": {
        "none": 54
      },
      "timing.phases_s.review": {
        "none": 54
      },
      "timing.phases_s.setup": {
        "none": 54
      },
      "timing.phases_s.shape": {
        "none": 54
      },
      "tokens.phases.develop.cached_input": {
        "none": 54
      },
      "tokens.phases.develop.input": {
        "none": 54
      },
      "tokens.phases.develop.output": {
        "none": 54
      },
      "tokens.phases.develop.reasoning": {
        "none": 54
      },
      "tokens.phases.gate.cached_input": {
        "none": 54
      },
      "tokens.phases.gate.input": {
        "none": 54
      },
      "tokens.phases.gate.output": {
        "none": 54
      },
      "tokens.phases.gate.reasoning": {
        "none": 54
      },
      "tokens.phases.plan.cached_input": {
        "none": 54
      },
      "tokens.phases.plan.input": {
        "none": 54
      },
      "tokens.phases.plan.output": {
        "none": 54
      },
      "tokens.phases.plan.reasoning": {
        "none": 54
      },
      "tokens.phases.review.cached_input": {
        "none": 54
      },
      "tokens.phases.review.input": {
        "none": 54
      },
      "tokens.phases.review.output": {
        "none": 54
      },
      "tokens.phases.review.reasoning": {
        "none": 54
      },
      "tokens.phases.setup.cached_input": {
        "none": 54
      },
      "tokens.phases.setup.input": {
        "none": 54
      },
      "tokens.phases.setup.output": {
        "none": 54
      },
      "tokens.phases.setup.reasoning": {
        "none": 54
      },
      "tokens.phases.shape.cached_input": {
        "none": 54
      },
      "tokens.phases.shape.input": {
        "none": 54
      },
      "tokens.phases.shape.output": {
        "none": 54
      },
      "tokens.phases.shape.reasoning": {
        "none": 54
      },
      "tokens.total.cached_input": {
        "none": 54
      },
      "tokens.total.input": {
        "none": 54
      },
      "tokens.total.output": {
        "none": 54
      },
      "tokens.total.reasoning": {
        "none": 54
      },
      "tools.codex_cli": {
        "none": 54
      },
      "tools.grader": {
        "none": 54
      },
      "tools.runner": {
        "none": 54
      },
      "tools.toolchains.elixir": {
        "none": 54
      },
      "tools.toolchains.erlang": {
        "none": 54
      },
      "tools.toolchains.node": {
        "none": 54
      },
      "tools.toolchains.other_inventory": {
        "none": 54
      },
      "tools.toolchains.ruby": {
        "none": 54
      },
      "tools.toolchains.rust": {
        "none": 54
      }
    },
    "reconstructable": {}
  },
  "round": "r47"
}
```
