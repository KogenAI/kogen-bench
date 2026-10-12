#!/usr/bin/env python3
"""Finish staged preparation after the whole-slot hold; never launch cells."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from <SERVER_ID> import ROOT
from shape_common import digest, write_json
from linux_support import linux_gap_lock


def main(host, tasks):
    while not (ROOT/'prep/hold.json').exists():
        time.sleep(2)
    hold = json.loads((ROOT/'prep/hold.json').read_text())
    try:
        install = json.loads((ROOT/'prep/install.json').read_text())
        with linux_gap_lock():
            if hold['host']!=host or hold['held'] is not True:
                raise RuntimeError('wrong host hold')
            if digest('<ROOT>')!=hold['queue_sha256']:
                raise RuntimeError('queue changed')
            if Path('<ROOT>').read_text()!=hold['stop_payload']:
                raise RuntimeError('hold state changed')
            current = Path('/benchmark-root/kits/current')
            already_installed = install.get('switched') is True and str(current.resolve())==install['staged_kit']
            if not already_installed and str(current.resolve())!=install['previous_kit']:
                raise RuntimeError('current kit changed since staging')
            stage = Path(install['staged_kit'])
            if not (stage/'.complete').is_file():
                raise RuntimeError('incomplete staged kit')
            # Exact symlink-replacement mechanism from switch_kit.sh, with the
            # quiet-slot lock and stop state additionally checked here.
            if not already_installed:
                Path('<ROOT>').write_text(install['previous_kit']+'\n')
                temporary = current.with_name('current.new')
                if temporary.exists() or temporary.is_symlink():
                    raise RuntimeError('another kit switch is pending')
                temporary.symlink_to(stage)
                os.replace(temporary,current)
            install['switched']=True;install['switch_utc']=__import__('<SERVER_ID>').utc()
            write_json(ROOT/'prep/install.json',install)
        environment = dict(os.environ,SHAPE_SOURCE_ROOT=str(ROOT/'input'),
                           SHAPE_SEALED_ROOT=str(ROOT/'private'))
        process = subprocess.run(['/usr/bin/python3',str(ROOT/'<SERVER_ID>.py'),host,*tasks],env=environment)
        return process.returncode
    except Exception as exc:
        write_json(ROOT/'prep/controller-error.json',{'host':host,'error_type':type(exc).__name__})
        subprocess.run(['/usr/bin/python3',str(ROOT/'<SERVER_ID>.py'),'--release'],check=True)
        return 2


if __name__=='__main__':
    raise SystemExit(main(sys.argv[1],sys.argv[2:]))
