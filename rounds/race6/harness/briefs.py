from pathlib import Path
from condition import ARMS,condition,language
SPEC={
'a':'The spec files present are prose CORE, WIRE, OUTCOMES, schemas, and prose design documents.',
'b':'The spec files present are prose CORE, WIRE, OUTCOMES, schemas, prose design documents, and Quint models and their supporting files.',
'c':'The spec files present are prose CORE, WIRE, OUTCOMES, schemas, prose design documents, and Gherkin features including STEPS and FAKES.',
'd':'The spec files present are the complete frozen race 5 spec, including prose, schemas, Quint, Gherkin, and remaining spec artifacts.'}
QUINT='The pinned Quint 0.33.0 TypeScript-backend `quint` CLI is on PATH.'
LANGUAGE={'ex':'Elixir','go':'Go'}
TOOLCHAIN={'ex':'Elixir/OTP and Mix','go':'Go'}
def render(root,arm):
    c=condition(arm);lang=language(arm)
    return (Path(root)/'BRIEF.tmpl').read_text().replace('{SPEC_SENTENCE}',SPEC[c]).replace('{QUINT_LINE}',QUINT if c in 'bd' else '').replace('{LANGUAGE}',LANGUAGE[lang]).replace('{TOOLCHAIN}',TOOLCHAIN[lang])
def check(root):
    root=Path(root);baseline=None
    for arm in ARMS:
        text=(root/f'BRIEF-{arm}.md').read_text();c=condition(arm);lang=language(arm)
        assert text==render(root,arm),f'brief differs: {arm}'
        normalized=text.replace(SPEC[c],'{SPEC_SENTENCE}').replace(QUINT,'').replace(LANGUAGE[lang],'{LANGUAGE}').replace(TOOLCHAIN[lang],'{TOOLCHAIN}')
        # Normalize language/toolchain by rendering the placeholder template, avoiding overlapping Go literals.
        expected=(root/'BRIEF.tmpl').read_text().replace('{SPEC_SENTENCE}',SPEC[c]).replace('{QUINT_LINE}',QUINT if c in 'bd' else '')
        assert text==expected.replace('{LANGUAGE}',LANGUAGE[lang]).replace('{TOOLCHAIN}',TOOLCHAIN[lang])
        print(f'PASS BRIEF-{arm}.md')
    print('PASS brief equality: within language only spec/Quint; across languages only language/toolchain')
