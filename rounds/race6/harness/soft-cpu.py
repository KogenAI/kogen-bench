#!/usr/bin/env python3
"""Soft process-tree CPU budget; one-second bursts, host-equal limits."""
import os,signal,subprocess,sys,time
def descendants(rows,root):
    seen={root}
    while True:
        extra={p for p,(pp,cpu) in rows.items() if pp in seen}-seen
        if not extra:return seen
        seen.update(extra)
def main():
    budget=float(sys.argv[1]);assert 0<budget<=2
    child=subprocess.Popen(sys.argv[2:],start_new_session=True);stopped=set()
    def resume():
        for p in stopped:
            try:os.kill(p,signal.SIGCONT)
            except ProcessLookupError:pass
        stopped.clear()
    def finish(sig,frame):
        resume()
        try:os.killpg(child.pid,sig)
        except ProcessLookupError:pass
    signal.signal(signal.SIGTERM,finish);signal.signal(signal.SIGINT,finish)
    try:
        while child.poll() is None:
            rows={}
            for line in subprocess.check_output(['ps','-axo','pid=,ppid=,pcpu='],text=True).splitlines():
                p,pp,cpu=line.split();rows[int(p)]=(int(pp),float(cpu))
            tree=descendants(rows,child.pid);usage=sum(rows[p][1] for p in tree if p in rows)/100
            if usage>budget:
                for p in tree:
                    try:os.kill(p,signal.SIGSTOP);stopped.add(p)
                    except ProcessLookupError:pass
                time.sleep(min(.8,max(.05,1-budget/usage)));resume()
            time.sleep(.2)
    except BaseException:
        resume()
        try:os.killpg(child.pid,signal.SIGTERM)
        except ProcessLookupError:pass
        try:child.wait(timeout=5)
        except subprocess.TimeoutExpired:
            try:os.killpg(child.pid,signal.SIGKILL)
            except ProcessLookupError:pass
            child.wait()
        raise
    finally:resume()
    sys.exit(child.wait())
if __name__=='__main__':main()
