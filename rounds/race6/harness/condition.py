"""Separate language kit identity from specification condition."""
CONDITIONS=('a','b','c','d')
LANGUAGES=('ex','go')
ARMS=tuple(lang+'-'+cond for lang in LANGUAGES for cond in CONDITIONS)
def condition(arm):
    value=arm.rsplit('-',1)[-1]
    if value not in CONDITIONS:raise ValueError('unknown condition: '+arm)
    return value
def language(arm):
    if arm in CONDITIONS:return 'ex' # synthetic compatibility fixtures only
    if arm not in ARMS:raise ValueError('unknown arm: '+arm)
    return arm.split('-',1)[0]
