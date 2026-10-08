# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 50,
  "fields": {
    "arm": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Arm label not retained": 1
      }
    },
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Boundary telemetry not retained": 50
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Boundary telemetry not retained": 50
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Boundary telemetry not retained": 50
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "No matching controller samples retained": 50
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 25,
      "reasons": {
        "Complete per-model billable vector unavailable": 24,
        "Not available for ungraded delivery": 1
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "No dated account-class receipt": 50
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "No per-cell CPU allocation receipt": 49,
        "Not available for ungraded delivery": 1
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "No per-cell CPU receipt": 49,
        "Not available for ungraded delivery": 1
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "No per-cell RAM receipt": 49,
        "Not available for ungraded delivery": 1
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 49
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 49
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 49
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 49
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 1,
      "reasons": {
        "No official grade in the public snapshot": 1
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 10,
      "reasons": {
        "Boolean receipt not recorded": 9,
        "No official grade in the public snapshot": 1
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 1,
      "reasons": {
        "No official grade in the public snapshot": 1
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 50,
      "reasons": {
        "No per-cell CPU receipt": 49,
        "Not available for ungraded delivery": 1
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 50,
      "reasons": {
        "No per-cell RAM receipt": 49,
        "Not available for ungraded delivery": 1
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 50,
      "reasons": {
        "No per-cell CPU allocation receipt": 49,
        "Not available for ungraded delivery": 1
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 10,
      "reasons": {
        "Invalid/environment cause requires evidence audit": 9,
        "Ungraded delivery needs evidence audit": 1
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 1,
      "reasons": {
        "No captured cohort launch receipt": 1
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 10,
      "reasons": {
        "No audited ITT receipt": 1,
        "No evidence-backed ITT classification": 9
      }
    },
    "kogen.best_candidate": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 10,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Not recorded in available public metadata": 9
      }
    },
    "kogen.landed": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 1,
      "reasons": {
        "No official grade in the public snapshot": 1
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "setup.adapter_harness_sha": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Not recorded in available public metadata": 50
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 9,
      "reasons": {
        "Runner status does not establish normalized stop cause": 9
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Attempt boundary receipts unavailable": 50
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Absolute phase boundary not retained": 50
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Absolute phase boundary not retained": 50
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 5,
      "reasons": {
        "Absolute phase boundary not retained": 5
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Absolute phase boundary not retained": 50
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Absolute phase boundary not retained": 50
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Absolute phase boundary not retained": 50
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Absolute phase boundary not retained": 50
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Absolute phase boundary not retained": 50
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Absolute phase boundary not retained": 50
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Absolute phase boundary not retained": 50
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Absolute phase boundary not retained": 50
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Phase wall not emitted or not separable": 5
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Phase wall not emitted or not separable": 5
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 10,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Phase wall not emitted or not separable": 9
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Phase wall not emitted or not separable": 49
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 5
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 5
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 5
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 5
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 1,
      "reasons": {
        "Not available for ungraded delivery": 1
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 49
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Per-phase token counter not emitted": 49
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 49,
        "Not available for ungraded delivery": 1
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 49,
        "Not available for ungraded delivery": 1
      }
    },
    "tools.harness": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Not recorded in available public metadata": 50
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 49,
        "Not available for ungraded delivery": 1
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 49
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 49
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 49
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 49
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 49
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 50,
      "reasons": {
        "Not available for ungraded delivery": 1,
        "Toolchain version/inventory not recorded": 49
      }
    }
  },
  "gap_sources": {
    "lost": {
      "arm": {
        "none": 1
      },
      "circumstances.cap_end": {
        "none": 50
      },
      "circumstances.concurrent_cells_end": {
        "none": 50
      },
      "circumstances.load1_end": {
        "none": 50
      },
      "circumstances.load_samples": {
        "none": 50
      },
      "cost.accounting": {
        "none": 1
      },
      "cost.calculator_version": {
        "none": 1
      },
      "cost.long_context_reconciled": {
        "none": 1
      },
      "cost.price_table_version": {
        "none": 1
      },
      "cost.usd": {
        "none": 25
      },
      "environment.account_class": {
        "none": 50
      },
      "environment.cores": {
        "none": 50
      },
      "environment.cpu_model": {
        "none": 50
      },
      "environment.ram_gib": {
        "none": 50
      },
      "environment.toolchains.node": {
        "none": 50
      },
      "environment.toolchains.other_inventory": {
        "none": 50
      },
      "environment.toolchains.ruby": {
        "none": 50
      },
      "environment.toolchains.rust": {
        "none": 50
      },
      "grade.grader": {
        "not re-derivable from the public record": 1
      },
      "grade.tests_ran": {
        "none": 9,
        "not re-derivable from the public record": 1
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 1
      },
      "host.cpu": {
        "none": 50
      },
      "host.ram_gib": {
        "none": 50
      },
      "host.spec_ref": {
        "none": 1
      },
      "host.vcpu": {
        "none": 50
      },
      "itt.class": {
        "none": 10
      },
      "itt.cohort": {
        "none": 1
      },
      "itt.evidence_ref": {
        "none": 10
      },
      "kogen.best_candidate": {
        "none": 10
      },
      "kogen.landed": {
        "none": 1
      },
      "outcome": {
        "not re-derivable from the public record": 1
      },
      "recipe": {
        "none": 1
      },
      "setup.adapter_harness_sha": {
        "none": 50
      },
      "stop_reason": {
        "none": 9
      },
      "task.base_repo": {
        "none": 1
      },
      "timestamps.attempts": {
        "none": 50
      },
      "timestamps.phases.develop.end_utc": {
        "none": 50
      },
      "timestamps.phases.develop.start_utc": {
        "none": 50
      },
      "timestamps.phases.gate.end_utc": {
        "none": 5
      },
      "timestamps.phases.gate.start_utc": {
        "none": 5
      },
      "timestamps.phases.grade.end_utc": {
        "none": 50
      },
      "timestamps.phases.grade.start_utc": {
        "none": 50
      },
      "timestamps.phases.plan.end_utc": {
        "none": 50
      },
      "timestamps.phases.plan.start_utc": {
        "none": 50
      },
      "timestamps.phases.review.end_utc": {
        "none": 50
      },
      "timestamps.phases.review.start_utc": {
        "none": 50
      },
      "timestamps.phases.shape.end_utc": {
        "none": 50
      },
      "timestamps.phases.shape.start_utc": {
        "none": 50
      },
      "timing.phases_s.develop": {
        "none": 6
      },
      "timing.phases_s.gate": {
        "none": 6
      },
      "timing.phases_s.grade": {
        "none": 10
      },
      "timing.phases_s.plan": {
        "none": 1
      },
      "timing.phases_s.review": {
        "none": 50
      },
      "timing.phases_s.setup": {
        "none": 1
      },
      "timing.phases_s.shape": {
        "none": 1
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
        "none": 50
      },
      "tokens.phases.gate.input": {
        "none": 50
      },
      "tokens.phases.gate.output": {
        "none": 50
      },
      "tokens.phases.gate.reasoning": {
        "none": 50
      },
      "tokens.phases.grade.cached_input": {
        "none": 1
      },
      "tokens.phases.grade.input": {
        "none": 1
      },
      "tokens.phases.grade.output": {
        "none": 1
      },
      "tokens.phases.grade.reasoning": {
        "none": 1
      },
      "tokens.phases.plan.cached_input": {
        "none": 1
      },
      "tokens.phases.plan.input": {
        "none": 1
      },
      "tokens.phases.plan.output": {
        "none": 1
      },
      "tokens.phases.plan.reasoning": {
        "none": 1
      },
      "tokens.phases.review.cached_input": {
        "none": 50
      },
      "tokens.phases.review.input": {
        "none": 50
      },
      "tokens.phases.review.output": {
        "none": 50
      },
      "tokens.phases.review.reasoning": {
        "none": 50
      },
      "tokens.phases.setup.cached_input": {
        "none": 50
      },
      "tokens.phases.setup.input": {
        "none": 50
      },
      "tokens.phases.setup.output": {
        "none": 50
      },
      "tokens.phases.setup.reasoning": {
        "none": 50
      },
      "tokens.phases.shape.cached_input": {
        "none": 50
      },
      "tokens.phases.shape.input": {
        "none": 50
      },
      "tokens.phases.shape.output": {
        "none": 50
      },
      "tokens.phases.shape.reasoning": {
        "none": 50
      },
      "tools.codex_cli": {
        "none": 50
      },
      "tools.grader": {
        "none": 50
      },
      "tools.harness": {
        "none": 50
      },
      "tools.runner": {
        "none": 50
      },
      "tools.toolchains.elixir": {
        "none": 50
      },
      "tools.toolchains.erlang": {
        "none": 50
      },
      "tools.toolchains.node": {
        "none": 50
      },
      "tools.toolchains.other_inventory": {
        "none": 50
      },
      "tools.toolchains.ruby": {
        "none": 50
      },
      "tools.toolchains.rust": {
        "none": 50
      }
    },
    "reconstructable": {}
  },
  "publication_reconciliation": {
    "disposition": "The public official outcome export contains fewer r71 rows than the captured delivery ledger, so it does not reconstruct the planned provided-versus-shaped contrast. Keep INTERIM; the historical arm rates are source-reported, not reproducible from public data.",
    "original_execution_command": "not recorded in the public snapshot",
    "harness_source_commit": "absent; tools.harness values are wrapper fingerprints",
    "kogen_source_commit": "Exact commit is present in the per-cell setup.kogen_sha field; see README.md.",
    "raw_public_records": [
      "results/run-records/r71.jsonl",
      "results/cells.jsonl"
    ],
    "public_record_rebuild": "python3 reproduce/export_results.py; python3 reproduce/build_records.py; python3 reproduce/validate_round.py --round r71"
  },
  "round": "r71"
}
```
