#!/usr/bin/env python3
"""read-outcome.py: read the outcome of one Build log (Lab C9, BUILD-FAILURES-2026-11-05 section 3).

Replaces the first-matching-line read in auto-requeue.sh
    grep -E -A4 '^(candidate|intent|shape)/' ~/logs/<slug>.log | head -6
with a reader of the Build's FINAL outcome.

usage: read-outcome.py <log> [<log> ...]      one TSV line per log:
    <log>\t<class>\t<code>\t<exit>\t<evidence>\t<chain of every stop seen, in order>

class  green          the Build landed or ended as "already present" (do not retry, do not count as failed)
       red            Kogen's final structured stop is <code> (phase/code, e.g. candidate/build_blocked)
       usage_limit    red whose final stop is a usage limit (the resumable class in auto-requeue.sh)
       none           no final structured stop: <code> is exit-<N> (process ended with EXIT=N and no stop line) or
                      no-exit (process gone; neither a success nor a diagnosed failure: check the host, never call it failed)

Rules (the three candidate fixes):
 (a) FINAL stop, not first: the last stop line `^(candidate|intent|shape|environment|executor|provider)/<code>` counts only
     if no `step approve|build|done`-style progress marker for a LATER phase follows it. A stop printed during shaping
     (intent/not_ready from an internal shaping retry) that is followed by `step approve`/`step build` is not final.
 (b) a `landed <slug> <sha>` line is success even if EXIT= is missing or non-zero (lost EXIT on a green Build).
 (c) EXIT=0 is success; intent/exists with EXIT=0 ("already present ... at HEAD") is done, not failed.
The reader never prints more than the stop line and one evidence line; it never reads or prints environment or credentials.
"""
import re
import sys

STOP = re.compile(r'^(candidate|intent|shape|environment|executor|provider)/([a-z_]+)')
STEP = re.compile(r'^step (shape|approve|build|done)\b')
LANDED = re.compile(r'^landed (\S+) ([0-9a-f]{7,40})\b')
EXITL = re.compile(r'^EXIT=(\d+)\s*$')
APPROVAL_REFUSED = re.compile(r'^no approval digest:')


def read(path, approval_marker=True):
    stop = None          # (line_no, phase/code, text)
    chain = []           # every stop code seen, in order
    progress_after = False  # a step approve/build marker seen after the last stop
    landed = None
    exit_code = None
    present = False
    last_step = None
    with open(path, errors='replace') as fh:
        for n, line in enumerate(fh, 1):
            line = line.rstrip('\n')
            m = STOP.match(line)
            if m:
                stop = (n, m.group(1) + '/' + m.group(2), line[:160])
                chain.append(stop[1])
                progress_after = False
                continue
            if approval_marker and APPROVAL_REFUSED.match(line) and last_step == 'approve':
                # approval refused without its own structured line ("no approval digest:" then the readiness report):
                # Kogen's stop for this is intent/not_ready; only used if no structured line follows it
                stop = (n, 'intent/not_ready', 'approval refused (no approval digest)')
                chain.append(stop[1] + '*')
                progress_after = False
                continue
            m = STEP.match(line)
            if m:
                last_step = m.group(1)
                if stop is not None and last_step in ('approve', 'build'):
                    progress_after = True
                continue
            m = LANDED.match(line)
            if m:
                landed = line[:120]
                continue
            m = EXITL.match(line)
            if m:
                exit_code = int(m.group(1))
                continue
            if 'already present' in line and 'HEAD' in line:
                present = True
    # (b) landed line wins over any missing/non-zero EXIT and over any earlier stop
    if landed:
        return 'green', 'landed', exit_code, landed, chain
    # (c) EXIT=0 is success; "already present at HEAD" is done
    if exit_code == 0:
        return 'green', 'exists' if (present or (stop and stop[1] == 'intent/exists')) else 'ok', 0, (stop[2] if stop else 'EXIT=0'), chain
    # (a) the final structured stop, unless later progress shows it was an internal retry notice
    if stop and not progress_after:
        cls = 'usage_limit' if stop[1].endswith('usage_limit') else 'red'
        return cls, stop[1], exit_code, stop[2], chain
    if exit_code is not None:
        return 'none', 'exit-%d' % exit_code, exit_code, ('last step: %s' % last_step if last_step else 'no step line'), chain
    return 'none', 'no-exit', None, ('last step: %s' % last_step if last_step else 'no step line'), chain


def main(argv):
    for p in argv:
        cls, code, ex, ev, chain = read(p)
        print('\t'.join([p, cls, code, '' if ex is None else str(ex), ev.replace('\t', ' '), '>'.join(chain)]))


if __name__ == '__main__':
    main(sys.argv[1:])
