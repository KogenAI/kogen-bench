Build kogen-mini from the frozen SPEC.md, PROTOCOL.md, quint/ models, features/ scenarios and STEPS.md in spec/. Those documents define the external contract; do not change them.

Everything must be implemented in Go.

Work as one builder using gpt-6.1-sol with high reasoning effort. Do not use reviewers, subagents, delegation or additional model sessions. You have a 90-minute build cap. Write and run your own tests; hidden tests are unavailable. Start each shell with `. ./.kit-env.sh`. Kit templates and caches are starting aids; use or remove their sample application code as needed.

REAL-WORKFLOW: Hex and Go module installation, normal documentation browsing and web search are allowed. Do not access kogen.dev, operator.kogen.dev, github.com/KogenAI, any existing Kogen repository, another arm, harness outputs, hidden tests, the witness, model session stores or protected files outside this workspace. Do not make real model-provider calls from your commands. Violations void the run. The harness observes commands and audits them; no complete OS access boundary is claimed.

Provide a prebuilt executable or wrapper `./kogen` at the workspace root. It must run from a relocated snapshot without fetching packages. Bundle runtime dependencies in the workspace; snapshots retain deps/ and _build/ but omit private .kitcache/, .kit-tools/ and .cache/. Do not rely on absolute workspace paths. Read the kit language aids under docs/ and USAGE_RULES.md when present.

Keep a concise BUILD-LOG.md with the commands and elapsed times of your build and test checks. When you believe all your own tests pass, state exactly `ALL TESTS PASS` in your assistant response; later continuation turns are counted as repair turns. This claim does not expose or imply a hidden-test result.
