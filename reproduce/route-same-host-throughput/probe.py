"""Same-host route A/B/C of output streaming rate, each route through its own client. 
Routes:  Lc  kogen-loop binary (loop's ChatGPT login; api.openai.com/v1/responses); timing from loop's own
             request.attempt record (ttft_ms = first parsed delta, last_byte_ms), both from request start.
         Lr  raw HTTP/SSE to api.openai.com/v1/responses with loop's credential (subroute-probe.py route A, empty UA).
         C   Codex 0.165.0 `codex app-server` (stdio JSON-RPC; initialize clientInfo name codex_exec, as `codex exec` uses in process);
             first item/agentMessage/delta -> item/completed(agentMessage); usage from thread/tokenUsage/updated.
         P   Pi 0.73.1 `pi --print --mode json`; first text_delta -> message_end; usage from message_end.
Credentials are only read by their own clients, except Lr, which reads loop's token in memory (never printed)
and sends it only to api.openai.com. Prints one JSON record per request: timings, usage, status. No content.
usage: probe.py HOST BLOCKS ROUTES   e.g. Linux-A 20 Lc,C,P,Lr   (HOST is only a label written into each record)
Required env: RAB_JOB (empty scratch dir), RAB_LOOP_BIN, RAB_CODEX_BIN, RAB_CODEX_HOME; optional RAB_LOOP_HOME,
RAB_LOOP_CRED, RAB_PI_BIN, RAB_PI_DIR, RAB_HOME. Never put credentials in the command line.
"""
import json, os, sys, time, uuid, signal, datetime, subprocess, select, urllib.request, tempfile, pathlib

HOME = pathlib.Path(os.environ.get('RAB_HOME', os.path.expanduser('~')))
MODEL, EFFORT = 'gpt-6.1-terra', 'medium'
PROMPT = ('Do not use any tools. In plain prose only (no headings, no lists, no code, no markdown), write about '
          '400 words describing how a small coastal town changes from early morning to late evening. '
          'Reply with the prose only.')
J = pathlib.Path(os.environ['RAB_JOB'])            # empty scratch dir for this run
LOOP_BIN = os.environ['RAB_LOOP_BIN']
LOOP_HOME = os.environ.get('RAB_LOOP_HOME', str(HOME))   # home dir holding loop's own login
CODEX_BIN = os.environ['RAB_CODEX_BIN']
CODEX_HOME = os.environ['RAB_CODEX_HOME']
PI_BIN = os.environ.get('RAB_PI_BIN', '')
PI_DIR = os.environ.get('RAB_PI_DIR', '')
TIMEOUT = 240
L_INSTR = 'Follow the user request exactly. Do not use tools.'   # same instructions as Lr; loop's default tells the model to call finish

def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def rec(**k): print(json.dumps(k), flush=True)

def busy():
    """Overlap tagging was specific to the original hosts and is omitted here."""
    return []

def spawn(cmd, env, cwd, stdin=subprocess.DEVNULL):
    return subprocess.Popen(cmd, env=env, cwd=cwd, stdin=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            start_new_session=True)

def stop(p):
    if p.poll() is None:
        try: os.killpg(p.pid, signal.SIGTERM)
        except ProcessLookupError: pass
        try: p.wait(5)
        except subprocess.TimeoutExpired:
            try: os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError: pass
            p.wait()

def lines(p, t0, until):
    """Yield (t_since_t0, parsed JSON) for each stdout line until until(obj) is true or timeout."""
    buf = b''; fd = p.stdout.fileno()
    while time.monotonic() - t0 < TIMEOUT:
        r, _, _ = select.select([fd], [], [], 1.0)
        if not r:
            if p.poll() is not None: return
            continue
        c = os.read(fd, 65536)
        if not c: return
        now = time.monotonic() - t0; buf += c
        while b'\n' in buf:
            l, buf = buf.split(b'\n', 1)
            try: o = json.loads(l)
            except ValueError: continue
            yield now, o
            if until(o): return

def base_env(extra):
    t = J / 'agent-tmp'; t.mkdir(exist_ok=True)
    env = dict(PATH='/usr/local/bin:/usr/bin:/bin', LANG='C.UTF-8', HOME=str(HOME), TMPDIR=str(t),
               GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT='0')
    env.update(extra); return env

def fresh_ws():
    return tempfile.mkdtemp(prefix='ws-', dir=J)

