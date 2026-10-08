# L3b: missing run-record fields (declared before bulk release)

Declared 2026-10-08, before any bulk cell was released. The round is released as **DESCRIPTIVE** with this strict-record gap disclosed.

The three pilot cells (RESTART `r70-4-ts-bun-fe2` r9018, CONTINUE `r70-4-ts-bun-fe2-l3b9c` r9020, REPAIR `r70-4-elixir-fe2-l3b13r` r9016) have Standard 1.2 run records rebuilt from the sanitized pilot source with `python3 reproduce/build_l3b_records.py`. The schema check reports zero errors, and the outcome, official grade, cell identity, cost and intention-to-treat fields are complete. Strict validation does not pass: **193 of 444 values (43.5%) are missing**, across 67 field paths.

## External evidence not available (6 values)

| Field | Values | Reason |
| --- | ---: | --- |
| `environment.account_class` | 3 | No class-only account receipt exists for these cells. |
| `circumstances.incidents` | 3 | No per-cell provider incident receipt was retained for the cell interval. |

These are not emitter gaps: the runner cannot produce them, and no receipt for them may ever exist.

## Runner and telemetry fields not emitted (187 values)

| Field group | Values |
| --- | ---: |
| `tokens.phases` (per-phase token counters) | 72 |
| `timestamps.phases` (absolute phase boundaries) | 42 |
| `timing.phases_s` (per-phase durations) | 21 |
| `environment.toolchains` / `tools.toolchains` (toolchain inventories) | 28 |
| `circumstances` boundary telemetry (cap, concurrency and load at start/end; load samples) | 21 |
| `tools.runner` | 3 |

Cell-level totals (wall time, request and token totals, official outcome) are present. Results built on these records report only fields that are present; no missing value is estimated.

## Machine-readable declaration

