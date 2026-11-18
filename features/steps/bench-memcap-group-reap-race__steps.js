const assert = require('node:assert');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const { When, Then } = require('@cucumber/cucumber');

const ROOT = path.resolve(__dirname, '..', '..');
const DRIVER = path.join(__dirname, 'bench-memcap-group-reap-race__driver', 'probe.py');
const MEMCAP_SHA256 = '80dd33f33ebef34548b662e7957ab9e2da3d628c14e436fdf1c65fb30b1f2e38';

function drive(world, mode) {
  const r = spawnSync('python3', ['-I', DRIVER, mode], { cwd: ROOT, encoding: 'utf8', timeout: 60000 });
  assert.strictEqual(r.status, 0, `driver ${mode} exited ${r.status}: ${r.stdout}${r.stderr}`);
  world.group = JSON.parse(r.stdout.trim().split('\n').pop());
}

When('bench-memcap-group-reap-race: the leader of a process group is reaped and the last other member exits 0.5 seconds later', function () {
  drive(this, 'delayed');
});
When('bench-memcap-group-reap-race: a member of the process group is still alive after the wait bound, shortened to 0.3 seconds', function () {
  drive(this, 'outlives');
});
When('bench-memcap-group-reap-race: the group probe raises PermissionError with the default wait bound', function () {
  drive(this, 'permission');
});
When('bench-memcap-group-reap-race: the group is checked while its last member exits 0.5 seconds after the leader and signals are recorded', function () {
  drive(this, 'delayed');
});
When('bench-memcap-group-reap-race: the memcap test file is read', function () {
  this.memcap = fs.readFileSync(path.join(ROOT, 'lanes', 'tests', 'test_memcap.py'));
});

Then('bench-memcap-group-reap-race: the group check returns without raising CustodyUnknown', function () {
  assert.strictEqual(this.group.raised, null, `_require_group_gone raised ${this.group.raised} after ${this.group.elapsed}s`);
});
Then('bench-memcap-group-reap-race: the group check raises CustodyUnknown', function () {
  assert.strictEqual(this.group.raised, 'CustodyUnknown', `_require_group_gone raised ${this.group.raised} (expected CustodyUnknown) after ${this.group.elapsed}s`);
});
Then('bench-memcap-group-reap-race: the group check took at least {float} seconds', function (min) {
  assert.ok(this.group.elapsed >= min, `_require_group_gone took ${this.group.elapsed}s, expected at least ${min}s`);
});
Then('bench-memcap-group-reap-race: the group check took less than {int} second', function (max) {
  assert.ok(this.group.elapsed < max, `_require_group_gone took ${this.group.elapsed}s, expected under ${max}s`);
});
Then('bench-memcap-group-reap-race: no signal other than the zero probe was sent to the group', function () {
  assert.deepStrictEqual(this.group.signals, [], `signals sent to the group: ${JSON.stringify(this.group.signals)}`);
  assert.strictEqual(this.group.raised, null, `_require_group_gone raised ${this.group.raised}`);
});
Then('bench-memcap-group-reap-race: the memcap test file is byte-identical to its content on main and keeps both branches', function () {
  const sha = crypto.createHash('sha256').update(this.memcap).digest('hex');
  assert.strictEqual(sha, MEMCAP_SHA256, 'lanes/tests/test_memcap.py differs from main');
  const text = this.memcap.toString('utf8');
  assert.ok(text.includes('def test_watchdog') && text.includes('def test_cgroup'), 'a branch is missing');
});
