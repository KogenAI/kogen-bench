#!/bin/sh
# heavy-lab.sh: LAB COPY of hostbin/heavy.sh for build-speed E2/E3 (live hostbin untouched). Same lock core (flock,
# FIFO poll queue, arrival order); the policy is injected by the orchestrator instead of heavy.sh's command sniffing:
#   LAB_ARM   A exclusive for every Go lock user (live policy) | B shared for class small, exclusive for class large
#             | C as B, but class large runs shared too, capped at LAB_CAP concurrent large suites (slot files)
#   LAB_CLASS small|large   (set per command file by the orchestrator; "# lab-class:" first line of the file)
#   LAB_LOCKDIR             private lock dir (never /var/tmp)
#   heavy-lab.sh <command-file>   run it with /bin/sh in the current directory; exit status passes through
LD=${LAB_LOCKDIR:?LAB_LOCKDIR}; L=$LD/kogen-heavy.lock
mkdir -p "$LD"; for f in $L $LD/kogen-heavy.log; do [ -e $f ] || : > $f; done
[ -f "${1:-}" ] || { echo "heavy-lab.sh: no command file ${1:-}" >&2; exit 2; }
case "${LAB_ARM:?}:${LAB_CLASS:-small}" in
  A:*) M=ex;; B:small) M=sh;; B:large) M=ex;; C:*) M=sh;; *) echo "bad arm" >&2; exit 2;; esac
SLOT=; [ "$LAB_ARM:${LAB_CLASS:-small}" = C:large ] && SLOT=${LAB_CAP:-2}
exec /usr/bin/python3 -c 'import fcntl,os,sys,time,subprocess
fd=os.open(sys.argv[1],os.O_RDONLY); m=sys.argv[2]; cmd=sys.argv[3]; slots=int(sys.argv[4] or 0); cls=sys.argv[5]
ld=os.path.dirname(sys.argv[1]); logp=os.path.join(ld,"kogen-heavy.log")
def log(msg):
    open(logp,"a").write("%.3f %d %s %s %s\n"%(time.time(),os.getpid(),msg,cls,os.path.basename(os.path.dirname(cmd))+"/"+os.path.basename(cmd)))
log("wait-"+m+("-slot" if slots else ""))
sfd=None
if slots:   # cap: hold one of N slot files for the whole large suite (acquired before queueing for the shared lock)
    sf=[os.open(os.path.join(ld,"slot%d"%i),os.O_RDWR|os.O_CREAT,0o666) for i in range(slots)]
    while sfd is None:
        for f in sf:
            try: fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB); sfd=f; break
            except OSError: pass
        else: time.sleep(1)
qd=sys.argv[1]+".q"; os.makedirs(qd,exist_ok=True)
me=os.path.join(qd,"1-%017.6f-%d"%(time.time(),os.getpid())); open(me,"w").close()
def first():
    for e in sorted(os.listdir(qd)):
        try: os.kill(int(e.rsplit("-",1)[1]),0)
        except (OSError,ValueError):
            try: os.unlink(os.path.join(qd,e))
            except OSError: pass
            continue
        return os.path.join(qd,e)==me
    return True
while True:
    if first():
        try: fcntl.flock(fd,(fcntl.LOCK_EX if m=="ex" else fcntl.LOCK_SH)|fcntl.LOCK_NB); break
        except OSError: pass
    time.sleep(2)
try: os.unlink(me)
except OSError: pass
t=time.time(); log("run")
rc=subprocess.call(["/bin/sh",cmd])
log("end rc=%d %.1fs"%(rc,time.time()-t)); sys.exit(rc)' "$L" "$M" "$1" "$SLOT" "${LAB_CLASS:-small}"
