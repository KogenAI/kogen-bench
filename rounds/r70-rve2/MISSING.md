# Missing evidence and protocol deviations — r70-rve2

The Standard records preserve captured fields and declare every absent receipt using the official missing-reason legend. For the status-based publication route, [MISSING-DECLARED.json](MISSING-DECLARED.json) maps every missing field to a reason code from that legend. The JSON declaration below preserves the original field inventory and reconstruction-source accounting.

## Protocol deviations

- Standard run records were not emitted for these cells before execution; public rows were assembled retrospectively from surviving evidence.
- Per-cell phase timing, complete toolchain inventory, sandbox fingerprint, dated account class, grader version, and cost inputs were not retained.

## Exact missing-value declaration

```json
{
  "cells": 17,
  "fields": {
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 17
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 17
      }
    },
    "circumstances.dispatcher_id": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Per-cell dispatcher revision is not present in the public round data": 17
      }
    },
    "circumstances.incidents": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Per-cell incident receipt was not captured": 17
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Host boundary load was not captured in the public round data": 17
      }
    },
    "circumstances.load1_start": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Host boundary load was not captured in the public round data": 17
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 17
      }
    },
    "circumstances.queue": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Queue receipt was not captured": 17
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Cost calculator version not recorded": 17
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Price table version not recorded": 17
      }
    },
    "cost.usd": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 17
      }
    },
    "environment.account_class": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Dated account-class receipt is not present in the public round data": 17
      }
    },
    "environment.network.allowlist_hosts": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 17
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Toolchain version not recorded": 17
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Toolchain version not recorded": 17
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Toolchain version not recorded": 17
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 17
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Toolchain inventory not recorded": 17
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Toolchain version not recorded": 17
      }
    },
    "grade.grader": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Per-cell grader software version is not in the public data": 17
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt": 17
      }
    },
    "sandbox.egress_allow": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 17
      }
    },
    "sandbox.profile": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 17
      }
    },
    "sandbox.profile_sha256": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 17
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Per-cell dependency source is not recorded": 17
      }
    },
    "setup.sandbox_mode": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 17
      }
    },
    "setup.sandbox_profile_sha256": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 17
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Attempt-boundary receipts are not in the public round data": 17
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "develop phase timing was not separately recorded in the public round data": 17
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "grade phase timing was not separately recorded in the public round data": 17
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "setup phase timing was not separately recorded in the public round data": 17
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "develop phase token counter was not recorded separately": 17
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "develop phase token counter was not recorded separately": 17
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "develop phase token counter was not recorded separately": 17
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "develop phase token counter was not recorded separately": 17
      }
    },
    "tools.grader": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Per-cell grader software version is not in the public data": 17
      }
    },
    "tools.runner": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Per-cell grader software version is not in the public data": 17
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Toolchain version not recorded": 17
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Toolchain version not recorded": 17
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Toolchain version not recorded": 17
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 17
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Toolchain inventory not recorded": 17
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Missing capture receipts limit release eligibility and measurement completeness; observed official outcomes remain unchanged.",
      "count": 17,
      "reasons": {
        "Toolchain version not recorded": 17
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.concurrent_cells_end": {
        "none": 17
      },
      "circumstances.concurrent_cells_start": {
        "none": 17
      },
      "circumstances.dispatcher_id": {
        "none": 17
      },
      "circumstances.incidents": {
        "none": 17
      },
      "circumstances.load1_end": {
        "none": 17
      },
      "circumstances.load1_start": {
        "none": 17
      },
      "circumstances.load_samples": {
        "none": 17
      },
      "circumstances.queue": {
        "none": 17
      },
      "cost.calculator_version": {
        "none": 17
      },
      "cost.price_table_version": {
        "none": 17
      },
      "cost.usd": {
        "none": 17
      },
      "environment.account_class": {
        "none": 17
      },
      "environment.network.allowlist_hosts": {
        "none": 17
      },
      "environment.toolchains.elixir": {
        "none": 17
      },
      "environment.toolchains.erlang": {
        "none": 17
      },
      "environment.toolchains.node": {
        "none": 17
      },
      "environment.toolchains.other_inventory": {
        "none": 17
      },
      "environment.toolchains.ruby": {
        "none": 17
      },
      "environment.toolchains.rust": {
        "none": 17
      },
      "grade.grader": {
        "none": 17
      },
      "grade.timestamp": {
        "none": 17
      },
      "sandbox.egress_allow": {
        "none": 17
      },
      "sandbox.profile": {
        "none": 17
      },
      "sandbox.profile_sha256": {
        "none": 17
      },
      "setup.deps_source": {
        "none": 17
      },
      "setup.sandbox_mode": {
        "none": 17
      },
      "setup.sandbox_profile_sha256": {
        "none": 17
      },
      "timestamps.attempts": {
        "none": 17
      },
      "timestamps.phases.develop.end_utc": {
        "none": 17
      },
      "timestamps.phases.develop.start_utc": {
        "none": 17
      },
      "timestamps.phases.gate.end_utc": {
        "none": 17
      },
      "timestamps.phases.gate.start_utc": {
        "none": 17
      },
      "timestamps.phases.grade.end_utc": {
        "none": 17
      },
      "timestamps.phases.grade.start_utc": {
        "none": 17
      },
      "timestamps.phases.plan.end_utc": {
        "none": 17
      },
      "timestamps.phases.plan.start_utc": {
        "none": 17
      },
      "timestamps.phases.review.end_utc": {
        "none": 17
      },
      "timestamps.phases.review.start_utc": {
        "none": 17
      },
      "timestamps.phases.setup.end_utc": {
        "none": 17
      },
      "timestamps.phases.setup.start_utc": {
        "none": 17
      },
      "timestamps.phases.shape.end_utc": {
        "none": 17
      },
      "timestamps.phases.shape.start_utc": {
        "none": 17
      },
      "timing.phases_s.develop": {
        "none": 17
      },
      "timing.phases_s.grade": {
        "none": 17
      },
      "timing.phases_s.setup": {
        "none": 17
      },
      "tokens.phases.develop.cached_input": {
        "none": 17
      },
      "tokens.phases.develop.input": {
        "none": 17
      },
      "tokens.phases.develop.output": {
        "none": 17
      },
      "tokens.phases.develop.reasoning": {
        "none": 17
      },
      "tools.grader": {
        "none": 17
      },
      "tools.runner": {
        "none": 17
      },
      "tools.toolchains.elixir": {
        "none": 17
      },
      "tools.toolchains.erlang": {
        "none": 17
      },
      "tools.toolchains.node": {
        "none": 17
      },
      "tools.toolchains.other_inventory": {
        "none": 17
      },
      "tools.toolchains.ruby": {
        "none": 17
      },
      "tools.toolchains.rust": {
        "none": 17
      }
    },
    "reconstructable": {}
  },
  "protocol_deviations": [
    "Standard run records were not emitted for these cells before execution; public rows were assembled retrospectively from surviving evidence.",
    "Per-cell phase timing, complete toolchain inventory, sandbox fingerprint, dated account class, grader version, and cost inputs were not retained."
  ],
  "round": "r70-rve2"
}
```
