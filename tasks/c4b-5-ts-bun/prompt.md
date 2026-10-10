# Segmented key-value store

Implement a durable, offline log-structured key-value store in process in the selected language. `make build` creates `./bin/app`; `make check` and `make test` work offline. Keep record encoding, replay/index construction, storage publication, and compaction in separate modules. No external services or subprocess storage engines.

## CLI

```
./bin/app COMMAND --root DIR [FLAGS]
init    --limit N
put     --key KEY --value HEX
delete  --key KEY
get     --key KEY
scan
verify
compact
```

Command first, then separate flag/value pairs in any order. Only the flags shown plus required `--root` are accepted. Reject missing, extra, duplicate or unknown flags/commands and positional arguments before touching storage. Values beginning with `--` are still values. All arguments must be valid UTF-8. DIR is nonempty. KEY matches `[A-Za-z0-9_-]{1,64}`, case sensitive. HEX is an even-length string of 0..8192 lowercase hex digits (empty means a zero-byte value). N is canonical decimal without leading zeros, 64..65536. Invalid arguments are USAGE.

Success exits 0 with exactly one LF-terminated single-line JSON object on stdout and empty stderr. Failure has empty stdout, exactly one LF-terminated single-line JSON object on stderr, and the exit code below. No debug output. JSON whitespace and object key order are immaterial; exact key sets, types and array ordering matter. Integers use integer syntax; no timestamps.

| Error code | Exit | Meaning |
| --- | --- | --- |
| USAGE | 2 | invalid CLI |
| NOT_INITIALIZED | 3 | MANIFEST absent, except init |
| CONFIG | 4 | init on a valid store with a different limit |
| CORRUPT | 5 | invalid authoritative bytes as defined below |
| IO_ERROR | 6 | other OS/storage failures |

Error shape is exactly `{"error":{"code":"CODE","message":"TEXT"}}`, where TEXT is a nonempty string; wording is free. A storage error precedes logical results, including a get for an absent key and an init limit mismatch. Validate the entire authoritative store on every invocation. No repair on CORRUPT.

## Results and sequencing

`init` creates a store or validates an existing one and returns `{"limit":N}`. Same-limit init is idempotent. `put` and `delete` each append one record and return `{"seq":S}`. Delete of an absent key still appends a tombstone. S is one greater than the maximum of MANIFEST.floor and all complete referenced record sequence numbers; starts at 1. Successful writes are durable before response. Failed argument validation consumes no sequence. Sequence numbers and segment IDs are limited to 1..9007199254740991; exhaustion is IO_ERROR.

`get` returns exactly `{"key":"KEY","found":true,"value":"HEX","seq":S}` for the latest put, or `{"key":"KEY","found":false,"value":null,"seq":null}` for an absent/deleted key. `scan` returns `{"items":[{"key":"KEY","value":"HEX","seq":S},...]}` with only live keys, sorted by ASCII bytes. `verify` returns `{"valid":true,"seq":S,"records":R,"segments":C}`: S is the current high water mark (0 initially), R counts complete referenced physical records including overwritten values and tombstones, C is the manifest segment count. Build the index anew on open; no persistent index is authoritative.

## Authoritative disk format

All application-created entries are below DIR. Linux, local ordinary filesystem, no malicious symlinks, no external mutations during an invocation except the documented hook release files. The whole store is at most 16 MiB. No network. All unsigned integers below are little endian. CRC is IEEE CRC-32 (reflected polynomial 0xedb88320, initial 0xffffffff, final xor 0xffffffff), covering all preceding bytes of the object, excluding the trailing checksum.

`DIR/MANIFEST` is binary: 4 bytes ASCII `KVM1`, u32 limit, u64 floor, u64 next, u32 count, count u64 segment IDs in replay order, then u32 CRC. No extra bytes. Limit has the CLI range; floor is 0..9007199254740991; next and IDs have the positive range above; count >=1; IDs are distinct and each <next. IDs need not be numerically sorted. The final ID is the sole appendable active segment; the others are sealed. The initial manifest has limit N, floor 0, next 2, IDs [1]. Segment filenames are `seg-ID.log` using canonical decimal ID.

Each segment is the concatenation of records, without a file header. Each record: 4 bytes `KV1\0`, u8 kind (1 put, 2 delete), u64 seq, u32 key length, u32 value length, raw ASCII key, raw value bytes, u32 CRC. Thus total size is 25 + key length + value length. Key and value have the CLI constraints after decoding; kind 2 requires value length 0. Seq is in the positive range above and strictly increases across complete records in manifest replay order, with gaps allowed. Floor is a high water mark retained when compaction discards records; it is not a lower bound on stored record seq.

Unreferenced segment files and temporary files are ignored, even if malformed. Missing referenced segments are CORRUPT. Invalid manifest length/magic/ranges/IDs/checksum, invalid complete record magic/kind/seq/length/key/checksum, nonincreasing record seq, or ANY incomplete record in a sealed segment is CORRUPT. Never salvage complete bad records.

