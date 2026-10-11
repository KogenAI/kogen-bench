"""Access-aware hidden-suite audit: targets/provenance, never a generic basename."""
import ast,json,os,re,shlex
from pathlib import Path
from command_policy import executable_text,executed_requests,KOGEN
READERS={'cat','head','tail','less','more','ls','find','rg','grep','stat','du','cp','sed','awk','source','.','readlink','realpath'}
READ_CALL=re.compile(r'(?:^|\.)(?:open|read_text|read_bytes|readFile|readFileSync|listdir|scandir|walk|glob|rglob|load|loads|import_module)$')
def _python_targets(script):
    try:tree=ast.parse(script)
    except SyntaxError:return []
    bindings={}
    for n in ast.walk(tree):
        if isinstance(n,ast.Assign) and isinstance(n.value,ast.Constant) and isinstance(n.value.value,str):
            bindings.update({t.id:n.value.value for t in n.targets if isinstance(t,ast.Name)})
    result=[]
    for n in ast.walk(tree):
        if not isinstance(n,ast.Call):continue
        name=ast.unparse(n.func)
        if not READ_CALL.search(name):continue
        if name.endswith('open'):
            modes=[v.value for v in n.args[1:2] if isinstance(v,ast.Constant)]+[v.value.value for v in n.keywords if v.arg=='mode' and isinstance(v.value,ast.Constant)]
            if modes and any(char in str(modes[0]) for char in 'wax') and '+' not in str(modes[0]):continue
        for node in [*n.args,n.func]:
            for v in ast.walk(node):
                if isinstance(v,ast.Constant) and isinstance(v.value,str):result.append(v.value)
                elif isinstance(v,ast.Name) and v.id in bindings:result.append(bindings[v.id])
    return result
def access_targets(command,cwd=None):
    text=executable_text(command);targets=[]
    bindings=dict(re.findall(r'(?:^|[;\n])\s*(?:export\s+)?(\w+)=[\"\']?([^\s;\"\']+)',text))
    for key,value in bindings.items():text=text.replace('${'+key+'}',value).replace('$'+key,value)
    # Executed interpreter heredocs retain their code; data heredoc bodies are stripped.
    h=re.search(r"python[0-9.]*\s+-?\s*<<\s*['\"]?(\w+)['\"]?[^\n]*\n(.*?)\n\1",text,re.S)
    if h:targets+=_python_targets(h[2]);text=text[:h.start()]+text[h.end():]
    try:
        lexer=shlex.shlex(text,posix=True,punctuation_chars=';&|\n');lexer.whitespace=' \t\r';lexer.whitespace_split=True;lexer.commenters='#'
        segments=[];current=[]
        for word in lexer:
            if word and all(c in ';&|\n' for c in word):
                if current:segments.append(current);current=[]
            else:current.append(word)
        if current:segments.append(current)
    except ValueError:return targets
    for words in segments:
        while words and (words[0] in ('env','command','sudo','exec') or re.fullmatch(r'\w+=.*',words[0])):words=words[1:]
        if not words:continue
        if words[0]=='cd' and len(words)>1:
            target=Path(os.path.expanduser(words[1]));cwd=target if target.is_absolute() else (Path(cwd)/target if cwd else target)
            targets.append(str(cwd));continue
        program=Path(words[0]).name
        for sub in re.findall(r'\$\((.*?)\)|`(.*?)`',' '.join(words),re.S):targets+=access_targets(next(s for s in sub if s))
        if program in ('sh','bash','zsh') and '-c' in words and words.index('-c')+1<len(words):targets+=access_targets(words[words.index('-c')+1]);continue
        if re.fullmatch('python[0-9.]*',program) and '-c' in words and words.index('-c')+1<len(words):targets+=_python_targets(words[words.index('-c')+1]);continue
        if program in ('node','bun','deno') and any(w in ('-e','--eval') for w in words):
            script=words[-1]
            # Only executed reader argument literals; source write payloads are not targets.
            targets+=re.findall(r'(?:readFileSync|readFile|readdirSync|require|import)\s*\(\s*[\"\']([^\"\']+)',script);continue
        if program in ('echo','printf','tee','touch','mkdir'):continue
        if program in READERS:
            # A pure cat data heredoc writes source; no input artifact is accessed.
            if program=='cat' and any('<<' in w for w in words):continue
            args=[w for w in words[1:] if not w.startswith('-') and w not in ('>','>>','<')]
            if program in ('rg','grep'):args=args[1:] or ([str(cwd)] if cwd else ['.'])  # First positional is a pattern, not an access target.
            targets += args
        elif '/' in words[0]:targets.append(words[0])
        if program not in READERS and program not in ('echo','printf','tee'):
            # Explicit executable/import/script paths are accesses too.
            targets += [w for w in words[1:] if w.startswith(('/','../','./','$HOME/')) and '://' not in w]
    targets=[os.path.expanduser(t.replace('${HOME}',str(Path.home())).replace('$HOME',str(Path.home()))) for t in targets]
    if cwd is not None:
        targets=[str(Path(cwd)/t) if not Path(t).is_absolute() and '://' not in t else t for t in targets]
    return targets

