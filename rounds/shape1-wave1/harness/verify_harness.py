#!/usr/bin/env python3
"""Offline harness controls; these are pilots, never experiment measurements."""
import json
import tempfile
from pathlib import Path
from analyze import sign_test, wilcoxon
from run_shaper import audit_events
from score_cell import native, validity
from shape_common import ROOT, SEALED, LANGS, tool_env, write_json


def main():
    SEALED.mkdir(parents=True,exist_ok=True)
    work=Path(tempfile.mkdtemp(prefix='harness-controls-',dir=SEALED))
    result={'pilot':True,'native':{},'audit':{}}
    for label,command in [('clean','cat prompt.md'),('planted','cat /tmp/hidden/suite/test.py')]:
        events=work/(label+'.jsonl')
        events.write_text(json.dumps({'type':'item.completed','item':{'id':'x','type':'command_execution','command':command}})+'\n'+
                          json.dumps({'type':'turn.completed','usage':{'input_tokens':100,'cached_input_tokens':0,'output_tokens':20}})+'\n')
        result['audit'][label]=audit_events(events)
    assert result['audit']['clean']['flagged']==0
    assert result['audit']['planted']['flagged']==1
    assert sign_test([1]*6,[0]*6)['p_two_sided']==.03125
    assert sign_test([1,0],[1,0])['p_two_sided']==1
    assert wilcoxon([1]*5,[0]*5)['p_two_sided']==.0625
    assert wilcoxon([1,0],[0,1])['p_two_sided']==1
    for lang in LANGS:
        env=tool_env(work/lang/'cache')
        rows={}
        for variant in ['base','reference']:
            repo=work/lang/variant/'repo';(repo/'bin').mkdir(parents=True);(repo/'acceptance').mkdir()
            (repo/'bin/app').write_text('#!/bin/sh\nprintf "'+variant+'\\n"\n');(repo/'bin/app').chmod(0o700)
            if lang=='rust':
                (repo/'acceptance/src').mkdir()
                (repo/'acceptance/Cargo.toml').write_text('[package]\nname="shape-control"\nversion="0.1.0"\nedition="2024"\n')
                (repo/'acceptance/src/lib.rs').write_text('#[test]\nfn acceptance() {\n let o = std::process::Command::new(std::env::var("SHAPE_APP").unwrap()).output().unwrap();\n assert_eq!(o.stdout, b"reference\\n");\n}\n')
            elif lang=='go':
                (repo/'go.mod').write_text('module shapecontrol\n\ngo 1.27\n')
                (repo/'acceptance/control_test.go').write_text('package acceptance\nimport("os";"os/exec";"testing")\nfunc TestAcceptance(t *testing.T){o,e:=exec.Command(os.Getenv("SHAPE_APP")).Output();if e!=nil||string(o)!="reference\\n"{t.Fatalf("mismatch %s %v",o,e)}}\n')
            else:
                (repo/'acceptance/control.test.ts').write_text('import {expect,test} from "bun:test";\ntest("acceptance",()=>{const p=Bun.spawnSync([process.env.SHAPE_APP!]);expect(p.stdout.toString()).toBe("reference\\n")});\n')
            rows[variant]=native(repo,lang,env,work/lang/variant/'logs')
        result['native'][lang]={'base_assertion_failed':rows['base']['assertion_failure'],
                               'reference_passed':rows['reference']['passed'],'valid':validity(rows['base'],rows['reference']),
                               'results':rows}
        assert result['native'][lang]['valid'],lang
    write_json(work/'controls.json',result);write_json(ROOT/'results/harness-controls.json',result)
    print(json.dumps({'native':{l:r['valid'] for l,r in result['native'].items()},'audit_controls':'pass','paired_statistics':'pass'}))


if __name__=='__main__':main()
