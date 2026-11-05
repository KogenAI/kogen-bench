# Kill-group zombie probe: start a shell with a background child in its own group, SIGKILL the
# group, reap the shell, then poll kill(pid, 0) on the orphaned child for up to 5 s.
import os, signal, subprocess, sys, time
p = subprocess.Popen(["/bin/sh", "-c", "/bin/sleep 300 & echo $!; wait"], stdout=subprocess.PIPE, start_new_session=True)
gpid = int(p.stdout.readline())
os.killpg(p.pid, signal.SIGKILL)
p.wait()
t = time.time()
while time.time() - t < 5:
    try:
        os.kill(gpid, 0)
    except ProcessLookupError:
        print("ZPROBE PASS: killed group member gone after %.2fs" % (time.time() - t)); sys.exit(0)
    time.sleep(0.05)
try:
    st = open("/proc/%d/stat" % gpid).read().rsplit(")", 1)[1].split()[0]
except OSError:
    st = "?"
print("ZPROBE FAIL: killed group member %d still present after 5s, state %s" % (gpid, st)); sys.exit(1)
