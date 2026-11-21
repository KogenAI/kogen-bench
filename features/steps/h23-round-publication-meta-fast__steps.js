const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const { Given, Then } = require('@cucumber/cucumber');

const ROOT = path.resolve(__dirname, '..', '..');
const SLUG = 'h23-round-publication-meta-fast';
const ROUND = 'h23-release-bbf56fdc-vs-891c91b3';
const ROUND_DIR = path.join(ROOT, 'rounds', ROUND);
const CODES = 'DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE';

function run(cmd, args, cwd) {
  const r = spawnSync(cmd, args, { cwd, encoding: 'utf8', timeout: 60000 });
  const out = (r.stdout || '') + (r.stderr || '');
  return { status: r.status, out, error: r.error };
}

Given('h23-round-publication-meta-fast: the repository working tree', function () {
  assert.ok(fs.existsSync(path.join(ROOT, 'rounds', 'STATUS.md')), 'rounds/STATUS.md is missing');
  assert.ok(fs.existsSync(path.join(ROUND_DIR, 'README.md')), `rounds/${ROUND}/README.md is missing`);
});

Then('h23-round-publication-meta-fast: STATUS.md has one DESCRIPTIVE row with the three reason codes and the README has the metadata lines and sections', function () {
  const status = fs.readFileSync(path.join(ROOT, 'rounds', 'STATUS.md'), 'utf8').split('\n');
  const rows = status.filter((l) => l.trim().startsWith(ROUND));
  assert.strictEqual(rows.length, 1, `rounds/STATUS.md must have exactly one row for ${ROUND}, found ${rows.length}`);
  const parts = rows[0].split('|').map((p) => p.trim());
  assert.strictEqual(parts.length, 3, `the row must have three columns: ${rows[0]}`);
  assert.strictEqual(parts[0], ROUND, 'first column must be the round id');
  assert.strictEqual(parts[1], 'DESCRIPTIVE', `second column must be DESCRIPTIVE, got ${parts[1]}`);
  assert.ok(parts[2].startsWith(CODES + ' — '), `third column must start with "${CODES} — ": ${parts[2]}`);
  assert.ok(parts[2].slice((CODES + ' — ').length).trim().length > 0, 'the row must give a reason sentence');

  const lines = fs.readFileSync(path.join(ROUND_DIR, 'README.md'), 'utf8').split('\n');
  const exact = (field, value) => {
    const found = lines.filter((l) => l.startsWith(field + ':'));
    assert.deepStrictEqual(found, [`${field}: ${value}`], `README must have exactly one ${field} line equal to "${field}: ${value}", found ${JSON.stringify(found)}`);
  };
  exact('Round date', '2026-11-16');
  exact('Label', 'DESCRIPTIVE');
  exact('Publication badge', 'DESCRIPTIVE; KEPT FOR AUDIT');
  exact('Recomputation status', 'OBSERVED SOURCE ONLY');
  const why = lines.filter((l) => l.startsWith('Why not VALID:'));
  assert.strictEqual(why.length, 1, `README must have one Why not VALID line, found ${why.length}`);
  for (const code of CODES.split(', ')) assert.ok(why[0].includes(code), `Why not VALID line must name ${code}: ${why[0]}`);
  for (const heading of ['## Metadata', '## Execution record', "## What's missing and why"]) {
    assert.ok(lines.includes(heading), `README must contain the section ${heading}`);
  }
});

const SINGLE_ROUND_PY = `
import sys, shutil, tempfile
from pathlib import Path
root = Path.cwd()
sys.path.insert(0, str(root / 'reproduce'))
import validate_release as vr
from validate_round import records, validate
rid = sys.argv[1]
src = root / 'rounds' / rid
with tempfile.TemporaryDirectory() as t:
    tmp = Path(t)
    (tmp / 'rounds' / rid).mkdir(parents=True)
    for name in ('README.md', 'MISSING-DECLARED.json'):
        shutil.copy(src / name, tmp / 'rounds' / rid / name)
    rows = []
    for line in (root / 'rounds' / 'STATUS.md').read_text(encoding='utf-8').splitlines():
        m = vr.STATUS_RE.match(line)
        if m and m.group(1).strip() == rid:
            rows.append(line)
    (tmp / 'rounds' / 'STATUS.md').write_text('# Status\\n\\n' + '\\n'.join(rows) + '\\n', encoding='utf-8')
    errors, historical = vr.validate_historical_inventory(tmp)
    statuses = vr.status_rows(tmp)
    if rid in statuses:
        status_errors, status = vr.resolve_status(rid, statuses[rid][0], tmp)
        report = validate(rid, records(), strict=True)
        if report['errors']:
            errors.append(rid + ' strict record validation failed: ' + '; '.join(report['errors'][:5]))
        declaration_errors, _count = vr.declared_missing_errors(rid, status, report, tmp)
        errors.extend(declaration_errors)
    for error in errors:
        print('- ' + error)
    print('CHECKED ' + rid)
`;