# --- Lc: kogen-loop binary --------------------------------------------------------------------------------------
def run_Lc():
    ws = fresh_ws()
    task = {'protocol': 'kogen-loop/v1', 'root': ws,
            'role': {'provider': 'chatgpt', 'model': MODEL, 'effort': EFFORT, 'base_url': ''},
            'instructions': L_INSTR, 'prompt': PROMPT, 'tools': [], 'protected': [], 'excluded': [],
            'terminal': ['finish'], 'deadline_seconds': TIMEOUT - 30,
            'session': {'dir': os.path.join(ws, '.loop-session'), 'resume': False}, 'requires': []}
    tf = os.path.join(J, 'task-%s.json' % uuid.uuid4().hex); json.dump(task, open(tf, 'w'))
    t0 = time.monotonic(); p = spawn([LOOP_BIN, 'run', '--task', tf], base_env({'HOME': LOOP_HOME}), ws)
    attempts, kinds, resp = [], [], {}
    try:
        for now, o in lines(p, t0, lambda o: o.get('type') == 'session.ended'):
            k = o.get('type'); kinds.append(k)
            if k == 'request.attempt': attempts.append(o)
            if k == 'response': resp = o
    finally: stop(p)
    def flat(a):
        d = {}
        for src in (a, a.get('fields') or {}, a.get('record') or {}): d.update({k: v for k, v in src.items() if k not in ('fields', 'record')})
        return d
    A = []
    for a in attempts:
        d = flat(a); u = d.get('usage') or {}
        out = u.get('output_tokens', u.get('output')); rs = u.get('reasoning', u.get('reasoning_tokens'))
        A.append(dict(output=out, reasoning=rs, ttft_ms=d.get('ttft_ms'), first_byte_ms=d.get('first_byte_ms'),
                      last_byte_ms=d.get('last_byte_ms'), wall_ms=d.get('wall_ms'), tier=d.get('effective_service_tier'),
                      requested_tier=d.get('requested_service_tier'), outcome=d.get('outcome'),
                      http_status=d.get('http_status', d.get('status')), effective_model=d.get('effective_model'),
                      effective_effort=d.get('effective_effort'), end_reason=d.get('end_reason')))
    # the prose is generated in the attempt with the most visible output; later attempts (if any) only call 'finish'
    vis = lambda x: (x['output'] or 0) - (x['reasoning'] or 0)
    a = max(A, key=vis) if A else {}
    ttft, last = a.get('ttft_ms'), a.get('last_byte_ms')
    return dict(client='kogen-loop', first_out_s=ttft / 1000 if ttft is not None else None,
                end_s=last / 1000 if last is not None else None, first_byte_s=(a.get('first_byte_ms') or 0) / 1000 or None,
                output=a.get('output'), reasoning=a.get('reasoning'), tier=a.get('tier'), requested_tier=a.get('requested_tier'),
                outcome=a.get('outcome'), http_status=a.get('http_status'), effective_model=a.get('effective_model'),
                effective_effort=a.get('effective_effort'), prose_attempt=A.index(a) + 1 if A else None, attempts=A,
                exit=p.returncode, kinds=sorted(set(kinds)))

