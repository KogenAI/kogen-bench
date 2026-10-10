# Missing evidence and protocol deviations — r70-spot1

The Standard records preserve captured fields and declare every absent receipt using the official missing-reason legend. For the status-based publication route, [MISSING-DECLARED.json](MISSING-DECLARED.json) maps every missing field to a reason code from that legend. The JSON declaration below preserves the original field inventory and reconstruction-source accounting.

## Protocol deviations

- Standard run records were not emitted for these cells before execution; public rows were assembled retrospectively from surviving evidence.
- Per-cell phase timing, complete toolchain inventory, sandbox fingerprint, dated account class, grader version, and cost inputs were not retained.

## Exact missing-value declaration

```json
{
  "cells": 8,
  "fields": {
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 8
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 8
      }
    },
    "circumstances.dispatcher_id": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Per-cell dispatcher revision is not present in the public round data": 8
      }
    },
    "circumstances.incidents": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Per-cell incident receipt was not captured": 8
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Host boundary load was not captured in the public round data": 8
      }
    },
    "circumstances.load1_start": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Host boundary load was not captured in the public round data": 8
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 8
      }
    },
    "circumstances.queue": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Queue receipt was not captured": 8
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Cost calculator version not recorded": 8
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Price table version not recorded": 8
      }
    },
    "cost.usd": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 8
      }
    },
    "environment.account_class": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Dated account-class receipt is not present in the public round data": 8
      }
    },
    "environment.network.allowlist_hosts": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 8
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Toolchain version not recorded": 8
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Toolchain version not recorded": 8
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Toolchain version not recorded": 8
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 8
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Toolchain inventory not recorded": 8
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Toolchain version not recorded": 8
      }
    },
    "grade.grader": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Per-cell grader software version is not in the public data": 8
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt": 8
      }
    },
    "sandbox.egress_allow": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 8
      }
    },
    "sandbox.profile": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 8
      }
    },
    "sandbox.profile_sha256": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 8
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Per-cell dependency source is not recorded": 8
      }
    },
    "setup.sandbox_mode": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 8
      }
    },
    "setup.sandbox_profile_sha256": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 8
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Attempt-boundary receipts are not in the public round data": 8
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "develop phase timing was not separately recorded in the public round data": 8
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "grade phase timing was not separately recorded in the public round data": 8
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "setup phase timing was not separately recorded in the public round data": 8
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 1,
      "reasons": {
        "develop phase token counter was not recorded separately": 1
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 1,
      "reasons": {
        "develop phase token counter was not recorded separately": 1
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 1,
      "reasons": {
        "develop phase token counter was not recorded separately": 1
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 1,
      "reasons": {
        "develop phase token counter was not recorded separately": 1
      }
    },
    "tools.grader": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Per-cell grader software version is not in the public data": 8
      }
    },
    "tools.runner": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Per-cell grader software version is not in the public data": 8
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Toolchain version not recorded": 8
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Toolchain version not recorded": 8
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Toolchain version not recorded": 8
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 8
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Toolchain inventory not recorded": 8
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 8,
      "reasons": {
        "Toolchain version not recorded": 8
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.concurrent_cells_end": {
        "none": 8
      },
      "circumstances.concurrent_cells_start": {
        "none": 8
      },
      "circumstances.dispatcher_id": {
        "none": 8
      },
      "circumstances.incidents": {
        "none": 8
      },
      "circumstances.load1_end": {
        "none": 8
      },
      "circumstances.load1_start": {
        "none": 8
      },
      "circumstances.load_samples": {
        "none": 8
      },
      "circumstances.queue": {
        "none": 8
      },
      "cost.calculator_version": {
        "none": 8
      },
      "cost.price_table_version": {
        "none": 8
      },
      "cost.usd": {
        "none": 8
      },
      "environment.account_class": {
        "none": 8
      },
      "environment.network.allowlist_hosts": {
        "none": 8
      },
      "environment.toolchains.elixir": {
        "none": 8
      },
      "environment.toolchains.erlang": {
        "none": 8
      },
      "environment.toolchains.node": {
        "none": 8
      },
      "environment.toolchains.other_inventory": {
        "none": 8
      },
      "environment.toolchains.ruby": {
        "none": 8
      },
      "environment.toolchains.rust": {
        "none": 8
      },
      "grade.grader": {
        "none": 8
      },
      "grade.timestamp": {
        "none": 8
      },
      "sandbox.egress_allow": {
        "none": 8
      },
      "sandbox.profile": {
        "none": 8
      },
      "sandbox.profile_sha256": {
        "none": 8
      },
      "setup.deps_source": {
        "none": 8
      },
      "setup.sandbox_mode": {
        "none": 8
      },
      "setup.sandbox_profile_sha256": {
        "none": 8
      },
      "timestamps.attempts": {
        "none": 8
      },
      "timestamps.phases.develop.end_utc": {
        "none": 8
      },
      "timestamps.phases.develop.start_utc": {
        "none": 8
      },
      "timestamps.phases.gate.end_utc": {
        "none": 8
      },
      "timestamps.phases.gate.start_utc": {
        "none": 8
      },
      "timestamps.phases.grade.end_utc": {
        "none": 8
      },
      "timestamps.phases.grade.start_utc": {
        "none": 8
      },
      "timestamps.phases.plan.end_utc": {
        "none": 8
      },
      "timestamps.phases.plan.start_utc": {
        "none": 8
      },
      "timestamps.phases.review.end_utc": {
        "none": 8
      },
      "timestamps.phases.review.start_utc": {
        "none": 8
      },
      "timestamps.phases.setup.end_utc": {
        "none": 8
      },
      "timestamps.phases.setup.start_utc": {
        "none": 8
      },
      "timestamps.phases.shape.end_utc": {
        "none": 8
      },
      "timestamps.phases.shape.start_utc": {
        "none": 8
      },
      "timing.phases_s.develop": {
        "none": 8
      },
      "timing.phases_s.grade": {
        "none": 8
      },
      "timing.phases_s.setup": {
        "none": 8
      },
      "tokens.phases.develop.cached_input": {
        "none": 8
      },
      "tokens.phases.develop.input": {
        "none": 8
      },
      "tokens.phases.develop.output": {
        "none": 8
      },
      "tokens.phases.develop.reasoning": {
        "none": 8
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
      "tools.grader": {
        "none": 8
      },
      "tools.runner": {
        "none": 8
      },
      "tools.toolchains.elixir": {
        "none": 8
      },
      "tools.toolchains.erlang": {
        "none": 8
      },
      "tools.toolchains.node": {
        "none": 8
      },
      "tools.toolchains.other_inventory": {
        "none": 8
      },
      "tools.toolchains.ruby": {
        "none": 8
      },
      "tools.toolchains.rust": {
        "none": 8
      }
    },
    "reconstructable": {}
  },
  "protocol_deviations": [
    "Standard run records were not emitted for these cells before execution; public rows were assembled retrospectively from surviving evidence.",
    "Per-cell phase timing, complete toolchain inventory, sandbox fingerprint, dated account class, grader version, and cost inputs were not retained."
  ],
  "round": "r70-spot1"
}
```
