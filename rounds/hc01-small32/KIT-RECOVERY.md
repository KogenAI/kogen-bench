# HC01 rerun-kit recovery

Recorded 2026-10-08. This is evidence for four completed attempts found on `kogen-bench-us`: syn06 r1 OFF/ON and board r1 OFF/ON. The active attempt was excluded, and not-yet-started cells were not inspected. The release-checklist receipt was consulted read-only for items 4, 5, and 10 and was not changed. No launcher, PLAN.json, running-cell files, grade rows, COMPLETE/manifest JSON, or raw cell output was read or changed. The host work was read-only and ran at nice 10. The full per-cell records and all 2,124 PATH tool hashes are in kit-recovery.json (not included in this public extract).

## Recovered values and method

- **Network policy:** each selected attempt config records `chatgpt.com-only egress` in `isolation_flags`; compacted whitespace, trimmed, encoded as UTF-8 without a trailing newline, then SHA-256 hashed. All four hashes are `ed018f18885f493c51a38239bad2d41557a12df85b89fc95196e527d8a9c30c4`. The per-cell `egress.jsonl` metadata showed `chatgpt.com` as the observed host; this is an observation, not a substitute for the policy clause.
- **Mount/bind inventory:** parsed the actual bwrap argv saved in each attempt’s `sandbox.sb`, took mount operations before the `--` command separator, represented each as operation/source/target (or operation/target), sorted by compact sorted-key JSON encoding, serialized as UTF-8 compact sorted-key JSON without a trailing newline, and SHA-256 hashed. The four values are in the table. Each underlying `sandbox.sb` SHA is also recorded in the JSON.
- **Tools:** for each recorded `PATH` (`/usr/bin:/bin:/usr/sbin:/sbin`), enumerated the first executable of each name in PATH precedence order, resolved symlinks, and recorded the executable’s SHA-256. The canonical list is sorted by tool name and hashed as compact sorted-key UTF-8 JSON without a trailing newline. All four attempts have 2,124 tools and inventory SHA `6377e357c7e48fa0df1b23dd6ff4564fd9a85a303ef2f51577b15b714767333e`.
- **Commands and inputs:** each cell has one replay command below and in the JSON. The deployed spec, attempt config, wrapper, sandbox file, and binary hashes are recorded per cell. The command is documentation only; it was not run.

| Cell | Spec SHA-256 | Config SHA-256 | `sandbox.sb` SHA-256 | Network policy SHA-256 | Mount inventory SHA-256 | Tool inventory SHA-256 |
| --- | --- | --- | --- | --- | --- | --- |
| syn06 r1 OFF | `2b678c8c46ec5e58f263eb9ee395bbc9e6599075e9bcd80882881a130dc937c8` | `775f6d3df6f88179d694d713032f538d1ecdec4bce97950e537132d1f07ad5d4` | `1dc50f4f70d3e68b6f8b8d96d1c24cb8514b7907e611dbaa2156b03696578627` | `ed018f18885f493c51a38239bad2d41557a12df85b89fc95196e527d8a9c30c4` | `13d9bcd3a158e169e6cee273020ce36e4d946f5eaf7496ee79d18a30bf62cb25` | `6377e357c7e48fa0df1b23dd6ff4564fd9a85a303ef2f51577b15b714767333e` |
| syn06 r1 ON | `ae734e76fe0c8ec1775dff669294c49e238c78c0dc3a3f421d793486d4685934` | `af488199357d78c7acdece4ddd5e834ce25ae66706de6545e06b2de53ca52485` | `ae716b886df616bf9ae4cd18044612815a705f5d2574c149b401b503887c8c22` | `ed018f18885f493c51a38239bad2d41557a12df85b89fc95196e527d8a9c30c4` | `0ab6b8bf82d5ff874d6a412b1898222c2254552b4d1a00ba494da8173bbf5b92` | `6377e357c7e48fa0df1b23dd6ff4564fd9a85a303ef2f51577b15b714767333e` |
| board r1 OFF | `9483e29cd8c7e15384a3c88be12cca3adfe466efcde63b6c44c851dfa10eb90f` | `eca39863c44ce0a98c61c6e124ae4f25bad97f6ed501b6dd4798101fc9fc0e98` | `25993f2ee7cd2a49ac6b12045da68ba8d640ee94ab5b015754acab82be5c5c44` | `ed018f18885f493c51a38239bad2d41557a12df85b89fc95196e527d8a9c30c4` | `9c237b73e8a6275ce4f6329d0938854c45cd9d8b0bbf2e8fd8bab0891fdd4a76` | `6377e357c7e48fa0df1b23dd6ff4564fd9a85a303ef2f51577b15b714767333e` |
| board r1 ON | `25e745a26528ef5de7d70b565025ed87682de0e2f6dc08b4794dbb6bae6a0ebb` | `ca1d6cd46bcda7fb7b22a36f082e52cf01cfff57f9c2d30af429ce4f61a28cb4` | `892db74fe8bc5b83fcbca5983faf2eff75a7b527185ff594e202d4db349bb503` | `ed018f18885f493c51a38239bad2d41557a12df85b89fc95196e527d8a9c30c4` | `0d92e934391524daefbb0cb3f162b9f6d1dbde3a353d7b795846fe2d74392df0` | `6377e357c7e48fa0df1b23dd6ff4564fd9a85a303ef2f51577b15b714767333e` |

