# kogen-prompt-cache-cold-starts

Why do about a quarter of Kogen's model requests get no prompt-cache discount, and does putting the unchanging testing rules at the front of each conversation's first message fix it? **The cold requests are the first request of each build and review conversation; moving the testing rules to the front does not make the provider reuse them (0 of 58 first requests got any cache, the same as without the change).** The provider reuses only a fixed 4,096-token front across conversations, and only the shaper's instructions and tool definitions are that long; the builder's and reviewer's are not, and text placed in the first message does not count toward it.

## What was looked at

**Model-free characterisation.** Earlier runs on one server (eu2): `lrp-eu2-r1` to `r5` (Kogen `69d09e1`) and `shc2-eu2-r1` to `r3` (Kogen `bc54c65`), 13 Go request-only tasks (`T01` to `T13`, names and hidden suites withheld), gpt-6.1-terra at medium effort for every role on the ChatGPT route. Every request's provider-reported usage (`input`, `cached`) and the local-byte fingerprints of the request front (instructions, tool definitions, opening message) were read from the cells' run logs and shaping event logs.

**One screen.** Kogen main `e6f69a155ed8e7d0907524903008db86e03e0413` (vendored kogen-loop `166ec7f`) against the same Kogen plus one lane patch, same model and effort for shape, build and review, the same 13 tasks, one paired run per task per repetition, stage `screen`, Kogen only. Runs `lcache-eu2-r1` (eu2), `lcache-eu-r1` (EU) and `lcache-st-r1` (Studio), lanes tree `a3fddb9e`, no pinned support directory. A fourth run (laptop) was taken off the queue before it started, once the change was seen not to work. The Studio run was slow on a loaded machine and is read as it stood 2 hours after launch: 12 of 26 cells, 6 pairs, not yet hidden-graded, so it counts for the cache measures only. The last cell used finished 19:19:49 UTC.

| Arm | Kogen | Artifact (linux x86_64 / darwin arm64 sha256) |
| --- | --- | --- |
| base | `e6f69a1` | `1933cdcf9c06f122a07bfc2ce6141a9c7c4126df8871803100fd6ca9511bea07` / `03a566fc3d46bcc95b647c50d11ce9eb265a823292813be682cc0c3bfd12b272` |
| lever | `e6f69a1` + `patches/lcache.diff` | `5509ed3958ffb778e3b8a574e7a359b8041795735805d646184a5c5af9dcebd7` / `d5f9f777733956307d7797c753d1e86e618a2ff579ec8b7bb3af10f40115d30c` |

The patch (sha256 `ad85813bb4a10f6621ddff1f2717d23d6a57eb7d157091d5750d7b7dcb6a440c`) moves the testing-rules section (15,677 bytes, the same in every conversation) from the middle to the head of the first block of the opening message in the builder's brief, the reviewer's authority, the shaper's contract and refine; no byte is added or removed, and the cache identity is unchanged. Kogen's own tests pass on the patched tree (`go vet`, `go test` on the shape context/refine and the build brief, review material, external-context, golden and review-retry tests); six test fixtures that pin the exact request bytes are updated by moving the same section (`golden_move.py`).

## Result

### Where the cold requests are (earlier runs, 184 cells)

| Conversation | First requests | Got no cache | Got exactly 4,096 | Got more (same task, whole prompt repeated) | Instructions + tool definitions |
| --- | ---: | ---: | ---: | ---: | --- |
| build | 147 | 147 | 0 | 0 | 3,246 + 2,866 bytes |
| review | 136 | 136 | 0 | 0 | 6,451 + 3,227 bytes |
| shaping | 184 | 1 | 111 | 72 | 16,792 + 6,668 bytes |
| shaping example check | 190 | 189 | 0 | 0 (1 smaller) | 959 + 611 bytes |

