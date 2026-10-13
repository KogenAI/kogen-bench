# Harness package

cmp.py, fx.c and test_cmp.py provide a public, inspectable mirror of the CMP-SMALL apparatus. The exact deployed source hashes are recorded in DEPLOYED-SOURCE-HASHES.txt. The measured apparatus digest is recorded in the round README and results.json.

The mirror omits literal machine-local account-home paths by resolving the two account homes at runtime. The loopback endpoint uses the localhost name rather than a numeric address. The fixture source renames a variable that held the test value read from the environment; no value is embedded in the public source. These are privacy edits. The mirror is not byte-identical to the measured source, and its local checks are not presented as a replay of the measurement.

The compiled Linux fixture, pinned vendor executable and private per-cell JSON bodies are not bundled. Their source hashes and the pulled matrix are documented in the round files. The apparatus hash also binds host tools and the built fixture; it is not a hash of the kernel, systemd daemon or every dynamic library.