### One command per recovered cell

Run from the HC01 lane directory. These are replay commands, not executed launches.

```sh
cd public-source-location-withheld && /opt/bench/mise/installs/python/3.14.7/bin/python3 bench-rs.py run specs/us-syn06-off.json --only kogen-rs-hc01-off__gpt-6-luna__max__default__syn-06-migration-ticket-numbers__r1 --timeout 4800 --retries 0 --jobs 1 --no-gate --no-status-pause --cleanup
cd public-source-location-withheld && /opt/bench/mise/installs/python/3.14.7/bin/python3 bench-rs.py run specs/us-syn06-on.json --only kogen-rs-hc01-on__gpt-6-luna__max__default__syn-06-migration-ticket-numbers__r1 --timeout 4800 --retries 0 --jobs 1 --no-gate --no-status-pause --cleanup
cd public-source-location-withheld && /opt/bench/mise/installs/python/3.14.7/bin/python3 bench-rs.py run specs/us-board-off.json --only kogen-rs-hc01-off__gpt-6-luna__max__default__elx-port-board-publish-unpublish-public-boundary__r1 --timeout 4800 --retries 0 --jobs 1 --no-gate --no-status-pause --cleanup
cd public-source-location-withheld && /opt/bench/mise/installs/python/3.14.7/bin/python3 bench-rs.py run specs/us-board-on.json --only kogen-rs-hc01-on__gpt-6-luna__max__default__elx-port-board-publish-unpublish-public-boundary__r1 --timeout 4800 --retries 0 --jobs 1 --no-gate --no-status-pause --cleanup
```

## Kogen source receipt

