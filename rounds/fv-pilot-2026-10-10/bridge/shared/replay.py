"""Common reporting policy: locations only, one failing evaluation/transition."""
import json

class Replay:
    def __init__(self,ir):
        self.functions={};self.visited=[];self.calls=[];self.module=None
        for mod in ir['modules']:
            for f in mod['functions']:self.functions.setdefault((mod['name'],f['name'],len(f['params'])),[]).append(f)
    def mark(self,n):
        loc=n.get('loc')
        if loc and loc not in self.visited:self.visited.append(loc)
    def bind(self,p,v,env):
        self.mark(p);k=p['kind']
        if k=='var':env[p['name']]=v;return True
        if k=='wildcard':return True
        if k in ('atom','bool','int'):return v==p['value']
        if k=='record_pattern':return isinstance(v,dict) and all(f['name'] in v and v[f['name']]!='__missing__' and self.bind(f['value'],v[f['name']],env) for f in p['fields'])
        if k=='tuple_pattern':return isinstance(v,tuple) and len(v)==len(p['items']) and all(self.bind(p,x,env) for p,x in zip(p['items'],v))
        raise ValueError('unsupported replay pattern')
    def call(self,module,function,args):
        saved=self.module;self.module=module
        for f in self.functions[(module,function,len(args))]:
            env={}
            if all(self.bind(p,v,env) for p,v in zip(f['params'],args)):
                self.mark(f);out=self.eval(f['body'],env);self.module=saved
                self.calls.append((module,function,args,out,f['loc']))
                return out
        raise ValueError('non-total function')
    def eval(self,n,env):
        self.mark(n);k=n['kind']
        if k=='var':return env[n['name']]
        if k in ('atom','bool','int'):return n['value']
        if k=='get':return self.eval(n['base'],env)[n['field']]
        if k in ('record','update'):
            d={} if k=='record' else dict(self.eval(n['base'],env))
            if k=='record' and n.get('struct'):d['__struct__']=n['struct'] if n['struct'].startswith('Elixir.') else 'Elixir.'+n['struct']
            d.update({f['name']:self.eval(f['value'],env) for f in n['fields']});return d
        if k=='tuple':return tuple(self.eval(x,env) for x in n['items'])
        if k=='binary':
            a=self.eval(n['left'],env);op=n['op']
            if op=='and':return a and self.eval(n['right'],env)
            if op=='or':return a or self.eval(n['right'],env)
            b=self.eval(n['right'],env)
            if op=='==':return a==b
            if op=='!=':return a!=b
            if op=='+':return a+b
            if op=='-':return a-b
        if k=='unary':return not self.eval(n['value'],env)
        if k=='if':return self.eval(n['then'] if self.eval(n['condition'],env) else n['else'],env)
        if k=='let':
            b=dict(env)
            if not self.bind(n['pattern'],self.eval(n['value'],env),b):raise ValueError('binding failed')
            return self.eval(n['body'],b)
        if k=='case':
            v=self.eval(n['value'],env)
            for br in n['branches']:
                b=dict(env)
                if self.bind(br['pattern'],v,b):return self.eval(br['body'],b)
            raise ValueError('case failed')
        if k=='call':
            args=[self.eval(x,env) for x in n['args']]
            if n.get('module')=='Map':
                d,field=args[:2]
                present=field in d and d[field]!='__missing__'
                if n['name']=='get':return d[field] if present else args[2]
                if n['name']=='has_key?':return present
            return self.call(n.get('module') or self.module,n['name'],args)
        raise ValueError('unsupported replay expression '+k)

def decode(x):
    if isinstance(x,list):return [decode(v) for v in x]
    if isinstance(x,dict):
        if '#bigint' in x:return int(x['#bigint'])
        if '#tup' in x:return tuple(decode(v) for v in x['#tup'])
        return {k:decode(v) for k,v in x.items() if k!='#meta'}
    return x

def report(ir, laws, law, args, expected=None):
    replay=Replay(ir)
    actual=replay.call(laws['module'], 'can_read' if laws['task']=='F01' else 'step', args)
    if expected is not None and actual!=expected: raise ValueError('IR replay disagrees with native counterexample')
    locations=sorted({(x['file'],x['line'],x['column']) for x in replay.visited})
    for file,line,column in locations: print(f'FV-TRACE-SOURCE {law} {file}:{line}:{column}')
    return locations

def map_trace(path,ir,laws,law):
    states=decode(json.loads(path.read_text()).get('states',[]))
    usable=states if laws['task']=='F01' else [s for s in states if s.get('depth',0)>0]
    if not usable: raise ValueError('missing native failing evaluation/transition')
    state=usable[-1]
    args=[state['actor'],state['resource']] if laws['task']=='F01' else [state['before'],state['event']]
    report(ir,laws,law,args,state['result'] if laws['task']=='F01' else state['state'])
