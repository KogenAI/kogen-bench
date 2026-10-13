# Missing and unresolved coverage

This observation preserves invalid and not-run rows rather than treating them as successful containment.

| Arm and fixtures | Rows | Published status | Effect |
|---|---:|---|---|
| b: file_read_outside, secret_file_read, net_loopback | 9 | INVALID(launch ok), three repetitions per fixture | The launcher completed, but the apparatus did not prove the fixture result. No containment pass is claimed. |
| c2: all 11 fixtures | 33 | NOT-RUN, three planned repetitions per fixture | Its live allowed_rw control did not produce the expected marker. A manual nono run in the same scope did; the cause remains unresolved. No c2 result is inferred. |
| z: mem_cap, pids_cap | 6 | UNSUPPORTED(no mechanism), three repetitions per fixture | These cells document that the control has no such mechanism. They are not cap enforcement successes. |

## Limits that remain

- One EU host and one kernel; three repetitions per fixture.
- No language model was run.
- The fixture set is small and does not establish broad containment.
- c2 has no measured cells.
- The b read and loopback-network outcomes are invalid.
- The b memory and process-count results are for a composite systemd-scoped arm.
- The evidence does not compare either arm with Kogen's own containment helper. CORE-04 is separate and still under qualification.
- No ranking or deployment qualification follows from this round.
- Hardware model and total memory allocation were not established in the published environment record.
- macOS documentation review is not included as measurement.

The detailed machine-readable declarations are in MISSING-DECLARED.json. Hashes identify the private per-cell source JSON, but do not expose its machine-local paths or contents.

## Standard run-record coverage

The Standard run-record file contains the 66 executed z and b fixture observations. All 99 planned statuses, including 33 c2 NOT-RUN rows, remain in the result data. The records do not claim an official model grade.