- Source clone: `public-source-location-withheld`.
- `git status --porcelain` was empty; its empty-output SHA-256 is `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. The stricter `--untracked-files=all` form was also empty.
- `git diff --binary HEAD` was empty with the same SHA-256, so the observed working-tree dirty patch is empty.
- `git rev-parse HEAD` was `1bc242254bd9c0d793795e956b27ca0926c9875b`, matching the expected commit.
- `target/release/kogen` SHA-256 was `ec94cbcf14419a9ae46b3cf6580781b83c9522feaa6a425b130342c9679aa894`, matching the HC01 `READY.md` pin.
- `build-1bc2422.log` exists with SHA-256 `2f8ac0fb5695ffd1421fb0e11ffa854776347a666206421cfa66b4099e976e20`. It provides no pre-build status/HEAD receipt; clean-at-build is therefore **not proven**. The current clean tree and matching binary do not establish when the tree was clean.

## ENVIRONMENT gap disposition

| Existing gap | Status | Reason |
| --- | --- | --- |
| `environments[*].host.allocation` | Still partial | The capture has visible CPU counts but no root cgroup quota; the recovered per-cell records do not establish the quota at capture time. |
| Host continuity over complete cell intervals | Still partial | One point-in-time host receipt cannot establish host state/load over each full interval; active/future cells were not inspected. |
| Effective model and effort per role | Still partial | Attempt configs contain configured harness/recipe metadata, not per-request effective role/model/effort; request contents were not inspected. |
| `client.dirty_patch_sha256` | Still partial | Current tree is clean and pinned, but the build log has no contemporaneous clean-tree receipt, and not every cell interval has a source-state receipt. |
| Network policy and mount/tool inventory hashes | Still partial for the round; recovered for four completed attempts | Exact per-cell values are recorded above and in JSON. The active attempt and remaining cells were excluded or had no attempt config yet. |
| Immutable grader engine and suite manifest hashes | Unresolved | Permitted lane evidence identifies the route wrapper but not the immutable engine or public suite-manifest digest. No sealed grader material was read. |
| Reasoning-in-output and cache-write semantics | Still partial | Collector/parser code records separate counters but does not establish provider-side inclusion semantics. |
| Interrupted/missing usage | Still partial | The current parser maps absent usage values to zero; no historical receipt changes that behavior. |
| Filesystem cache policy | Still partial | Mount inventories show the per-cell binds, but do not prove cross-arm dependency-cache warmth, writability, or continuity for all cells. |

### Proposed replacement `gaps:` YAML for `ENVIRONMENT.md`

```yaml
gaps:
- field: environments[*].host.allocation
  reason: The host receipt records visible physical/logical cores but no root cgroup CPU quota; recovered attempt configs do not establish the quota at capture time.
  recoverability: partial
  evidence: host-us-20261008T0551Z.json SHA-256 listed in evidence.local_files
- field: environments[*].host continuity over complete cell intervals
  reason: The point-in-time host receipt does not establish host state/load throughout complete cell intervals; the active and not-yet-started cells were not inspected.
  recoverability: partial
  evidence: host receipt plus recovered per-cell attempt/sandbox receipts in levers/hc01-lane/kit-recovery.json
- field: recipe.roles[*].effective_model and effective_effort
  reason: Configured recipe pins are known, but allowed attempt configs do not establish per-request effective role/model/effort; request contents were not inspected.
  recoverability: partial
  evidence: RECIPE.json SHA-256 and per-cell attempt config hashes in levers/hc01-lane/kit-recovery.json
- field: client.dirty_patch_sha256
  reason: The source clone is currently clean at the pinned HEAD and its binary matches READY.md, but the build log has no pre-build status/HEAD receipt and does not prove a clean build.
  recoverability: partial
  evidence: levers/hc01-lane/kit-recovery.json source_receipt; READY.md; build-1bc2422.log SHA-256 2f8ac0fb5695ffd1421fb0e11ffa854776347a666206421cfa66b4099e976e20
- field: sandbox.network_policy_sha256 and mount_tool_inventory_sha256
  reason: Per-cell canonical hashes are recovered for four completed attempts; the active cell was excluded and remaining attempts were not available at collection time.
  recoverability: partial
  evidence: per-cell hashes and canonical inventories in levers/hc01-lane/kit-recovery.json
- field: grader immutable engine hash and task suite manifest hash
  reason: The permitted evidence identifies the route wrapper but not the immutable grader engine or public suite-manifest digest.
  recoverability: unresolved
  evidence: grade_cell.sh route-wrapper SHA-256; no permitted engine/suite digest receipt
- field: accounting.reasoning_in_output and exact cache-write semantics
  reason: The code stores reasoning and cache_write separately but does not establish provider-side inclusion semantics.
  recoverability: partial
  evidence: run_r74recipe_r5.py and run_kogen_rs_cell.py SHA-256 citations in ENVIRONMENT.md
- field: accounting.interrupted_or_missing_usage
  reason: The current parser converts absent usage fields to zero rather than preserving null/unknown.
  recoverability: partial
  evidence: run_r74recipe_r5.py lines 83-107 and run_kogen_rs_cell.py lines 445-461, with SHA-256 citations in ENVIRONMENT.md
- field: accounting.filesystem_cache_policy
  reason: Per-cell bind inventories are recovered for four attempts, but they do not establish dependency-cache state/writability across arms or all cell intervals.
  recoverability: partial
  evidence: levers/hc01-lane/kit-recovery.json mount inventories and per-cell attempt config hashes
```
