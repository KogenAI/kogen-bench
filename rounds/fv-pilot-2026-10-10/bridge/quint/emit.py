#!/usr/bin/env python3
"""Source IR v1 -> typed Quint. No application code runs here."""
import argparse
import hashlib
import json
import re
from pathlib import Path

class TranslationError(Exception):
    pass

def fail(node, reason):
    loc = node.get('loc', {})
    raise TranslationError(f"FV-QUINT {loc.get('file','?')}:{loc.get('line',0)}:{loc.get('column',0)}: {reason}")

def name(s):
    return re.sub(r'[^A-Za-z0-9_]', '_', s) + ('_fn' if s in {'init','step','match','type','val','var','and','or','not','if','else','Set','Map','List'} else '')

class TV:
    def __init__(self): self.ref = None

class RecordType(dict):
    def __init__(self, fields, identity=None, optional=()):
        super().__init__(fields);self.identity=identity;self.optional=set(optional)

def prune(t):
    if isinstance(t, TV) and t.ref is not None:
        t.ref = prune(t.ref)
        return t.ref
    return t

def unify(a, b, node):
    a,b = prune(a),prune(b)
    if a is b: return
    if isinstance(a, TV): a.ref=b; return
    if isinstance(b, TV): b.ref=a; return
    if isinstance(a, dict) and isinstance(b, dict):
        if isinstance(a,RecordType) and isinstance(b,RecordType):
            if a.identity is not None and b.identity is not None and a.identity!=b.identity:
                fail(node,'incompatible record identities '+a.identity+' and '+b.identity)
            identity=a.identity if a.identity is not None else b.identity
            a.identity=b.identity=identity
            optional=a.optional|b.optional
            a.optional=b.optional=optional
        for key in set(a)|set(b):
            if key in a and key in b: unify(a[key], b[key], node)
            elif key in a: b[key]=a[key]
            else: a[key]=b[key]
        return
    if isinstance(a, tuple) and isinstance(b, tuple) and len(a)==len(b):
        for x,y in zip(a,b): unify(x,y,node)
        return
    if a != b: fail(node, f'inconsistent types {a} and {b}')

def qtype(t, node):
    t=prune(t)
    if isinstance(t,TV): fail(node,'unresolved type (no unchecked polymorphism)')
    if isinstance(t,dict): return '{ ' + ', '.join(f'{name(k)}: {qtype(v,node)}' for k,v in sorted(t.items()))+' }'
    if isinstance(t,tuple): return '('+', '.join(qtype(v,node) for v in t)+')'
    return t

