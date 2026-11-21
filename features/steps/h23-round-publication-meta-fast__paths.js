const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const { Then } = require('@cucumber/cucumber');

const ROOT = path.resolve(__dirname, '..', '..');
const ROUND = 'h23-release-bbf56fdc-vs-891c91b3';
const REQUIRED = ['rounds/STATUS.md', `rounds/${ROUND}/README.md`, `rounds/${ROUND}/recompute.py`];
const OWN = ['.kogen/intents/h23-round-publication-meta-fast/', 'features/steps/h23-round-publication-meta-fast__'];

// The unchanged tree has no row for the round in STATUS.md, no What's missing section in
// its README and no recompute.py, so these markers show that a requested path was changed
// even when the verification checkout has the candidate committed and git status is clean.
const CONTENT_CHANGED = {
  'rounds/STATUS.md': (text) => text.split('\n').some((l) => l.trim().startsWith(ROUND)),
  [`rounds/${ROUND}/README.md`]: (text) => text.split('\n').includes("## What's missing and why"),
  [`rounds/${ROUND}/recompute.py`]: () => true,
};

Then('h23-round-publication-meta-fast: exactly the three requested paths are changed', function () {
  const r = spawnSync('git', ['status', '--porcelain', '--untracked-files=all'], { cwd: ROOT, encoding: 'utf8', timeout: 60000 });
  assert.strictEqual(r.status, 0, `git status failed: ${r.stderr}`);
  const changed = r.stdout.split('\n').filter(Boolean).map((l) => l.slice(3).trim());
  const others = changed.filter((p) => !REQUIRED.includes(p) && !OWN.some((o) => p.startsWith(o)));
  assert.deepStrictEqual(others, [], `paths changed beyond the three requested ones: ${others.join(', ')}`);
  const missing = REQUIRED.filter((p) => {
    if (changed.includes(p)) return false;
    const file = path.join(ROOT, p);
    if (!fs.existsSync(file)) return true;
    return !CONTENT_CHANGED[p](fs.readFileSync(file, 'utf8'));
  });
  assert.deepStrictEqual(missing, [], `requested paths not changed: ${missing.join(', ')}`);
});
