# Missing evidence and protocol deviations — r70-rve3

The Standard records preserve captured fields and declare every absent receipt using the official missing-reason legend. For the status-based publication route, [MISSING-DECLARED.json](MISSING-DECLARED.json) maps every missing field to a reason code from that legend. The JSON declaration below preserves the original field inventory and reconstruction-source accounting.

## Protocol deviations

- Standard run records were not emitted for these cells before execution; public rows were assembled retrospectively from surviving evidence.
- Per-cell phase timing, complete toolchain inventory, sandbox fingerprint, dated account class, grader version, and cost inputs were not retained.

## Exact missing-value declaration

```json
{
  "cells": 24,
  "fields": {
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 24
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 24
      }
    },
    "circumstances.dispatcher_id": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Per-cell dispatcher revision is not present in the public round data": 24
      }
    },
    "circumstances.incidents": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Per-cell incident receipt was not captured": 24
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Host boundary load was not captured in the public round data": 24
      }
    },
    "circumstances.load1_start": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Host boundary load was not captured in the public round data": 24
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 24
      }
    },
    "circumstances.queue": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Queue receipt was not captured": 24
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Cost calculator version not recorded": 24
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Price table version not recorded": 24
      }
    },
    "cost.usd": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 24
      }
    },
    "environment.account_class": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Dated account-class receipt is not present in the public round data": 24
      }
    },
    "environment.network.allowlist_hosts": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 24
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Toolchain version not recorded": 24
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Toolchain version not recorded": 24
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Toolchain version not recorded": 24
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 24
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Toolchain inventory not recorded": 24
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Toolchain version not recorded": 24
      }
    },
    "grade.grader": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Per-cell grader software version is not in the public data": 24
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt": 24
      }
    },
    "sandbox.egress_allow": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 24
      }
    },
    "sandbox.profile": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 24
      }
    },
    "sandbox.profile_sha256": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 24
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Per-cell dependency source is not recorded": 24
      }
    },
    "setup.sandbox_mode": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 24
      }
    },
    "setup.sandbox_profile_sha256": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 24
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Attempt-boundary receipts are not in the public round data": 24
      }
    },
    "timestamps.cell.end_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 2,
      "reasons": {
        "Per-cell contestant end timestamp not recorded in the public round data": 2
      }
    },
    "timestamps.cell.start_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 2,
      "reasons": {
        "Per-cell contestant start timestamp not recorded in the public round data": 2
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "develop phase timing was not separately recorded in the public round data": 24
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "grade phase timing was not separately recorded in the public round data": 24
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "setup phase timing was not separately recorded in the public round data": 24
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "develop phase token counter was not recorded separately": 24
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "develop phase token counter was not recorded separately": 24
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "develop phase token counter was not recorded separately": 24
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "develop phase token counter was not recorded separately": 24
      }
    },
    "tools.grader": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Per-cell grader software version is not in the public data": 24
      }
    },
    "tools.runner": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Per-cell grader software version is not in the public data": 24
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Toolchain version not recorded": 24
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Toolchain version not recorded": 24
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Toolchain version not recorded": 24
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 24
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Toolchain inventory not recorded": 24
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 24,
      "reasons": {
        "Toolchain version not recorded": 24
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.concurrent_cells_end": {
        "none": 24
      },
      "circumstances.concurrent_cells_start": {
        "none": 24
      },
      "circumstances.dispatcher_id": {
        "none": 24
      },
      "circumstances.incidents": {
        "none": 24
      },
      "circumstances.load1_end": {
        "none": 24
      },
      "circumstances.load1_start": {
        "none": 24
      },
      "circumstances.load_samples": {
        "none": 24
      },
      "circumstances.queue": {
        "none": 24
      },
      "cost.calculator_version": {
        "none": 24
      },
      "cost.price_table_version": {
        "none": 24
      },
      "cost.usd": {
        "none": 24
      },
      "environment.account_class": {
        "none": 24
      },
      "environment.network.allowlist_hosts": {
        "none": 24
      },
      "environment.toolchains.elixir": {
        "none": 24
      },
      "environment.toolchains.erlang": {
        "none": 24
      },
      "environment.toolchains.node": {
        "none": 24
      },
      "environment.toolchains.other_inventory": {
        "none": 24
      },
      "environment.toolchains.ruby": {
        "none": 24
      },
      "environment.toolchains.rust": {
        "none": 24
      },
      "grade.grader": {
        "none": 24
      },
      "grade.timestamp": {
        "none": 24
      },
      "sandbox.egress_allow": {
        "none": 24
      },
      "sandbox.profile": {
        "none": 24
      },
      "sandbox.profile_sha256": {
        "none": 24
      },
      "setup.deps_source": {
        "none": 24
      },
      "setup.sandbox_mode": {
        "none": 24
      },
      "setup.sandbox_profile_sha256": {
        "none": 24
      },
      "timestamps.attempts": {
        "none": 24
      },
      "timestamps.cell.end_utc": {
        "none": 2
      },
      "timestamps.cell.start_utc": {
        "none": 2
      },
      "timestamps.phases.develop.end_utc": {
        "none": 24
      },
      "timestamps.phases.develop.start_utc": {
        "none": 24
      },
      "timestamps.phases.gate.end_utc": {
        "none": 24
      },
      "timestamps.phases.gate.start_utc": {
        "none": 24
      },
      "timestamps.phases.grade.end_utc": {
        "none": 24
      },
      "timestamps.phases.grade.start_utc": {
        "none": 24
      },
      "timestamps.phases.plan.end_utc": {
        "none": 24
      },
      "timestamps.phases.plan.start_utc": {
        "none": 24
      },
      "timestamps.phases.review.end_utc": {
        "none": 24
      },
      "timestamps.phases.review.start_utc": {
        "none": 24
      },
      "timestamps.phases.setup.end_utc": {
        "none": 24
      },
      "timestamps.phases.setup.start_utc": {
        "none": 24
      },
      "timestamps.phases.shape.end_utc": {
        "none": 24
      },
      "timestamps.phases.shape.start_utc": {
        "none": 24
      },
      "timing.phases_s.develop": {
        "none": 24
      },
      "timing.phases_s.grade": {
        "none": 24
      },
      "timing.phases_s.setup": {
        "none": 24
      },
      "tokens.phases.develop.cached_input": {
        "none": 24
      },
      "tokens.phases.develop.input": {
        "none": 24
      },
      "tokens.phases.develop.output": {
        "none": 24
      },
      "tokens.phases.develop.reasoning": {
        "none": 24
      },
      "tools.grader": {
        "none": 24
      },
      "tools.runner": {
        "none": 24
      },
      "tools.toolchains.elixir": {
        "none": 24
      },
      "tools.toolchains.erlang": {
        "none": 24
      },
      "tools.toolchains.node": {
        "none": 24
      },
      "tools.toolchains.other_inventory": {
        "none": 24
      },
      "tools.toolchains.ruby": {
        "none": 24
      },
      "tools.toolchains.rust": {
        "none": 24
      }
    },
    "reconstructable": {}
  },
  "protocol_deviations": [
    "Standard run records were not emitted for these cells before execution; public rows were assembled retrospectively from surviving evidence.",
    "Per-cell phase timing, complete toolchain inventory, sandbox fingerprint, dated account class, grader version, and cost inputs were not retained."
  ],
  "round": "r70-rve3"
}
```
