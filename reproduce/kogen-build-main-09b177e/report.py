#!/usr/bin/env python3
import json,sys
from pathlib import Path
d=json.loads(Path(sys.argv[1]).read_text());m=d['metadata'];rows=d['rows'];seen=[r['candidate'] for r in rows if r['candidate'] is not None]
print('Verdict:',m['verdict'],'('+m['status']+')')
print('Observed:',len(seen),'of',len(rows),'assigned; not run:',len(rows)-len(seen))
print('Valid Intent:',sum(c['valid_intent'] for c in seen),'of',len(seen))
print('Landed:',sum(c['landed'] for c in seen),'of',len(seen))
print('Hidden all-pass:',sum(c['hidden_pass'] is True for c in seen),'of',len(seen),'observed;',sum(c['grade_complete'] is True for c in seen),'complete grades')
print('Reviews:',sum(c['review_count'] for c in seen))
print('Model input tokens:',sum(c['tokens']['input_tokens'] or 0 for c in seen))
print('Cached input tokens:',sum(c['tokens']['cached_input_tokens'] or 0 for c in seen))
print('Model output tokens:',sum(c['tokens']['output_tokens'] or 0 for c in seen))
print('Reasoning tokens (subset of output):',sum(c['tokens']['reasoning_tokens'] or 0 for c in seen))
print('Sum of cell wall seconds (includes failed attempts):',format(sum(c['wall_s'] for c in seen),'.3f'))
print('Edit-to-feedback: unavailable (shell arguments hashed)')
print('Finish-to-feedback seconds:',', '.join(format(v,'.3f') for c in seen for v in c['finish_to_feedback_s']))
print('Dollars: unpriced')
print('Stored hidden grades:',sum((r['stored'] or {}).get('graded',0) for r in rows),'of',sum((r['stored'] or {}).get('n',0) for r in rows),'stored cells; missing grades remain unknown')
