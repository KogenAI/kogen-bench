# Offline dependency sources

The packages in `vendor/` are unmodified copies of the pinned public Gleam 1.18.1 toolchain cache at `the pinned public Gleam dependency cache` on us. `gleam_stdlib` is version 1.0.5; `gleeunit` is version 1.11.0. Both include their upstream Apache-2.0 licences. The root manifest resolves both as local path dependencies, including gleeunit's stdlib dependency. Dependency development dependencies are not used.

`vendor-sha256.json` inventories every vendored source, include and licence file. No downloads, registry access, precompiled application code or task solution are needed by the starter. The toolchain's Erlang/OTP 29 standard library provides JSON and OS facilities; using Erlang FFI is permitted by the task brief.