Later requests in a conversation are almost never cold (11 of 2,294): each one starts with the whole previous request, which the provider has just seen. So the cold requests are the conversation starts, about two per cell (one build, one review), and they carry 9.2% of all input tokens (shaping included; 16% of build and review input). Instructions and tool definitions are byte-identical in every conversation of a role, and every conversation has its own random cache key (Kogen's specification: different conversations never share one), yet the shaper's first request always reuses 4,096 tokens from other tasks' conversations. The builder's and reviewer's first requests never reuse anything, although their instructions and tools are also identical every time. The difference is size: only the shaper's unchanging front (instructions plus tools, 23 KB) is long enough.

The largest unchanging block, the testing rules (15,677 bytes), sits in the middle of every first message, after text that differs per run (source provenance, the Intent, the request, the README). That is why the lever moved it to the front.

### The screen (3 runs, 32 pairs)

| Measure | base | lever |
| --- | ---: | ---: |
| Build first requests with any cache | 0 / 32 | 0 / 30 |
| Review first requests with any cache | 0 / 30 | 0 / 28 |
| Shaping first requests: exactly 4,096 / more | 27 / 5 | 32 / 0 |
| Cached share of all input (pooled) | 84.2% | 81.5% |
| Cached share, paired difference | | -0.8 points (95% CI -2.1 to +0.5) |
| Cost index, paired ratio (uncached 1, cached 0.1, output 8) | | 0.92 (95% CI 0.83 to 1.01) |
| Requests, paired difference | | -1.8 (95% CI -4.0 to +0.5) |
| Hidden pass (26 graded pairs, eu2 and EU) | 19 / 26 | 17 / 26 |

The change does not fire. Several lever first requests came 40 seconds to 4 minutes after another lever conversation had sent the identical new front on the same account, and still reused nothing; the lever's shaping first requests stayed at exactly 4,096, although their unchanging front is now about 39 KB. Text placed in the first message does not extend what a new conversation can reuse; only the 4,096-token front does, and in Kogen only the shaper's instructions and tools reach it. The five base shaping requests that reused more than 4,096 tokens repeated a whole first request of the same task that another study had just sent with the same Kogen build; the lever's reordered prompt had no such twin, which is part of why its pooled cached share is slightly lower. The cost index favours the lever by 8% but its interval includes no change, and it comes from fewer and shorter requests, not from caching.

Hidden passes, every pair that changed (classes as in the earlier screens: a = caused by the patched stage, b = a defect written at shaping time, e = no stage cause shown): two lever losses are builds the builder stopped because the shaped acceptance contradicted the rules (one is the known negative-zero equality trap seen in both arms of earlier screens, b; one is a tie-order contradiction, b, a possible but unproven a because shaping is a patched stage here); the other two pairs are the same hidden test failing once on each side (e). Net -2 in 26 pairs, inside ordinary pair-to-pair flipping.

### What could still work

A shared cache key per role would let new conversations land where the same front was just processed. Kogen's specification gives every conversation its own key so that a reviewer never inherits builder state; changing that is a decision for Kogen's owner, not a screen, and the possible gain is small (the cold starts are 9% of input). Moving the testing rules into the builder's and reviewer's instructions would make their unchanging front long enough for the 4,096-token reuse; that is a change to what the builder and reviewer are told and needs its own full-pipeline screen; it would save at most about 4,000 cached tokens per first request.

## Limits

The provider's caching is observed from the outside (provider-reported cached tokens); the 4,096-token front is the pattern in 841 first requests, not a documented rule, and it may differ for other models or routes. One model and route (gpt-6.1-terra, ChatGPT). The screen is small (32 pairs, 26 graded) because the change visibly did nothing; hidden passes are a guard, not a test. The base arm shared hosts and the account with another study running the same Kogen build, which gave some base shaping requests whole-prompt reuse the lever could not get. Wall time includes failed attempts and overlapping work and is not reported as a result.

## Rerun

```sh
python3 -I reproduce/kogen-prompt-cache-cold-starts/report.py reproduce/kogen-prompt-cache-cold-starts/data | diff - reproduce/kogen-prompt-cache-cold-starts/expected-output.txt
```

`report.py` uses only the standard library and rebuilds every count above from `data/firsts.tsv` (one row per conversation start: study, run, task, arm, role, time, input tokens, cached tokens, instructions and tool-definition bytes) and `data/cells.tsv` (one row per cell: outcome, hidden pass, requests, input, cached and output tokens, later requests and how many of them were cold, wall seconds). `build_data.py` produced both from the run directories (`python3 -I build_data.py <out> baseline=<runs root>:lrp-eu2-r1,... screen=<runs root>:lcache-eu2-r1`). To run the screen again you need the two Kogen builds above (build `e6f69a1` with and without `patches/lcache.diff` and compare the artifact sha256), the 13 Go request-only tasks with their hidden graders, lanes `a3fddb9e` (experiment `lcache-<host>-r<N>`, lane `g0` with no patch, lane `g1` with the patch) and a ChatGPT login for gpt-6.1-terra at medium effort.