```json
{
  "cells": 3,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Boundary telemetry not retained": 3
      }
    },
    "circumstances.cap_start": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Boundary telemetry not retained": 3
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Boundary telemetry not retained": 3
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Boundary telemetry not retained": 3
      }
    },
    "circumstances.incidents": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Cell interval unavailable for incident overlap audit": 3
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Boundary telemetry not retained": 3
      }
    },
    "circumstances.load1_start": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Boundary telemetry not retained": 3
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "No matching controller samples retained": 3
      }
    },
    "environment.account_class": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "No owner-approved class-only account receipt is available for the cell": 3
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 2,
      "reasons": {
        "Toolchain version/inventory not recorded": 2
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 2,
      "reasons": {
        "Toolchain version/inventory not recorded": 2
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Toolchain version/inventory not recorded": 3
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 1,
      "reasons": {
        "Toolchain version/inventory not recorded": 1
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Toolchain version/inventory not recorded": 3
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Toolchain version/inventory not recorded": 3
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Absolute phase boundary not retained": 3
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Absolute phase boundary not retained": 3
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Absolute phase boundary not retained": 3
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Absolute phase boundary not retained": 3
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Absolute phase boundary not retained": 3
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Absolute phase boundary not retained": 3
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Absolute phase boundary not retained": 3
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Absolute phase boundary not retained": 3
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Absolute phase boundary not retained": 3
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Absolute phase boundary not retained": 3
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Absolute phase boundary not retained": 3
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Absolute phase boundary not retained": 3
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Absolute phase boundary not retained": 3
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Absolute phase boundary not retained": 3
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Phase wall not emitted or not separable": 3
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Phase wall not emitted or not separable": 3
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Phase wall not emitted or not separable": 3
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Phase wall not emitted or not separable": 3
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Phase wall not emitted or not separable": 3
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Phase wall not emitted or not separable": 3
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Phase wall not emitted or not separable": 3
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Per-phase token counter not emitted": 3
      }
    },
    "tools.runner": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 3
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 2,
      "reasons": {
        "Toolchain version/inventory not recorded": 2
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 2,
      "reasons": {
        "Toolchain version/inventory not recorded": 2
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Toolchain version/inventory not recorded": 3
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 1,
      "reasons": {
        "Toolchain version/inventory not recorded": 1
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Toolchain version/inventory not recorded": 3
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Missing run-record detail is disclosed; it does not alter the recorded intention-to-treat outcome.",
      "count": 3,
      "reasons": {
        "Toolchain version/inventory not recorded": 3
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 3
      },
      "circumstances.cap_start": {
        "none": 3
      },
      "circumstances.concurrent_cells_end": {
        "none": 3
      },
      "circumstances.concurrent_cells_start": {
        "none": 3
      },
      "circumstances.incidents": {
        "none": 3
      },
      "circumstances.load1_end": {
        "none": 3
      },
      "circumstances.load1_start": {
        "none": 3
      },
      "circumstances.load_samples": {
        "none": 3
      },
      "environment.account_class": {
        "none": 3
      },
      "environment.toolchains.elixir": {
        "none": 2
      },
      "environment.toolchains.erlang": {
        "none": 2
      },
      "environment.toolchains.node": {
        "none": 3
      },
      "environment.toolchains.other_inventory": {
        "none": 1
      },
      "environment.toolchains.ruby": {
        "none": 3
      },
      "environment.toolchains.rust": {
        "none": 3
      },
      "timestamps.phases.develop.end_utc": {
        "none": 3
      },
      "timestamps.phases.develop.start_utc": {
        "none": 3
      },
      "timestamps.phases.gate.end_utc": {
        "none": 3
      },
      "timestamps.phases.gate.start_utc": {
        "none": 3
      },
      "timestamps.phases.grade.end_utc": {
        "none": 3
      },
      "timestamps.phases.grade.start_utc": {
        "none": 3
      },
      "timestamps.phases.plan.end_utc": {
        "none": 3
      },
      "timestamps.phases.plan.start_utc": {
        "none": 3
      },
      "timestamps.phases.review.end_utc": {
        "none": 3
      },
      "timestamps.phases.review.start_utc": {
        "none": 3
      },
      "timestamps.phases.setup.end_utc": {
        "none": 3
      },
      "timestamps.phases.setup.start_utc": {
        "none": 3
      },
      "timestamps.phases.shape.end_utc": {
        "none": 3
      },
      "timestamps.phases.shape.start_utc": {
        "none": 3
      },
      "timing.phases_s.develop": {
        "none": 3
      },
      "timing.phases_s.gate": {
        "none": 3
      },
      "timing.phases_s.grade": {
        "none": 3
      },
      "timing.phases_s.plan": {
        "none": 3
      },
      "timing.phases_s.review": {
        "none": 3
      },
      "timing.phases_s.setup": {
        "none": 3
      },
      "timing.phases_s.shape": {
        "none": 3
      },
      "tokens.phases.develop.cached_input": {
        "none": 3
      },
      "tokens.phases.develop.input": {
        "none": 3
      },
      "tokens.phases.develop.output": {
        "none": 3
      },
      "tokens.phases.develop.reasoning": {
        "none": 3
      },
      "tokens.phases.gate.cached_input": {
        "none": 3
      },
      "tokens.phases.gate.input": {
        "none": 3
      },
      "tokens.phases.gate.output": {
        "none": 3
      },
      "tokens.phases.gate.reasoning": {
        "none": 3
      },
      "tokens.phases.plan.cached_input": {
        "none": 3
      },
      "tokens.phases.plan.input": {
        "none": 3
      },
      "tokens.phases.plan.output": {
        "none": 3
      },
      "tokens.phases.plan.reasoning": {
        "none": 3
      },
      "tokens.phases.review.cached_input": {
        "none": 3
      },
      "tokens.phases.review.input": {
        "none": 3
      },
      "tokens.phases.review.output": {
        "none": 3
      },
      "tokens.phases.review.reasoning": {
        "none": 3
      },
      "tokens.phases.setup.cached_input": {
        "none": 3
      },
      "tokens.phases.setup.input": {
        "none": 3
      },
      "tokens.phases.setup.output": {
        "none": 3
      },
      "tokens.phases.setup.reasoning": {
        "none": 3
      },
      "tokens.phases.shape.cached_input": {
        "none": 3
      },
      "tokens.phases.shape.input": {
        "none": 3
      },
      "tokens.phases.shape.output": {
        "none": 3
      },
      "tokens.phases.shape.reasoning": {
        "none": 3
      },
      "tools.runner": {
        "none": 3
      },
      "tools.toolchains.elixir": {
        "none": 2
      },
      "tools.toolchains.erlang": {
        "none": 2
      },
      "tools.toolchains.node": {
        "none": 3
      },
      "tools.toolchains.other_inventory": {
        "none": 1
      },
      "tools.toolchains.ruby": {
        "none": 3
      },
      "tools.toolchains.rust": {
        "none": 3
      }
    },
    "reconstructable": {}
  },
  "protocol_deviations": [
    "Only the three pre-bulk pilot cells have retained Standard 1.2 run records; the other 21 scored cells have official grade rows but no retained Standard run record.",
    "Pilot records omit declared phase-level token, timing, toolchain, and boundary telemetry; unavailable values are not estimated."
  ],
  "round": "l3b-repair-vs-continue"
}
```
