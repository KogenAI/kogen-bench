#!/usr/bin/env python3
"""Check every fixed law by exhaustive bounded Apalache; never sample."""
import argparse
import json
import os
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path
from emit import name
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'shared'))
from replay import map_trace

TOOLS=Path('/opt/fv-tools')
def environment():
    env=os.environ.copy();java=TOOLS/'mise/installs/java/temurin-21.0.6+7.0.LTS'
    env.update(HOME=str(TOOLS/'quint-home'),QUINT_HOME=str(TOOLS/'quint-home/.quint'),JAVA_HOME=str(java),PATH=str(TOOLS/'mise/installs/node/22.14.0/bin')+':'+str(java/'bin')+':'+env.get('PATH','/usr/bin:/bin'),JVM_ARGS='-Xmx1800m -XX:ActiveProcessorCount=1',LANG='C.UTF-8')
    return env

def check(out,laws):
    backend=TOOLS/'quint/node_modules/.bin/quint'
    apalache=TOOLS/'quint-home/.quint/apalache-dist-0.62.1/apalache/bin/apalache-mc'
    started=time.monotonic();passed=0;server=None;log=None;deadline=started+70
    if not backend.exists() or not apalache.exists():
        print('FV-QUINT infrastructure error: pinned offline toolchain is missing');return 2,0,0
    try:
        with socket.socket() as sock:
            sock.bind(('localhost',0));port=sock.getsockname()[1]
        log=(out/'apalache-server.log').open('w')
        server=subprocess.Popen(['nice','-n','10',str(apalache),'server',f'--port={port}'],cwd=out,env=environment(),stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
        # Start one owned server per cycle and reuse it for all law checks.
        while True:
            if server.poll() is not None:raise RuntimeError('owned Apalache server exited; see apalache-server.log')
            try:
                with socket.create_connection(('localhost',port),timeout=.2):break
            except OSError:
                if time.monotonic()>started+20:raise RuntimeError('owned Apalache server failed to start')
                time.sleep(.1)
        failed=False
        for law in laws['laws']:
            lawid=name(law['id']);trace=out/('law-'+lawid+'.itf.json');trace.unlink(missing_ok=True)
            cmd=['nice','-n','10',str(backend),'verify','laws.qnt','--main','laws','--backend','apalache','--max-steps',str(laws['max_sequence_length']),'--apalache-version','0.62.1','--server-endpoint',f'localhost:{port}','--invariant','law_'+lawid,'--out-itf',str(trace)]
            remaining=deadline-time.monotonic()
            if remaining<=0:raise RuntimeError('check cycle exceeded 70-second backend cap')
            r=subprocess.run(cmd,cwd=out,env=environment(),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=remaining)
            (out/('law-'+lawid+'.log')).write_text(r.stdout)
            # Native diagnostics are the measured variable: default verbosity,
            # complete stdout/stderr, unchanged for success and failure alike.
            print(r.stdout,end='')
            if r.returncode==0:
                passed+=1;print('FV-LAW '+law['id']+' PASS exhaustive bound='+str(laws['max_sequence_length']))
            elif trace.exists():
                failed=True;print('FV-LAW '+law['id']+' FAIL counterexample:')
                map_trace(trace,json.loads((out/'ir.json').read_text()),laws,law['id'])
            else:
                raise RuntimeError('checker failed without a machine-readable counterexample')
        elapsed=time.monotonic()-started
        print(f'FV-QUINT exhaustive {"FAIL" if failed else "PASS"} bound={laws["max_sequence_length"]} laws={passed}/{len(laws["laws"])} seconds={elapsed:.3f}')
        return 1 if failed else 0,passed,elapsed
    except (OSError,RuntimeError,ValueError,KeyError,subprocess.TimeoutExpired) as ex:
        print('FV-QUINT infrastructure error:',ex);return 2,passed,time.monotonic()-started
    finally:
        if server is not None and server.poll() is None:
            os.killpg(server.pid,signal.SIGTERM)
            try:server.wait(timeout=3)
            except subprocess.TimeoutExpired:os.killpg(server.pid,signal.SIGKILL);server.wait()
        if log:log.close()

def main():
    p=argparse.ArgumentParser();p.add_argument('out',type=Path);p.add_argument('laws',type=Path);a=p.parse_args()
    laws=json.loads(a.laws.read_text());code,passed,seconds=check(a.out.resolve(),laws)
    print(f'FV-CHECK laws_ok={passed}/{len(laws["laws"])} seconds={seconds:.3f}');sys.exit(code)
if __name__=='__main__':main()
