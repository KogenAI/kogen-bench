#!/usr/bin/env python3
"""Post-stop scoring waits until this host has no live race arm drivers."""
import re,time
from pathlib import Path
from processes import table
ROOT=Path(__file__).resolve().parent
def host_idle(rows=None):
    rows=table() if rows is None else rows
    return not any(re.search(r'/race[^ /]*/arm(?:-cont)?\.sh(?:\s|$)',cmd) for _,cmd in rows.values())
if __name__=='__main__':
    assert (ROOT/'DONE').exists(),'scoring before DONE prohibited'
    assert (ROOT/'snapshots/FINAL/SNAPSHOT_COMPLETE').exists(),'FINAL incomplete'
    while not host_idle():time.sleep(5)
