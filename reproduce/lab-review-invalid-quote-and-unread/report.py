import json
from pathlib import Path
x = json.loads(Path(__file__).with_name('quotation.json').read_text())
def identity(s):
    return ' '.join(s.split()).lower()
def normal(s):
    return s.replace('\\"', '"')
a, b = x['requirement'], x['finding_message']
print('baseline quoted:', identity(a) in identity(b))
print('normalized quoted:', identity(normal(a)) in identity(normal(b)))
