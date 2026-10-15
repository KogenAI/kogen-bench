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
        marker = "case123-net_loopback-z-r0"

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
            rows = [{"peer_marker": "case123-net_loopback-z-r0", "peer_argv0": "cmp-bridge case123-net_loopback-z-r0"}]

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
                runid = "sample-overhead-resume"; outdir = cmp_harness.OUT / runid; outdir.mkdir(parents=True)
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
        self.assertEqual(plan["excluded_arms"], {arm:cmp_harness.excluded_arm_reason(arm, selected) for arm in ("c2", "a")})
        self.assertTrue(plan["cells"])
        self.assertTrue(all(cell[0] in selected for cell in plan["cells"]))
        self.assertEqual(len(plan["not_run_cells"]), len(cmp_harness.FIXTURES) * 3 * 2 + 3)  # c2 and a cells, plus a-bash allowed_rw per rep
        self.assertTrue(all(row["status"].startswith("NOT-RUN(excluded:") for row in plan["not_run_cells"]))
        check_not_run = cmp_harness.excluded_cell_rows(cmp_harness.matrix_cells_for_check(), selected)
        self.assertTrue(any(row["arm"] == "c2" and row["fixture"] == "allowed_rw" and row["status"].startswith("NOT-RUN(excluded:") for row in check_not_run))
        with tempfile.TemporaryDirectory() as d:
            old_out = cmp_harness.OUT
            try:
                cmp_harness.OUT = pathlib.Path(d)
                outdir = cmp_harness.OUT / "sample-selected"; outdir.mkdir()
                for row in plan["not_run_cells"]:
                    evidence = cmp_harness.write_not_run_evidence(outdir,row["arm"],row["fixture"],row["rep"],selected)
                    self.assertTrue(evidence["status"].startswith("NOT-RUN(excluded:"))
                cmp_harness.validate_not_run_evidence(outdir,plan["not_run_cells"])
                rows = cmp_harness.evidence_matrix("sample-selected",3,selected)
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
                checkdir = cmp_harness.OUT / "probe-check"; checkdir.mkdir()
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
                checkdir = pathlib.Path(d) / "probe-check"
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
        marker="case123-file_read_outside-z-r0-a456"
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
        marker = "case123-file_read_outside-c2-r2"
        self.assertEqual(cmp_harness.scope_name(marker), cmp_harness.scope_name(marker))
        self.assertNotEqual(cmp_harness.scope_name(marker), cmp_harness.scope_name(marker + "x"))
        args = cmp_harness.launcher_payload(marker, "env_secret", [], False, "/app/fx")
        self.assertIn(marker, args)
        self.assertIn("/app/fx", args)

    def test_scoped_launchers_mount_only_fixture_and_allowed_root(self):
        marker = "case123-allowed_rw-b-r0"
        allowed = cmp_harness.ROOT / "work" / "case123" / "allowed_rw-r0" / "allowed"
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


