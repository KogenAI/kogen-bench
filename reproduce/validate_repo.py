#!/usr/bin/env python3
"""Offline schema, coverage, link and privacy checks for the local repository."""
import csv, json, math, re, statistics, subprocess
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import unquote, urlsplit
from export_results import FIELDS
from privacy import contains_private_path
from pass_counts import collect_planned_task_pairs, markdown_tables, self_test as pass_count_self_test, validate_all_round_pages
from audit_round70_evidence import audit as audit_round70_evidence, self_test as round70_evidence_self_test
from r70_completeness import audit as audit_r70_completeness, self_test as r70_completeness_self_test
from validate_spec_snapshot import audit_snapshot as audit_spec_snapshot
from validate_release import read_round_label, round_date
from validation_policy import (
    has_standard_run_records,
    is_preparation_only_registration,
    spec_source_disclosed_unvendored,
    undocumented_unmatched_graded_ids,
)
from run_records import indexed_records, is_run_record_file
from missing_reasons import compact_encoding_issues, load_legend
from partitioned_jsonl import read_partitions
ROOT=Path(__file__).resolve().parents[1]
MISSING_REASON_CODES=load_legend(ROOT/'results/missing-reasons.json')
MAX_REPOSITORY_FILE_BYTES=10_000_000
# Recovered Rails snapshots are single-file Git bundles; keep their explicit cap below 50 MB.
MAX_RAILS_BASE_BUNDLE_BYTES=50_000_000
REGISTERED_ROUND_IDS=json.loads((ROOT/'rounds/index.json').read_text())
TRACKED_PATHS=set(subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0'))
TRACKED_ROUND_DIRS={parts[1] for name in TRACKED_PATHS if name.startswith('rounds/') for parts in [name.split('/')] if len(parts)>2}
errors=[]
blockers=[]
resolved_gates=[]

def unregistered_round_path(path):
    try:relative=Path(path).relative_to(ROOT)
    except ValueError:return False
    return len(relative.parts)>1 and relative.parts[0]=='rounds' and relative.parts[1] not in REGISTERED_ROUND_IDS
def check(condition,message):
    if not condition:errors.append(message)

def check_compact_encoding(rows,label,allow_legacy_single=False):
    for number,row in enumerate(rows,1):
        issues=compact_encoding_issues(row,MISSING_REASON_CODES,allow_legacy_single=allow_legacy_single)
        if issues:
            check(False,f'{label} row {number} has invalid missing-value encoding: {issues[0]}')
            return


PRIVACY_RULES = [
    ('Bearer token', re.compile(r'Bearer\s+eyJ', re.I)),
    ('JWT', re.compile(r'\beyJ[A-Za-z0-9_-]{20,}\.eyJ', re.I)),
    ('IPv4 address', re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')),
    ('email address', re.compile(r'\b[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}')),
    ('private hostname', re.compile(r'\b[\w.-]+\.local\b', re.I)),
    ('local user path', re.compile(r'/'+'Users'+r'/[A-Za-z0-9_.-]+/')),
    ('home path', re.compile(r'/'+'home'+r'/[a-z0-9_.-]+/')),
    ('API key', re.compile(r'\b(?:sk-|sk_)[A-Za-z0-9]{16,}')),
    ('UUID', re.compile(r'\b[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b', re.I)),
]
PUBLIC_GIT_EMAIL = 'almir.sarajcic'+'@'+'icloud.com'
EDITORIAL_RULES = [
    ('quoted conversation block', re.compile(r'(?im)^\s*>\s*(?:owner|participant|user)\b')),
    ('conversation attribution', re.compile(r'(?i)\b(?:owner|participant)\s+(?:said|asked|wrote|messaged|quoted)\b')),
    ('private-source artifact reference', re.compile(r'(?i)\b(?:corpus/|transcript\.jsonl|grade\.sh|test_hidden\.py|solution\.patch|reference\.patch)\b')),
    ('credential-like value', re.compile(r'(?i)\b(?:api[_ -]?key|secret|password|authorization)\s*[:=]\s*\S+')),
]
SPEC_PROTOCOL_ALLOWLIST = {
    ('spec/01-cli.md', 'private-source artifact reference'): [
        re.compile(r'(?im)^Transcript: <run dir>/transcript\.jsonl$'),
    ],
    ('spec/02-formats.md', 'private-source artifact reference'): [
        re.compile(r'(?im)^- .*runs/<run_id>/[^\n]*transcript\.jsonl[^\n]*$'),
    ],
    ('spec/06-non-goals.md', 'private-source artifact reference'): [
        re.compile(r'(?im)^- The contents of .{0,3}transcript\.jsonl.{0,3},.*$'),
    ],
    ('spec/04-provider.md', 'IPv4 address'): [
        re.compile(r'127\.0\.0\.1'),
    ],
    ('spec/04-provider.md', 'credential-like value'): [
        re.compile(r'(?i)authorization:\s*Bearer\s+<(?:token|access_token)>'),
    ],
    ('spec/CONFORMANCE.md', 'email address'): [
        re.compile(r'test@kogen\.invalid'),
    ],
}


TASK_SOURCE_TREE_RE=re.compile(r'^tasks/(?:_grader/|_bases/rails-[^/]+\.bundle$|[^/]+/(?:hidden|grader|base)/)')
TASK_REFERENCE_PATCH_EVIDENCE=re.compile(r'(?i)("evidence"\s*:\s*)\[\s*"hidden/solution\.patch"')
TASK_UPSTREAM_PATCH_PATH=re.compile(r'(?i)"upstream_path"\s*:\s*"tasks/[^"\n]+/solution\.patch"')
TASK_SEALED_PATCH_EVIDENCE=re.compile(r'(?i)"hidden/sealed/solution\.patch"')
TASK_COMPARISON_PATCH_PATH=re.compile(r'(?i)tasks/(?:rails-[^`|]+/hidden/sealed|[^`|]+)/solution\.patch')
# Exported task suites, graders and bases are third-party or grader source code: fixture
# emails, UUIDs, version-like dotted numbers and bench toolchain paths are expected there.
# Only credential and personal-path rules apply to them.
TASK_SOURCE_RULES={'Bearer token','JWT','local user path','home path','API key'}
SYNTHETIC_GIT_IDENTITIES={
    'bench@localhost',
    'bench@example.invalid',
    'r70-author@invalid.local',
    'task-author@example.invalid',
}


def publication_scan_findings(text, relative_path):
    findings=[]
    task_source=bool(TASK_SOURCE_TREE_RE.match(relative_path))
    if not task_source and contains_private_path(text):
        findings.append('private filesystem/archive path')
    rules=[('privacy',label,pattern) for label,pattern in PRIVACY_RULES if not task_source or label in TASK_SOURCE_RULES]
    if not task_source and Path(relative_path).suffix.lower() in {'.md','.json','.jsonl','.csv','.txt'}:
        rules.extend(('editorial',label,pattern) for label,pattern in EDITORIAL_RULES)
    for family,label,pattern in rules:
        allowances=SPEC_PROTOCOL_ALLOWLIST.get((relative_path,label),()) if relative_path.startswith('spec/') else ()
        allowed_spans=[match.span() for allowance in allowances for match in allowance.finditer(text)]
        if label=='private-source artifact reference' and (relative_path=='tasks/index.json' or (relative_path.startswith('tasks/rails-') and relative_path.endswith('/task.json'))):
            allowed_spans.extend(match.span() for match in TASK_REFERENCE_PATCH_EVIDENCE.finditer(text))
            allowed_spans.extend(match.span() for match in TASK_UPSTREAM_PATCH_PATH.finditer(text))
            allowed_spans.extend(match.span() for match in TASK_SEALED_PATCH_EVIDENCE.finditer(text))
        if label=='private-source artifact reference' and relative_path=='RAILS-AI-EVALS-COMPARISON.md':
            allowed_spans.extend(match.span() for match in TASK_COMPARISON_PATCH_PATH.finditer(text))
        for match in pattern.finditer(text):
            # The publication security note explicitly documents the author's
            # intentionally retained public Git identity. Allow it only there.
            if (
                label == 'email address'
                and relative_path == 'SECURITY-NOTES.md'
                and match.group(0).lower() == PUBLIC_GIT_EMAIL
            ):
                continue
            # Bundle provenance preserves these synthetic Git author addresses verbatim.
            # They use reserved/local domains and identify no person or reachable host.
            if label=='email address' and match.group(0).lower().split('@')[-1] in {
                address.split('@',1)[1] for address in SYNTHETIC_GIT_IDENTITIES
            } and match.group(0).lower() in SYNTHETIC_GIT_IDENTITIES:
                continue
            if label=='private hostname' and any(
                re.search(r'\b'+re.escape(address)+r'\b',text,re.I)
                and match.group(0).lower() in {address.split('@',1)[1],address.split('@',1)[1].split('.',1)[-1]}
                for address in SYNTHETIC_GIT_IDENTITIES
            ):
                continue
            if any(start<=match.start() and match.end()<=end for start,end in allowed_spans):
                continue
            findings.append(f'{family} rule: {label}')
            break
    return findings


def publication_scan_self_test():
    user_path='/'+'Users'+'/'+'private'+'/'+'workspace'
    if not publication_scan_findings(user_path,'spec/04-provider.md'):
        raise AssertionError('spec privacy scan failed to reject a local path')
    quoted='> owner: ' + 'private note'
    if not publication_scan_findings(quoted,'spec/example.md'):
        raise AssertionError('spec editorial scan failed to reject an owner quote')
    secret='Authorization: Bearer ' + 'sk-' + ('x'*24)
    if not publication_scan_findings(secret,'spec/04-provider.md'):
        raise AssertionError('spec privacy scan failed to reject a credential')
    protocol=('redirect_uri=http://'+'127.0'+'.0.1:1455/auth/callback\n'
              'authorization: Bearer <token>')
    if publication_scan_findings(protocol,'spec/04-provider.md'):
        raise AssertionError('the documented loopback and token placeholders should be allowed')
    email='test'+'@'+'kogen.invalid'
    if publication_scan_findings(email,'spec/CONFORMANCE.md'):
        raise AssertionError('the reserved conformance placeholder should be allowed')
    public_identity=PUBLIC_GIT_EMAIL
    if publication_scan_findings(public_identity,'SECURITY-NOTES.md'):
        raise AssertionError('the documented public Git identity should be allowed in SECURITY-NOTES.md')
    if not publication_scan_findings(public_identity,'README.md'):
        raise AssertionError('the public Git identity exception must not exempt other repository files')
    transcript='Transcript: <run dir>/transcript.jsonl'
    if publication_scan_findings(transcript,'spec/01-cli.md'):
        raise AssertionError('the documented public transcript filename should be allowed')
    if not publication_scan_findings(transcript,'README.md'):
        raise AssertionError('the protocol exception must not exempt the rest of the repository')


publication_scan_self_test()


spec_snapshot_errors,spec_fragment_count=audit_spec_snapshot(ROOT/'spec',ROOT/'EVIDENCE-MAP.md')
for error in spec_snapshot_errors:check(False,error)


HYPOTHESIS_PAGE_NAMES = {
    'F01':'f01-shape-intent-plan.md',
    'F02':'f02-isolation-landing-interface.md',
    'F03':'f03-harness-loop.md',
    'F04':'f04-models-routing.md',
    'F05':'f05-context-cache-jev.md',
    'F06':'f06-checks-review-recovery.md',
    'F07':'f07-tasks-method.md',
    'F08':'f08-language-spec.md',
    'F09':'f09-campfire-webstacks.md',
    'F10':'f10-agent-output.md',
    'F11':'f11-claim-reconciliation.md',
    'F12':'f12-lever-recipes.md',
    'F13':'f13-product-mechanisms.md',
    'F14':'f14-context-store-task-policy.md',
}
EXPECTED_HYPOTHESES={f'H{i:02d}' for i in range(1,154)}
ROUND_STATUS_RE=re.compile(r'STATUS: \*\*(VALID|CONFOUNDED|INVALID|INTERIM|WITHDRAWN|NOT-RUN|DESCRIPTIVE|INCOMPLETE|PILOT)\b')
SENSITIVE_FILENAMES={'auth.json','transcript.jsonl','test_hidden.py','grade.sh','solution.patch','reference.patch'}


def private_or_sealed_path(path):
    """Skip genuinely private artifacts; task grading inputs are public but agent-hidden."""
    try:
        relative = path.relative_to(ROOT)
    except ValueError:
        relative = path
    parts = tuple(part.lower() for part in relative.parts)
    if len(parts) >= 3 and parts[0] == 'tasks' and parts[2] in {'hidden', 'grader'}:
        return False
    return (
        path.name.lower() in SENSITIVE_FILENAMES
        or path.name.lower()=='private.md'
        or bool(set(parts) & {'sealed','author-private','author_private'})
    )


def public_markdown_files():
    for path in ROOT.rglob('*.md'):
        if unregistered_round_path(path):continue
        if '.git' in path.parts or path.is_symlink() or private_or_sealed_path(path):
            continue
        if 'sources' in path.parts and path!=ROOT/'sources/README.md':
            continue
        yield path


def read_jsonl(path, label, *, required=False):
    if not path.is_file():
        if required:check(False,'Missing required '+label+': '+str(path.relative_to(ROOT)))
        return []
    out=[]
    try:
        for line_no,line in enumerate(path.read_text().splitlines(),1):
            if not line.strip():continue
            try:out.append(json.loads(line))
            except json.JSONDecodeError:
                check(False,f'Malformed JSONL in {path.relative_to(ROOT)}:{line_no}')
    except OSError:
        check(False,'Cannot read '+label+': '+str(path.relative_to(ROOT)))
    return out


def markdown_anchor(value):
    value=re.sub(r'`([^`]*)`',r'\1',value)
    value=re.sub(r'\[([^]]+)\]\([^)]+\)',r'\1',value)
    value=re.sub(r'<[^>]+>','',value).strip().lower()
    value=re.sub(r'[^\w\- ]','',value,flags=re.UNICODE)
    return re.sub(r'\s+','-',value)


def markdown_anchors(text):
    anchors=set()
    counts=Counter()
    for match in re.finditer(r'^#{1,6}\s+(.+?)\s*#*\s*$',text,re.MULTILINE):
        base=markdown_anchor(match.group(1))
        counts[base]+=1
        anchors.add(base if counts[base]==1 else f'{base}-{counts[base]-1}')
    anchors.update(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)["\']',text,re.IGNORECASE))
    return anchors


def validate_markdown_links():
    for page in public_markdown_files():
        try:text=page.read_text()
        except OSError:
            check(False,'Cannot read Markdown page '+str(page.relative_to(ROOT)))
            continue
        anchors=markdown_anchors(text)
        for raw_target in re.findall(r'\]\(([^)]+)\)',text):
            target=raw_target.strip().strip('<>')
            parsed=urlsplit(target)
            if parsed.scheme or target.startswith('//'):
                continue
            dest=unquote(parsed.path)
            fragment=unquote(parsed.fragment)
            target_page=(page.parent/dest) if dest else page
            if not target_page.exists():
                check(False,f'Missing link {page.relative_to(ROOT)} -> {dest or target}')
                continue
            if fragment and target_page.is_file():
                try:target_anchors=anchors if target_page==page else markdown_anchors(target_page.read_text())
                except OSError:
                    check(False,'Cannot read linked page '+str(target_page.relative_to(ROOT)))
                    continue
                if fragment not in target_anchors:
                    check(False,f'Missing link anchor {page.relative_to(ROOT)} -> {target_page.relative_to(ROOT)}#{fragment}')


def validate_hypothesis_publication():
    register=ROOT/'hypotheses/README.md'
    findings=ROOT/'FINDINGS.md'
    if not register.is_file():
        check(False,'Missing hypothesis register: hypotheses/README.md')
        return
    register_text=register.read_text()
    definitions=defaultdict(list)
    owners={}
    for line_no,line in enumerate(register_text.splitlines(),1):
        cells=[cell.strip().strip('`*') for cell in line.strip().strip('|').split('|')]
        if not cells or not re.fullmatch(r'H\d{2,3}',cells[0]):
            continue
        hid=cells[0]
        definitions[hid].append(line_no)
        family=next((cell for cell in cells[1:] if re.fullmatch(r'F\d{2}',cell)),None)
        if family:owners[hid]=family
    observed=set(definitions)
    for hid in sorted(EXPECTED_HYPOTHESES-observed):check(False,'Hypothesis register is missing '+hid)
    for hid in sorted(observed-EXPECTED_HYPOTHESES):check(False,'Unknown hypothesis ID in register: '+hid)
    for hid,lines in definitions.items():
        if len(lines)!=1:check(False,f'Hypothesis {hid} appears {len(lines)} times in the register')
    for hid in sorted(EXPECTED_HYPOTHESES & observed):
        family=owners.get(hid)
        if family not in HYPOTHESIS_PAGE_NAMES:
            check(False,'Hypothesis has no valid family owner: '+hid)
            continue
        page=ROOT/'hypotheses'/HYPOTHESIS_PAGE_NAMES[family]
        if not page.is_file():
            check(False,'Missing hypothesis family page: '+str(page.relative_to(ROOT)))
        elif not re.search(rf'\b{hid}\b',page.read_text()):
            check(False,f'Hypothesis owner page does not contain {hid}: {page.relative_to(ROOT)}')
    if not findings.is_file():
        check(False,'Missing family findings page: FINDINGS.md')
    else:
        text=findings.read_text()
        headings=re.findall(r'^##\s+(F\d{2})\b',text,re.MULTILINE)
        for family in HYPOTHESIS_PAGE_NAMES:
            if headings.count(family)!=1:check(False,f'FINDINGS.md must contain exactly one {family} section')
        for idx,family in enumerate(headings):
            start=re.search(rf'^##\s+{family}\b.*$',text,re.MULTILINE)
            if not start:continue
            next_heading=re.search(r'^##\s+F\d{2}\b',text[start.end():],re.MULTILINE)
            end=start.end()+next_heading.start() if next_heading else len(text)
            section=text[start.start():end]
            for label in ('Hypothesis','What ran','Result','What it does not show','Evidence'):
                if not re.search(rf'\b{re.escape(label)}\b',section,re.IGNORECASE):
                    check(False,f'{family} FINDINGS section lacks the {label} paragraph')
    known=EXPECTED_HYPOTHESES
    for page in public_markdown_files():
        try:text=page.read_text()
        except OSError:continue
        for hid in set(re.findall(r'\bH\d{2,3}\b',text))-known:
            check(False,f'Orphan hypothesis reference {hid} in {page.relative_to(ROOT)}')


def round_index_ids(value):
    if isinstance(value,dict):
        return {str(k) for k in value}
    if isinstance(value,list):
        return {item if isinstance(item,str) else item.get('id') for item in value if isinstance(item,str) or (isinstance(item,dict) and isinstance(item.get('id'),str))}
    return set()


ROUND_FIELDS={'round','round_id','audit_round','public_round','public_round_id','source_round','source_round_id','rounds','round_ids'}


def round_refs(value):
    refs=set()
    if isinstance(value,dict):
        for key,item in value.items():
            if key in ROUND_FIELDS:
                if isinstance(item,str) and item and item!='unmapped':refs.add(item)
                elif isinstance(item,list):refs.update(x for x in item if isinstance(x,str) and x and x!='unmapped')
            else:refs.update(round_refs(item))
    elif isinstance(value,list):
        for item in value:refs.update(round_refs(item))
    return refs


def explicit_disposition(value):
    if not isinstance(value,dict):return False
    for key in ('alias','alias_of','round_alias','disposition','publication_disposition'):
        item=value.get(key)
        if isinstance(item,str) and item.strip():return True
        if isinstance(item,dict) and any(isinstance(v,str) and v.strip() for v in item.values()):return True
    return False


def validate_round_crosswalk(round_ids, cells, claims, crosswalk):
    known=set(round_ids)
    for rid in sorted(known):
        page=ROOT/'rounds'/rid/'README.md'
        if not page.is_file():check(False,'Round register ID has no page or alias: '+rid)
    sources=[('results/cells.jsonl',cells),('results/claim-ledger.jsonl',claims),('results/source-crosswalk/index.json',crosswalk)]
    for label,items in sources:
        for index,item in enumerate(items):
            refs=round_refs(item)
            if not refs:continue
            if not any(ref in known or (ROOT/'rounds'/ref/'README.md').is_file() for ref in refs):
                if not explicit_disposition(item):
                    check(False,f'{label} row {index+1} has no public round page or explicit disposition')
            for ref in refs:
                if ref in known or (ROOT/'rounds'/ref/'README.md').is_file():continue
                if not explicit_disposition(item):
                    check(False,f'{label} row {index+1} has unresolved round ID {ref!r}')

    for item in crosswalk:
        rid=item.get('round_id')
        declared=item.get('round_status')
        if rid not in known or declared not in {'VALID','CONFOUNDED','INVALID','INTERIM','WITHDRAWN','NOT-RUN','DESCRIPTIVE','INCOMPLETE','PILOT'}:continue
        page=ROOT/'rounds'/rid/'README.md'
        if page.is_file():
            found=ROUND_STATUS_RE.findall(page.read_text())
            if found and declared not in found:
                check(False,'Source-crosswalk lifecycle status differs from the round page: '+rid)

    mapped_export_keys=set()
    for item in crosswalk:
        identity=item.get('export_identity') or item.get('export_row') or item.get('public_identity')
        if isinstance(identity,dict):
            key=tuple(str(identity.get(field) or identity.get({'round':'round_id','rep':'repetition'}.get(field,'')) or '') for field in ('round','task','arm','rep','model','effort'))
            if any(key):mapped_export_keys.add(key)
        elif isinstance(identity,str):mapped_export_keys.add(identity)
    unmapped_rows=[]
    for index,item in enumerate(cells):
        if item.get('round') not in {'',None,'unmapped'}:continue
        key=tuple(str(item.get(field,'') or '') for field in ('round','task','arm','rep','model','effort'))
        if key not in mapped_export_keys and not item.get('cell_id'):
            unmapped_rows.append(index+1)
    if unmapped_rows:
        check(False,f'results/cells.jsonl has {len(unmapped_rows)} unmapped rows without exact crosswalk identities (first rows: {unmapped_rows[:5]})')

    # Round-level accounting must keep planned, started, finished, graded and ITT
    # populations in separate integer fields. A page may express them in a table
    # or a nearby JSON protocol record; counts are never inferred from one another.
    labels={
        'planned':re.compile(r'planned',re.I),
        'started':re.compile(r'identified scored starts|started|start count',re.I),
        'finished':re.compile(r'finished|completed',re.I),
        'graded':re.compile(r'officially graded|graded cells|graded count',re.I),
        'itt':re.compile(r'itt denominator|itt n|itt count',re.I),
    }
    disposition_unknown=defaultdict(set)
    disposition_records=defaultdict(list)
    count_fields={'planned':'planned_n','started':'started_n','finished':'finished_n','graded':'graded_n','itt':'itt_n'}
    for item in crosswalk:
        if item.get('record_role')!='round_disposition':continue
        rid=item.get('round_id')
        counts=item.get('lifecycle_counts')
        if not isinstance(rid,str) or not isinstance(counts,dict):continue
        disposition_records[rid].append(item)
        count_status=counts.get('count_status')
        for target,source in count_fields.items():
            if source not in counts:
                check(False,'Round disposition lacks '+source+': '+rid)
            elif isinstance(counts[source],int) and not isinstance(counts[source],bool):
                disposition_unknown[rid].discard(target)
            elif counts[source] is None and isinstance(count_status,str) and count_status.strip():
                disposition_unknown[rid].add(target)
            else:
                check(False,'Round disposition has an unlabelled non-integer '+source+': '+rid)
    for rid in sorted(known):
        directory=ROOT/'rounds'/rid
        candidates=[directory/name for name in ('README.md','MEASURED.md','PLAN.json','STATUS.json')]
        observed=defaultdict(list)
        for item in disposition_records.get(rid,[]):
            counts=item.get('lifecycle_counts') or {}
            for target,source in count_fields.items():
                value=counts.get(source)
                if isinstance(value,int) and not isinstance(value,bool):observed[target].append(value)
        for path in candidates:
            if not path.is_file():continue
            if path.suffix=='.json':
                try:content=json.loads(path.read_text())
                except (OSError,json.JSONDecodeError):continue
                stack=[content]
                while stack:
                    current=stack.pop()
                    if isinstance(current,dict):
                        for key,value in current.items():
                            normalized=key.lower().replace('_',' ')
                            if isinstance(value,int) and not isinstance(value,bool):
                                for name,pattern in labels.items():
                                    if pattern.search(normalized):observed[name].append(value)
                            else:stack.append(value)
                    elif isinstance(current,list):stack.extend(current)
            else:
                try:content=path.read_text()
                except OSError:continue
                for table_header,table_rows,_ in markdown_tables(content):
                    value_header=next((header for header in table_header if header.strip().lower() in {'n','count','value'}),None)
                    label_header=next((header for header in table_header if header!=value_header),None)
                    if not value_header or not label_header:continue
                    for row,_line in table_rows:
                        label=row.get(label_header,'')
                        value=row.get(value_header,'').strip().replace(',','')
                        if not re.fullmatch(r'\d+',value):continue
                        for name,pattern in labels.items():
                            if pattern.search(label):observed[name].append(int(value))
        missing=[name for name in labels if not observed[name] and name not in disposition_unknown[rid]]
        if missing:
            register_text=(ROOT/'rounds/README.md').read_text()
            if not is_preparation_only_registration(rid,register_text):
                check(False,f'Round {rid} lacks separate integer accounting fields: {", ".join(missing)}')
        for name,values in observed.items():
            if len(set(values))>1:check(False,f'Round {rid} has conflicting {name} counts: {sorted(set(values))}')

    # Source-crosswalk disposition rows form the planned-cell partition when
    # they include an exact cell identity and an integer count.
    grouped=defaultdict(list)
    for item in crosswalk:
        refs=round_refs(item)
        rid=next((ref for ref in refs if ref in known),None)
        if rid and explicit_disposition(item):grouped[rid].append(item)
    for rid,items in grouped.items():
        ids=[item.get('cell_id') or item.get('public_cell_id') or item.get('source_cell_id') for item in items]
        ids=[x for x in ids if isinstance(x,str) and x]
        if ids and len(ids)!=len(set(ids)):
            check(False,'Duplicate exact cell identity in source-crosswalk for '+rid)
    for rid,items in disposition_records.items():
        if len(items)>1:
            scopes=[(item.get('lifecycle_counts') or {}).get('count_status') for item in items]
            if any(not isinstance(scope,str) or not scope.strip() for scope in scopes) or len(scopes)!=len(set(scopes)):
                check(False,'Source-crosswalk has duplicate or unscoped round-disposition rows for '+rid)


def claim_cell_ids(claim):
    for key in ('cell_ids','exact_cell_ids','public_cell_ids','cells'):
        value=claim.get(key)
        if isinstance(value,list):return [item for item in value if isinstance(item,str)]
    return []


def claim_status(claim):
    return str(claim.get('publication_status') or claim.get('status') or claim.get('analysis_status') or '').strip().lower()


def wilson_interval(successes,total,level=0.95):
    if total<=0:return None
    # The publication contract uses a two-sided normal quantile for the
    # registered confidence level; the common 95% value is kept explicit.
    z={0.90:1.6448536269514722,0.95:1.959963984540054,0.99:2.5758293035489004}.get(float(level))
    if z is None:return None
    p=successes/total
    denom=1+z*z/total
    center=(p+z*z/(2*total))/denom
    half=z*math.sqrt((p*(1-p)+z*z/(4*total))/total)/denom
    return center-half,center+half


def exact_binomial_two_sided(n,observed,p=0.5):
    if n<0 or observed<0 or observed>n:return None
    probabilities=[math.comb(n,k)*(p**k)*((1-p)**(n-k)) for k in range(n+1)]
    threshold=probabilities[observed]
    return min(1.0,sum(value for value in probabilities if value<=threshold+1e-15))


def fisher_exact_two_sided(a,b,c,d):
    if min(a,b,c,d)<0:return None
    row1=a+b;row2=c+d;col1=a+c;total=row1+row2
    if total==0:return None
    lo=max(0,col1-row2);hi=min(row1,col1)
    def probability(x):
        return math.comb(col1,x)*math.comb(total-col1,row1-x)/math.comb(total,row1)
    observed=probability(a)
    return min(1.0,sum(probability(x) for x in range(lo,hi+1) if probability(x)<=observed+1e-15))


def compare_reported_number(claim_id,label,reported,derived):
    if isinstance(reported,(int,float)) and isinstance(derived,(int,float)):
        if not math.isclose(float(reported),float(derived),rel_tol=1e-6,abs_tol=1e-9):
            check(False,f'Claim {claim_id} {label} differs from public records')


def validate_claims_and_records(claims, cells, run_records, crosswalk):
    claim_ids=[row.get('claim_id') for row in claims]
    if any(not isinstance(cid,str) or not cid for cid in claim_ids):
        check(False,'Claim ledger contains a row without a stable claim_id')
    duplicates=[cid for cid,count in Counter(cid for cid in claim_ids if isinstance(cid,str) and cid).items() if count>1]
    for cid in duplicates:check(False,'Duplicate stable claim_id: '+cid)
    for row in claims:
        required=('schema_version','claim_id','round_id','metric','claim_status','publication_status','evidence_status','analysis_rule','exact_cell_ids','numerator','denominator')
        absent=[key for key in required if key not in row]
        if absent:check(False,'Claim row lacks declared fields: '+str(row.get('claim_id','(missing ID)'))+' ('+', '.join(absent)+')')
        if not isinstance(row.get('analysis_rule'),str) or not row.get('analysis_rule').strip():
            check(False,'Claim lacks an explicit analysis rule: '+str(row.get('claim_id','(missing ID)')))
        if not isinstance(row.get('evidence_status'),str) or not row.get('evidence_status').strip():
            check(False,'Claim lacks an evidence status: '+str(row.get('claim_id','(missing ID)')))
    # Preserve and diagnose immutable identities instead of silently choosing a
    # duplicate attempt or treating a missing official grade as a failure.
    record_ids=[row.get('cell_id') for row in run_records if isinstance(row.get('cell_id'),str) and row.get('cell_id')]
    duplicate_records=[key for key,count in Counter(record_ids).items() if count>1]
    for cid in duplicate_records:check(False,'Duplicate captured run-record identity: '+cid)
    official_by_id=defaultdict(list)
    for row in cells:
        cid=row.get('cell_id')
        if isinstance(cid,str) and cid:official_by_id[cid].append(row)
    for cid,matched in official_by_id.items():
        if len(matched)>1:check(False,'Duplicate official cell identity: '+cid)

    crosswalk_by_id={}
    crosswalk_status_by_id=defaultdict(list)
    crosswalk_by_export_key={}
    for item in crosswalk:
        ids=[item.get(key) for key in ('cell_id','public_cell_id','source_cell_id','source_record_id')]
        ids.extend(item.get('linked_cell_ids') or [])
        for cid in ids:
            if isinstance(cid,str) and cid:
                crosswalk_by_id[cid]=item
                crosswalk_status_by_id[cid].append(item)
        identity=item.get('export_identity') or item.get('export_row') or item.get('public_identity')
        if isinstance(identity,dict):
            key=tuple(str(identity.get(field) or identity.get({'round':'round_id','rep':'repetition'}.get(field,'')) or '') for field in ('round','task','arm','rep','model','effort'))
            if any(key):crosswalk_by_export_key[key]=item
    run_by_id={row.get('cell_id'):row for row in run_records if isinstance(row.get('cell_id'),str) and row.get('cell_id')}
    run_record_source_by_id={
        cell_id:f"results/run-records/{row['round_id'] if isinstance(row.get('round_id'),str) else 'unassigned'}.jsonl"
        for cell_id,row in run_by_id.items()
    }
    for item in crosswalk:
        if item.get('record_role')!='captured_delivery':continue
        source_id=item.get('source_record_id')
        expected_path=run_record_source_by_id.get(source_id)
        if expected_path:
            check(item.get('source_file')==expected_path,'Captured-delivery crosswalk path does not match indexed run records: '+str(source_id))
        elif is_run_record_file(item.get('source_file')):
            check(False,'Captured-delivery crosswalk references an ID absent from indexed run records: '+str(source_id))
    for row in cells:
        if isinstance(row.get('cell_id'),str) and row['cell_id']:continue
        key=tuple(str(row.get(field,'') or '') for field in ('round','task','arm','rep','model','effort'))
        crosswalk_item=crosswalk_by_export_key.get(key)
        if crosswalk_item:
            cid=crosswalk_item.get('cell_id') or crosswalk_item.get('public_cell_id') or crosswalk_item.get('source_cell_id')
            if isinstance(cid,str) and cid:official_by_id[cid].append(row)
    if cells and not any(row.get('cell_id') for row in cells) and not crosswalk_by_export_key:
        check(False,'Official outcome export has no immutable cell IDs and no exact export-identity mappings in source-crosswalk')
    unmatched_graded=[]
    for cid,row in run_by_id.items():
        matches=official_by_id.get(cid,[])
        official_crosswalk=[item for item in crosswalk_status_by_id.get(cid,[]) if (item.get('record_role') in {'official_outcome_export_row','official_test_count'} and item.get('linkage_status') in {'exact_cell_id_crosswalk_anchor','exact_cell_id_to_test_count'}) or (item.get('record_role')=='captured_delivery' and item.get('linkage_status') in {'exact_official_grade_join','capture_reported_identity_mapping'})]
        if not matches and not official_crosswalk:
            # An ungraded surviving delivery is expected to have no official grade.
            if row.get('graded') is True:
                unmatched_graded.append(cid)
            continue
        if matches:
            official=matches[0]
            if isinstance(official.get('round'),str) and isinstance(row.get('audit_round'),str) and official['round'] not in {row['audit_round'],row.get('round_id')}:
                check(False,'Official/captured round lifecycle mismatch for '+cid)
            outcome=row.get('outcome')
            if isinstance(outcome,dict):outcome=outcome.get('result') or outcome.get('value')
            if isinstance(outcome,str) and outcome in {'pass','fail','invalid'} and official.get('outcome') not in {outcome,'unknown'}:
                check(False,'Official/captured outcome lifecycle mismatch for '+cid)
    if unmatched_graded:
        undocumented=undocumented_unmatched_graded_ids(unmatched_graded,crosswalk)
        if undocumented:
            check(False,f'{len(undocumented)} of {len(unmatched_graded)} captured graded records without an exact outcome join lack an explicit unresolved source-crosswalk disposition')
        else:
            blockers.append(f'{len(unmatched_graded):,} captured graded records remain without an exact official-grade ID join')

    unresolved_capture_ids={
        item.get('source_record_id')
        for item in crosswalk
        if item.get('record_role')=='captured_delivery'
        and is_run_record_file(item.get('source_file'))
        and item.get('linkage_status') in {'unresolved_no_shared_exact_cell_id','capture_reported_identity_mapping'}
        and isinstance(item.get('source_record_id'),str)
    }
    outcome_metrics={'pass_rate','full_pass_rate','pass_count','passes','official_full_pass','smoke_test_fraction','cost_per_pass','usd_per_pass','cost_per_success','mean_wall','median_wall','wall_s','wall_time','wall_summary'}
    verified_statuses={'verified','reconciled','publishable','headline','released','supported'}
    for claim in claims:
        exact_ids=set(claim_cell_ids(claim))
        status=claim_status(claim)
        publication=str(claim.get('publication_status') or '').strip().lower()
        metric=str(claim.get('metric') or claim.get('measure') or '').lower().replace('-','_')
        marked_verified=status in verified_statuses or publication in verified_statuses
        if marked_verified and metric in outcome_metrics and exact_ids.intersection(unresolved_capture_ids):
            check(False,'Verified outcome claim depends on an unresolved captured delivery: '+str(claim.get('claim_id','(missing ID)')))

    # A claim cannot be marked publishable when its exact records are unresolved.
    bad_cells={}
    for row in cells:
        bad=(row.get('round') in {'','unmapped',None} or row.get('ITT outcome') in {'unresolved','not_scored'})
        if bad:
            cid=row.get('cell_id')
            if isinstance(cid,str):bad_cells[cid]=row
    releasable={'verified','reconciled','publishable','headline','released','supported'}
    for claim in claims:
        status=claim_status(claim)
        ids=claim_cell_ids(claim)
        if status in releasable:
            if not ids:
                check(False,'Claim marked publishable without exact cell IDs: '+str(claim.get('claim_id','(missing ID)')))
            affected=[cid for cid in ids if cid in bad_cells]
            if affected:
                check(False,'Claim marked publishable while linked cells have unresolved round/ITT fields: '+str(claim.get('claim_id','(missing ID)')))

    # Recalculate the count and common resource summaries only when their exact
    # inputs are present. A source-reported claim may remain unreconciled, but it
    # cannot be marked verified when the public inputs do not support a replay.
    cell_map={row.get('cell_id'):row for row in cells if isinstance(row.get('cell_id'),str)}
    test_count_rows=read_jsonl(ROOT/'results/test-counts.jsonl','Round 70 test-count ledger')
    test_count_map={row.get('cell_id'):row for row in test_count_rows if isinstance(row.get('cell_id'),str)}
    run_map=run_by_id
    resource_rows=read_jsonl(ROOT/'results/cost-time.jsonl','cost/time ledger')
    cost_map={row.get('cell_id'):row for row in resource_rows if isinstance(row.get('cell_id'),str)}
    multiplicity_families=defaultdict(list)
    for claim in claims:
        cid=str(claim.get('claim_id') or '(missing ID)')
        status=claim_status(claim)
        ids=claim_cell_ids(claim)
        metric=str(claim.get('metric') or claim.get('measure') or '').lower().replace('-','_')
        numerator=claim.get('numerator')
        denominator=claim.get('denominator')
        reproducible=bool(ids) and all(item in cell_map for item in ids)
        selected=[cell_map[item] for item in ids if item in cell_map]
        observed=sum(row.get('ITT outcome')=='pass' for row in selected)
        scored=sum(row.get('ITT outcome') in {'pass','fail'} for row in selected)
        exact_test_rows=[test_count_map[item] for item in ids if item in test_count_map]
        test_ledger_complete=bool(ids) and len(exact_test_rows)==len(ids)
        evidence_status=str(claim.get('evidence_status') or '').lower()
        if metric in {'pass_rate','full_pass_rate','pass_count','passes','official_full_pass'} and test_ledger_complete:
            exact_test_rows=[row for row in exact_test_rows if row.get('scored') is True]
            observed=sum(row.get('outcome')=='pass' for row in exact_test_rows)
            scored=len(exact_test_rows)
            reproducible=True
        elif metric=='smoke_test_fraction' and test_ledger_complete:
            observed=sum(row.get('tests_passed',0) for row in exact_test_rows)
            scored=sum(row.get('tests_total',0) for row in exact_test_rows)
            reproducible=True
        elif metric=='candidate_delivery_capture' and ids and all(item in run_map for item in ids):
            observed=len(ids);scored=len(ids);reproducible=True
        elif metric=='unmatched_ungraded_delivery_count' and ids and all(item in run_map for item in ids):
            observed=len(ids);scored=len(ids);reproducible=True
        if metric in {'pass_rate','full_pass_rate','pass_count','passes','official_full_pass','smoke_test_fraction','candidate_delivery_capture','unmatched_ungraded_delivery_count'} and reproducible:
            if isinstance(numerator,int) and numerator!=observed:check(False,f'Claim {cid} numerator differs from exact official outcomes')
            if isinstance(denominator,int) and denominator!=scored:check(False,f'Claim {cid} denominator differs from exact public records')
            values=claim.get('reported_values') or {}
            if metric=='official_full_pass':
                if values.get('full_passes')!=observed or values.get('graded_scored_cells')!=scored:
                    check(False,'Claim '+cid+' reported values differ from exact test-count rows')
            elif metric=='smoke_test_fraction':
                if values.get('tests_passed')!=observed or values.get('tests_total')!=scored:
                    check(False,'Claim '+cid+' reported smoke fraction differs from exact test-count rows')
                if values.get('scored') is not False:
                    check(False,'Smoke diagnostic claim is not explicitly marked unscored: '+cid)
        if metric in {'cost_per_pass','usd_per_pass','cost_per_success'} and ids and all(item in cost_map for item in ids):
            passes=sum(cell_map.get(item,{}).get('ITT outcome')=='pass' for item in ids)
            values=[cost_map[item].get('cost_usd') for item in ids]
            if passes and all(isinstance(value,(int,float)) and math.isfinite(value) for value in values):
                derived=sum(values)/passes
                reported=claim.get('value')
                if isinstance(reported,(int,float)) and not math.isclose(reported,derived,rel_tol=1e-6,abs_tol=1e-9):
                    check(False,f'Claim {cid} cost/pass differs from public cost/time rows')
            elif status in releasable:
                check(False,f'Claim {cid} cost/pass is marked publishable without complete cost and pass rows')
        if metric in {'mean_wall','median_wall','wall_s','wall_time','wall_summary'} and ids and all(item in cost_map for item in ids):
            wall=[cost_map[item].get('wall_s') for item in ids]
            if all(isinstance(value,(int,float)) and math.isfinite(value) for value in wall):
                if metric in {'mean_wall','wall_time'}:derived=sum(wall)/len(wall)
                elif metric=='median_wall':derived=statistics.median(wall)
                else:derived=None
                if derived is not None:compare_reported_number(cid,'wall summary',claim.get('value'),derived)
                summary=claim.get('summary')
                if isinstance(summary,dict):
                    for key,derived_value in (('mean',sum(wall)/len(wall)),('median',statistics.median(wall)),('min',min(wall)),('max',max(wall))):
                        if key in summary:compare_reported_number(cid,key,summary[key],derived_value)
            elif status in releasable:
                check(False,f'Claim {cid} wall summary is marked publishable without complete wall rows')

        interval=claim.get('confidence_interval') or claim.get('ci')
        if interval and metric in {'pass_rate','full_pass_rate'} and reproducible:
            level=interval.get('level',0.95) if isinstance(interval,dict) else 0.95
            derived=wilson_interval(observed,scored,level)
            if derived is None:
                check(False,'Claim '+cid+' uses an unsupported confidence interval level')
            elif isinstance(interval,dict):
                lower=interval.get('lower');upper=interval.get('upper')
                if not isinstance(lower,(int,float)) or not isinstance(upper,(int,float)):
                    check(False,'Claim '+cid+' confidence interval lacks numeric bounds')
                compare_reported_number(cid,'confidence interval lower bound',lower,derived[0])
                compare_reported_number(cid,'confidence interval upper bound',upper,derived[1])
                if interval.get('method') not in {'wilson','Wilson score'}:
                    check(False,'Claim '+cid+' confidence interval method is not declared as Wilson')

        test_name=str(claim.get('test') or claim.get('test_method') or '').lower().replace('-','_')
        reported_p=claim.get('p_value')
        derived_p=None
        groups=claim.get('comparison_groups') or claim.get('groups')
        if test_name in {'fisher_exact','fisher'} and isinstance(groups,list) and len(groups)==2:
            left,right=groups
            left_n=left.get('denominator');left_k=left.get('numerator')
            right_n=right.get('denominator');right_k=right.get('numerator')
            if all(isinstance(value,int) and not isinstance(value,bool) for value in (left_n,left_k,right_n,right_k)):
                derived_p=fisher_exact_two_sided(left_k,left_n-left_k,right_k,right_n-right_k)
        elif test_name in {'mcnemar_exact','exact_mcnemar'}:
            discordant_a=claim.get('discordant_a') or claim.get('wins_a')
            discordant_b=claim.get('discordant_b') or claim.get('wins_b')
            if isinstance(discordant_a,int) and isinstance(discordant_b,int):
                derived_p=exact_binomial_two_sided(discordant_a+discordant_b,min(discordant_a,discordant_b))
        elif test_name in {'sign_exact','exact_sign','binomial_exact'}:
            trials=claim.get('n') or denominator
            successes=claim.get('successes') or numerator
            if isinstance(trials,int) and isinstance(successes,int):derived_p=exact_binomial_two_sided(trials,successes)
        if derived_p is not None:compare_reported_number(cid,'p-value',reported_p,derived_p)
        elif reported_p is not None and status in releasable:
            check(False,'Publishable claim '+cid+' has a p-value without replayable test inputs')

        multiplicity=claim.get('multiplicity')
        if isinstance(multiplicity,dict):
            method=str(multiplicity.get('method') or '').lower()
            family_id=claim.get('multiplicity_family') or multiplicity.get('family')
            if family_id and claim.get('p_value_raw') is not None:
                multiplicity_families[family_id].append(claim)
            if method=='bonferroni':
                raw=claim.get('p_value_raw');adjusted=claim.get('p_value_adjusted');size=multiplicity.get('family_size')
                if isinstance(raw,(int,float)) and isinstance(size,int):
                    compare_reported_number(cid,'Bonferroni-adjusted p-value',adjusted,min(1.0,raw*size))
        refs=round_refs(claim)
        if any(re.fullmatch(r'r(?:51|53|56[a-z]?|57[a-z]?|64[a-z]?|69|70(?:-[a-z0-9]+)?|71|72|74)',rid,re.I) for rid in refs):
            if claim.get('supports_superiority') is True and status in releasable and not (claim.get('conflict_resolution') or claim.get('reconciliation_status')):
                check(False,'Conflict-sensitive comparison is publishable without a reconciliation disposition: '+cid)
        if status in releasable and not reproducible and not claim.get('source_reported_not_reproducible'):
            check(False,'Claim marked publishable without a reproducible exact-cell join: '+cid)
        metric_has_comparison=bool(claim.get('comparison') or claim.get('comparison_units') or claim.get('comparison_unit'))
        numeric_claim=(numerator is not None or denominator is not None)
        if numeric_claim and not isinstance(claim.get('unit'),str) and status in releasable:
            check(False,'Publishable claim lacks an explicit metric unit: '+cid)
        if metric_has_comparison and status in releasable:
            if not claim.get('comparison_units') and not claim.get('comparison_unit'):
                check(False,'Publishable comparison lacks recorded comparison units: '+cid)
            if not claim.get('analysis_direction') and not claim.get('direction') and not claim.get('analysis_rule'):
                check(False,'Publishable comparison lacks an analysis direction: '+cid)
            if 'exclusion' not in claim and 'exclusions' not in claim:
                check(False,'Publishable comparison lacks an explicit exclusion rule: '+cid)
            if 'multiplicity' not in claim:
                check(False,'Publishable comparison lacks an explicit multiplicity rule: '+cid)
        if numeric_claim and not ids and 'source-reported, not reproducible from public data' not in evidence_status:
            # This is the required honest label when a numeric historical variant
            # has no public exact-cell path. A status-only claim remains visible.
            if status in {'reconciliation_queue','status_only'}:
                check(False,'Unjoined numeric claim lacks the source-reported status label: '+cid)
    for family_id,family_claims in multiplicity_families.items():
        methods={str((claim.get('multiplicity') or {}).get('method') or '').lower() for claim in family_claims}
        if methods=={'holm'}:
            ordered=sorted(family_claims,key=lambda claim:claim.get('p_value_raw',1))
            size=len(ordered);running=0.0
            for rank,claim in enumerate(ordered):
                raw=claim.get('p_value_raw')
                if not isinstance(raw,(int,float)):continue
                adjusted=min(1.0,(size-rank)*raw)
                running=max(running,adjusted)
                compare_reported_number(str(claim.get('claim_id','(missing ID)')),'Holm-adjusted p-value',claim.get('p_value_adjusted'),running)

    # Design dates, stop causes, host epochs, pinned task/model/harness details,
    # effort clamps and token semantics are release requirements for claims.
    for claim in claims:
        cid=str(claim.get('claim_id') or '(missing ID)')
        status=claim_status(claim)
        if status not in releasable:continue
        ids=claim_cell_ids(claim)
        records=[run_by_id[item] for item in ids if item in run_by_id]
        if ids and len(records)!=len(ids):
            check(False,'Publishable claim has missing captured records: '+cid)
        for record in records:
            missing=[]
            if not record.get('task'):missing.append('task pin')
            if not record.get('model'):missing.append('model')
            if not record.get('effort'):missing.append('effort')
            if not record.get('recipe'):missing.append('recipe')
            if not record.get('tools',{}):missing.append('harness/tool versions')
            if not record.get('setup'):missing.append('setup/harness revision')
            if not record.get('tokens'):missing.append('token semantics')
            if missing:check(False,'Publishable claim has missing per-cell pins ('+', '.join(missing)+'): '+cid)
            effort=record.get('effort')
            model=record.get('model')
            if isinstance(effort,dict):
                requested=str(effort.get('requested') or '').lower()
                effective=str(effort.get('effective') or '').lower()
            else:requested=effective=''
            if requested=='max' and effective=='xhigh' and 'confounded' not in status:
                check(False,'Known max-to-xhigh effort clamp is not labelled CONFOUNDED: '+cid)
        rounds=round_refs(claim)
        for rid in rounds:
            plan=ROOT/'rounds'/rid/'PLAN.json'
            if not plan.is_file():continue
            try:protocol=json.loads(plan.read_text())
            except (OSError,json.JSONDecodeError):continue
            registered=protocol.get('registered_at') or protocol.get('design_frozen_at') or protocol.get('preregistered_at')
            first=protocol.get('first_cell_at') or protocol.get('first_started_at')
            if status in {'confirmatory','verified','reconciled','publishable','headline','released','supported'}:
                if not isinstance(registered,str) or not isinstance(first,str):
                    check(False,'Confirmatory claim lacks design-freeze and first-cell timestamps: '+cid)
                elif registered>first:
                    check(False,'Confirmatory design was frozen after first cell: '+cid)
            stop=protocol.get('early_stop') or protocol.get('cancellation')
            if stop and (not stop.get('time') or not stop.get('reason') or not stop.get('itt_treatment')):
                check(False,'Early stop/cancellation lacks time, reason, or ITT treatment: '+rid)
            if claim.get('metric') in {'wall_time','wall_s','latency'}:
                comparison=protocol.get('host_comparison') or protocol.get('timing_comparison') or {}
                if comparison and comparison.get('cross_host') is True:
                    required=('host','load','concurrency','epoch','paired_balance_rule')
                    if any(not comparison.get(key) for key in required):
                        check(False,'Cross-host timing lacks host/load/concurrency/epoch balance fields: '+rid)


def validate_r70_page_tables(test_count_rows):
    """Reconcile the two separate RvE/task-8v2 page tables to their raw ledger."""
    original=[row for row in test_count_rows if row.get('cohort')=='r70-original-rve' and row.get('scored') is True]
    page=ROOT/'rounds/r70-rve/README.md'
    if page.is_file():
        found=False
        expected=defaultdict(list)
        for source in original:expected[(source.get('task'),source.get('stack'))].append(source)
        for header,table_rows,_line in markdown_tables(page.read_text()):
            by_name={value.strip().lower():value for value in header}
            task_col=next((value for key,value in by_name.items() if key in {'task','task id'}),None)
            arm_col=next((value for key,value in by_name.items() if 'arm' in key),None)
            pass_col=next((value for key,value in by_name.items() if 'pass' in key),None)
            n_col=next((value for key,value in by_name.items() if key in {'n','graded cells'}),None)
            if not (task_col and arm_col and pass_col and n_col):continue
            found=True
            seen=set()
            for row,_number in table_rows:
                key=(row.get(task_col,''),row.get(arm_col,''))
                source=expected.get(key)
                if source is None:
                    check(False,'R70 original pass table has an unknown task/exact-arm pair')
                    continue
                if key in seen:check(False,'R70 original pass table repeats a task/exact-arm pair')
                seen.add(key)
                expected_pass=sum(candidate.get('outcome')=='pass' for candidate in source)
                actual_pass=row.get(pass_col,'').strip()
                expected_n=len(source)
                if actual_pass!=str(expected_pass):check(False,'R70 original pass table differs from official test-count rows for '+key[0]+' / '+key[1])
                if row.get(n_col,'').strip()!=str(expected_n):check(False,'R70 original graded-cell count differs from official test-count rows for '+key[0]+' / '+key[1])
            if seen!=set(expected):check(False,'R70 original pass table does not cover every task/exact-arm pair in the test-count ledger')
        if not found:check(False,'R70 original pass table lacks task and exact-arm columns')

    v2=[row for row in test_count_rows if row.get('cohort')=='r70-task8-v2-smoke']
    page=ROOT/'rounds/r70-rve-task8v2/README.md'
    if page.is_file():
        found=False
        expected={(row.get('task'),row.get('stack')):row for row in v2}
        for header,table_rows,_line in markdown_tables(page.read_text()):
            by_name={value.strip().lower():value for value in header}
            task_col=next((value for key,value in by_name.items() if key in {'task','task id'}),None)
            arm_col=next((value for key,value in by_name.items() if 'arm' in key),None)
            id_col=next((value for key,value in by_name.items() if key=='cell id'),None)
            outcome_col=next((value for key,value in by_name.items() if 'result' in key),None)
            fraction_col=next((value for key,value in by_name.items() if 'fraction' in key),None)
            scored_col=next((value for key,value in by_name.items() if 'scored' in key),None)
            if not all((task_col,arm_col,id_col,outcome_col,fraction_col,scored_col)):continue
            found=True
            seen=set()
            for row,_number in table_rows:
                key=(row.get(task_col,''),row.get(arm_col,''))
                source=expected.get(key)
                if source is None:
                    check(False,'Task-8 v2 table has an unknown task/exact-arm pair')
                    continue
                if key in seen:check(False,'Task-8 v2 table repeats a task/exact-arm pair')
                seen.add(key)
                fraction=f"{source.get('tests_passed')}/{source.get('tests_total')}"
                scored='yes' if source.get('scored') is True else 'no'
                comparisons=(
                    (row.get(id_col,'').strip().strip('`'),source.get('cell_id')),
                    (row.get(outcome_col,'').strip().lower(),source.get('outcome')),
                    (row.get(fraction_col,''),fraction),
                    (row.get(scored_col,'').strip().lower(),scored),
                )
                if any(actual!=str(wanted) for actual,wanted in comparisons):
                    check(False,'Task-8 v2 table differs from official smoke test-count rows for '+key[0]+' / '+key[1])
            if seen!=set(expected):check(False,'Task-8 v2 table does not cover every task/exact-arm pair in the test-count ledger')
        if not found:check(False,'Task-8 v2 smoke table lacks task and exact-arm columns')


def validate_claim_references(claims):
    """Make numeric editorial claims carry the ledger ID and its current status."""
    claim_by_id={
        row['claim_id']:row for row in claims
        if isinstance(row.get('claim_id'),str) and row.get('claim_id')
    }
    pages=[ROOT/'FINDINGS.md',ROOT/'EVIDENCE-MAP.md']+sorted((ROOT/'hypotheses').glob('f*.md'))
    numeric=re.compile(r'(?<![A-Za-z0-9_])(?:\$\s*\d+(?:\.\d+)?|\d+(?:\.\d+)?%?|\d+\s*/\s*\d+)(?![A-Za-z0-9_])')
    source_label=re.compile(r'source-reported, not reproducible from public data',re.I)
    pinned_spec_label=re.compile(
        r'(?:locally sanitized v1\.2 clause-reference snapshot|pinned fragment locally verified|'
        r'upstream public sanitization revision|all \d+ pinned v1\.2 fragments linked below are locally verified|'
        r'every v1\.2 clause fragment linked above is locally verified)',
        re.I,
    )
    for page in pages:
        if not page.is_file() or private_or_sealed_path(page):continue
        text=page.read_text()
        lines=text.splitlines()
        def context_for(line_index):
            if page.name=='EVIDENCE-MAP.md':
                start=line_index
                while start>0 and lines[start-1].strip():start-=1
                end=line_index+1
                while end<len(lines) and lines[end].strip():end+=1
                return ' '.join(lines[start:end])
            if page.name=='FINDINGS.md':
                starts=[m.start() for m in re.finditer(r'^##\s+F\d{2}\b',text,re.MULTILINE)]
                pos=sum(len(line)+1 for line in lines[:line_index])
                start=max((value for value in starts if value<=pos),default=0)
                end=next((value for value in starts if value>pos),len(text))
                return text[start:end]
            return text
        for index,line in enumerate(lines):
            referenced=[claim_id for claim_id in claim_by_id if claim_id in line]
            if referenced:
                paragraph=line if '|' in line else context_for(index)
                for claim_id in referenced:
                    row=claim_by_id[claim_id]
                    expected={str(row.get('claim_status') or '').strip(),claim_status(row).upper()}
                    expected.discard('')
                    if not any(re.search(rf'\b{re.escape(status)}\b',paragraph,re.I) for status in expected):
                        check(False,'Editorial claim reference omits its ledger status: '+str(page.relative_to(ROOT))+' ('+claim_id+')')
            stripped=re.sub(r'\[[^]]*\]\([^)]+\)','',line)
            stripped=re.sub(r'[\w./-]+\.md(?:#[^\s)]*)?','',stripped,flags=re.I)
            stripped=re.sub(r'\b(?:H\d{2,3}|F\d{2}|r\d+[a-z]?(?:-[A-Za-z0-9_.-]+)?|CL-[A-Za-z0-9_-]+|[0-9a-f]{40})\b','',stripped,flags=re.I)
            stripped=re.sub(r'\b\d{4}-\d{2}-\d{2}(?:T\S+)?\b','',stripped)
            stripped=re.sub(r'\b(?:19|20)\d{2}\b','',stripped)
            stripped=re.sub(r'§\s*\d+(?:\.\d+)*','',stripped)
            if numeric.search(stripped) and not referenced and not source_label.search(line) and not (page.name=='EVIDENCE-MAP.md' and pinned_spec_label.search(line)):
                check(False,'Numeric editorial statement lacks a claim ID or source-reported label: '+str(page.relative_to(ROOT))+':'+str(index+1))


def validate_evidence_map(claims):
    path=ROOT/'EVIDENCE-MAP.md'
    if not path.is_file():
        check(False,'Missing spec evidence map: EVIDENCE-MAP.md')
        return
    text=path.read_text()
    spec_roots=[candidate for candidate in (ROOT/'spec',ROOT/'kogen-spec/spec') if candidate.is_dir()]
    if not spec_roots:
        if spec_source_disclosed_unvendored(text):
            blockers.append('The public specification source is not vendored, so clause-heading coverage cannot be independently rechecked from this worktree')
        else:
            check(False,'Missing public spec source for EVIDENCE-MAP.md clause coverage without an explicit disclosure')
    mapped_spec_files={
        unquote(match)
        for match in re.findall(r'\bspec/([^/#\s`]+\.md)#',text)
    }
    required=set()
    current_decisions=set()
    for spec_root in spec_roots:
        for doc in spec_root.rglob('*.md'):
            doc_text=doc.read_text()
            current_decisions.update(re.findall(r'\b(?:DEC|dec)[-_][A-Za-z0-9_-]+\b',doc_text))
            # The evidence map indexes normative clauses and conformance
            # sections; source README/review notes are provenance, not clauses.
            relative=doc.relative_to(ROOT).as_posix()
            if relative not in mapped_spec_files or doc.name=='README.md':continue
            for heading in re.findall(r'^##\s+(.+)$|^###\s+(.+)$',doc_text,re.MULTILINE):
                title=next((item for item in heading if item), '')
                required.add(f'{doc.relative_to(ROOT).as_posix()}#{markdown_anchor(title)}')
    mapped=set()
    for md_link in re.findall(r'\]\(([^)]+)\)',text):
        target=md_link.strip('<>')
        if '#' in target:
            dest,anchor=target.split('#',1)
            if 'spec/' in dest or dest.startswith('#'):
                mapped.add((dest.lstrip('./')+'#'+anchor) if dest else '#'+anchor)
    for clause in sorted(required):
        if not any(clause.endswith('#'+link.split('#')[-1]) or link.endswith(clause.split('#')[-1]) for link in mapped):
            # A clause can also be keyed explicitly in the first column without a Markdown link.
            if clause.split('#')[-1] not in text:
                check(False,'Spec clause missing from EVIDENCE-MAP.md: '+clause)
    for decision in sorted(current_decisions):
        if decision not in text:check(False,'Current decision ID missing from EVIDENCE-MAP.md: '+decision)
    for claim in claims:
        status=str(claim.get('claim_status') or claim_status(claim)).upper()
        links=round_refs(claim)
        if not links:continue
        if claim.get('supports_superiority') is True or claim.get('supports_measured_superiority') is True:
            blocked=[]
            for rid in links:
                page=ROOT/'rounds'/rid/'README.md'
                if page.is_file():
                    found=ROUND_STATUS_RE.findall(page.read_text())
                    if any(value in {'WITHDRAWN','INVALID','NOT-RUN'} for value in found):blocked.append(rid)
            if blocked:check(False,'Claim uses withdrawn/invalid/not-run rounds for measured superiority: '+str(claim.get('claim_id','(missing ID)')))
        if status in {'WITHDRAWN','INVALID','NOT-RUN'} and claim.get('supports_measured_superiority') is True:
            check(False,'Invalid lifecycle claim is marked as measured superiority: '+str(claim.get('claim_id','(missing ID)')))


def validate_reproduction_records():
    required={
        'Kogen commit':r'Kogen\s+commit',
        'harness commit':r'harness\s+commit',
        'model and effort':r'model\s+and\s+effort',
        'task IDs':r'task\s+IDs?',
        'command':r'(?:historical\s+execution\s+)?command',
        'raw records':r'raw\s+records',
    }
    unavailable=re.compile(r'not applicable|not retained|not preserved|not recorded|unavailable|unknown|not run|not-run|no[^\n]{0,80}(?:commit|revision|sha)[^\n]{0,80}(?:preserv|record|retain|available)',re.I)
    sha=re.compile(r'\b[0-9a-f]{40}\b',re.I)
    for rid in REGISTERED_ROUND_IDS:
        page=ROOT/'rounds'/rid/'README.md'
        if not page.is_file():continue
        if private_or_sealed_path(page):continue
        text=page.read_text()
        missing=[]
        for label,pattern in required.items():
            match=re.search(pattern+r'[^\n]*',text,re.I)
            if not match:
                missing.append(label)
                continue
            value=match.group(0)
            if label in {'Kogen commit','harness commit'} and not sha.search(value) and not unavailable.search(value):
                missing.append(label+' (exact SHA or explicit unavailable status)')
        if missing:check(False,'Round reproduction record incomplete in '+str(page.relative_to(ROOT))+': '+', '.join(missing))
    try:
        inventory=json.loads((ROOT/'reproduce/round-inventory.json').read_text())
    except (OSError,json.JSONDecodeError):
        check(False,'Missing or malformed per-round reproduction inventory: reproduce/round-inventory.json')
        return
    round_ids=json.loads((ROOT/'rounds/index.json').read_text())
    entries=inventory.get('rounds')
    if not isinstance(entries,list):
        check(False,'Per-round reproduction inventory must contain a rounds list')
        return
    ids=[entry.get('round_id') for entry in entries]
    check(len(ids)==len(set(ids)) and set(ids)==set(round_ids),'Per-round reproduction inventory must contain exactly one entry per rounds/index.json ID')
    full_replay_ids=[]
    for entry in entries:
        rid=str(entry.get('round_id') or '(missing round ID)')
        check(entry.get('replay_type') in {'analysis-only','full-execution','unavailable'},'Invalid replay type in reproduction inventory: '+rid)
        check(isinstance(entry.get('full_execution_replayable'),bool),'Missing full-execution replay flag in reproduction inventory: '+rid)
        check(isinstance(entry.get('inputs'),list),'Inputs must be a list in reproduction inventory: '+rid)
        if entry.get('full_execution_replayable') is True:full_replay_ids.append(rid)
        command=entry.get('script')
        if command is not None:
            match=re.match(r'(?:python3?\s+)?([^\s]+\.py)(?:\s|$)',str(command))
            check(bool(match),'Script command does not identify a Python script: '+rid)
            if match:check((ROOT/match.group(1)).is_file(),'Reproduction script is missing for '+rid+': '+match.group(1))
        for input_value in entry.get('inputs',[]) if isinstance(entry.get('inputs'),list) else []:
            input_path=str(input_value).split(' (',1)[0]
            if '*' not in input_path:check((ROOT/input_path).is_file(),'Reproduction input is missing for '+rid+': '+input_path)
    check(set(inventory.get('full_execution_replayable_rounds',[]))==set(full_replay_ids),'Full execution replay summary differs from inventory rows')


def validate_publication_privacy():
    # Automated checks deliberately avoid opening private/sealed artifacts.
    denylist=[
        (r'(?im)^\s*>\s*(?:owner|participant|user)\b','quoted conversation block'),
        (r'(?i)\b(?:owner|participant)\s+(?:said|asked|wrote|messaged|quoted)\b','conversation attribution'),
        (r'(?i)\b(?:corpus/|transcript\.jsonl|grade\.sh|test_hidden\.py|solution\.patch|reference\.patch)\b','private-source artifact reference'),
        (r'(?i)\b(?:api[_ -]?key|secret|password|authorization)\s*[:=]\s*\S+','credential-like value'),
    ]
    for path in ROOT.rglob('*'):
        if unregistered_round_path(path):continue
        if '.git' in path.parts or path.is_dir() or path.is_symlink():continue
        if private_or_sealed_path(path):
            if path.name.lower() in SENSITIVE_FILENAMES or any(part.lower() in {'sealed','author-private','author_private'} for part in path.parts):
                check(False,'Forbidden private/sealed artifact present: '+str(path.relative_to(ROOT)))
            continue
        if not path.is_file():continue
        try:text=path.read_text(errors='replace')
        except OSError:
            check(False,'Cannot read public artifact '+str(path.relative_to(ROOT)))
            continue
        check(not contains_private_path(text),'Private filesystem/archive path in '+str(path.relative_to(ROOT)))
        if path.suffix.lower() in {'.md','.json','.jsonl','.csv','.txt'}:
            for pattern,label in denylist:
                check(not re.search(pattern,text),'Publication denylist ('+label+') in '+str(path.relative_to(ROOT)))
check((ROOT/'rounds/GLOSSARY.md').is_file(),'Missing canonical glossary at rounds/GLOSSARY.md')
check(not (ROOT/'GLOSSARY.md').exists(),'Duplicate root glossary remains; rounds/GLOSSARY.md is canonical')
rounds=json.loads((ROOT/'rounds/index.json').read_text())
tasks=json.loads((ROOT/'tasks/index.json').read_text())
for rid in rounds:
    p=ROOT/'rounds'/rid/'README.md';check(p.is_file(),'Missing round '+rid)
    if p.is_file():check(bool(re.search(r'STATUS: \*\*(VALID|CONFOUNDED|INVALID|INTERIM|WITHDRAWN|NOT-RUN|DESCRIPTIVE|INCOMPLETE|PILOT)',p.read_text())),'No status '+rid)
for t in tasks:
    p=ROOT/'tasks'/t['id']/'task.json';check(p.exists(),'Missing task '+t['id'])
    if p.exists():check(json.loads(p.read_text())==t,'Index mismatch '+t['id'])
    check(isinstance(t['retired'],bool),'No retired flag '+t['id'])
with (ROOT/'results/cells.csv').open(newline='') as f:
    reader=csv.DictReader(f);check(reader.fieldnames==FIELDS,'CSV schema mismatch');csvrows=list(reader)
rows=[json.loads(s) for s in (ROOT/'results/cells.jsonl').read_text().splitlines()]
check(len(csvrows)==len(rows),'CSV/JSONL row count differs')
for i,(a,b) in enumerate(zip(csvrows,rows)):
    check(set(b)==set(FIELDS),'JSONL schema mismatch '+str(i))
    check(all(a[k]==('' if b[k] is None else str(b[k])) for k in FIELDS),'CSV/JSONL content differs '+str(i))
    check(b['round']=='unmapped' or b['round'] in rounds,'Missing result round '+b['round'])
    check(b['task'] in {t['id'] for t in tasks},'Unknown result task '+b['task'])
    check(b['ITT outcome'] in ['pass','fail','unresolved','not_scored'],'Invalid ITT value')
report=json.loads((ROOT/'results/export-report.json').read_text())
check(report['exported_cell_rows']==len(rows),'Export report mismatch')
# Task usage has explicit meanings: used_in is captured delivery coverage;
# graded_in is coverage of the official outcome export. The task index and
# individual records are checked together below.
try:
    run_record_rows=indexed_records(ROOT)
    check(not (ROOT/'results/run-records.jsonl').exists(),'Legacy monolithic results/run-records.jsonl still exists')
    check((ROOT/'results/run-records/index.json').stat().st_size<100_000,'Run-record index is not tiny')
    check_compact_encoding(run_record_rows,'Indexed run records')
except (OSError,ValueError,json.JSONDecodeError) as exc:
    check(False,'Invalid indexed run-record export: '+str(exc))
    run_record_rows=[]
for family,round_field in [
    ('reproduce/inputs/run-evidence','round_id'),
    ('reproduce/inputs/context-evidence',None),
    ('reproduce/inputs/ungraded-evidence','round_id'),
]:
    try:
        _index,family_rows=read_partitions(ROOT/family,round_field=round_field)
        check((ROOT/family/'index.json').stat().st_size<100_000,f'{family}/index.json is not tiny')
        # The source run-evidence seed is schema 1.0 and retains its distinct
        # one-key missing markers; full reason/source markers must use codes.
        check_compact_encoding(family_rows,family,allow_legacy_single=(family=='reproduce/inputs/run-evidence'))
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        check(False,f'Invalid indexed evidence family {family}: {exc}')
captured_pairs={t['id']:set() for t in tasks}
graded_pairs={t['id']:set() for t in tasks}
for record in run_record_rows:
    rid=record.get('audit_round')
    task=record.get('task')
    tid=task.get('id') if isinstance(task,dict) else None
    if isinstance(rid,str) and rid not in {'','unmapped'} and isinstance(tid,str):
        if tid in captured_pairs:captured_pairs[tid].add(rid)
        else:check(False,'Captured task ID missing from task catalogue: '+tid)
for row in rows:
    rid=row.get('round');tid=row.get('task')
    if isinstance(rid,str) and rid not in {'','unmapped'} and isinstance(tid,str) and tid in graded_pairs:
        graded_pairs[tid].add(rid)
planned_pairs=collect_planned_task_pairs(ROOT,{task['id'] for task in tasks})
planned_by_task={task['id']:set() for task in tasks}
for tid,rid in planned_pairs:planned_by_task[tid].add(rid)
for task in tasks:
    tid=task['id']
    check(set(task.get('used_in',[]))==captured_pairs[tid],'Captured task/round pairs mismatch in index: '+tid)
    check(set(task.get('graded_in',[]))==graded_pairs[tid],'Official task/round pairs mismatch in index: '+tid)
    check(set(task.get('planned_in',[]))==planned_by_task[tid],'Planned task/round pairs mismatch in index: '+tid)
    page_mentions=task.get('round_page_mentions',[])
    legacy_refs=task.get('unverified_round_refs',[])
    check(isinstance(page_mentions,list) and isinstance(legacy_refs,list),'Malformed task round-reference fields: '+tid)
    check(not (set(page_mentions)&set(legacy_refs)),'Overlapping task round-reference fields: '+tid)
# Round-page table pass counts are authoritative only when they reconcile to
# the official cells export. Unsupported table shapes produce errors rather
# than being silently skipped.
# The original RvE outcome export predates immutable cell IDs in cells.jsonl.
# Its official outcomes are available in the supplemental test-count ledger.
# Add only this separate cohort to the pass-table join; rerun/extension cohorts
# already have exact rows in cells.jsonl and must not be double-counted.
test_count_rows=read_jsonl(ROOT/'results/test-counts.jsonl','Round 70 test-count ledger')
pass_count_rows=[]
if not any(row.get('round')=='r70-rve' for row in rows):
    for item in test_count_rows:
        if item.get('cohort')=='r70-original-rve' and item.get('scored') is True:
            pass_count_rows.append({
                'round':'r70-rve','task':item.get('task'),'arm':item.get('stack'),
                'rep':str(item.get('rep')),'model':'gpt-6-luna',
                'ITT outcome':item.get('outcome'),
            })
pass_table_errors,pass_table_groups=validate_all_round_pages(ROOT,rows+pass_count_rows)
for error in pass_table_errors:check(False,error)
validate_r70_page_tables(test_count_rows)
pass_count_self_test(ROOT)
round70_evidence_self_test()
round70_errors, round70_summary = audit_round70_evidence(ROOT)
for error in round70_errors:check(False,error)
r70_completeness_self_test()
for error in audit_r70_completeness(ROOT):check(False,error)
# Authored links and anchors are checked on the public editorial surface. The
# private release note and restricted artifacts are deliberately not opened.
validate_markdown_links()
links=sum(len(re.findall(r'\]\(([^)]+)\)',page.read_text())) for page in public_markdown_files())
files=0
for f in ROOT.rglob('*'):
    if unregistered_round_path(f):continue
    if '.git' in f.parts or '__pycache__' in f.parts:continue
    if f.is_symlink():
        check(False,'Symlink '+str(f.relative_to(ROOT)))
        continue
    if not f.is_file():continue
    if private_or_sealed_path(f):
        if f.name.lower() in SENSITIVE_FILENAMES or any(part.lower() in {'sealed','author-private','author_private'} for part in f.parts):
            check(False,'Forbidden artifact '+str(f.relative_to(ROOT)))
        continue
    files+=1
    text=f.read_text(errors='replace')
    relative=f.relative_to(ROOT).as_posix()
    for finding in publication_scan_findings(text,relative):
        check(False,'Publication scan ('+finding+') in '+relative)
# Register and status consistency (added 6 Oct 2026): every round directory is indexed and listed,
# the register status equals the page status, a page has one status, and summaries do not contradict it.
STATUSES='VALID|CONFOUNDED|INVALID|INTERIM|WITHDRAWN|NOT-RUN|DESCRIPTIVE|INCOMPLETE|PILOT'
STATUS_RE=re.compile(r'STATUS: \*\*('+STATUSES+r')\b')
def page_status(rid):
    p=ROOT/'rounds'/rid/'README.md'
    if not p.is_file():return None
    found=STATUS_RE.findall(p.read_text())
    check(len(set(found))<=1,'Conflicting status lines in rounds/'+rid+'/README.md: '+', '.join(sorted(set(found))))
    return found[0] if found else None
round_dirs=sorted(TRACKED_ROUND_DIRS)
for rid in round_dirs:
    check(rid in rounds,'Round directory missing from rounds/index.json: '+rid)
register=(ROOT/'rounds/README.md').read_text()
listed={}
for line in register.splitlines():
    m=re.match(r'- \[([^\]]+)\]\(([^)/]+)/README\.md\)',line)
    if m:
        st=re.findall(r'\*\*('+STATUSES+r')\b',line)
        listed[m.group(2)]=st[0] if st else None
for rid in round_dirs:
    check(rid in listed,'Round directory missing from the register (rounds/README.md): '+rid)
    st=page_status(rid)
    if rid in listed and st:check(listed[rid]==st,f'Register status {listed[rid]} != page status {st} for {rid}')
summary_files=list((ROOT/'categories').glob('*.md'))+[ROOT/'results/validation-summary.md',ROOT/'README.md']
for f in summary_files:
    if not f.is_file():continue
    for line in f.read_text().splitlines():
        for rid in re.findall(r'rounds/([^/)\s]+)/(?:README|MEASURED)\.md',line):
            st=page_status(rid) if (ROOT/'rounds'/rid).is_dir() else None
            words=set(re.findall(r'\b('+STATUSES+r')\b',line))
            if st and words and len(set(re.findall(r'rounds/([^/)\s]+)/',line)))==1:
                check(st in words,f'{f.relative_to(ROOT)} labels {rid} {sorted(words)} but its page status is {st}')
# Standard records and exact historical declarations are part of repository validity.
from validate_round import records as standard_records, validate as validate_standard_round
standard=standard_records()
standard_rounds=set(rounds)|{r.get('audit_round') for r in standard}
for rid in sorted(standard_rounds):
    if not has_standard_run_records(rid,standard):continue
    audit=validate_standard_round(rid,standard)
    for error in audit['errors']:check(False,'Standard record '+rid+': '+error)

try:
    release_round_config=json.loads((ROOT/'reproduce/release-rounds.json').read_text())
    strict_from_date=__import__('datetime').date.fromisoformat(release_round_config['strict_from_date'])
except (OSError,json.JSONDecodeError,KeyError,TypeError,ValueError):
    strict_from_date=None
check(strict_from_date is not None and strict_from_date.isoformat()=='2026-10-09',
      'Strict new-round start date must be 2026-10-09')
new_rounds=[]
for rid in rounds:
    declared_date=round_date(rid)
    if strict_from_date and declared_date and declared_date>=strict_from_date:
        new_rounds.append(rid)
for rid in new_rounds:
    if not has_standard_run_records(rid,standard):
        check(False,'New strict round has no Standard records: '+rid)
        continue
    audit=validate_standard_round(rid,standard,strict=True)
    for error in audit['errors']:check(False,'New strict Standard record '+rid+': '+error)
    if not audit['strict_release_eligible']:
        blockers.append(f"{rid} has {audit['missing']} missing Standard capture fields and {len(audit['protocol_deviations'])} protocol deviations; new-round strict release is blocked")

# Publication gates are evaluated from their evidence type and declared source
# inputs. Gate IDs and the number of gates are data, not validator constants.
claim_rows=read_jsonl(ROOT/'results/claim-ledger.jsonl','claim ledger',required=True)
try:
    crosswalk_index,crosswalk_rows=read_partitions(ROOT/'results/source-crosswalk',round_field='round_id')
    check((ROOT/'results/source-crosswalk/index.json').stat().st_size<100_000,'Source-crosswalk index is not tiny')
    check_compact_encoding(crosswalk_rows,'Source-crosswalk')
except (OSError,ValueError,json.JSONDecodeError) as exc:
    check(False,'Invalid indexed source-crosswalk export: '+str(exc))
    crosswalk_index,crosswalk_rows={},[]
try:
    publication_register=json.loads((ROOT/'results/publication-blockers.json').read_text())
except (OSError,json.JSONDecodeError):
    publication_register={}
publication_blockers=publication_register.get('blockers',[])
gate_ids=[item.get('id') for item in publication_blockers if isinstance(item,dict)]
check(bool(publication_blockers) and len(gate_ids)==len(publication_blockers) and all(isinstance(value,str) and value for value in gate_ids) and len(set(gate_ids))==len(gate_ids),
      'Publication evidence register must contain unique, named gate rows')
check(all(item.get('status') in {'open','resolved'} for item in publication_blockers if isinstance(item,dict)),
      'Publication evidence register contains an unknown gate status')
expected_publication_status='blocked' if any(item.get('status')!='resolved' for item in publication_blockers if isinstance(item,dict)) else 'ready'
check(publication_register.get('publication_status')==expected_publication_status,
      'Publication status must follow the registered evidence gate states')
grade_gate=next((item for item in publication_blockers if item.get('evidence_key')=='official_grade_export_join'),{})
spec_gate=next((item for item in publication_blockers if item.get('evidence_key')=='spec_decision_sources'),{})

grade_join_input=read_jsonl(ROOT/'results/grade-join-input.jsonl','exact grade-join input',required=True)
grade_join_rows=[]
try:
    with (ROOT/'results/grade-join.csv').open(newline='',encoding='utf-8') as stream:
        grade_join_rows=list(csv.DictReader(stream))
except OSError:
    check(False,'Missing results/grade-join.csv exact join output')
public_grade_rows=read_jsonl(ROOT/'reproduce/inputs/grades.final.jsonl','public grade snapshot',required=True)
graded_capture_ids=[row.get('cell_id') for row in run_record_rows if row.get('graded') is True and isinstance(row.get('cell_id'),str)]
input_delivery_ids=[row.get('delivery_id') for row in grade_join_input]
input_grade_ids=[row.get('official_grade_id') for row in grade_join_input]
csv_delivery_ids=[row.get('delivery_id') for row in grade_join_rows]
csv_grade_ids=[row.get('official_grade_id') for row in grade_join_rows]
public_snapshot_ids={row.get('cell_id') for row in public_grade_rows if isinstance(row.get('cell_id'),str) and row.get('cell_id')}
exact_input=bool(grade_join_input) and all(
    row.get('delivery_id')==row.get('official_grade_id')
    and ((row.get('official_grade_id') in public_snapshot_ids and row.get('source')=='grades.final.jsonl' and 'exact equality' in str(row.get('rule','')))
         or (row.get('official_grade_id') not in public_snapshot_ids and row.get('source')=='run-record capture metadata' and 'capture-reported' in str(row.get('rule','')) and 'official export row absent' in str(row.get('rule',''))))
    for row in grade_join_input
)
exact_csv=bool(grade_join_rows) and all(
    row.get('delivery_id')==row.get('official_grade_id')
    and ((row.get('official_grade_id') in public_snapshot_ids and row.get('source')=='grades.final.jsonl' and 'exact equality' in str(row.get('rule','')))
         or (row.get('official_grade_id') not in public_snapshot_ids and row.get('source')=='run-record capture metadata' and 'capture-reported' in str(row.get('rule','')) and 'official export row absent' in str(row.get('rule',''))))
    for row in grade_join_rows
)
crosswalk_by_delivery=defaultdict(list)
for item in crosswalk_rows:
    if item.get('record_role')=='captured_delivery' and is_run_record_file(item.get('source_file')):
        crosswalk_by_delivery[item.get('source_record_id')].append(item)
exact_crosswalk_ids={item.get('source_record_id') for item in crosswalk_rows if item.get('record_role')=='captured_delivery' and is_run_record_file(item.get('source_file')) and item.get('linkage_status')=='exact_official_grade_join'}
crosswalk_join_complete=(len(input_delivery_ids)==5020 and all(
    len(crosswalk_by_delivery.get(row.get('delivery_id'),[]))==1
    and crosswalk_by_delivery[row.get('delivery_id')][0].get('source_record_id')==row.get('official_grade_id')
    and crosswalk_by_delivery[row.get('delivery_id')][0].get('public_cell_id')==row.get('official_grade_id')
    and crosswalk_by_delivery[row.get('delivery_id')][0].get('linked_cell_ids')==[row.get('official_grade_id')]
    and crosswalk_by_delivery[row.get('delivery_id')][0].get('linkage_status')==('exact_official_grade_join' if row.get('official_grade_id') in public_snapshot_ids else 'capture_reported_identity_mapping')
    and crosswalk_by_delivery[row.get('delivery_id')][0].get('grade_publication_status')==('public_export' if row.get('official_grade_id') in public_snapshot_ids else 'capture_reported_export_absent')
    and crosswalk_by_delivery[row.get('delivery_id')][0].get('grade_publication_label')==('officially graded; in the public export' if row.get('official_grade_id') in public_snapshot_ids else 'capture-reported grade; official export row absent')
    for row in grade_join_rows
)) and exact_crosswalk_ids=={row.get('delivery_id') for row in grade_join_rows if row.get('official_grade_id') in public_snapshot_ids}
public_join_count=sum(grade_id in public_snapshot_ids for grade_id in input_grade_ids)
capture_reported_count=sum(grade_id not in public_snapshot_ids for grade_id in input_grade_ids)
b1_join_complete=(
    len(grade_join_input)==5020
    and len(grade_join_rows)==5020
    and len(set(input_delivery_ids))==5020
    and len(set(input_grade_ids))==5020
    and len(set(csv_delivery_ids))==5020
    and len(set(csv_grade_ids))==5020
    and exact_input
    and exact_csv
    and set(input_delivery_ids)==set(graded_capture_ids)
    and set(csv_delivery_ids)==set(input_delivery_ids)
    and set(csv_grade_ids)==set(input_grade_ids)
    and crosswalk_join_complete
    and public_join_count==5020
    and capture_reported_count==0
    and all(
        crosswalk_by_delivery[row.get('delivery_id')][0].get('grade_publication_status')==(
            'public_export' if row.get('official_grade_id') in public_snapshot_ids else 'capture_reported_export_absent'
        )
        for row in grade_join_rows
    )
)
check(grade_gate.get('count')==5020 and grade_gate.get('capture_reported_count')==0,
      'Official-grade gate must report all 5,020 exact public matches and no capture-reported mappings')
check(grade_gate.get('status')==('resolved' if b1_join_complete else 'open'),
      'Official-grade gate may resolve only when every capture ID has an independently available official-export row')
if not b1_join_complete:
    blockers.append(f"{grade_gate.get('id','Official-grade gate')} remains open: {public_join_count:,}/5,020 official-export IDs are publicly cross-checked; {capture_reported_count:,} mappings have capture-side outcomes/timestamps but no official-export rows")
else:
    resolved_gates.append('Official-grade gate: all captured delivery IDs are independently matched to official-export rows')
spec_inputs=spec_gate.get('evidence_inputs',[])
spec_sources_complete=(
    bool(spec_inputs)
    and all(isinstance(path,str) and (ROOT/path).is_file() for path in spec_inputs)
    and bool(spec_fragment_count)
    and not spec_snapshot_errors
)
check(spec_gate.get('status')==('resolved' if spec_sources_complete else 'open'),
      'Specification-source gate may resolve only when the pinned snapshot and all EVIDENCE-MAP fragments verify')
if not spec_sources_complete:
    blockers.append(str(spec_gate.get('id','Specification-source gate'))+' remains open: the pinned specification snapshot or an EVIDENCE-MAP fragment is missing or invalid')
else:
    resolved_gates.append(f'Specification-source gate: {spec_fragment_count} pinned v1.2 fragments locally verified; decision-ledger coverage remains limited')
grade_join_report=(ROOT/'results/GRADE-JOIN.md').read_text(encoding='utf-8')
check('5,020/5,020' in grade_join_report and 'source_record_id == public_cell_id == grades.final.jsonl cell_id' in grade_join_report,
      'Grade-join report must document the public exact-ID rule and refreshed cross-check count')
check('84 model pass' in grade_join_report.lower() and '19 model fail' in grade_join_report.lower()
      and 'control_apply' in grade_join_report.lower() and 'not model failures' in grade_join_report.lower(),
      'Grade-join report must distinguish model outcomes from invalid control applications')
check(grade_gate.get('evidence_path')=='results/GRADE-JOIN.md','Official-grade gate must link the exact grade-join report')
check('not model failures' in grade_gate.get('claim_scope','').lower(),'Official-grade gate must distinguish invalid control rows from model failures')
spec_summary=spec_gate.get('summary','').lower()
check(spec_gate.get('count')==spec_fragment_count
      and 'locally' in spec_summary and 'v1.2' in spec_summary
      and '1118f7fc0dbb042af8c8de2ffd1b85768cf9e2a0' in spec_summary
      and '30d9b25e4eefa7117121de44298fed504b429f4e' in spec_summary
      and 'published-byte sha-256 manifest verifies' in spec_summary
      and 'comprehensive decision-to-clause coverage remains limited' in spec_summary,
      'Specification-source gate must document local verification, both source revisions, published-byte hashes, limited decision-ledger coverage, and the verified fragment count')
validation_text=(ROOT/'results/publication-validation.md').read_text() if (ROOT/'results/publication-validation.md').is_file() else ''
check('5,020/5,020' in validation_text and 'results/GRADE-JOIN.md' in validation_text
      and '84 model pass' in validation_text.lower() and '19 model fail' in validation_text.lower()
      and 'control_apply' in validation_text.lower() and 'not model failures' in validation_text.lower(),
      'Publication validation report must document the complete refreshed join and separate invalid controls from model outcomes')
validation_text_lower=validation_text.lower()
check(f'{spec_fragment_count} linked v1.2 fragments resolve' in validation_text_lower
      and 'published-byte hashes verify' in validation_text_lower
      and 'comprehensive decision-to-clause coverage remains limited' in validation_text_lower,
      'Publication validation report must document the locally verified snapshot, published-byte hashes, and limited decision-ledger coverage')
validate_hypothesis_publication()
indexed_round_ids=round_index_ids(rounds)
validate_round_crosswalk(indexed_round_ids,rows,claim_rows,crosswalk_rows)
validate_claims_and_records(claim_rows,rows,run_record_rows,crosswalk_rows)
validate_claim_references(claim_rows)
validate_evidence_map(claim_rows)
validate_reproduction_records()
# Remote configuration is outside this read-only local audit's scope.
oversized=[(relative,(ROOT/relative).stat().st_size) for relative in sorted(TRACKED_PATHS)
           if (ROOT/relative).is_file() and (ROOT/relative).stat().st_size>(MAX_RAILS_BASE_BUNDLE_BYTES if relative.startswith('tasks/_bases/rails-') and relative.endswith('.bundle') else MAX_REPOSITORY_FILE_BYTES)]
for relative,size in oversized:
    limit=MAX_RAILS_BASE_BUNDLE_BYTES if relative.startswith('tasks/_bases/rails-') and relative.endswith('.bundle') else MAX_REPOSITORY_FILE_BYTES
    errors.append(f'Committed file exceeds {limit//1_000_000} MB: {relative} ({size} bytes)')
if errors:raise SystemExit('\n'.join(sorted(set(errors))))
print(f'Validated {len(rounds)} round pages, {len(tasks)} task records, {len(rows)} matching CSV/JSONL rows, {pass_table_groups} table pass-count groups, {links} authored links and {files} files; pass-count self-test passed; no privacy/forbidden-artifact failures; remote configuration not inspected.')
for gate in sorted(resolved_gates):
    print('PUBLICATION GATE RESOLVED: '+gate)
for blocker in sorted(set(blockers)):
    print('PUBLICATION BLOCKER: '+blocker)
