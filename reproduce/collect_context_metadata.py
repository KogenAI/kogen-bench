#!/usr/bin/env python3
"""Read bounded public metadata from configured roots; emit source IDs, not paths.

Usage: VENUE PUBLIC_ROOT [--results-root DIR] [--event-root DIR]. All roots must
be inside PUBLIC_ROOT. Never pass a sealed, grader, production, or private root.
"""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path

from privacy import contains_private_path


def parse_args():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('venue',choices=['kogen-bench-us','kogen-bench-eu','studio'])
    parser.add_argument('public_root',type=Path)
    parser.add_argument('--results-root',action='append',default=[])
    parser.add_argument('--event-root',action='append',default=[])
    parser.add_argument('--state-root',action='append',default=[])
    parser.add_argument('--queue-file',type=Path)
    parser.add_argument('--status-file',type=Path)
    return parser.parse_args()


args=parse_args()
root=args.public_root.resolve()
studio=args.venue=='studio'


def inside_root(value):
    path=value if isinstance(value,Path) else Path(value)
    path=(root/path).resolve() if not path.is_absolute() else path.resolve()
    if not path.is_relative_to(root):
        raise ValueError('Configured metadata inputs must remain under PUBLIC_ROOT')
    return path


def configured(values,default):
    return [inside_root(v) for v in values] if values else [inside_root(default)]


result_roots=configured(args.results_root,'results')
event_roots=configured(args.event_root,'events')
state_roots=configured(args.state_root,'state') if studio else []
queue_file=inside_root(args.queue_file) if args.queue_file else inside_root('queue.jsonl')
status_file=inside_root(args.status_file) if args.status_file else inside_root('status.log')
out={'venue':args.venue,'manifests':[],'states':[],'queue':[],'events':[],'sources':[]}


def source_id(path):
    try:relative=path.resolve().relative_to(root).as_posix()
    except ValueError:relative=path.name
    return 'source-id-'+hashlib.sha256(relative.encode()).hexdigest()[:12]


def clean(value):
    if isinstance(value,dict):
        return {k:clean(v) for k,v in value.items() if k not in ('node','path','base_dir','profile','log','errors','final_text_head','session_id')}
    if isinstance(value,list):return [clean(v) for v in value]
    if isinstance(value,str) and (contains_private_path(value) or re.search(r'@|/Users/|/home/|/tmp/|resp_|\b(?:\d{1,3}\.){3}\d{1,3}\b',value)):return None
    return value


def record_source(path,raw):
    out['sources'].append({'source_id':source_id(path),'sha256':hashlib.sha256(raw).hexdigest()})


def public_manifests(search_root):
    stack=[(search_root,0)]
    while stack:
        directory,depth=stack.pop()
        manifest=directory/'manifest.json'
        if manifest.is_file():
            yield manifest
            continue
        if depth>=3:continue
        try:
            for entry in os.scandir(directory):
                if entry.name.startswith(('attempt-','grades','grading','sealed')) or entry.name in ['work','workspace','homes','logs','cells','state','runner','tools']:
                    continue
                if entry.is_dir(follow_symlinks=False):stack.append((Path(entry.path),depth+1))
        except OSError:pass


