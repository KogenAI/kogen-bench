"""ARCH constants; production clocks cannot be overridden by environment."""
from pathlib import Path
import hashlib
import json
import os
import tempfile

STUDIO_WAVES = {
    'A': ('arch-e1', 'arch-e2', 'arch-g1', 'arch-g2'),
    'B': ('arch-e3', 'arch-e4', 'arch-g3', 'arch-g4'),
}
STUDIO_ARMS = tuple(arm for wave in STUDIO_WAVES.values() for arm in wave)
MACBOOK_ARMS = ('arch-e5', 'arch-e6', 'arch-g5', 'arch-g6')
ARMS = STUDIO_ARMS + MACBOOK_ARMS
PAIRS = (('arch-e1', 'arch-g1'), ('arch-e2', 'arch-g2'),
         ('arch-e3', 'arch-g3'), ('arch-e4', 'arch-g4'),
         ('arch-e5', 'arch-g5'), ('arch-e6', 'arch-g6'))
MODEL, EFFORT = 'gpt-6.1-sol', 'high'
PHASE_SECONDS = {'build': 5400, 'maintenance': 1800}
CORES = {'macbook': 3.0, 'studio': 2.5}
CONSTRAINTS = {
    'E': 'The core (coordinator plus worker logic) must be Elixir/OTP; the kogen CLI must be a Go binary speaking the JSON-lines TCP protocol specified in PROTOCOL.md.',
    'G': 'Everything must be implemented in Go.',
}
CONTINUATION = 'Continue implementing and checking the frozen task brief in this workspace until the original phase deadline. Fix remaining failures and verify your work with your own tests.'
CACHE_EXCLUDES = {'.kitcache', '.kit-tools', '.cache', '__pycache__'}
SOURCE_ONLY_EXCLUDES = CACHE_EXCLUDES | {'deps', '_build', 'vendor', 'generated', 'node_modules', 'target'}
SNAPSHOT_EXCLUDES = {'.git'} | CACHE_EXCLUDES
LOC_EXCLUDES = SOURCE_ONLY_EXCLUDES | {'spec', 'docs'}
TOKEN_KEYS = ('input_tokens', 'cached_input_tokens', 'output_tokens', 'reasoning_output_tokens', 'total_tokens')

def treatment(arm):
    if arm not in ARMS:
        raise ValueError('Unknown ARCH arm: ' + arm)
    return 'E' if arm.startswith('arch-e') else 'G'

def arms_for_host(host):
    if host == 'studio': return STUDIO_ARMS
    if host == 'macbook': return MACBOOK_ARMS
    raise ValueError('Unknown ARCH host: ' + host)

def wave_for_arm(arm):
    for label, arms in STUDIO_WAVES.items():
        if arm in arms: return label
    if arm in MACBOOK_ARMS: return 'optional'
    raise ValueError('Unknown ARCH arm: ' + arm)

def pair_for_arm(arm):
    for e_arm, g_arm in PAIRS:
        if arm == e_arm: return e_arm.replace('arch-e', 'pair-')
        if arm == g_arm: return e_arm.replace('arch-e', 'pair-')
    raise ValueError('Unknown ARCH arm: ' + arm)

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def dump(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.arch-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as stream:
            json.dump(value, stream, indent=2, sort_keys=True)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)

def load(root):
    return json.loads((Path(root) / 'ARCH-CONFIG.json').read_text())

def render(template, arm):
    if template.count('{CONSTRAINT}') != 1:
        raise ValueError('Brief template must contain exactly one constraint slot')
    return template.replace('{CONSTRAINT}', CONSTRAINTS[treatment(arm)])
