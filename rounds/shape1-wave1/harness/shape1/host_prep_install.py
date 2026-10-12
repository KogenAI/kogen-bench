#!/usr/bin/env python3
"""Stage assigned overlays atop the current kit, without switching it."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
from <SERVER_ID> import ROOT, registration
from shape_common import LANGS, digest, write_json


def stage(host, tasks):
    reg, frozen = registration()
    source = Path('/benchmark-root/kits/current').resolve()
    if not (source/'.complete').is_file():
        raise RuntimeError('current kit incomplete')
    destination = source.parent/('core4-shape1-'+host+'-'+digest(reg)[:12])
    if destination.exists():
        raise RuntimeError('staged kit already exists')
    shutil.copytree(source, destination, symlinks=True)
    rows = []
    for task in tasks:
        archive = ROOT/'overlays'/('overlay-shape-'+task+'.tar')
        if digest(archive) != frozen['files'][str(archive.relative_to(ROOT))]:
            raise RuntimeError('overlay no longer registered')
        with tarfile.open(archive) as tar:
            for member in tar.getmembers():
                path = Path(member.name)
                if path.is_absolute() or '..' in path.parts or member.issym() or member.islnk():
                    raise RuntimeError('unsafe overlay path')
                if not (path.parts and path.parts[0] == 'tasks'):
                    raise RuntimeError('overlay touches lane code')
            for lang in LANGS:
                definition = destination/'tasks'/('shape-'+task+'-'+lang)
                if definition.exists():
                    raise RuntimeError('existing task would be replaced')
            # Registered overlays carry only the registered non-scoring stub;
            # extraction copies those bytes, never reads live hidden suites.
            tar.extractall(destination)
        for lang in LANGS:
            definition = destination/'tasks'/('shape-'+task+'-'+lang)
            metadata = json.loads((definition/'task.json').read_text())
            bundle = destination/'tasks'/metadata['base_bundle'] if 'base_bundle' in metadata else None
            if bundle is None:
                bundles = list((destination/'tasks/_bases').glob('shape-'+task+'-'+lang+'*.bundle'))
                if len(bundles)!=1:raise RuntimeError('ambiguous base bundle')
                bundle = bundles[0]
            if digest(bundle)!=metadata['base_bundle_sha256'] or digest(definition/'prompt.md')!=metadata['prompt_sha256_original']:
                raise RuntimeError('public overlay integrity failed')
            for path in [definition,*definition.rglob('*'),bundle]:
                os.chown(path,0,0)
                os.chmod(path,0o755 if path.is_dir() or path.stat().st_mode & 0o111 else 0o644)
        rows.append(dict(task=task,overlay_sha256=digest(archive),public_integrity=True,
                         grader='registered-non-scoring-stub'))
    # Retain every original bundle, as the existing installer does. The text
    # checksum manifest is regenerated, not inspected directly.
    bases = destination/'tasks/_bases'
    lines = [digest(p)+'  ./'+str(p.relative_to(bases)) for p in sorted(bases.rglob('*'))
             if p.is_file() and p.name!='MANIFEST.sha256']
    (bases/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
    if digest(source/'reproduce/sandbox-profile.sh')!=digest(destination/'reproduce/sandbox-profile.sh') or digest(source/'reproduce/run-lane.sh')!=digest(destination/'reproduce/run-lane.sh'):
        raise RuntimeError('pre-RC lane code changed')
    result = dict(host=host,previous_kit=str(source),staged_kit=str(destination),
                  switched=False,registration_sha256=digest(reg),overlays=rows)
    write_json(ROOT/'prep/install.json',result)
    print(json.dumps({'host':host,'overlay_stage':'PASSED','tasks':tasks}))


if __name__=='__main__':
    stage(sys.argv[1],sys.argv[2:])
