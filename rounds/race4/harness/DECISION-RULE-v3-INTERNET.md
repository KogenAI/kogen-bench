# Archived Internet and package policy draft

This document did not govern the race. The governing policy is included in DECISION-RULE-v3.md.

Agents may install packages using their ecosystem's package manager and read
documentation on the web as a developer normally would. Calls to real model
providers remain forbidden; the suite uses a local fake. The agent's own Codex
client traffic is not visible to the command audit and is not flagged.

Each arm receives its own writable caches inside its repository, seeded with
copies of the prefetched kit caches. Cargo, Go, Mix/Hex, Bun, XDG and npm caches
are private; no arm shares writable caches with another. Agent environments
remove offline switches and restore Go's normal package proxy and checksum service.

Scoring and warm-up run offline using dead HTTP/HTTPS/ALL proxies at
`http://127.0.0.1:9`, with `NO_PROXY=127.0.0.1,localhost` for the local fake, and
Cargo, Go, Hex and npm offline switches. The harness exec wrapper reapplies these
settings after the conformance runner's environment filtering. GOFLAGS is unset;
build-cache variables are removed from the implementation environment and the
deliverable is prebuilt. macOS offers no unprivileged hard network block:
this policy is enforced by proxies and offline flags, not a kernel network deny.

Every runtime dependency must be vendored, bundled or cached inside repository
content retained in snapshots, which include build output. The snapshot mechanism
excludes `.kitcache/`, so implementations must not depend on that build cache at
runtime or on paths back to the original arm or kit.

The command audit logs observed network accesses and package installs per arm in
`out/network-<arm>.log`; those accesses are permitted. Command-policy flags apply
only to real provider calls and reads outside the arm of `$HOME/.codex*`, `$HOME/Library`,
iCloud, `$HOME/Areas`, other arms or other races. Existing frozen-input, snapshot and
model/effort receipt integrity checks remain in force. This is a static event-log
audit, not packet capture; it cannot observe hidden traffic inside arbitrary
programs or the agent's Codex client.

Supervisor smoke (after final inputs are frozen):
`./smoke-race4.sh`. Preview with `./smoke-race4.sh --dry-run`.
The smoke prepares fresh arms, installs one package per ecosystem, builds native
stubs that use the installed package, snapshots them, and verifies each warm-up
and the suite's version case through the offline `score-arm.sh` path. Smoke runs
are isolated under this harness and retained for review; no models are launched.