Then('h23-round-publication-meta-fast: the release validator reports no failure line for the round', function () {
  const r = run('python3', ['-I', '-c', SINGLE_ROUND_PY, ROUND], ROOT);
  assert.strictEqual(r.status, 0, `the single round check crashed (exit ${r.status}): ${r.out}`);
  assert.ok(r.out.includes('CHECKED ' + ROUND), `the single round check did not finish: ${r.out}`);
  const failures = r.out.split('\n').filter((l) => l.startsWith('- ' + ROUND));
  assert.deepStrictEqual(failures, [], `the validator reports failure lines for ${ROUND}:\n${failures.join('\n')}`);
});

Then('h23-round-publication-meta-fast: the historical round metadata test passes alone and the release test files are unchanged', function () {
  const name = 'test_validate_release.ReleasePolicyTest.test_every_historical_round_has_publication_metadata';
  const r = run('python3', ['-m', 'unittest', name], path.join(ROOT, 'reproduce'));
  assert.strictEqual(r.status, 0, `python3 -m unittest ${name} failed (exit ${r.status}): ${r.out}`);
  assert.ok(/Ran 1 test/.test(r.out) && /\nOK\s*$/.test(r.out), `${name} did not run once and pass: ${r.out}`);
  const diff = run('git', ['diff', '--quiet', 'HEAD', '--', 'reproduce/test_validate_release.py', 'reproduce/validate_release.py'], ROOT);
  assert.strictEqual(diff.status, 0, 'reproduce/test_validate_release.py or reproduce/validate_release.py differs from HEAD');
  const text = fs.readFileSync(path.join(ROOT, 'reproduce', 'test_validate_release.py'), 'utf8');
  assert.ok(text.includes('self.assertEqual(len(historical), 179)'), 'the expected count of 179 is not in the test file');
});

Then('h23-round-publication-meta-fast: recompute.py has the exact retained bytes and prints the expected task means', function () {
  const file = path.join(ROUND_DIR, 'recompute.py');
  assert.ok(fs.existsSync(file), `rounds/${ROUND}/recompute.py does not exist`);
  const want = fs.readFileSync(path.join(ROOT, '.kogen', 'intents', SLUG, 'fixtures', 'recompute.py'));
  assert.ok(fs.readFileSync(file).equals(want), 'recompute.py bytes differ from the SOURCE FILE');
  const r = spawnSync('python3', ['recompute.py'], { cwd: ROUND_DIR, encoding: 'utf8', timeout: 60000 });
  assert.strictEqual(r.status, 0, `python3 recompute.py exited ${r.status}: ${(r.stdout || '') + (r.stderr || '')}`);
  const printed = JSON.parse(r.stdout);
  const cells = JSON.parse(fs.readFileSync(path.join(ROUND_DIR, 'cells.json'), 'utf8'));
  assert.strictEqual(cells.original_decision, 'rejected', 'cells.json original_decision is not rejected');
  assert.strictEqual(printed.original_decision, 'rejected', 'printed original_decision is not rejected');
  assert.strictEqual(printed.causal_comparison, false, 'printed causal_comparison is not false');
  assert.deepStrictEqual(Object.keys(printed.task_means).sort(), Object.keys(cells.expected_task_means).sort(), 'printed arms differ from cells.json');
  for (const [arm, tasks] of Object.entries(cells.expected_task_means)) {
    assert.deepStrictEqual(Object.keys(printed.task_means[arm]).sort(), Object.keys(tasks).sort(), `printed tasks differ for ${arm}`);
    for (const [task, value] of Object.entries(tasks)) {
      assert.ok(Math.abs(printed.task_means[arm][task] - value) <= 1e-9, `${arm} ${task}: printed ${printed.task_means[arm][task]}, expected ${value}`);
    }
  }
});
