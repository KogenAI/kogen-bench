# HC01 post-release missing-field declaration

This inventory is generated from the two sanitized schema-1.2 smoke records. It lists only fields that still contain a missing marker; outcome, official grade, cost, and decision fields are complete. The recorded API-equivalent USD uses aggregate Kogen token usage and levers/cost.py; long-context reconciliation is explicitly false because request-level usage totals are unavailable.

The allowed bulk dry-run receipt specifies one job at a time but marks the smoke cells as already complete; it does not establish their dispatcher hash or host-wide boundary samples. The final strict validator run returned rc 1 with 58 of 296 field slots missing (80.405% complete); it reported no record-schema errors. Its four errors are the absent round-level MISSING.md, README.md, and MEASURED.md plus the strict deviation-declaration check, because the validator cannot see this lane declaration. The kogen-bench checkout is read-only, so those round files were not created there.

```json
{
  "cells": 2,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "Not recorded in available public metadata": 2
      }
    },
    "circumstances.cap_start": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "Not recorded in available public metadata": 2
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 2
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 2
      }
    },
    "circumstances.dispatcher_id": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "Per-cell dispatcher revision is not present in the public round data": 2
      }
    },
    "circumstances.incidents": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "Per-cell incident receipt was not captured": 2
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "Host boundary load was not captured in the public round data": 2
      }
    },
    "circumstances.load_samples[].pressure": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "Not recorded in available public metadata": 2
      }
    },
    "environment.account_class": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "No dated account-class receipt": 2
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "Absolute phase boundary not retained": 2
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "Absolute phase boundary not retained": 2
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "Absolute phase boundary not retained": 2
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "Absolute phase boundary not retained": 2
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "Absolute phase boundary not retained": 2
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "Absolute phase boundary not retained": 2
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "Absolute phase boundary not retained": 2
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "Absolute phase boundary not retained": 2
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "Absolute phase boundary not retained": 2
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "Absolute phase boundary not retained": 2
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "Absolute phase boundary not retained": 2
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "Absolute phase boundary not retained": 2
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "Absolute phase boundary not retained": 2
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "develop phase timing was not separately recorded in the public round data": 2
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "Phase wall not emitted or not separable": 2
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "grade phase timing was not separately recorded in the public round data": 2
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "Phase wall not emitted or not separable": 2
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "Phase wall not emitted or not separable": 2
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "setup phase timing was not separately recorded in the public round data": 2
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Required record field is absent; strict completeness is not met.",
      "count": 2,
      "reasons": {
        "Phase wall not emitted or not separable": 2
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 2
      },
      "circumstances.cap_start": {
        "none": 2
      },
      "circumstances.concurrent_cells_end": {
        "none": 2
      },
      "circumstances.concurrent_cells_start": {
        "none": 2
      },
      "circumstances.dispatcher_id": {
        "none": 2
      },
      "circumstances.incidents": {
        "none": 2
      },
      "circumstances.load1_end": {
        "none": 2
      },
      "circumstances.load_samples[].pressure": {
        "none": 2
      },
      "environment.account_class": {
        "none": 2
      },
      "timestamps.phases.develop.end_utc": {
        "none": 2
      },
      "timestamps.phases.develop.start_utc": {
        "none": 2
      },
      "timestamps.phases.gate.end_utc": {
        "none": 2
      },
      "timestamps.phases.gate.start_utc": {
        "none": 2
      },
      "timestamps.phases.grade.end_utc": {
        "none": 2
      },
      "timestamps.phases.plan.end_utc": {
        "none": 2
      },
      "timestamps.phases.plan.start_utc": {
        "none": 2
      },
      "timestamps.phases.review.end_utc": {
        "none": 2
      },
      "timestamps.phases.review.start_utc": {
        "none": 2
      },
      "timestamps.phases.setup.end_utc": {
        "none": 2
      },
      "timestamps.phases.setup.start_utc": {
        "none": 2
      },
      "timestamps.phases.shape.end_utc": {
        "none": 2
      },
      "timestamps.phases.shape.start_utc": {
        "none": 2
      },
      "timing.phases_s.develop": {
        "none": 2
      },
      "timing.phases_s.gate": {
        "none": 2
      },
      "timing.phases_s.grade": {
        "none": 2
      },
      "timing.phases_s.plan": {
        "none": 2
      },
      "timing.phases_s.review": {
        "none": 2
      },
      "timing.phases_s.setup": {
        "none": 2
      },
      "timing.phases_s.shape": {
        "none": 2
      }
    },
    "reconstructable": {}
  },
  "protocol_deviations": [
    "The smoke receipts do not contain absolute phase boundaries or host-wide dispatcher/resource boundary captures; these remaining slots are enumerated exactly in fields.",
    "The allowed bulk dry-run receipt shows jobs=1 but lists the smoke cells as skipped-complete; it does not establish those earlier smoke cells' dispatcher SHA or host-wide start/end samples.",
    "Kogen usage is aggregate, so per-request long-context surcharge reconciliation is unavailable; cost.usd is the Standard API aggregate calculation and long_context_reconciled is explicitly false.",
    "The read-only kogen-bench repository has no rounds/hc01-small32/MISSING.md, README.md, or MEASURED.md; this lane declaration was updated without writing to that repository."
  ],
  "round": "hc01-small32"
}
```
