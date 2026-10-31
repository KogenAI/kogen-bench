import os,pathlib,json,collections,itertools,csv,math,statistics,hashlib,datetime
R=pathlib.Path(os.environ.get('SHELLTAIL_SNAPSHOT') or pathlib.Path(__file__).resolve().parent);O=pathlib.Path(os.environ.get('SHELLTAIL_OUT') or '.')
ps=json.loads((R/'pairs.json').read_text());ts=json.loads((R/'calls.json').read_text());cs=json.loads((R/'commands.json').read_text());cells=json.loads((R/'cells.json').read_text())
lt=collections.defaultdict(list);ct=collections.defaultdict(list)
for t in ts:lt[t['key']].append(t)
for t in cs:ct[t['key']].append(t)
def grp(p):return p['loop']['batch'],p['loop']['effort']
groups=[(g,list(v)) for g,v in itertools.groupby(sorted(ps,key=grp),grp)]
def label(g):return {'confirmation-eu-20261029':'EU','confirmation-eu-medium-20261029':'EU'}.get(g[0],g[0])+' '+g[1]
def num(x):return f'{x:,.1f}'
def integer(x):return f'{x:,}'
def table(head,rows):return '\n'.join(['| '+' | '.join(head)+' |','|'+'|'.join(['---']*len(head))+'|']+['| '+' | '.join(map(str,r))+' |' for r in rows])+'\n'
def sumfield(pp,side,k):return sum(p[side][k] for p in pp)
def sh(p):return [t for t in lt[p['loop']['key']] if t['name']=='shell']
def lower(tt):return sum(max(0,t['seconds']-1) for t in tt)
def upper(tt):return sum(t['seconds']+1 for t in tt)
def crepeatbytes(p):
 seen=set();total=0
 for t in ct[p['codex']['key']]:
  if t['command'] in seen:total+=t['output_bytes']
  seen.add(t['command'])
 return total
def known(p):return [t for t in sh(p) if t['command'] is not None]
def delta(p):return p['loop']['wall']-p['codex']['wall']
def bucket(t,loop=False):
 if loop and t['name'] in ['read_file','list_files','search_text']:return 'read-discovery'
 if loop and t['name']=='write_file':return 'write-file'
 if loop and t['command'] is None:return 'unclassified-shell'
 k=t.get('kinds',[])
 for name in ['module-test','targeted-test','test','make-check','acceptance','build','vet','format','git','read']:
  if name in k:return 'read-discovery' if name=='read' else name
 return 'other-command'
