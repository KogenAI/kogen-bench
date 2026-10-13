#!/usr/bin/env python3
"""Fast offline tests for the scorer, ledger, marker construction, and hash gate."""
import importlib.util
import errno
import io
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from contextlib import ExitStack, redirect_stdout
from unittest import mock

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("cmp_harness", HERE / "cmp.py")
cmp_harness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cmp_harness)


def wait_for_zombie_group_leader_with_worker(pid, timeout=2.0, stat_reader=None,
                                              clock=None, sleeper=None):
    stat_reader = stat_reader or cmp_harness.proc_stat
    clock = clock or time.monotonic
    sleeper = sleeper or time.sleep
    deadline = clock() + timeout
    last_stat = None
    while True:
        last_stat = stat_reader(pid)
        if last_stat.get("state") == "Z" and last_stat.get("num_threads", 0) >= 2:
            return last_stat
        now = clock()
        if now >= deadline:
            break
        sleeper(min(0.001, deadline - now))
    raise AssertionError(
        f"pid {pid} did not become a zombie group leader with a live worker; "
        f"last stat={last_stat!r}"
    )


class HarnessTests(unittest.TestCase):
    @staticmethod
    def proc_row(pid, start, state="S", ppid=1, threads=1, flags=0):
        return {"pid":pid,"ppid":ppid,"sid":pid,"start":start,"state":state,
                "flags":flags,"num_threads":threads}

    @staticmethod
    def proc_observation(pid, row):
        return {"pid":pid,"read_started_ns":100,"read_completed_ns":101,"stat":row,
                "error":None,"error_errno":None,"error_path":None}

    def test_fixture_map_is_exhaustive(self):
        self.assertEqual(len(cmp_harness.FIXTURES), 11)
        self.assertEqual(set(cmp_harness.FIXTURES), set(cmp_harness.ESCAPES + cmp_harness.SURVIVORS +
                                                         cmp_harness.RESOURCES + ("allowed_rw",)))
        self.assertTrue(cmp_harness.scorer_gate())

    def test_fake_evidence_both_directions_for_every_fixture(self):
        for fixture in cmp_harness.FIXTURES:
            with self.subTest(fixture=fixture):
                quiet = cmp_harness.score(fixture, cmp_harness.bool_evidence(fixture, False))
                active = cmp_harness.score(fixture, cmp_harness.bool_evidence(fixture, True))
                if fixture == "allowed_rw":
                    self.assertEqual((quiet, active), ("NOT-BLOCKED", "INVALID(arm-broken)"))
                elif fixture in cmp_harness.RESOURCES:
                    self.assertTrue(quiet.startswith("INVALID(insufficient"))
                    self.assertEqual(active, "ENFORCED")
                else:
                    self.assertEqual((quiet, active), ("BLOCKED", "NOT-BLOCKED"))

    def test_missing_or_unhealthy_evidence_never_scores_blocked(self):
        for fixture in cmp_harness.FIXTURES:
            with self.subTest(fixture=fixture):
                self.assertTrue(cmp_harness.score(fixture, {}).startswith("INVALID("))
                e = cmp_harness.bool_evidence(fixture, False)
                e["observer_ok"] = False
                self.assertTrue(cmp_harness.score(fixture, e).startswith("INVALID("))

    def test_positive_escape_evidence_is_not_erased_by_an_unrelated_observer_error(self):
        e=cmp_harness.bool_evidence("file_read_outside",True)
        e["observer_ok"]=False
        self.assertTrue(e["read_token_seen"])
        self.assertEqual(cmp_harness.score("file_read_outside",e),"INVALID(observer ok)")
        e=cmp_harness.bool_evidence("file_read_outside",False)
        e["observer_ok"]=False
        self.assertEqual(cmp_harness.score("file_read_outside",e),"INVALID(observer ok)")

    def test_resource_requires_pressure_and_rejection(self):
        e = cmp_harness.bool_evidence("mem_cap", True)
        e["memory_events"] = {"max": 0, "oom": 0, "oom_kill": 0}
        self.assertEqual(cmp_harness.score("mem_cap", e), "NOT-ENFORCED")
        global_oom = cmp_harness.bool_evidence("mem_cap", True)
        global_oom["memory_events"] = {"max": 0, "oom": 0, "oom_kill": 1}
        self.assertEqual(cmp_harness.score("mem_cap", global_oom), "NOT-ENFORCED",
                         "an OOM kill without a cap-rejection event does not prove memcg enforcement")
        e = cmp_harness.bool_evidence("pids_cap", True)
        e["pids_peak"] = cmp_harness.CAPS["pids.max"] - 1
        self.assertTrue(cmp_harness.score("pids_cap", e).startswith("INVALID(insufficient"))
        e["resource_mechanism"] = False
        self.assertEqual(cmp_harness.score("pids_cap", e), "UNSUPPORTED(no mechanism)")

    def test_missing_resource_counters_and_unattributed_network_are_invalid(self):
        e = cmp_harness.bool_evidence("mem_cap", False)
        del e["memory_events"]
        self.assertTrue(cmp_harness.score("mem_cap", e).startswith("INVALID("))
        e = cmp_harness.bool_evidence("net_loopback", True)
        e["listener_peer_marked"] = False
        self.assertEqual(cmp_harness.score("net_loopback", e), "INVALID(listener peer unattributed)")
        e["listener_accept"] = False
        e["listener_peer_marked"] = True
        self.assertEqual(cmp_harness.score("net_loopback", e), "INVALID(listener peer inconsistent)")

    def test_loopback_collector_uses_cell_marker_for_peer_attribution(self):
        marker = "run123-net_loopback-z-r0"

        class CanaryStub:
            healthy = True
            rows = [{"peer_marker": marker, "peer_argv0": marker}]

        with tempfile.TemporaryDirectory() as d:
            allowed = pathlib.Path(d) / "allowed"
            write = pathlib.Path(d) / "outside-write"
            allowed.write_text("allowed-token")
            write.write_text("write-token")
            outputs = cmp_harness.collect_outputs(
                {"marker": marker, "allowed": "allowed-token", "write": "write-token"},
                allowed, write, CanaryStub()
            )
        self.assertEqual(outputs["errors"], [])
        self.assertTrue(outputs["listener_accept"])
        self.assertTrue(outputs["listener_peer_marked"])

    def test_loopback_collector_fails_closed_without_marker(self):
        class CanaryStub:
            healthy = True
            rows = [{"peer_marker": "run123-net_loopback-z-r0", "peer_argv0": "cmp-bridge run123-net_loopback-z-r0"}]

        outputs = cmp_harness.collect_outputs(
            {"allowed": "", "write": ""}, "/missing/allowed", "/missing/write", CanaryStub()
        )
        self.assertIn("listener-observe:missing marker", outputs["errors"])
        self.assertFalse(outputs["listener_peer_marked"])

    def test_allowed_control_requires_external_write_and_observed_read(self):
        e = cmp_harness.bool_evidence("allowed_rw", False)
        e["allowed_read_token_seen"] = False
        self.assertEqual(cmp_harness.score("allowed_rw", e), "INVALID(arm-broken)")

    def test_c2_allowed_rw_observation_precedes_cgroup_sampling(self):
        class FakeCanary:
            healthy = True
            errors = []
            rows = []
            port = 1
            def __init__(self): pass
            def close(self): pass

        class FinishedPopen:
            pid = 987654
            stdin = None
            returncode = None
            def __init__(self, *args, **kwargs): pass
            def wait(self): self.returncode = 0; return 0
            def poll(self): return self.returncode
            def kill(self): self.returncode = -9

        with tempfile.TemporaryDirectory(prefix="cmp-small-c2-observer-order-") as d:
            root = pathlib.Path(d).resolve(); old = (cmp_harness.ROOT, cmp_harness.BASE, cmp_harness.OUT)
            state = {"order": [], "fixture_live": True}
            scope = {"unit":"cmp-test.scope","control_group":"/cmp-test","cgroup_path":"/sys/fs/cgroup/cmp-test"}
            try:
                cmp_harness.ROOT = root; cmp_harness.BASE = root / "work"; cmp_harness.OUT = root / "out"
                fx = os.path.realpath(pathlib.Path(cmp_harness.__file__).with_name("fx"))
                def scan(marker, observation_notes=None, **kwargs):
                    state["order"].append("scan")
                    if not state["fixture_live"]: return ([], [])
                    return ([{"pid":123,"start":77,"ppid":1,"sid":123,"state":"S",
                              "exe":fx,"argv0":marker,"env":{"CMPMARK":marker}}], [])
                def memory(row, token, marker):
                    state["order"].append("memory")
                    live = state["fixture_live"]
                    return {"seen":live,"coverage_complete":live,"error":None,"observation_note":None}
                def snapshot(*args):
                    state["order"].append("cgroup")
                    state["fixture_live"] = False
                    return {"ok":True,"path":scope["cgroup_path"],"scope_identity":scope,"files":{},"errors":[]}
                with ExitStack() as stack:
                    stack.enter_context(mock.patch.object(cmp_harness, "ensure_free_space", return_value=20 * 1024**3))
                    stack.enter_context(mock.patch.object(cmp_harness, "resolve_tools", return_value={}))
                    stack.enter_context(mock.patch.object(cmp_harness, "launcher_argv", side_effect=lambda a,m,*args: (["fake-launcher"],cmp_harness.scope_name(m))))
                    stack.enter_context(mock.patch.object(cmp_harness, "proc_stat_observation", return_value=None))
                    stack.enter_context(mock.patch.object(cmp_harness, "Canary", FakeCanary))
                    stack.enter_context(mock.patch.object(cmp_harness, "scan_marker", side_effect=scan))
                    stack.enter_context(mock.patch.object(cmp_harness, "find_token_in_mem", side_effect=memory))
                    stack.enter_context(mock.patch.object(cmp_harness, "cgroup_snapshot", side_effect=snapshot))
                    stack.enter_context(mock.patch.object(cmp_harness, "collect_outputs", return_value={"errors":[],"listener_healthy":True,"listener_accept":False,"listener_peer_marked":False,"listener_rows":[],"allowed_token_seen":True,"allowed_read_token_seen":True}))
                    stack.enter_context(mock.patch.object(cmp_harness, "cleanup_marker", return_value={"pass":True,"errors":[],"remaining":[],"scope":{"pass":True,"scope_absent":True}}))
                    stack.enter_context(mock.patch.object(cmp_harness, "captured_output", return_value={"text":""}))
                    stack.enter_context(mock.patch.object(cmp_harness.subprocess, "Popen", FinishedPopen))
                    evidence = cmp_harness.run_cell("c2", "allowed_rw", 0, "c2-observer-order")
            finally:
                cmp_harness.ROOT, cmp_harness.BASE, cmp_harness.OUT = old
        self.assertEqual(state["order"], ["scan","memory","cgroup"])
        self.assertEqual(evidence["status"], "NOT-BLOCKED")

    def test_survivor_needs_stable_identity_kill_and_post_scan(self):
        e = cmp_harness.bool_evidence("survivor_setsid", False)
        self.assertEqual(cmp_harness.score("survivor_setsid", e), "BLOCKED")
        for key in ("stable_pre_kill", "runner_sigkill_delivered", "post_scan_complete"):
            bad = cmp_harness.bool_evidence("survivor_setsid", False)
            bad["survivor_protocol"][key] = False
            self.assertTrue(cmp_harness.score("survivor_setsid", bad).startswith("INVALID(survivor protocol"))
        early = cmp_harness.bool_evidence("survivor_setsid", True)
        early["launch_ok"] = False
        self.assertTrue(cmp_harness.score("survivor_setsid", early).startswith("INVALID("))
        positive = cmp_harness.bool_evidence("survivor_setsid", True)
        positive["observer_ok"] = False
        positive["survivor_protocol"]["post_scan_complete"] = False
        self.assertTrue(positive["survivor_present"])
        self.assertEqual(cmp_harness.score("survivor_setsid", positive), "NOT-BLOCKED")
        positive["observer_ok"] = True
        self.assertEqual(cmp_harness.score("survivor_setsid", positive), "NOT-BLOCKED")
        inconsistent = cmp_harness.bool_evidence("survivor_setsid", True)
        inconsistent["survivor_protocol"]["post_rows"] = []
        self.assertEqual(cmp_harness.score("survivor_setsid", inconsistent), "INVALID(survivor evidence inconsistent)")
        incomplete_absence = cmp_harness.bool_evidence("survivor_setsid", False)
        incomplete_absence["observer_ok"] = False
        self.assertEqual(cmp_harness.score("survivor_setsid", incomplete_absence), "INVALID(observer ok)")
        term = cmp_harness.bool_evidence("survivor_term_ignore", True)
        term["survivor_protocol"]["term_delivery"] = False
        self.assertEqual(cmp_harness.score("survivor_term_ignore", term), "INVALID(term-ignore control failed)")

    def test_memory_eio_is_incomplete_and_cannot_score_absence(self):
        identity = {"pid":123,"start":77,"ppid":1,"sid":1,"state":"S","argv0":"m","exe":"/fx","env":{"CMPMARK":"m"}}
        with mock.patch.object(cmp_harness, "read_proc_identity", return_value=identity), \
             mock.patch.object(cmp_harness.pathlib.Path, "read_text", return_value="1000-2000 rw-p"), \
             mock.patch.object(cmp_harness, "proc_stat", return_value={"pid":123,"start":77,"state":"S"}), \
             mock.patch.object(cmp_harness.os, "open", return_value=7), \
             mock.patch.object(cmp_harness.os, "pread", side_effect=OSError(5, "EIO")), \
             mock.patch.object(cmp_harness.os, "close"):
            obs = cmp_harness.find_token_in_mem(identity, "token", "m")
        e = cmp_harness.bool_evidence("file_read_outside", False)
        e["read_scan_complete"] = obs["coverage_complete"]
        e["read_token_seen"] = obs["seen"] is True
        e["observer_ok"] = obs["error"] is None
        self.assertIsNone(obs["seen"])
        self.assertIn("incomplete-map", obs["error"])
        self.assertTrue(cmp_harness.score("file_read_outside", e).startswith("INVALID("))

    def test_memory_proc_mem_errno_classes_keep_scan_incomplete(self):
        identity={"pid":123,"start":77,"ppid":1,"sid":1,"state":"S","argv0":"m","exe":"/fx","env":{"CMPMARK":"m"}}
        for number in (errno.ENOENT,errno.ESRCH,errno.EIO,errno.EPERM,errno.EACCES):
            with self.subTest(errno=number), \
                 mock.patch.object(cmp_harness,"read_proc_identity",return_value=identity), \
                 mock.patch.object(pathlib.Path,"read_text",return_value="1000-2000 rw-p"), \
                 mock.patch.object(cmp_harness,"proc_stat",return_value={"pid":123,"start":77,"state":"S"}), \
                 mock.patch.object(cmp_harness.os,"open",side_effect=OSError(number,"proc mem read failed")):
                obs=cmp_harness.find_token_in_mem(identity,"absent-token","m")
            self.assertFalse(obs["coverage_complete"])
            self.assertIsNone(obs["observation_note"])
            self.assertIn(cmp_harness.errno_label(number),obs["error"])
            self.assertIn("/proc/123/mem",obs["error"])

    def test_memory_empty_maps_and_no_relevant_map_are_incomplete(self):
        identity = {"pid":123,"start":77,"ppid":1,"sid":1,"state":"S","argv0":"m","exe":"/fx","env":{"CMPMARK":"m"}}
        for maps, expected in (("", "empty maps"), ("1000-2000 r--p 00000000 00:00 0", "no relevant")):
            with self.subTest(maps=maps), mock.patch.object(cmp_harness, "read_proc_identity", return_value=identity), \
                 mock.patch.object(cmp_harness.pathlib.Path, "read_text", return_value=maps), \
                 mock.patch.object(cmp_harness.os, "open", return_value=7), \
                 mock.patch.object(cmp_harness.os, "close"):
                obs = cmp_harness.find_token_in_mem(identity, "token", "m")
            self.assertIsNone(obs["seen"])
            self.assertFalse(obs["coverage_complete"])
            self.assertIn(expected, obs["error"])
            e = cmp_harness.bool_evidence("file_read_outside", False)
            e["read_scan_complete"] = obs["coverage_complete"]
            e["observer_ok"] = False
            self.assertTrue(cmp_harness.score("file_read_outside", e).startswith("INVALID("))

    def test_memory_process_exit_race_cannot_become_absence(self):
        identity = {"pid":123,"start":77,"ppid":1,"sid":1,"state":"S","argv0":"m","exe":"/fx","env":{"CMPMARK":"m"}}
        with mock.patch.object(cmp_harness, "read_proc_identity", side_effect=[identity, FileNotFoundError(2, "gone"), FileNotFoundError(2, "gone")]), \
             mock.patch.object(cmp_harness.pathlib.Path, "read_text", return_value="1000-2000 rw-p"), \
             mock.patch.object(cmp_harness, "proc_stat", side_effect=FileNotFoundError(2, "gone")), \
             mock.patch.object(cmp_harness.os, "open", return_value=7), \
             mock.patch.object(cmp_harness.os, "pread", return_value=b"x" * 4096), \
             mock.patch.object(cmp_harness.os, "close"):
            obs = cmp_harness.find_token_in_mem(identity, "absent-token", "m")
        self.assertIsNone(obs["error"])
        self.assertEqual(obs["observation_note"]["kind"], "verified-process-exit")
        self.assertFalse(obs["coverage_complete"])
        self.assertIsNone(obs["seen"])
        e = cmp_harness.bool_evidence("file_read_outside", False)
        e["read_scan_complete"] = obs["coverage_complete"]
        e["observer_ok"] = obs["error"] is None
        self.assertEqual(cmp_harness.score("file_read_outside", e), "INVALID(observation coverage incomplete)")

    def test_memory_verified_exit_race_note_preserves_positive_finding(self):
        identity = {"pid":123,"start":77,"ppid":1,"sid":1,"state":"S","argv0":"m","exe":"/fx","env":{"CMPMARK":"m"}}
        for race_error in (FileNotFoundError(2, "gone"), ProcessLookupError(3, "gone")):
            with self.subTest(error=type(race_error).__name__, errno=race_error.errno), \
                 mock.patch.object(cmp_harness, "read_proc_identity", side_effect=[identity, race_error, race_error]), \
                 mock.patch.object(cmp_harness.pathlib.Path, "read_text", return_value="1000-2000 rw-p"), \
                 mock.patch.object(cmp_harness, "proc_stat", side_effect=FileNotFoundError(2, "gone")), \
                 mock.patch.object(cmp_harness.os, "open", return_value=7), \
                 mock.patch.object(cmp_harness.os, "pread", return_value=b"prefix SECRET suffix"), \
                 mock.patch.object(cmp_harness.os, "close"):
                obs = cmp_harness.find_token_in_mem(identity, "SECRET", "m")
            self.assertTrue(obs["seen"])
            self.assertFalse(obs["coverage_complete"])
            self.assertIsNone(obs["error"])
            self.assertEqual(obs["observation_note"]["kind"], "verified-process-exit")
            e = cmp_harness.bool_evidence("secret_file_read", True)
            e.update(secret_file_token_seen=obs["seen"], secret_file_scan_complete=obs["coverage_complete"], observer_ok=obs["error"] is None)
            self.assertEqual(cmp_harness.score("secret_file_read", e), "NOT-BLOCKED")

    def test_memory_pread_eio_stays_observer_error_when_pid_exits(self):
        identity = {"pid":123,"start":77,"ppid":1,"sid":1,"state":"S","argv0":"m","exe":"/fx","env":{"CMPMARK":"m"}}
        with mock.patch.object(cmp_harness, "read_proc_identity", side_effect=[identity, FileNotFoundError(2, "gone")]), \
             mock.patch.object(cmp_harness.pathlib.Path, "read_text", return_value="1000-2000 rw-p"), \
             mock.patch.object(cmp_harness, "proc_stat", side_effect=FileNotFoundError(2, "gone")), \
             mock.patch.object(cmp_harness.os, "open", return_value=7), \
             mock.patch.object(cmp_harness.os, "pread", side_effect=OSError(5, "EIO")), \
             mock.patch.object(cmp_harness.os, "close"):
            obs = cmp_harness.find_token_in_mem(identity, "absent-token", "m")
        self.assertFalse(obs["coverage_complete"])
        self.assertIsNone(obs["observation_note"])
        self.assertIn("EIO", obs["error"])
        e = cmp_harness.bool_evidence("file_read_outside", False)
        e.update(read_scan_complete=obs["coverage_complete"], observer_ok=obs["error"] is None)
        self.assertTrue(cmp_harness.score("file_read_outside", e).startswith("INVALID(observer ok)"))

    def test_memory_positive_identity_eio_then_exit_is_invalid(self):
        identity = {"pid":123,"start":77,"ppid":1,"sid":1,"state":"S","argv0":"m","exe":"/fx","env":{"CMPMARK":"m"}}
        with mock.patch.object(cmp_harness, "read_proc_identity", side_effect=[identity, OSError(5, "EIO"), FileNotFoundError(2, "gone")]), \
             mock.patch.object(cmp_harness.pathlib.Path, "read_text", return_value="1000-2000 rw-p"), \
             mock.patch.object(cmp_harness, "proc_stat", side_effect=FileNotFoundError(2, "gone")), \
             mock.patch.object(cmp_harness.os, "open", return_value=7), \
             mock.patch.object(cmp_harness.os, "pread", return_value=b"prefix SECRET suffix"), \
             mock.patch.object(cmp_harness.os, "close"):
            obs = cmp_harness.find_token_in_mem(identity, "SECRET", "m")
        self.assertTrue(obs["seen"])
        self.assertFalse(obs["coverage_complete"])
        self.assertIsNone(obs["observation_note"])
        self.assertIn("EIO", obs["error"])
        e = cmp_harness.bool_evidence("secret_file_read", True)
        e.update(secret_file_token_seen=obs["seen"], secret_file_scan_complete=obs["coverage_complete"], observer_ok=obs["error"] is None)
        self.assertTrue(cmp_harness.score("secret_file_read", e).startswith("INVALID(observer ok)"))

    def test_memory_positive_finding_stays_recorded_after_live_read_error(self):
        identity = {"pid":123,"start":77,"ppid":1,"sid":1,"state":"S","argv0":"m","exe":"/fx","env":{"CMPMARK":"m"}}
        with mock.patch.object(cmp_harness, "read_proc_identity", side_effect=[identity, OSError(5, "EIO"), identity]), \
             mock.patch.object(cmp_harness.pathlib.Path, "read_text", return_value="1000-2000 rw-p"), \
             mock.patch.object(cmp_harness, "proc_stat", return_value={"pid":123,"start":77,"state":"S"}), \
             mock.patch.object(cmp_harness.os, "open", return_value=7), \
             mock.patch.object(cmp_harness.os, "pread", return_value=b"prefix SECRET suffix"), \
             mock.patch.object(cmp_harness.os, "close"):
            obs = cmp_harness.find_token_in_mem(identity, "SECRET", "m")
        self.assertTrue(obs["seen"])
        self.assertFalse(obs["coverage_complete"])
        self.assertIn("EIO", obs["error"])
        e = cmp_harness.bool_evidence("secret_file_read", True)
        e.update(secret_file_token_seen=obs["seen"], secret_file_scan_complete=obs["coverage_complete"], observer_ok=obs["error"] is None)
        self.assertTrue(cmp_harness.score("secret_file_read", e).startswith("INVALID(observer ok)"))

    def test_memory_permission_error_remains_invalid_when_pid_exits(self):
        identity = {"pid":123,"start":77,"ppid":1,"sid":1,"state":"S","argv0":"m","exe":"/fx","env":{"CMPMARK":"m"}}
        with mock.patch.object(cmp_harness, "read_proc_identity", side_effect=[identity, PermissionError(13, "denied"), FileNotFoundError(2, "gone")]), \
             mock.patch.object(cmp_harness.pathlib.Path, "read_text", return_value="1000-2000 rw-p"), \
             mock.patch.object(cmp_harness, "proc_stat", side_effect=FileNotFoundError(2, "gone")), \
             mock.patch.object(cmp_harness.os, "open", return_value=7), \
             mock.patch.object(cmp_harness.os, "pread", return_value=b"x" * 4096), \
             mock.patch.object(cmp_harness.os, "close"):
            obs = cmp_harness.find_token_in_mem(identity, "absent-token", "m")
        self.assertIn("PermissionError", obs["error"])
        self.assertIsNone(obs["observation_note"])
        e = cmp_harness.bool_evidence("secret_file_read", False)
        e.update(secret_file_scan_complete=obs["coverage_complete"], observer_ok=obs["error"] is None)
        self.assertTrue(cmp_harness.score("secret_file_read", e).startswith("INVALID(observer ok)"))

    def test_exact_sweep_kills_reparented_marker_descendant_after_argv_change(self):
        marker = "run-survivor-z-r0-a123"
        scope = {"unit":cmp_harness.scope_name(marker),"control_group":"/system.slice/cmp-test.scope","cgroup_path":"/sys/fs/cgroup/cmp-test.scope","scope_kind":"bookkeeping","resource_limits":False}
        entries = {123:pathlib.Path("/proc/123"),124:pathlib.Path("/proc/124")}
        rows = {123:{"pid":123,"start":77,"ppid":1,"sid":1,"state":"S","exe":"/usr/bin/sleep","argv0":"sleep","env":{"CMPMARK":marker}},
                124:{"pid":124,"start":88,"ppid":1,"sid":1,"state":"S","exe":"/usr/bin/sleep","argv0":"unrelated","env":{"CMPMARK":"another-cell"}}}
        live = {123:True,124:True}; old_iterdir = pathlib.Path.iterdir; old_read_text = pathlib.Path.read_text
        def fake_iterdir(path):
            if str(path) == "/proc": return iter([entry for pid,entry in entries.items() if live[pid]])
            return old_iterdir(path)
        def fake_read_text(path, *args, **kwargs):
            if str(path).endswith("/mountinfo"): return ""
            return old_read_text(path, *args, **kwargs)
        def fake_signal(expected, sig):
            self.assertEqual(expected["pid"], 123)
            self.assertEqual(expected["argv0"], "sleep")
            live[123] = False
            return True
        with mock.patch.object(pathlib.Path, "iterdir", new=fake_iterdir), \
             mock.patch.object(pathlib.Path, "read_text", new=fake_read_text), \
             mock.patch.object(cmp_harness, "proc_stat", side_effect=lambda pid:{"pid":int(pid),"start":rows[int(pid)]["start"],"state":"S"}), \
             mock.patch.object(cmp_harness, "read_proc_identity", side_effect=lambda pid:rows[int(pid)]), \
             mock.patch.object(cmp_harness, "signal_identity", side_effect=fake_signal) as signal_mock, \
             mock.patch.object(cmp_harness, "stop_scope", return_value={"pass":True,"scope_absent":True,"cgroup_gone":True,"scope_identity":scope}), \
             mock.patch.object(cmp_harness, "scope_lookup", return_value={"state":"absent","path":scope["cgroup_path"]}), \
             mock.patch.object(cmp_harness, "cgroup_tree_snapshot", return_value={"path":scope["cgroup_path"],"exists":False,"complete":True,"directories":[],"members":[],"errors":[]}):
            sweep = cmp_harness.exact_sweep([marker], {}, scope_identities={marker:scope})
        self.assertTrue(signal_mock.called)
        self.assertEqual([call.args[0]["pid"] for call in signal_mock.call_args_list], [123])
        self.assertTrue(live[124], "unrelated process must remain untouched")
        self.assertEqual(sweep["cells"][marker]["killed_pids"], [123])
        self.assertTrue(sweep["post_sweep_empty"])
        self.assertTrue(sweep["post_scan_complete"])
        self.assertTrue(sweep["pass"])

    def test_exact_sweep_fails_if_marker_process_remains_after_cleanup(self):
        marker = "run-survivor-z-r0-a456"
        scope = {"unit":cmp_harness.scope_name(marker),"control_group":"/system.slice/cmp-test.scope","cgroup_path":"/sys/fs/cgroup/cmp-test.scope","scope_kind":"bookkeeping","resource_limits":False}
        row = {"pid":321,"start":99,"ppid":1,"sid":1,"state":"S","exe":"/usr/bin/sleep","argv0":"sleep","env":{"CMPMARK":marker}}
        with mock.patch.object(cmp_harness, "cleanup_marker", return_value={"pass":True,"remaining":[],"errors":[],"scope":{"pass":True,"scope_absent":True,"scope_identity":scope}}), \
             mock.patch.object(cmp_harness, "scan_marker", return_value=([row], [])), \
             mock.patch.object(pathlib.Path, "iterdir", return_value=iter([])), \
             mock.patch.object(cmp_harness, "scope_lookup", return_value={"state":"absent","path":scope["cgroup_path"]}), \
             mock.patch.object(cmp_harness, "cgroup_tree_snapshot", return_value={"path":scope["cgroup_path"],"exists":False,"complete":True,"directories":[],"members":[],"errors":[]}):
            sweep = cmp_harness.exact_sweep([marker], {}, scope_identities={marker:scope})
        self.assertFalse(sweep["post_sweep_empty"])
        self.assertEqual([r["pid"] for r in sweep["remaining"]], [321])
        self.assertFalse(sweep["pass"])

    def _run_scrubbed_scope_descendant(self, shape):
        marker = f"run-survivor-z-r0-{shape}"
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d); cg = root / "cell.scope"; cg.mkdir()
            child = cg / "child"; child.mkdir(); grandchild = child / "grandchild"; grandchild.mkdir()
            (cg / "cgroup.kill").write_text(""); (cg / "cgroup.procs").write_text("")
            (child / "cgroup.procs").write_text(""); (grandchild / "cgroup.procs").write_text("")
            if shape == "same-session":
                pid, ppid, sid, member_dir = (501,400,400,cg)
            elif shape == "setsid-cleared-env":
                pid, ppid, sid, member_dir = (502,1,502,child)
            else:
                pid, ppid, sid, member_dir = (503,1,503,grandchild)
            outsider = 599
            (member_dir / "cgroup.procs").write_text(str(pid))
            rows = {pid:{"pid":pid,"start":pid+1000,"ppid":ppid,"sid":sid,"state":"S","exe":"/usr/bin/sleep","argv0":"sleep","env":{}},
                    outsider:{"pid":outsider,"start":outsider+1000,"ppid":1,"sid":outsider,"state":"S","exe":"/usr/bin/sleep","argv0":"unrelated","env":{"CMPMARK":"other-cell","USER":"bench"}}}
            live = {pid:True,outsider:True}; scope_active = {"value":True}; killed=[]; old_iterdir=pathlib.Path.iterdir; old_read_text=pathlib.Path.read_text
            identity={"unit":cmp_harness.scope_name(marker),"control_group":"/system.slice/cell.scope","cgroup_path":str(cg),"scope_kind":"bookkeeping","resource_limits":False}
            def fake_iterdir(path):
                if str(path) == "/proc": return iter([pathlib.Path(f"/proc/{p}") for p in rows if live[p]])
                return old_iterdir(path)
            def fake_read_text(path, *args, **kwargs):
                if str(path).endswith("/mountinfo"): return ""
                return old_read_text(path,*args,**kwargs)
            def fake_proc_stat(p):
                row=rows[int(p)]; return {k:row[k] for k in ("pid","start","ppid","sid","state")}
            def fake_lookup(unit, tools, expected=None):
                state="present" if scope_active["value"] else "absent"
                return {"state":state,"unit":unit,"path":str(cg),"control_group":identity["control_group"],"cgroup_present":scope_active["value"],"errors":[]}
            def fake_systemctl(command, **kwargs):
                self.assertEqual(command[1:3],["stop","--no-block"])
                if (cg / "cgroup.kill").read_text() == "1":
                    tree=cmp_harness.cgroup_tree_snapshot(cg); killed.extend(x["pid"] for x in tree["members"])
                    for victim in killed: live[victim]=False
                    shutil.rmtree(cg); scope_active["value"]=False
                return __import__("subprocess").CompletedProcess(command,0,b"",b"")
            clock={"value":0}
            def monotonic(): clock["value"]+=1; return clock["value"]
            with mock.patch.object(pathlib.Path,"iterdir",new=fake_iterdir), \
                 mock.patch.object(pathlib.Path,"read_text",new=fake_read_text), \
                 mock.patch.object(cmp_harness,"proc_stat",side_effect=fake_proc_stat), \
                 mock.patch.object(cmp_harness,"read_proc_identity",side_effect=lambda p:rows[int(p)]), \
                 mock.patch.object(cmp_harness,"scope_lookup",side_effect=fake_lookup), \
                 mock.patch.object(cmp_harness.subprocess,"run",side_effect=fake_systemctl), \
                 mock.patch.object(cmp_harness.time,"monotonic",side_effect=monotonic), \
                 mock.patch.object(cmp_harness.time,"sleep",return_value=None):
                sweep=cmp_harness.exact_sweep([marker],{"systemctl":pathlib.Path("/fake/systemctl")},scope_identities={marker:identity})
            return sweep,live,killed

    def test_exact_sweep_catches_same_session_marker_scrub(self):
        sweep,live,killed=self._run_scrubbed_scope_descendant("same-session")
        self.assertTrue(sweep["pass"],sweep)
        self.assertEqual(killed,[501])
        self.assertFalse(live[501])
        self.assertTrue(live[599],"unrelated bench process outside cell cgroup must remain live")

    def test_exact_sweep_catches_setsid_cleared_environment_descendant(self):
        sweep,live,killed=self._run_scrubbed_scope_descendant("setsid-cleared-env")
        self.assertTrue(sweep["pass"],sweep)
        self.assertEqual(killed,[502])
        self.assertFalse(live[502])
        self.assertTrue(live[599],"unrelated bench process outside cell cgroup must remain live")

    def test_exact_sweep_catches_double_fork_cleared_environment_descendant(self):
        sweep,live,killed=self._run_scrubbed_scope_descendant("double-fork-cleared-env")
        self.assertTrue(sweep["pass"],sweep)
        self.assertEqual(killed,[503])
        self.assertFalse(live[503])
        self.assertTrue(live[599],"unrelated bench process outside cell cgroup must remain live")

    def test_exact_sweep_fails_if_unmarked_cgroup_member_remains(self):
        marker="run-survivor-z-r0-residual"
        identity={"unit":cmp_harness.scope_name(marker),"control_group":"/system.slice/cell.scope","cgroup_path":"/sys/fs/cgroup/cell.scope","scope_kind":"bookkeeping","resource_limits":False}
        tree={"path":identity["cgroup_path"],"exists":True,"complete":True,"directories":[identity["cgroup_path"]],
              "members":[{"pid":777,"cgroup_path":identity["cgroup_path"]}],"errors":[]}
        with mock.patch.object(cmp_harness,"cleanup_marker",return_value={"pass":True,"remaining":[],"errors":[],"scope":{"pass":True,"scope_absent":False,"scope_identity":identity}}), \
             mock.patch.object(cmp_harness,"scan_marker",return_value=([],[])), \
             mock.patch.object(cmp_harness,"scope_lookup",return_value={"state":"present","path":identity["cgroup_path"],"errors":[]}), \
             mock.patch.object(cmp_harness,"cgroup_tree_snapshot",return_value=tree), \
             mock.patch.object(pathlib.Path,"iterdir",return_value=iter([])):
            sweep=cmp_harness.exact_sweep([marker],{},scope_identities={marker:identity})
        self.assertFalse(sweep["post_sweep_empty"])
        self.assertEqual(sweep["custody_remaining"][0]["tree"]["members"][0]["pid"],777)
        self.assertFalse(sweep["pass"])

    def test_post_sweep_detects_live_marked_pid_replacement(self):
        marker="run-survivor-z-r0-replacement"
        identity={"unit":cmp_harness.scope_name(marker),"control_group":"/system.slice/cell.scope","cgroup_path":"/sys/fs/cgroup/cell.scope","scope_kind":"bookkeeping","resource_limits":False}
        entry=pathlib.Path("/proc/123"); old_iterdir=pathlib.Path.iterdir; old_read_text=pathlib.Path.read_text
        replacement={"pid":123,"start":88,"ppid":1,"sid":88,"state":"S","exe":"/usr/bin/sleep","argv0":"sleep","env":{"CMPMARK":marker}}
        def fake_iterdir(path): return iter([entry]) if str(path)=="/proc" else old_iterdir(path)
        def fake_read_text(path,*args,**kwargs): return "" if str(path).endswith("/mountinfo") else old_read_text(path,*args,**kwargs)
        cleanup={"pass":True,"remaining":[],"errors":[],"scope":{"pass":True,"scope_absent":True,"scope_identity":identity}}
        with mock.patch.object(cmp_harness,"cleanup_marker",return_value=cleanup), \
             mock.patch.object(pathlib.Path,"iterdir",new=fake_iterdir), \
             mock.patch.object(pathlib.Path,"read_text",new=fake_read_text), \
             mock.patch.object(cmp_harness,"proc_stat",side_effect=[{"pid":123,"start":77,"state":"S"},{"pid":123,"start":88,"state":"S"},{"pid":123,"start":88,"state":"S"}]), \
             mock.patch.object(cmp_harness,"observe_proc_cgroup",return_value={"membership":{"path":identity["control_group"]},"after":{"stat":{"start":88}}}), \
             mock.patch.object(cmp_harness,"read_proc_identity",side_effect=[FileNotFoundError(2,"old identity gone"),replacement]), \
             mock.patch.object(cmp_harness,"scope_lookup",return_value={"state":"absent","path":identity["cgroup_path"]}), \
             mock.patch.object(cmp_harness,"cgroup_tree_snapshot",return_value={"path":identity["cgroup_path"],"exists":False,"complete":True,"directories":[],"members":[],"errors":[]}):
            sweep=cmp_harness.exact_sweep([marker],{},scope_identities={marker:identity})
        self.assertFalse(sweep["post_sweep_empty"])
        self.assertEqual(sweep["remaining"],[replacement])
        self.assertTrue(any(n.get("kind")=="pid-identity-rescanned" for n in sweep["observation_notes"]))
        self.assertFalse(sweep["pass"])

    def test_scan_marker_counts_verified_pid_disappearance_as_note(self):
        entry = pathlib.Path("/proc/123"); old_iterdir = pathlib.Path.iterdir
        def fake_iterdir(path):
            if str(path) == "/proc": return iter([entry])
            return old_iterdir(path)
        with mock.patch.object(pathlib.Path, "iterdir", new=fake_iterdir), \
             mock.patch.object(cmp_harness, "proc_stat", side_effect=[{"pid":123,"start":77,"state":"S"}, FileNotFoundError(2, "gone")]), \
             mock.patch.object(cmp_harness, "read_proc_identity", side_effect=FileNotFoundError(2, "gone")):
            notes=[]; rows, errors = cmp_harness.scan_marker("cell-marker", notes)
        self.assertEqual(rows, [])
        self.assertEqual(errors, [])
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["kind"], "verified-process-exit")
        self.assertEqual(notes[0]["expected_start"], 77)

    def test_proc_stat_parses_pf_kthread_flag_after_the_last_comm_parenthesis(self):
        tail = [b"S", b"11", b"22", b"33", b"0", b"-1", str(cmp_harness.PF_KTHREAD).encode()] + [b"0"] * 10 + [b"1", b"0", b"777"]
        raw = b"123 (worker ) with paren) " + b" ".join(tail)
        with mock.patch.object(pathlib.Path, "read_bytes", return_value=raw):
            stat = cmp_harness.proc_stat(123)
        self.assertEqual(stat["flags"], cmp_harness.PF_KTHREAD)
        self.assertEqual(stat["start"], 777)
        self.assertEqual(stat["state"], "S")
        self.assertEqual(stat["num_threads"], 1)
        self.assertEqual(stat["pid"], 123)
        zombie_tail=list(tail); zombie_tail[0]=b"Z"; zombie_tail[17]=b"0"
        with mock.patch.object(pathlib.Path,"read_bytes",return_value=b"123 (worker) "+b" ".join(zombie_tail)):
            self.assertEqual(cmp_harness.proc_stat(123)["num_threads"],0)

    def test_proc_stat_rejects_truncated_or_invalid_kernel_thread_counts(self):
        rows = [b"123 (worker) S 11", b"123 (worker) S 11 22 33 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 77"]
        for raw in rows:
            with self.subTest(raw=raw), mock.patch.object(pathlib.Path, "read_bytes", return_value=raw):
                with self.assertRaises(ValueError): cmp_harness.proc_stat(123)

    def test_kernel_thread_exception_requires_unambiguous_no_mm_identity(self):
        good_status = b"Name:\ttask-2\nState:\tS (sleeping)\nKthread:\t1\n"

        def probe(status=good_status, cmdline=b"", exe_errno=errno.ENOENT, starts=(77, 77), flags=None):
            flags = flags if flags is not None else (cmp_harness.PF_KTHREAD, cmp_harness.PF_KTHREAD)
            calls = {"stat":0}

            def fake_read_bytes(path, *args, **kwargs):
                if str(path).endswith("/status"): return status
                if str(path).endswith("/cmdline"): return cmdline
                raise AssertionError(f"unexpected proc read: {path}")

            def fake_stat(pid):
                index = min(calls["stat"], len(starts) - 1); calls["stat"] += 1
                flag_index = min(index, len(flags) - 1)
                return {"start":starts[index], "flags":flags[flag_index], "state":"S"}

            def fake_readlink(path):
                if exe_errno is not None: raise OSError(exe_errno, "kernel task exe link unavailable")
                return "/usr/bin/python3"

            with mock.patch.object(pathlib.Path, "read_bytes", new=fake_read_bytes), \
                 mock.patch.object(os, "readlink", side_effect=fake_readlink), \
                 mock.patch.object(cmp_harness, "proc_stat", side_effect=fake_stat):
                return cmp_harness.proc_is_kernel_thread(2, 77)

        self.assertTrue(probe(), "a stable PF_KTHREAD with empty cmdline and no exe is exempt")
        rejected = [
            ("nonempty-cmdline", {"cmdline":b"/usr/bin/python3\x00"}, "userspace cmdline prevents the exemption"),
            ("readable-exe", {"exe_errno":None}, "a readable executable prevents the exemption"),
            ("non-pfkthread", {"flags":(0, 0)}, "the status field alone is not trusted"),
            ("changed-start", {"starts":(77, 78)}, "a changed start time rejects PID reuse"),
            ("missing-field", {"status":b"Name:\ttask-2\nState:\tS\n"}, "missing Kthread field fails closed"),
            ("malformed-field", {"status":b"Name:\ttask-2\nKthread\t1\n"}, "malformed Kthread field fails closed"),
            ("duplicate-field", {"status":b"Kthread:\t1\nKthread:\t1\n"}, "duplicate Kthread fields fail closed"),
        ]
        rejected.extend((f"exe-errno-{number}", {"exe_errno":number}, "unrelated exe-link errors remain fatal")
                        for number in (errno.EACCES, errno.EPERM, errno.EIO, errno.EINVAL))
        for condition, kwargs, message in rejected:
            with self.subTest(condition=condition):
                self.assertFalse(probe(**kwargs), message)

    def test_scan_marker_skips_only_verified_live_kernel_threads_without_mm(self):
        entries = [pathlib.Path("/proc/2"), pathlib.Path("/proc/123")]
        old_iterdir = pathlib.Path.iterdir; old_read_bytes = pathlib.Path.read_bytes

        def fake_iterdir(path):
            return iter(entries) if str(path) == "/proc" else old_iterdir(path)

        def fake_read_bytes(path, *args, **kwargs):
            if str(path).endswith("/environ"):
                raise ProcessLookupError(errno.ESRCH, "No such process")
            if str(path).endswith("/status"):
                pid = int(path.parent.name)
                return f"Name:\ttask-{pid}\nState:\tS (sleeping)\nKthread:\t{1 if pid == 2 else 0}\n".encode()
            if str(path).endswith("/cmdline"):
                return b"" if path.parent.name == "2" else b"/usr/bin/python3\x00bench-process\x00"
            return old_read_bytes(path, *args, **kwargs)

        def same_live_process(pid):
            return {"pid":pid,"ppid":2 if pid == 2 else 1,"sid":pid,"start":1000 + pid,"state":"S",
                    "flags":cmp_harness.PF_KTHREAD if pid == 2 else 0}

        def fake_readlink(path):
            if path.parent.name == "2": raise FileNotFoundError(errno.ENOENT, "kernel task has no executable")
            return "/usr/bin/python3"

        with mock.patch.object(pathlib.Path, "iterdir", new=fake_iterdir), \
             mock.patch.object(pathlib.Path, "read_bytes", new=fake_read_bytes), \
             mock.patch.object(os, "readlink", side_effect=fake_readlink), \
             mock.patch.object(cmp_harness, "proc_stat", side_effect=same_live_process):
            notes = []; rows, errors = cmp_harness.scan_marker("cell-marker", notes)

        self.assertEqual(rows, [])
        self.assertEqual(errors, ["123:proc:3:/proc/123/environ:same-process-live"])
        self.assertEqual([note["pid"] for note in notes if note["kind"] == "verified-kernel-thread-without-userspace-mm"], [2])

    def test_scan_marker_rejects_comm_separators_that_spoof_kthread_status(self):
        entry = pathlib.Path("/proc/123"); old_iterdir = pathlib.Path.iterdir
        separators = (b"\r", b"\x0b", b"\x0c", b"\x1c", b"\x1d", b"\x1e", b"\xc2\x85", b"\xe2\x80\xa8", b"\xe2\x80\xa9")

        def fake_iterdir(path):
            return iter([entry]) if str(path) == "/proc" else old_iterdir(path)

        with tempfile.TemporaryDirectory() as d:
            status_file = pathlib.Path(d) / "status"
            old_read_bytes = pathlib.Path.read_bytes; old_read_text = pathlib.Path.read_text

            def routed_read_bytes(path, *args, **kwargs):
                if str(path) == "/proc/123/status": return old_read_bytes(status_file)
                return old_read_bytes(path, *args, **kwargs)

            def routed_read_text(path, *args, **kwargs):
                if str(path) == "/proc/123/status": return old_read_text(status_file, *args, **kwargs)
                return old_read_text(path, *args, **kwargs)

            for separator in separators:
                with self.subTest(separator=separator):
                    status_file.write_bytes(b"Name:\tx" + separator + b"Kthread: 1\nState:\tS (sleeping)\nUid:\t1001\t1001\t1001\t1001\nKthread:\t0\n")
                    with mock.patch.object(pathlib.Path, "iterdir", new=fake_iterdir), \
                         mock.patch.object(pathlib.Path, "read_bytes", new=routed_read_bytes), \
                         mock.patch.object(pathlib.Path, "read_text", new=routed_read_text), \
                         mock.patch.object(cmp_harness, "proc_stat", return_value={"pid":123,"ppid":1,"sid":123,"start":77,"state":"S","flags":0}), \
                         mock.patch.object(cmp_harness, "read_proc_identity", side_effect=ProcessLookupError(errno.ESRCH, "no userspace memory")):
                        notes = []; rows, errors = cmp_harness.scan_marker("cell-marker", notes)
                    self.assertEqual(rows, [])
                    self.assertEqual(errors, ["123:proc:3:<unknown-path>:same-process-live"])
                    self.assertFalse(any(note["kind"] == "verified-kernel-thread-without-userspace-mm" for note in notes))

    def test_scan_marker_verifies_zombie_separately_from_kernel_thread_fallback(self):
        entry = pathlib.Path("/proc/123"); old_iterdir = pathlib.Path.iterdir

        def fake_iterdir(path):
            return iter([entry]) if str(path) == "/proc" else old_iterdir(path)

        for number in (errno.EACCES, errno.EPERM, errno.EIO, errno.EINVAL):
            exc_type = PermissionError if number in (errno.EACCES, errno.EPERM) else OSError
            exc = exc_type(number, "proc read failed")
            with self.subTest(errno=number), \
                 mock.patch.object(pathlib.Path, "iterdir", new=fake_iterdir), \
                 mock.patch.object(cmp_harness, "proc_stat", return_value={"pid":123,"ppid":1,"sid":123,"start":77,"state":"S","flags":cmp_harness.PF_KTHREAD}), \
                 mock.patch.object(cmp_harness, "read_proc_identity", side_effect=exc), \
                 mock.patch.object(cmp_harness, "proc_is_kernel_thread") as thread_check:
                notes = []; rows, errors = cmp_harness.scan_marker("cell-marker", notes)
            self.assertEqual(rows, [])
            self.assertFalse(any(note["kind"] == "verified-kernel-thread-without-userspace-mm" for note in notes))
            self.assertEqual(errors, [f"123:{'permission' if number in (errno.EACCES, errno.EPERM) else 'proc'}:{number}:<unknown-path>"])
            thread_check.assert_not_called()

        same=self.proc_row(123,77,ppid=2,flags=cmp_harness.PF_KTHREAD)
        zombie=self.proc_row(123,77,state="Z",ppid=2,flags=cmp_harness.PF_KTHREAD)
        with mock.patch.object(pathlib.Path, "iterdir", new=fake_iterdir), \
             mock.patch.object(cmp_harness, "proc_stat", side_effect=[same,zombie]), \
             mock.patch.object(cmp_harness, "read_proc_identity", side_effect=ProcessLookupError(errno.ESRCH, "no userspace memory")), \
             mock.patch.object(cmp_harness, "verify_nonrunnable_group", return_value={"ok":False,"reason":"parent stat context unavailable"}), \
             mock.patch.object(cmp_harness, "proc_is_kernel_thread") as thread_check:
            notes = []; rows, errors = cmp_harness.scan_marker("cell-marker", notes)
        self.assertEqual(rows, [])
        self.assertEqual(len(errors),1)
        self.assertEqual(notes[0]["kind"], "unverified-zombie-group")
        self.assertEqual(notes[0]["expected_start"], 77)
        self.assertEqual(notes[0]["current_start"], 77)
        self.assertEqual(notes[0]["state"], "Z")
        self.assertFalse(any(note["kind"] == "verified-kernel-thread-without-userspace-mm" for note in notes))
        thread_check.assert_not_called()

    def test_double_fork_zombie_esrch_is_a_proved_nonrunnable_note(self):
        entry = pathlib.Path("/proc/123"); old_iterdir = pathlib.Path.iterdir
        marker = "cell-double-fork"
        def fake_iterdir(path): return iter([entry]) if str(path) == "/proc" else old_iterdir(path)
        same = self.proc_row(123,77)
        zombie = self.proc_row(123,77,state="Z")
        parent = self.proc_row(1,10)
        error = ProcessLookupError(errno.ESRCH, "No such process", "/proc/123/environ")
        with mock.patch.object(pathlib.Path, "iterdir", new=fake_iterdir), \
             mock.patch.object(pathlib.Path, "read_text", new=lambda path,*a,**k: "0::/system.slice/cell.scope\n" if str(path)=="/proc/123/cgroup" else ""), \
             mock.patch.object(cmp_harness, "proc_stat", side_effect=[same,zombie,parent,zombie,zombie,parent]), \
             mock.patch.object(cmp_harness, "proc_task_census", return_value={"path":"/proc/123/task","tids":[123],"read_started_ns":1,"read_completed_ns":2,"error":None}), \
             mock.patch.object(cmp_harness, "read_proc_identity", side_effect=error), \
             mock.patch.object(cmp_harness, "proc_is_kernel_thread") as thread_check:
            notes=[]; diagnostics=[]; rows, errors=cmp_harness.scan_marker(marker,notes,proc_diagnostics=diagnostics)
        self.assertEqual(rows,[])
        self.assertEqual(errors,[])
        self.assertEqual(len(notes),1)
        self.assertEqual(notes[0]["kind"],"verified-nonrunnable-zombie")
        self.assertEqual(notes[0]["error_errno"],errno.ESRCH)
        self.assertEqual(notes[0]["error_path"],"/proc/123/environ")
        self.assertEqual(notes[0]["expected_start"],notes[0]["current_start"])
        self.assertEqual(notes[0]["state"],"Z")
        self.assertEqual(notes[0]["proof"]["thread_census"]["tids"],[123])
        self.assertEqual(notes[0]["proof"]["parent_context"]["pid"],1)
        self.assertEqual(notes[0]["proc_path"],"/proc/123/environ")
        self.assertEqual(notes[0]["errno"],errno.ESRCH)
        self.assertEqual(notes[0]["start_time"],77)
        self.assertEqual(notes[0]["cgroup"],"/system.slice/cell.scope")
        self.assertTrue(diagnostics)
        self.assertEqual(diagnostics[0]["proc_path"],"/proc/123/environ")
        self.assertEqual(diagnostics[0]["pid"],123)
        self.assertEqual(diagnostics[0]["start_time"],77)
        self.assertEqual(diagnostics[0]["errno"],errno.ESRCH)
        thread_check.assert_not_called()
        evidence=cmp_harness.bool_evidence("survivor_double_fork",False)
        evidence["observer_ok"]=not errors
        evidence["survivor_protocol"]["post_scan_complete"]=not errors
        self.assertEqual(cmp_harness.score("survivor_double_fork",evidence),"BLOCKED")

    def test_scan_marker_distinguishes_reused_zombie_from_same_live_process(self):
        entry=pathlib.Path("/proc/123"); old_iterdir=pathlib.Path.iterdir
        def fake_iterdir(path): return iter([entry]) if str(path)=="/proc" else old_iterdir(path)
        before=self.proc_row(123,77)
        replacement=self.proc_row(123,88,state="Z")
        error=ProcessLookupError(errno.ESRCH,"No such process","/proc/123/environ")
        with mock.patch.object(pathlib.Path,"iterdir",new=fake_iterdir), \
             mock.patch.object(cmp_harness,"proc_stat",side_effect=[before,replacement]), \
             mock.patch.object(cmp_harness,"read_proc_identity",side_effect=error):
            notes=[]; rows,errors=cmp_harness.scan_marker("cell-marker",notes)
        self.assertEqual(rows,[])
        self.assertEqual(len(errors),1)
        self.assertEqual(notes[0]["kind"],"unverified-zombie-identity")
        self.assertEqual(notes[0]["expected_start"],77)
        self.assertEqual(notes[0]["current_start"],88)
        self.assertEqual(notes[0]["verification"],"pid-reused-zombie")

    def test_scan_marker_keeps_unidentified_zombie_invalid(self):
        entry=pathlib.Path("/proc/123"); old_iterdir=pathlib.Path.iterdir
        def fake_iterdir(path): return iter([entry]) if str(path)=="/proc" else old_iterdir(path)
        zombie=self.proc_row(123,88,state="Z")
        error=ProcessLookupError(errno.ESRCH,"No such process","/proc/123/stat")
        with mock.patch.object(pathlib.Path,"iterdir",new=fake_iterdir), \
             mock.patch.object(cmp_harness,"proc_stat",side_effect=[error,zombie]), \
             mock.patch.object(cmp_harness,"read_proc_identity",side_effect=error):
            notes=[]; rows,errors=cmp_harness.scan_marker("cell-marker",notes)
        self.assertEqual(rows,[])
        self.assertTrue(errors)
        self.assertEqual(notes[0]["kind"],"unverified-zombie-identity")
        self.assertIsNone(notes[0]["expected_start"])
        self.assertEqual(notes[0]["current_start"],88)

    def test_zombie_group_with_live_sibling_tid_stays_incomplete(self):
        expected={"pid":123,"start":77}; before=self.proc_row(123,77,ppid=1)
        zombie=self.proc_row(123,77,state="Z",ppid=1,threads=2)
        parent=self.proc_row(1,10)
        observations=[self.proc_observation(1,parent),self.proc_observation(123,zombie),
                      self.proc_observation(123,zombie),self.proc_observation(1,parent)]
        verification={"pid":123,"expected_start":77,"current_start":77,"state":"Z",
                      "verification":"same-process-zombie","current_stat":zombie,
                      "stat_observation":self.proc_observation(123,zombie)}
        census={"path":"/proc/123/task","tids":[123,124],"read_started_ns":1,"read_completed_ns":2,"error":None}
        cgroup={"pid":123,"expected_start":77,"membership":{"path":"/system.slice/cell.scope","read_error":None},
                "verified_identity":True,"cgroup_path":"/system.slice/cell.scope"}
        with mock.patch.object(cmp_harness,"proc_stat_observation",side_effect=observations), \
             mock.patch.object(cmp_harness,"proc_task_census",return_value=census), \
             mock.patch.object(cmp_harness,"observe_proc_cgroup",return_value=cgroup):
            proof=cmp_harness.verify_nonrunnable_group(expected,self.proc_observation(123,before),verification)
        self.assertFalse(proof["ok"])
        self.assertEqual(proof["reason"],"zombie thread group has additional or unidentified tasks")
        self.assertEqual(proof["thread_census"]["tids"],[123,124])

    def test_zombie_proof_requires_complete_task_and_parent_context(self):
        expected={"pid":123,"start":77}; before=self.proc_row(123,77,ppid=1)
        zombie=self.proc_row(123,77,state="Z",ppid=1)
        verification={"pid":123,"expected_start":77,"current_start":77,"state":"Z",
                      "verification":"same-process-zombie","current_stat":zombie,
                      "stat_observation":self.proc_observation(123,zombie)}
        parent_error={"pid":1,"read_started_ns":1,"read_completed_ns":2,"stat":None,
                      "error":"FileNotFoundError","error_errno":errno.ESRCH,"error_path":"/proc/1/stat"}
        parent=self.proc_observation(1,self.proc_row(1,10))
        final=self.proc_observation(123,zombie)
        cgroup={"pid":123,"expected_start":77,"membership":{"path":"/system.slice/cell.scope","read_error":None},
                "verified_identity":True,"cgroup_path":"/system.slice/cell.scope"}
        for condition,census,stat_observations in (
            ("missing-parent",{"path":"/proc/123/task","tids":[123],"error":None},[parent_error,final,parent_error]),
            ("truncated-task-census",{"path":"/proc/123/task","tids":None,"error":"EIO","error_errno":errno.EIO},[parent,final,parent]),
        ):
            with self.subTest(condition=condition), \
                 mock.patch.object(cmp_harness,"proc_stat_observation",side_effect=stat_observations), \
                 mock.patch.object(cmp_harness,"proc_task_census",return_value=census), \
                 mock.patch.object(cmp_harness,"observe_proc_cgroup",return_value=cgroup):
                proof=cmp_harness.verify_nonrunnable_group(expected,self.proc_observation(123,before),verification)
            self.assertFalse(proof["ok"])
            self.assertIsNotNone(proof["reason"])

    def test_live_zombie_regression_wait_retries_transient_runnable_state(self):
        runnable = self.proc_row(123, 77, state="R", threads=2)
        zombie = self.proc_row(123, 77, state="Z", threads=2)
        rows = iter((runnable, zombie))
        ticks = iter((0.0, 0.0))
        sleeps = []
        result = wait_for_zombie_group_leader_with_worker(
            123, timeout=1.0, stat_reader=lambda pid: next(rows),
            clock=lambda: next(ticks), sleeper=sleeps.append,
        )
        self.assertEqual(result, zombie)
        self.assertEqual(sleeps, [0.001])

    def test_live_zombie_regression_timeout_keeps_non_zombie_unqualified(self):
        runnable = self.proc_row(123, 77, state="R", threads=2)
        ticks = iter((0.0, 0.0, 1.0))
        with self.assertRaisesRegex(AssertionError, "last stat=.*'state': 'R'"):
            wait_for_zombie_group_leader_with_worker(
                123, timeout=1.0, stat_reader=lambda pid: runnable,
                clock=lambda: next(ticks), sleeper=lambda delay: None,
            )

    @unittest.skipUnless(sys.platform.startswith("linux") and pathlib.Path("/proc/self/task").is_dir(),
                         "requires Linux procfs and pthreads")
    def test_linux_zombie_group_leader_does_not_hide_live_worker(self):
        source='''#include <pthread.h>
#include <stdio.h>
#include <unistd.h>
static void *worker(void *unused) { (void)unused; for (;;) pause(); return NULL; }
int main(void) { pthread_t thread; setvbuf(stdout, NULL, _IONBF, 0);
  if (pthread_create(&thread, NULL, worker, NULL) != 0) return 2;
  puts("worker-ready"); pthread_exit(NULL); }
'''
        marker="cmp-small11-live-thread-group-"+str(os.getpid())
        with tempfile.TemporaryDirectory() as directory:
            source_path=pathlib.Path(directory)/"thread_group.c"; binary=pathlib.Path(directory)/"thread_group"
            source_path.write_text(source)
            build=subprocess.run(["cc","-O2","-pthread",str(source_path),"-o",str(binary)],
                                 stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,check=False)
            self.assertEqual(build.returncode,0,build.stderr)
            env=dict(os.environ); env["CMPMARK"]=marker
            child=subprocess.Popen([str(binary)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=env)
            try:
                self.assertEqual(child.stdout.readline().strip(),"worker-ready")
                stat=wait_for_zombie_group_leader_with_worker(child.pid)
                tids=cmp_harness.proc_task_census(child.pid)["tids"]
                self.assertIsNotNone(tids)
                self.assertGreaterEqual(len(tids),2)
                with self.assertRaises(OSError) as environ_error:
                    cmp_harness.proc_read_bytes(f"/proc/{child.pid}/environ")
                self.assertEqual(environ_error.exception.errno,errno.ESRCH)
                notes=[]; diagnostics=[]
                rows,errors=cmp_harness.scan_marker(marker,notes,proc_diagnostics=diagnostics)
                self.assertFalse(any(row.get("pid")==child.pid for row in rows))
                self.assertTrue(any(str(child.pid) in error and "zombie" in error for error in errors),errors)
                event=next(d for d in diagnostics if d.get("pid")==child.pid and d.get("event_type")=="error")
                self.assertEqual(event["start_time"],stat["start"])
                self.assertIsNotNone(event["identity_snapshots"]["before"])
            finally:
                child.kill(); child.wait(timeout=5)

    def test_read_proc_identity_keeps_partial_identity_when_exe_link_read_fails(self):
        marker="exact-exe-race-marker"
        def read_proc(path):
            if str(path)=="/proc/123/environ": return f"CMPMARK={marker}\x00USER=bench\x00".encode()
            if str(path)=="/proc/123/cmdline": return b"fixture-runner\x00arg\x00"
            raise AssertionError(f"unexpected proc read: {path}")
        stat=self.proc_row(123,77,ppid=2)
        error=FileNotFoundError(errno.ENOENT,"exe link vanished","/proc/123/exe")
        with mock.patch.object(cmp_harness,"proc_read_bytes",side_effect=read_proc), \
             mock.patch.object(cmp_harness,"proc_stat",return_value=stat), \
             mock.patch.object(os.path,"realpath",side_effect=error):
            with self.assertRaises(FileNotFoundError) as caught:
                cmp_harness.read_proc_identity(123)
        self.assertEqual(cmp_harness.proc_error_path(caught.exception),"/proc/123/exe")
        self.assertEqual(caught.exception.partial_identity["start"],77)
        self.assertEqual(caught.exception.partial_identity["env"]["CMPMARK"],marker)
        self.assertEqual(caught.exception.partial_identity["argv0"],"fixture-runner")
        self.assertIsNone(caught.exception.partial_identity["exe"])

    def test_scan_marker_proves_transient_exe_link_exit_and_retains_positive_marker(self):
        marker="run-exe-link-z-r0-transient"; entry=pathlib.Path("/proc/123"); old_iterdir=pathlib.Path.iterdir
        stat=self.proc_row(123,77,ppid=2)
        def fake_iterdir(path): return iter([entry]) if str(path)=="/proc" else old_iterdir(path)
        def read_proc(path):
            if str(path)=="/proc/123/environ": return f"CMPMARK={marker}\x00".encode()
            if str(path)=="/proc/123/cmdline": return marker.encode()+b"\x00"
            raise AssertionError(f"unexpected proc read: {path}")
        same={"pid":123,"start":77,"state":"S","current_start":77,
              "stat_observation":self.proc_observation(123,stat)}
        gone={"pid":123,"expected_start":77,"verification":"proc-entry-gone",
              "stat_observation":{"pid":123,"stat":None,"error":"gone"}}
        sequence=[(False,{**same,"verification":"same-process-live"}),
                  (False,{**same,"verification":"same-process-live"}),(True,gone)]
        exe_error=FileNotFoundError(errno.ENOENT,"executable link vanished","/proc/123/exe")
        with mock.patch.object(pathlib.Path,"iterdir",new=fake_iterdir), \
             mock.patch.object(cmp_harness,"proc_read_bytes",side_effect=read_proc), \
             mock.patch.object(cmp_harness,"proc_stat",return_value=stat), \
             mock.patch.object(os.path,"realpath",side_effect=exe_error), \
             mock.patch.object(cmp_harness,"verified_process_exit",side_effect=sequence) as verify, \
             mock.patch.object(cmp_harness,"proc_is_kernel_thread",return_value=False), \
             mock.patch.object(cmp_harness,"proc_cgroup_info",return_value={"pid":123,"path":"/system.slice/test.scope"}), \
             mock.patch.object(cmp_harness.time,"sleep",return_value=None):
            notes=[]; diagnostics=[]; rows,errors=cmp_harness.scan_marker(marker,notes,proc_diagnostics=diagnostics)
        self.assertEqual(rows,[])
        self.assertEqual(errors,[])
        self.assertEqual(verify.call_count,3)
        partial=next(note for note in notes if note["kind"]=="partial-positive-marker-observation")
        self.assertTrue(partial["marker_match"])
        self.assertEqual(partial["cmpmark"],marker)
        exit_note=next(note for note in notes if note["kind"]=="verified-process-exit")
        self.assertEqual(len(exit_note["rechecks"]),2)

    def test_scan_marker_keeps_live_exe_link_error_and_structured_rechecks(self):
        marker="run-exe-link-b-r0-live"; entry=pathlib.Path("/proc/123"); old_iterdir=pathlib.Path.iterdir
        stat=self.proc_row(123,77,ppid=2,state="D")
        def fake_iterdir(path): return iter([entry]) if str(path)=="/proc" else old_iterdir(path)
        def read_proc(path):
            if str(path)=="/proc/123/environ": return f"CMPMARK={marker}\x00".encode()
            if str(path)=="/proc/123/cmdline": return marker.encode()+b"\x00"
            raise AssertionError(f"unexpected proc read: {path}")
        live={"pid":123,"expected_start":77,"current_start":77,"state":"D",
              "verification":"same-process-live","current_stat":stat,
              "stat_observation":self.proc_observation(123,stat)}
        error=FileNotFoundError(errno.ENOENT,"executable link unavailable","/proc/123/exe")
        with mock.patch.object(pathlib.Path,"iterdir",new=fake_iterdir), \
             mock.patch.object(cmp_harness,"proc_read_bytes",side_effect=read_proc), \
             mock.patch.object(cmp_harness,"proc_stat",return_value=stat), \
             mock.patch.object(os.path,"realpath",side_effect=error), \
             mock.patch.object(cmp_harness,"verified_process_exit",return_value=(False,live)) as verify, \
             mock.patch.object(cmp_harness,"proc_is_kernel_thread",return_value=False), \
             mock.patch.object(cmp_harness,"observe_proc_cgroup",return_value={"membership":{"path":"/system.slice/test.scope"}}), \
             mock.patch.object(cmp_harness.time,"sleep",return_value=None):
            notes=[]; diagnostics=[]; rows,errors=cmp_harness.scan_marker(marker,notes,proc_diagnostics=diagnostics)
        self.assertEqual(rows,[])
        self.assertEqual(errors,["123:proc:2:/proc/123/exe:same-process-live"])
        self.assertEqual(verify.call_count,4)
        error_record=next(row for row in diagnostics if row["event_type"]=="error")
        self.assertEqual(error_record["proc_path"],"/proc/123/exe")
        self.assertEqual(error_record["errno"],errno.ENOENT)
        self.assertEqual(error_record["pid"],123)
        self.assertEqual(error_record["start_time"],77)
        self.assertEqual(error_record["cgroup"],"/system.slice/test.scope")
        self.assertEqual(len(error_record["identity_snapshots"]["rechecks"]),3)
        self.assertTrue(any(note["kind"]=="partial-positive-marker-observation" for note in notes))

    def test_exact_sweep_retains_structured_observer_errors(self):
        marker="synthetic-final-sweep-marker"
        diagnostic={"event_type":"error","message":"observer race","proc_path":"/proc/123/exe",
                    "errno":errno.ENOENT,"pid":123,"start_time":77,"cgroup":"/system.slice/test.scope"}
        def scanner(_marker,_notes,proc_diagnostics):
            proc_diagnostics.append(diagnostic)
            return [],["123:proc:2:/proc/123/exe:same-process-live"]
        with mock.patch.object(cmp_harness,"cleanup_marker",return_value={"pass":True,"scope":{"pass":True,"scope_absent":True},"observation_notes":[]}), \
             mock.patch.object(cmp_harness,"scan_marker",side_effect=scanner), \
             mock.patch.object(pathlib.Path,"iterdir",return_value=iter([])):
            sweep=cmp_harness.exact_sweep([marker],{})
        self.assertFalse(sweep["pass"])
        self.assertEqual(sweep["observer_errors"],[{**diagnostic,"marker":marker}])

    def test_scan_marker_rechecks_environ_esrch_until_same_process_disappears(self):
        marker="run-environ-exit-z-r0-transient"; entry=pathlib.Path("/proc/123"); old_iterdir=pathlib.Path.iterdir
        stat=self.proc_row(123,77,ppid=2)
        def fake_iterdir(path): return iter([entry]) if str(path)=="/proc" else old_iterdir(path)
        error=ProcessLookupError(errno.ESRCH,"No userspace memory","/proc/123/environ")
        def fail_environ(path):
            if str(path)=="/proc/123/environ": raise error
            raise AssertionError(f"unexpected proc read: {path}")
        live={"pid":123,"expected_start":77,"current_start":77,"state":"R",
              "verification":"same-process-live","current_stat":stat,
              "stat_observation":self.proc_observation(123,stat)}
        gone={"pid":123,"expected_start":77,"verification":"proc-entry-gone",
              "stat_observation":{"pid":123,"stat":None,"error":"gone"}}
        with mock.patch.object(pathlib.Path,"iterdir",new=fake_iterdir), \
             mock.patch.object(cmp_harness,"proc_read_bytes",side_effect=fail_environ), \
             mock.patch.object(cmp_harness,"proc_stat",return_value=stat), \
             mock.patch.object(cmp_harness,"verified_process_exit",side_effect=[(False,live),(True,gone)]) as verify, \
             mock.patch.object(cmp_harness,"proc_is_kernel_thread",return_value=False), \
             mock.patch.object(cmp_harness,"proc_cgroup_info",return_value={"pid":123,"path":"/system.slice/test.scope"}), \
             mock.patch.object(cmp_harness.time,"sleep",return_value=None):
            notes=[]; diagnostics=[]; rows,errors=cmp_harness.scan_marker(marker,notes,proc_diagnostics=diagnostics)
        self.assertEqual(rows,[])
        self.assertEqual(errors,[])
        self.assertEqual(verify.call_count,2)
        note=next(item for item in notes if item["kind"]=="verified-process-exit")
        self.assertEqual(note["error_path"],"/proc/123/environ")
        self.assertEqual(note["error_errno"],errno.ESRCH)
        self.assertEqual(note["expected_start"],77)
        self.assertEqual(len(note["rechecks"]),1)
        self.assertTrue(any(item.get("event_type")=="note" and item.get("proc_path")=="/proc/123/environ"
                            for item in diagnostics))

    def test_scan_marker_keeps_unattributed_d_state_esrch_invalid(self):
        entry=pathlib.Path("/proc/123"); old_iterdir=pathlib.Path.iterdir
        def fake_iterdir(path): return iter([entry]) if str(path)=="/proc" else old_iterdir(path)
        same={"pid":123,"ppid":1,"sid":123,"start":77,"state":"D","flags":0}
        live={"pid":123,"expected_start":77,"current_start":77,"state":"D",
              "verification":"same-process-live","current_stat":same,
              "stat_observation":self.proc_observation(123,same)}
        error=ProcessLookupError(errno.ESRCH,"No such process","/proc/123/environ")
        with mock.patch.object(pathlib.Path,"iterdir",new=fake_iterdir), \
             mock.patch.object(cmp_harness,"proc_stat",return_value=same), \
             mock.patch.object(cmp_harness,"read_proc_identity",side_effect=error), \
             mock.patch.object(cmp_harness,"verified_process_exit",return_value=(False,live)) as verify, \
             mock.patch.object(cmp_harness,"proc_is_kernel_thread",return_value=False), \
             mock.patch.object(cmp_harness.time,"sleep",return_value=None):
            notes=[]; diagnostics=[]; rows,errors=cmp_harness.scan_marker("cell-marker",notes,proc_diagnostics=diagnostics)
        self.assertEqual(rows,[])
        self.assertEqual(errors,["123:proc:3:/proc/123/environ:same-process-live"])
        self.assertEqual(verify.call_count,4)
        event=next(row for row in diagnostics if row.get("event_type")=="error")
        self.assertEqual(len(event["identity_snapshots"]["rechecks"]),3)
        self.assertFalse(notes)

    def _oom_cell_evidence(self, marker, oom_kill=1):
        unit=cmp_harness.scope_name(marker); control=f"/system.slice/{unit}"
        identity={"unit":unit,"control_group":control,"cgroup_path":"/sys/fs/cgroup"+control}
        def sample(final, killed):
            events=f"low 0\nhigh 0\nmax {1 if killed else 0}\noom {killed}\noom_kill {killed}\n"
            if killed != oom_kill: events="low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\n"
            return {"ok":True,"path":identity["cgroup_path"],"scope_identity":identity,"final":final,
                    "files":{"memory.current":"1","memory.peak":str(cmp_harness.CAPS["memory.max"]),
                             "memory.max":str(cmp_harness.CAPS["memory.max"]),"memory.events":events,
                             "pids.current":"3","pids.peak":"4","pids.max":"64","pids.events":"max 0",
                             "cgroup.events":"populated 1\nfrozen 0"}}
        return cmp_harness.cgroup_evidence([sample(False,0),sample(True,oom_kill)])

    def test_mem_cap_oom_esrch_is_ignored_only_with_same_scope_and_final_oom_kill(self):
        entry=pathlib.Path("/proc/123"); old_iterdir=pathlib.Path.iterdir; old_read_text=pathlib.Path.read_text
        marker="run-mem_cap-b-r0-oom-proof"; scope_evidence=self._oom_cell_evidence(marker)
        identity=scope_evidence["resource_scope_identity"]
        def fake_iterdir(path): return iter([entry]) if str(path)=="/proc" else old_iterdir(path)
        def fake_read_text(path,*args,**kwargs):
            if str(path)=="/proc/123/cgroup": return f"0::{identity['control_group']}\n"
            return old_read_text(path,*args,**kwargs)
        same=self.proc_row(123,77,state="D")
        error=ProcessLookupError(errno.ESRCH,"No such process","/proc/123/environ")
        wait_context={"pid":200,"start_time":66,"returncode":0,"wait_observed_monotonic_ns":3}
        with mock.patch.object(pathlib.Path,"iterdir",new=fake_iterdir), \
             mock.patch.object(pathlib.Path,"read_text",new=fake_read_text), \
             mock.patch.object(cmp_harness,"proc_stat",side_effect=[same,same,same,same,ProcessLookupError(errno.ESRCH,"gone","/proc/123/stat")]), \
             mock.patch.object(cmp_harness,"read_proc_identity",side_effect=error), \
             mock.patch.object(cmp_harness,"proc_is_kernel_thread",return_value=False):
            notes=[]; diagnostics=[]; rows,errors=cmp_harness.scan_marker(marker,notes,resource_scope_identity=identity,
                proc_diagnostics=diagnostics,harness_wait_result=wait_context)
        self.assertEqual(rows,[])
        self.assertEqual(len(errors),1)
        self.assertIn("/proc/123/environ",errors[0])
        candidate=next(n for n in notes if n["kind"]=="resource-scope-proc-read-candidate")
        self.assertEqual(candidate["proc_cgroup"],identity["control_group"])
        cmp_harness.reconcile_resource_oom_observer_errors("mem_cap",marker,errors,notes,scope_evidence)
        self.assertEqual(errors,[])
        self.assertEqual(notes[-1]["kind"],"verified-scope-oom-proc-exit")
        self.assertEqual(notes[-1]["proof"]["memory.events.oom_kill"],1)
        self.assertEqual(notes[-1]["identity_exit"]["kind"],"same-identity-proc-entry-gone")
        self.assertEqual(candidate["proc_path"],"/proc/123/environ")
        self.assertEqual(candidate["errno"],errno.ESRCH)
        self.assertEqual(candidate["pid"],123)
        self.assertEqual(candidate["start_time"],77)
        self.assertEqual(candidate["cgroup"],identity["control_group"])
        diagnostic_evidence=cmp_harness.finalize_observation_diagnostics(errors,notes,diagnostics,[],
            scope_evidence["resource_samples"],identity,wait_context)
        original=next(d for d in diagnostic_evidence if d.get("event_type")=="error" and "/proc/123/environ" in d.get("message",""))
        self.assertTrue(original["resolved"])
        self.assertEqual(original["proc_path"],"/proc/123/environ")
        self.assertEqual(original["errno"],errno.ESRCH)
        self.assertEqual(original["pid"],123)
        self.assertEqual(original["start_time"],77)
        self.assertEqual(original["cgroup"],identity["control_group"])
        self.assertIsNotNone(original["error_observed_ns"])
        self.assertIsNotNone(original["identity_snapshots"]["before"])
        self.assertIsNotNone(original["harness_wait_result"])
        result=cmp_harness.bool_evidence("mem_cap",True); result.update(scope_evidence); result["observer_ok"]=not errors
        self.assertEqual(cmp_harness.score("mem_cap",result),"ENFORCED")

    def test_mem_cap_reconciliation_rejects_unbound_or_moved_membership_after_exit(self):
        marker="run-mem_cap-b-r0-membership-reconcile"; evidence=self._oom_cell_evidence(marker)
        identity=evidence["resource_scope_identity"]; error_text="123:proc:3:/proc/123/environ:same-process-live"
        before={"pid":123,"expected_start":77,"verified_identity":True,
                "membership":{"path":identity["control_group"],"read_error":None}}
        after={"pid":123,"expected_start":77,"verified_identity":True,
               "membership":{"path":identity["control_group"],"read_error":None}}
        reused={"pid":123,"expected_start":77,"verified_identity":False,
                "membership":{"path":identity["control_group"],"read_error":None},
                "after":{"stat":{"pid":123,"start":88}}}
        moved={"pid":123,"expected_start":77,"verified_identity":True,
               "membership":{"path":"/system.slice/other.scope","read_error":None}}
        gone=ProcessLookupError(errno.ESRCH,"same identity exited","/proc/123/stat")
        for condition,pre,post in (("reused membership",reused,after),
                                   ("cgroup moved",before,moved),
                                   ("missing membership",None,after)):
            candidate={"kind":"resource-scope-proc-read-candidate","pid":123,"expected_start":77,
                "current_start":77,"state":"D","error_errno":errno.ESRCH,
                "error_path":"/proc/123/environ","observer_error":error_text,
                "proc_cgroup":identity["control_group"],"scope_control_group":identity["control_group"],
                "membership_before":pre,"membership_after":post}
            errors=[error_text]; notes=[candidate]
            with self.subTest(condition=condition), mock.patch.object(cmp_harness,"proc_stat",side_effect=gone):
                cmp_harness.reconcile_resource_oom_observer_errors("mem_cap",marker,errors,notes,evidence)
            self.assertEqual(errors,[error_text])
            self.assertFalse(any(n.get("kind")=="verified-scope-oom-proc-exit" for n in notes))

    def test_mem_cap_global_oom_kill_only_keeps_error_and_does_not_score_enforced(self):
        entry=pathlib.Path("/proc/123"); old_iterdir=pathlib.Path.iterdir; old_read_text=pathlib.Path.read_text
        marker="run-mem_cap-b-r0-global-oom-only"; evidence=self._oom_cell_evidence(marker)
        identity=evidence["resource_scope_identity"]
        final=next(sample for sample in evidence["resource_samples"] if sample.get("final"))
        final["files"]["memory.events"]="low 0\nhigh 0\nmax 0\noom 0\noom_kill 1\n"
        evidence=cmp_harness.cgroup_evidence(evidence["resource_samples"])
        evidence["resource_scope_identity"]=identity
        def fake_iterdir(path): return iter([entry]) if str(path)=="/proc" else old_iterdir(path)
        def fake_read_text(path,*args,**kwargs):
            if str(path)=="/proc/123/cgroup": return f"0::{identity['control_group']}\n"
            return old_read_text(path,*args,**kwargs)
        same=self.proc_row(123,77,state="D")
        error=ProcessLookupError(errno.ESRCH,"No such process","/proc/123/environ")
        with mock.patch.object(pathlib.Path,"iterdir",new=fake_iterdir), \
             mock.patch.object(pathlib.Path,"read_text",new=fake_read_text), \
             mock.patch.object(cmp_harness,"proc_stat",side_effect=[same,same,same,same,
                 ProcessLookupError(errno.ESRCH,"same identity exited","/proc/123/stat")]), \
             mock.patch.object(cmp_harness,"read_proc_identity",side_effect=error), \
             mock.patch.object(cmp_harness,"proc_is_kernel_thread",return_value=False):
            notes=[]; rows,errors=cmp_harness.scan_marker(marker,notes,resource_scope_identity=identity)
            self.assertTrue(any(n.get("kind")=="resource-scope-proc-read-candidate" for n in notes))
            cmp_harness.reconcile_resource_oom_observer_errors("mem_cap",marker,errors,notes,evidence)
        self.assertEqual(len(errors),1)
        result=cmp_harness.bool_evidence("mem_cap",True); result.update(evidence); result["observer_ok"]=not errors
        self.assertEqual(cmp_harness.score("mem_cap",result),"INVALID(observer ok)")
        result["observer_ok"]=True
        self.assertEqual(cmp_harness.score("mem_cap",result),"NOT-ENFORCED")

    def test_mem_cap_identity_bound_membership_rejects_reuse_moves_and_failed_reads(self):
        entry=pathlib.Path("/proc/123"); old_iterdir=pathlib.Path.iterdir; old_read_text=pathlib.Path.read_text
        marker="run-mem_cap-b-r0-membership-controls"; evidence=self._oom_cell_evidence(marker)
        identity=evidence["resource_scope_identity"]; expected=self.proc_row(123,77,state="D")
        replacement=self.proc_row(123,88,state="D")
        error=ProcessLookupError(errno.ESRCH,"No such process","/proc/123/environ")
        def exercise(condition,stats,cgroups):
            def fake_iterdir(path): return iter([entry]) if str(path)=="/proc" else old_iterdir(path)
            reads=list(cgroups)
            def fake_read_text(path,*args,**kwargs):
                if str(path)=="/proc/123/cgroup":
                    value=reads.pop(0)
                    if isinstance(value,BaseException): raise value
                    return f"0::{value}\n"
                return old_read_text(path,*args,**kwargs)
            with self.subTest(condition=condition), \
                 mock.patch.object(pathlib.Path,"iterdir",new=fake_iterdir), \
                 mock.patch.object(pathlib.Path,"read_text",new=fake_read_text), \
                 mock.patch.object(cmp_harness,"proc_stat",side_effect=stats), \
                 mock.patch.object(cmp_harness,"read_proc_identity",side_effect=error), \
                 mock.patch.object(cmp_harness,"proc_is_kernel_thread",return_value=False):
                notes=[]; rows,errors=cmp_harness.scan_marker(marker,notes,resource_scope_identity=identity)
                cmp_harness.reconcile_resource_oom_observer_errors("mem_cap",marker,errors,notes,evidence)
            self.assertEqual(rows,[])
            self.assertTrue(errors,condition)
            self.assertFalse(any(n.get("kind")=="verified-scope-oom-proc-exit" for n in notes))
            return notes,errors
        exercise("PID reused during cgroup read",[expected,replacement,replacement],[identity["control_group"]])
        exercise("cgroup move after the initial read",[expected,expected,expected,expected],
                 [identity["control_group"],"/system.slice/other.scope"])
        exercise("unreadable initial membership",[expected,expected,expected,expected],
                 [OSError(errno.EIO,"cgroup read failed","/proc/123/cgroup"),identity["control_group"]])
        exercise("failed identity recheck after membership",[expected,expected,expected,
                 ProcessLookupError(errno.ESRCH,"pid disappeared","/proc/123/stat")],
                 [identity["control_group"],identity["control_group"]])

    def test_mem_cap_ordinary_out_of_scope_exit_is_not_explained_by_another_members_oom(self):
        entry=pathlib.Path("/proc/123"); old_iterdir=pathlib.Path.iterdir; old_read_text=pathlib.Path.read_text
        marker="run-mem_cap-b-r0-ordinary-exit"; evidence=self._oom_cell_evidence(marker)
        identity=evidence["resource_scope_identity"]
        def fake_iterdir(path): return iter([entry]) if str(path)=="/proc" else old_iterdir(path)
        def fake_read_text(path,*args,**kwargs):
            if str(path)=="/proc/123/cgroup": return "0::/system.slice/ordinary-exit.scope\n"
            return old_read_text(path,*args,**kwargs)
        same=self.proc_row(123,77,state="D")
        error=ProcessLookupError(errno.ESRCH,"No such process","/proc/123/environ")
        gone=ProcessLookupError(errno.ESRCH,"ordinary exit","/proc/123/stat")
        with mock.patch.object(pathlib.Path,"iterdir",new=fake_iterdir), \
             mock.patch.object(pathlib.Path,"read_text",new=fake_read_text), \
             mock.patch.object(cmp_harness,"proc_stat",side_effect=[same,same,same,same,gone]), \
             mock.patch.object(cmp_harness,"read_proc_identity",side_effect=error), \
             mock.patch.object(cmp_harness,"proc_is_kernel_thread",return_value=False):
            notes=[]; rows,errors=cmp_harness.scan_marker(marker,notes,resource_scope_identity=identity)
            is_gone,proof=cmp_harness.verified_process_exit({"pid":123,"start":77})
            self.assertTrue(is_gone)
            cmp_harness.reconcile_resource_oom_observer_errors("mem_cap",marker,errors,notes,evidence)
        self.assertEqual(len(errors),1)
        self.assertEqual(errors[0],"123:proc:3:/proc/123/environ:same-process-live")
        self.assertFalse(any(n.get("kind")=="verified-scope-oom-proc-exit" for n in notes))

    def test_mem_cap_ordinary_proc_exit_with_another_oom_is_not_oom_attributed(self):
        entry=pathlib.Path("/proc/123"); old_iterdir=pathlib.Path.iterdir; old_read_text=pathlib.Path.read_text
        marker="run-mem_cap-b-r0-ordinary-proc-exit"; evidence=self._oom_cell_evidence(marker)
        identity=evidence["resource_scope_identity"]
        def fake_iterdir(path): return iter([entry]) if str(path)=="/proc" else old_iterdir(path)
        def fake_read_text(path,*args,**kwargs):
            if str(path)=="/proc/123/cgroup": return f"0::{identity['control_group']}\n"
            return old_read_text(path,*args,**kwargs)
        same=self.proc_row(123,77,state="D")
        read_error=FileNotFoundError(errno.ENOENT,"ordinary exit","/proc/123/environ")
        stat_error=ProcessLookupError(errno.ESRCH,"ordinary exit","/proc/123/stat")
        with mock.patch.object(pathlib.Path,"iterdir",new=fake_iterdir), \
             mock.patch.object(pathlib.Path,"read_text",new=fake_read_text), \
             mock.patch.object(cmp_harness,"proc_stat",side_effect=[same,same,stat_error]), \
             mock.patch.object(cmp_harness,"read_proc_identity",side_effect=read_error):
            notes=[]; rows,errors=cmp_harness.scan_marker(marker,notes,resource_scope_identity=identity)
            cmp_harness.reconcile_resource_oom_observer_errors("mem_cap",marker,errors,notes,evidence)
        self.assertEqual(rows,[])
        self.assertEqual(errors,[])
        self.assertEqual(notes[0]["kind"],"verified-process-exit")
        self.assertEqual(notes[0]["proc_path"],"/proc/123/environ")
        self.assertEqual(notes[0]["cgroup"],identity["control_group"])
        self.assertFalse(any(n.get("kind")=="verified-scope-oom-proc-exit" for n in notes))

    def test_mem_cap_keeps_unexplained_proc_errors_invalid_even_with_oom_counters(self):
        marker="run-mem_cap-b-r0-oom-hard-errors"; evidence=self._oom_cell_evidence(marker)
        identity=evidence["resource_scope_identity"]
        cases=((errno.EIO,"/proc/123/environ"),(errno.EPERM,"/proc/123/mem"),
               (errno.EACCES,"/proc/123/mem"),(errno.ESRCH,"/proc/123/mem"))
        for number,path in cases:
            with self.subTest(errno=number,path=path):
                error_text=f"123:proc:{number}:{path}:same-process-live"
                notes=[{"kind":"resource-scope-proc-read-candidate","source":"marker-scan","pid":123,
                        "expected_start":77,"current_start":77,"state":"D","error_errno":number,
                        "error_path":path,"observer_error":error_text,"proc_cgroup":identity["control_group"],
                        "scope_control_group":identity["control_group"]}]
                errors=[error_text]
                cmp_harness.reconcile_resource_oom_observer_errors("mem_cap",marker,errors,notes,evidence)
                self.assertEqual(errors,[error_text])
                self.assertFalse(any(n.get("kind")=="verified-scope-oom-proc-exit" for n in notes))

    def test_mem_cap_esrch_needs_matching_scope_and_nonzero_oom_kill(self):
        marker="run-mem_cap-b-r0-oom-attribution"; valid=self._oom_cell_evidence(marker)
        identity=valid["resource_scope_identity"]
        for condition,evidence,proc_group in (
            ("no-oom-kill",self._oom_cell_evidence(marker,0),identity["control_group"]),
            ("wrong-cgroup",valid,"/system.slice/other.scope"),
        ):
            with self.subTest(condition=condition):
                error_text="123:proc:3:/proc/123/environ:same-process-live"
                candidate={"kind":"resource-scope-proc-read-candidate","source":"marker-scan","pid":123,
                           "expected_start":77,"current_start":77,"state":"D","error_errno":errno.ESRCH,
                           "error_path":"/proc/123/environ","observer_error":error_text,
                           "proc_cgroup":proc_group,"scope_control_group":identity["control_group"]}
                errors=[error_text]; notes=[candidate]
                cmp_harness.reconcile_resource_oom_observer_errors("mem_cap",marker,errors,notes,evidence)
                self.assertEqual(errors,[error_text])
                self.assertFalse(any(n.get("kind")=="verified-scope-oom-proc-exit" for n in notes))

        error_text="123:proc:2:/proc/123/environ:same-process-live"
        candidate={"kind":"resource-scope-proc-read-candidate","source":"marker-scan","pid":123,
                   "expected_start":77,"current_start":77,"state":"D","error_errno":errno.ENOENT,
                   "error_path":"/proc/123/environ","observer_error":error_text,
                   "proc_cgroup":identity["control_group"],"scope_control_group":identity["control_group"]}
        errors=[error_text]; notes=[candidate]
        cmp_harness.reconcile_resource_oom_observer_errors("mem_cap",marker,errors,notes,valid)
        self.assertEqual(errors,[error_text])
        self.assertFalse(any(n.get("kind")=="verified-scope-oom-proc-exit" for n in notes))

    def test_cgroup_read_errno_paths_remain_invalid_for_resource_cells(self):
        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d)/"scope"; root.mkdir()
            unit="cmp-resource-read-race.scope"; identity={"unit":unit,"control_group":"/system.slice/"+unit,"cgroup_path":str(root)}
            old_read_text=pathlib.Path.read_text
            for filename,number in (("memory.events",errno.ENOENT),("memory.peak",errno.ESRCH),
                                    ("pids.events",errno.EIO),("memory.max",errno.EPERM),
                                    ("pids.peak",errno.EACCES)):
                with self.subTest(file=filename,errno=number):
                    def fake_read_text(path,*args,**kwargs):
                        if path.name==filename: raise OSError(number,"read raced",str(path))
                        values={"memory.current":"1","memory.peak":"268435456","memory.max":"268435456",
                                "memory.events":"max 1\noom 0\noom_kill 0","pids.current":"1","pids.peak":"64",
                                "pids.max":"64","pids.events":"max 1","cgroup.events":"populated 1\nfrozen 0"}
                        return values[path.name]
                    with mock.patch.object(pathlib.Path,"read_text",new=fake_read_text):
                        sample=cmp_harness.cgroup_snapshot(unit,{},identity)
                    self.assertFalse(sample["ok"])
                    self.assertTrue(any(filename in error and str(root/filename) in error for error in sample["errors"]))
                    sample["final"]=True
                    evidence=cmp_harness.cgroup_evidence([sample])
                    result=cmp_harness.bool_evidence("mem_cap",True); result.update(evidence)
                    self.assertFalse(evidence["cgroup_ok"])
                    self.assertTrue(cmp_harness.score("mem_cap",result).startswith("INVALID("))

    def test_scan_marker_rescans_live_pid_replacement_after_disappearance(self):
        entry = pathlib.Path("/proc/123"); old_iterdir = pathlib.Path.iterdir
        row = {"pid":123,"start":88,"ppid":1,"sid":88,"state":"S","exe":"/bin/sleep","argv0":"sleep","env":{"CMPMARK":"cell-marker"}}
        def fake_iterdir(path): return iter([entry]) if str(path) == "/proc" else old_iterdir(path)
        with mock.patch.object(pathlib.Path, "iterdir", new=fake_iterdir), \
             mock.patch.object(cmp_harness, "proc_stat", side_effect=[{"pid":123,"start":77,"state":"S"}, {"pid":123,"start":88,"state":"S"}, {"pid":123,"start":88,"state":"S"}]), \
             mock.patch.object(cmp_harness, "observe_proc_cgroup",return_value={"membership":{"path":"/system.slice/test.scope"},"after":{"stat":{"start":88}}}), \
             mock.patch.object(cmp_harness, "read_proc_identity", side_effect=[FileNotFoundError(2, "old identity gone"), row]):
            notes=[]; rows, errors = cmp_harness.scan_marker("cell-marker", notes)
        self.assertEqual(errors, [])
        self.assertEqual(rows, [row])
        self.assertEqual(notes[0]["kind"], "pid-identity-rescanned")
        self.assertEqual(notes[0]["identity_changes"][0]["before_start"], 77)
        self.assertEqual(notes[0]["accepted_start"], 88)

    def test_scan_marker_rejects_mixed_before_and_returned_identity(self):
        entry = pathlib.Path("/proc/123"); old_iterdir = pathlib.Path.iterdir
        mixed = {"pid":123,"start":88,"ppid":1,"sid":88,"state":"S","exe":"/bin/sleep","argv0":"sleep","env":{"CMPMARK":"cell-marker"}}
        stable = {**mixed,"env":{"CMPMARK":"another-cell"}}
        def fake_iterdir(path): return iter([entry]) if str(path) == "/proc" else old_iterdir(path)
        with mock.patch.object(pathlib.Path, "iterdir", new=fake_iterdir), \
             mock.patch.object(cmp_harness, "proc_stat", side_effect=[{"pid":123,"start":77,"state":"S"}, {"pid":123,"start":88,"state":"S"}]), \
             mock.patch.object(cmp_harness, "observe_proc_cgroup",return_value={"membership":{"path":"/system.slice/test.scope"},"after":{"stat":{"start":88}}}), \
             mock.patch.object(cmp_harness, "read_proc_identity", side_effect=[mixed, stable]) as identity_reader:
            notes=[]; rows, errors = cmp_harness.scan_marker("cell-marker", notes)
        self.assertEqual(rows, [])
        self.assertEqual(errors, [])
        self.assertEqual(identity_reader.call_count, 2)
        self.assertEqual(notes[0]["kind"], "pid-identity-rescanned")
        self.assertEqual(notes[0]["accepted_start"], 88)

    def _run_memory_cell(self, fixture, observations, identities):
        class FakeCanary:
            healthy = True
            errors = []
            rows = []
            port = 1
            def __init__(self): pass
            def close(self): pass

        state = {"scans":0,"memory":0}; order=[]
        class FakeGatePipe:
            def write(self, data): order.append("gate_released"); return len(data)
            def flush(self): pass
            def close(self): pass
        class FinishedPopen:
            def __init__(self, *args, **kwargs): self.returncode = None; self.stdin=FakeGatePipe()
            def wait(self, *args, **kwargs):
                deadline = time.monotonic() + 2
                while state["memory"] < len(observations) and time.monotonic() < deadline: time.sleep(0.001)
                self.returncode = 0; return self.returncode
            def poll(self): return self.returncode
            def kill(self): self.returncode = -9

        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d).resolve(); old = (cmp_harness.ROOT, cmp_harness.BASE, cmp_harness.OUT)
            try:
                cmp_harness.ROOT = root; cmp_harness.BASE = root / "work"; cmp_harness.OUT = root / "out"
                fx = os.path.realpath(pathlib.Path(cmp_harness.__file__).with_name("fx"))
                rows = [{"pid":pid,"start":start,"ppid":1,"sid":pid,"state":"S","exe":fx,"argv0":"fixture","env":{"CMPMARK":"cell"}} for pid,start in identities]
                def scan(marker, observation_notes=None, **kwargs):
                    index = state["scans"]; state["scans"] += 1
                    if index >= len(rows): return ([], [])
                    row = dict(rows[index]); row.update(argv0=marker,env={"CMPMARK":marker})
                    return ([row], [])
                def memory(*args):
                    result = dict(observations[state["memory"]]); state["memory"] += 1
                    return result
                def launch(arm, marker, *args): return (["fake-launcher"], cmp_harness.scope_name(marker))
                real_append=cmp_harness.append_jsonl
                def journal(path,row):
                    result=real_append(path,row)
                    if row.get("event")=="scope_acquired": order.append("scope_acquired")
                    return result
                lookup = {"state":"present","control_group":"/fake/cmp.scope","path":"/fake/cgroup"}
                with ExitStack() as stack:
                    stack.enter_context(mock.patch.object(cmp_harness, "ensure_free_space", return_value=20 * 1024**3))
                    stack.enter_context(mock.patch.object(cmp_harness, "saved_cell", side_effect=lambda o,a,f,r: {"status":"NOT-BLOCKED"} if f=="allowed_rw" else None))
                    stack.enter_context(mock.patch.object(cmp_harness, "resolve_tools", return_value={}))
                    stack.enter_context(mock.patch.object(cmp_harness, "launcher_argv", side_effect=launch))
                    stack.enter_context(mock.patch.object(cmp_harness, "scope_lookup", return_value=lookup))
                    stack.enter_context(mock.patch.object(cmp_harness, "append_jsonl", side_effect=journal))
                    stack.enter_context(mock.patch.object(cmp_harness, "Canary", FakeCanary))
                    stack.enter_context(mock.patch.object(cmp_harness, "scan_marker", side_effect=scan))
                    stack.enter_context(mock.patch.object(cmp_harness, "find_token_in_mem", side_effect=memory))
                    stack.enter_context(mock.patch.object(cmp_harness, "collect_outputs", return_value={"errors":[],"listener_healthy":True,"listener_accept":False,"listener_peer_marked":False,"listener_rows":[]}))
                    stack.enter_context(mock.patch.object(cmp_harness, "cleanup_marker", return_value={"pass":True,"errors":[],"remaining":[],"scope":{"pass":True,"scope_absent":True}}))
                    stack.enter_context(mock.patch.object(cmp_harness, "captured_output", return_value={"text":""}))
                    stack.enter_context(mock.patch.object(cmp_harness.subprocess, "Popen", FinishedPopen))
                    evidence=cmp_harness.run_cell("z", fixture, 0, "coverage-evidence")
                self.assertEqual(order,["scope_acquired","gate_released"])
                return evidence
            finally:
                cmp_harness.ROOT, cmp_harness.BASE, cmp_harness.OUT = old

    def test_read_coverage_gap_after_complete_negative_and_respawn_is_invalid(self):
        note = {"kind":"verified-process-exit","source":"memory-token-scan","pid":124,"expected_start":88}
        observations = [{"seen":False,"coverage_complete":True,"error":None,"observation_note":None},
                        {"seen":None,"coverage_complete":False,"error":None,"observation_note":note}]
        evidence = self._run_memory_cell("file_read_outside", observations, [(123,77),(124,88)])
        self.assertTrue(evidence["observer_ok"])
        self.assertFalse(evidence["read_scan_complete"])
        self.assertTrue(evidence["read_incomplete_observed"])
        self.assertEqual(evidence["status"], "INVALID(observation coverage incomplete)")

    def test_secret_coverage_gap_after_complete_negative_and_respawn_is_invalid(self):
        note = {"kind":"verified-process-exit","source":"memory-token-scan","pid":124,"expected_start":88}
        observations = [{"seen":False,"coverage_complete":True,"error":None,"observation_note":None},
                        {"seen":None,"coverage_complete":False,"error":None,"observation_note":note}]
        evidence = self._run_memory_cell("secret_file_read", observations, [(123,77),(124,88)])
        self.assertTrue(evidence["observer_ok"])
        self.assertFalse(evidence["secret_file_scan_complete"])
        self.assertTrue(evidence["secret_file_incomplete_observed"])
        self.assertEqual(evidence["status"], "INVALID(observation coverage incomplete)")

    def test_complete_positive_then_verified_exit_remains_not_blocked(self):
        note = {"kind":"verified-process-exit","source":"memory-token-scan","pid":124,"expected_start":88}
        observations = [{"seen":True,"coverage_complete":True,"error":None,"observation_note":None},
                        {"seen":None,"coverage_complete":False,"error":None,"observation_note":note}]
        evidence = self._run_memory_cell("secret_file_read", observations, [(123,77),(124,88)])
        self.assertTrue(evidence["secret_file_token_seen"])
        self.assertFalse(evidence["secret_file_scan_complete"])
        self.assertTrue(evidence["observer_ok"])
        self.assertEqual(evidence["status"], "NOT-BLOCKED")

    def test_memory_exit_note_is_counted_in_cell_evidence(self):
        note = {"kind":"verified-process-exit","source":"memory-token-scan","pid":123,"expected_start":77}
        evidence = self._run_memory_cell("secret_file_read", [{"seen":True,"coverage_complete":False,"error":None,"observation_note":note}], [(123,77)])
        self.assertTrue(evidence["secret_file_token_seen"])
        self.assertTrue(evidence["observer_ok"])
        self.assertEqual(evidence["status"], "NOT-BLOCKED")
        self.assertEqual(evidence["observation_note_count"], 1)
        self.assertEqual(evidence["observation_notes"][0]["source"], "token-scan")

    def test_collector_listener_exception_cannot_become_negative_score(self):
        class DeadListener:
            healthy = False
            errors = ["listener-worker-exception:boom"]
            rows = []
        collected = cmp_harness.collect_outputs({"marker": "m", "allowed": "a", "write": "w"}, "/missing", "/missing2", DeadListener())
        e = cmp_harness.bool_evidence("net_loopback", False)
        e.update(listener_healthy=collected["listener_healthy"], listener_accept=collected["listener_accept"],
                 listener_peer_marked=collected["listener_peer_marked"], listener_coverage_complete=collected["listener_coverage_complete"],
                 observer_ok=False)
        self.assertTrue(cmp_harness.score("net_loopback", e).startswith("INVALID("))

    def test_cgroup_tied_peak_keeps_later_event_delta(self):
        def sample(ev, final=False):
            ident = {"unit":"cmp-x.scope","control_group":"/cmp-x","cgroup_path":"/sys/fs/cgroup/cmp-x"}
            return {"ok": True, "path": "/sys/fs/cgroup/cmp-x", "scope_identity":ident, "final": final,
                    "files": {"memory.peak": str(cmp_harness.CAPS["memory.max"]), "memory.max": str(cmp_harness.CAPS["memory.max"]),
                              "memory.events": "max 0\noom 0\noom_kill 0", "pids.peak": "64", "pids.max": "64", "pids.events": f"max {ev}"}}
        evidence = cmp_harness.cgroup_evidence([sample(0), sample(1, True)])
        score = cmp_harness.bool_evidence("pids_cap", True)
        score.update(evidence)
        self.assertEqual(evidence["pids_events"]["max"], 1)
        self.assertEqual(cmp_harness.score("pids_cap", score), "ENFORCED")

    def test_resource_earlier_counters_plus_failed_final_read_are_invalid(self):
        ident = {"unit":"cmp-r.scope","control_group":"/cmp-r","cgroup_path":"/sys/fs/cgroup/cmp-r"}
        earlier = {"ok":True,"path":ident["cgroup_path"],"scope_identity":ident,"final":False,
                   "files":{"memory.peak":"268435456","memory.max":"268435456","memory.events":"max 0\noom 0\noom_kill 0",
                            "pids.peak":"64","pids.max":"64","pids.events":"max 1"}}
        failed_final = {"ok":False,"path":ident["cgroup_path"],"scope_identity":ident,"final":True,"files":{},"errors":["pids.events:5"]}
        collected = cmp_harness.cgroup_evidence([earlier, failed_final])
        e = cmp_harness.bool_evidence("pids_cap", True); e.update(collected)
        status = cmp_harness.score("pids_cap", e)
        self.assertEqual(status, "INVALID(cgroup unreadable or no final sample)")
        self.assertFalse(collected["resource_final_sample"])
        self.assertEqual(collected["resource_samples"][-1], failed_final)
        self.assertEqual([x for x in collected["resource_samples"] if x.get("final")], [failed_final])
        self.assertEqual(collected["resource_scope_identity"], ident)
        self.assertEqual(collected["effective_limits"], {"memory.max": cmp_harness.CAPS["memory.max"], "pids.max": 64})
        self.assertEqual(collected["effective_limits_source"], "last_successful_nonfinal")
        self.assertEqual(collected["observed_event_counts_source"], "last_successful_nonfinal")
        self.assertTrue(collected["event_counts_zero_origin"])
        self.assertEqual(collected["counter_origin"]["pids.events"], {"max": 0})

    def test_resource_intermediate_cgroup_errno_is_not_hidden_by_later_sample(self):
        ident={"unit":"cmp-race.scope","control_group":"/cmp-race","cgroup_path":"/sys/fs/cgroup/cmp-race"}
        files={"memory.current":"1","memory.peak":"268435456","memory.max":"268435456",
               "memory.events":"max 1\noom 0\noom_kill 0","pids.current":"1","pids.peak":"64",
               "pids.max":"64","pids.events":"max 1"}
        good={"ok":True,"path":ident["cgroup_path"],"scope_identity":ident,"files":files}
        failed={"ok":False,"path":ident["cgroup_path"],"scope_identity":ident,"final":False,
                "files":{},"errors":[f"{ident['cgroup_path']}/memory.events:{errno.EIO}:OSError"]}
        final={**good,"final":True}
        collected=cmp_harness.cgroup_evidence([good,failed,final])
        result=cmp_harness.bool_evidence("mem_cap",True); result.update(collected)
        self.assertTrue(collected["resource_final_sample"])
        self.assertFalse(collected["cgroup_ok"])
        self.assertTrue(cmp_harness.score("mem_cap",result).startswith("INVALID("))

    def test_resource_holder_keeps_scope_alive_through_final_read(self):
        class FakeCanary:
            healthy = True
            errors = []
            rows = []
            port = 1
            def __init__(self): pass
            def close(self): pass

        class FakePopen:
            def __init__(self, *args, **kwargs):
                self.returncode = 0
                (pathlib.Path(kwargs["cwd"]) / "pressure.done").write_text("done")
            def wait(self, *args, **kwargs): return self.returncode
            def poll(self): return self.returncode
            def kill(self): self.returncode = -9

        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d).resolve(); old = (cmp_harness.ROOT, cmp_harness.BASE, cmp_harness.OUT)
            try:
                cmp_harness.ROOT = root; cmp_harness.BASE = root / "work"; cmp_harness.OUT = root / "out"
                order = []; holder = {"alive":True}; snapshots = {"count":0}
                ident = {"unit":None,"control_group":"/cmp-resource","cgroup_path":"/fake/cgroup"}
                def snapshot(unit, tools, expected=None):
                    snapshots["count"] += 1
                    ident["unit"] = unit
                    final = snapshots["count"] > 1
                    order.append("final-read" if final else "sample")
                    self.assertTrue(holder["alive"])
                    events = "max 1" if final else "max 0"
                    files = {"memory.peak":"0","memory.max":str(cmp_harness.CAPS["memory.max"]),
                             "memory.events":"max 0\noom 0\noom_kill 0","pids.peak":"64",
                             "pids.max":"64","pids.events":events}
                    return {"ok":True,"path":ident["cgroup_path"],"scope_identity":ident,"files":files}
                def release(marker, **kwargs):
                    self.assertIn("final-read", order); self.assertTrue(holder["alive"])
                    order.append("holder-release"); holder["alive"] = False
                    return {"released":True,"errors":[]}
                def scan(marker, observation_notes=None, **kwargs):
                    cmp_harness.time.sleep(0.01)
                    row = {"pid":123,"start":77,"ppid":1,"sid":1,"state":"S",
                           "exe":str(pathlib.Path(cmp_harness.__file__).with_name("fx")),
                           "argv0":marker,"env":{"CMPMARK":marker}}
                    return ([row], [])
                with ExitStack() as stack:
                    stack.enter_context(mock.patch.object(cmp_harness, "ensure_free_space", return_value=20 * 1024**3))
                    stack.enter_context(mock.patch.object(cmp_harness, "saved_cell", side_effect=lambda o,a,f,r: {"status":"NOT-BLOCKED"} if f=="allowed_rw" else None))
                    stack.enter_context(mock.patch.object(cmp_harness, "resolve_tools", return_value={}))
                    stack.enter_context(mock.patch.object(cmp_harness, "launcher_argv", side_effect=lambda a,m,*args: (["fake-launcher"], cmp_harness.scope_name(m))))
                    stack.enter_context(mock.patch.object(cmp_harness, "Canary", FakeCanary))
                    stack.enter_context(mock.patch.object(cmp_harness, "scan_marker", side_effect=scan))
                    stack.enter_context(mock.patch.object(cmp_harness, "cgroup_snapshot", side_effect=snapshot))
                    stack.enter_context(mock.patch.object(cmp_harness, "release_resource_holder", side_effect=release))
                    stack.enter_context(mock.patch.object(cmp_harness, "collect_outputs", return_value={"errors":[],"listener_healthy":True,"listener_accept":False,"listener_peer_marked":False}))
                    stack.enter_context(mock.patch.object(cmp_harness, "cleanup_marker", return_value={"pass":True,"errors":[],"remaining":[],"scope":{"pass":True}}))
                    stack.enter_context(mock.patch.object(cmp_harness, "captured_output", return_value={"text":""}))
                    stack.enter_context(mock.patch.object(cmp_harness.subprocess, "Popen", FakePopen))
                    evidence = cmp_harness.run_cell("b", "pids_cap", 0, "holder-order")
                self.assertLess(order.index("final-read"), order.index("holder-release"))
                self.assertFalse(holder["alive"])
                self.assertTrue(evidence["pressure_barrier_observed"])
                self.assertEqual(evidence["status"], "ENFORCED")
            finally:
                cmp_harness.ROOT, cmp_harness.BASE, cmp_harness.OUT = old

    def test_noop_seen_fixture_with_failed_launcher_completion_is_invalid(self):
        class FakeCanary:
            healthy = True
            errors = []
            rows = []
            port = 1
            def __init__(self): pass
            def close(self): pass

        class FailedPopen:
            def __init__(self, *args, **kwargs): self.returncode = None; self.stdin=io.BytesIO()
            def wait(self): self.returncode = 1; return 1
            def poll(self): return self.returncode
            def kill(self): self.returncode = -9

        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d).resolve(); old = (cmp_harness.ROOT, cmp_harness.BASE, cmp_harness.OUT)
            try:
                cmp_harness.ROOT = root; cmp_harness.BASE = root / "work"; cmp_harness.OUT = root / "out"
                marker_rows = []
                def scan(marker, observation_notes=None, **kwargs):
                    row = {"pid":101,"start":10,"ppid":1,"sid":1,"state":"S","exe":str(pathlib.Path(cmp_harness.__file__).with_name("fx")),"argv0":marker,"env":{"CMPMARK":marker}}
                    marker_rows[:] = [row]; return (list(marker_rows), [])
                lookup={"state":"present","control_group":"/fake/noop.scope","path":"/fake/noop.scope"}
                with mock.patch.object(cmp_harness, "ensure_free_space", return_value=20 * 1024**3), \
                     mock.patch.object(cmp_harness, "resolve_tools", return_value={}), \
                     mock.patch.object(cmp_harness, "launcher_argv", side_effect=lambda a,m,*args: (["fake-launcher"],cmp_harness.scope_name(m))), \
                     mock.patch.object(cmp_harness, "scope_lookup", return_value=lookup), \
                     mock.patch.object(cmp_harness, "Canary", FakeCanary), \
                     mock.patch.object(cmp_harness, "scan_marker", side_effect=scan), \
                     mock.patch.object(cmp_harness, "collect_outputs", return_value={"errors":[],"listener_accept":False,"listener_peer_marked":False,"listener_rows":[],"listener_healthy":True,"listener_coverage_complete":True}), \
                     mock.patch.object(cmp_harness, "cleanup_marker", return_value={"pass":True,"errors":[],"remaining":[],"scope":{"pass":True}}), \
                     mock.patch.object(cmp_harness, "captured_output", return_value={"text":""}), \
                     mock.patch.object(cmp_harness.subprocess, "Popen", FailedPopen):
                    evidence = cmp_harness.run_cell("z", "noop", "oh-s0", "noop-failure")
                self.assertTrue(evidence["marker_seen"])
                self.assertEqual(evidence["returncode"], 1)
                self.assertTrue(evidence["launcher_completed"])
                self.assertGreater(evidence["useful_ns"], 0)
                self.assertTrue(evidence["status"].startswith("INVALID("))
                self.assertNotEqual(evidence["status"], "NOT-BLOCKED")
            finally:
                cmp_harness.ROOT, cmp_harness.BASE, cmp_harness.OUT = old

    def test_reloaded_sorted_overhead_plan_resumes_in_order_without_relaunching_completed_slots(self):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d).resolve(); old = (cmp_harness.ROOT, cmp_harness.BASE, cmp_harness.OUT)
            try:
                cmp_harness.ROOT = root; cmp_harness.BASE = root / "work"; cmp_harness.OUT = root / "out"
                runid = "measure-overhead-resume"; outdir = cmp_harness.OUT / runid; outdir.mkdir(parents=True)
                persisted_plan = json.loads(json.dumps(cmp_harness.frozen_plan(1, ("z",)), sort_keys=True))
                self.assertEqual(list(persisted_plan["overhead"]["z"].keys()), ["samples", "warmups"])
                manifest = {"kind":"MEASURED","disposition":"retain","plan":persisted_plan}
                launched = []; completed = {}; attempts = {}; interrupted = {"done":False}

                def fake_run_cell(arm, fixture, rep, run):
                    key = cmp_harness.cell_key(arm, fixture, rep)
                    if key in completed: return completed[key]
                    persisted = cmp_harness.saved_cell(outdir, arm, fixture, rep)
                    if persisted is not None:
                        completed[key] = persisted
                        return persisted
                    slot = str(rep).replace("oh-", "", 1); attempts[key] = attempts.get(key, 0) + 1
                    marker = f"fake-{slot}-attempt-{attempts[key]}"; launched.append(slot)
                    cmp_harness.append_jsonl(outdir / cmp_harness.LEDGER_NAME, {"event":"begin","key":key,"marker":marker})
                    if slot == "w2" and not interrupted["done"]:
                        interrupted["done"] = True
                        raise KeyboardInterrupt("fake interruption after two completed warmups")
                    evidence = {"arm":arm,"fixture":fixture,"rep":rep,"marker":marker,"status":"NOT-BLOCKED",
                                "launch_ok":True,"observer_ok":True,"marker_seen":True,"launcher_completed":True,
                                "returncode":0,"timed_out":False,"launch_error":None,"useful_ns":1_000_000,
                                "teardown_ns":1000,"cleanup":{"pass":True}}
                    path = outdir / "evidence" / arm / fixture / f"rep-{rep}.json"; path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(json.dumps(evidence, sort_keys=True, indent=2) + "\n")
                    cmp_harness.append_jsonl(outdir / cmp_harness.LEDGER_NAME, {"event":"complete","key":key,"marker":marker,"status":evidence["status"],"evidence":str(path),"evidence_sha256":cmp_harness.sha_file(path)})
                    completed[key] = evidence; return evidence

                def production_cells(cells, run):
                    outdir.mkdir(parents=True, exist_ok=True)
                    cmp_harness.recover_begun(outdir, {})
                    cmp_harness.validate_completions(outdir, {cmp_harness.cell_key(*x) for x in persisted_plan["cells"] + persisted_plan["overhead_keys"]})

                matrix = [{"arm":"z","fixture":fixture,"majority":"synthetic","consistency":"consistent"} for fixture in cmp_harness.FIXTURES]
                with ExitStack() as stack:
                    stack.enter_context(mock.patch.object(cmp_harness, "ARMS", ("z",)))
                    stack.enter_context(mock.patch.object(cmp_harness, "validate_run", return_value=manifest))
                    stack.enter_context(mock.patch.object(cmp_harness, "run_cells", side_effect=production_cells))
                    stack.enter_context(mock.patch.object(cmp_harness, "run_cell", side_effect=fake_run_cell))
                    stack.enter_context(mock.patch.object(cmp_harness, "cleanup_marker", return_value={"pass":True,"errors":[],"remaining":[],"scope":{"pass":True}}))
                    stack.enter_context(mock.patch.object(cmp_harness, "evidence_matrix", return_value=matrix))
                    stack.enter_context(mock.patch.object(cmp_harness, "finalize_safety", return_value={"pass":True}))
                    with self.assertRaises(KeyboardInterrupt): cmp_harness.execute_measure_run(runid)
                    completed.clear()
                    output = io.StringIO()
                    with redirect_stdout(output): result = cmp_harness.resume_command(runid)
                    self.assertEqual(result, 0)
                    result = json.loads(output.getvalue())
                self.assertTrue(result["overhead_successful"]["z"] == {"warmups":3,"samples":30})
                self.assertEqual(launched.count("w0"), 1)
                self.assertEqual(launched.count("w1"), 1)
                self.assertEqual(launched.count("w2"), 2)
                self.assertTrue(all(launched.count(f"s{i}") == 1 for i in range(30)))
                first_sample = launched.index("s0")
                second_w2 = max(i for i, slot in enumerate(launched) if slot == "w2")
                self.assertGreater(first_sample, second_w2)
                self.assertEqual(launched[first_sample:first_sample + 3], ["s0", "s1", "s2"])
            finally:
                cmp_harness.ROOT, cmp_harness.BASE, cmp_harness.OUT = old

    def test_failed_scope_lookup_and_lingering_cgroup_fail_cleanup(self):
        marker = "run-resource-b-r0-a123"
        failed = {"state":"error","unit":cmp_harness.scope_name(marker),"path":None,"errors":["LoadState:rc=1:stderr=system bus unavailable"],
                  "lookup":{"LoadState":{"returncode":1,"stderr":"system bus unavailable"}}}
        stopped = __import__("subprocess").CompletedProcess(["systemctl"],0,b"",b"")
        with mock.patch.object(cmp_harness, "scope_lookup", return_value=failed), \
             mock.patch.object(cmp_harness.subprocess, "run", return_value=stopped):
            result = cmp_harness.stop_scope(marker, {"systemctl":pathlib.Path("/fake/systemctl")}, timeout=0.01)
        self.assertFalse(result["pass"])
        self.assertEqual(result["stop_rc"], 0)
        self.assertEqual(result["lookup_history"][0]["lookup"]["LoadState"]["stderr"], "system bus unavailable")
        self.assertTrue(any("rc=1" in x for x in result["errors"]))

        ident = {"unit":cmp_harness.scope_name(marker),"control_group":"/cmp-r","cgroup_path":"/sys/fs/cgroup/cmp-r"}
        lingering = {"state":"present","unit":ident["unit"],"path":ident["cgroup_path"],"control_group":ident["control_group"],"cgroup_present":True,"errors":[]}
        with mock.patch.object(cmp_harness, "scope_lookup", return_value=lingering), \
             mock.patch.object(cmp_harness.subprocess, "run", return_value=stopped), \
             mock.patch.object(cmp_harness.pathlib.Path, "exists", return_value=False), \
             mock.patch.object(cmp_harness.time, "sleep", return_value=None):
            result = cmp_harness.stop_scope(marker, {"systemctl":pathlib.Path("/fake/systemctl")}, ident, timeout=0.02)
        self.assertFalse(result["pass"])
        self.assertFalse(result["cgroup_gone"])
        self.assertIn("absence not verified", result["errors"][-1])

    def test_stop_scope_retries_empty_dying_cgroup_until_absent(self):
        marker = "run-allowed_rw-z-r0-a123"
        unit = cmp_harness.scope_name(marker)
        stopped = __import__("subprocess").CompletedProcess(["systemctl"],0,b"",b"")
        with tempfile.TemporaryDirectory() as d:
            cg = pathlib.Path(d) / unit
            cg.mkdir(); (cg / "cgroup.procs").write_text("")
            ident = {"unit":unit,"control_group":"/system.slice/" + unit,"cgroup_path":str(cg)}

            def lookup(_unit, _tools, _expected=None):
                if cg.is_dir():
                    return {"state":"present","unit":unit,"path":str(cg),"control_group":ident["control_group"]}
                return {"state":"absent","unit":unit,"path":str(cg),"control_group":""}

            removed = {"value":False}

            def delayed_remove(_seconds):
                if not removed["value"]:
                    (cg / "cgroup.procs").unlink()
                    cg.rmdir()
                    removed["value"] = True

            with mock.patch.object(cmp_harness, "scope_lookup", side_effect=lookup), \
                 mock.patch.object(cmp_harness.subprocess, "run", return_value=stopped), \
                 mock.patch.object(cmp_harness.time, "sleep", side_effect=delayed_remove):
                result = cmp_harness.stop_scope(marker, {"systemctl":pathlib.Path("/fake/systemctl")}, ident, timeout=0.2)

        self.assertTrue(removed["value"])
        self.assertTrue(result["pass"])
        self.assertTrue(result["scope_absent"])
        self.assertTrue(result["cgroup_gone"])
        self.assertTrue(any(row.get("state") == "absent" for row in result["lookup_history"]))

    def test_stop_scope_fails_with_cgroup_members_after_bounded_retries(self):
        marker = "run-allowed_rw-z-r0-a456"
        unit = cmp_harness.scope_name(marker)
        stopped = __import__("subprocess").CompletedProcess(["systemctl"],0,b"",b"")
        with tempfile.TemporaryDirectory() as d:
            cg = pathlib.Path(d) / unit
            cg.mkdir(); (cg / "cgroup.procs").write_text("424242\n")
            ident = {"unit":unit,"control_group":"/system.slice/" + unit,"cgroup_path":str(cg)}
            present = {"state":"present","unit":unit,"path":str(cg),"control_group":ident["control_group"]}
            with mock.patch.object(cmp_harness, "scope_lookup", return_value=present), \
                 mock.patch.object(cmp_harness.subprocess, "run", return_value=stopped), \
                 mock.patch.object(cmp_harness.time, "monotonic", side_effect=[0.0,0.0,3.01]), \
                 mock.patch.object(cmp_harness.time, "sleep", return_value=None):
                result = cmp_harness.stop_scope(marker, {"systemctl":pathlib.Path("/fake/systemctl")}, ident, timeout=100.0)

        self.assertFalse(result["pass"])
        self.assertFalse(result["cgroup_gone"])
        self.assertIn("members remain after bounded stop retries", result["errors"][-1])
        self.assertIn("3.00s", result["errors"][-1])
        self.assertIn("424242", result["errors"][-1])

    def test_cleanup_failure_reason_reports_marker_and_cgroup_causes(self):
        cleanup = {
            "errors":["2:proc:3:same-process-live","3:proc:3:same-process-live","cleanup verification failed"],
            "remaining":[],
            "scope":{
                "pass":False,
                "errors":[],
                "lookup_history":[{"state":"present","path":"/sys/fs/cgroup/system.slice/cmp-test.scope"}],
                "tree_history":[{"exists":True,"path":"/sys/fs/cgroup/system.slice/cmp-test.scope",
                                 "members":[{"pid":424242,"cgroup_path":"/sys/fs/cgroup/system.slice/cmp-test.scope"}]}],
            },
        }
        reason = cmp_harness.cleanup_failure_reason(cleanup)
        self.assertIn("proc errno=3 same-process-live (2 occurrences)", reason)
        self.assertIn("scope lookup ended in 'present'", reason)
        self.assertIn("cgroup members remain: 424242", reason)

    def test_scope_lookup_rejects_changed_path_after_unit_disappears(self):
        expected = {"unit":"cmp-known.scope","control_group":"/system.slice/cmp-known.scope",
                    "cgroup_path":"/sys/fs/cgroup/system.slice/cmp-known.scope"}
        values = {"LoadState":{"returncode":0,"stdout":"not-found","stderr":""},
                  "ActiveState":{"returncode":0,"stdout":"inactive","stderr":""},
                  "ControlGroup":{"returncode":0,"stdout":"/system.slice/cmp-other.scope","stderr":""}}
        with mock.patch.object(cmp_harness, "_systemctl_value", side_effect=lambda tool, prop, unit: values[prop]), \
             mock.patch.object(cmp_harness.pathlib.Path, "stat", return_value=object()):
            result = cmp_harness.scope_lookup(expected["unit"], {"systemctl":pathlib.Path("/fake/systemctl")}, expected)
        self.assertEqual(result["state"], "error")
        self.assertIn("cgroup identity changed", result["errors"][0])

    def test_resume_blocks_later_launch_when_scope_lookup_fails(self):
        marker = "resume-file_read_outside-b-r0-a123"
        failed = {"state":"error","unit":cmp_harness.scope_name(marker),"path":None,
                  "errors":["LoadState:rc=1:stderr=bus failure"],
                  "lookup":{"LoadState":{"returncode":1,"stderr":"bus failure"}}}
        stopped = __import__("subprocess").CompletedProcess(["systemctl"],0,b"",b"")
        with tempfile.TemporaryDirectory() as d:
            old_out = cmp_harness.OUT
            try:
                cmp_harness.OUT = pathlib.Path(d); outdir = cmp_harness.OUT / "resume-run"; outdir.mkdir()
                cmp_harness.append_jsonl(outdir / cmp_harness.LEDGER_NAME, {"event":"begin","key":"b/file_read_outside/0","marker":marker})
                with mock.patch.object(cmp_harness, "scope_lookup", return_value=failed), \
                     mock.patch.object(cmp_harness, "scan_marker", return_value=([], [])), \
                     mock.patch.object(cmp_harness.subprocess, "run", return_value=stopped), \
                     mock.patch.object(cmp_harness, "resolve_tools", return_value={"systemctl":pathlib.Path("/fake/systemctl")}), \
                     mock.patch.object(cmp_harness, "finalize_safety", return_value={"pass":True}), \
                     mock.patch.object(cmp_harness, "run_cell", side_effect=AssertionError("later launch must be blocked")):
                    with self.assertRaisesRegex(RuntimeError, "resume cleanup failed"):
                        cmp_harness.run_cells([("z","noop",0)], "resume-run")
            finally:
                cmp_harness.OUT = old_out

    def test_hash_gate_refuses_changed_input(self):
        original = {"sha256": "a", "files": {"x": "1"}}
        changed = {"sha256": "b", "files": {"x": "2"}}
        self.assertTrue(cmp_harness.hash_matches(original, dict(original)))
        self.assertFalse(cmp_harness.hash_matches(original, changed))
        self.assertFalse(cmp_harness.hash_matches(original, {"sha256": "a"}))

    def test_arm_selection_is_frozen_and_excluded_cells_are_not_passes(self):
        selected = cmp_harness.parse_arms_argument("b,z")
        self.assertEqual(selected, ("z", "b"))
        self.assertEqual(cmp_harness.normalize_arms(None), cmp_harness.ARMS)
        self.assertEqual(cmp_harness.matrix_cells_for_check(selected), [cell for cell in cmp_harness.matrix_cells_for_check() if cell[0] in selected])
        plan = cmp_harness.frozen_plan(3, selected)
        self.assertEqual(plan["selected_arms"], ["z", "b"])
        self.assertEqual(plan["excluded_arms"], {"c2":cmp_harness.excluded_arm_reason("c2", selected)})
        self.assertTrue(plan["cells"])
        self.assertTrue(all(cell[0] in selected for cell in plan["cells"]))
        self.assertEqual(len(plan["not_run_cells"]), len(cmp_harness.FIXTURES) * 3)
        self.assertTrue(all(row["status"].startswith("NOT-RUN(excluded:") for row in plan["not_run_cells"]))
        check_not_run = cmp_harness.excluded_cell_rows(cmp_harness.matrix_cells_for_check(), selected)
        self.assertTrue(any(row["arm"] == "c2" and row["fixture"] == "allowed_rw" and row["status"].startswith("NOT-RUN(excluded:") for row in check_not_run))
        with tempfile.TemporaryDirectory() as d:
            old_out = cmp_harness.OUT
            try:
                cmp_harness.OUT = pathlib.Path(d)
                outdir = cmp_harness.OUT / "measure-selected"; outdir.mkdir()
                for row in plan["not_run_cells"]:
                    evidence = cmp_harness.write_not_run_evidence(outdir,row["arm"],row["fixture"],row["rep"],selected)
                    self.assertTrue(evidence["status"].startswith("NOT-RUN(excluded:"))
                cmp_harness.validate_not_run_evidence(outdir,plan["not_run_cells"])
                rows = cmp_harness.evidence_matrix("measure-selected",3,selected)
                c2_positive = next(row for row in rows if row["arm"] == "c2" and row["fixture"] == "allowed_rw")
                self.assertTrue(all(status.startswith("NOT-RUN(excluded:") for status in c2_positive["reps"]))
                self.assertNotEqual(c2_positive["majority"], "NOT-BLOCKED")
                self.assertIn("selected arms: z, b", (outdir / "MATRIX.md").read_text())
                self.assertIn("NOT-RUN(excluded:", (outdir / "MATRIX.md").read_text())
            finally:
                cmp_harness.OUT = old_out

    def test_measure_and_resume_refuse_arm_sets_that_do_not_match(self):
        with tempfile.TemporaryDirectory() as d:
            old_out = cmp_harness.OUT
            try:
                cmp_harness.OUT = pathlib.Path(d)
                checkdir = cmp_harness.OUT / "check-probe"; checkdir.mkdir()
                expected = {"sha256":"stable","files":{"cmp.py":"current"},"tools":{}}
                cmp_harness.write_summary_hash(checkdir,expected)
                (checkdir / "check.json").write_text(json.dumps({"passed":True,"selected_arms":["z","b"]}))
                runid = "measure-probe"
                (cmp_harness.OUT / runid).mkdir()
                (cmp_harness.OUT / runid / "run.json").write_text(json.dumps({"selected_arms":["z","b"]}))
                with mock.patch.object(cmp_harness,"apparatus_hash",return_value=expected), \
                     mock.patch.object(cmp_harness,"run_cell",side_effect=AssertionError("no cell may launch")):
                    with self.assertRaisesRegex(RuntimeError,"arm set differs from latest passing check"):
                        cmp_harness.measure_command(3,arms=("z","c2"))
                    with self.assertRaisesRegex(RuntimeError,"arm set differs from frozen run"):
                        cmp_harness.resume_command(runid,("z","c2"))
                self.assertFalse(any(p.name.startswith("measure-") and p.name != runid for p in cmp_harness.OUT.iterdir()))
            finally:
                cmp_harness.OUT = old_out

    def test_measure_command_refuses_changed_apparatus_before_any_cell_launch(self):
        with tempfile.TemporaryDirectory() as d:
            old_out = cmp_harness.OUT
            try:
                cmp_harness.OUT = pathlib.Path(d)
                checkdir = pathlib.Path(d) / "check-probe"
                checkdir.mkdir()
                expected = {"sha256": "stable", "files": {"cmp.py": "original"}, "tools": {}}
                cmp_harness.write_summary_hash(checkdir, expected)
                result = cmp_harness.measure_refusal_gate(checkdir, expected)
                self.assertTrue(result["pass"], result)
                self.assertEqual(result["reason"], "apparatus hash differs from check; refusing measure")
                self.assertEqual(list(pathlib.Path(d).glob("measure-*")), [])
            finally:
                cmp_harness.OUT = old_out

    def test_z_scope_acquisition_failure_keeps_payload_gated_and_invalid(self):
        class FakeCanary:
            healthy = True
            errors = []
            rows = []
            port = 1
            def __init__(self): pass
            def close(self): pass

        class FakeGatePipe:
            def __init__(self): self.writes=[]; self.closed=False
            def write(self, data): self.writes.append(data); return len(data)
            def flush(self): pass
            def close(self): self.closed=True

        class ParserRejectingPopen:
            instance = None
            def __init__(self, command, **kwargs):
                self.command=list(command); self.stdin=FakeGatePipe(); self.returncode=1
                self.parser_rejected = "--scope" in command and "--pipe" in command
                self.stderr = (b"--pty/--pipe is not compatible in timer or --scope mode"
                               if self.parser_rejected else b"simulated scope acquisition failure")
                ParserRejectingPopen.instance=self
            def wait(self, *args, **kwargs): return self.returncode
            def poll(self): return self.returncode
            def kill(self): self.returncode=-9

        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d).resolve(); old=(cmp_harness.ROOT,cmp_harness.BASE,cmp_harness.OUT)
            try:
                cmp_harness.ROOT=root; cmp_harness.BASE=root/"work"; cmp_harness.OUT=root/"out"
                tools={name:pathlib.Path("/usr/bin/"+name) for name in ("systemd-run","setsid","runuser","shell")}
                with ExitStack() as stack:
                    stack.enter_context(mock.patch.object(cmp_harness,"ensure_free_space",return_value=20*1024**3))
                    stack.enter_context(mock.patch.object(cmp_harness,"saved_cell",side_effect=lambda out,arm,fixture,rep: {"status":"NOT-BLOCKED"} if fixture=="allowed_rw" else None))
                    stack.enter_context(mock.patch.object(cmp_harness,"resolve_tools",return_value=tools))
                    stack.enter_context(mock.patch.object(cmp_harness,"scope_lookup",return_value={"state":"absent","path":None}))
                    stack.enter_context(mock.patch.object(cmp_harness,"Canary",FakeCanary))
                    scan=mock.Mock(return_value=([],[])); stack.enter_context(mock.patch.object(cmp_harness,"scan_marker",scan))
                    stack.enter_context(mock.patch.object(cmp_harness,"collect_outputs",return_value={"errors":[],"listener_healthy":True,"listener_accept":False,"listener_peer_marked":False,"listener_rows":[]}))
                    stack.enter_context(mock.patch.object(cmp_harness,"cleanup_marker",return_value={"pass":True,"errors":[],"remaining":[],"scope":{"pass":True,"scope_absent":True}}))
                    stack.enter_context(mock.patch.object(cmp_harness,"captured_output",return_value={"text":""}))
                    stack.enter_context(mock.patch.object(cmp_harness.subprocess,"Popen",ParserRejectingPopen))
                    evidence=cmp_harness.run_cell("z","file_read_outside",0,"scope-rejection")
                self.assertEqual(ParserRejectingPopen.instance.stdin.writes,[])
                self.assertTrue(ParserRejectingPopen.instance.stdin.closed)
                self.assertFalse(evidence["custody_gate_released"])
                self.assertFalse(evidence["marker_seen"])
                scan.assert_not_called()
                self.assertTrue(evidence["status"].startswith("INVALID("),evidence)
                self.assertEqual(evidence["status"],"INVALID(launch ok)")
                self.assertNotIn("--pipe",evidence["launcher_argv"])
                self.assertNotIn("--pty",evidence["launcher_argv"])
                self.assertFalse(ParserRejectingPopen.instance.parser_rejected,
                                 ParserRejectingPopen.instance.stderr.decode())
            finally:
                cmp_harness.ROOT,cmp_harness.BASE,cmp_harness.OUT=old

    def test_z_launcher_uses_unique_unlimited_bookkeeping_scope_and_gate(self):
        marker="run123-file_read_outside-z-r0-a456"
        tools={name:pathlib.Path("/usr/bin/"+name) for name in ("systemd-run","setsid","runuser","shell")}
        command,unit=cmp_harness.launcher_argv("z",marker,"file_read_outside",["/tmp/secret"],pathlib.Path("/tmp/allowed"),tools,True)
        self.assertEqual(unit,cmp_harness.scope_name(marker))
        self.assertEqual(command[:4],[str(tools["systemd-run"]),"--scope","--expand-environment=no","--unit="+unit])
        self.assertEqual(command[4],str(tools["setsid"]))
        self.assertLess(command.index(str(tools["systemd-run"])),command.index(str(tools["runuser"])))
        self.assertNotIn("--pipe",command)
        self.assertNotIn("--pty",command)
        self.assertTrue(any("IFS= read -r gate" in arg for arg in command))
        self.assertNotIn("Delegate=yes",command)
        self.assertFalse(any(any(key in arg for key in ("MemoryMax","TasksMax","CPUQuota")) for arg in command))

    def test_executor_temp_root_resolves_symlinked_parent(self):
        with tempfile.TemporaryDirectory() as parent:
            physical=pathlib.Path(parent)/"physical"; physical.mkdir()
            alias=pathlib.Path(parent)/"alias"; alias.symlink_to(physical,target_is_directory=True)
            with tempfile.TemporaryDirectory(dir=alias) as d:
                lexical=pathlib.Path(d); root=lexical.resolve()
                self.assertNotEqual(lexical,root)
                old=(cmp_harness.ROOT,cmp_harness.BASE,cmp_harness.OUT)
                try:
                    cmp_harness.ROOT=root; cmp_harness.BASE=root/"work"; cmp_harness.OUT=root/"out"
                    work,allowed=cmp_harness.prepare_dirs("run","z","noop",0,"attempt")
                    self.assertTrue(work.resolve().is_relative_to(root))
                    self.assertTrue(allowed.is_dir())
                finally:
                    cmp_harness.ROOT,cmp_harness.BASE,cmp_harness.OUT=old

    def test_cgroup_tree_snapshot_reads_descendant_cgroups(self):
        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d)/"scope"; child=root/"child"; grandchild=child/"grandchild"
            grandchild.mkdir(parents=True); (root/"cgroup.procs").write_text("101\n")
            (child/"cgroup.procs").write_text("102\n"); (grandchild/"cgroup.procs").write_text("103\n")
            tree=cmp_harness.cgroup_tree_snapshot(root)
        self.assertTrue(tree["complete"])
        self.assertTrue(tree["exists"])
        self.assertEqual({x["pid"] for x in tree["members"]},{101,102,103})
        self.assertEqual(len(tree["directories"]),3)

    def test_scope_and_argv_markers_are_unique(self):
        marker = "run123-file_read_outside-c2-r2"
        self.assertEqual(cmp_harness.scope_name(marker), cmp_harness.scope_name(marker))
        self.assertNotEqual(cmp_harness.scope_name(marker), cmp_harness.scope_name(marker + "x"))
        args = cmp_harness.launcher_payload(marker, "env_secret", [], False, "/app/fx")
        self.assertIn(marker, args)
        self.assertIn("/app/fx", args)

    def test_scoped_launchers_mount_only_fixture_and_allowed_root(self):
        marker = "run123-allowed_rw-b-r0"
        allowed = cmp_harness.ROOT / "work" / "run123" / "allowed_rw-r0" / "allowed"
        tools = {name: pathlib.Path("/usr/bin/" + name) for name in
                 ("systemd-run", "runuser", "bwrap", "nono", "setsid")}
        build_fx = str(cmp_harness.ROOT / "fx")

        bcmd, _ = cmp_harness.launcher_argv("b", marker, "allowed_rw", [], allowed, tools)
        runuser_at = bcmd.index(str(tools["runuser"]))
        self.assertNotEqual(bcmd[runuser_at - 1], "--")
        bwrap_at = bcmd.index(str(tools["bwrap"]))
        fx_mount_at = bcmd.index(build_fx, bwrap_at)
        for parent in cmp_harness.path_parents(allowed):
            parent_at = bcmd.index(parent, bwrap_at)
            self.assertEqual(bcmd[parent_at - 1], "--dir")
            self.assertLess(parent_at, fx_mount_at)
        for mount in (("--symlink", "usr/bin", "/bin"),
                      ("--ro-bind", "/usr", "/usr"),
                      ("--ro-bind", "/lib", "/lib"),
                      ("--ro-bind", "/lib64", "/lib64"),
                      ("--ro-bind", build_fx, build_fx),
                      ("--bind", str(allowed), str(allowed))):
            self.assertTrue(any(bcmd[i:i + len(mount)] == list(mount)
                                for i in range(len(bcmd) - len(mount) + 1)), mount)
        self.assertNotIn("/etc", bcmd)
        self.assertIn(cmp_harness.BENCH_HOME, bcmd)

        ccmd, _ = cmp_harness.launcher_argv("c2", marker, "allowed_rw", [], allowed, tools)
        nono_at = ccmd.index(str(tools["nono"]))
        expected_reads = ["run", "--read", "/usr", "--read", "/lib", "--read", "/lib64",
                          "--read-file", build_fx, "--allow", str(allowed)]
        self.assertEqual(ccmd[nono_at + 1:nono_at + 1 + len(expected_reads)], expected_reads)
        self.assertNotIn("/etc", ccmd)
        self.assertIn("HOME=" + cmp_harness.BENCH_HOME, ccmd)

    def test_ledger_resume_is_keyed_by_completed_event(self):
        with tempfile.TemporaryDirectory() as d:
            path = pathlib.Path(d) / "ledger.jsonl"
            cmp_harness.append_jsonl(path, {"event": "begin", "key": "z/a/0"})
            self.assertNotIn("z/a/0", cmp_harness.completed_cells(path))
            cmp_harness.append_jsonl(path, {"event": "complete", "key": "z/a/0"})
            self.assertIn("z/a/0", cmp_harness.completed_cells(path))

    def test_failed_positive_control_invalidates_arm_cells_and_resume_skips(self):
        with tempfile.TemporaryDirectory(prefix="cmp-small-test-") as d:
            old_out = cmp_harness.OUT
            try:
                cmp_harness.OUT = pathlib.Path(d)
                out = pathlib.Path(d) / "run"
                base = out / "evidence" / "z" / "allowed_rw"
                base.mkdir(parents=True)
                path = base / "rep-0.json"
                bad = {"arm": "z", "fixture": "allowed_rw", "rep": 0, "arm_broken": True, "status": "INVALID(arm-broken)"}
                path.write_text(__import__("json").dumps(bad))
                cmp_harness.append_jsonl(out / cmp_harness.LEDGER_NAME, {"event": "complete", "key": "z/allowed_rw/0", "status": bad["status"], "evidence": str(path), "evidence_sha256": cmp_harness.sha_file(path)})
                first = cmp_harness.run_cell("z", "file_read_outside", 0, "run")
                again = cmp_harness.run_cell("z", "file_read_outside", 0, "run")
                self.assertEqual(first["status"], "INVALID(arm-broken)")
                self.assertEqual(again["status"], first["status"])
                events = cmp_harness.ledger_state(pathlib.Path(d) / "run" / cmp_harness.LEDGER_NAME)
                self.assertEqual(sum(x.get("event") == "begin" for x in events), 0)
            finally:
                cmp_harness.OUT = old_out


if __name__ == "__main__":
    unittest.main(verbosity=2)
