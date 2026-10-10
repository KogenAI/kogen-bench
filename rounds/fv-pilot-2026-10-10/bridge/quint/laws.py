"""Fixed contract encoder. Never reads implementation bodies."""
import json
from emit import name, qtype

def val(v):
    if isinstance(v,bool):return str(v).lower()
    if isinstance(v,int):return str(v)
    if isinstance(v,str):return json.dumps(v)
    return '{ '+', '.join(name(k)+': '+val(x) for k,x in sorted(v.items()))+' }'

def upd(laws,s,fields):
    return '{ '+', '.join(name(f)+': '+fields.get(f,s+'.'+name(f)) for f in sorted(laws['state_fields']))+' }'

def generate_laws(laws,e):
    task=laws['task'];mod=laws['module'];lines=['// FIXED: accepted laws and domains; hash checked before every repair.','module laws {','  import app.* from "./app"']
    expected_ids={'F01':['read_iff'],'W01':['approval_binding','edit','admission_iff'],'W04':['success','failure','cleanup_gate','retry_idempotent'],'X01':['selection','reuse_iff','recompute']}
    if [x['id'] for x in laws['laws']]!=expected_ids.get(task):raise ValueError('unsupported fixed law catalog '+task)
    def fn(n,a):return e.fname((mod,n,a))
    if task=='F01':
        lines+=['  var actor: { tenant: str, role: str }','  var resource: { tenant: str }','  var result: bool',
          '  action init = {',
          '    nondet at = '+valset(laws['domains']['tenant']+['__missing__'])+'.oneOf()',
          '    nondet rt = '+valset(laws['domains']['tenant']+['__missing__'])+'.oneOf()',
          '    nondet role = '+valset(laws['domains']['role']+['__missing__'])+'.oneOf()',
          '    val a = { tenant: at, role: role }',
          '    val r = { tenant: rt }',
          '    all { actor\' = a, resource\' = r, result\' = '+fn('can_read',2)+'(a, r) }','  }',
          "  action step = all { actor' = actor, resource' = resource, result' = result }",
          '  val law_read_iff = result == (actor.tenant != "__missing__" and actor.role != "__missing__" and resource.tenant != "__missing__" and actor.tenant == resource.tenant and (actor.role == "owner" or actor.role == "viewer"))']
    else:
        st='{ '+', '.join(name(f)+': '+('bool' if d=='boolean' else 'int' if isinstance(laws['domains'].get(d),dict) else 'str') for f,d in sorted(laws['state_fields'].items()))+' }';bound=laws['max_sequence_length']
        lines+=['  var state: '+st,'  var before: '+st,'  var event: str','  var depth: int',
          '  pure val fixed_initial = '+val(laws['initial']),
          '  action init = {']
        if laws.get('enumerate_all_states'):
            for field in sorted(laws['state_fields']):lines.append(f'    nondet initial_{field} = Set(false, true).oneOf()')
            initial='{ '+', '.join(f'{name(f)}: initial_{f}' for f in sorted(laws['state_fields']))+' }'
        else:initial=fn('init',0)
        lines+=['    val initial = '+initial,"    all { state' = initial, before' = initial, event' = \"__init__\", depth' = 0 }",'  }',
          '  action step = {', '    nondet chosen = '+valset(laws['events'])+'.oneOf()',
          f'    if (depth < {bound}) all {{ before\' = state, event\' = chosen, state\' = {fn("step",2)}(state, chosen), depth\' = depth + 1 }}',
          "    else all { before' = before, event' = event, state' = state, depth' = depth }",'  }']
        expected={}
        if task=='W01':
            expected['approval_binding']='(event != "approve" or state == '+upd(laws,'before',{'approved':'before.revision'})+')'
            expected['edit']='((event != "edit_r1" or state == '+upd(laws,'before',{'revision':'"r1"','admitted':'false'})+') and (event != "edit_r2" or state == '+upd(laws,'before',{'revision':'"r2"','admitted':'false'})+'))'
            expected['admission_iff']='(event != "start" or state == '+upd(laws,'before',{'admitted':'before.approved == before.revision'})+')'
        elif task=='W04':
            expected['success']='(event != "preserve_ok" or state == '+upd(laws,'before',{'saved':'before.saved or before.work','pending':'before.work'})+')'
            expected['failure']='(event != "preserve_fail" or state == '+upd(laws,'before',{'pending':'before.work'})+')'
            expected['cleanup_gate']='((event != "cleanup" and event != "retry") or state == (if (before.pending and before.saved) '+upd(laws,'before',{'work':'false','pending':'false'})+' else before))'
            expected['retry_idempotent']='(event != "retry" or '+fn('step',2)+'(state, "retry") == state)'
        elif task=='X01':
            parts=[]
            for ev in laws['events']:
                if ev=='request':continue
                field,token=ev.split('_',1)
                parts.append('(event != '+val(ev)+' or state == '+upd(laws,'before',{field:val(token),'reused':'false'})+')')
            expected['selection']='('+' and '.join(parts)+')'
            hit='(before.cached_tree == before.tree and before.cached_context == before.context)'
            expected['reuse_iff']='(event != "request" or (state.reused == '+hit+' and (not('+hit+') or state == '+upd(laws,'before',{'reused':'true'})+')))'
            expected['recompute']='(event != "request" or '+hit+' or state == '+upd(laws,'before',{'cached_tree':'before.tree','cached_context':'before.context','computations':'before.computations + 1','reused':'false'})+')'
        else:raise ValueError('unsupported fixed task '+task)
        for law in laws['laws']:
            if law['id'] not in expected:raise ValueError('unknown fixed law '+law['id'])
            lines.append('  val law_'+name(law['id'])+' = ('+fn('init',0)+' == fixed_initial) and (depth == 0 or '+expected[law['id']]+')')
    lines+=['  val all_laws = '+' and '.join('law_'+name(l['id']) for l in laws['laws']),'}']
    return '\n'.join(lines)+'\n'

def valset(xs):return 'Set('+', '.join(val(x) for x in xs)+')'