seen=set()
for search_root in result_roots:
    for path in public_manifests(search_root):
        if path in seen:continue
        seen.add(path)
        try:
            raw=path.read_bytes();manifest=json.loads(raw);started=manifest.get('started_at','')
            if not '2026-09-28'<=started<'2026-10-06':continue
            keep={k:manifest.get(k) for k in ['cell_id','experiment','harness','requested','observed','started_at','ended_at','timestamps','host','sandbox','workdir','wrapper','cli_version','runner','status','usage','wall_s','total_wall_s_all_attempts','attempts']}
            keep['alias']=path.parent.name;keep['venue']=args.venue;keep['sha256']=hashlib.sha256(raw).hexdigest();keep['source_id']=source_id(path);keep['attempt_boundaries']=[]
            for attempt in path.parent.glob('attempt-*/attempt.json'):
                info=json.loads(attempt.read_text());keep['attempt_boundaries'].append({k:info.get(k) for k in ['n','started_at','ended_at','run_started_at','run_ended_at']})
            profiles=list(path.parent.glob('attempt-*/sandbox.sb'))
            if profiles:keep['profile_sha256']=hashlib.sha256(profiles[-1].read_bytes()).hexdigest()
            keep['phase_boundaries']={}
            for event_file in path.parent.glob('attempt-*/kogen-out/events.jsonl'):
                for line in event_file.read_text().splitlines():
                    try:event=json.loads(line)
                    except ValueError:continue
                    phase={'setup:task-setup':'setup','gate_run':'gate'}.get(event.get('name'))
                    if event.get('event')=='phase_timing' and phase and isinstance(event.get('started_at'),int) and isinstance(event.get('finished_at'),int):
                        from datetime import datetime,timezone
                        keep['phase_boundaries'].setdefault(phase,[]).append({'start_utc':datetime.fromtimestamp(event['started_at']/1000,timezone.utc).isoformat().replace('+00:00','Z'),'end_utc':datetime.fromtimestamp(event['finished_at']/1000,timezone.utc).isoformat().replace('+00:00','Z')})
            out['manifests'].append(clean(keep))
        except (OSError,ValueError):pass

if studio:
    for state_root in state_roots:
        for path in state_root.glob('*.json'):
            try:
                state=json.loads(path.read_text())
                out['states'].append(clean({k:state.get(k) for k in ['name','cell_id','task','arm','harness','rep','suffix','block','start','end','conc_start','conc_end','cap_start','requeue_of','state']}))
            except (OSError,ValueError):pass
    if queue_file.is_file():
        raw=queue_file.read_bytes();record_source(queue_file,raw)
        for line in raw.splitlines():
            try:entry=json.loads(line);out['queue'].append(clean({k:entry.get(k) for k in ['name','task','arm','harness','rep','suffix','block']}))
            except ValueError:pass
    if status_file.is_file():
        raw=status_file.read_bytes();record_source(status_file,raw)
        for line in raw.decode(errors='replace').splitlines():
            match=re.match(r'(\S+) (START|END) (\S+) (.*)',line)
            if match:out['events'].append({'timestamp':match[1],'event':match[2],'cell':match[3],'values':dict(re.findall(r'(conc|cap|conc_at_end)=([0-9]+)',match[4])),'source':source_id(status_file)})
else:
    for event_root in event_roots:
        for path in list(event_root.glob('**/events.log'))+list(event_root.glob('**/*dispatch.log'))+list(event_root.glob('**/dispatch.jsonl')):
            try:raw=path.read_bytes();record_source(path,raw)
            except OSError:continue
            for line in raw.decode(errors='replace').splitlines():
                if path.suffix=='.jsonl':
                    try:
                        event=json.loads(line)
                        if event.get('event')=='launch' and event.get('exp'):
                            out['events'].append({'timestamp':event.get('at'),'event':'launch','cell':event['exp'],'values':{'active':str(event.get('active_before')),'cap':str(event.get('cap'))},'source':source_id(path)})
                    except (ValueError,KeyError):pass
                    continue
                match=re.match(r'(\S+) (start|launch|end|done) (\S+) (.*)',line)
                if not match:continue
                values=dict(re.findall(r'(running|active|total|cap|load)=([0-9.]+)',match[4]))
                fraction=re.search(r'(?:active|total)=[0-9]+/([0-9]+)',match[4]);exp=re.search(r'exp=(\S+)',line)
                if fraction:values['cap']=fraction[1]
                if 'total' in values:values['active']=values['total']
                out['events'].append({'timestamp':match[1],'event':match[2],'cell':exp[1] if exp else match[3],'values':values,'source':source_id(path)})

print(json.dumps(out))
