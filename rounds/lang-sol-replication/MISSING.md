# Declared gaps and protocol deviations — lang-sol-replication

This declaration describes gaps in the public Standard records. No missing receipt is replaced with a reconstructed or invented value. The exact fields and counts below are generated from `records.jsonl`.

## Protocol deviations

- The full Standard-record gate was deferred until analysis under the lane's emitter-gap exception. The referenced strict-exception receipt is not included in the public bundle; this retrospective record validation does not establish pre-run compliance.
- The exact pre-run design commitment and first-call-start receipts are not in the public bundle. Registration timing remains operator-reported.
- Per-cell runner manifests, sandbox fingerprints, phase counters, cost inputs, host-load samples, effective-setting receipts, and stop-cause receipts were not recovered into the public bundle. Missing fields remain explicit.
- The 31 reused t5-t7 cells are already represented in the Round 70 source cohort; this round's Standard file records only its 27 new scored cells to avoid duplicate exact identities.

## Exact missing-value declaration

```json
{
  "round": "lang-sol-replication",
  "cells": 27,
  "fields": {
    "circumstances.concurrent_cells_end": {
      "count": 27,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "circumstances.concurrent_cells_start": {
      "count": 27,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "circumstances.dispatcher_id": {
      "count": 27,
      "reasons": {
        "Exact dispatcher revision is not present in the public receipt extract": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "circumstances.incidents": {
      "count": 27,
      "reasons": {
        "Per-cell incident receipt was not captured": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "circumstances.load1_end": {
      "count": 27,
      "reasons": {
        "Host boundary load was not captured in the public round data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "circumstances.load1_start": {
      "count": 27,
      "reasons": {
        "Host boundary load was not captured in the public round data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "circumstances.load_samples": {
      "count": 27,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "circumstances.queue": {
      "count": 27,
      "reasons": {
        "Queue receipt was not captured": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "cost.calculator_version": {
      "count": 27,
      "reasons": {
        "Cost calculator version not recorded": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "cost.price_table_version": {
      "count": 27,
      "reasons": {
        "Price table version not recorded": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "cost.usd": {
      "count": 27,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "effort.effective": {
      "count": 27,
      "reasons": {
        "Per-cell effective-effort receipt not published": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "environment.account_class": {
      "count": 27,
      "reasons": {
        "Dated account-class receipt is not present in the public round data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "environment.network.allowlist_hosts": {
      "count": 27,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "environment.network.profile": {
      "count": 27,
      "reasons": {
        "Per-cell network profile not present in the public round data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "environment.toolchains.elixir": {
      "count": 27,
      "reasons": {
        "Toolchain version not recorded": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "environment.toolchains.erlang": {
      "count": 27,
      "reasons": {
        "Toolchain version not recorded": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "environment.toolchains.node": {
      "count": 27,
      "reasons": {
        "Toolchain version not recorded": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "environment.toolchains.other_inventory": {
      "count": 27,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "environment.toolchains.python": {
      "count": 27,
      "reasons": {
        "Python toolchain version not recorded for the public round data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "environment.toolchains.ruby": {
      "count": 27,
      "reasons": {
        "Toolchain inventory not recorded": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "environment.toolchains.rust": {
      "count": 27,
      "reasons": {
        "Toolchain version not recorded": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "grade.grader": {
      "count": 27,
      "reasons": {
        "Per-cell grader software version is not in the public data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "model.effective": {
      "count": 27,
      "reasons": {
        "Per-cell effective-model receipt not published": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "provenance.manifest_sha256": {
      "count": 27,
      "reasons": {
        "Per-cell run manifest fingerprint not in the public round data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "sandbox.egress_allow": {
      "count": 27,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "sandbox.egress_profile": {
      "count": 27,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "sandbox.profile": {
      "count": 27,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "sandbox.profile_sha256": {
      "count": 27,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "setup.adapter_harness_sha": {
      "count": 27,
      "reasons": {
        "Per-cell Codex adapter fingerprint not recorded in the public round data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "setup.deps_source": {
      "count": 27,
      "reasons": {
        "Per-cell dependency source is not recorded": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "setup.sandbox_mode": {
      "count": 27,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "setup.sandbox_profile_sha256": {
      "count": 27,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "stop_reason": {
      "count": 27,
      "reasons": {
        "A scored outcome does not establish the runner stop cause": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.attempts": {
      "count": 27,
      "reasons": {
        "Attempt-boundary receipts are not in the public round data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.cell.end_utc": {
      "count": 27,
      "reasons": {
        "Per-cell contestant end timestamp not recorded in the public round data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.cell.start_utc": {
      "count": 27,
      "reasons": {
        "Per-cell contestant start timestamp not recorded in the public round data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.phases.develop.end_utc": {
      "count": 27,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.phases.develop.start_utc": {
      "count": 27,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.phases.gate.end_utc": {
      "count": 27,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.phases.gate.start_utc": {
      "count": 27,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.phases.plan.end_utc": {
      "count": 27,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.phases.plan.start_utc": {
      "count": 27,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.phases.review.end_utc": {
      "count": 27,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.phases.review.start_utc": {
      "count": 27,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.phases.setup.end_utc": {
      "count": 27,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.phases.setup.start_utc": {
      "count": 27,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.phases.shape.end_utc": {
      "count": 27,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timestamps.phases.shape.start_utc": {
      "count": 27,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timing.phases_s.develop": {
      "count": 27,
      "reasons": {
        "develop phase timing was not separately recorded in the public round data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timing.phases_s.grade": {
      "count": 27,
      "reasons": {
        "grade phase timing was not separately recorded in the public round data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "timing.phases_s.setup": {
      "count": 27,
      "reasons": {
        "setup phase timing was not separately recorded in the public round data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "tokens.phases.develop.cached_input": {
      "count": 27,
      "reasons": {
        "develop phase token counter was not recorded separately": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "tokens.phases.develop.input": {
      "count": 27,
      "reasons": {
        "develop phase token counter was not recorded separately": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "tokens.phases.develop.output": {
      "count": 27,
      "reasons": {
        "develop phase token counter was not recorded separately": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "tokens.phases.develop.reasoning": {
      "count": 27,
      "reasons": {
        "develop phase token counter was not recorded separately": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "tokens.total.reasoning": {
      "count": 27,
      "reasons": {
        "Reasoning counter not recorded separately": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "tools.grader": {
      "count": 27,
      "reasons": {
        "Per-cell grader software version is not in the public data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "tools.runner": {
      "count": 27,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "tools.toolchains.elixir": {
      "count": 27,
      "reasons": {
        "Toolchain version not recorded": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "tools.toolchains.erlang": {
      "count": 27,
      "reasons": {
        "Toolchain version not recorded": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "tools.toolchains.node": {
      "count": 27,
      "reasons": {
        "Toolchain version not recorded": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "tools.toolchains.other_inventory": {
      "count": 27,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "tools.toolchains.python": {
      "count": 27,
      "reasons": {
        "Python toolchain version not recorded for the public round data": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "tools.toolchains.ruby": {
      "count": 27,
      "reasons": {
        "Toolchain inventory not recorded": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    },
    "tools.toolchains.rust": {
      "count": 27,
      "reasons": {
        "Toolchain version not recorded": 27
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv."
    }
  },
  "gap_sources": {
    "reconstructable": {},
    "lost": {
      "circumstances.concurrent_cells_end": {
        "none": 27
      },
      "circumstances.concurrent_cells_start": {
        "none": 27
      },
      "circumstances.dispatcher_id": {
        "none": 27
      },
      "circumstances.incidents": {
        "none": 27
      },
      "circumstances.load1_end": {
        "none": 27
      },
      "circumstances.load1_start": {
        "none": 27
      },
      "circumstances.load_samples": {
        "none": 27
      },
      "circumstances.queue": {
        "none": 27
      },
      "cost.calculator_version": {
        "none": 27
      },
      "cost.price_table_version": {
        "none": 27
      },
      "cost.usd": {
        "none": 27
      },
      "effort.effective": {
        "none": 27
      },
      "environment.account_class": {
        "none": 27
      },
      "environment.network.allowlist_hosts": {
        "none": 27
      },
      "environment.network.profile": {
        "none": 27
      },
      "environment.toolchains.elixir": {
        "none": 27
      },
      "environment.toolchains.erlang": {
        "none": 27
      },
      "environment.toolchains.node": {
        "none": 27
      },
      "environment.toolchains.other_inventory": {
        "none": 27
      },
      "environment.toolchains.python": {
        "none": 27
      },
      "environment.toolchains.ruby": {
        "none": 27
      },
      "environment.toolchains.rust": {
        "none": 27
      },
      "grade.grader": {
        "none": 27
      },
      "model.effective": {
        "none": 27
      },
      "provenance.manifest_sha256": {
        "none": 27
      },
      "sandbox.egress_allow": {
        "none": 27
      },
      "sandbox.egress_profile": {
        "none": 27
      },
      "sandbox.profile": {
        "none": 27
      },
      "sandbox.profile_sha256": {
        "none": 27
      },
      "setup.adapter_harness_sha": {
        "none": 27
      },
      "setup.deps_source": {
        "none": 27
      },
      "setup.sandbox_mode": {
        "none": 27
      },
      "setup.sandbox_profile_sha256": {
        "none": 27
      },
      "stop_reason": {
        "none": 27
      },
      "timestamps.attempts": {
        "none": 27
      },
      "timestamps.cell.end_utc": {
        "none": 27
      },
      "timestamps.cell.start_utc": {
        "none": 27
      },
      "timestamps.phases.develop.end_utc": {
        "none": 27
      },
      "timestamps.phases.develop.start_utc": {
        "none": 27
      },
      "timestamps.phases.gate.end_utc": {
        "none": 27
      },
      "timestamps.phases.gate.start_utc": {
        "none": 27
      },
      "timestamps.phases.plan.end_utc": {
        "none": 27
      },
      "timestamps.phases.plan.start_utc": {
        "none": 27
      },
      "timestamps.phases.review.end_utc": {
        "none": 27
      },
      "timestamps.phases.review.start_utc": {
        "none": 27
      },
      "timestamps.phases.setup.end_utc": {
        "none": 27
      },
      "timestamps.phases.setup.start_utc": {
        "none": 27
      },
      "timestamps.phases.shape.end_utc": {
        "none": 27
      },
      "timestamps.phases.shape.start_utc": {
        "none": 27
      },
      "timing.phases_s.develop": {
        "none": 27
      },
      "timing.phases_s.grade": {
        "none": 27
      },
      "timing.phases_s.setup": {
        "none": 27
      },
      "tokens.phases.develop.cached_input": {
        "none": 27
      },
      "tokens.phases.develop.input": {
        "none": 27
      },
      "tokens.phases.develop.output": {
        "none": 27
      },
      "tokens.phases.develop.reasoning": {
        "none": 27
      },
      "tokens.total.reasoning": {
        "none": 27
      },
      "tools.grader": {
        "none": 27
      },
      "tools.runner": {
        "none": 27
      },
      "tools.toolchains.elixir": {
        "none": 27
      },
      "tools.toolchains.erlang": {
        "none": 27
      },
      "tools.toolchains.node": {
        "none": 27
      },
      "tools.toolchains.other_inventory": {
        "none": 27
      },
      "tools.toolchains.python": {
        "none": 27
      },
      "tools.toolchains.ruby": {
        "none": 27
      },
      "tools.toolchains.rust": {
        "none": 27
      }
    }
  },
  "protocol_deviations": [
    "The full Standard-record gate was deferred until analysis under the lane's emitter-gap exception. The referenced strict-exception receipt is not included in the public bundle; this retrospective record validation does not establish pre-run compliance.",
    "The exact pre-run design commitment and first-call-start receipts are not in the public bundle. Registration timing remains operator-reported.",
    "Per-cell runner manifests, sandbox fingerprints, phase counters, cost inputs, host-load samples, effective-setting receipts, and stop-cause receipts were not recovered into the public bundle. Missing fields remain explicit.",
    "The 31 reused t5-t7 cells are already represented in the Round 70 source cohort; this round's Standard file records only its 27 new scored cells to avoid duplicate exact identities."
  ]
}
```