# --- Lr: raw HTTP/SSE, loop's credential, api.openai.com only ----------------------------------------------------
def run_Lr():
    cred = json.load(open(os.environ.get('RAB_LOOP_CRED', os.path.join(LOOP_HOME, '.kogen/credentials/chatgpt.json')))); tok = cred['access_token']
    if (cred.get('expires_at') or 0) < time.time() + 30:   # never send an expired token; loop (Lc) refreshes its own login
        return dict(client='raw-sse', error='token-expired-not-sent')
    sid = str(uuid.uuid4())
    body = dict(model=MODEL, instructions=L_INSTR,
                input=[dict(role='user', content=[dict(type='input_text', text=PROMPT)])], reasoning=dict(effort=EFFORT),
                include=['reasoning.encrypted_content'], stream=True, store=False, prompt_cache_key=sid)
    h = {'Content-Type': 'application/json', 'Accept': 'text/event-stream', 'session_id': sid, 'conversation_id': sid,
         'Authorization': 'Bearer ' + tok, 'User-Agent': ''}
    st = dict(first=None, last=None, delta=None, usage={}, tier=None, status=None); buf = b''; t0 = time.monotonic()
    try:
        with urllib.request.urlopen(urllib.request.Request('https://api.openai.com/v1/responses', data=json.dumps(body).encode(),
                                                           headers=h, method='POST'), timeout=60) as r:
            st['status'] = r.status
            while True:
                c = r.read1(65536)
                if not c: break
                now = time.monotonic() - t0
                if st['first'] is None: st['first'] = now
                st['last'] = now; buf += c
                while b'\n\n' in buf:
                    blk, buf = buf.split(b'\n\n', 1)
                    for line in blk.splitlines():
                        if not line.startswith(b'data:') or line[5:].strip() == b'[DONE]': continue
                        try: e = json.loads(line[5:].strip())
                        except ValueError: continue
                        k = e.get('type', '')
                        if k == 'response.output_text.delta':
                            st['chars'] = st.get('chars', 0) + len(e.get('delta') or '')
                            if st['delta'] is None: st['delta'] = now
                        if k == 'response.completed':
                            rr = e.get('response', {}); st['usage'] = rr.get('usage', {}); st['tier'] = rr.get('service_tier')
    except Exception as e:
        return dict(client='raw-sse', error=type(e).__name__, http_status=getattr(e, 'code', None))
    u = st['usage']
    return dict(client='raw-sse', first_out_s=st['delta'], first_byte_s=st['first'], end_s=st['last'],
                output=u.get('output_tokens'), reasoning=(u.get('output_tokens_details') or {}).get('reasoning_tokens'),
                tier=st['tier'], http_status=st['status'], chars=st.get('chars'))

# --- C: Codex app-server ----------------------------------------------------------------------------------------
def run_C():
    ws = fresh_ws()
    ci = {'name': 'codex_exec', 'title': None, 'version': '0.165.0'}
    p = spawn([CODEX_BIN, 'app-server'], base_env({'CODEX_HOME': CODEX_HOME}), ws,
              stdin=subprocess.PIPE)
    def send(o): p.stdin.write((json.dumps(o) + '\n').encode()); p.stdin.flush()
    st = dict(first=None, end=None, usage=None, done=None, err=None, kinds=set(), tier=None, model=None)
    t0 = time.monotonic(); t_turn = None
    try:
        send({'id': 1, 'method': 'initialize', 'params': {'clientInfo': ci}})
        thread = None
        for now, o in lines(p, t0, lambda o: o.get('id') == 2 or 'error' in o):
            if o.get('id') == 1 and 'result' in o:
                send({'method': 'initialized'})
                send({'id': 2, 'method': 'thread/start', 'params': {'model': MODEL, 'cwd': ws, 'approvalPolicy': 'never',
                                                                     'sandbox': 'read-only', 'ephemeral': True}})
            if o.get('id') == 2: thread = (o.get('result') or {}).get('thread', {}).get('id'); st['err'] = o.get('error')
            if 'error' in o: st['err'] = o['error']; break
        if thread:
            t_turn = time.monotonic() - t0
            send({'id': 3, 'method': 'turn/start', 'params': {'threadId': thread, 'effort': EFFORT,
                                                               'input': [{'type': 'text', 'text': PROMPT, 'text_elements': []}]}})
            for now, o in lines(p, t0, lambda o: o.get('method') in ('turn/completed',)):
                m = o.get('method'); st['kinds'].add(m or ('resp%s' % o.get('id')))
                pr = o.get('params') or {}
                if 'id' in o and 'method' in o:      # server request (approval etc.): decline
                    send({'id': o['id'], 'error': {'code': -32601, 'message': 'declined by probe'}})
                if m == 'item/agentMessage/delta':
                    st['chars'] = st.get('chars', 0) + len(pr.get('delta') or '')
                    if st['first'] is None: st['first'] = now; st['first_ms'] = o.get('emittedAtMs')
                    st['last_delta_ms'] = o.get('emittedAtMs')
                if m == 'item/completed' and (pr.get('item') or {}).get('type') == 'agentMessage':
                    st['end'] = now; st['end_ms'] = o.get('emittedAtMs')
                if m == 'thread/tokenUsage/updated': st['usage'] = pr.get('tokenUsage')
                if m == 'model/rerouted': st['model'] = pr
                if m == 'turn/completed': st['done'] = now; st['turn_status'] = (pr.get('turn') or {}).get('status'); \
                    st['err'] = (pr.get('turn') or {}).get('error')
                if m == 'error': st['err'] = pr
    finally:
        try: p.stdin.close()
        except Exception: pass
        stop(p)
    if st['first'] is None:
        st['stderr_tail'] = p.stderr.read()[-300:].decode('utf-8', 'replace')
    last = ((st['usage'] or {}).get('last') or {})
    f = lambda x: None if x is None or t_turn is None else x - t_turn
    return dict(client='codex-app-server', first_out_s=f(st['first']), end_s=f(st['end']), turn_done_s=f(st['done']),
                output=last.get('outputTokens'), reasoning=last.get('reasoningOutputTokens'), input=last.get('inputTokens'),
                turn_status=st.get('turn_status'), error=st['err'], rerouted=st['model'], kinds=sorted(st['kinds']),
                stderr_tail=st.get('stderr_tail'), chars=st.get('chars'),
                server_stream_s=(st['end_ms'] - st['first_ms']) / 1000 if st.get('end_ms') and st.get('first_ms') else None)