class FixBTests(unittest.TestCase):
    """FIX-B: blocked read/net attempts must stay observable; scoring rules unchanged."""

    def _observed_failed_attempt(self, fixture):
        ev = cmp_harness.bool_evidence(fixture, False)
        ev.update(returncode=4 if fixture == "net_loopback" else 2, launcher_completed=True, timed_out=False, launch_error=None)
        return ev

    def test_observed_failed_outside_attempt_scores_blocked(self):
        for fixture in ("file_read_outside", "secret_file_read", "net_loopback"):
            with self.subTest(fixture=fixture):
                self.assertEqual(cmp_harness.score(fixture, self._observed_failed_attempt(fixture)), "BLOCKED")

    def test_unobserved_failed_attempt_stays_invalid_whatever_the_exit_code(self):
        # Mirrors failed b attempts with no marker: nonzero exit does not establish blocking.
        for fixture in ("file_read_outside", "secret_file_read", "net_loopback"):
            for missing in ("launch_ok", "marker_seen"):
                with self.subTest(fixture=fixture, missing=missing):
                    ev = self._observed_failed_attempt(fixture); ev[missing] = False
                    if missing == "marker_seen": ev["launch_ok"] = False
                    self.assertEqual(cmp_harness.score(fixture, ev), "INVALID(launch ok)")

    def test_failed_attempt_with_incomplete_coverage_stays_invalid(self):
        for fixture, cov in (("file_read_outside", "read_scan_complete"), ("secret_file_read", "secret_file_scan_complete"),
                             ("net_loopback", "listener_coverage_complete")):
            with self.subTest(fixture=fixture):
                ev = self._observed_failed_attempt(fixture); ev[cov] = False
                self.assertEqual(cmp_harness.score(fixture, ev), "INVALID(observation coverage incomplete)")

    def test_successful_outside_attempt_still_not_blocked(self):
        for fixture in ("file_read_outside", "secret_file_read", "net_loopback"):
            with self.subTest(fixture=fixture):
                self.assertEqual(cmp_harness.score(fixture, cmp_harness.bool_evidence(fixture, True)), "NOT-BLOCKED")

    def test_c2_is_no_longer_deferred(self):
        reason = cmp_harness.excluded_arm_reason("c2", ("z", "b"))
        self.assertEqual(reason, "not selected by --arms z,b")
        self.assertNotIn("deferred", reason)
        self.assertEqual(cmp_harness.excluded_arm_reason("b", ("z", "c2")), "not selected by --arms z,c2")
        self.assertEqual(cmp_harness.normalize_arms("z,b,c2"), ("z", "b", "c2"))

    def test_bench_home_is_the_deployment_root(self):
        self.assertEqual(cmp_harness.BENCH_HOME, str(cmp_harness.ROOT))

    @unittest.skipUnless(shutil.which("cc"), "requires a C compiler")
    def test_fx_failed_read_and_connect_stay_alive_as_long_as_success(self):
        import socket
        with tempfile.TemporaryDirectory() as d:
            binary = pathlib.Path(d) / "fx"
            build = subprocess.run(["cc", "-O2", "-std=c99", "-Wall", "-Wextra", "-Werror", str(HERE / "fx.c"), "-o", str(binary)],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
            self.assertEqual(build.returncode, 0, build.stderr)
            # First exec of a new binary can be slowed by host policy scans; time only warm runs.
            self.assertEqual(subprocess.run([str(binary), "noop"], timeout=30).returncode, 0)
            canary = pathlib.Path(d) / "canary"; canary.write_text("READ_token")
            missing = str(pathlib.Path(d) / "absent" / "outside-read")
            listener = socket.socket(); listener.bind(("127.0" + ".0.1", 0)); listener.listen(4); open_port = listener.getsockname()[1]
            probe = socket.socket(); probe.bind(("127.0" + ".0.1", 0)); closed_port = probe.getsockname()[1]; probe.close()
            allowed_in = pathlib.Path(d) / "allowed-input"; allowed_in.write_text("ALLOW_token")
            cases = {"allowed_ok": (["allowed_rw", str(pathlib.Path(d) / "allowed-rw"), str(allowed_in)], 0),
                     "read_ok": (["file_read_outside", str(canary)], 0), "read_missing": (["file_read_outside", missing], 2),
                     "secret_missing": (["secret_file_read", missing], 2), "net_ok": (["net_loopback", str(open_port), "NET_t"], 0),
                     "net_refused": (["net_loopback", str(closed_port), "NET_t"], 4)}
            import threading
            results = {}
            def run(k, argv):
                t0 = time.monotonic(); proc = subprocess.Popen([str(binary), *argv])
                results[k] = (proc.wait(timeout=10), time.monotonic() - t0)
            try:
                threads = [threading.Thread(target=run, args=(k, argv)) for k, (argv, _) in cases.items()]
                for t in threads: t.start()
                for t in threads: t.join(timeout=15)
            finally:
                listener.close()
            for k, (_, rc) in cases.items(): self.assertEqual(results[k][0], rc, (k, results))
            elapsed = {k: v[1] for k, v in results.items()}
            for k in ("read_missing", "secret_missing", "net_refused", "allowed_ok"):
                self.assertGreaterEqual(elapsed[k], 0.95, (k, elapsed))
            self.assertGreaterEqual(elapsed["read_missing"], elapsed["read_ok"] - 0.3, elapsed)
            self.assertGreaterEqual(elapsed["net_refused"], elapsed["net_ok"] - 0.3, elapsed)

    def _build_warm_fx(self, d):
        binary = pathlib.Path(d) / "fx"
        build = subprocess.run(["cc", "-O2", "-std=c99", "-Wall", "-Wextra", "-Werror", str(HERE / "fx.c"), "-o", str(binary)],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
        self.assertEqual(build.returncode, 0, build.stderr)
        # First exec of a new binary can be slowed by host policy scans; time only warm runs.
        self.assertEqual(subprocess.run([str(binary), "noop"], timeout=30).returncode, 0)
        return binary

    @unittest.skipUnless(shutil.which("cc"), "requires a C compiler")
    def test_fx_empty_file_read_failure_holds_before_exit_3(self):
        # read_canary(): read() returns 0 on an empty file -> the `n <= 0` branch must still hold ~850 ms.
        with tempfile.TemporaryDirectory() as d:
            binary = self._build_warm_fx(d)
            empty = pathlib.Path(d) / "empty-canary"; empty.write_bytes(b"")
            for mode in ("file_read_outside", "secret_file_read"):
                with self.subTest(mode=mode):
                    t0 = time.monotonic()
                    rc = subprocess.run([str(binary), mode, str(empty)], timeout=15).returncode
                    elapsed = time.monotonic() - t0
                    self.assertEqual(rc, 3, (mode, rc, elapsed))
                    self.assertGreaterEqual(elapsed, 0.8, (mode, elapsed))

    @unittest.skipUnless(shutil.which("cc"), "requires a C compiler")
    def test_fx_socket_failure_holds_before_exit_3(self):
        # net_probe(): a real socket() failure (EMFILE) must still hold ~850 ms; rc 3 (not 2 arg parse / 4 connect) proves the branch.
        # RLIMIT_NOFILE=3 set from a preexec_fn aborts every macOS process in libSystem init, so the limit is lowered by a
        # constructor linked next to the unmodified fx.c: it runs after dynamic-loader init and before main().
        import socket
        limiter = "#define _GNU_SOURCE\n#include <sys/resource.h>\n__attribute__((constructor)) static void cmp_no_new_fds(void) {\n" \
                  "    struct rlimit r; r.rlim_cur = 3; r.rlim_max = 3; (void)setrlimit(RLIMIT_NOFILE, &r);\n}\n"
        with tempfile.TemporaryDirectory() as d:
            (pathlib.Path(d) / "limiter.c").write_text(limiter)
            binary = pathlib.Path(d) / "fx-nofd"
            build = subprocess.run(["cc", "-O2", "-std=c99", "-Wall", "-Wextra", "-Werror", str(HERE / "fx.c"), str(pathlib.Path(d) / "limiter.c"),
                                    "-o", str(binary)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
            self.assertEqual(build.returncode, 0, build.stderr)
            # First exec of a new binary can be slowed by host policy scans; time only warm runs.
            self.assertEqual(subprocess.run([str(binary), "noop"], timeout=30).returncode, 0)
            probe = socket.socket(); probe.bind(("127.0" + ".0.1", 0)); port = probe.getsockname()[1]; probe.close()
            t0 = time.monotonic()
            rc = subprocess.run([str(binary), "net_loopback", str(port), "NET_t"], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL, close_fds=True, timeout=15).returncode
            elapsed = time.monotonic() - t0
            self.assertEqual(rc, 3, (rc, elapsed))
            self.assertGreaterEqual(elapsed, 0.8, elapsed)


class ArmATests(unittest.TestCase):
    """Arm a (Kogen containment helper) and its a-bash variant; everything runs without Linux, cgroups or the real helper."""

    NS = __import__("types").SimpleNamespace
    DEFAULT_PROFILE = object()
    MANDATORY = ("filesystem-denial", "network-denial", "environment-isolation", "controller-protection", "descendant-custody",
                 "owner-death-cleanup", "wall-timeout", "cpu-timeout", "memory-threshold", "task-limit", "disk-limit",
                 "file-limit", "bounded-output", "reconciliation")
    PROFILE = {"os":"linux-cgroupv2", "host_identity":"host-1", "kernel_version":"6.8.0-test", "backend_id":"linux-ns-ptrace-v1",
               "backend_version":"1.2.3", "backend_digest":"sha256:" + "a" * 64, "qualification_digest":"sha256:" + "b" * 64,
               "privilege_identity":"uid-0"}
    FAKE_HELPER = r'''
import json, os, sys
mode, dump = sys.argv[1], sys.argv[2]
with open(dump, "w") as f:
    f.write(json.dumps(sorted(os.environ)))
for line in sys.stdin.buffer:
    frame = json.loads(line)
    op = frame["operation"]
    resp = {"protocol_major": 1, "protocol_minor": 0, "request_id": frame["request_id"], "status": "ok", "code": None, "payload": {}, "event_seq": 0}
    if op == "hello" and mode == "refuse-hello":
        resp.update(status="rejected", code="protocol-mismatch", payload={"error": {"code": "protocol-mismatch", "message": "no common version"}})
    elif op == "submit" and mode == "refuse-submit":
        resp.update(status="rejected", code="unsupported-capability", payload={"error": {"code": "unsupported-capability", "message": "seeded workspace quota capability is unqualified"}})
    elif op == "submit":
        resp["payload"] = {"handle": "h-1", "process_scope_id": "s-under-qualification-1"}
    elif op == "query":
        resp["payload"] = {"state": "terminal", "result": {"termination": {"exit_code": 7}}}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()
'''

    @classmethod
    def setUpClass(cls):
        cls.validate = cmp_harness.arm_a_load_pinned("validate.py")

    @staticmethod
    def hand_roots(extra_read=()):
        rows = [{"root_id":"fx-readonly", "path":"/var/lib/containment-fixture/ro", "object_identity":"linux-dev.10-ino.20", "mode":"read"}]
        for i, (rid, path) in enumerate(extra_read):
            rows.append({"root_id":rid, "path":path, "object_identity":f"linux-dev.10-ino.{0x40 + i:x}", "mode":"read"})
        for i, rid in enumerate(("allowed", "home", "temp", "cache")):
            rows.append({"root_id":rid, "path":f"/var/lib/containment-fixture/tmpfs/c1/{rid}", "object_identity":f"linux-dev.10-ino.{0x30 + i:x}", "mode":"write"})
        return rows

    def make_cfg(self, optional=(), run_id="case1", roots=None, profile=DEFAULT_PROFILE, **kw):
        return cmp_harness.arm_a_config(delegated="/sys/fs/cgroup/system.slice/cmp-x.scope", tmpfs="/var/lib/containment-fixture/tmpfs",
                                        roots=self.hand_roots() if roots is None else roots, profile=dict(self.PROFILE) if profile is self.DEFAULT_PROFILE else profile,
                                        implemented_optional=optional, run_id=run_id, uid=1001, expires_at="2030-01-01T00:00:00Z",
                                        protected=[pathlib.Path("/var/lib/containment-work")], **kw)

    def make_manifest(self, cfg=None, **kw):
        args = dict(command="/var/lib/containment-fixture/ro/fxa", argv=["mk", "run", "/var/lib/containment-fixture/ro/fx", "allowed_rw"], marker="mk",
                    reservation=4194304, now=1800000000)
        args.update(kw)
        return cmp_harness.arm_a_manifest(self.validate, cfg or self.make_cfg(), **args)

    # 1. payload ------------------------------------------------------------------------------------------------------------------
    def test_payload_arm_a_runs_static_fxa_with_mode_dependent_delay(self):
        marker, fx, done = "run-x-a-r0-a1", "/var/lib/containment-fixture/ro/fx", "/work/allowed/pressure.done"
        for mode in cmp_harness.ESCAPES + cmp_harness.SURVIVORS + cmp_harness.RESOURCES + ("allowed_rw",):
            with self.subTest(mode=mode):
                args = ["/p/one", "two"]
                command, argv = cmp_harness.arm_a_payload("a", marker, mode, args, fx, done if mode in cmp_harness.RESOURCES else None)
                self.assertEqual(command, str(cmp_harness.ARM_A_RO / "fxa"))
                self.assertEqual(command, "/var/lib/containment-fixture/ro/fxa")
                delay = "30" if mode in cmp_harness.SURVIVORS else done if mode in cmp_harness.RESOURCES else "run"
                self.assertEqual(argv, [marker, delay, fx, mode, "/p/one", "two"])
        # A done path never changes the delay of a non-resource mode; a resource mode without one falls back to 2 s.
        self.assertEqual(cmp_harness.arm_a_payload("a", marker, "file_read_outside", [], fx, done)[1][1], "run")
        self.assertEqual(cmp_harness.arm_a_payload("a", marker, "survivor_setsid", [], fx, done)[1][1], "30")
        self.assertEqual(cmp_harness.arm_a_payload("a", marker, "mem_cap", [], fx, None)[1][1], "2")

    def test_payload_arm_a_bash_is_b_bash_wrapper_unchanged(self):
        marker, fx, done = "run-x-a-bash-r0-a1", "/var/lib/containment-fixture/ro/fx", "/work/allowed/pressure.done"
        for mode in cmp_harness.ESCAPES + cmp_harness.SURVIVORS + cmp_harness.RESOURCES + ("allowed_rw",):
            with self.subTest(mode=mode):
                done_path = done if mode in cmp_harness.RESOURCES else None
                expected = cmp_harness.launcher_payload(marker, mode, ["a1"], mode in cmp_harness.SURVIVORS or mode in cmp_harness.RESOURCES, fx, done_path)
                command, argv = cmp_harness.arm_a_payload("a-bash", marker, mode, ["a1"], fx, done_path)
                self.assertEqual((command, argv), (expected[0], expected[1:]))
        command, argv = cmp_harness.arm_a_payload("a-bash", marker, "allowed_rw", [], fx, None)
        self.assertEqual(command, "/usr/bin/bash")
        self.assertEqual((argv[0], argv[2], argv[3]), ("-c", "cmp-bridge", marker))

    def test_payload_rejects_every_other_arm(self):
        for arm in ("z", "b", "c2", "a2", "A", "", None):
            with self.subTest(arm=arm):
                with self.assertRaises(ValueError):
                    cmp_harness.arm_a_payload(arm, "m", "allowed_rw", [], "/fx", None)

    # 2. config -------------------------------------------------------------------------------------------------------------------
    def test_config_has_closed_key_set_and_qualification_shape(self):
        profile = dict(self.PROFILE); before = dict(profile); roots = self.hand_roots()
        cfg = self.make_cfg(roots=roots, profile=profile, run_id="case42")
        self.assertEqual(set(cfg), {"delegated_cgroup", "private_tmpfs", "protected_roots", "roots", "qualification",
                                    "qualification_artifacts", "epochs", "admission_profile"})
        self.assertEqual(cfg["admission_profile"], "QUALIFICATION")
        self.assertEqual(cfg["delegated_cgroup"], "/sys/fs/cgroup/system.slice/cmp-x.scope")
        self.assertEqual(cfg["private_tmpfs"], "/var/lib/containment-fixture/tmpfs")
        self.assertEqual(cfg["protected_roots"], ["/var/lib/containment-work"])
        self.assertEqual(cfg["roots"], roots)
        self.assertEqual(cfg["qualification_artifacts"], {})
        q = cfg["qualification"]
        self.assertEqual(set(q), {"profile", "capabilities", "accounting", "expires_at", "harness"})
        self.assertEqual(q["profile"]["backend_id"], "linux-ns-ptrace-v1-under-qualification")
        self.assertEqual({k: v for k, v in q["profile"].items() if k != "backend_id"}, {k: v for k, v in before.items() if k != "backend_id"})
        self.assertEqual(profile, before, "the raw inspect tuple must not be mutated")
        self.assertEqual(q["accounting"], "under-qualification-linux-cgroupv2")
        self.assertEqual(q["expires_at"], "2030-01-01T00:00:00Z")
        self.assertEqual(q["harness"], {"run_id":"case42", "caller_id":"qualification.case42", "delegated_uid":1001})
        self.assertEqual(sorted(q["capabilities"]), sorted(self.MANDATORY))
        self.assertEqual(len(q["capabilities"]), 14)
        self.assertEqual(len(cfg["epochs"]), 1)
        epoch = cfg["epochs"][0]
        self.assertEqual(set(epoch), {"build_id", "attempt_id", "epoch"})
        self.assertEqual(epoch["epoch"], 1)
        self.assertEqual(str(cmp_harness.uuid.UUID(epoch["build_id"])), epoch["build_id"])
        self.assertNotEqual(self.make_cfg()["epochs"][0]["build_id"], epoch["build_id"])
        json.dumps(cfg)

    def test_config_seeded_workspace_quota_only_when_implemented(self):
        for optional in (None, (), [], ["other-optional"]):
            with self.subTest(optional=optional):
                self.assertEqual(sorted(self.make_cfg(optional=optional)["qualification"]["capabilities"]), sorted(self.MANDATORY))
        caps = self.make_cfg(optional=["other-optional", "seeded-workspace-quota"])["qualification"]["capabilities"]
        self.assertEqual(sorted(caps), sorted(self.MANDATORY + ("seeded-workspace-quota",)))
        self.assertEqual(len(caps), 15)

    def test_config_uses_the_given_epoch_and_refuses_unexpected_backend(self):
        epoch = {"build_id":"b-1", "attempt_id":"a-1", "epoch":7}
        self.assertEqual(self.make_cfg(epoch=epoch)["epochs"], [epoch])
        for bad in ({**self.PROFILE, "backend_id":"linux-ns-ptrace-v2"}, {**self.PROFILE, "backend_id":"linux-ns-ptrace-v1-under-qualification"},
                    {k: v for k, v in self.PROFILE.items() if k != "backend_id"}, ["linux-ns-ptrace-v1"], None):
            with self.subTest(profile=bad):
                with self.assertRaises(RuntimeError):
                    self.make_cfg(profile=bad)

    # 3. manifest -----------------------------------------------------------------------------------------------------------------
    def test_manifest_passes_pinned_validator_and_binds_the_cell(self):
        cfg = self.make_cfg(); validate = self.validate
        m = self.make_manifest(cfg, command=pathlib.Path("/var/lib/containment-fixture/ro/fxa"), argv=[pathlib.Path("/var/lib/containment-fixture/ro/fx"), 7], marker="mk-1", reservation=5242880)
        validate.validate_document("manifest", validate.canonical(m))
        self.assertEqual(m["version"], "1.0")
        self.assertEqual(m["purpose"], "tool")
        self.assertEqual((m["build_id"], m["attempt_id"], m["epoch"]), (cfg["epochs"][0]["build_id"], cfg["epochs"][0]["attempt_id"], cfg["epochs"][0]["epoch"]))
        self.assertEqual(m["command"], "/var/lib/containment-fixture/ro/fxa")
        self.assertEqual(m["argv"], ["/var/lib/containment-fixture/ro/fx", "7"])
        self.assertEqual(m["deadline"], "2027-01-15T08:02:00Z")
        self.assertNotEqual(m["command_id"], m["owner_id"])
        self.assertEqual(m["resource_limits"]["memory_bytes"], cmp_harness.CAPS["memory.max"] + 5242880)
        self.assertEqual(m["resource_limits"]["tasks"], cmp_harness.CAPS["pids.max"])
        self.assertEqual(m["resource_limits"]["tasks"], 64)
        for key, value in cmp_harness.ARM_A_STORAGE.items():
            self.assertEqual(m["resource_limits"][key], value)
        self.assertEqual(set(m["resource_limits"]), {"memory_bytes", "tasks", *cmp_harness.ARM_A_STORAGE})
        self.assertEqual(m["timeouts"], cmp_harness.ARM_A_TIMEOUTS)
        self.assertEqual(m["env_allowlist"], {"PATH":"/usr/bin:/bin", "HOME":"/var/lib/containment-fixture/tmpfs/c1/home", "CMPMARK":"mk-1"})
        self.assertNotIn("CMPSECRET", m["env_allowlist"])
        self.assertEqual(m["cwd"], "/var/lib/containment-fixture/tmpfs/c1/allowed")
        self.assertEqual(m["private_dirs"], {"home":"home", "temp":"temp", "cache":"cache", "build":"allowed"})
        self.assertEqual(m["network"], {"mode":"deny", "endpoints":[]})
        self.assertEqual(m["identity_hash"], validate.manifest_digest(m))
        self.assertEqual(m["profile"]["qualification_digest"], validate.digest(cfg["qualification"]))
        self.assertNotEqual(m["profile"]["qualification_digest"], self.PROFILE["qualification_digest"])
        self.assertEqual(m["profile"]["backend_id"], "linux-ns-ptrace-v1-under-qualification")

    def test_manifest_roots_drop_mode_and_keep_order(self):
        m = self.make_manifest()
        self.assertEqual(m["readable_roots"], [{"root_id":"fx-readonly", "path":"/var/lib/containment-fixture/ro", "object_identity":"linux-dev.10-ino.20"}])
        self.assertEqual([r["root_id"] for r in m["writable_roots"]], ["allowed", "home", "temp", "cache"])
        for row in m["readable_roots"] + m["writable_roots"]:
            self.assertEqual(set(row), {"root_id", "path", "object_identity"})

    def test_manifest_a_bash_needs_the_usr_read_root(self):
        marker = "run-x-a-bash-r0-a1"
        command, argv = cmp_harness.arm_a_payload("a-bash", marker, "allowed_rw", ["/w/allowed-rw", "/w/allowed-input"], "/var/lib/containment-fixture/ro/fx", None)
        with self.assertRaises(self.validate.Rejected):
            self.make_manifest(command=command, argv=argv, marker=marker)
        cfg = self.make_cfg(roots=self.hand_roots(extra_read=(("usr", "/usr"),)))
        m = self.make_manifest(cfg, command=command, argv=argv, marker=marker)
        self.assertEqual([r["root_id"] for r in m["readable_roots"]], ["fx-readonly", "usr"])
        self.assertEqual(m["argv"], argv)
        self.assertEqual(m["env_allowlist"]["CMPMARK"], marker)

    # 4. frames -------------------------------------------------------------------------------------------------------------------
    def test_frames_carry_manifest_binding_only_when_given(self):
        validate = self.validate; m = self.make_manifest()
        submit = cmp_harness.arm_a_frame(validate, "submit", {"manifest":m}, m)
        self.assertEqual(set(submit), {"protocol_major", "protocol_minor", "request_id", "operation", "payload", "payload_digest",
                                       "build_id", "attempt_id", "epoch", "capability_digest", "deadline"})
        self.assertEqual((submit["protocol_major"], submit["protocol_minor"], submit["operation"]), (1, 0, "submit"))
        self.assertEqual((submit["build_id"], submit["attempt_id"], submit["epoch"]), (m["build_id"], m["attempt_id"], m["epoch"]))
        self.assertEqual(submit["capability_digest"], m["identity_hash"])
        self.assertEqual(submit["deadline"], m["deadline"])
        self.assertEqual(submit["payload_digest"], validate.digest(submit["payload"]))
        self.assertEqual(str(cmp_harness.uuid.UUID(submit["request_id"])), submit["request_id"])
        for op, payload in (("hello", {"supported_major":[1], "supported_minor":[0]}), ("query", {"handle":"h-1"})):
            frame = cmp_harness.arm_a_frame(validate, op, payload)
            with self.subTest(op=op):
                self.assertEqual(set(frame), {"protocol_major", "protocol_minor", "request_id", "operation", "payload", "payload_digest"})
                self.assertEqual(frame["payload"], payload)
                self.assertEqual(frame["payload_digest"], validate.digest(payload))
                self.assertNotEqual(frame["request_id"], submit["request_id"])
        # The canonical wire form round-trips through the strict loader the client uses.
        self.assertEqual(validate.strict_load(validate.canonical(submit)), submit)

    # 5. refusal / exit code / status ---------------------------------------------------------------------------------------------
    def test_refusal_extracts_code_and_message_from_rejected_responses(self):
        refusal = cmp_harness.arm_a_refusal
        rejected = {"status":"rejected", "code":"unsupported-capability", "payload":{"error":{"code":"other", "message":"capability unqualified"}}}
        self.assertEqual(refusal(rejected), {"code":"unsupported-capability", "message":"capability unqualified"})
        self.assertEqual(refusal({"status":"rejected", "code":None, "payload":{"error":{"code":"from-error", "detail":"the detail"}}}),
                         {"code":"from-error", "message":"the detail"})
        self.assertEqual(refusal({"status":"rejected", "code":"c", "payload":None}), {"code":"c", "message":"{}"})
        fallback = refusal({"status":"rejected", "code":"c", "payload":{"error":{"x":"y" * 400}}})
        self.assertEqual(fallback["code"], "c")
        self.assertEqual(len(fallback["message"]), 300)
        self.assertTrue(fallback["message"].startswith('{"x": "yyy'))

    def test_refusal_is_none_for_ok_and_explicit_for_no_response(self):
        self.assertIsNone(cmp_harness.arm_a_refusal({"status":"ok", "code":None, "payload":{}}))
        self.assertIsNone(cmp_harness.arm_a_refusal({"status":"accepted", "payload":{"error":{"code":"x"}}}))
        for missing in (None, [], "rejected"):
            with self.subTest(response=missing):
                self.assertEqual(cmp_harness.arm_a_refusal(missing), {"code":"no-response", "message":"no helper response"})

    def test_exit_code_from_termination(self):
        code = cmp_harness.arm_a_exit_code
        self.assertEqual(code({"termination":{"exit_code":0}}), 0)
        self.assertEqual(code({"termination":{"exit_code":7}}), 7)
        self.assertEqual(code({"termination":{"exit_code":256 + 3}}), 3)
        self.assertEqual(code({"termination":{"signal":"KILL"}}), 137)
        self.assertEqual(code({"termination":{"signal":"SIGTERM"}}), 143)
        self.assertEqual(code({"termination":{"signal":"term"}}), 143)
        self.assertEqual(code({"termination":{"exit_code":None, "signal":"KILL"}}), 137)
        self.assertEqual(code({"termination":{"exit_code":5, "signal":"KILL"}}), 5)
        for odd in ({}, {"termination":None}, {"termination":{}}, {"termination":{"signal":"NOTASIGNAL"}}, {"termination":{"exit_code":"7"}},
                    {"termination":{"exit_code":True}}, {"termination":"exit"}, None, "x", []):
            with self.subTest(result=odd):
                self.assertEqual(code(odd), 70)

    def test_status_refusal_wins_for_both_variants(self):
        helper = {"refusal":{"code":"unsupported-capability", "message":"seeded workspace quota capability is unqualified"}, "marker_seen":True}
        for arm in ("a", "a-bash"):
            for scored in ("BLOCKED", "NOT-BLOCKED", "INVALID(x)", "ENFORCED"):
                with self.subTest(arm=arm, scored=scored):
                    self.assertEqual(cmp_harness.arm_a_status(arm, scored, helper),
                                     "REFUSED(unsupported-capability: seeded workspace quota capability is unqualified)")
        self.assertEqual(cmp_harness.arm_a_status("a", "INVALID(x)", {"refusal":None}), "INVALID(x)")

    def test_status_a_bash_is_never_blocked(self):
        for helper in ({"marker_seen":True}, {"marker_seen":False}, {}, None):
            with self.subTest(helper=helper):
                status = cmp_harness.arm_a_status("a-bash", "BLOCKED", helper)
                self.assertTrue(status.startswith("INVALID("), status)
                self.assertIn("never scored BLOCKED", status)
        self.assertEqual(cmp_harness.arm_a_status("a-bash", "NOT-BLOCKED", {"marker_seen":True}), "NOT-BLOCKED")
        self.assertEqual(cmp_harness.arm_a_status("a-bash", "NOT-BLOCKED", {"marker_seen":False}), "NOT-BLOCKED")
        self.assertEqual(cmp_harness.arm_a_status("a-bash", "INVALID(insufficient)", {"marker_seen":True}), "INVALID(insufficient)")

    def test_status_a_bash_launch_failed_needs_affirmative_start_failure(self):
        helper = {"marker_seen":False, "client_returncode":70,
                  "result":{"status":"uncertain", "termination":{"cause":"start-failed", "exit_code":None, "signal":None}, "error":{"code":"cleanup-uncertain", "message":"x"}}}
        status = cmp_harness.arm_a_status("a-bash", "INVALID(launch ok)", helper)
        self.assertTrue(status.startswith("LAUNCH-FAILED("), status)
        self.assertEqual(json.loads(status[len("LAUNCH-FAILED("):-1]),
                         {"result_status":"uncertain", "termination":{"cause":"start-failed", "exit_code":None, "signal":None}, "error":"cleanup-uncertain", "client_rc":70})
        #  an unobserved but successful helper exit, or empty helper evidence, stays the scorer's INVALID.
        for unproven in (None, {}, {"result":"not-a-dict"}, {"marker_seen":False, "result":{"status":"finished", "termination":{"cause":"exited", "exit_code":0}}},
                         {"marker_seen":False, "result":{"error":"plain"}}):
            with self.subTest(helper=unproven):
                self.assertEqual(cmp_harness.arm_a_status("a-bash", "INVALID(launch ok)", unproven), "INVALID(launch ok)")
        self.assertEqual(cmp_harness.arm_a_status("a-bash", "INVALID(x)", {"marker_seen":True, "result":helper["result"]}), "INVALID(x)")

    def test_status_arm_a_passes_the_scored_value_through(self):
        for scored in ("BLOCKED", "NOT-BLOCKED", "ENFORCED", "INVALID(insufficient)", "INVALID(arm-broken)"):
            for helper in ({"marker_seen":True}, {"marker_seen":False}, {}, None):
                with self.subTest(scored=scored, helper=helper):
                    self.assertEqual(cmp_harness.arm_a_status("a", scored, helper), scored)

    # 6. memory reservation -------------------------------------------------------------------------------------------------------
    def fake_statvfs(self, blocks, bfree, files, ffree, calls=None):
        def statvfs(path):
            if calls is not None: calls.append(path)
            return self.NS(f_bsize=4096, f_blocks=blocks, f_bfree=bfree, f_files=files, f_ffree=ffree)
        return statvfs

    def test_memory_reservation_formula_and_entry_surcharge(self):
        mib4 = 4 * 1024 * 1024
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d) / "tmpfs"; root.mkdir()
            (root / "cell" / "sub").mkdir(parents=True); (root / "cell" / "f1").write_text("x"); (root / "cell" / "sub" / "f2").write_text("y"); (root / "top").write_text("z")
            # root, cell, sub, f1, f2, top: six inventoried entries.
            calls = []
            low = cmp_harness.arm_a_memory_reservation(root, self.fake_statvfs(1000, 900, 20, 17, calls))
            self.assertEqual(calls, [str(root)])
            self.assertEqual(low["data_bytes"], 100 * 4096)
            self.assertEqual((low["objects"], low["entries"]), (3, 6))
            self.assertEqual(low["extra_entry_bytes"], 3 * 8192)
            self.assertEqual(low["block_size"], 4096)
            self.assertEqual(low["reservation_bytes"], mib4 + 100 * 4096 + 3 * 8192 + 3 * 8192)
            for objects in (6, 50):
                with self.subTest(used_inodes=objects):
                    high = cmp_harness.arm_a_memory_reservation(root, self.fake_statvfs(1000, 1000, 100, 100 - objects))
                    self.assertEqual(high["extra_entry_bytes"], 0)
                    self.assertEqual(high["data_bytes"], 0)
                    self.assertEqual(high["reservation_bytes"], mib4 + objects * 8192)
            real = cmp_harness.arm_a_memory_reservation(root)
            self.assertEqual(real["entries"], 6)
            self.assertGreaterEqual(real["reservation_bytes"], mib4)
            self.assertGreater(real["block_size"], 0)

    def test_memory_reservation_counts_symlinks_once_without_following_them(self):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d) / "tmpfs"; (root / "a").mkdir(parents=True); (root / "a" / "f").write_text("x"); (root / "l").symlink_to(root / "a", target_is_directory=True)
            got = cmp_harness.arm_a_memory_reservation(root, self.fake_statvfs(10, 10, 4, 4))
            self.assertEqual(got["entries"], 4)  # root, a, f, l
            self.assertEqual(got["reservation_bytes"], 4 * 1024 * 1024 + 4 * 8192)
            empty = pathlib.Path(d) / "empty"; empty.mkdir()
            self.assertEqual(cmp_harness.arm_a_memory_reservation(empty, self.fake_statvfs(10, 10, 1, 1))["reservation_bytes"], 4 * 1024 * 1024 + 8192)

    # 7. candidate cgroup sampling ------------------------------------------------------------------------------------------------
    CUSTODY = {"unit":"cmp-x.scope", "cgroup_path":"/sys/fs/cgroup/system.slice/cmp-x.scope"}
    FX_ROW = {"pid":4242, "start":777}

    def snapshot(self, observed, custody=None, state=None, fx_row=FX_ROW, expected=None):
        calls = []
        def observe(pid, start, *rest):
            calls.append((pid, start)); return observed
        with mock.patch.object(cmp_harness, "observe_proc_cgroup", side_effect=observe):
            result = cmp_harness.arm_a_cgroup_snapshot("cmp-x.scope", self.CUSTODY if custody is None else custody, fx_row, expected, state)
        return result, calls

    def test_cgroup_snapshot_rejects_a_candidate_outside_the_custody_scope(self):
        child = {"verified_identity":True, "cgroup_path":"/system.slice/cmp-x.scope/s-under-qualification-1"}
        for custody in ({"cgroup_path":"/sys/fs/cgroup/system.slice/other.scope"}, {"cgroup_path":None}, {}, None):
            with self.subTest(custody=custody):
                result, calls = self.snapshot(child, custody=custody if custody is not None else {})
                self.assertFalse(result["ok"])
                self.assertEqual(calls, [(4242, 777)])
                self.assertTrue(any("not a child of the custody scope" in e for e in result["errors"]), result["errors"])
                self.assertEqual(result["path"], "/sys/fs/cgroup/system.slice/cmp-x.scope/s-under-qualification-1")
                self.assertEqual(result["files"], {})
                self.assertIsNone(result["scope_identity"])
        grandchild = {"verified_identity":True, "cgroup_path":"/system.slice/cmp-x.scope/s-under-qualification-1/deeper"}
        result, _ = self.snapshot(grandchild)
        self.assertFalse(result["ok"])
        self.assertTrue(any("not a child of the custody scope" in e for e in result["errors"]))

    def test_cgroup_snapshot_rejects_the_runner_leaf(self):
        result, _ = self.snapshot({"verified_identity":True, "cgroup_path":"/system.slice/cmp-x.scope/runner"})
        self.assertFalse(result["ok"])
        self.assertTrue(any("runner leaf" in e for e in result["errors"]), result["errors"])
        self.assertIsNone(result["scope_identity"])

    def test_cgroup_snapshot_rejects_a_scope_id_that_differs_from_the_helper_report(self):
        child = {"verified_identity":True, "cgroup_path":"/system.slice/cmp-x.scope/s-under-qualification-1"}
        result, _ = self.snapshot(child, state={"submit_scope_id":"s-under-qualification-2"})
        self.assertFalse(result["ok"])
        self.assertTrue(any("differs from the helper-reported process_scope_id" in e for e in result["errors"]), result["errors"])
        # Same id: the identity checks pass and only the (absent on this host) cgroup directory stops the sample.
        result, _ = self.snapshot(child, state={"submit_scope_id":"s-under-qualification-1"})
        self.assertFalse(result["ok"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertTrue(result["errors"][0].startswith("candidate cgroup stat:"), result["errors"])
        identity = result["scope_identity"]
        self.assertEqual(identity["scope_kind"], "helper-candidate-cgroup")
        self.assertEqual((identity["unit"], identity["custody_unit"]), ("cmp-x.scope", "cmp-x.scope"))
        self.assertEqual(identity["control_group"], "/system.slice/cmp-x.scope/s-under-qualification-1")
        self.assertEqual(identity["cgroup_path"], "/sys/fs/cgroup/system.slice/cmp-x.scope/s-under-qualification-1")
        self.assertEqual(identity["helper_process_scope_id"], "s-under-qualification-1")
        self.assertEqual(identity["located_from"], {"pid":4242, "start":777, "verified_identity":True})

    def test_cgroup_snapshot_requires_a_verified_process_identity(self):
        path = "/system.slice/cmp-x.scope/s-under-qualification-1"
        for observed in ({"verified_identity":False, "cgroup_path":path}, {"verified_identity":None, "cgroup_path":path},
                         {"verified_identity":True, "cgroup_path":None}, {"verified_identity":True, "cgroup_path":""}, {}):
            with self.subTest(observed=observed):
                result, calls = self.snapshot(observed)
                self.assertFalse(result["ok"])
                self.assertEqual(calls, [(4242, 777)])
                self.assertIn("candidate cgroup membership not verified for the marked fx PID", result["errors"])
                self.assertEqual(result["files"], {})
                self.assertIsNone(result["scope_identity"])

    def test_cgroup_snapshot_needs_an_fx_row_or_an_expected_identity(self):
        for expected in (None, {}, {"unit":"u"}, {"cgroup_path":""}):
            for row in (None, "not-a-row", []):
                with self.subTest(expected=expected, row=row):
                    result, calls = self.snapshot({"verified_identity":True, "cgroup_path":"/x"}, fx_row=row, expected=expected)
                    self.assertFalse(result["ok"])
                    self.assertEqual(calls, [])
                    self.assertEqual(result["errors"], ["no marked fx process to locate the candidate cgroup"])
                    self.assertIsNone(result["path"])
                    self.assertEqual(result["files"], {})
                    self.assertIsNone(result["scope_identity"])

    def test_cgroup_snapshot_reads_the_counters_of_an_expected_identity(self):
        with tempfile.TemporaryDirectory() as d:
            cg = pathlib.Path(d) / "s-under-qualification-1"; cg.mkdir()
            for i, name in enumerate(cmp_harness.ARM_A_CGROUP_FILES): (cg / name).write_text(f"{i * 11}\n")
            (cg / "memory.events").write_text("low 0\nhigh 0\nmax 3\noom 1\n")
            expected = {"unit":"cmp-x.scope", "cgroup_path":str(cg)}
            result, calls = self.snapshot({"verified_identity":True, "cgroup_path":"/never/used"}, expected=expected)
            self.assertEqual(calls, [], "an expected identity must not re-locate the cgroup from /proc")
            self.assertTrue(result["ok"], result["errors"])
            self.assertEqual(result["errors"], [])
            self.assertEqual(result["path"], str(cg))
            self.assertIs(result["scope_identity"], expected)
            self.assertIsNone(result["locate"])
            self.assertEqual(set(result["files"]), set(cmp_harness.ARM_A_CGROUP_FILES))
            self.assertEqual(result["files"]["memory.current"], "0")
            self.assertEqual(result["files"]["pids.max"], "66")
            self.assertEqual(result["files"]["memory.events"], "low 0\nhigh 0\nmax 3\noom 1")
            # A missing counter file is an error, not a silently shorter sample.
            (cg / "pids.events").unlink()
            result, _ = self.snapshot(None, expected=expected)
            self.assertFalse(result["ok"])
            self.assertNotIn("pids.events", result["files"])
            self.assertEqual(len(result["errors"]), 1)
            self.assertIn("pids.events", result["errors"][0])
            self.assertIn("FileNotFoundError", result["errors"][0])
            # A vanished cgroup directory is reported before any file is read.
            gone = {"unit":"cmp-x.scope", "cgroup_path":str(cg / "gone")}
            result, _ = self.snapshot(None, expected=gone)
            self.assertFalse(result["ok"])
            self.assertEqual(result["files"], {})
            self.assertTrue(result["errors"][0].startswith("candidate cgroup stat:"))
            self.assertIs(result["scope_identity"], gone)

    # 8. plans --------------------------------------------------------------------------------------------------------------------
    def test_check_matrix_has_arm_a_and_three_a_bash_controls_only_when_a_bash_is_selected(self):
        cells = cmp_harness.matrix_cells_for_check(("z", "b", "a", "a-bash"))
        self.assertEqual(len(cells), len(set(cells)))
        self.assertIn(("a", "allowed_rw", 0), cells)
        for fixture in cmp_harness.SURVIVORS + cmp_harness.RESOURCES: self.assertIn(("a", fixture, 0), cells)
        self.assertEqual([c for c in cells if c[0] == "a-bash"], [("a-bash", "allowed_rw", r) for r in range(3)])
        self.assertEqual({c[0] for c in cells}, {"z", "b", "a", "a-bash"})
        self.assertFalse([c for c in cmp_harness.matrix_cells_for_check(("z", "b", "a")) if c[0] == "a-bash"])
        self.assertEqual(cmp_harness.matrix_cells_for_check(cmp_harness.SELECTABLE_ARMS).count(("a-bash", "allowed_rw", 0)), 1)
        self.assertEqual(cmp_harness.normalize_arms("a-bash,a,z"), ("z", "a", "a-bash"))
        with self.assertRaises(ValueError): cmp_harness.normalize_arms("z,a-bash")
        self.assertEqual(cmp_harness.normalize_arms(None), cmp_harness.ARMS)

    def test_check_matrix_without_arm_a_has_no_a_cells_and_marks_a_bash_not_run(self):
        selected = ("z", "b")
        cells = cmp_harness.matrix_cells_for_check(selected)
        self.assertFalse([c for c in cells if c[0] in ("a", "a-bash")])
        full = cmp_harness.matrix_cells_for_check(cmp_harness.SELECTABLE_ARMS)
        rows = cmp_harness.excluded_cell_rows(full, selected)
        bash_rows = [r for r in rows if r["arm"] == "a-bash"]
        self.assertEqual([(r["fixture"], r["rep"]) for r in bash_rows], [("allowed_rw", 0), ("allowed_rw", 1), ("allowed_rw", 2)])
        for row in bash_rows:
            self.assertEqual(row["status"], "NOT-RUN(excluded: not selected by --arms z,b)")
            self.assertEqual(row["reason"], "not selected by --arms z,b")
        self.assertTrue({"a", "a-bash", "c2"} <= {r["arm"] for r in rows})
        self.assertFalse({"z", "b"} & {r["arm"] for r in rows})

    def test_check_matrix_with_a_bash_excludes_no_a_bash_row(self):
        full = cmp_harness.matrix_cells_for_check(cmp_harness.SELECTABLE_ARMS)
        selected = ("z", "b", "a", "a-bash")
        rows = cmp_harness.excluded_cell_rows(full, selected)
        self.assertEqual({r["arm"] for r in rows}, {"c2"})
        self.assertEqual({r["arm"] for r in cmp_harness.excluded_cell_rows(full, ("z", "b", "a"))}, {"c2", "a-bash"})
        self.assertEqual(cmp_harness.excluded_cell_rows(full, cmp_harness.SELECTABLE_ARMS), [])
        excluded = {(r["arm"], r["fixture"], r["rep"]) for r in rows}
        self.assertEqual({c for c in full if c not in excluded}, set(cmp_harness.matrix_cells_for_check(selected)))

    def test_measurement_cells_pair_a_bash_with_each_allowed_rw_repetition(self):
        cells = cmp_harness.measurement_cells(2, ("z", "a", "a-bash"))
        for rep in range(2):
            self.assertIn(("a-bash", "allowed_rw", rep), cells)
            self.assertIn(("a", "file_write_outside", rep), cells)
            self.assertIn(("z", "file_write_outside", rep), cells)
            self.assertIn(("a", "allowed_rw", rep), cells)
        self.assertEqual([c for c in cells if c[0] == "a-bash"], [("a-bash", "allowed_rw", 0), ("a-bash", "allowed_rw", 1)])
        self.assertEqual(len(cells), len(set(cells)))
        self.assertFalse([c for c in cmp_harness.measurement_cells(2, ("z", "a")) if c[0] == "a-bash"])
        self.assertFalse([c for c in cmp_harness.measurement_cells(2, ("z", "b")) if c[0] in ("a", "a-bash")])
        self.assertEqual(cmp_harness.overhead_plan(("z", "a", "a-bash")).keys(), {"z", "a"})

    def test_frozen_plan_lists_a_bash_as_not_run_when_unselected(self):
        plan = cmp_harness.frozen_plan(2, ("z", "b"))
        self.assertFalse([c for c in plan["cells"] if c[0] in ("a", "a-bash")])
        self.assertEqual([(r["arm"], r["fixture"], r["rep"]) for r in plan["not_run_cells"] if r["arm"] == "a-bash"],
                         [("a-bash", "allowed_rw", 0), ("a-bash", "allowed_rw", 1)])
        selected = cmp_harness.frozen_plan(2, ("z", "a", "a-bash"))
        self.assertIn(["a-bash", "allowed_rw", 1], selected["cells"])
        self.assertFalse([r for r in selected["not_run_cells"] if r["arm"] in ("a", "a-bash")])
        self.assertFalse([k for k in selected["overhead_keys"] if k[0] == "a-bash"])
        self.assertEqual(selected["selected_arms"], ["z", "a", "a-bash"])

    # 9. custody launcher ---------------------------------------------------------------------------------------------------------
    FAKE_TOOLS = {"systemd-run":pathlib.Path("/fake/systemd-run"), "runuser":pathlib.Path("/fake/runuser"), "python":pathlib.Path("/fake/python3"),
                  "shell":pathlib.Path("/fake/bash"), "setsid":pathlib.Path("/fake/setsid"), "bwrap":pathlib.Path("/fake/bwrap")}

    def test_launcher_argv_is_an_unmetered_delegated_custody_scope(self):
        marker = "case1-allowed_rw-a-r0-a1234567890"
        argv, unit = cmp_harness.arm_a_launcher_argv(marker, "/tmp/session", self.FAKE_TOOLS)
        self.assertEqual(unit, cmp_harness.scope_name(marker))
        self.assertEqual(argv[:7], ["/fake/systemd-run", "--scope", "--expand-environment=no", "--unit=" + unit, "-p", "Delegate=yes", "/fake/bash"])
        self.assertEqual(argv.count("-p"), 1)
        joined = " ".join(argv)
        for forbidden in ("MemoryMax", "TasksMax", "CPUQuota", "MemoryHigh", "CPUWeight"): self.assertNotIn(forbidden, joined)
        self.assertEqual(argv[7], "-c")
        self.assertIn("read -r gate", argv[8])
        self.assertIn('"$gate" = release', argv[8])
        self.assertIn('exec "$@"', argv[8])
        self.assertEqual(argv[9], "cmp-gate")
        self.assertEqual(argv[10:], ["/fake/runuser", "-u", "bench", "--", "/fake/python3", "-B", "-I", str(cmp_harness.ROOT / "cmp.py"),
                                     "_arm_a_client", "/tmp/session/spec.json"])
        again, _ = cmp_harness.arm_a_launcher_argv(marker, pathlib.Path("/tmp/session"), self.FAKE_TOOLS)
        self.assertEqual(again, argv)

    def test_launcher_gate_script_matches_the_z_gate_and_arm_a_is_not_in_launcher_argv(self):
        marker = "case1-allowed_rw-a-r0-a1234567890"
        a_argv, _ = cmp_harness.arm_a_launcher_argv(marker, "/tmp/session", self.FAKE_TOOLS)
        z_argv, z_unit = cmp_harness.launcher_argv("z", "case1-allowed_rw-z-r0-a1", "allowed_rw", [], "/tmp/allowed", self.FAKE_TOOLS, True)
        self.assertEqual(a_argv[a_argv.index("cmp-gate") - 1], z_argv[z_argv.index("cmp-gate") - 1])
        self.assertEqual(z_unit, cmp_harness.scope_name("case1-allowed_rw-z-r0-a1"))
        self.assertEqual(cmp_harness.launcher_argv("a", marker, "allowed_rw", [], "/tmp/allowed", self.FAKE_TOOLS), (None, None))

    # 10. custody regex -----------------------------------------------------------------------------------------------------------
    def stop_with_failing_lookup(self, marker):
        failed = {"state":"error", "unit":cmp_harness.scope_name(marker), "path":None, "errors":["LoadState:rc=1:stderr=bus unavailable"], "lookup":{}}
        stopped = subprocess.CompletedProcess(["systemctl"], 0, b"", b"")
        with mock.patch.object(cmp_harness, "scope_lookup", return_value=failed) as lookup, \
             mock.patch.object(cmp_harness.subprocess, "run", return_value=stopped) as run:
            result = cmp_harness.stop_scope(marker, {"systemctl":pathlib.Path("/fake/systemctl")}, timeout=0.01)
        return result, lookup, run

    def test_stop_scope_treats_arm_a_markers_as_scoped(self):
        for marker in ("case1-allowed_rw-a-r0-a1234567890", "case1-allowed_rw-a-bash-r0-a12", "case1-file_write_outside-a-r1-a99", "case1-allowed_rw-a-bash-r2-a7"):
            with self.subTest(marker=marker):
                result, lookup, run = self.stop_with_failing_lookup(marker)
                self.assertEqual(result["unit"], cmp_harness.scope_name(marker))
                self.assertIsNotNone(result["unit"])
                self.assertFalse(result["pass"])
                self.assertTrue(any("bus unavailable" in e for e in result["errors"]), result["errors"])
                self.assertEqual(lookup.call_args_list[0].args[0], cmp_harness.scope_name(marker))
                self.assertEqual(run.call_args.args[0][1:], ["stop", "--no-block", cmp_harness.scope_name(marker)])

    def test_stop_scope_passes_through_markers_without_a_custody_arm(self):
        for marker in ("case1-allowed_rw-x-r0-a123", "case1-allowed_rw-ab-r0-a123", "case1-allowed_rw-xa-bash-r0-a1", "case1-allowed_rw-a-bash"):
            with self.subTest(marker=marker):
                result, lookup, run = self.stop_with_failing_lookup(marker)
                self.assertIsNone(result["unit"])
                self.assertTrue(result["pass"])
                lookup.assert_not_called(); run.assert_not_called()

    # 11. client, end to end against a fake helper --------------------------------------------------------------------------------
    def run_client(self, scenario, verify_error=None):
        real_loader = cmp_harness.arm_a_load_pinned; seen = {}
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {"CORE04_STALE":"stale", "CMP_PASSTHROUGH":"1"}):
            tmp = pathlib.Path(tmp); script = tmp / "fake_helper.py"; script.write_text(self.FAKE_HELPER)
            env_dump = tmp / "helper-env.json"; session = tmp / "session"; session.mkdir(); tmpfs = tmp / "tmpfs"; tmpfs.mkdir()
            config = tmp / "config.json"; config.write_text(json.dumps(self.make_cfg(run_id="case9")))
            marker = "case9-allowed_rw-a-r0-a1234567890"
            spec = {"helper":"/fake/kogen-contain", "state_dir":str(session / "state"), "config":str(config), "session_dir":str(session), "run_id":"case9",
                    "caller_id":"qualification-caller", "tmpfs":str(tmpfs), "marker":marker, "command":"/var/lib/containment-fixture/ro/fxa",
                    "argv":[marker, "run", "/var/lib/containment-fixture/ro/fx", "allowed_rw", "/w/allowed-rw", "/w/allowed-input"],
                    "result_path":str(session / "client-result.json"), "transcript_path":str(session / "transcript.json"), "helper_stderr":str(session / "helper.stderr")}
            spec_path = tmp / "spec.json"; spec_path.write_text(json.dumps(spec))
            helper_cmd = [sys.executable, "-B", str(script), scenario, str(env_dump)]

            def env_now(): return {k: os.environ.get(k) for k in ("CORE04_QUALIFICATION_RUN_ID", "CORE04_QUALIFICATION_CALLER_ID")}
            def verify_backend_host(backend):
                seen["verify"] = {"backend":backend, "env":env_now()}
                if verify_error: raise ValueError(verify_error)
            def backend_command(*args, **kwargs):
                seen["command"] = {"args":args, "kwargs":kwargs, "env":env_now()}; return helper_cmd
            adapter = self.NS(verify_backend_host=verify_backend_host, backend_command=backend_command)
            loader = lambda name, vendor=None: adapter if name == "adapter.py" else real_loader(name, vendor)
            with mock.patch.object(cmp_harness, "arm_a_load_pinned", side_effect=loader), \
                 mock.patch.object(cmp_harness, "arm_a_memory_reservation", return_value={"reservation_bytes":4194304}):
                rc = cmp_harness.arm_a_client(str(spec_path))
            result = json.loads((session / "client-result.json").read_text())
            transcript = json.loads((session / "transcript.json").read_text()) if (session / "transcript.json").exists() else None
            helper_env = json.loads(env_dump.read_text()) if env_dump.exists() else None
            stderr_exists = (session / "helper.stderr").exists()
            leaked_tmp_files = sorted(p.name for p in session.iterdir() if p.name.endswith(".tmp"))
        return rc, result, transcript, helper_env, seen, spec, helper_cmd, stderr_exists, leaked_tmp_files

    def test_client_records_a_submit_refusal_and_keeps_qualification_metadata_out_of_the_helper(self):
        before = {k: os.environ.get(k) for k in ("CORE04_QUALIFICATION_RUN_ID", "CORE04_QUALIFICATION_CALLER_ID", "CORE04_STALE")}
        rc, result, transcript, helper_env, seen, spec, helper_cmd, stderr_exists, leaked = self.run_client("refuse-submit")
        self.assertEqual(rc, cmp_harness.ARM_A_REFUSED_RC)
        self.assertEqual(result["refusal"], {"code":"unsupported-capability", "message":"seeded workspace quota capability is unqualified"})
        self.assertEqual(result["refusal_stage"], "submit")
        self.assertNotIn("client_error", result)
        self.assertEqual(result["label"], cmp_harness.ARM_A_LABEL)
        self.assertEqual(result["hello"]["status"], "ok")
        self.assertEqual((result["submit"]["status"], result["submit"]["code"]), ("rejected", "unsupported-capability"))
        self.assertEqual(result["reservation"], {"reservation_bytes":4194304})
        self.assertEqual(result["manifest"]["resource_limits"]["memory_bytes"], cmp_harness.CAPS["memory.max"] + 4194304)
        self.assertEqual(result["manifest"]["env_allowlist"]["CMPMARK"], spec["marker"])
        self.assertEqual(result["helper_argv"], helper_cmd)
        self.assertEqual(result["transcript_frames"], 2)
        self.assertIn("finished_ns", result)
        self.assertNotIn("final_query", result)
        self.assertEqual(len(transcript), 2)
        self.assertEqual([t["request"]["operation"] for t in transcript], ["hello", "submit"])
        self.assertEqual([t["response"]["status"] for t in transcript], ["ok", "rejected"])
        self.assertEqual(transcript[1]["request"]["capability_digest"], result["manifest"]["identity_hash"])
        self.assertNotIn("capability_digest", transcript[0]["request"])
        self.assertTrue(stderr_exists)
        self.assertEqual(leaked, [])
        # The adapter got the helper path, the linux backend and the per-cell identity; the qualification env was already set for it.
        self.assertEqual(seen["verify"], {"backend":"linux-cgroupv2", "env":{"CORE04_QUALIFICATION_RUN_ID":"case9", "CORE04_QUALIFICATION_CALLER_ID":"qualification.case9"}})
        self.assertEqual(seen["command"]["args"], ("/fake/kogen-contain", "linux-cgroupv2"))
        self.assertEqual(seen["command"]["kwargs"], {"state_dir":spec["state_dir"], "caller_id":spec["caller_id"], "linux_config":spec["config"]})
        self.assertEqual(seen["command"]["env"], seen["verify"]["env"])
        # The helper itself runs without any CORE04_* variable but keeps the rest of the environment.
        self.assertFalse([k for k in helper_env if k.startswith("CORE04_")], helper_env)
        self.assertIn("CMP_PASSTHROUGH", helper_env)
        self.assertIn("PATH", helper_env)
        # arm_a_client leaves nothing behind in the process environment once the test's patch is undone.
        self.assertEqual({k: os.environ.get(k) for k in before}, before)

    def test_client_records_a_hello_refusal_before_building_a_manifest(self):
        rc, result, transcript, _, seen, _, _, _, _ = self.run_client("refuse-hello")
        self.assertEqual(rc, cmp_harness.ARM_A_REFUSED_RC)
        self.assertEqual(result["refusal"], {"code":"protocol-mismatch", "message":"no common version"})
        self.assertEqual(result["refusal_stage"], "hello")
        self.assertEqual(result["transcript_frames"], 1)
        self.assertEqual(len(transcript), 1)
        for absent in ("manifest", "submit", "reservation"): self.assertNotIn(absent, result)

    def test_client_returns_the_workload_exit_code_when_the_helper_accepts(self):
        rc, result, transcript, _, _, _, _, _, _ = self.run_client("accept")
        self.assertEqual(rc, 7)
        self.assertNotIn("refusal", result)
        self.assertNotIn("client_error", result)
        self.assertEqual(result["result"], {"termination":{"exit_code":7}})
        self.assertEqual(result["submit"]["payload"]["handle"], "h-1")
        self.assertEqual([t["request"]["operation"] for t in transcript], ["hello", "submit", "query"])
        self.assertEqual(transcript[2]["request"]["payload"], {"handle":"h-1"})
        self.assertEqual(result["transcript_frames"], 3)

    def test_client_host_verification_failure_is_a_client_error_without_a_helper(self):
        rc, result, transcript, helper_env, seen, _, _, stderr_exists, _ = self.run_client("accept", verify_error="linux-cgroupv2 requires a Linux host")
        self.assertEqual(rc, 71)
        self.assertIn("requires a Linux host", result["client_error"])
        self.assertNotIn("command", seen)
        self.assertNotIn("transcript_frames", result)
        self.assertIsNone(transcript)
        self.assertIsNone(helper_env)
        self.assertFalse(stderr_exists)
        self.assertNotIn("refusal", result)

    # Helpers and contracts around the client -------------------------------------------------------------------------------------
    def test_real_adapter_turns_the_clients_env_into_the_qualification_command(self):
        adapter = cmp_harness.arm_a_load_pinned("adapter.py")
        with mock.patch.dict(os.environ, {"CORE04_QUALIFICATION_RUN_ID":"case9", "CORE04_QUALIFICATION_CALLER_ID":"qualification.case9"}):
            cmd = adapter.backend_command("/h/kogen-contain", cmp_harness.ARM_A_BACKEND, state_dir="/abs/state", caller_id="ignored", linux_config="/abs/config.json")
        self.assertEqual(cmd, ["/h/kogen-contain", "--state-dir", "/abs/state", "--caller-id", "qualification.case9",
                               "--linux-config", "/abs/config.json", "--qualification", "--qualification-run-id", "case9"])
        self.assertEqual(cmp_harness.ARM_A_BACKEND, "linux-cgroupv2")

    def test_pinned_modules_match_their_sha256_and_tampering_is_refused(self):
        for name, pin in cmp_harness.ARM_A_PINS.items():
            with self.subTest(name=name):
                self.assertEqual(cmp_harness.sha_file(cmp_harness.ARM_A_VENDOR / name), pin)
        self.assertTrue(hasattr(self.validate, "manifest_digest"))
        with tempfile.TemporaryDirectory() as d:
            vendor = pathlib.Path(d)
            shutil.copy(cmp_harness.ARM_A_VENDOR / "validate.py", vendor / "validate.py")
            self.assertTrue(hasattr(cmp_harness.arm_a_load_pinned("validate.py", vendor), "validate_document"))
            with open(vendor / "validate.py", "ab") as f: f.write(b"\n# tampered\n")
            with self.assertRaises(RuntimeError) as ctx:
                cmp_harness.arm_a_load_pinned("validate.py", vendor)
            self.assertIn("differs from pin", str(ctx.exception))
            (vendor / "unpinned.py").write_text("x")
            with self.assertRaises(KeyError):
                cmp_harness.arm_a_load_pinned("unpinned.py", vendor)

    def test_object_identity_is_the_helpers_birth_pinned_format(self):
        with tempfile.TemporaryDirectory() as d:
            st = os.lstat(d)
            self.assertEqual(cmp_harness.arm_a_object_identity(d, btime=lambda p: (-1, 7)),
                             f"linux-dev.{st.st_dev:x}-ino.{st.st_ino:x}-btime.ffffffffffffffff.7")
            with self.assertRaises(RuntimeError): cmp_harness.arm_a_object_identity(d, btime=lambda p: (1, 1000000000))

    def test_roots_cell_dirs_and_object_identity_on_real_directories(self):
        original = cmp_harness.arm_a_statx_btime
        cmp_harness.arm_a_statx_btime = lambda p: (0x1234, 0x56)
        self.addCleanup(setattr, cmp_harness, "arm_a_statx_btime", original)
        with tempfile.TemporaryDirectory() as d:
            base = pathlib.Path(d); (base / "ro").mkdir(); (base / "usr").mkdir(); (base / "plain-file").write_text("x"); (base / "link").symlink_to(base / "ro", target_is_directory=True)
            st = os.lstat(base / "ro")
            self.assertEqual(cmp_harness.arm_a_object_identity(base / "ro"), f"linux-dev.{st.st_dev:x}-ino.{st.st_ino:x}-btime.1234.56")
            for bad in (base / "plain-file", base / "link"):
                with self.subTest(bad=bad.name):
                    with self.assertRaises(RuntimeError): cmp_harness.arm_a_object_identity(bad)
            tmpfs = base / "tmpfs"; tmpfs.mkdir()
            cell, dirs = cmp_harness.arm_a_cell_dirs("att1", "a-bash", "allowed_rw", 2, tmpfs=tmpfs)
            self.assertEqual(cell, tmpfs / "att1-a-bash-allowed_rw-r2")
            self.assertEqual(list(dirs), ["allowed", "home", "temp", "cache"])
            self.assertEqual(oct(os.lstat(cell).st_mode & 0o777), "0o755")
            for rid, path in dirs.items():
                with self.subTest(root=rid):
                    self.assertEqual(path, cell / rid)
                    self.assertEqual(oct(os.lstat(path).st_mode & 0o777), "0o700")
            with self.assertRaises(RuntimeError): cmp_harness.arm_a_cell_dirs("att1", "a-bash", "allowed_rw", 2, tmpfs=tmpfs)
            rows = cmp_harness.arm_a_roots(base / "ro", dirs, extra_read=(("usr", base / "usr"),))
            self.assertEqual([(r["root_id"], r["mode"]) for r in rows],
                             [("fx-readonly", "read"), ("usr", "read"), ("allowed", "write"), ("home", "write"), ("temp", "write"), ("cache", "write")])
            self.assertEqual(rows[0]["path"], str(base / "ro"))
            self.assertEqual(rows[2]["object_identity"], cmp_harness.arm_a_object_identity(dirs["allowed"]))
            self.assertEqual(len({r["object_identity"] for r in rows}), 6)

    def test_session_readers_pair_client_record_with_helper_recorded_reservation(self):
        self.assertEqual(cmp_harness.arm_a_read_session({"run_id":"r"}), {"label":cmp_harness.ARM_A_LABEL, "run_id":"r", "session_dir":None})
        with tempfile.TemporaryDirectory() as d:
            session = pathlib.Path(d); state = {"run_id":"r", "session_dir":str(session)}
            missing = cmp_harness.arm_a_read_session(state)
            self.assertIn("client_read_error", missing)
            self.assertFalse(missing["reservation_matches_helper"])
            self.assertIsNone(cmp_harness.arm_a_peek_scope_id(state))
            client = {"refusal":None, "result":{"termination":{"exit_code":0}}, "reservation":{"reservation_bytes":5000},
                      "submit":{"payload":{"process_scope_id":"s-under-qualification-1", "handle":"h-1"}}}
            (session / "client-result.json").write_text(json.dumps(client))
            (session / "state" / "a1").mkdir(parents=True); (session / "state" / "a1" / "linux.json").write_text(json.dumps({"memory_reservation_bytes":5000, "cgroup_path":"/c"}))
            got = cmp_harness.arm_a_read_session(state)
            self.assertTrue(got["reservation_matches_helper"])
            self.assertEqual((got["handle"], got["submit_scope_id"]), ("h-1", "s-under-qualification-1"))
            self.assertEqual(got["result"], client["result"])
            self.assertEqual(got["helper_recorded"][0]["cgroup_path"], "/c")
            self.assertEqual(cmp_harness.arm_a_peek_scope_id(state), "s-under-qualification-1")
            (session / "state" / "a2").mkdir(); (session / "state" / "a2" / "linux.json").write_text(json.dumps({"memory_reservation_bytes":5001}))
            self.assertFalse(cmp_harness.arm_a_read_session(state)["reservation_matches_helper"])
            (session / "client-result.json").write_text("not json")
            self.assertIsNone(cmp_harness.arm_a_peek_scope_id(state))

    def test_resolve_tools_lists_arm_a_files_only_when_present(self):
        with tempfile.TemporaryDirectory() as d:
            d = pathlib.Path(d); helper = d / "kogen-contain"; helper.write_text("x"); ro = d / "ro"; ro.mkdir(); (ro / "fx").write_text("x")
            vendor = d / "vendor"; vendor.mkdir(); (vendor / "adapter.py").write_text("x"); (vendor / "manifest.json").write_text("{}")
            with mock.patch.object(cmp_harness, "ARM_A_HELPER", helper), mock.patch.object(cmp_harness, "ARM_A_RO", ro), mock.patch.object(cmp_harness, "ARM_A_VENDOR", vendor):
                tools = cmp_harness.resolve_tools(require_all=False)
            arm_a = {k: v for k, v in tools.items() if k.startswith("arm-a-")}
            self.assertEqual(arm_a, {"arm-a-helper":helper, "arm-a-fx":ro / "fx", "arm-a-adapter":vendor / "adapter.py", "arm-a-manifest-schema":vendor / "manifest.json"})
            with mock.patch.object(cmp_harness, "ARM_A_HELPER", d / "none"), mock.patch.object(cmp_harness, "ARM_A_RO", d / "none-ro"), mock.patch.object(cmp_harness, "ARM_A_VENDOR", d / "none-vendor"):
                self.assertFalse([k for k in cmp_harness.resolve_tools(require_all=False) if k.startswith("arm-a-")])
                try: strict = cmp_harness.resolve_tools(require_all=True)
                except RuntimeError as exc: self.assertNotIn("arm-a", str(exc))
                else: self.assertFalse([k for k in strict if k.startswith("arm-a-")])


class ArmAReviewFixTests(unittest.TestCase):
    """Regressions for fail-closed result validation, status mapping and final-read order."""

    def _completed(self, outdir, arm, helper, scored_override=None):
        ev = {"arm":arm, "fixture":"allowed_rw", "rep":0, "launch_ok":False, "marker_seen":False, "observer_ok":True, "arm_a":helper}
        scored = cmp_harness.score("allowed_rw", ev); ev["scored_status"] = scored_override or scored
        ev["status"] = cmp_harness.arm_a_status(arm, scored, helper)
        path = outdir / "evidence" / arm / "allowed_rw" / "rep-0.json"; path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(ev, sort_keys=True, indent=2) + "\n")
        cmp_harness.append_jsonl(outdir / cmp_harness.LEDGER_NAME, {"event":"complete", "key":cmp_harness.cell_key(arm, "allowed_rw", 0),
                                 "status":ev["status"], "evidence":str(path), "evidence_sha256":cmp_harness.sha_file(path)})
        return ev

    START_FAILED = {"marker_seen":False, "client_returncode":70, "result":{"status":"uncertain", "termination":{"cause":"start-failed", "exit_code":None, "signal":None}, "error":{"code":"cleanup-uncertain"}}}

    def test_completed_a_bash_launch_failed_and_a_refused_cells_resume(self):
        with tempfile.TemporaryDirectory() as d:
            outdir = pathlib.Path(d)
            bash = self._completed(outdir, "a-bash", self.START_FAILED)
            self.assertTrue(bash["status"].startswith("LAUNCH-FAILED("))
            self.assertEqual(cmp_harness.saved_cell(outdir, "a-bash", "allowed_rw", 0)["status"], bash["status"])
            refused = self._completed(outdir, "a", {"refusal":{"code":"policy-violation", "message":"unregistered objects on private quota filesystem"}})
            self.assertEqual(refused["status"], "REFUSED(policy-violation: unregistered objects on private quota filesystem)")
            self.assertEqual(cmp_harness.saved_cell(outdir, "a", "allowed_rw", 0)["status"], refused["status"])

    def test_completed_arm_a_cell_with_tampered_scored_status_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            outdir = pathlib.Path(d)
            self._completed(outdir, "a-bash", self.START_FAILED, scored_override="BLOCKED")
            with self.assertRaises(RuntimeError): cmp_harness.saved_cell(outdir, "a-bash", "allowed_rw", 0)

    def _watcher(self, custody):
        w = cmp_harness.ArmAResourceWatcher("cmp-x.scope", {"unit":"cmp-x.scope", "cgroup_path":str(custody)}, "mark-1", {"session_dir":str(custody / "no-session")})
        w.cgroup_root = ""; return w

    def test_watcher_retains_process_read_eacces_even_after_a_later_success(self):
        with tempfile.TemporaryDirectory() as d:
            custody = pathlib.Path(d); cand = custody / "s-cand"; cand.mkdir(); (cand / "cgroup.procs").write_text("4242\n")
            calls = {"n":0}
            def fake_identity(pid):
                calls["n"] += 1
                if calls["n"] == 1:
                    exc = PermissionError(errno.EACCES, "Permission denied", f"/proc/{pid}/environ"); raise exc
                return {"pid":pid, "start":7, "ppid":1, "sid":1, "env":{"CMPMARK":"mark-1"}, "argv0":"mark-1", "exe":"/x/fx"}
            def fake_observe(pid, start, before_observation=None):
                live = self._live_stat(pid)
                return {"verified_identity":True, "cgroup_path":str(cand), "membership":{"read_error":None}, "before":live, "after":live}
            with mock.patch.object(cmp_harness, "read_proc_identity", fake_identity), mock.patch.object(cmp_harness, "observe_proc_cgroup", fake_observe), \
                    mock.patch.object(cmp_harness, "proc_stat_observation", self._live_stat):
                w = self._watcher(custody); w._locate(); self.assertIsNone(w.identity); w._locate()
            self.assertEqual(w.identity["cgroup_path"], str(cand))
            self.assertTrue([e for e in w.errors if e.startswith("process-read:4242:")], w.errors)

    def test_watcher_retains_membership_read_and_malformed_listing_failures(self):
        with tempfile.TemporaryDirectory() as d:
            custody = pathlib.Path(d); bad = custody / "s-bad"; bad.mkdir(); (bad / "cgroup.procs").mkdir()
            odd = custody / "s-odd"; odd.mkdir(); (odd / "cgroup.procs").write_text("12x\n")
            w = self._watcher(custody); w._locate()
            self.assertTrue([e for e in w.errors if e.startswith("membership-read:") and "s-bad" in e], w.errors)
            self.assertTrue([e for e in w.errors if e.startswith("malformed cgroup.procs:") and "s-odd" in e], w.errors)

    @staticmethod
    def _live_stat(pid):
        return {"pid":int(pid), "stat":{"pid":int(pid), "start":7, "state":"S", "ppid":1, "sid":1, "num_threads":1, "flags":0},
                "error":None, "error_errno":None, "error_path":None, "read_started_ns":1, "read_completed_ns":2}

    @staticmethod
    def _gone_stat(pid):
        exc = FileNotFoundError(errno.ENOENT, "No such file", f"/proc/{pid}/stat")
        return {"pid":int(pid), "stat":None, "error":repr(exc), "error_errno":errno.ENOENT, "error_path":f"/proc/{pid}/stat", "error_object":exc,
                "read_started_ns":1, "read_completed_ns":2}

    GOOD_ROW = {"pid":4242, "start":7, "ppid":1, "sid":1, "env":{"CMPMARK":"mark-1"}, "argv0":"mark-1", "exe":"/x/fx"}

    def _good_observe(self, cand):
        live = self._live_stat(4242)
        return lambda pid, start, before_observation=None: {"verified_identity":True, "cgroup_path":str(cand), "membership":{"read_error":None},
                                                            "before":live, "after":live}

    def test_watcher_treats_verified_process_exit_as_a_note_not_an_error(self):
        with tempfile.TemporaryDirectory() as d:
            custody = pathlib.Path(d); cand = custody / "s-cand"; cand.mkdir(); (cand / "cgroup.procs").write_text("4242\n")
            def gone(pid): raise FileNotFoundError(errno.ENOENT, "No such file", f"/proc/{pid}/environ")
            stats = iter([self._live_stat(4242), self._gone_stat(4242)])
            with mock.patch.object(cmp_harness, "read_proc_identity", gone), mock.patch.object(cmp_harness, "proc_stat_observation", lambda pid: next(stats)):
                w = self._watcher(custody); w._locate()
            self.assertEqual(w.errors, []); self.assertTrue([n for n in w.locate_notes if "verified-exit" in n], w.locate_notes)

    def _invalid_after_later_success(self, watcher):
        """A later successful location must not clear the earlier failure: the cell scores INVALID."""
        ev = cmp_harness.bool_evidence("mem_cap", True); ev.update(observer_errors=[], observer_ok=True)
        self.assertEqual(cmp_harness.score("mem_cap", ev), "ENFORCED")   # same evidence without the retained failure
        errors = cmp_harness.arm_a_watcher_observer_errors(watcher)
        ev.update(observer_errors=errors, observer_ok=not errors)
        return cmp_harness.score("mem_cap", ev)

    def test_watcher_unverified_enoent_is_retained_and_a_later_success_still_scores_invalid(self):
        # The review noted: environ ENOENT while /proc/PID/stat still shows the same live task is not a disappearance.
        with tempfile.TemporaryDirectory() as d:
            custody = pathlib.Path(d); cand = custody / "s-cand"; cand.mkdir(); (cand / "cgroup.procs").write_text("4242\n")
            calls = {"n":0}
            def flaky(pid):
                calls["n"] += 1
                if calls["n"] == 1: raise FileNotFoundError(errno.ENOENT, "No such file", f"/proc/{pid}/environ")
                return dict(self.GOOD_ROW)
            with mock.patch.object(cmp_harness, "read_proc_identity", flaky), mock.patch.object(cmp_harness, "proc_stat_observation", self._live_stat), \
                    mock.patch.object(cmp_harness, "observe_proc_cgroup", self._good_observe(cand)):
                w = self._watcher(custody); w._locate(); self.assertIsNone(w.identity); w._locate()
            self.assertEqual(w.identity["cgroup_path"], str(cand))
            self.assertTrue([e for e in w.errors if e.startswith("process-read:4242:") and "unverified:same-process-live" in e], w.errors)
            self.assertEqual(self._invalid_after_later_success(w), "INVALID(observer ok)")

    def test_watcher_identity_stat_eacces_in_cgroup_observation_is_retained(self):
        # The review noted: observe_proc_cgroup's before/after stat failure (EACCES) used to become only "locate-unverified".
        with tempfile.TemporaryDirectory() as d:
            custody = pathlib.Path(d); cand = custody / "s-cand"; cand.mkdir(); (cand / "cgroup.procs").write_text("4242\n")
            denied = {"pid":4242, "stat":None, "error":"PermissionError(13)", "error_errno":errno.EACCES, "error_path":"/proc/4242/stat"}
            live = self._live_stat(4242); calls = {"n":0}
            def observe(pid, start, before_observation=None):
                calls["n"] += 1
                if calls["n"] == 1: return {"verified_identity":False, "cgroup_path":str(cand), "membership":{"read_error":None}, "before":denied, "after":live}
                return {"verified_identity":True, "cgroup_path":str(cand), "membership":{"read_error":None}, "before":live, "after":live}
            with mock.patch.object(cmp_harness, "read_proc_identity", lambda pid: dict(self.GOOD_ROW)), mock.patch.object(cmp_harness, "proc_stat_observation", self._live_stat), \
                    mock.patch.object(cmp_harness, "observe_proc_cgroup", observe):
                w = self._watcher(custody); w._locate(); self.assertIsNone(w.identity); w._locate()
            self.assertEqual(w.identity["cgroup_path"], str(cand))
            self.assertTrue([e for e in w.errors if e.startswith("identity-before:4242:") and e.endswith(":13")], w.errors)
            self.assertEqual(self._invalid_after_later_success(w), "INVALID(observer ok)")

    def test_watcher_membership_enoent_needs_the_cgroup_to_be_gone(self):
        with tempfile.TemporaryDirectory() as d:
            custody = pathlib.Path(d); cand = custody / "s-cand"; cand.mkdir()   # no cgroup.procs file but the directory exists
            w = self._watcher(custody); self.assertIsNone(w._members(cand))
            self.assertTrue([e for e in w.errors if "cgroup still present" in e], w.errors)
            w2 = self._watcher(custody); self.assertIsNone(w2._members(custody / "s-gone"))
            self.assertEqual(w2.errors, []); self.assertTrue(w2.locate_notes)

    def _sampling_watcher(self, d, events_text, snapshot_events):
        cg = pathlib.Path(d) / "s-cand"; cg.mkdir(); (cg / "cgroup.events").write_text(events_text)
        w = self._watcher(pathlib.Path(d)); w.identity = {"cgroup_path":str(cg), "unit":"cmp-x.scope"}; st = cg.stat(); w.cg_object = (st.st_dev, st.st_ino)
        snap = {"ok":True, "path":str(cg), "files":{"cgroup.events":snapshot_events, "memory.peak":"268435456"}, "scope_identity":w.identity, "errors":[]}
        return w, cg, snap

    def test_watcher_final_needs_counters_read_after_a_populated_zero_read(self):
        with tempfile.TemporaryDirectory() as d:
            w, cg, snap = self._sampling_watcher(d, "populated 1\nfrozen 0\n", "populated 0\nfrozen 0\n")
            with mock.patch.object(cmp_harness, "arm_a_cgroup_snapshot", lambda *a, **k: dict(snap)):
                self.assertFalse(w._sample())
            self.assertFalse(w.final_captured); self.assertFalse([s for s in w.samples if s.get("final")])

    def test_watcher_final_after_two_zero_reads_on_the_same_cgroup_object(self):
        with tempfile.TemporaryDirectory() as d:
            w, cg, snap = self._sampling_watcher(d, "populated 0\nfrozen 0\n", "populated 0\nfrozen 0\n")
            with mock.patch.object(cmp_harness, "arm_a_cgroup_snapshot", lambda *a, **k: dict(snap)):
                self.assertTrue(w._sample())
            self.assertTrue(w.final_captured); self.assertEqual([s.get("final") for s in w.samples], [True])
        with tempfile.TemporaryDirectory() as d:
            w, cg, snap = self._sampling_watcher(d, "populated 0\n", "populated 0\n"); w.cg_object = (0, 0)
            with mock.patch.object(cmp_harness, "arm_a_cgroup_snapshot", lambda *a, **k: dict(snap)):
                self.assertTrue(w._sample())
            self.assertFalse(w.final_captured); self.assertEqual(w.samples[-1]["ok"], False)


if __name__ == "__main__":
    unittest.main(verbosity=2)
