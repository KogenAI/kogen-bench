const assert = require('node:assert');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const { When, Then } = require('@cucumber/cucumber');

const ROOT = path.resolve(__dirname, '..', '..');
const LANES = path.join(ROOT, 'lanes');
const DRIVER = path.join(__dirname, 'bench-leftover-child-test-outlives-group-wait__driver', 'observe.py');
const TEST_ID = 'tests.test_common.Run.test_leftover_child_is_unknown_without_post_reap_signal';
const COMMON_SHA256 = '158b6b58fd960f8cdc4d02ed7bc74fcab000eeac026b9bc0be2e62d29678b39e';
const MEMCAP_SHA256 = '80dd33f33ebef34548b662e7957ab9e2da3d628c14e436fdf1c65fb30b1f2e38';
const OWN_PREFIXES = ['.kogen/', 'features/steps/bench-leftover-child-test-outlives-group-wait__'];

function sha(file) {
  return crypto.createHash('sha256').update(fs.readFileSync(path.join(ROOT, file))).digest('hex');
}

When('bench-leftover-child-test-outlives-group-wait: the method test_leftover_child_is_unknown_without_post_reap_signal is run alone once with python3 -m unittest', function () {
  const r = spawnSync('python3', ['-m', 'unittest', TEST_ID], {
    cwd: LANES, encoding: 'utf8', timeout: 60000, env: { ...process.env, PYTHONDONTWRITEBYTECODE: '1' },
  });
  this.unittest = r;
});
When('bench-leftover-child-test-outlives-group-wait: the same method is run once with a recorder of signals and of the leftover group lifetime', function () {
  const r = spawnSync('python3', ['-I', DRIVER, ROOT], { cwd: ROOT, encoding: 'utf8', timeout: 60000 });
  assert.strictEqual(r.status, 0, `observer exited ${r.status}: ${r.stdout}${r.stderr}`);
  this.rec = JSON.parse(r.stdout.trim().split('\n').pop());
});
When('bench-leftover-child-test-outlives-group-wait: the bytes of common.py and test_memcap.py and the list of changed files are read', function () {
  this.shas = { common: sha('lanes/lanes/common.py'), memcap: sha('lanes/tests/test_memcap.py') };
  const g = spawnSync('git', ['status', '--porcelain', '--untracked-files=all'], { cwd: ROOT, encoding: 'utf8', timeout: 30000 });
  this.changed = g.status === 0
    ? g.stdout.split('\n').filter(Boolean).map((l) => l.slice(3))
      .filter((p) => !p.includes('__pycache__') && !OWN_PREFIXES.some((x) => p.startsWith(x)))
    : null;
});

Then('bench-leftover-child-test-outlives-group-wait: the run reports one test and OK with no skip and no failure', function () {
  const r = this.unittest;
  const out = `${r.stdout}${r.stderr}`;
  assert.strictEqual(r.status, 0, `python3 -m unittest ${TEST_ID} exited ${r.status}: ${out}`);
  assert.ok(/^Ran 1 test in /m.test(out), `expected one test to run: ${out}`);
  assert.ok(/^OK$/m.test(out), `expected a plain OK line, with no skip: ${out}`);
});
Then('bench-leftover-child-test-outlives-group-wait: the test passed and CustodyUnknown was raised while the wait bound was 0.3 seconds', function () {
  assert.strictEqual(this.rec.tests_run, 1, `tests run: ${JSON.stringify(this.rec)}`);
  assert.strictEqual(this.rec.raised, true, `CustodyUnknown was not raised: ${JSON.stringify(this.rec)}`);
  assert.strictEqual(this.rec.bound, 0.3, `wait bound in force was ${this.rec.bound}`);
  assert.strictEqual(this.rec.ok, true, `the test did not pass: ${JSON.stringify(this.rec)}`);
});
Then('bench-leftover-child-test-outlives-group-wait: the group was still alive right after the raise, then disappeared by itself within 6 seconds with no signal sent', function () {
  const { alive_after: alive, gone_after: gone, signals } = this.rec;
  assert.strictEqual(alive, true, `group not alive right after the raise: ${JSON.stringify(this.rec)}`);
  assert.deepStrictEqual(signals, [], `signals sent: ${JSON.stringify(signals)}`);
  assert.ok(gone !== null && gone >= 1 && gone <= 6, `group gone ${gone} seconds after the raise, expected between 1 and 6 (a signalled group goes at once)`);
});
Then('bench-leftover-child-test-outlives-group-wait: common.py and test_memcap.py are byte-identical to the base tree and test_common.py is the only changed file', function () {
  assert.strictEqual(this.shas.common, COMMON_SHA256, 'lanes/lanes/common.py differs from the base tree');
  assert.strictEqual(this.shas.memcap, MEMCAP_SHA256, 'lanes/tests/test_memcap.py differs from the base tree');
  if (this.changed !== null) {
    const extra = this.changed.filter((p) => p !== 'lanes/tests/test_common.py');
    assert.deepStrictEqual(extra, [], `changed files other than test_common.py: ${extra.join(', ')}`);
  }
});