class Emitter:
    def __init__(self,ir,laws):
        self.ir,self.laws=ir,laws
        self.fns={}; self.types={}; self.node_types={}; self.source_map=[]
        for mod in ir['modules']:
            for fn in mod['functions']:
                key=(mod['name'],fn['name'],len(fn['params']))
                self.fns.setdefault(key,[]).append(fn)
                self.types.setdefault(key,([TV() for _ in fn['params']],TV()))
        self.mod=ir['modules'][0]['name']
        emitted={}
        for key in self.fns:
            identifier=self.fname(key)
            if identifier in emitted:fail(self.fns[key][0],'generated identifier collision')
            emitted[identifier]=key
        required=[(laws['module'],'can_read',2)] if laws['task']=='F01' else [(laws['module'],'init',0),(laws['module'],'step',2)]
        for key in required:
            if key not in self.fns:fail(ir['modules'][0],'missing fixed public API '+str(key))
    def fkey(self,node):
        key=(node.get('module') or self.mod,node['name'],len(node['args']))
        if key not in self.fns: fail(node,'unknown call '+str(key))
        return key
    def fname(self,key): return name(key[0].replace('.','_')+'_'+key[1]+'_'+str(key[2]))
    def pattern(self,p,t,env,seen=None):
        seen=set() if seen is None else seen
        k=p['kind']
        if k=='var':
            if p['name'] in seen:fail(p,'repeated pattern variables are outside the subset')
            seen.add(p['name']);env[p['name']]=t
        elif k=='wildcard': pass
        elif k in ('atom','bool','int'): unify(t,{'atom':'str','bool':'bool','int':'int'}[k],p)
        elif k=='record_pattern':
            fields=RecordType({f['name']:TV() for f in p['fields']}); unify(t,fields,p)
            for f in p['fields']: self.pattern(f['value'],fields[f['name']],env,seen)
        elif k=='tuple_pattern':
            if len(p['items'])<2:fail(p,'tuples must have at least two components')
            ts=tuple(TV() for _ in p['items']); unify(t,ts,p)
            for x,xt in zip(p['items'],ts): self.pattern(x,xt,env,seen)
        else: fail(p,'unsupported pattern '+k)
        self.node_types[id(p)]=t
    def infer(self,n,env):
        k=n['kind']; t=TV()
        if k=='var':
            if n['name'] not in env: fail(n,'unbound variable '+n['name'])
            t=env[n['name']]
        elif k in ('atom','bool','int'):
            if k=='atom' and n['value']=='__missing__':fail(n,'reserved missing-field token is outside the atom domain')
            t={'atom':'str','bool':'bool','int':'int'}[k]
        elif k=='get':
            base=self.infer(n['base'],env); unify(base,RecordType({n['field']:t}),n)
        elif k in ('record','update'):
            fields={f['name']:self.infer(f['value'],env) for f in n['fields']}
            if k=='record':
                t=RecordType(fields,n.get('struct') or 'map')
                if n.get('struct'):t['__struct__']='str'
            else:
                t=self.infer(n['base'],env); unify(t,RecordType(fields,n.get('struct')),n)
        elif k=='tuple':
            if len(n['items'])<2:fail(n,'tuples must have at least two components')
            t=tuple(self.infer(x,env) for x in n['items'])
        elif k=='binary':
            a=self.infer(n['left'],env); b=self.infer(n['right'],env)
            if n['op'] in ('and','or'): unify(a,'bool',n);unify(b,'bool',n);t='bool'
            elif n['op'] in ('==','!='): unify(a,b,n);t='bool'
            elif n['op'] in ('+','-'): unify(a,'int',n);unify(b,'int',n);t='int'
            else: fail(n,'unsupported operator '+n['op'])
        elif k=='unary': unify(self.infer(n['value'],env),'bool',n);t='bool'
        elif k=='if':
            unify(self.infer(n['condition'],env),'bool',n)
            t=self.infer(n['then'],env);unify(t,self.infer(n['else'],env),n)
        elif k=='case':
            vt=self.infer(n['value'],env)
            for branch in n['branches']:
                benv=dict(env);self.pattern(branch['pattern'],vt,benv);unify(t,self.infer(branch['body'],benv),branch)
        elif k=='let':
            benv=dict(env);self.pattern(n['pattern'],self.infer(n['value'],env),benv);t=self.infer(n['body'],benv)
        elif k=='call':
            if n.get('module')=='Map':
                if n['name'] not in ('get','has_key?'): fail(n,'unsupported Map call')
                field=n['args'][1]
                if field['kind']!='atom':fail(n,'dynamic field')
                ft=TV();unify(self.infer(n['args'][0],env),RecordType({field['value']:ft}),n)
                if n['name']=='get':
                    if len(n['args'])!=3:fail(n,'Map.get requires explicit default')
                    unify(ft,self.infer(n['args'][2],env),n);t=ft
                else:t='bool'
            else:
                ats,rt=self.types[self.fkey(n)]
                for arg,at in zip(n['args'],ats):unify(self.infer(arg,env),at,n)
                t=rt
        else:fail(n,'unsupported expression '+k)
        self.node_types[id(n)]=t;return t
    def infer_all(self):
        if self.laws['task']=='F01':
            key=(self.laws['module'],'can_read',2);node=self.fns[key][0]
            unify(self.types[key][0][0],RecordType({'tenant':'str','role':'str'},'map',('tenant','role')),node)
            unify(self.types[key][0][1],RecordType({'tenant':'str'},'map',('tenant',)),node)
            unify(self.types[key][1],'bool',node)
        elif 'state_fields' in self.laws:
            fields=RecordType({f: ('bool' if d=='boolean' else 'int' if isinstance(self.laws['domains'].get(d),dict) else 'str') for f,d in self.laws['state_fields'].items()},'map')
            mod=self.laws['module']; node=self.fns[(mod,'step',2)][0]
            unify(self.types[(mod,'step',2)][0][0],fields,node)
            unify(self.types[(mod,'step',2)][0][1],'str',node)
            unify(self.types[(mod,'step',2)][1],fields,node)
            unify(self.types[(mod,'init',0)][1],fields,node)
        # Propagate complete record shapes through every named helper call.
        for _ in range(len(self.fns)+1):
            for key,clauses in self.fns.items():
                self.mod=key[0]
                for fn in clauses:
                    env={};seen=set();ats,rt=self.types[key]
                    for p,t in zip(fn['params'],ats):self.pattern(p,t,env,seen)
                    unify(rt,self.infer(fn['body'],env),fn)
        # Recursion is outside the translation subset, including mutual recursion.
        graph={k:set() for k in self.fns}
        def walk(n,key):
            if isinstance(n,dict):
                if n.get('kind')=='call' and n.get('module')!='Map':
                    self.mod=key[0];graph[key].add(self.fkey(n))
                for v in n.values():walk(v,key)
            elif isinstance(n,list):
                for v in n:walk(v,key)
        for k,fs in self.fns.items():walk(fs,k)
        order=[];active=set();done=set()
        def visit(k):
            if k in active:fail(self.fns[k][0],'recursive call graph')
            if k in done:return
            active.add(k)
            for c in sorted(graph[k]):visit(c)
            active.remove(k);done.add(k);order.append(k)
        for k in graph:visit(k)
        roots=[(self.laws['module'],'can_read',2)] if self.laws['task']=='F01' else [(self.laws['module'],'init',0),(self.laws['module'],'step',2)]
        reachable=set()
        def mark(k):
            if k in reachable:return
            reachable.add(k)
            for child in graph[k]:mark(child)
        for k in roots:mark(k)
        def instantiate(t):
            t=prune(t)
            if isinstance(t,TV):t.ref='str'
            elif isinstance(t,dict):
                for v in t.values():instantiate(v)
            elif isinstance(t,tuple):
                for v in t:instantiate(v)
        # Dead helpers can retain ignored arguments after a valid refactor.
        # Monomorphic atom instantiation does not constrain a checked API path.
        for key in self.fns.keys()-reachable:
            ats,rt=self.types[key]
            for t in ats:instantiate(t)
            instantiate(rt)
        return order
    def pat_bind(self,p,x,bindings):
        k=p['kind']
        if k=='var':bindings[p['name']]=x;return 'true'
        if k=='wildcard':return 'true'
        if k in ('atom','bool','int'):return f'({x} == {self.expr(p,bindings)})'
        if k=='record_pattern':
            checks=[]
            for f in p['fields']:
                fx=f'{x}.{name(f["name"])}'
                ft=prune(self.node_types[id(p)])[f['name']]
                if qtype(ft,p)=='str':checks.append(f'({fx} != "__missing__")')
                checks.append(self.pat_bind(f['value'],fx,bindings))
            return '('+' and '.join(checks)+')' if checks else 'true'
        if k=='tuple_pattern':return '('+' and '.join(self.pat_bind(v,f'{x}._{i+1}',bindings) for i,v in enumerate(p['items']))+')'
        fail(p,'unsupported pattern '+k)
    def expr(self,n,env):
        k=n['kind']
        if k=='var':return env[n['name']]
        if k=='atom':return json.dumps(n['value'])
        if k=='bool':return str(n['value']).lower()
        if k=='int':return str(n['value'])
        if k=='get':
            bt=prune(self.node_types[id(n['base'])])
            if isinstance(bt,RecordType) and n['field'] in bt.optional:fail(n,'optional field access requires Map.get/3')
            return f'({self.expr(n["base"],env)}).{name(n["field"])}'
        if k=='record':
            supplied={f['name'] for f in n['fields']}
            if n.get('struct'):supplied.add('__struct__')
            inferred=set(prune(self.node_types[id(n)]))
            if supplied!=inferred:fail(n,'inconsistent record construction shape')
            values=[f'{name(f["name"])}: {self.expr(f["value"],env)}' for f in n['fields']]
            if n.get('struct'):
                tag=n['struct'] if n['struct'].startswith('Elixir.') else 'Elixir.'+n['struct']
                values.append('__struct__: '+json.dumps(tag))
            return '{ '+', '.join(values)+' }'
        if k=='update':
            base=self.expr(n['base'],env);fs={f['name']:f['value'] for f in n['fields']}
            typ=prune(self.node_types[id(n)])
            return '{ '+', '.join(f'{name(f)}: {self.expr(fs[f],env) if f in fs else "("+base+")."+name(f)}' for f in sorted(typ))+' }'
        if k=='tuple':return '('+', '.join(self.expr(v,env) for v in n['items'])+')'
        if k=='binary':return f'({self.expr(n["left"],env)} {n["op"]} {self.expr(n["right"],env)})'
        if k=='unary':return f'(not({self.expr(n["value"],env)}))'
        if k=='if':return f'(if ({self.expr(n["condition"],env)}) {self.expr(n["then"],env)} else {self.expr(n["else"],env)})'
        if k=='let':
            b=dict(env);condition=self.pat_bind(n['pattern'],self.expr(n['value'],env),b)
            if condition!='true':fail(n,'refutable binding unsupported')
            return self.expr(n['body'],b)
        if k=='case':
            value=self.expr(n['value'],env);out=None
            for branch in reversed(n['branches']):
                b=dict(env);condition=self.pat_bind(branch['pattern'],value,b);body=self.expr(branch['body'],b)
                if out is None:
                    if condition!='true': fail(branch,'case requires final catch-all for totality')
                    out=body
                else:out=f'(if ({condition}) {body} else {out})'
            return out
        if k=='call':
            if n.get('module')=='Map':
                field=name(n['args'][1]['value']);value=f'({self.expr(n["args"][0],env)}).{field}'
                bt=prune(self.node_types[id(n['args'][0])]);ft=bt[n['args'][1]['value']]
                if n['name']=='has_key?':return f'({value} != "__missing__")' if qtype(ft,n)=='str' else 'true'
                if qtype(self.node_types[id(n)],n)!='str':
                    if isinstance(bt,RecordType) and n['args'][1]['value'] not in bt.optional:return value
                    fail(n,'missing fields currently require atom-valued fields')
                return f'(if ({value} == "__missing__") {self.expr(n["args"][2],env)} else {value})'
            return self.fname(self.fkey(n))+('('+', '.join(self.expr(a,env) for a in n['args'])+')' if n['args'] else '')
        fail(n,'unsupported expression '+k)
    def implementation(self):
        order=self.infer_all();lines=['// Generated from current Elixir source. Do not edit.','module app {']
        for key in order:
            self.mod=key[0];clauses=self.fns[key];ats,rt=self.types[key];params=[f'arg{i}' for i in range(len(ats))]
            out=None
            for fn in reversed(clauses):
                env={};conditions=[self.pat_bind(p,a,env) for p,a in zip(fn['params'],params)]
                condition=' and '.join(conditions) or 'true';body=self.expr(fn['body'],env)
                if out is None:
                    if any(c!='true' for c in conditions):fail(fn,'function requires final catch-all for totality')
                    out=body
                else:out=f'(if ({condition}) {body} else {out})'
            loc=clauses[0]['loc'];line=len(lines)+2
            lines.append(f'  // src: {loc["file"]}:{loc["line"]}')
            decl=('def '+self.fname(key)+'('+', '.join(f'{p}: {qtype(t,clauses[0])}' for p,t in zip(params,ats))+')') if params else 'val '+self.fname(key)
            lines.append('  pure '+decl+': '+qtype(rt,clauses[0])+' = '+out)
            self.source_map.append({'definition':self.fname(key),'generated_line':line,'source':loc,'nodes':self.locations(clauses)})
        lines.append('}');return '\n'.join(lines)+'\n'
    def locations(self,n):
        out=[]
        def visit(x):
            if isinstance(x,dict):
                if 'loc' in x:out.append({'kind':x.get('kind'),'loc':x['loc']})
                for k,v in x.items():
                    if k!='loc':visit(v)
            elif isinstance(x,list):
                for v in x:visit(v)
        visit(n);return out

def main():
    p=argparse.ArgumentParser();p.add_argument('ir',type=Path);p.add_argument('laws',type=Path);p.add_argument('out',type=Path);p.add_argument('--freeze-laws',action='store_true');a=p.parse_args()
    try:
        ir=json.loads(a.ir.read_text());laws=json.loads(a.laws.read_text())
        if ir.get('version')!=1:raise TranslationError('FV-QUINT unsupported IR version')
        e=Emitter(ir,laws);app=e.implementation();a.out.mkdir(parents=True,exist_ok=True)
        (a.out/'app.qnt').write_text(app);(a.out/'source-map.json').write_text(json.dumps(e.source_map,indent=2)+'\n')
        if a.freeze_laws:
            from laws import generate_laws
            fixed=generate_laws(laws,e)
            dest=a.out/'laws.qnt'
            if dest.exists() and dest.read_text()!=fixed:raise TranslationError('FV-QUINT refuses to overwrite changed fixed laws')
            dest.write_text(fixed)
        print('FV-QUINT regenerated='+hashlib.sha256(a.ir.read_bytes()+app.encode()).hexdigest())
    except (TranslationError,KeyError,ValueError) as ex:
        print(str(ex));raise SystemExit(2)
if __name__=='__main__':main()
