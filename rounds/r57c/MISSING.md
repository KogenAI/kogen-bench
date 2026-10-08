# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 80,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Boundary telemetry not retained": 80
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Boundary telemetry not retained": 80
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 80
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Boundary telemetry not retained": 80
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "No matching controller samples retained": 80
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "No dated account-class receipt": 80
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "No per-cell CPU allocation receipt": 80
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "No per-cell CPU receipt": 80
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "No per-cell RAM receipt": 80
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Toolchain version/inventory not recorded": 80
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Toolchain version/inventory not recorded": 80
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Toolchain version/inventory not recorded": 80
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Toolchain version/inventory not recorded": 80
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Toolchain version/inventory not recorded": 80
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Toolchain version/inventory not recorded": 80
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 80,
      "reasons": {
        "No per-cell CPU receipt": 80
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 80,
      "reasons": {
        "No per-cell RAM receipt": 80
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 80,
      "reasons": {
        "No per-cell CPU allocation receipt": 80
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Not recorded in available public metadata": 80
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Dependency source not pinned per cell": 80
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Attempt boundary receipts unavailable": 80
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Absolute phase boundary not retained": 80
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Absolute phase boundary not retained": 80
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Absolute phase boundary not retained": 80
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Absolute phase boundary not retained": 80
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Absolute phase boundary not retained": 80
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Absolute phase boundary not retained": 80
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Absolute phase boundary not retained": 80
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Absolute phase boundary not retained": 80
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Absolute phase boundary not retained": 80
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Absolute phase boundary not retained": 80
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Absolute phase boundary not retained": 80
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Absolute phase boundary not retained": 80
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Absolute phase boundary not retained": 80
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Absolute phase boundary not retained": 80
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 80,
      "reasons": {
        "Phase wall not emitted or not separable": 80
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 80,
      "reasons": {
        "Phase wall not emitted or not separable": 80
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 80,
      "reasons": {
        "Phase wall not emitted or not separable": 80
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 80,
      "reasons": {
        "Phase wall not emitted or not separable": 80
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 80,
      "reasons": {
        "Phase wall not emitted or not separable": 80
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 80,
      "reasons": {
        "Phase wall not emitted or not separable": 80
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 80,
      "reasons": {
        "Per-phase token counter not emitted": 80
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 80,
      "reasons": {
        "Per-phase token counter not emitted": 80
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 80,
      "reasons": {
        "Per-phase token counter not emitted": 80
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 80,
      "reasons": {
        "Per-phase token counter not emitted": 80
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 80,
      "reasons": {
        "Per-phase token counter not emitted": 80
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 80,
      "reasons": {
        "Per-phase token counter not emitted": 80
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 80,
      "reasons": {
        "Per-phase token counter not emitted": 80
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 80,
      "reasons": {
        "Per-phase token counter not emitted": 80
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 80,
      "reasons": {
        "Per-phase token counter not emitted": 80
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 80,
      "reasons": {
        "Per-phase token counter not emitted": 80
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 80,
      "reasons": {
        "Per-phase token counter not emitted": 80
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 80,
      "reasons": {
        "Per-phase token counter not emitted": 80
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 80,
      "reasons": {
        "Per-phase token counter not emitted": 80
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 80,
      "reasons": {
        "Per-phase token counter not emitted": 80
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 80,
      "reasons": {
        "Per-phase token counter not emitted": 80
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 80,
      "reasons": {
        "Per-phase token counter not emitted": 80
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 80,
      "reasons": {
        "Per-phase token counter not emitted": 80
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 80,
      "reasons": {
        "Per-phase token counter not emitted": 80
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 80,
      "reasons": {
        "Per-phase token counter not emitted": 80
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 80,
      "reasons": {
        "Per-phase token counter not emitted": 80
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 80,
      "reasons": {
        "Per-phase token counter not emitted": 80
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 80,
      "reasons": {
        "Per-phase token counter not emitted": 80
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 80,
      "reasons": {
        "Per-phase token counter not emitted": 80
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 80,
      "reasons": {
        "Per-phase token counter not emitted": 80
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 80
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 80
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 80
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Toolchain version/inventory not recorded": 80
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Toolchain version/inventory not recorded": 80
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Toolchain version/inventory not recorded": 80
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Toolchain version/inventory not recorded": 80
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Toolchain version/inventory not recorded": 80
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 80,
      "reasons": {
        "Toolchain version/inventory not recorded": 80
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 80
      },
      "circumstances.concurrent_cells_end": {
        "none": 80
      },
      "circumstances.concurrent_cells_start": {
        "none": 80
      },
      "circumstances.load1_end": {
        "none": 80
      },
      "circumstances.load_samples": {
        "none": 80
      },
      "environment.account_class": {
        "none": 80
      },
      "environment.cores": {
        "none": 80
      },
      "environment.cpu_model": {
        "none": 80
      },
      "environment.ram_gib": {
        "none": 80
      },
      "environment.toolchains.elixir": {
        "none": 80
      },
      "environment.toolchains.erlang": {
        "none": 80
      },
      "environment.toolchains.node": {
        "none": 80
      },
      "environment.toolchains.other_inventory": {
        "none": 80
      },
      "environment.toolchains.ruby": {
        "none": 80
      },
      "environment.toolchains.rust": {
        "none": 80
      },
      "host.cpu": {
        "none": 80
      },
      "host.ram_gib": {
        "none": 80
      },
      "host.vcpu": {
        "none": 80
      },
      "recipe": {
        "none": 80
      },
      "setup.deps_source": {
        "none": 80
      },
      "timestamps.attempts": {
        "none": 80
      },
      "timestamps.phases.develop.end_utc": {
        "none": 80
      },
      "timestamps.phases.develop.start_utc": {
        "none": 80
      },
      "timestamps.phases.gate.end_utc": {
        "none": 80
      },
      "timestamps.phases.gate.start_utc": {
        "none": 80
      },
      "timestamps.phases.grade.end_utc": {
        "none": 80
      },
      "timestamps.phases.grade.start_utc": {
        "none": 80
      },
      "timestamps.phases.plan.end_utc": {
        "none": 80
      },
      "timestamps.phases.plan.start_utc": {
        "none": 80
      },
      "timestamps.phases.review.end_utc": {
        "none": 80
      },
      "timestamps.phases.review.start_utc": {
        "none": 80
      },
      "timestamps.phases.setup.end_utc": {
        "none": 80
      },
      "timestamps.phases.setup.start_utc": {
        "none": 80
      },
      "timestamps.phases.shape.end_utc": {
        "none": 80
      },
      "timestamps.phases.shape.start_utc": {
        "none": 80
      },
      "timing.phases_s.develop": {
        "none": 80
      },
      "timing.phases_s.gate": {
        "none": 80
      },
      "timing.phases_s.plan": {
        "none": 80
      },
      "timing.phases_s.review": {
        "none": 80
      },
      "timing.phases_s.setup": {
        "none": 80
      },
      "timing.phases_s.shape": {
        "none": 80
      },
      "tokens.phases.develop.cached_input": {
        "none": 80
      },
      "tokens.phases.develop.input": {
        "none": 80
      },
      "tokens.phases.develop.output": {
        "none": 80
      },
      "tokens.phases.develop.reasoning": {
        "none": 80
      },
      "tokens.phases.gate.cached_input": {
        "none": 80
      },
      "tokens.phases.gate.input": {
        "none": 80
      },
      "tokens.phases.gate.output": {
        "none": 80
      },
      "tokens.phases.gate.reasoning": {
        "none": 80
      },
      "tokens.phases.plan.cached_input": {
        "none": 80
      },
      "tokens.phases.plan.input": {
        "none": 80
      },
      "tokens.phases.plan.output": {
        "none": 80
      },
      "tokens.phases.plan.reasoning": {
        "none": 80
      },
      "tokens.phases.review.cached_input": {
        "none": 80
      },
      "tokens.phases.review.input": {
        "none": 80
      },
      "tokens.phases.review.output": {
        "none": 80
      },
      "tokens.phases.review.reasoning": {
        "none": 80
      },
      "tokens.phases.setup.cached_input": {
        "none": 80
      },
      "tokens.phases.setup.input": {
        "none": 80
      },
      "tokens.phases.setup.output": {
        "none": 80
      },
      "tokens.phases.setup.reasoning": {
        "none": 80
      },
      "tokens.phases.shape.cached_input": {
        "none": 80
      },
      "tokens.phases.shape.input": {
        "none": 80
      },
      "tokens.phases.shape.output": {
        "none": 80
      },
      "tokens.phases.shape.reasoning": {
        "none": 80
      },
      "tools.codex_cli": {
        "none": 80
      },
      "tools.grader": {
        "none": 80
      },
      "tools.runner": {
        "none": 80
      },
      "tools.toolchains.elixir": {
        "none": 80
      },
      "tools.toolchains.erlang": {
        "none": 80
      },
      "tools.toolchains.node": {
        "none": 80
      },
      "tools.toolchains.other_inventory": {
        "none": 80
      },
      "tools.toolchains.ruby": {
        "none": 80
      },
      "tools.toolchains.rust": {
        "none": 80
      }
    },
    "reconstructable": {}
  },
  "publication_reconciliation": {
    "disposition": "Keep this additional Elixir repetition lane separate from r57/r57b/r57d and r57e. Public row summaries are descriptive; they do not reproduce the pooled interval analysis.",
    "original_execution_command": "not recorded in the public snapshot",
    "harness_source_commit": "absent; tools.harness values are wrapper fingerprints",
    "kogen_source_commit": "Public records mark the Kogen product commit not applicable for these harness records.",
    "raw_public_records": [
      "results/run-records/r57c.jsonl",
      "results/cells.jsonl"
    ],
    "public_record_rebuild": "python3 reproduce/export_results.py; python3 reproduce/build_records.py; python3 reproduce/validate_round.py --round r57c"
  },
  "round": "r57c"
}
```
