import unittest
from unittest import mock
from lanes import common


class GroupGone(unittest.TestCase):
    def test_waits_for_a_member_that_exits_after_the_leader(self):
        probes = [None, None, None, ProcessLookupError()]
        def killpg(pgid, sig):
            self.assertEqual(sig, 0)
            r = probes.pop(0)
            if r: raise r
        with mock.patch.object(common.os, 'killpg', side_effect=killpg), \
                mock.patch.object(common.time, 'sleep') as sleep:
            common._require_group_gone(1234)
        self.assertEqual(probes, [])
        self.assertEqual(sleep.call_count, 3)

    def test_group_that_outlives_the_bound_is_custody_unknown(self):
        with mock.patch.object(common, 'GROUP_GONE_TIMEOUT_S', 0.2), \
                mock.patch.object(common.os, 'killpg') as killpg:
            with self.assertRaises(common.CustodyUnknown):
                common._require_group_gone(1234)
        self.assertGreater(killpg.call_count, 1)
        for call in killpg.call_args_list:
            self.assertEqual(call.args, (1234, 0))

    def test_permission_error_does_not_wait(self):
        with mock.patch.object(common.os, 'killpg', side_effect=PermissionError), \
                mock.patch.object(common.time, 'sleep') as sleep:
            with self.assertRaises(common.CustodyUnknown):
                common._require_group_gone(1234)
        sleep.assert_not_called()

    def test_gone_group_returns_at_once(self):
        with mock.patch.object(common.os, 'killpg', side_effect=ProcessLookupError), \
                mock.patch.object(common.time, 'sleep') as sleep:
            common._require_group_gone(1234)
        sleep.assert_not_called()


if __name__ == '__main__':
    unittest.main()
