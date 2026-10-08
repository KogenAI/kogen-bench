# Declared gaps and protocol deviations — l3-repair

This declaration describes gaps in the public Standard records. No missing receipt is replaced with a reconstructed or invented value. The exact fields and counts below are generated from `records.jsonl`.

## Protocol deviations

- The complete Standard-record gate was not run before analysis. These records were assembled retrospectively from cells.csv and the sanitized lane release-state summary; the pre-registration timing remains operator-reported.
- Per-cell contestant manifests, official repair-grade timestamp receipts, sandbox fingerprints, phase counters, cost inputs, host-load samples, and stop-cause receipts were not recovered into the public bundle. Missing fields remain explicit.
- Per-test grade outcomes are absent from the public bundle, so the registered per-test pass-set no-regression condition is unverifiable. Aggregate test counts are not substituted for it.
- The six paired original failures belong to the existing Round 70 cohort. This Standard file records only the six new repair cells to avoid duplicate exact identities.

## Exact missing-value declaration

```json
{
  "round": "l3-repair",
  "cells": 6,
  "fields": {
    "circumstances.concurrent_cells_end": {
      "count": 6,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "circumstances.concurrent_cells_start": {
      "count": 6,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "circumstances.dispatcher_id": {
      "count": 6,
      "reasons": {
        "Per-cell dispatcher revision is not present in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "circumstances.incidents": {
      "count": 6,
      "reasons": {
        "Per-cell incident receipt was not captured": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "circumstances.load1_end": {
      "count": 6,
      "reasons": {
        "Host boundary load was not captured in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "circumstances.load1_start": {
      "count": 6,
      "reasons": {
        "Host boundary load was not captured in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "circumstances.load_samples": {
      "count": 6,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "circumstances.queue": {
      "count": 6,
      "reasons": {
        "Queue receipt was not captured": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "cost.calculator_version": {
      "count": 6,
      "reasons": {
        "Cost calculator version not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "cost.price_table_version": {
      "count": 6,
      "reasons": {
        "Price table version not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "cost.usd": {
      "count": 6,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "effort.effective": {
      "count": 6,
      "reasons": {
        "Per-cell effective-effort receipt not published": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "environment.account_class": {
      "count": 6,
      "reasons": {
        "Dated account-class receipt is not present in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "environment.network.allowlist_hosts": {
      "count": 6,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "environment.network.profile": {
      "count": 6,
      "reasons": {
        "Per-cell network profile not present in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "environment.toolchains.elixir": {
      "count": 6,
      "reasons": {
        "Toolchain version not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "environment.toolchains.erlang": {
      "count": 6,
      "reasons": {
        "Toolchain version not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "environment.toolchains.node": {
      "count": 6,
      "reasons": {
        "Toolchain version not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "environment.toolchains.other_inventory": {
      "count": 6,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "environment.toolchains.ruby": {
      "count": 6,
      "reasons": {
        "Toolchain inventory not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "environment.toolchains.rust": {
      "count": 6,
      "reasons": {
        "Toolchain version not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "grade.grader": {
      "count": 6,
      "reasons": {
        "Per-cell grader software version is not in the public data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "grade.timestamp": {
      "count": 6,
      "reasons": {
        "Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "model.effective": {
      "count": 6,
      "reasons": {
        "Per-cell effective-model receipt not published": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "provenance.manifest_sha256": {
      "count": 6,
      "reasons": {
        "Per-cell run manifest fingerprint not in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "sandbox.egress_allow": {
      "count": 6,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "sandbox.egress_profile": {
      "count": 6,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "sandbox.profile": {
      "count": 6,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "sandbox.profile_sha256": {
      "count": 6,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "setup.deps_source": {
      "count": 6,
      "reasons": {
        "Per-cell dependency source is not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "setup.sandbox_mode": {
      "count": 6,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "setup.sandbox_profile_sha256": {
      "count": 6,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "stop_reason": {
      "count": 6,
      "reasons": {
        "A scored outcome does not establish the runner stop cause": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.attempts": {
      "count": 6,
      "reasons": {
        "Attempt-boundary receipts are not in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.cell.end_utc": {
      "count": 6,
      "reasons": {
        "Per-cell contestant end timestamp not recorded in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.cell.start_utc": {
      "count": 6,
      "reasons": {
        "Per-cell contestant start timestamp not recorded in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.phases.develop.end_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.phases.develop.start_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.phases.gate.end_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.phases.gate.start_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.phases.grade.end_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.phases.grade.start_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.phases.plan.end_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.phases.plan.start_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.phases.review.end_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.phases.review.start_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.phases.setup.end_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.phases.setup.start_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.phases.shape.end_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.phases.shape.start_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timing.phases_s.develop": {
      "count": 6,
      "reasons": {
        "develop phase timing was not separately recorded in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timing.phases_s.grade": {
      "count": 6,
      "reasons": {
        "grade phase timing was not separately recorded in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timing.phases_s.setup": {
      "count": 6,
      "reasons": {
        "setup phase timing was not separately recorded in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "tokens.phases.develop.cached_input": {
      "count": 6,
      "reasons": {
        "develop phase token counter was not recorded separately": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "tokens.phases.develop.input": {
      "count": 6,
      "reasons": {
        "develop phase token counter was not recorded separately": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "tokens.phases.develop.output": {
      "count": 6,
      "reasons": {
        "develop phase token counter was not recorded separately": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "tokens.phases.develop.reasoning": {
      "count": 6,
      "reasons": {
        "develop phase token counter was not recorded separately": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "tokens.total.reasoning": {
      "count": 6,
      "reasons": {
        "Reasoning counter not recorded separately": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "tools.grader": {
      "count": 6,
      "reasons": {
        "Per-cell grader software version is not in the public data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "tools.toolchains.elixir": {
      "count": 6,
      "reasons": {
        "Toolchain version not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "tools.toolchains.erlang": {
      "count": 6,
      "reasons": {
        "Toolchain version not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "tools.toolchains.node": {
      "count": 6,
      "reasons": {
        "Toolchain version not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "tools.toolchains.other_inventory": {
      "count": 6,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "tools.toolchains.ruby": {
      "count": 6,
      "reasons": {
        "Toolchain inventory not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "tools.toolchains.rust": {
      "count": 6,
      "reasons": {
        "Toolchain version not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    }
  },
  "gap_sources": {
    "reconstructable": {},
    "lost": {
      "circumstances.concurrent_cells_end": {
        "none": 6
      },
      "circumstances.concurrent_cells_start": {
        "none": 6
      },
      "circumstances.dispatcher_id": {
        "none": 6
      },
      "circumstances.incidents": {
        "none": 6
      },
      "circumstances.load1_end": {
        "none": 6
      },
      "circumstances.load1_start": {
        "none": 6
      },
      "circumstances.load_samples": {
        "none": 6
      },
      "circumstances.queue": {
        "none": 6
      },
      "cost.calculator_version": {
        "none": 6
      },
      "cost.price_table_version": {
        "none": 6
      },
      "cost.usd": {
        "none": 6
      },
      "effort.effective": {
        "none": 6
      },
      "environment.account_class": {
        "none": 6
      },
      "environment.network.allowlist_hosts": {
        "none": 6
      },
      "environment.network.profile": {
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
        "none": 6
      },
      "grade.timestamp": {
        "none": 6
      },
      "model.effective": {
        "none": 6
      },
      "provenance.manifest_sha256": {
        "none": 6
      },
      "sandbox.egress_allow": {
        "none": 6
      },
      "sandbox.egress_profile": {
        "none": 6
      },
      "sandbox.profile": {
        "none": 6
      },
      "sandbox.profile_sha256": {
        "none": 6
      },
      "setup.deps_source": {
        "none": 6
      },
      "setup.sandbox_mode": {
        "none": 6
      },
      "setup.sandbox_profile_sha256": {
        "none": 6
      },
      "stop_reason": {
        "none": 6
      },
      "timestamps.attempts": {
        "none": 6
      },
      "timestamps.cell.end_utc": {
        "none": 6
      },
      "timestamps.cell.start_utc": {
        "none": 6
      },
      "timestamps.phases.develop.end_utc": {
        "none": 6
      },
      "timestamps.phases.develop.start_utc": {
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
      "timing.phases_s.grade": {
        "none": 6
      },
      "timing.phases_s.setup": {
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
      "tokens.total.reasoning": {
        "none": 6
      },
      "tools.grader": {
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
    }
  },
  "protocol_deviations": [
    "The complete Standard-record gate was not run before analysis. These records were assembled retrospectively from cells.csv and the sanitized lane release-state summary; the pre-registration timing remains operator-reported.",
    "Per-cell contestant manifests, official repair-grade timestamp receipts, sandbox fingerprints, phase counters, cost inputs, host-load samples, and stop-cause receipts were not recovered into the public bundle. Missing fields remain explicit.",
    "Per-test grade outcomes are absent from the public bundle, so the registered per-test pass-set no-regression condition is unverifiable. Aggregate test counts are not substituted for it.",
    "The six paired original failures belong to the existing Round 70 cohort. This Standard file records only the six new repair cells to avoid duplicate exact identities."
  ]
}
```
