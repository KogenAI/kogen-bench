const assert = require('node:assert');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const { Given, Then } = require('@cucumber/cucumber');

const ROOT = path.resolve(__dirname, '..', '..');
const SLUG = 'h23-round-cells-json-data';
const FIXTURES = path.join(ROOT, '.kogen', 'intents', SLUG, 'fixtures');
const ROUND_ID = 'h23-release-bbf56fdc-vs-891c91b3';
const ROUND_DIR = `rounds/${ROUND_ID}`;

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

function listFiles(dir, prefix) {
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const rel = prefix ? `${prefix}/${entry.name}` : entry.name;
    if (entry.isDirectory()) out.push(...listFiles(path.join(dir, entry.name), rel));
    else out.push(rel);
  }
  return out.sort();
}

Given('h23-round-cells-json-data: the repository working tree', function () {
  assert.ok(fs.existsSync(path.join(ROOT, 'reproduce', 'round-inventory.json')), 'reproduce/round-inventory.json is missing from the working tree');
  assert.ok(fs.existsSync(FIXTURES), 'the recorded fixtures are missing');
  this.expected = JSON.parse(fs.readFileSync(path.join(FIXTURES, 'expected.json'), 'utf8'));
  this.sourceText = fs.readFileSync(path.join(FIXTURES, 'source-cells.json'), 'utf8');
});

Then('h23-round-cells-json-data: the round directory holds only the allowed files and cells.json is the source data with its 18 slots', function () {
  const dir = path.join(ROOT, ROUND_DIR);
  assert.ok(fs.existsSync(dir), `${ROUND_DIR} does not exist`);
  const files = listFiles(dir, '');
  const optional = ['manifest.json', 'recompute.py'];
  const unexpected = files.filter((f) => f !== 'README.md' && f !== 'cells.json' && !optional.includes(f));
  assert.ok(files.includes('README.md'), `${ROUND_DIR} holds ${JSON.stringify(files)}; README.md is missing`);
  assert.ok(files.includes('cells.json'), `${ROUND_DIR} holds ${JSON.stringify(files)}; cells.json is missing`);
  assert.deepStrictEqual(unexpected, [], `${ROUND_DIR} holds unexpected files ${JSON.stringify(unexpected)}; allowed are README.md, cells.json, manifest.json and recompute.py`);

  const actual = stripOneNewline(fs.readFileSync(path.join(dir, 'cells.json'), 'utf8'));
  const expected = stripOneNewline(this.sourceText);
  assert.ok(actual === expected, `${ROUND_DIR}/cells.json differs from the source data (actual ${actual.length} characters, expected ${expected.length})`);

  let data;
  try {
    data = JSON.parse(actual);
  } catch (e) {
    assert.fail(`${ROUND_DIR}/cells.json does not parse as JSON: ${e.message}`);
  }
  assert.ok(Array.isArray(data.cells), 'cells.json has no cells list');
  const slots = new Set(data.cells.map((c) => JSON.stringify([c.arm, c.task, c.rep])));
  assert.strictEqual(data.cells.length, 18, `cells.json holds ${data.cells.length} cells; expected 18`);
  assert.strictEqual(slots.size, 18, `cells.json holds ${slots.size} unique (arm, task, rep) slots; expected 18`);
  const numeric = data.cells.filter((c) => typeof c.score === 'number' && typeof c.total === 'number').length;
  const empty = data.cells.filter((c) => c.score === null && c.total === null).length;
  assert.strictEqual(numeric, 12, `cells.json holds ${numeric} cells with numeric score and total; expected 12`);
  assert.strictEqual(empty, 6, `cells.json holds ${empty} cells with null score and total; expected 6`);
  assert.strictEqual(data.candidate_adopted, null, 'candidate_adopted is not null');
});

Then('h23-round-cells-json-data: the inventory keeps the earlier entries in order and ends with the one h23 entry listing cells.json then the page', function () {
  let inventory;
  try {
    inventory = JSON.parse(fs.readFileSync(path.join(ROOT, 'reproduce', 'round-inventory.json'), 'utf8'));
  } catch (e) {
    assert.fail(`reproduce/round-inventory.json does not parse as JSON: ${e.message}`);
  }
  const rounds = inventory.rounds;
  assert.ok(Array.isArray(rounds), 'reproduce/round-inventory.json has no rounds list');
  const { earlierCount, earlierSha256, lastEntry } = this.expected;
  assert.strictEqual(rounds.length, earlierCount + 1, `the inventory holds ${rounds.length} entries; expected the ${earlierCount} earlier entries plus exactly the one h23 entry`);
  assert.strictEqual(sha256(stable(rounds.slice(0, -1))), earlierSha256, 'the earlier inventory entries differ from the recorded ones or are reordered');
  const want = { ...lastEntry, inputs: [`${ROUND_DIR}/cells.json`, `${ROUND_DIR}/README.md`] };
  assert.strictEqual(stable(rounds[rounds.length - 1]), stable(want), 'the last inventory entry is not the unchanged h23 entry with inputs cells.json then README.md');
});
