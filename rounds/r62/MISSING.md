# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 18,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Boundary telemetry not retained": 18
      }
    },
    "circumstances.cap_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Boundary telemetry not retained": 18
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Boundary telemetry not retained": 18
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 18
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Boundary telemetry not retained": 18
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "No matching controller samples retained": 18
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 18,
      "reasons": {
        "Complete per-model billable vector unavailable": 18
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "No dated account-class receipt": 18
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "No per-cell CPU allocation receipt": 18
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "No per-cell CPU receipt": 18
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "No per-cell RAM receipt": 18
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Toolchain version/inventory not recorded": 18
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Toolchain version/inventory not recorded": 18
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Toolchain version/inventory not recorded": 18
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Toolchain version/inventory not recorded": 18
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Toolchain version/inventory not recorded": 18
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Toolchain version/inventory not recorded": 18
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 1,
      "reasons": {
        "Boolean receipt not recorded": 1
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 18,
      "reasons": {
        "No per-cell CPU receipt": 18
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 18,
      "reasons": {
        "No per-cell RAM receipt": 18
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 18,
      "reasons": {
        "No per-cell CPU allocation receipt": 18
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 1,
      "reasons": {
        "Invalid/environment cause requires evidence audit": 1
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 1,
      "reasons": {
        "No evidence-backed ITT classification": 1
      }
    },
    "kogen.best_candidate": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not recorded in available public metadata": 1
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
      "count": 12,
      "reasons": {
        "Not recorded in available public metadata": 12
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Dependency source not pinned per cell": 18
      }
    },
    "setup.kogen_sha": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 18
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 18,
      "reasons": {
        "Runner status does not establish normalized stop cause": 18
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Attempt boundary receipts unavailable": 18
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Absolute phase boundary not retained": 18
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Absolute phase boundary not retained": 18
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Absolute phase boundary not retained": 18
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Absolute phase boundary not retained": 18
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Absolute phase boundary not retained": 18
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Absolute phase boundary not retained": 18
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Absolute phase boundary not retained": 18
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Absolute phase boundary not retained": 18
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Absolute phase boundary not retained": 18
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Absolute phase boundary not retained": 18
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Absolute phase boundary not retained": 18
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Absolute phase boundary not retained": 18
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Absolute phase boundary not retained": 18
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Absolute phase boundary not retained": 18
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
      "count": 18,
      "reasons": {
        "Phase wall not emitted or not separable": 18
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 1,
      "reasons": {
        "Phase wall not emitted or not separable": 1
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 18,
      "reasons": {
        "Phase wall not emitted or not separable": 18
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 18,
      "reasons": {
        "Phase wall not emitted or not separable": 18
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 18,
      "reasons": {
        "Phase wall not emitted or not separable": 18
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 17,
      "reasons": {
        "Phase wall not emitted or not separable": 17
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
      "count": 18,
      "reasons": {
        "Per-phase token counter not emitted": 18
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 18,
      "reasons": {
        "Per-phase token counter not emitted": 18
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 18,
      "reasons": {
        "Per-phase token counter not emitted": 18
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 18,
      "reasons": {
        "Per-phase token counter not emitted": 18
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 18,
      "reasons": {
        "Per-phase token counter not emitted": 18
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 18,
      "reasons": {
        "Per-phase token counter not emitted": 18
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 18,
      "reasons": {
        "Per-phase token counter not emitted": 18
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 18,
      "reasons": {
        "Per-phase token counter not emitted": 18
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 18,
      "reasons": {
        "Per-phase token counter not emitted": 18
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 18,
      "reasons": {
        "Per-phase token counter not emitted": 18
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 18,
      "reasons": {
        "Per-phase token counter not emitted": 18
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 18,
      "reasons": {
        "Per-phase token counter not emitted": 18
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 18,
      "reasons": {
        "Per-phase token counter not emitted": 18
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 18,
      "reasons": {
        "Per-phase token counter not emitted": 18
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 18,
      "reasons": {
        "Per-phase token counter not emitted": 18
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 18,
      "reasons": {
        "Per-phase token counter not emitted": 18
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 17,
      "reasons": {
        "Per-phase token counter not emitted": 17
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 17,
      "reasons": {
        "Per-phase token counter not emitted": 17
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 17,
      "reasons": {
        "Per-phase token counter not emitted": 17
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 17,
      "reasons": {
        "Per-phase token counter not emitted": 17
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 18
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 18
      }
    },
    "tools.harness": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Not recorded in available public metadata": 12
      }
    },
    "tools.kogen": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 18
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 18
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Toolchain version/inventory not recorded": 18
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Toolchain version/inventory not recorded": 18
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Toolchain version/inventory not recorded": 18
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Toolchain version/inventory not recorded": 18
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Toolchain version/inventory not recorded": 18
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 18,
      "reasons": {
        "Toolchain version/inventory not recorded": 18
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 18
      },
      "circumstances.cap_start": {
        "none": 18
      },
      "circumstances.concurrent_cells_end": {
        "none": 18
      },
      "circumstances.concurrent_cells_start": {
        "none": 18
      },
      "circumstances.load1_end": {
        "none": 18
      },
      "circumstances.load_samples": {
        "none": 18
      },
      "cost.usd": {
        "none": 18
      },
      "environment.account_class": {
        "none": 18
      },
      "environment.cores": {
        "none": 18
      },
      "environment.cpu_model": {
        "none": 18
      },
      "environment.ram_gib": {
        "none": 18
      },
      "environment.toolchains.elixir": {
        "none": 18
      },
      "environment.toolchains.erlang": {
        "none": 18
      },
      "environment.toolchains.node": {
        "none": 18
      },
      "environment.toolchains.other_inventory": {
        "none": 18
      },
      "environment.toolchains.ruby": {
        "none": 18
      },
      "environment.toolchains.rust": {
        "none": 18
      },
      "grade.tests_ran": {
        "none": 1
      },
      "host.cpu": {
        "none": 18
      },
      "host.ram_gib": {
        "none": 18
      },
      "host.vcpu": {
        "none": 18
      },
      "itt.class": {
        "none": 1
      },
      "itt.evidence_ref": {
        "none": 1
      },
      "kogen.best_candidate": {
        "none": 1
      },
      "kogen.landed": {
        "none": 1
      },
      "setup.adapter_harness_sha": {
        "none": 12
      },
      "setup.deps_source": {
        "none": 18
      },
      "setup.kogen_sha": {
        "none": 18
      },
      "stop_reason": {
        "none": 18
      },
      "timestamps.attempts": {
        "none": 18
      },
      "timestamps.phases.develop.end_utc": {
        "none": 18
      },
      "timestamps.phases.develop.start_utc": {
        "none": 18
      },
      "timestamps.phases.gate.end_utc": {
        "none": 18
      },
      "timestamps.phases.gate.start_utc": {
        "none": 18
      },
      "timestamps.phases.grade.end_utc": {
        "none": 18
      },
      "timestamps.phases.grade.start_utc": {
        "none": 18
      },
      "timestamps.phases.plan.end_utc": {
        "none": 18
      },
      "timestamps.phases.plan.start_utc": {
        "none": 18
      },
      "timestamps.phases.review.end_utc": {
        "none": 18
      },
      "timestamps.phases.review.start_utc": {
        "none": 18
      },
      "timestamps.phases.setup.end_utc": {
        "none": 18
      },
      "timestamps.phases.setup.start_utc": {
        "none": 18
      },
      "timestamps.phases.shape.end_utc": {
        "none": 18
      },
      "timestamps.phases.shape.start_utc": {
        "none": 18
      },
      "timing.phases_s.develop": {
        "none": 1
      },
      "timing.phases_s.gate": {
        "none": 18
      },
      "timing.phases_s.grade": {
        "none": 1
      },
      "timing.phases_s.plan": {
        "none": 18
      },
      "timing.phases_s.review": {
        "none": 18
      },
      "timing.phases_s.setup": {
        "none": 18
      },
      "timing.phases_s.shape": {
        "none": 17
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
        "none": 18
      },
      "tokens.phases.gate.input": {
        "none": 18
      },
      "tokens.phases.gate.output": {
        "none": 18
      },
      "tokens.phases.gate.reasoning": {
        "none": 18
      },
      "tokens.phases.plan.cached_input": {
        "none": 18
      },
      "tokens.phases.plan.input": {
        "none": 18
      },
      "tokens.phases.plan.output": {
        "none": 18
      },
      "tokens.phases.plan.reasoning": {
        "none": 18
      },
      "tokens.phases.review.cached_input": {
        "none": 18
      },
      "tokens.phases.review.input": {
        "none": 18
      },
      "tokens.phases.review.output": {
        "none": 18
      },
      "tokens.phases.review.reasoning": {
        "none": 18
      },
      "tokens.phases.setup.cached_input": {
        "none": 18
      },
      "tokens.phases.setup.input": {
        "none": 18
      },
      "tokens.phases.setup.output": {
        "none": 18
      },
      "tokens.phases.setup.reasoning": {
        "none": 18
      },
      "tokens.phases.shape.cached_input": {
        "none": 17
      },
      "tokens.phases.shape.input": {
        "none": 17
      },
      "tokens.phases.shape.output": {
        "none": 17
      },
      "tokens.phases.shape.reasoning": {
        "none": 17
      },
      "tools.codex_cli": {
        "none": 18
      },
      "tools.grader": {
        "none": 18
      },
      "tools.harness": {
        "none": 12
      },
      "tools.kogen": {
        "none": 18
      },
      "tools.runner": {
        "none": 18
      },
      "tools.toolchains.elixir": {
        "none": 18
      },
      "tools.toolchains.erlang": {
        "none": 18
      },
      "tools.toolchains.node": {
        "none": 18
      },
      "tools.toolchains.other_inventory": {
        "none": 18
      },
      "tools.toolchains.ruby": {
        "none": 18
      },
      "tools.toolchains.rust": {
        "none": 18
      }
    },
    "reconstructable": {}
  },
  "round": "r62"
}
```
