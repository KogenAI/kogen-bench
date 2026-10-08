# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 90,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Boundary telemetry not retained": 90
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Boundary telemetry not retained": 90
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 90
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Boundary telemetry not retained": 90
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "No matching controller samples retained": 90
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 90,
      "reasons": {
        "Complete per-model billable vector unavailable": 90
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "No dated account-class receipt": 90
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "No per-cell CPU allocation receipt": 90
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "No per-cell CPU receipt": 90
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "No per-cell RAM receipt": 90
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Toolchain version/inventory not recorded": 90
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Toolchain version/inventory not recorded": 90
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Toolchain version/inventory not recorded": 90
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Toolchain version/inventory not recorded": 90
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 26,
      "reasons": {
        "Boolean receipt not recorded": 26
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 90,
      "reasons": {
        "No per-cell CPU receipt": 90
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 90,
      "reasons": {
        "No per-cell RAM receipt": 90
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 90,
      "reasons": {
        "No per-cell CPU allocation receipt": 90
      }
    },
    "kogen.best_candidate": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 26,
      "reasons": {
        "Not recorded in available public metadata": 26
      }
    },
    "kogen.landed": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 3,
      "reasons": {
        "Kogen report status absent": 3
      }
    },
    "setup.adapter_harness_sha": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Not recorded in available public metadata": 90
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 26,
      "reasons": {
        "Runner status does not establish normalized stop cause": 26
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 20,
      "reasons": {
        "Value withheld by PRIVATE.md": 20
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Attempt boundary receipts unavailable": 90
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Absolute phase boundary not retained": 90
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Absolute phase boundary not retained": 90
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 7,
      "reasons": {
        "Absolute phase boundary not retained": 7
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 7,
      "reasons": {
        "Absolute phase boundary not retained": 7
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Absolute phase boundary not retained": 90
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Absolute phase boundary not retained": 90
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Absolute phase boundary not retained": 90
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Absolute phase boundary not retained": 90
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Absolute phase boundary not retained": 90
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Absolute phase boundary not retained": 90
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Absolute phase boundary not retained": 90
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Absolute phase boundary not retained": 90
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "Phase wall not emitted or not separable": 6
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 7,
      "reasons": {
        "Phase wall not emitted or not separable": 7
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 26,
      "reasons": {
        "Phase wall not emitted or not separable": 26
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 48,
      "reasons": {
        "Phase wall not emitted or not separable": 48
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 90,
      "reasons": {
        "Phase wall not emitted or not separable": 90
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 90,
      "reasons": {
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 90,
      "reasons": {
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 90,
      "reasons": {
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 90,
      "reasons": {
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 48,
      "reasons": {
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 90,
      "reasons": {
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 90,
      "reasons": {
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 90,
      "reasons": {
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 90,
      "reasons": {
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 90,
      "reasons": {
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 90,
      "reasons": {
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 90,
      "reasons": {
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 90,
      "reasons": {
        "Per-phase token counter not emitted": 90
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Per-phase token counter not emitted": 86
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Per-phase token counter not emitted": 86
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Per-phase token counter not emitted": 86
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Per-phase token counter not emitted": 86
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 90
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 90
      }
    },
    "tools.harness": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Not recorded in available public metadata": 90
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 90
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Toolchain version/inventory not recorded": 90
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Toolchain version/inventory not recorded": 90
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Toolchain version/inventory not recorded": 90
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Toolchain version/inventory not recorded": 90
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Toolchain version/inventory not recorded": 90
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 90,
      "reasons": {
        "Toolchain version/inventory not recorded": 90
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 90
      },
      "circumstances.concurrent_cells_end": {
        "none": 90
      },
      "circumstances.concurrent_cells_start": {
        "none": 90
      },
      "circumstances.load1_end": {
        "none": 90
      },
      "circumstances.load_samples": {
        "none": 90
      },
      "cost.usd": {
        "none": 90
      },
      "environment.account_class": {
        "none": 90
      },
      "environment.cores": {
        "none": 90
      },
      "environment.cpu_model": {
        "none": 90
      },
      "environment.ram_gib": {
        "none": 90
      },
      "environment.toolchains.node": {
        "none": 90
      },
      "environment.toolchains.other_inventory": {
        "none": 90
      },
      "environment.toolchains.ruby": {
        "none": 90
      },
      "environment.toolchains.rust": {
        "none": 90
      },
      "grade.tests_ran": {
        "none": 26
      },
      "host.cpu": {
        "none": 90
      },
      "host.ram_gib": {
        "none": 90
      },
      "host.vcpu": {
        "none": 90
      },
      "kogen.best_candidate": {
        "none": 26
      },
      "kogen.landed": {
        "none": 3
      },
      "setup.adapter_harness_sha": {
        "none": 90
      },
      "stop_reason": {
        "none": 26
      },
      "task.base_repo": {
        "none": 20
      },
      "timestamps.attempts": {
        "none": 90
      },
      "timestamps.phases.develop.end_utc": {
        "none": 90
      },
      "timestamps.phases.develop.start_utc": {
        "none": 90
      },
      "timestamps.phases.gate.end_utc": {
        "none": 7
      },
      "timestamps.phases.gate.start_utc": {
        "none": 7
      },
      "timestamps.phases.grade.end_utc": {
        "none": 90
      },
      "timestamps.phases.grade.start_utc": {
        "none": 90
      },
      "timestamps.phases.plan.end_utc": {
        "none": 90
      },
      "timestamps.phases.plan.start_utc": {
        "none": 90
      },
      "timestamps.phases.review.end_utc": {
        "none": 90
      },
      "timestamps.phases.review.start_utc": {
        "none": 90
      },
      "timestamps.phases.shape.end_utc": {
        "none": 90
      },
      "timestamps.phases.shape.start_utc": {
        "none": 90
      },
      "timing.phases_s.develop": {
        "none": 6
      },
      "timing.phases_s.gate": {
        "none": 7
      },
      "timing.phases_s.grade": {
        "none": 26
      },
      "timing.phases_s.plan": {
        "none": 48
      },
      "timing.phases_s.review": {
        "none": 90
      },
      "tokens.phases.develop.cached_input": {
        "none": 6
      },
      "tokens.phases.develop.input": {
        "none": 6
      },
      "tokens.phases.develop.output": {
        "none": 6
      },
      "tokens.phases.develop.reasoning": {
        "none": 6
      },
      "tokens.phases.gate.cached_input": {
        "none": 90
      },
      "tokens.phases.gate.input": {
        "none": 90
      },
      "tokens.phases.gate.output": {
        "none": 90
      },
      "tokens.phases.gate.reasoning": {
        "none": 90
      },
      "tokens.phases.plan.cached_input": {
        "none": 48
      },
      "tokens.phases.plan.input": {
        "none": 48
      },
      "tokens.phases.plan.output": {
        "none": 48
      },
      "tokens.phases.plan.reasoning": {
        "none": 48
      },
      "tokens.phases.review.cached_input": {
        "none": 90
      },
      "tokens.phases.review.input": {
        "none": 90
      },
      "tokens.phases.review.output": {
        "none": 90
      },
      "tokens.phases.review.reasoning": {
        "none": 90
      },
      "tokens.phases.setup.cached_input": {
        "none": 90
      },
      "tokens.phases.setup.input": {
        "none": 90
      },
      "tokens.phases.setup.output": {
        "none": 90
      },
      "tokens.phases.setup.reasoning": {
        "none": 90
      },
      "tokens.phases.shape.cached_input": {
        "none": 86
      },
      "tokens.phases.shape.input": {
        "none": 86
      },
      "tokens.phases.shape.output": {
        "none": 86
      },
      "tokens.phases.shape.reasoning": {
        "none": 86
      },
      "tools.codex_cli": {
        "none": 90
      },
      "tools.grader": {
        "none": 90
      },
      "tools.harness": {
        "none": 90
      },
      "tools.runner": {
        "none": 90
      },
      "tools.toolchains.elixir": {
        "none": 90
      },
      "tools.toolchains.erlang": {
        "none": 90
      },
      "tools.toolchains.node": {
        "none": 90
      },
      "tools.toolchains.other_inventory": {
        "none": 90
      },
      "tools.toolchains.ruby": {
        "none": 90
      },
      "tools.toolchains.rust": {
        "none": 90
      }
    },
    "reconstructable": {}
  },
  "round": "r65b"
}
```
