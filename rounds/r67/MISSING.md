# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 61,
  "fields": {
    "arm": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Arm label not retained": 60
      }
    },
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Boundary telemetry not retained": 61
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Boundary telemetry not retained": 61
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 61
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Boundary telemetry not retained": 61
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "No matching controller samples retained": 61
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Not available for ungraded delivery": 60
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Not available for ungraded delivery": 60
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Not available for ungraded delivery": 60
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Not available for ungraded delivery": 60
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Complete per-model billable vector unavailable": 1,
        "Not available for ungraded delivery": 60
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "No dated account-class receipt": 61
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "No per-cell CPU allocation receipt": 1,
        "Not available for ungraded delivery": 60
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "No per-cell CPU receipt": 1,
        "Not available for ungraded delivery": 60
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "No per-cell RAM receipt": 1,
        "Not available for ungraded delivery": 60
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Toolchain version/inventory not recorded": 1
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Toolchain version/inventory not recorded": 1
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Toolchain version/inventory not recorded": 1
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Toolchain version/inventory not recorded": 1
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Toolchain version/inventory not recorded": 1
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Toolchain version/inventory not recorded": 1
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 60,
      "reasons": {
        "No official grade in the public snapshot": 60
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 61,
      "reasons": {
        "Boolean receipt not recorded": 1,
        "No official grade in the public snapshot": 60
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 60,
      "reasons": {
        "No official grade in the public snapshot": 60
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 61,
      "reasons": {
        "No per-cell CPU receipt": 1,
        "Not available for ungraded delivery": 60
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 61,
      "reasons": {
        "No per-cell RAM receipt": 1,
        "Not available for ungraded delivery": 60
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 60,
      "reasons": {
        "Not available for ungraded delivery": 60
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 61,
      "reasons": {
        "No per-cell CPU allocation receipt": 1,
        "Not available for ungraded delivery": 60
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 61,
      "reasons": {
        "Invalid/environment cause requires evidence audit": 1,
        "Ungraded delivery needs evidence audit": 60
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 60,
      "reasons": {
        "No captured cohort launch receipt": 60
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 61,
      "reasons": {
        "No audited ITT receipt": 60,
        "No evidence-backed ITT classification": 1
      }
    },
    "kogen.best_candidate": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Not recorded in available public metadata": 1
      }
    },
    "kogen.landed": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Kogen report status absent": 1,
        "Not available for ungraded delivery": 60
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 60,
      "reasons": {
        "No official grade in the public snapshot": 60
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Not available for ungraded delivery": 60
      }
    },
    "setup.adapter_harness_sha": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Not recorded in available public metadata": 61
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Dependency source not pinned per cell": 61
      }
    },
    "setup.kogen_sha": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 1,
        "Not available for ungraded delivery": 60
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 61,
      "reasons": {
        "No normalized stop receipt": 60,
        "Runner status does not establish normalized stop cause": 1
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Not available for ungraded delivery": 60
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Attempt boundary receipts unavailable": 61
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Absolute phase boundary not retained": 61
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Absolute phase boundary not retained": 61
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Absolute phase boundary not retained": 60
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Absolute phase boundary not retained": 60
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Absolute phase boundary not retained": 61
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Absolute phase boundary not retained": 61
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Absolute phase boundary not retained": 61
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Absolute phase boundary not retained": 61
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Absolute phase boundary not retained": 61
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Absolute phase boundary not retained": 61
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Absolute phase boundary not retained": 61
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Absolute phase boundary not retained": 61
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Phase wall not emitted or not separable": 1
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Phase wall not emitted or not separable": 1
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Phase wall not emitted or not separable": 1
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Phase wall not emitted or not separable": 1
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Phase wall not emitted or not separable": 1
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 60,
      "reasons": {
        "Not available for ungraded delivery": 60
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 60,
      "reasons": {
        "Not available for ungraded delivery": 60
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Per-phase token counter not emitted": 1
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Per-phase token counter not emitted": 1
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Per-phase token counter not emitted": 1
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Per-phase token counter not emitted": 1
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Per-phase token counter not emitted": 1
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Per-phase token counter not emitted": 1
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Per-phase token counter not emitted": 1
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Per-phase token counter not emitted": 1
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Not available for ungraded delivery": 60
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Not available for ungraded delivery": 60
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Not available for ungraded delivery": 60
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Not available for ungraded delivery": 60
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Per-phase token counter not emitted": 1
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Per-phase token counter not emitted": 1
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Per-phase token counter not emitted": 1
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Per-phase token counter not emitted": 1
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Per-phase token counter not emitted": 1
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Per-phase token counter not emitted": 1
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Per-phase token counter not emitted": 1
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Per-phase token counter not emitted": 1
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Per-phase token counter not emitted": 1
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Per-phase token counter not emitted": 1
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Per-phase token counter not emitted": 1
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Per-phase token counter not emitted": 1
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Not available for ungraded delivery": 60
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Not available for ungraded delivery": 60
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Not available for ungraded delivery": 60
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Not available for ungraded delivery": 60
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 1,
        "Not available for ungraded delivery": 60
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 1,
        "Not available for ungraded delivery": 60
      }
    },
    "tools.harness": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Not recorded in available public metadata": 61
      }
    },
    "tools.kogen": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 1,
        "Not available for ungraded delivery": 60
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 1,
        "Not available for ungraded delivery": 60
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Toolchain version/inventory not recorded": 1
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Toolchain version/inventory not recorded": 1
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Toolchain version/inventory not recorded": 1
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Toolchain version/inventory not recorded": 1
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Toolchain version/inventory not recorded": 1
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 60,
        "Toolchain version/inventory not recorded": 1
      }
    }
  },
  "gap_sources": {
    "lost": {
      "arm": {
        "none": 60
      },
      "circumstances.cap_end": {
        "none": 61
      },
      "circumstances.concurrent_cells_end": {
        "none": 61
      },
      "circumstances.concurrent_cells_start": {
        "none": 61
      },
      "circumstances.load1_end": {
        "none": 61
      },
      "circumstances.load_samples": {
        "none": 61
      },
      "cost.accounting": {
        "none": 60
      },
      "cost.calculator_version": {
        "none": 60
      },
      "cost.long_context_reconciled": {
        "none": 60
      },
      "cost.price_table_version": {
        "none": 60
      },
      "cost.usd": {
        "none": 61
      },
      "environment.account_class": {
        "none": 61
      },
      "environment.cores": {
        "none": 61
      },
      "environment.cpu_model": {
        "none": 61
      },
      "environment.ram_gib": {
        "none": 61
      },
      "environment.toolchains.elixir": {
        "none": 61
      },
      "environment.toolchains.erlang": {
        "none": 61
      },
      "environment.toolchains.node": {
        "none": 61
      },
      "environment.toolchains.other_inventory": {
        "none": 61
      },
      "environment.toolchains.ruby": {
        "none": 61
      },
      "environment.toolchains.rust": {
        "none": 61
      },
      "grade.grader": {
        "not re-derivable from the public record": 60
      },
      "grade.tests_ran": {
        "none": 1,
        "not re-derivable from the public record": 60
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 60
      },
      "host.cpu": {
        "none": 61
      },
      "host.ram_gib": {
        "none": 61
      },
      "host.spec_ref": {
        "none": 60
      },
      "host.vcpu": {
        "none": 61
      },
      "itt.class": {
        "none": 61
      },
      "itt.cohort": {
        "none": 60
      },
      "itt.evidence_ref": {
        "none": 61
      },
      "kogen.best_candidate": {
        "none": 61
      },
      "kogen.landed": {
        "none": 61
      },
      "outcome": {
        "not re-derivable from the public record": 60
      },
      "recipe": {
        "none": 60
      },
      "setup.adapter_harness_sha": {
        "none": 61
      },
      "setup.deps_source": {
        "none": 61
      },
      "setup.kogen_sha": {
        "none": 61
      },
      "stop_reason": {
        "none": 61
      },
      "task.base_repo": {
        "none": 60
      },
      "timestamps.attempts": {
        "none": 61
      },
      "timestamps.phases.develop.end_utc": {
        "none": 61
      },
      "timestamps.phases.develop.start_utc": {
        "none": 61
      },
      "timestamps.phases.gate.end_utc": {
        "none": 60
      },
      "timestamps.phases.gate.start_utc": {
        "none": 60
      },
      "timestamps.phases.grade.end_utc": {
        "none": 61
      },
      "timestamps.phases.grade.start_utc": {
        "none": 61
      },
      "timestamps.phases.plan.end_utc": {
        "none": 61
      },
      "timestamps.phases.plan.start_utc": {
        "none": 61
      },
      "timestamps.phases.review.end_utc": {
        "none": 61
      },
      "timestamps.phases.review.start_utc": {
        "none": 61
      },
      "timestamps.phases.shape.end_utc": {
        "none": 61
      },
      "timestamps.phases.shape.start_utc": {
        "none": 61
      },
      "timing.phases_s.develop": {
        "none": 61
      },
      "timing.phases_s.gate": {
        "none": 61
      },
      "timing.phases_s.grade": {
        "none": 61
      },
      "timing.phases_s.plan": {
        "none": 61
      },
      "timing.phases_s.review": {
        "none": 61
      },
      "timing.phases_s.setup": {
        "none": 60
      },
      "timing.phases_s.shape": {
        "none": 60
      },
      "tokens.phases.develop.cached_input": {
        "none": 61
      },
      "tokens.phases.develop.input": {
        "none": 61
      },
      "tokens.phases.develop.output": {
        "none": 61
      },
      "tokens.phases.develop.reasoning": {
        "none": 61
      },
      "tokens.phases.gate.cached_input": {
        "none": 61
      },
      "tokens.phases.gate.input": {
        "none": 61
      },
      "tokens.phases.gate.output": {
        "none": 61
      },
      "tokens.phases.gate.reasoning": {
        "none": 61
      },
      "tokens.phases.grade.cached_input": {
        "none": 60
      },
      "tokens.phases.grade.input": {
        "none": 60
      },
      "tokens.phases.grade.output": {
        "none": 60
      },
      "tokens.phases.grade.reasoning": {
        "none": 60
      },
      "tokens.phases.plan.cached_input": {
        "none": 61
      },
      "tokens.phases.plan.input": {
        "none": 61
      },
      "tokens.phases.plan.output": {
        "none": 61
      },
      "tokens.phases.plan.reasoning": {
        "none": 61
      },
      "tokens.phases.review.cached_input": {
        "none": 61
      },
      "tokens.phases.review.input": {
        "none": 61
      },
      "tokens.phases.review.output": {
        "none": 61
      },
      "tokens.phases.review.reasoning": {
        "none": 61
      },
      "tokens.phases.setup.cached_input": {
        "none": 61
      },
      "tokens.phases.setup.input": {
        "none": 61
      },
      "tokens.phases.setup.output": {
        "none": 61
      },
      "tokens.phases.setup.reasoning": {
        "none": 61
      },
      "tokens.phases.shape.cached_input": {
        "none": 60
      },
      "tokens.phases.shape.input": {
        "none": 60
      },
      "tokens.phases.shape.output": {
        "none": 60
      },
      "tokens.phases.shape.reasoning": {
        "none": 60
      },
      "tools.codex_cli": {
        "none": 61
      },
      "tools.grader": {
        "none": 61
      },
      "tools.harness": {
        "none": 61
      },
      "tools.kogen": {
        "none": 61
      },
      "tools.runner": {
        "none": 61
      },
      "tools.toolchains.elixir": {
        "none": 61
      },
      "tools.toolchains.erlang": {
        "none": 61
      },
      "tools.toolchains.node": {
        "none": 61
      },
      "tools.toolchains.other_inventory": {
        "none": 61
      },
      "tools.toolchains.ruby": {
        "none": 61
      },
      "tools.toolchains.rust": {
        "none": 61
      }
    },
    "reconstructable": {}
  },
  "round": "r67"
}
```
