# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 41,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Boundary telemetry not retained": 41
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Boundary telemetry not retained": 41
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 41
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Boundary telemetry not retained": 41
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "No matching controller samples retained": 41
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Complete per-model billable vector unavailable": 1
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "No dated account-class receipt": 41
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "No per-cell CPU allocation receipt": 41
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "No per-cell CPU receipt": 41
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "No per-cell RAM receipt": 41
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Toolchain version/inventory not recorded": 41
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Toolchain version/inventory not recorded": 41
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Toolchain version/inventory not recorded": 41
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Toolchain version/inventory not recorded": 41
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Toolchain version/inventory not recorded": 41
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Toolchain version/inventory not recorded": 41
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 41,
      "reasons": {
        "No per-cell CPU receipt": 41
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 41,
      "reasons": {
        "No per-cell RAM receipt": 41
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 41,
      "reasons": {
        "No per-cell CPU allocation receipt": 41
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Not recorded in available public metadata": 41
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Dependency source not pinned per cell": 41
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Attempt boundary receipts unavailable": 41
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Absolute phase boundary not retained": 41
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Absolute phase boundary not retained": 41
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Absolute phase boundary not retained": 41
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Absolute phase boundary not retained": 41
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Absolute phase boundary not retained": 41
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Absolute phase boundary not retained": 41
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Absolute phase boundary not retained": 41
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Absolute phase boundary not retained": 41
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Absolute phase boundary not retained": 41
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Absolute phase boundary not retained": 41
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Absolute phase boundary not retained": 41
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Absolute phase boundary not retained": 41
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Absolute phase boundary not retained": 41
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Absolute phase boundary not retained": 41
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 41,
      "reasons": {
        "Phase wall not emitted or not separable": 41
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 41,
      "reasons": {
        "Phase wall not emitted or not separable": 41
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 41,
      "reasons": {
        "Phase wall not emitted or not separable": 41
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 41,
      "reasons": {
        "Phase wall not emitted or not separable": 41
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 41,
      "reasons": {
        "Phase wall not emitted or not separable": 41
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 41,
      "reasons": {
        "Phase wall not emitted or not separable": 41
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 41,
      "reasons": {
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 41,
      "reasons": {
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 41,
      "reasons": {
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 41,
      "reasons": {
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 41,
      "reasons": {
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 41,
      "reasons": {
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 41,
      "reasons": {
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 41,
      "reasons": {
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 41,
      "reasons": {
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 41,
      "reasons": {
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 41,
      "reasons": {
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 41,
      "reasons": {
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 41,
      "reasons": {
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 41,
      "reasons": {
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 41,
      "reasons": {
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 41,
      "reasons": {
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 41,
      "reasons": {
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 41,
      "reasons": {
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 41,
      "reasons": {
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 41,
      "reasons": {
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 41,
      "reasons": {
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 41,
      "reasons": {
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 41,
      "reasons": {
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 41,
      "reasons": {
        "Per-phase token counter not emitted": 41
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 1
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 1
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 1
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 1
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 41
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 41
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 41
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Toolchain version/inventory not recorded": 41
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Toolchain version/inventory not recorded": 41
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Toolchain version/inventory not recorded": 41
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Toolchain version/inventory not recorded": 41
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Toolchain version/inventory not recorded": 41
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 41,
      "reasons": {
        "Toolchain version/inventory not recorded": 41
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 41
      },
      "circumstances.concurrent_cells_end": {
        "none": 41
      },
      "circumstances.concurrent_cells_start": {
        "none": 41
      },
      "circumstances.load1_end": {
        "none": 41
      },
      "circumstances.load_samples": {
        "none": 41
      },
      "cost.usd": {
        "none": 1
      },
      "environment.account_class": {
        "none": 41
      },
      "environment.cores": {
        "none": 41
      },
      "environment.cpu_model": {
        "none": 41
      },
      "environment.ram_gib": {
        "none": 41
      },
      "environment.toolchains.elixir": {
        "none": 41
      },
      "environment.toolchains.erlang": {
        "none": 41
      },
      "environment.toolchains.node": {
        "none": 41
      },
      "environment.toolchains.other_inventory": {
        "none": 41
      },
      "environment.toolchains.ruby": {
        "none": 41
      },
      "environment.toolchains.rust": {
        "none": 41
      },
      "host.cpu": {
        "none": 41
      },
      "host.ram_gib": {
        "none": 41
      },
      "host.vcpu": {
        "none": 41
      },
      "recipe": {
        "none": 41
      },
      "setup.deps_source": {
        "none": 41
      },
      "timestamps.attempts": {
        "none": 41
      },
      "timestamps.phases.develop.end_utc": {
        "none": 41
      },
      "timestamps.phases.develop.start_utc": {
        "none": 41
      },
      "timestamps.phases.gate.end_utc": {
        "none": 41
      },
      "timestamps.phases.gate.start_utc": {
        "none": 41
      },
      "timestamps.phases.grade.end_utc": {
        "none": 41
      },
      "timestamps.phases.grade.start_utc": {
        "none": 41
      },
      "timestamps.phases.plan.end_utc": {
        "none": 41
      },
      "timestamps.phases.plan.start_utc": {
        "none": 41
      },
      "timestamps.phases.review.end_utc": {
        "none": 41
      },
      "timestamps.phases.review.start_utc": {
        "none": 41
      },
      "timestamps.phases.setup.end_utc": {
        "none": 41
      },
      "timestamps.phases.setup.start_utc": {
        "none": 41
      },
      "timestamps.phases.shape.end_utc": {
        "none": 41
      },
      "timestamps.phases.shape.start_utc": {
        "none": 41
      },
      "timing.phases_s.develop": {
        "none": 41
      },
      "timing.phases_s.gate": {
        "none": 41
      },
      "timing.phases_s.plan": {
        "none": 41
      },
      "timing.phases_s.review": {
        "none": 41
      },
      "timing.phases_s.setup": {
        "none": 41
      },
      "timing.phases_s.shape": {
        "none": 41
      },
      "tokens.phases.develop.cached_input": {
        "none": 41
      },
      "tokens.phases.develop.input": {
        "none": 41
      },
      "tokens.phases.develop.output": {
        "none": 41
      },
      "tokens.phases.develop.reasoning": {
        "none": 41
      },
      "tokens.phases.gate.cached_input": {
        "none": 41
      },
      "tokens.phases.gate.input": {
        "none": 41
      },
      "tokens.phases.gate.output": {
        "none": 41
      },
      "tokens.phases.gate.reasoning": {
        "none": 41
      },
      "tokens.phases.plan.cached_input": {
        "none": 41
      },
      "tokens.phases.plan.input": {
        "none": 41
      },
      "tokens.phases.plan.output": {
        "none": 41
      },
      "tokens.phases.plan.reasoning": {
        "none": 41
      },
      "tokens.phases.review.cached_input": {
        "none": 41
      },
      "tokens.phases.review.input": {
        "none": 41
      },
      "tokens.phases.review.output": {
        "none": 41
      },
      "tokens.phases.review.reasoning": {
        "none": 41
      },
      "tokens.phases.setup.cached_input": {
        "none": 41
      },
      "tokens.phases.setup.input": {
        "none": 41
      },
      "tokens.phases.setup.output": {
        "none": 41
      },
      "tokens.phases.setup.reasoning": {
        "none": 41
      },
      "tokens.phases.shape.cached_input": {
        "none": 41
      },
      "tokens.phases.shape.input": {
        "none": 41
      },
      "tokens.phases.shape.output": {
        "none": 41
      },
      "tokens.phases.shape.reasoning": {
        "none": 41
      },
      "tokens.total.cached_input": {
        "none": 1
      },
      "tokens.total.input": {
        "none": 1
      },
      "tokens.total.output": {
        "none": 1
      },
      "tokens.total.reasoning": {
        "none": 1
      },
      "tools.codex_cli": {
        "none": 41
      },
      "tools.grader": {
        "none": 41
      },
      "tools.runner": {
        "none": 41
      },
      "tools.toolchains.elixir": {
        "none": 41
      },
      "tools.toolchains.erlang": {
        "none": 41
      },
      "tools.toolchains.node": {
        "none": 41
      },
      "tools.toolchains.other_inventory": {
        "none": 41
      },
      "tools.toolchains.ruby": {
        "none": 41
      },
      "tools.toolchains.rust": {
        "none": 41
      }
    },
    "reconstructable": {}
  },
  "publication_reconciliation": {
    "disposition": "The current page preserves the control-arm mapping conflict: default-tools maps to multiple public exported arms, so its arm-level comparison is not reconstructed. Do not pool this page with r57b/r57c/r57d or the separate r57e replacement.",
    "original_execution_command": "not recorded in the public snapshot",
    "harness_source_commit": "absent; tools.harness values are wrapper fingerprints",
    "kogen_source_commit": "Public records mark the Kogen product commit not applicable for these harness records.",
    "raw_public_records": [
      "results/run-records/r57.jsonl",
      "results/cells.jsonl"
    ],
    "public_record_rebuild": "python3 reproduce/export_results.py; python3 reproduce/build_records.py; python3 reproduce/validate_round.py --round r57"
  },
  "round": "r57"
}
```
