import subprocess,threading,unittest
from unittest import mock
from types import SimpleNamespace
from lanes import cell,common,dispatch
class ProcessCustody(unittest.TestCase):
 def test_cell_normal_exit_sends_no_post_reap_signal(self):
  c=object.__new__(cell.Cell);c.abort=threading.Event();c.cut=False;c.ws='/tmp';c.env={}
  proc=SimpleNamespace(pid=1234,returncode=0,wait=lambda timeout:0)
  with mock.patch.object(cell.subprocess,'Popen',return_value=proc),mock.patch.object(common,'_killpg') as send,mock.patch.object(common,'_require_group_gone') as gone:
   self.assertEqual(c._group(['fake'],None,None,None,10),(0,False));send.assert_not_called();gone.assert_called_once_with(1234)
 def test_runner_unknown_sets_stop_and_never_sends_post_reap_signal(self):
  proc=mock.Mock();proc.pid=1234;proc.returncode=0;proc.wait.return_value=0
  with mock.patch.object(dispatch.subprocess,'Popen',return_value=proc),mock.patch.object(common,'_killpg') as send,mock.patch.object(common,'_require_group_gone',side_effect=common.CustodyUnknown('fixture')):
   r=dispatch.Runner()
   with self.assertRaises(common.CustodyUnknown):r.run(['fake'])
   self.assertTrue(r.custody_unknown.is_set());self.assertTrue(r.stopped.is_set());send.assert_not_called()
 def test_timeout_signals_only_before_wait_reaps(self):
  p=SimpleNamespace(pid=1234,returncode=None)
  def wait():p.returncode=-9;return -9
  p.wait=wait; events=[]
  def send(pid,sig):self.assertIsNone(p.returncode);events.append(sig)
  with mock.patch.object(common,'_killpg',side_effect=send),mock.patch.object(common,'_require_group_gone') as gone,mock.patch.object(common.time,'sleep'):
   common._kill_group(p,grace_s=0)
  self.assertEqual(len(events),2);gone.assert_called_once_with(1234)
if __name__=='__main__':unittest.main()
