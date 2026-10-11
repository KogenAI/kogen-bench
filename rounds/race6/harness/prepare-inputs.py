#!/usr/bin/env python3
from pathlib import Path
from validity import tree_hash
from scoring_config import counts,scored_ids
from spec_split import verify
from briefs import render
from condition import ARMS
ROOT=Path(__file__).resolve().parent
def main():
    assert tree_hash(ROOT/'inputs',frozen=True)==(ROOT/'inputs.sha').read_text().strip()
    assert counts(ROOT)[0]['N_scored']==len(scored_ids(ROOT))==106
    verify(ROOT)
    expected={f'BRIEF-{a}.md':render(ROOT,a) for a in ARMS}
    expected['TARGET.md']='The hidden suite has 106 scored cases.\n'
    for name,text in expected.items():
        p=ROOT/name
        if (ROOT/'FREEZE.json').exists(): assert p.read_text()==text, f'frozen {name} changed'
        else: p.write_text(text)
    print('PASS race6 frozen inputs, split, 106 cases and briefs')
if __name__=='__main__':main()