# Auditable per-pair measurements, no hidden test bodies, outputs, reasoning or credentials.
rows=[];mech=[];recovered=[]
for p in ps:
 l,c=p['loop'],p['codex'];ss=sh(p);kk=known(p);lc=lt[l['key']];cc=ct[c['key']]
 row=dict(batch=l['batch'],effort=l['effort'],task=l['task'],rep=l['rep'],both_pass=l['passed'],tail=p['tail'],loop_key=l['key'],codex_key=c['key'],loop_wall_s=l['wall'],codex_wall_s=c['wall'],wall_delta_s=delta(p),loop_shell_n=len(ss),loop_known_shell_n=len(kk),codex_command_n=c['cmd_n'],loop_shell_s_q=l['shell_s'],loop_shell_lower_s=lower(ss),loop_shell_upper_s=upper(ss),codex_shell_s=None,shell_excess_strict_lower_s=lower(ss)-c['wall'],loop_output_bytes=l['tool_bytes'],codex_saved_output_bytes=c['cmd_bytes'],saved_output_delta_bytes=l['tool_bytes']-c['cmd_bytes'],loop_logical_output_replay_bytes=l['logical_replay_bytes'],loop_shell_output_bytes=l['shell_bytes'],loop_builtin_read_output_bytes=l['read_bytes'],loop_cut_n=l['cuts'],loop_builtin_read_n=sum(t['name']=='read_file' for t in lc),loop_builtin_list_n=sum(t['name']=='list_files' for t in lc),loop_builtin_search_n=sum(t['name']=='search_text' for t in lc),loop_builtin_write_n=sum(t['name']=='write_file' for t in lc),codex_invalid_lines=c['bad'],loop_repeat_shell_n=l['repeat_shells'],loop_repeat_shell_s_q=l['repeat_shell_s'],loop_repeat_shell_output_bytes=l['repeat_shell_bytes'],codex_repeat_saved_output_bytes=crepeatbytes(p),repeat_shell_saved_byte_delta=l['repeat_shell_bytes']-crepeatbytes(p),codex_exact_repeat_command_n=c['codex_repeats'],loop_multishell_responses=l['multishell'],codex_overlapping_starts=c['overlap'])
 for k in ['test','module-test','targeted-test','race','count','build','vet','format','read','git','make-check','acceptance']:
  row['loop_known_'+k+'_commands']=sum(k in t.get('kinds',[]) for t in kk);row['codex_'+k+'_commands']=sum(k in t['kinds'] for t in cc)
 rows.append(row)
 unk=[t for t in ss if t['command'] is None];unkbytes=sum(t['bytes'] for t in unk)
 for b in sorted(set([bucket(t,True) for t in lc]+[bucket(t) for t in cc])):
  ll=[t for t in lc if bucket(t,True)==b];rr=[t for t in cc if bucket(t)==b]
  # These are command-bucket envelopes, not exclusive runtime within compound commands.
  lb=sum(t['bytes'] for t in ll);cb=sum(t['output_bytes'] for t in rr)
  mech.append(dict(batch=l['batch'],effort=l['effort'],task=l['task'],rep=l['rep'],both_pass=l['passed'],tail=p['tail'],bucket=b,loop_observed_n=len(ll),loop_seconds_q=sum(t['seconds'] for t in ll),loop_seconds_lower=lower(ll),loop_seconds_upper=upper(ll),loop_observed_bytes=lb,loop_logical_output_replay_bytes=sum(t['logical_replay_bytes'] for t in ll),codex_saved_command_n=len(rr),codex_saved_output_bytes=cb,codex_seconds=None,exact_excess_seconds=None,loop_unclassified_shell_n=len(unk),loop_unclassified_shell_seconds_q=sum(t['seconds'] for t in unk),loop_unclassified_shell_bytes=unkbytes,loop_minus_saved_codex_bytes_min=lb-cb,loop_minus_saved_codex_bytes_max=lb+unkbytes-cb))
 for t in kk:recovered.append(dict(key=l['key'],seq=t['seq'],call_id=t['call_id'],arguments_sha256=t['arg'],command=t['command'],seconds_q=t['seconds'],output_bytes=t['bytes'],cut=t['cut']))
