"""One mode policy for preparation, briefs, gates and the event audit."""
from pathlib import Path

MODES = ('sealed', 'real-workflow')
DENYLIST_RULE = 'Do not access any existing Kogen repository, kogen.dev or bench.kogen.dev.'
POLICY = {
    'sealed': ('SEALED: work offline using only the supplied kit libraries and local documentation. '
               'Do not download or install packages, fetch remote repositories, access the web, '
               'or use web search. Never call real model providers; the suite uses a local fake.'),
    'real-workflow': ('REAL-WORKFLOW: you may install packages with your ecosystem\'s package manager, '
                      'read documentation on the web, and use live Codex web search as a developer '
                      'normally would. Never call real model providers; the suite uses a local fake.'),
}


def read_mode(root):
    try:
        mode = (Path(root) / 'MODE').read_text().strip()
    except OSError as error:
        raise ValueError('MODE file is required') from error
    if mode not in MODES:
        raise ValueError('MODE must be sealed or real-workflow')
    return mode


def render_policy(text, mode):
    if mode not in MODES:
        raise ValueError('invalid MODE')
    return text.replace('{MODE}', mode).replace('{MODE_POLICY}', POLICY[mode])


def brief_template(root):
    root = Path(root)
    return render_policy((root / 'BRIEF.tmpl').read_text(), read_mode(root))
