import pathlib,json,re,datetime
root=pathlib.Path('<ROOT>');receipt=json.loads((root/'run2/hold.json').read_text())
row={'host':receipt['host'],'held':receipt['held'],'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'start_confirmed':False}
if receipt['held'] is False:
 lines=pathlib.Path('<ROOT>').read_text().splitlines()
 releases=[i for i,l in enumerate(lines) if 'RELEASE-FOR-SHAPE1' in l and 'host='+receipt['host'] in l]
 for i in range(releases[-1]+1,len(lines)) if releases else []:
  line=lines[i]
  if not re.search(r'\bSTART\b',line) or 'SHAPE-' in line or 'run_id=s1-' in line:continue
  fields=dict(re.findall(r'\b(utc|host|run_id|task|rep|arm|pair|model|effort)=([^\s]+)',line))
  stamp=re.search(r'\d{4}-\d{2}-\d{2}[T ][0-9:.]+(?:Z|\+00:00)?',line)
  row.update(start_confirmed=True,line_number=i+1,fields=fields,start_utc=stamp.group() if stamp else fields.get('utc'),released_utc=receipt['released_utc'],queue_hash_verified=receipt['released_queue_sha256']==receipt['queue_sha256'] and receipt['queue_unchanged'] is True);break
(root/'run2/resume.json').write_text(json.dumps(row,indent=2)+'\n');print(json.dumps(row))
