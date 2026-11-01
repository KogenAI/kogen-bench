"""usage: regrade.py <clean lanes dir (lanes-7bf6990c/lanes)> <round dir> <tool dirs: go bin> <node bin>
Model-free regrade of every counted cell's final-tree.tar with the clean lanes tree (7bf6990c). Writes <R>/regrade-7bf6990c/<task>-<arm>.json; never touches the cells' own evaluation.json."""
import sys,os,json,pathlib
CLEAN,ROUND,GOBIN,NODEBIN=sys.argv[1:5]
R=pathlib.Path(ROUND)
sys.path.insert(0,CLEAN)
os.environ.update(LANES_DIR=CLEAN,PATH=GOBIN+':'+NODEBIN+':/usr/bin:/bin',GOMAXPROCS='2',GOPROXY='off',GOTOOLCHAIN='local',LANES_HEAVY_LOCK='off')
from lanes import grading
out=R/'regrade-7bf6990c';out.mkdir(exist_ok=True)
for tdir in sorted((R/'counted/cells').iterdir()):
    for arm in ('pin','main'):
        d=tdir/'r1'/arm;f=out/f'{tdir.name}-{arm}.json'
        if f.exists():continue
        task=grading.load_task(str(R/'tasks'/tdir.name))
        rec=grading.grade_archive(task,str(d/'final-tree.tar'))
        old=json.loads((d/'evaluation.json').read_text())
        f.write_text(json.dumps({'all_passed':rec.get('all_passed'),'infrastructure':rec.get('infrastructure'),'totals':rec.get('totals'),'old_all_passed':old.get('all_passed'),'old_totals':old.get('totals'),'fixture_repairs':rec.get('fixture_repairs')},sort_keys=True))
        print(tdir.name,arm,rec.get('all_passed'),old.get('all_passed'),rec.get('totals'),flush=True)
print('REGRADE-DONE',flush=True)