def inventory(root):
    root=Path(root);data=json.loads((root/'hidden-inventory.json').read_text()) if (root/'hidden-inventory.json').exists() else {'locks':[]}
    local=root/'out/host-inventory/hidden-inventory.json'
    if local.exists():
        extra=json.loads(local.read_text());data=dict(data,locks=data['locks']+extra['locks'])
    source=Path(data.get('source_root',str(root)));locked=set(data['locks'])
    locked.update(str(root/Path(p).relative_to(source)) for p in data['locks'] if source in Path(p).parents)
    if (root/'locks.tsv').exists():locked.update(line.split('\t',1)[1] for line in (root/'locks.tsv').read_text().splitlines())
    return locked

def hidden_suite_targets(command,root,arm):
    root=Path(root);base=root/arm;locked=inventory(root);found=[]
    for raw in access_targets(command,base):
        raw=raw.replace('${HOME}',str(Path.home())).replace('$HOME',str(Path.home()))
        if '://' in raw:continue
        path=Path(os.path.expanduser(raw))
        if not path.is_absolute():path=base/path
        try:path=path.resolve(strict=False)
        except (OSError,RuntimeError):path=Path(os.path.normpath(path))
        recursive=bool(re.search(r'\b(?:find|rg|grep|cp)\b',command))
        if any(path==Path(p) or Path(p) in path.parents or (recursive and path in Path(p).parents) for p in locked):found.append(str(path))
    return sorted(set(found))
def hidden_suite_access(command,root,arm):return bool(hidden_suite_targets(command,root,arm))
def patterns(root):
    p=Path(root)/'network-patterns.json'
    return json.loads(p.read_text()) if p.exists() else {'case_prefixes':[]}
def prohibited_resource(value,root):
    return bool(KOGEN.search(value) or re.search(r'kogen-bench|kogen-conformance',value,re.I) or any(prefix.lower() in value.lower() for prefix in patterns(root)['case_prefixes']))
def prohibited_network_access(command,root):
    targets=list(executed_requests(command))
    text=executable_text(command)
    try:
        words=shlex.split(text)
        if words and Path(words[0]).name in ('sh','bash','zsh') and '-c' in words:targets+=prohibited_network_access(words[words.index('-c')+1],root)
    except (ValueError,IndexError):pass
    for segment in re.split(r'[;\n]|&&|\|\|',text):
        try:words=shlex.split(segment,comments=True)
        except ValueError:continue
        if not words:continue
        program=Path(words[0]).name
        network=program in ('curl','wget') or (program=='git' and len(words)>1 and words[1] in ('clone','fetch','pull','ls-remote')) or (program in ('npm','bun','pip') and len(words)>1 and words[1] in ('add','install','ci','fetch','download'))
        if network:targets += [word for word in words[1:] if word.startswith(('https://','http://'))]
    return [value for value in targets if prohibited_resource(value,root)]
def web_targets(value):
    result=[]
    if isinstance(value,dict):
        for key,item in value.items():
            if key in ('url','href','query','q','queries','search_query'):
                if isinstance(item,str):result.append(item)
                elif isinstance(item,list):result += [v for v in item if isinstance(v,str)];result+=web_targets(item)
                else:result+=web_targets(item)
            elif key=='arguments' and isinstance(item,str):
                try:result+=web_targets(json.loads(item))
                except ValueError:pass
            else:result+=web_targets(item)
    elif isinstance(value,list):
        for item in value:
            if isinstance(item,str) and item.startswith(('https://','http://')):result.append(item)
            else:result+=web_targets(item)
    return result
