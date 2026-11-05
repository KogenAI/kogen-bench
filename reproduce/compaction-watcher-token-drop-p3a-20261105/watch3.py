#!/usr/bin/env python3
"""Arm 2: transcript watcher (stdlib, no model calls). Tails one harness transcript by byte offset
and prints one JSON line per compaction entry:
  {"loop": <id>, "session": <id>, "harness": "claude"|"codex", "kind": ..., "at_line": n, "t": epoch}
Studio would turn that line into a re-serve flag for the loop. Usage:
  watch3.py --harness claude|codex --loop LOOP --file PATH [--poll 1.0] [--seconds N] [--from-start]
Cost model: one os.stat per poll when idle; reads only the bytes appended since the last offset;
a line is parsed only when it contains one of the marker substrings (cheap prefilter).
Identity: Claude entries carry sessionId (= file name) and cwd; Codex session_meta carries the thread
id and cwd. The launcher knows the loop id and the session id/cwd it started, so it passes --loop;
the watcher cannot learn the loop id from the transcript itself."""
import argparse, json, os, sys, time, resource

MARK = {'claude': ('compact_boundary', 'isCompactSummary'),
        'codex': ('"compacted"', 'context_compacted')}

def hit(h, d):
    if h == 'claude':
        if d.get('type') == 'system' and d.get('subtype') == 'compact_boundary': return 'compact_boundary'
        if d.get('type') == 'user' and d.get('isCompactSummary'): return 'isCompactSummary'
    else:
        p = d.get('payload') if isinstance(d.get('payload'), dict) else {}
        if d.get('type') == 'compacted': return 'compacted'
        if d.get('type') == 'event_msg' and p.get('type') == 'context_compacted': return 'context_compacted'

def main():
    a = argparse.ArgumentParser()
    a.add_argument('--harness', required=True); a.add_argument('--loop', required=True)
    a.add_argument('--file', required=True); a.add_argument('--poll', type=float, default=1.0)
    a.add_argument('--seconds', type=float, default=0); a.add_argument('--from-start', action='store_true')
    a.add_argument('--stats', action='store_true')
    o = a.parse_args()
    off = 0 if o.from_start else os.path.getsize(o.file)
    buf = b''; n = 0; polls = 0; reads = 0; nbytes = 0; t_end = time.time() + o.seconds if o.seconds else None
    r0 = resource.getrusage(resource.RUSAGE_SELF); w0 = time.time()
    sess = os.path.splitext(os.path.basename(o.file))[0]
    while True:
        polls += 1
        try: size = os.stat(o.file).st_size
        except FileNotFoundError: size = off
        if size < off: off, buf = 0, b''           # truncated / rotated
        if size > off:
            with open(o.file, 'rb') as f:
                f.seek(off); chunk = f.read(min(size - off, 4 << 20))  # 4 MiB cap per read; the rest on the next loop pass
            reads += 1; nbytes += len(chunk); off += len(chunk)
            buf += chunk
            *lines, buf = buf.split(b'\n')          # keep the partial last line
            for ln in lines:
                n += 1
                if not any(m.encode() in ln for m in MARK[o.harness]): continue
                try: d = json.loads(ln)
                except Exception: continue
                k = hit(o.harness, d)
                if k:
                    print(json.dumps(dict(loop=o.loop, session=sess, harness=o.harness, kind=k, at_line=n, t=time.time())), flush=True)
        if t_end and time.time() >= t_end: break
        if off < size: continue                      # more backlog, no sleep
        time.sleep(o.poll)
    if o.stats:
        r1 = resource.getrusage(resource.RUSAGE_SELF); wall = time.time() - w0
        cpu = (r1.ru_utime - r0.ru_utime) + (r1.ru_stime - r0.ru_stime)
        print(json.dumps(dict(stats=dict(wall_s=round(wall, 1), cpu_s=round(cpu, 4), cpu_pct=round(100 * cpu / wall, 3), polls=polls, reads=reads, bytes=nbytes, lines=n, maxrss_kb=r1.ru_maxrss // 1024))), flush=True)

if __name__ == '__main__': main()
