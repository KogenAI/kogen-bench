# Runner and warm-up locale audit

Every site below sets both `LANG=en_US.UTF-8` and `LC_ALL=en_US.UTF-8`.

| File and site | Scope |
| --- | --- |
| process_control.py: implementation_environment (line 23) | Common inherited Kogen/toolchain environment; sets both variables rather than inheriting host locale |
| process_control.py: run_process (line 89) | Final synchronous launch guard, including JSON commands/status observations, Gherkin commands and binary version probes; overrides case/step locale |
| runner.py: CaseWorld._base_env (lines 326–327) | Every legacy JSON case environment |
| runner.py: CaseWorld._enforce_sandbox_env (line 364) | Restores both variables after case and step overrides |
| quint_runner.py: _binary_metadata (line 742) | Actual Kogen `version` invocation used to collect metadata |
| quint_runner.py: _run_quint (line 770) | Quint generator helper, which does not itself launch Kogen; also changed to the same locale |
| quint_runner.py: CaptureProcess.start (line 1513) | Final foreground/background capture launch guard used by Quint and Gherkin; overrides supplied locale |
| quint_runner.py: TraceWorld._start_openid (line 1881) | Python OpenID fixture server, which does not launch Kogen; also changed to the same locale |
| quint_runner.py: TraceWorld._base_env (line 1908) | All Quint command environments |
| quint_runner.py: TraceWorld._environment (line 2103) | Restores both variables after SetEnv/UnsetEnv overrides |
| gherkin_runner.py: GherkinWorld._base_env (line 358) | All foreground and background Gherkin Kogen invocations |
| score-arm.sh (line 4) | Scorer shell environment, forced after env.sh and the per-arm .kit-env.sh |
| score-arm.sh: warmup_env/Popen (lines 57–58) | Explicit environment for the `./kogen version` warm-up |
| env.sh and env-studio.sh (line 5 in each) | Both hosts' harness baseline environment; already used the required locale |

The remaining `LC_ALL=C` sites are only ps probes in quint_runner.py (lines 1677 and 1691), and lsof/ps cleanup probes in process_control.py (lines 164 and 235). They never launch Kogen.

Seven offline regression tests in conformance/tests/test_race3_contract.py exercise the request boundary, case/step locale override resistance, synchronous/background UTF-8 launches, Gherkin fixtures and actual binary-version environment. The scoring integration test checks both locale variables in its stand-in executable, covering the warm-up and kg-wrap execution path.