```json
{
  "cells": 66,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m08",
      "reasons": {
        "Boundary telemetry not retained": 66
      }
    },
    "circumstances.cap_start": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m08",
      "reasons": {
        "Boundary telemetry not retained": 66
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m66",
      "reasons": {
        "Host-wide concurrent cell count was not captured": 66
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m66",
      "reasons": {
        "Host-wide concurrent cell count was not captured": 66
      }
    },
    "circumstances.dispatcher_id": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m63",
      "reasons": {
        "Exact dispatcher revision is not present in the public receipt extract": 66
      }
    },
    "circumstances.incidents": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m78",
      "reasons": {
        "Per-cell incident receipt was not captured": 66
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m65",
      "reasons": {
        "Host boundary load was not captured in the public round data": 66
      }
    },
    "circumstances.load1_start": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m65",
      "reasons": {
        "Host boundary load was not captured in the public round data": 66
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m93",
      "reasons": {
        "Timestamped host-wide load samples were not captured": 66
      }
    },
    "circumstances.queue": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m91",
      "reasons": {
        "Queue receipt was not captured": 66
      }
    },
    "cost.accounting": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m70",
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 66
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m61",
      "reasons": {
        "Cost calculator version not recorded": 66
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m07",
      "reasons": {
        "Boolean receipt not recorded": 66
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m89",
      "reasons": {
        "Price table version not recorded": 66
      }
    },
    "cost.usd": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m70",
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 66
      }
    },
    "environment.account_class": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m62",
      "reasons": {
        "Dated account-class receipt is not present in the public round data": 66
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m34",
      "reasons": {
        "No per-cell CPU receipt": 66
      }
    },
    "environment.network.allowlist_hosts": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m79",
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 66
      }
    },
    "environment.network.profile": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m80",
      "reasons": {
        "Per-cell network profile not present in the public round data": 66
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m35",
      "reasons": {
        "No per-cell RAM receipt": 66
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m64",
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 66
      }
    },
    "environment.toolchains.python": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m90",
      "reasons": {
        "Python toolchain version not recorded for the public round data": 66
      }
    },
    "grade.grader": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m77",
      "reasons": {
        "Per-cell grader software version is not in the public data": 66
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m81",
      "reasons": {
        "Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt": 66
      }
    },
    "host.cpu": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m34",
      "reasons": {
        "No per-cell CPU receipt": 66
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m35",
      "reasons": {
        "No per-cell RAM receipt": 66
      }
    },
    "outcome": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m32",
      "reasons": {
        "No official grade in the public snapshot": 66
      }
    },
    "sandbox.egress_allow": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m75",
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 66
      }
    },
    "sandbox.egress_profile": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m76",
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 66
      }
    },
    "sandbox.profile_sha256": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m86",
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 66
      }
    },
    "setup.adapter_harness_sha": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m67",
      "reasons": {
        "Per-cell Codex adapter fingerprint not recorded in the public round data": 66
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m11",
      "reasons": {
        "Dependency source not pinned per cell": 66
      }
    },
    "setup.sandbox_profile_sha256": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m86",
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 66
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m42",
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 66
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m43",
      "reasons": {
        "Original base revision type not recorded per cell": 66
      }
    },
    "task.base_repo": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m52",
      "reasons": {
        "Task identity not retained": 66
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m42",
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 66
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m43",
      "reasons": {
        "Original base revision type not recorded per cell": 66
      }
    },
    "task.id": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m52",
      "reasons": {
        "Task identity not retained": 66
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m60",
      "reasons": {
        "Attempt-boundary receipts are not in the public round data": 66
      }
    },
    "timestamps.cell.end_utc": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m68",
      "reasons": {
        "Per-cell contestant end timestamp not recorded in the public round data": 66
      }
    },
    "timestamps.cell.start_utc": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m69",
      "reasons": {
        "Per-cell contestant start timestamp not recorded in the public round data": 66
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m88",
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 66
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m88",
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 66
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m88",
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 66
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m88",
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 66
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m88",
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 66
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m88",
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 66
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m88",
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 66
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m88",
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 66
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m88",
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 66
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m88",
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 66
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m88",
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 66
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m88",
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 66
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m88",
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 66
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m88",
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 66
      }
    },
    "timing.timeout_cap_s": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m53",
      "reasons": {
        "Timeout receipt unavailable": 66
      }
    },
    "timing.total_wall_s": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m58",
      "reasons": {
        "Wall counter unavailable": 66
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m56",
      "reasons": {
        "Usage counter unavailable": 66
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m56",
      "reasons": {
        "Usage counter unavailable": 66
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m56",
      "reasons": {
        "Usage counter unavailable": 66
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m56",
      "reasons": {
        "Usage counter unavailable": 66
      }
    },
    "tools.runner": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m83",
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 66
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m64",
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 66
      }
    },
    "tools.toolchains.python": {
      "affects_verdict": "Limits metadata completeness and strict release eligibility; it does not change the retained fixture observations.",
      "count": 66,
      "note": "The per-cell receipt is not present in the public round record.",
      "reason_code": "m90",
      "reasons": {
        "Python toolchain version not recorded for the public round data": 66
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 66
      },
      "circumstances.cap_start": {
        "none": 66
      },
      "circumstances.concurrent_cells_end": {
        "none": 66
      },
      "circumstances.concurrent_cells_start": {
        "none": 66
      },
      "circumstances.dispatcher_id": {
        "none": 66
      },
      "circumstances.incidents": {
        "none": 66
      },
      "circumstances.load1_end": {
        "none": 66
      },
      "circumstances.load1_start": {
        "none": 66
      },
      "circumstances.load_samples": {
        "none": 66
      },
      "circumstances.queue": {
        "none": 66
      },
      "cost.accounting": {
        "none": 66
      },
      "cost.calculator_version": {
        "none": 66
      },
      "cost.long_context_reconciled": {
        "none": 66
      },
      "cost.price_table_version": {
        "none": 66
      },
      "cost.usd": {
        "none": 66
      },
      "environment.account_class": {
        "none": 66
      },
      "environment.cpu_model": {
        "none": 66
      },
      "environment.network.allowlist_hosts": {
        "none": 66
      },
      "environment.network.profile": {
        "none": 66
      },
      "environment.ram_gib": {
        "none": 66
      },
      "environment.toolchains.other_inventory": {
        "none": 66
      },
      "environment.toolchains.python": {
        "none": 66
      },
      "grade.grader": {
        "none": 66
      },
      "grade.timestamp": {
        "none": 66
      },
      "host.cpu": {
        "none": 66
      },
      "host.ram_gib": {
        "none": 66
      },
      "outcome": {
        "not re-derivable from the public record": 66
      },
      "sandbox.egress_allow": {
        "none": 66
      },
      "sandbox.egress_profile": {
        "none": 66
      },
      "sandbox.profile_sha256": {
        "none": 66
      },
      "setup.adapter_harness_sha": {
        "none": 66
      },
      "setup.deps_source": {
        "none": 66
      },
      "setup.sandbox_profile_sha256": {
        "none": 66
      },
      "setup.task_base.hash": {
        "none": 66
      },
      "setup.task_base.kind": {
        "none": 66
      },
      "task.base_repo": {
        "none": 66
      },
      "task.base_revision.hash": {
        "none": 66
      },
      "task.base_revision.kind": {
        "none": 66
      },
      "task.id": {
        "none": 66
      },
      "timestamps.attempts": {
        "none": 66
      },
      "timestamps.cell.end_utc": {
        "none": 66
      },
      "timestamps.cell.start_utc": {
        "none": 66
      },
      "timestamps.phases.develop.end_utc": {
        "none": 66
      },
      "timestamps.phases.develop.start_utc": {
        "none": 66
      },
      "timestamps.phases.gate.end_utc": {
        "none": 66
      },
      "timestamps.phases.gate.start_utc": {
        "none": 66
      },
      "timestamps.phases.grade.end_utc": {
        "none": 66
      },
      "timestamps.phases.grade.start_utc": {
        "none": 66
      },
      "timestamps.phases.plan.end_utc": {
        "none": 66
      },
      "timestamps.phases.plan.start_utc": {
        "none": 66
      },
      "timestamps.phases.review.end_utc": {
        "none": 66
      },
      "timestamps.phases.review.start_utc": {
        "none": 66
      },
      "timestamps.phases.setup.end_utc": {
        "none": 66
      },
      "timestamps.phases.setup.start_utc": {
        "none": 66
      },
      "timestamps.phases.shape.end_utc": {
        "none": 66
      },
      "timestamps.phases.shape.start_utc": {
        "none": 66
      },
      "timing.timeout_cap_s": {
        "none": 66
      },
      "timing.total_wall_s": {
        "none": 66
      },
      "tokens.total.cached_input": {
        "none": 66
      },
      "tokens.total.input": {
        "none": 66
      },
      "tokens.total.output": {
        "none": 66
      },
      "tokens.total.reasoning": {
        "none": 66
      },
      "tools.runner": {
        "none": 66
      },
      "tools.toolchains.other_inventory": {
        "none": 66
      },
      "tools.toolchains.python": {
        "none": 66
      }
    },
    "reconstructable": {}
  },
  "protocol_deviations": [
    "The measurement used standalone fixtures rather than model-run tasks, so task, model, and official-grade data are absent or not applicable.",
    "The public record does not include all per-cell timing, cost, sandbox, and host-load receipts required for complete Standard capture."
  ],
  "round": "containment-small-eu"
}
```