The active segment alone may end with one incomplete record. At an offset with 1..20 remaining bytes, treat all those bytes as an incomplete header without validating them. With at least 21 bytes, validate header magic/kind/seq/ranges/lengths (including seq order) first; an invalid header is CORRUPT even when its claimed payload is incomplete. A valid header whose entire record does not fit is an incomplete tail. Ignore an incomplete tail in read results. Before appending OR sealing the active segment, truncate that tail at its starting offset and fsync the file. Reads (get/scan/verify and same-limit init) do not truncate it. No bytes of complete records may change during ordinary writes.

## Rotation and durability

Before each append, if the active segment's complete byte length is nonzero AND adding the record would exceed limit, rotate to a fresh empty segment. Equality does not rotate; an oversized single record is allowed in an empty segment. Allocate ID = next, increment next, and append the ID to the manifest. Fsync the empty segment and DIR before publishing the manifest. Then append to the new active segment. Existing sealed segments are immutable except removal after compaction.

Every manifest change uses a temporary file below DIR: write the complete binary manifest, fsync it, atomic rename over MANIFEST, then fsync DIR. Fsync segment data before a manifest may reference it. SIGKILL at any step must leave a recoverable store. An unacknowledged append may be absent or present, but never affect earlier writes. A killed compaction must preserve all writes and deletes. Power loss and failing fsync/full disk are outside recovery tests; map OS failures to IO_ERROR.

## Concurrent compaction

Use stable regular files `.lock` and `.compact.lock`, never unlink or replace them. Use Linux `flock(2)` (not fcntl record locks), retry EINTR. Readers hold shared `.lock` across replay and response construction; init/writers hold exclusive `.lock` across replay, tail recovery, rotation, append and fsync. All compactors hold exclusive `.compact.lock` for their whole invocation; acquire it before `.lock`. These locks are released by process exit/SIGKILL. Bases include small native flock helpers.

Compaction has three phases:

1. Under exclusive `.lock`, replay and recover the active tail. Capture ALL currently referenced segments, their latest records per key, and cutoff = current high water mark. Reserve output ID = next; create a fresh active ID = next+1 and advance next by 2. Publish a manifest retaining the captured prefix plus this new active segment. Release `.lock`.
2. Outside `.lock`, write a single sealed output segment containing exactly the latest captured PUT for each live captured key, in increasing original seq order, retaining original seq and bytes. Drop all captured tombstones and obsolete puts. An empty output segment is required when no live captured keys remain. Fsync the output and DIR. Reads and writers must complete while this phase is paused at either hook below. Writers may rotate repeatedly during this phase.
3. Under exclusive `.lock`, reload and validate the CURRENT manifest/store; replace only the captured prefix with the output ID, retaining ALL newer suffix segments in their current order. Set floor = max(current floor, cutoff), retain current next and limit, and durably publish. Release `.lock`; remove all captured segment files and fsync DIR. Return `{"cutoff":S,"kept":K}` where S and K describe the captured snapshot, regardless of concurrent writes. Do not merge newer writes into output or reset their sequence allocation.

A subsequent reader may see either publication, but must see a coherent logical state. Never lose a newer update or resurrect a key deleted in the suffix. Removing captured tombstones is safe only because the complete captured prefix is replaced atomically. Compaction still runs these phases for an empty or already compacted store. Unreferenced crash artifacts may remain; successful compaction must remove its captured files. Serialize competing compactors without blocking ordinary work during phase 2.

## Deterministic SIGKILL/pause hooks

Optional `--hook STAGE` is allowed only on init, put, delete, compact, with stage appropriate to the command. It pauses at the indicated point by writing the ASCII bytes `ready\n` to `DIR/hook-STAGE.ready`, then waiting for `DIR/hook-STAGE.go` to exist (poll interval <=50 ms). Do not emit a response until released. Hook control files are ignored by storage replay and may remain. Tests use fresh marker names by removing old markers before each hooked invocation. The ready marker must be visible only after the stated step completes. SIGKILL is sent by the caller; the app must not implement hooks by exiting voluntarily.

| Stage | Commands | Point |
| --- | --- | --- |
| init-data | init of absent manifest | segment 1 and DIR fsynced, before manifest publication |
| init-publish | init of absent manifest | manifest and DIR durably published |
| rotate-data | put/delete requiring rotation | new empty segment and DIR fsynced, before manifest publication |
| rotate-publish | put/delete requiring rotation | rotated manifest and DIR durably published, before any append bytes |
| append-half | put/delete | first floor(record_size/2) bytes appended and fsynced, before remaining bytes |
| append-sync | put/delete | whole record appended and fsynced, before response |
| compact-snapshot | compact | phase 1 publication done and `.lock` released, before output creation |
| compact-data | compact | phase 2 data and DIR fsynced, `.lock` still released |
| compact-publish | compact | phase 3 manifest and DIR fsynced, `.lock` released, before deletions |
| compact-cleanup | compact | captured files removed and DIR fsynced, before response |

A valid hook whose stage is not reached simply does not pause (e.g. rotation without threshold crossing, or init on an existing store). Hooks may hold `.lock` at init/rotate/append stages; compact hooks never hold `.lock`. No additional flags, commands, caching, asynchronous daemon, or timing guarantee beyond the explicit hook concurrency is required.

Stack and checks: TypeScript/Bun. Build: `make build`; test: `make test`.
Checks: `make check` runs tsc --noEmit (strict), biome check ., bun test.
