const assert = require('node:assert');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const { Given, Then } = require('@cucumber/cucumber');

const ROOT = path.resolve(__dirname, '..', '..');
const SLUG = 'h23-round-page-and-register-index';
const FIXTURES = path.join(ROOT, '.kogen', 'intents', SLUG, 'fixtures');
const ROUND_ID = 'h23-release-bbf56fdc-vs-891c91b3';

function sha256(text) {
  return crypto.createHash('sha256').update(text).digest('hex');
}

function stable(value) {
  if (Array.isArray(value)) return '[' + value.map(stable).join(',') + ']';
  if (value && typeof value === 'object') {
    return '{' + Object.keys(value).sort().map((k) => JSON.stringify(k) + ':' + stable(value[k])).join(',') + '}';
  }
  return JSON.stringify(value);
}

function stripOneNewline(text) {
  return text.endsWith('\n') ? text.slice(0, -1) : text;
}

function readJson(rel) {
  const file = path.join(ROOT, rel);
  assert.ok(fs.existsSync(file), `${rel} is missing`);
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (e) {
    assert.fail(`${rel} does not parse as JSON: ${e.message}`);
  }
}

function listFiles(dir, prefix) {
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const rel = prefix ? `${prefix}/${entry.name}` : entry.name;
    if (entry.isDirectory()) out.push(...listFiles(path.join(dir, entry.name), rel));
    else out.push(rel);
  }
  return out.sort();
}

Given('h23-round-page-and-register-index: the repository working tree', function () {
  assert.ok(fs.existsSync(path.join(ROOT, 'rounds', 'index.json')), 'rounds/index.json is missing from the working tree');
  assert.ok(fs.existsSync(FIXTURES), 'the recorded fixtures are missing');
  this.expected = JSON.parse(fs.readFileSync(path.join(FIXTURES, 'expected.json'), 'utf8'));
});

Then('h23-round-page-and-register-index: the round page equals the retained page and the round directory holds only the allowed files', function () {
  const dir = path.join(ROOT, 'rounds', ROUND_ID);
  assert.ok(fs.existsSync(dir), `rounds/${ROUND_ID} does not exist`);
  const files = listFiles(dir, '');
  const allowed = [['README.md'], ['README.md', 'cells.json']];
  assert.ok(
    allowed.some((a) => JSON.stringify(a) === JSON.stringify(files)),
    `rounds/${ROUND_ID} holds ${JSON.stringify(files)}; expected README.md alone or README.md and cells.json`
  );
  const actual = stripOneNewline(fs.readFileSync(path.join(dir, 'README.md'), 'utf8'));
  const expected = stripOneNewline(fs.readFileSync(path.join(FIXTURES, 'page.md'), 'utf8'));
  assert.ok(actual === expected, `rounds/${ROUND_ID}/README.md differs from the retained page (actual ${actual.length} characters, expected ${expected.length})`);
});

Then('h23-round-page-and-register-index: the round register is the earlier register, one blank line and the retained bullet line', function () {
  const body = stripOneNewline(fs.readFileSync(path.join(ROOT, 'rounds', 'README.md'), 'utf8'));
  const bullet = this.expected.bullet;
  const tail = '\n' + bullet;
  assert.ok(body.endsWith(tail), 'rounds/README.md does not end with a line break followed by the retained bullet line as its last line');
  const earlier = body.slice(0, body.length - tail.length);
  assert.strictEqual(
    sha256(earlier),
    this.expected.registerBeforeSha256,
    'the text before the bullet line and its separating blank line differs from the earlier rounds/README.md'
  );
});

Then('h23-round-page-and-register-index: the index and the inventory each keep the earlier entries in order and gain exactly one new last entry for the round', function () {
  const ids = readJson('rounds/index.json');
  assert.ok(Array.isArray(ids), 'rounds/index.json is not a list');
  const wantCount = this.expected.indexBefore.count + 1;
  assert.strictEqual(ids.length, wantCount, `rounds/index.json holds ${ids.length} entries; expected the ${this.expected.indexBefore.count} earlier entries plus exactly one new entry`);
  assert.strictEqual(ids[ids.length - 1], ROUND_ID, `the last entry of rounds/index.json is ${JSON.stringify(ids[ids.length - 1])}; expected ${ROUND_ID}`);
  assert.strictEqual(sha256(stable(ids.slice(0, -1))), this.expected.indexBefore.sha256, 'the earlier entries of rounds/index.json differ from the recorded ones or are reordered');

  const inventory = readJson('reproduce/round-inventory.json');
  const rounds = inventory.rounds;
  assert.ok(Array.isArray(rounds), 'reproduce/round-inventory.json has no rounds list');
  const before = this.expected.inventoryBefore;
  assert.strictEqual(rounds.length, before.count + 1, `the inventory holds ${rounds.length} entries; expected ${before.count} earlier entries plus exactly one more`);
  assert.strictEqual(sha256(stable(rounds.slice(0, -1))), before.sha256, 'the earlier inventory entries differ from the recorded ones or are reordered');
  assert.strictEqual(stable(rounds[rounds.length - 1]), stable(this.expected.inventoryEntry), 'the last inventory entry is not the retained inventory entry');
});
