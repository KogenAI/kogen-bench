# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 16,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Boundary telemetry not retained": 16
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Boundary telemetry not retained": 16
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 16
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Boundary telemetry not retained": 16
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "No matching controller samples retained": 16
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 16,
      "reasons": {
        "Complete per-model billable vector unavailable": 16
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "No dated account-class receipt": 16
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "No per-cell CPU allocation receipt": 16
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "No per-cell CPU receipt": 16
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "No per-cell RAM receipt": 16
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Toolchain version/inventory not recorded": 16
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Toolchain version/inventory not recorded": 16
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Toolchain version/inventory not recorded": 16
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Toolchain version/inventory not recorded": 16
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 3,
      "reasons": {
        "Boolean receipt not recorded": 3
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 16,
      "reasons": {
        "No per-cell CPU receipt": 16
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 16,
      "reasons": {
        "No per-cell RAM receipt": 16
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 16,
      "reasons": {
        "No per-cell CPU allocation receipt": 16
      }
    },
    "kogen.best_candidate": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 3,
      "reasons": {
        "Not recorded in available public metadata": 3
      }
    },
    "kogen.landed": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Kogen report status absent": 1
      }
    },
    "setup.adapter_harness_sha": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Not recorded in available public metadata": 16
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 3,
      "reasons": {
        "Runner status does not establish normalized stop cause": 3
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Attempt boundary receipts unavailable": 16
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Absolute phase boundary not retained": 16
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Absolute phase boundary not retained": 16
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Absolute phase boundary not retained": 1
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Absolute phase boundary not retained": 1
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Absolute phase boundary not retained": 16
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Absolute phase boundary not retained": 16
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Absolute phase boundary not retained": 16
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Absolute phase boundary not retained": 16
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Absolute phase boundary not retained": 16
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Absolute phase boundary not retained": 16
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Absolute phase boundary not retained": 16
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Absolute phase boundary not retained": 16
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 1,
      "reasons": {
        "Phase wall not emitted or not separable": 1
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 1,
      "reasons": {
        "Phase wall not emitted or not separable": 1
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 3,
      "reasons": {
        "Phase wall not emitted or not separable": 3
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 8,
      "reasons": {
        "Phase wall not emitted or not separable": 8
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 16,
      "reasons": {
        "Phase wall not emitted or not separable": 16
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Per-phase token counter not emitted": 1
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Per-phase token counter not emitted": 1
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Per-phase token counter not emitted": 1
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Per-phase token counter not emitted": 1
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 16,
      "reasons": {
        "Per-phase token counter not emitted": 16
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 16,
      "reasons": {
        "Per-phase token counter not emitted": 16
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 16,
      "reasons": {
        "Per-phase token counter not emitted": 16
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 16,
      "reasons": {
        "Per-phase token counter not emitted": 16
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 16,
      "reasons": {
        "Per-phase token counter not emitted": 16
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 16,
      "reasons": {
        "Per-phase token counter not emitted": 16
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 16,
      "reasons": {
        "Per-phase token counter not emitted": 16
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 16,
      "reasons": {
        "Per-phase token counter not emitted": 16
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 16,
      "reasons": {
        "Per-phase token counter not emitted": 16
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 16,
      "reasons": {
        "Per-phase token counter not emitted": 16
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 16,
      "reasons": {
        "Per-phase token counter not emitted": 16
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 16,
      "reasons": {
        "Per-phase token counter not emitted": 16
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 16
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 16
      }
    },
    "tools.harness": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Not recorded in available public metadata": 16
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 16
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Toolchain version/inventory not recorded": 16
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Toolchain version/inventory not recorded": 16
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Toolchain version/inventory not recorded": 16
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Toolchain version/inventory not recorded": 16
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Toolchain version/inventory not recorded": 16
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 16,
      "reasons": {
        "Toolchain version/inventory not recorded": 16
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 16
      },
      "circumstances.concurrent_cells_end": {
        "none": 16
      },
      "circumstances.concurrent_cells_start": {
        "none": 16
      },
      "circumstances.load1_end": {
        "none": 16
      },
      "circumstances.load_samples": {
        "none": 16
      },
      "cost.usd": {
        "none": 16
      },
      "environment.account_class": {
        "none": 16
      },
      "environment.cores": {
        "none": 16
      },
      "environment.cpu_model": {
        "none": 16
      },
      "environment.ram_gib": {
        "none": 16
      },
      "environment.toolchains.node": {
        "none": 16
      },
      "environment.toolchains.other_inventory": {
        "none": 16
      },
      "environment.toolchains.ruby": {
        "none": 16
      },
      "environment.toolchains.rust": {
        "none": 16
      },
      "grade.tests_ran": {
        "none": 3
      },
      "host.cpu": {
        "none": 16
      },
      "host.ram_gib": {
        "none": 16
      },
      "host.vcpu": {
        "none": 16
      },
      "kogen.best_candidate": {
        "none": 3
      },
      "kogen.landed": {
        "none": 1
      },
      "setup.adapter_harness_sha": {
        "none": 16
      },
      "stop_reason": {
        "none": 3
      },
      "timestamps.attempts": {
        "none": 16
      },
      "timestamps.phases.develop.end_utc": {
        "none": 16
      },
      "timestamps.phases.develop.start_utc": {
        "none": 16
      },
      "timestamps.phases.gate.end_utc": {
        "none": 1
      },
      "timestamps.phases.gate.start_utc": {
        "none": 1
      },
      "timestamps.phases.grade.end_utc": {
        "none": 16
      },
      "timestamps.phases.grade.start_utc": {
        "none": 16
      },
      "timestamps.phases.plan.end_utc": {
        "none": 16
      },
      "timestamps.phases.plan.start_utc": {
        "none": 16
      },
      "timestamps.phases.review.end_utc": {
        "none": 16
      },
      "timestamps.phases.review.start_utc": {
        "none": 16
      },
      "timestamps.phases.shape.end_utc": {
        "none": 16
      },
      "timestamps.phases.shape.start_utc": {
        "none": 16
      },
      "timing.phases_s.develop": {
        "none": 1
      },
      "timing.phases_s.gate": {
        "none": 1
      },
      "timing.phases_s.grade": {
        "none": 3
      },
      "timing.phases_s.plan": {
        "none": 8
      },
      "timing.phases_s.review": {
        "none": 16
      },
      "tokens.phases.develop.cached_input": {
        "none": 1
      },
      "tokens.phases.develop.input": {
        "none": 1
      },
      "tokens.phases.develop.output": {
        "none": 1
      },
      "tokens.phases.develop.reasoning": {
        "none": 1
      },
      "tokens.phases.gate.cached_input": {
        "none": 16
      },
      "tokens.phases.gate.input": {
        "none": 16
      },
      "tokens.phases.gate.output": {
        "none": 16
      },
      "tokens.phases.gate.reasoning": {
        "none": 16
      },
      "tokens.phases.plan.cached_input": {
        "none": 8
      },
      "tokens.phases.plan.input": {
        "none": 8
      },
      "tokens.phases.plan.output": {
        "none": 8
      },
      "tokens.phases.plan.reasoning": {
        "none": 8
      },
      "tokens.phases.review.cached_input": {
        "none": 16
      },
      "tokens.phases.review.input": {
        "none": 16
      },
      "tokens.phases.review.output": {
        "none": 16
      },
      "tokens.phases.review.reasoning": {
        "none": 16
      },
      "tokens.phases.setup.cached_input": {
        "none": 16
      },
      "tokens.phases.setup.input": {
        "none": 16
      },
      "tokens.phases.setup.output": {
        "none": 16
      },
      "tokens.phases.setup.reasoning": {
        "none": 16
      },
      "tokens.phases.shape.cached_input": {
        "none": 15
      },
      "tokens.phases.shape.input": {
        "none": 15
      },
      "tokens.phases.shape.output": {
        "none": 15
      },
      "tokens.phases.shape.reasoning": {
        "none": 15
      },
      "tools.codex_cli": {
        "none": 16
      },
      "tools.grader": {
        "none": 16
      },
      "tools.harness": {
        "none": 16
      },
      "tools.runner": {
        "none": 16
      },
      "tools.toolchains.elixir": {
        "none": 16
      },
      "tools.toolchains.erlang": {
        "none": 16
      },
      "tools.toolchains.node": {
        "none": 16
      },
      "tools.toolchains.other_inventory": {
        "none": 16
      },
      "tools.toolchains.ruby": {
        "none": 16
      },
      "tools.toolchains.rust": {
        "none": 16
      }
    },
    "reconstructable": {}
  },
  "round": "r65"
}
```
