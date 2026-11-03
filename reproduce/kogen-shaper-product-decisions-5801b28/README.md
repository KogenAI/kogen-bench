# kogen-shaper-product-decisions-5801b28

Does a rule telling Kogen's shaping step to decide evidence-backed or reversible product questions itself, instead of asking the requester, get a stuck ticket to a finished Intent? **No. On the one ticket tried (three runs per arm), neither the adopted release nor the patched one produced an Intent: all six runs stopped on a single question. The rule changed how the question was worded and what options it offered, not what was asked. Verdict: same, no improvement. This is a small check (n=3 per arm, one ticket), not a general claim.**

## What was tried

With no one to answer questions, the shaping step stops as soon as it asks one. On a ticket about exporting and importing an account's data in a Rails app, the adopted release (Kogen 573d023) asked one question in every run and so ended with no Intent. The question was always about how the restored people should regain access to the new account. The options differed from run to run, so the choice was not settled by the application.

The candidate adds one rule to the shaper's instructions: look at the application code, tests and conventions first; when they, or a conventional and reversible default, settle a product detail, decide it, record it visibly under Decisions with its basis and the existing assumption marker, and carry on to a full Intent. Still ask when only the requester can know the answer (credentials, external accounts, business or legal facts) or when no sensible default exists and a wrong choice is costly; keep the mandatory security and authentication handoffs. A different model from the shaper wrote the patch from a problem description only, with no ticket text and no scoring material.

## Setup

- **Arms:** adopted release 573d023 (base) and the same release with only the shaping component replaced by the patched one (candidate). Release archive hashes: base `6e6c2587b2d85da8d61924c422750e3acdf208dcd2c6e3b0e2a5ce2ccc3186fa`; candidate `5801b287bda7a16ade89c839c4ffc5e385f8ce569247c75a930d9ea8539dd32e`.
- **Roles and model:** only the shaping role runs in this check (shape phase, stop at the final Intent; no approval, build or review). Shaper: gpt-6.1-terra at medium effort, through Kogen's configured provider on a signed-in seat (no API key), the same in both arms. The build and review roles are configured the same but never ran.
- **Same conditions:** same host, same ticket and starting tree, same Kogen settings, three runs per arm, no answerer, default 3600 s deadline, one lane per run.
- **Patch present in the binary:** the candidate binary contains the new rule text (checked by searching its text); the base binary does not. The run records pin the candidate archive hash.
- **Reading rule (set before the runs):** a run that ends on a question with no Intent counts as a failed Intent, not a dropped run. The scorer would only be called if an Intent existed; none did.

## Result

| arm | runs | Intents saved | ended on a question | model requests | input tokens | output tokens |
|---|---|---|---|---|---|---|
| base | 3 | 0 | 3 | 9 | 119,808 | 1,257 |
| candidate | 3 | 0 | 3 | 17 | 334,419 | 2,288 |

- **Same question, new wording:** all six runs asked one question about how restored people get access. In the candidate runs the question text gave more reasons (granting access from an uploaded file's email addresses could reach the wrong person) and offered two or three options; the recommended option differed between runs in both arms. The rule changed wording and option sets only.
- **More looking, no more deciding:** the candidate made 5 to 6 model requests per run instead of 3 and used about 2.8 times the input tokens. The inspection the rule asks for happened; the decision did not follow.
- **Why it may be right to ask:** granting access to people named in an uploaded file is the kind of choice the rule itself keeps as a question (only the requester knows, and it has a security side). So this ticket may be a poor fit for the rule rather than a failure of it. One ticket cannot tell the two apart.
- **A wording slip:** one candidate run printed the "recommended" tag twice on the same option.
- **Cost:** tokens only; the model is unlisted so no dollars are recorded. Every run stayed under the per-run watch limits. Time from the finished patch to the last candidate result was about 8 minutes, most of it the build and the queue.

See `data/cells.tsv` and `data/questions.tsv`.

## Limits

- One ticket, three runs per arm, no answerer, shaping only. Whether the ticket's question counts as one the rule should resolve is a judgement, and no held-out ticket was run.
- No Intent was produced, so nothing was scored for coverage or invented requirements.
- A similar change from the Kogen delivery team (deciding non-UX questions without asking) has since landed in the shaping component and has its own screen; this candidate is dropped rather than stacked on it.

## Rerun

Apply the one-rule patch to the shaping component at the adopted pin and assemble a release with only that component replaced (patch file hash `4d69da72d99ea7cf205831cec3267470ce6de32b742cb7812b2ca610d8d3efaa`). Then run the shape phase three times per arm with no answerer, using the same model and effort, and count Intents saved:

```sh
kogen intent shape <ticket> < request.md   # per run; exit code 5 means it stopped on a question
```

The rule text is the one described under "What was tried"; the component repositories are private. To recompute the verdict from the recorded tables:

```sh
python3 -I reproduce/kogen-shaper-product-decisions-5801b28/report.py reproduce/kogen-shaper-product-decisions-5801b28/data/cells.tsv reproduce/kogen-shaper-product-decisions-5801b28/data/questions.tsv | diff - reproduce/kogen-shaper-product-decisions-5801b28/expected-output.txt
```
