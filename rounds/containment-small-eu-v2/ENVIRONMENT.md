# Environment and configured setups

The retained run used one Linux test server and one kernel. The available evidence does not establish a general hardware inventory or baseline total memory allocation. No language model ran.

- No sandbox: no filesystem or network sandbox. A systemd scope held descendant custody; this setup had no memory or process-count cap mechanism.
- Bubblewrap setup: bubblewrap inside a systemd scope.
- nono setup: nono 0.79.0 inside a systemd scope.

The Bubblewrap and nono setup outcomes describe these complete command paths, including systemd limits. Both candidates used systemd memory and process-count limits. The environment-secret outcome tests the launcher environment allowlist.

The permitted folder was the work area created for each fixture. Positive controls checked the expected allowed read/write behavior. Network testing tried one IPv4 TCP connection to loopback and did not test any allowed network path.
