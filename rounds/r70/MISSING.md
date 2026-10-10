# Declared historical data gaps

The JSON declaration below covers the six Standard run records in [the public round record](../../results/run-records/r70.jsonl). The recovered result supplement ([cells.jsonl](cells.jsonl), with the full display table in [the per-cell table](README.md#per-cell-outcomes)) is an outcome-only overlay, not a new Standard run-record cohort. It reports the fields shown there and does not fill or imply values for the Standard fields that remain missing from the six-record snapshot. The gap declaration below continues to enumerate every missing Standard field and reason for that snapshot.

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 6,
  "fields": {
    "arm": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Arm label not retained": 6
      }
    },
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Boundary telemetry not retained": 6
      }
    },
    "circumstances.cap_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Boundary telemetry not retained": 6
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Boundary telemetry not retained": 6
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Boundary telemetry not retained": 6
      }
    },
    "circumstances.dispatcher_id": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Dispatcher receipt unavailable": 6
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Boundary telemetry not retained": 6
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "No matching controller samples retained": 6
      }
    },
    "circumstances.queue": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Queue receipt unavailable": 6
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "No dated account-class receipt": 6
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 6,
      "reasons": {
        "No official grade in the public snapshot": 6
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 6,
      "reasons": {
        "No official grade in the public snapshot": 6
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 6,
      "reasons": {
        "No official grade in the public snapshot": 6
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 6,
      "reasons": {
        "Ungraded delivery needs evidence audit": 6
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 6,
      "reasons": {
        "No audited ITT receipt": 6
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 6,
      "reasons": {
        "No official grade in the public snapshot": 6
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Dependency source not pinned per cell": 6
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Attempt boundary receipts unavailable": 6
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Absolute phase boundary not retained": 6
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Absolute phase boundary not retained": 6
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Absolute phase boundary not retained": 6
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Absolute phase boundary not retained": 6
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Absolute phase boundary not retained": 6
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Absolute phase boundary not retained": 6
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Absolute phase boundary not retained": 6
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Absolute phase boundary not retained": 6
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Absolute phase boundary not retained": 6
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Absolute phase boundary not retained": 6
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Absolute phase boundary not retained": 6
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Absolute phase boundary not retained": 6
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Not available for ungraded delivery": 6
      }
    }
  },
  "gap_sources": {
    "lost": {
      "arm": {
        "none": 6
      },
      "circumstances.cap_end": {
        "none": 6
      },
      "circumstances.cap_start": {
        "none": 6
      },
      "circumstances.concurrent_cells_end": {
        "none": 6
      },
      "circumstances.concurrent_cells_start": {
        "none": 6
      },
      "circumstances.dispatcher_id": {
        "none": 6
      },
      "circumstances.load1_end": {
        "none": 6
      },
      "circumstances.load_samples": {
        "none": 6
      },
      "circumstances.queue": {
        "none": 6
      },
      "cost.accounting": {
        "none": 6
      },
      "cost.calculator_version": {
        "none": 6
      },
      "cost.long_context_reconciled": {
        "none": 6
      },
      "cost.price_table_version": {
        "none": 6
      },
      "cost.usd": {
        "none": 6
      },
      "environment.account_class": {
        "none": 6
      },
      "environment.cores": {
        "none": 6
      },
      "environment.cpu_model": {
        "none": 6
      },
      "environment.ram_gib": {
        "none": 6
      },
      "environment.toolchains.elixir": {
        "none": 6
      },
      "environment.toolchains.erlang": {
        "none": 6
      },
      "environment.toolchains.node": {
        "none": 6
      },
      "environment.toolchains.other_inventory": {
        "none": 6
      },
      "environment.toolchains.ruby": {
        "none": 6
      },
      "environment.toolchains.rust": {
        "none": 6
      },
      "grade.grader": {
        "not re-derivable from the public record": 6
      },
      "grade.tests_ran": {
        "not re-derivable from the public record": 6
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 6
      },
      "host.cpu": {
        "none": 6
      },
      "host.ram_gib": {
        "none": 6
      },
      "host.spec_ref": {
        "none": 6
      },
      "host.vcpu": {
        "none": 6
      },
      "itt.class": {
        "none": 6
      },
      "itt.evidence_ref": {
        "none": 6
      },
      "outcome": {
        "not re-derivable from the public record": 6
      },
      "setup.deps_source": {
        "none": 6
      },
      "task.base_repo": {
        "none": 6
      },
      "timestamps.attempts": {
        "none": 6
      },
      "timestamps.phases.gate.end_utc": {
        "none": 6
      },
      "timestamps.phases.gate.start_utc": {
        "none": 6
      },
      "timestamps.phases.grade.end_utc": {
        "none": 6
      },
      "timestamps.phases.grade.start_utc": {
        "none": 6
      },
      "timestamps.phases.plan.end_utc": {
        "none": 6
      },
      "timestamps.phases.plan.start_utc": {
        "none": 6
      },
      "timestamps.phases.review.end_utc": {
        "none": 6
      },
      "timestamps.phases.review.start_utc": {
        "none": 6
      },
      "timestamps.phases.setup.end_utc": {
        "none": 6
      },
      "timestamps.phases.setup.start_utc": {
        "none": 6
      },
      "timestamps.phases.shape.end_utc": {
        "none": 6
      },
      "timestamps.phases.shape.start_utc": {
        "none": 6
      },
      "timing.phases_s.develop": {
        "none": 6
      },
      "timing.phases_s.gate": {
        "none": 6
      },
      "timing.phases_s.grade": {
        "none": 6
      },
      "timing.phases_s.plan": {
        "none": 6
      },
      "timing.phases_s.review": {
        "none": 6
      },
      "timing.phases_s.setup": {
        "none": 6
      },
      "timing.phases_s.shape": {
        "none": 6
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
        "none": 6
      },
      "tokens.phases.gate.input": {
        "none": 6
      },
      "tokens.phases.gate.output": {
        "none": 6
      },
      "tokens.phases.gate.reasoning": {
        "none": 6
      },
      "tokens.phases.grade.cached_input": {
        "none": 6
      },
      "tokens.phases.grade.input": {
        "none": 6
      },
      "tokens.phases.grade.output": {
        "none": 6
      },
      "tokens.phases.grade.reasoning": {
        "none": 6
      },
      "tokens.phases.plan.cached_input": {
        "none": 6
      },
      "tokens.phases.plan.input": {
        "none": 6
      },
      "tokens.phases.plan.output": {
        "none": 6
      },
      "tokens.phases.plan.reasoning": {
        "none": 6
      },
      "tokens.phases.review.cached_input": {
        "none": 6
      },
      "tokens.phases.review.input": {
        "none": 6
      },
      "tokens.phases.review.output": {
        "none": 6
      },
      "tokens.phases.review.reasoning": {
        "none": 6
      },
      "tokens.phases.setup.cached_input": {
        "none": 6
      },
      "tokens.phases.setup.input": {
        "none": 6
      },
      "tokens.phases.setup.output": {
        "none": 6
      },
      "tokens.phases.setup.reasoning": {
        "none": 6
      },
      "tokens.phases.shape.cached_input": {
        "none": 6
      },
      "tokens.phases.shape.input": {
        "none": 6
      },
      "tokens.phases.shape.output": {
        "none": 6
      },
      "tokens.phases.shape.reasoning": {
        "none": 6
      },
      "tools.grader": {
        "none": 6
      },
      "tools.runner": {
        "none": 6
      },
      "tools.toolchains.elixir": {
        "none": 6
      },
      "tools.toolchains.erlang": {
        "none": 6
      },
      "tools.toolchains.node": {
        "none": 6
      },
      "tools.toolchains.other_inventory": {
        "none": 6
      },
      "tools.toolchains.ruby": {
        "none": 6
      },
      "tools.toolchains.rust": {
        "none": 6
      }
    },
    "reconstructable": {}
  },
  "publication_reconciliation": {
    "disposition": "The six public records tagged r70 are ungraded delivery records for the frozen stack study. Keep them distinct from the original RvE, rerun and extension cohorts represented by separate supplemental ledgers/pages; their results do not close the frozen stack study.",
    "original_execution_command": "not recorded in the public snapshot",
    "harness_source_commit": "absent; tools.harness values are wrapper fingerprints",
    "kogen_source_commit": "Public records mark the Kogen product commit not applicable for these harness records.",
    "raw_public_records": [
      "results/run-records/r70.jsonl",
      "results/cells.jsonl"
    ],
    "public_record_rebuild": "python3 reproduce/export_results.py; python3 reproduce/build_records.py; python3 reproduce/validate_round.py --round r70"
  },
  "round": "r70"
}
```
