# kogen-loop-tool-error-classes-2fc1eb7

Does the newer version of Kogen's loop (`2fc1eb7`, which classifies tool errors and malformed tool calls) send the model anything different from the version Kogen currently vendors (`c6e2360`)? **No. In six scripted sessions covering tool errors, malformed calls and mixed calls, every request body is byte-identical across the vendored version, the version before the change (`fe2bcd7`) and the new one. The change only adds fields to the loop's own event log. This is a model-free check; no model was run, so it says nothing about quality, only that the model receives the same bytes.**

## What changed

Every tool in the loop now returns its result together with two category labels, an error kind and a malformed-call class. The session writes those labels into the `tool.result` event it logs. They never reach the text or parts that are sent back to the model. Every error text, every tool output string, the system prompt, the tool definitions, retries and timing bounds are unchanged, and a new test checks that the event names the labels.

## Evidence (no model calls, cost 0)

- **Read of the change:** the diff from `fe2bcd7` to `2fc1eb7` in the loop, tools and API files adds constants and the label fields; each error string and branch is the same as before.
- **Scripted sessions:** a fake provider (from the repository's own conformance harness) replays three scripts, each run once as one batched exchange and once with one call per exchange: 9 tool-error calls (missing file, directory read, path escape, protected file, unknown shell handle, a kill of a foreign process, a bad image, home path, search under a file), 11 malformed calls (unknown tool, missing or null or wrong-typed arguments, conflicting shell arguments) and 5 mixed ok and error calls. That is 6 sessions and 34 recorded request bodies per version.
- **Result:** after replacing the random cache key (`session-` followed by 16 hex digits, which changes on every run, even between two runs of the same version), all 6 recorded files are byte-identical across the three versions (equal sha256).
- **Existing tests:** the loop, provider, system and tools packages pass at the vendored version and at `2fc1eb7`. The conformance package fails the same two tests at both versions (one of them is this pack's own test when its output directory is unset); no difference between the versions. The new test for the event labels passes at `2fc1eb7`.

## Limits

A fake provider, not a live model; only the six sessions above; Linux only. A change that alters bytes in a case these sessions do not exercise would not show here.

## Rerun

```sh
python3 -I reproduce/kogen-loop-tool-error-classes-2fc1eb7/report.py reproduce/kogen-loop-tool-error-classes-2fc1eb7/data/sessions.tsv | diff - reproduce/kogen-loop-tool-error-classes-2fc1eb7/expected-output.txt
```

`report.py` uses only the standard library and rebuilds the counts above from `data/sessions.tsv`.

To repeat the byte comparison, clone the public `KogenAI/kogen-loop` repository and check out each of `c6e2360`, `fe2bcd7` and `2fc1eb7` in turn. Copy `l1_request_bytes_test.go` from this pack into the `conformance/` directory and run:

```sh
L1_OUT=<output dir for this version> go test ./conformance -run TestL1RequestBytes -count=1 -buildvcs=false
```

Then in each output file replace `session-` plus 16 hex digits with `session-X` and compare the six files across the three versions; the expected result is that they are identical.
