#!/usr/bin/env python3
"""Estimate APFS physical growth from distinct race 4 file versions and retention."""
import datetime
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
ARMS = ('rust', 'go', 'ts', 'ex')
BUILD = {'target', '_build', 'node_modules', '.venv', 'build', 'dist', 'ebin', 'obj'}


def files(root):
    source, build = {}, {}
    for base, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = [d for d in dirs if not (Path(base)/d).is_symlink()]
        for name in names:
            p = Path(base)/name
            if p.is_symlink():
                continue
            s = p.stat()
            rel = p.relative_to(root)
            # cp -p preserves times. Repeated versions of a relative path in
            # cp -c snapshots share physical blocks; charge that version once.
            key = (str(rel), s.st_size, s.st_mtime_ns)
            dest = build if rel.parts[0] in BUILD or (rel.parts[0] == 'deps' and any(part in BUILD for part in rel.parts[1:-1])) else source
            dest[key] = s.st_blocks * 512
    return source, build


def total(versions):
    return sum(versions.values())


def merge(maps):
    result = {}
    for m in maps:
        result.update(m)
    return result


def main():
    old = json.loads((ROOT/'evidence/race5-j3-logical-disk-defaults.json').read_text())
    measurements = []
    for wave in ('race4-st-a', 'race4-st-b'):
        root = ROOT.parent/wave
        for arm in ARMS:
            paths = sorted((root/'snapshots').glob('T+*m/'+arm))
            paths += [root/'snapshots/FINAL'/arm]
            versions = [files(p) for p in paths if p.is_dir()]
            if not versions:
                raise ValueError('No race 4 snapshots for ' + wave + '/' + arm)
            source = [v[0] for v in versions]; build = [v[1] for v in versions]
            peak_working = max(total(s)+total(b) for s,b in versions)
            peak_build = max(map(total,build))
            source_growth = max(0,total(merge(source))-max(map(total,source)))
            # Seven 5-minute build versions can be present at the exact 30-min
            # boundary. Add two peak versions as target/FINAL headroom.
            retained = max(total(merge(build[max(0,i-6):i+1])) for i in range(len(build)))
            extra_build = max(0,retained-peak_build) + 2*peak_build
            # Extrapolate observed 60-minute source growth to the three-hour cap.
            snapshot_growth = extra_build + 3*source_growth
            measurements.append(dict(wave=wave,arm=arm,peak_working_bytes=peak_working,
                peak_build_bytes=peak_build,retained_build_version_bytes=retained,
                source_growth_60m_bytes=source_growth,estimated_snapshot_growth_bytes=snapshot_growth,
                snapshot_bytes_per_arm=(snapshot_growth+36)//37))
    # A direct df clone probe is diagnostic, not an exclusive physical-growth
    # measurement: other jobs can change free space at the same time.
    probe_source = ROOT.parent/'race4-st-a/snapshots/T+055m/rust'
    before = shutil.disk_usage(ROOT).free
    with tempfile.TemporaryDirectory(prefix='.disk-clone-probe-',dir=ROOT) as tmp:
        subprocess.run(['cp','-c','-p','-R',str(probe_source),str(Path(tmp)/'clone')],check=True)
        after = shutil.disk_usage(ROOT).free
        clone_probe = dict(source=str(probe_source),free_before=before,free_after=after,
                           observed_df_delta_bytes=before-after,
                           apparent_bytes=int(subprocess.check_output(['du','-Ask',str(probe_source)],text=True).split()[0])*1024,
                           note='Concurrent host jobs can affect df delta; do not use this delta alone as wave growth.')
    payload = dict(measured_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        accounting='physical-growth-estimate', margin_percent=30,
        method='No historical df series in race4-st-a/b out/checks, setup, arms or CPU logs. Estimate APFS physical growth by charging distinct relative-path/size/mtime file versions once using st_blocks*512; cp -c shares repeated versions. Budget seven retained periodic build versions plus TARGET/FINAL headroom and extrapolate source changes from 60 to 180 minutes. Amortize retained physical growth over 37 snapshots. Include current live peak once; seed-cache APFS clones are shared. Metadata, allocator, compression and rewritten-identical-file uncertainty covered by 30% margin. Python uses the largest observed language estimate. Diagnostic df clone probe recorded separately.',
        arms=list(ARMS)+['py'],
        per_arm_working_bytes=max(m['peak_working_bytes'] for m in measurements),
        snapshot_bytes_per_arm=max(m['snapshot_bytes_per_arm'] for m in measurements),
        linux_per_arm_working_bytes=old['per_arm_working_bytes'],
        linux_snapshot_bytes_per_arm=old['snapshot_bytes_per_arm'],
        linux_method='Non-clone Linux copies reserve allocated working and snapshot bytes, only 3 periodic + TARGET + FINAL (5 copies).',
        clone_probe=clone_probe,measurements=measurements)
    print(json.dumps(payload,indent=2))

if __name__=='__main__':
    main()
