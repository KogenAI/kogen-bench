# Linux REAL-WORKFLOW egress window

EU and US used REAL-WORKFLOW with bench-user allow-all egress, ecosystem downloads, internet documentation and live Codex web search. The launch preparation report records that allow-all policy was already active during the prelaunch dry cells; its exact opening timestamp is not established here. The production waves ran A 2026-10-10 19:35–22:35Z and B 23:10Z–2026-10-11 02:10Z.

During this window, `/etc/hosts` sinkholed `kogen.dev`, `www.kogen.dev` and `bench.kogen.dev` to unspecified IPv4 and IPv6 addresses. Git URL rewrites redirected Kogen repositories to an invalid destination. These controls and the voiding event audit are not a general firewall or packet capture; a hosts sinkhole is not NXDOMAIN. Agent-issued real model-provider calls remained forbidden. The Codex model transport remained permitted. Scoring used a private offline bwrap network namespace.

After the Linux waves finished, around 2026-10-11 02:20Z, Linux bench egress was restored to provider-only mode and the hosts sinkhole was removed. The incident log calls the restored policy SEALED; execution MODE during the race was real-workflow. The report does not independently establish the exact transition second or hidden traffic.

Evidence: the retained Linux launch-preparation report (allow-all and sinkhole), `LAUNCH-REPORT.md` (production epochs and offline scoring), the frozen rule MODE section, and [INCIDENTS.md](INCIDENTS.md) (restoration). Original document hashes are recorded in PROVENANCE.tsv. Linux is reported only and does not enter PRIMARY or REPAIRED.