# --- P: Pi --------------------------------------------------------------------------------------------------------
def run_P():
    ws = fresh_ws()
    cmd = [PI_BIN, '--print', '--mode', 'json', '--no-session', '--provider', 'openai-codex', '--model', MODEL,
           '--thinking', EFFORT, '--no-tools', '--no-context-files', '--no-extensions', '--no-skills', PROMPT]
    t0 = time.monotonic(); p = spawn(cmd, base_env({'PI_CODING_AGENT_DIR': PI_DIR}), ws)
    st = dict(start=None, first=None, end=None, usage=None, stop=None, err=None, kinds=set())
    try:
        for now, o in lines(p, t0, lambda o: o.get('type') == 'agent_end'):
            k = o.get('type'); st['kinds'].add(k)
            if k in ('agent_start', 'turn_start') and st['start'] is None: st['start'] = now
            ev = o.get('assistantMessageEvent') or {}
            if k == 'message_update' and ev.get('type') == 'text_delta':
                st['chars'] = st.get('chars', 0) + len(ev.get('delta') or '')
                if st['first'] is None: st['first'] = now
            if k == 'message_update' and (ev.get('type') or '').startswith('thinking'): st['thinking_events'] = st.get('thinking_events', 0) + 1
            if k == 'message_end' and (o.get('message') or {}).get('role') == 'assistant':
                m = o['message']; st['end'] = now; st['usage'] = m.get('usage'); st['stop'] = m.get('stopReason')
                st['err'] = m.get('errorMessage')
                st['content_types'] = sorted({c.get('type') for c in m.get('content') or [] if isinstance(c, dict)})
    finally: stop(p)
    u = st['usage'] or {}; s = st['start']
    f = lambda x: None if x is None or s is None else x - s
    return dict(client='pi', first_out_s=f(st['first']), end_s=f(st['end']), launch_to_start_s=s,
                output=u.get('output'), reasoning=u.get('reasoning'), stop=st['stop'], error=st['err'],
                kinds=sorted(st['kinds']), usage_keys=sorted(u),
                chars=st.get('chars'), thinking_events=st.get('thinking_events', 0), content_types=st.get('content_types'))

RUN = {'Lc': run_Lc, 'Lr': run_Lr, 'C': run_C, 'P': run_P}
ROUTE = {'Lc': 'L', 'Lr': 'L', 'C': 'C', 'P': 'P'}

def main():
    host, blocks, routes = sys.argv[1], int(sys.argv[2]), sys.argv[3].split(',')
    for b in range(1, blocks + 1):
        k = (b - 1) % len(routes); order = routes[k:] + routes[:k]
        for pos, r in enumerate(order):
            busy0, started, w0 = busy(), utc(), time.monotonic()
            try: res = RUN[r]()
            except Exception as e: res = dict(error='%s: %s' % (type(e).__name__, str(e)[:200]))
            wall = time.monotonic() - w0
            fo, en, out, rs = res.get('first_out_s'), res.get('end_s'), res.get('output'), res.get('reasoning')
            span = en - fo if fo is not None and en is not None else None
            vis = out - rs if out is not None and rs is not None else None
            rec(host=host, block=b, pos=pos, order=''.join(order), probe=r, route=ROUTE[r], started=started, ended=utc(),
                wall_s=round(wall, 3), rate_out=out / span if out and span else None,
                rate_visible=vis / span if vis and span else None, stream_s=span,
                overlap_start=busy0, overlap_end=busy(), **res)
            time.sleep(2)

if __name__ == '__main__':
    main()