def savecsv(name,rs):
 with (O/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
savecsv('shelltail-cells.csv',rows);savecsv('shelltail-mechanisms.csv',mech)
(O/'shelltail-recovered-commands.jsonl').write_text(''.join(json.dumps(t,ensure_ascii=False)+'\n' for t in recovered))
receipt=dict(collected_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),archives={f.name:dict(bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in R.glob('*.tar.gz')},sources=json.loads((R/'sources.json').read_text()),analysis_sha256=hashlib.sha256((R/'analyze.py').read_bytes()).hexdigest(),report_script_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest())
(O/'shelltail-sources.json').write_text(json.dumps(receipt,indent=2)+'\n')
parts=['''# Shell tail — 30 October 2026

The supplied records support a shell-tail diagnosis, but not a complete command-by-command excess-time decomposition. **104 pairs have the same task, rep, prompt hash, starting commit, model and effort, and both pass.** A separate 12-pair h2h-22 stratum records `all_passed=false` on both clients; its dramatic tail must not be presented as time to the same successful outcome. Same host and round are required throughout the main tables.

Loop issues fewer shell invocations than Codex command executions in every cohort, and returns fewer recorded tool-output bytes in every subscription cohort. This does not prove less verification: Codex also edits and reads through shell; loop has separate file tools and can bundle several checks into one command. EU is different: loop delivers more recorded output bytes, especially readtime. The extra long shell executions are a loop trajectory to investigate, not a neutral host charge or proof of necessary work. Their exact commands mostly did not survive.

## Evidence and measurement contract



Actual loop command text lived in `<job-temp>/loop-session/session.json`, in `input` function-call items' `arguments`; the corresponding function outputs also lived there. Source witnesses: supplied loop `loop/session.go:98,108,411–430` (transcript and persistence), `:303–337` (event argument/result hashing), `:473` (raw argument-string digest). Remote harness `bare-agent/lanes_bare.py:375,615` puts that session under the cell temporary directory and removes the directory afterwards. Both Mac runners had zero `lanes-bare-*` workspaces in their actual Python temporary directory at inspection. EU had one remaining unrelated workspace without a loop session; the prior API inspection also established deletion of counted-cell workspaces. The supplied completed cell directories contain events, usage receipts, result/evaluation, prompt, stderr and final artifacts, **no request/response body or transcript**. Request-attempt records retain timing/usage/fingerprints, not response tool arguments. Final diffs contain final edits, not shell history.

Recovery therefore uses exact SHA-256 preimages: visible Codex commands, supplied prompt check literals, and finite candidate formatting/check chains, encoded as possible JSON argument strings. A match proves the whole argument text; a miss proves nothing about command category. Across all 531 parsed loop/Codex cells, 73 distinct shell argument hashes were recovered; in the matched strata, **81/697 shell invocations (422/6,535 quantized shell seconds)** are decoded. **616 commands / 6,113 seconds remain unclassified.** This extends the earlier API-only recovery but cannot recreate deleted transcripts. Full command text and call IDs for every match are in `shelltail-recovered-commands.jsonl`.

Loop time is tool.call→tool.result, summed over shell calls, with whole-second timestamps. Each interval d has bounds `[max(0,d−1), d+1]`; sums of these bounds are used below. Calls are serial in the supplied engine. Codex JSON command events have no timestamps or durations; receipt admission times do not restore command completion. `?` is unobserved. **A rigorous lower bound on shell excess is `loop shell lower − Codex entire agent wall`**, since all Codex shell wall fits within that agent interval. A positive bound proves some excess shell time, without identifying its command. Negative bounds do not imply a saving. No command timing is imputed from its name, output length or adjacent API receipt.

Loop bytes are delivered UTF-8 `tool.result.bytes`, **after** the 16 KiB cut, including numbered-file/shell framing. Source `provider/cache.go:183–193` confirms strings are fingerprinted as raw strings, not JSON-escaped strings. Codex bytes are UTF-8 `aggregated_output` in valid completed command items. They are a **saved-output proxy, not a wire capture of the exact text read into model context**: model-facing truncation/framing and replay multiplicity cannot be recovered here. Byte deltas below compare these two recorded quantities, not token counts, filesystem I/O or causal context cost. Loop's earlier outputs are retained for later requests; actual replay-byte exposure is not available for both clients. Only four h2h-22 Codex files have malformed records (20 invalid lines total), so their output/counts are lower bounds; none of the passing strata has malformed records. Zero-byte output is not a missing timing.

Tail = the slowest `ceil(n/4)` by **agent wall**, among completed **baseline loop** cells per round/effort, selected before matching/filtering by pass. Tables show eligible members of that tail. h2h-29 contains 23 agent-bearing loop cells and 24 Codex cells in this snapshot; one additional result lacks events/agent wall and is excluded. h2h-25 has no Codex arm; h2h-26 has Pi/OpenCode rather than Codex. Their data were inspected and used only as recovery vocabulary; no cross-round substitutes are mixed into the paired estimates. Nonbaseline experimental arms are also excluded.

## Overall and tail comparisons

All times below are summed agent seconds; Δ is loop minus Codex. Byte counts include all loop nonterminal tool results versus completed Codex command output. Shell L/C counts compare loop shell invocations with all Codex command executions, not elementary subcommands.
''']
rr=[]
for g,pp in groups:
 ls=[p['loop'] for p in pp];cc=[p['codex'] for p in pp]
 rr.append([label(g)+(' (both false)' if not ls[0]['passed'] else ''),len(pp),sum(p['tail'] for p in pp),f"{sum(z['shell_n'] for z in ls)}/{sum(z['cmd_n'] for z in cc)}",f"{sum(z['known_shells'] for z in ls)}/{sum(z['shell_n'] for z in ls)}",num(sum(z['shell_s'] for z in ls)),num(sum(delta(p) for p in pp)),integer(sum(z['tool_bytes'] for z in ls)),integer(sum(z['cmd_bytes'] for z in cc)),f"{sum(z['tool_bytes'] for z in ls)-sum(z['cmd_bytes'] for z in cc):+,}"])
parts.append(table(['Round/effort','Pairs','Tail pairs','Shell L / cmds C','Decoded L','L shell s','Δ agent s','L bytes','C saved bytes','Δ bytes'],rr))
parts.append('The both-pass restriction matters: h2h-21 high has 22 common passes although each client passes 23/24; medium has 21 common passes. These are not the 24-cell aggregates in highwall. The larger h2h-29 snapshot also differs from highwall\'s 11-pair partial snapshot. h2h-22\'s recorded grade is false even though evaluation command status fields report successful `gotest`/acceptance commands; this report preserves the recorded outcome and does not reinterpret it as a pass.\n')
rr=[]
for g,pp in groups:
 tt=[p for p in pp if p['tail']]
 rr.append([label(g),len(tt),num(sum(p['loop']['shell_s'] for p in tt)),num(sum(delta(p) for p in tt)),integer(sum(p['loop']['tool_bytes'] for p in tt)-sum(p['codex']['cmd_bytes'] for p in tt)),num(sum(t['seconds'] for p in tt for t in sh(p) if t['command'] is None))])
parts.append(table(['Tail only','n','L shell s','Δ agent s','Δ recorded bytes','Unclassified L shell s'],rr))
parts.append('## Ranked mechanisms: measured work, excess and attribution\n\nThe ranking follows observed shell-work envelopes. It is not a sum of causal savings: command-category envelopes, repeats and output cutting overlap.\n')
parts.append('''| Rank / mechanism | Seconds and bytes observed | Beyond Codex / attribution |
|---|---|---|
| 1. Long foreground shell executions in hard-task trajectories | h2h-22: 4,263 shell s, 398,284 shell-output bytes; 4,106 s in unclassified commands. Three selected tail cells alone spend 2,840 shell s. See exact per-task bounds below. | At least 3,019.712 s across six individual hard cells exceeds even Codex's entire wall, using conservative quantization bounds. Both outcomes are recorded false. Command scope and causal avoidability remain unknown. Selecting/serially waiting for these commands is loop behavior; the tasks also require build/test/acceptance. Neither fact proves necessity. |
| 2. Slow required whole-module tests | h2h-21 expr high: first exact `GOCACHE=$PWD/.cache/go go test ./...` takes 166 s / 3,694 bytes; same command later 3 s / 3,646 bytes. h2h-29 toml: exact same prescribed test takes 47 s / 1,134 bytes. | Both tasks explicitly prescribe this whole-module command. Codex also runs module tests (expr high 3 command items, toml h2h-29 5). No measured excess category time, extra breadth or loop-specific cold-cache cause is established. The long first run is not itself a redundant rerun. |
| 3. Serial tool admission versus Codex overlap | Counts by cohort below. Loop has 2–15 responses containing multiple shells per matched stratum, executed serially. | Structural loop behavior established in cxparallel; seconds saved by concurrency are **unknown** because Codex has no timings and loop arguments mostly cannot establish independence. Read-only built-ins often complete inside a timestamp second. Do not treat all shell sums as a parallelizable budget. |
| 4. Repeated identical calls / repeated checks | Across 104 common passes: 7 repeated shell argument hashes, 7 quantized s / 5,019 bytes, plus one repeated file read / 1,831 bytes / 0 quantized s. h2h-22 separately: 6 repeated shells / 17 s / 199 bytes. See per-task table. | Loop behavior exists but is too small, as measured, to explain the hard tail; Codex also repeats commands. These are occurrence envelopes, **not avoidable excess**: edits can intervene and identical argument hashes need not yield identical output. Unknown commands may edit. |
| 5. Output volume and cutting | EU high +62,982 and medium +84,874 recorded bytes; every subscription cohort has a negative total byte delta. Loop cut counts and result sizes below. | Loop's 16 KiB head/tail cap is implementation behavior; what is emitted/read is trajectory/task-dependent. Exact additional model-context bytes and attention seconds are **unknown** on Codex. More loop context is not a general explanation of the subscription wall tail. |
| 6. Finish/check policy | Delivered baseline policy is exactly 379 bytes, SHA-256 `15ea7933c708cebd7577fc3b8fdec8660482f053fbb9e7fe894594ade1c90f2d`, matching DefaultInstructions in all 974 matched provider-attempt fingerprints; zero terminal-reminder events. Baseline tool-schema fingerprint is 2,254 bytes. | Policy says check work and finish with a truthful claim; generic finish says the caller verifies independently. It does **not** require `go test ./...`, `-race`, extra vet/build passes, or a second full suite after successful checks. Several tasks explicitly require their checks. No measured additional shell seconds can be attributed to finish rules alone. |
''')
# Verify hard lower bound aggregate, exact lower not a difference of cell sums.
positive=[(p,lower(sh(p))-p['codex']['wall']) for p in ps if lower(sh(p))>p['codex']['wall']]
parts.append('Positive excess-shell lower bounds (strictly conservative; sum only positive per-cell bounds):\n\n'+table(['Round / task / rep','Both pass','L shell interval s','C entire agent s','Guaranteed excess shell s'],[[f"{p['loop']['batch']} / {p['loop']['task']} / {p['loop']['rep']}",p['loop']['passed'],f"{num(lower(sh(p)))}–{num(upper(sh(p)))}",num(p['codex']['wall']),f'>{x:.3f}'] for p,x in positive]))
parts.append('The only positive same-pass bound is r70-1 high: **>2.803 s**. Its shell commands are unclassified, so assigning those seconds to tests, build, reads or git would be fabrication. A nonpositive bound elsewhere leaves actual shell excess unresolved; it does not mean zero.\n')
parts.append('## Commands, breadth, repetition and scheduling\n\nCounts below are command items containing a category, with compounds allowed in several columns. Loop counts are **decoded lower bounds**; every other shell is unknown. Codex heredoc source bodies are excluded from matching so a test string written into source is not counted as an executed test. Commands that invoke `make check` are listed separately: recipes may run vet/test again. `targeted` includes a named package or `-run`, and can overlap module when both occur.\n')
rr=[]
for g,pp in groups:
 ls=[t for p in pp for t in known(p)];cc=[t for p in pp for t in ct[p['codex']['key']]]
 def counts(k):return f"≥{sum(k in t.get('kinds',[]) for t in ls)}/{sum(k in t['kinds'] for t in cc)}"
 rr.append([label(g)]+[counts(k) for k in ['test','module-test','targeted-test','race','count','build','vet','format','make-check','read','git']])
parts.append(table(['Round','test L/C','module','targeted','race','count','build','vet','fmt','make check','read/discover','git'],rr))
parts.append('Builtin loop calls are separate from the shell-category counts above; their exact counts and bytes must be included when comparing inspection behavior:\n')
builtin_rows=[]
for g,pp in groups:
 aa=[t for p in pp for t in lt[p['loop']['key']] if t['name']!='shell']
 builtin_rows.append([label(g)]+[sum(t['name']==k for t in aa) for k in ['list_files','read_file','search_text','write_file']]+[num(sum(t['seconds'] for t in aa)),integer(sum(t['bytes'] for t in aa if t['name'] in ['list_files','read_file','search_text']))])
parts.append(table(['Round','list','read','search','write','Builtin s quantized','Builtin read/discovery bytes'],builtin_rows))
parts.append('The delivered shell description tells loop to run finite commands, including tests, in the foreground until completion, with no command time limit, and forbids repeated sleep/tail/ps polling for finite work. This supports serial waiting as implementation behavior; it neither mandates a wider suite nor proves that any selected long command was necessary. There is no model-facing output-size argument on this shell tool.\n')
parts.append('''`≥0` on loop is unobserved category work, not evidence it did none. In h2h-22 all 12 decoded test-bearing loop calls use package-scoped `-count=1`, not `go test ./...`; they account for 156 s including compound format/build work. The specified package check is therefore demonstrably normal in recovered commands. The 4,106 unclassified seconds could contain broader suites or custom scripts; there is no retained witness to say which. No `-race` hash is recovered in baseline loop, whereas Codex visibly uses it on TOML in the passing subscription rounds; this is not proof loop never used race.

Concrete same-task comparisons:

| Task / round | Loop exact witness | Codex witness / interpretation |
|---|---|---|
| expr high h2h-21 | Required whole-module test twice, 169 s / 7,340 bytes; required vet twice, 2 s / 30 bytes. | Three module-test commands, three vet commands, five test-bearing items total. Loop does not demonstrably test more broadly or more often here. Other loop shells remain unknown. |
| toml medium h2h-29 | Required module test once recovered, 47 s / 1,134 bytes; acceptance 3 s. | Five module-test items, one with `-race`, one additional targeted item. Loop has 11 shells versus 18 Codex commands. Recovered breadth is task-driven. |
| artifact high EU r2 | Four separate recovered test/vet/format/acceptance calls in the same model response, then `make check` at 3 s; the visible Makefile check recipe reruns test/vet (apidiag witness). | Codex also has direct go test/vet and `make check`. Extra verification beyond the task exists within both trajectories; loop-minus-Codex verification seconds are unknown. |
| review-on-demand / shell-bound h2h-22 | Exact task-format/build/project-test check chain is repeated on review-on-demand r1/r2 and shell-bound r2. | Codex also repeats verification chains and targets project/build packages. These known repeat costs are 5, 7 and 4 s, far smaller than the long unknown shells. |

''')
rr=[]
for g,pp in groups:
 rr.append([label(g),sum(p['loop']['multishell'] for p in pp),sum(p['codex']['overlap'] for p in pp),sum(p['loop']['repeat_shells'] for p in pp),num(sum(p['loop']['repeat_shell_s'] for p in pp)),integer(sum(p['loop']['repeat_shell_bytes'] for p in pp)),sum(p['codex']['codex_repeats'] for p in pp),integer(sum(crepeatbytes(p) for p in pp)),f"{sum(p['loop']['repeat_shell_bytes']-crepeatbytes(p) for p in pp):+,}"])
parts.append(table(['Round','L multishell responses','C starts while active','L repeated shells','L repeat s','L repeat bytes','C repeated command text','C repeat saved bytes','Δ repeated bytes'],rr))
parts.append('Loop repetitions use exact raw argument hashes; Codex repetitions use exact command text. The repeat-byte delta compares later occurrences with each other, not proven unnecessary context; C-only repeating tasks remain included in the cohort totals. These measures miss semantically equivalent commands, and no-edit status is not provable through unknown shells. Codex overlap counts active items, including commands that may have yielded; it is not measured CPU parallelism.\n')
# Repeats by individual task, all nonterminal tools.
rr=[]
for p in ps:
 l=p['loop'];seen=set();dups=[]
 for t in lt[l['key']]:
  k=(t['name'],t['arg'])
  if k in seen:dups.append(t)
  seen.add(k)
 if dups:rr.append([label(grp(p)),l['task']+'/'+l['rep'],','.join(t['name'] for t in dups),num(sum(t['seconds'] for t in dups)),integer(sum(t['bytes'] for t in dups)),l['same_result_repeats'],p['codex']['codex_repeats'],integer(crepeatbytes(p)),f"{sum(t['bytes'] for t in dups)-crepeatbytes(p):+,}"])
parts.append(table(['Round','Task/rep','Repeated tools','Later-call s','Later-call bytes','Same result too (n)','C repeats','C repeat saved bytes','Δ repeated bytes'],rr))
parts.append('## Output bytes per result and cut behavior\n\nThe loop cap keeps the first 4,096 bytes and a suffix around an omission marker, at most 16,384 bytes per result (`tools/tools.go:523–555`). It does not stop the command early or prevent it from generating discarded output. No shell time saving follows from the byte cap alone. Codex markers here count visible truncation/omission language in saved output and are only a heuristic; they do not measure its model-facing output cap.\n')
def pct(vals,q):return sorted(vals)[max(0,math.ceil(len(vals)*q)-1)] if vals else 0
rr=[]
for g,pp in groups:
 a=[t for p in pp for t in lt[p['loop']['key']]];b=[t for p in pp for t in ct[p['codex']['key']]]
 for side,values,cuts in [('loop',[t['bytes'] for t in a],sum(t['cut'] for t in a)),('Codex saved',[t['output_bytes'] for t in b],sum(t['cut'] for t in b))]:
  rr.append([label(g),side,len(values),integer(int(statistics.median(values))),integer(pct(values,.9)),integer(max(values)),cuts])
parts.append(table(['Round','Side','Results','Median bytes','p90 bytes','Max bytes','Cuts / C marker hits'],rr))
parts.append('Loop-only logical result replay exposure is the sum of each delivered result bytes multiplied by the number of subsequent saved provider attempts. This follows the supplied engine history. It counts result text once per later attempt, excluding JSON/tool framing, source-generation output and terminal claims; it is not tokenizer input or a captured request-body byte total. Codex lacks attempt boundaries and model-delivered result text, so its counterpart and the exact replay excess are unknown.\n')
parts.append(table(['Round','Loop result bytes delivered once','Loop logical replay bytes','Codex replay / excess'],[[label(g),integer(sum(p['loop']['tool_bytes'] for p in pp)),integer(sum(p['loop']['logical_replay_bytes'] for p in pp)),'? / ?'] for g,pp in groups]))
parts.append('EU excess by task, both repetitions summed; total-output delta is exact for the recorded quantities. Shell versus builtin-read delivery is shown without pretending to know which category an unknown shell belongs to:\n')
rr=[]
for g,pp in groups[:2]:
 for task,v in itertools.groupby(sorted(pp,key=lambda p:p['loop']['task']),lambda p:p['loop']['task']):
  vv=list(v);rr.append([label(g),task,num(sum(p['loop']['shell_s'] for p in vv)),integer(sum(p['loop']['shell_bytes'] for p in vv)),integer(sum(p['loop']['read_bytes'] for p in vv)),integer(sum(p['codex']['cmd_bytes'] for p in vv)),f"{sum(p['loop']['tool_bytes']-p['codex']['cmd_bytes'] for p in vv):+,}"])
parts.append(table(['EU effort','Task','L shell s','L shell bytes','L builtin read bytes','C all saved bytes','Δ all bytes'],rr))
parts.append('## Per-task wall, shell and byte accounting\n\nEvery matched task is included below. EU/hard rows sum the two repetitions; other rows are one rep. `T` lists reps selected by the pre-filter tail rule. `Excess lower` is the sum of the signed per-cell lower bounds, not an estimate; positive individual bounds can be seen above even when the task sum is negative. C shell seconds and exact category excess seconds remain `?` for every row. Columns with C output/count are lower bounds in the four malformed hard-task files.\n')
for g,pp in groups:
 parts.append('### '+label(g)+(' — both recorded false' if not pp[0]['loop']['passed'] else ' — both pass')+'\n')
 rr=[]
 for task,v in itertools.groupby(sorted(pp,key=lambda p:p['loop']['task']),lambda p:p['loop']['task']):
  vv=list(v);ss=[t for p in vv for t in sh(p)];rr.append([task,len(vv),','.join(p['loop']['rep'] for p in vv if p['tail']) or '—',f"{sum(p['loop']['shell_n'] for p in vv)}/{sum(p['codex']['cmd_n'] for p in vv)}",sum(len(known(p)) for p in vv),num(sum(t['seconds'] for t in ss)),f"{num(lower(ss))}–{num(upper(ss))}",num(sum(lower(sh(p))-p['codex']['wall'] for p in vv)),f"{sum(delta(p) for p in vv):+.1f}",f"{sum(p['loop']['tool_bytes'] for p in vv):,}/{sum(p['codex']['cmd_bytes'] for p in vv):,}",f"{sum(p['loop']['tool_bytes']-p['codex']['cmd_bytes'] for p in vv):+,}"])
 parts.append(table(['Task','n','T','Shell L/C cmds','Decoded','L shell s','L interval s','Excess lower s','Δ wall s','Bytes L/C','Δ bytes'],rr))
parts.append('''## Mechanism accounting files and what remains unresolved

- `shelltail-cells.csv`: every paired repetition, pass/tail status, shell intervals and excess lower bound, total/shell/read bytes, repeats, concurrency and **per-task test/build/vet/format/read/git/scope counts**. Loop category counts are decoded lower bounds.
- `shelltail-mechanisms.csv`: per task/rep, disjoint command buckets, observed loop seconds/bytes, Codex saved bytes/count, and the unclassified-shell budget that could still belong to each bucket. Test-containing compounds go to module/targeted/other-test first, then make-check, acceptance, build, vet, format, git, read, other. Thus a compound's entire seconds/output are an envelope, not time spent solely inside its test. Separate category counts above intentionally overlap.
- For a bucket with K decoded loop bytes, U unclassified loop-shell bytes and C saved Codex bytes, the possible **recorded-output** delta is `[K−C, K+U−C]`; CSV supplies both endpoints. They are not additive across mechanisms because U cannot be allocated to all simultaneously. For `unclassified-shell`, the row is the unresolved pool itself rather than a candidate semantic mechanism. Codex context bytes and exact excess seconds are blank, never zero. Exact positive context overhead cannot be claimed from these bounds.
- `shelltail-recovered-commands.jsonl`: all 81 matched decoded loop commands with original argument hashes, call IDs, sequence numbers, seconds and result bytes. No tool output bodies, encrypted reasoning or credentials are published.
- `shelltail-sources.json`: private archive paths, byte sizes, SHA-256 receipts and per-input hashes. Reproduction scripts are retained at the private snapshot path in that receipt (`analyze.py`, `report.py`). No product source was changed.

The evidence does **not** show a universal loop tendency toward more shell invocations, more returned bytes, more `-race`, or more whole-module tests. It does show much longer selected shell executions on the hard tasks, one provable small shell excess on a common passing task, serial loop admission, and small measured repeat-call envelopes. Full per-command excess attribution requires the original loop argument/output transcript and Codex command start/end plus model-delivered output, which these completed cells did not retain. Labelling the unexplained 6,113 shell seconds “build/test redundancy” would overstate the evidence; labelling them inherently unavoidable would be equally unsupported.
''')
text='\n'.join(parts)
# Derive this particular bound rather than carrying a hand-calculated transcription.
hard=sum(x for p,x in positive if p['loop']['batch']=='h2h-22')
text=text.replace('3,019.712',f'{hard:,.3f}')
(O/'shelltail.md').write_text(text)
print('wrote',len(text),'chars; positive hard bound',hard,'pass pairs',sum(p['loop']['passed'] for p in ps),'tail pairs',sum(p['tail'] for p in ps),'mechanism rows',len(mech))
