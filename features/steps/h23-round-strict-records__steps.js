const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const { Given, Then } = require('@cucumber/cucumber');

const ROOT = path.resolve(__dirname, '..', '..');
const ROUND_ID = 'h23-release-bbf56fdc-vs-891c91b3';
const ROUND_DIR = path.join(ROOT, 'rounds', ROUND_ID);
const ADDED = ['MEASURED.md', 'MISSING-DECLARED.json', 'MISSING.md', 'records.jsonl'];
const SIX = ['MEASURED.md', 'MISSING-DECLARED.json', 'MISSING.md', 'README.md', 'cells.json', 'records.jsonl'];

const LEAKS = [
  ['home path', /(?:\/home\/|\/Users\/|\/root\b|[A-Za-z]:\\Users\\|~\/)/],
  ['host name', /\b[a-z0-9][a-z0-9-]*(?:\.[a-z0-9-]+)*\.(?:internal|local|lan|corp|home|localdomain|amazonaws\.com)\b/i],
  ['IP address', /\b(?:\d{1,3}\.){3}\d{1,3}\b/],
  ['e-mail address', /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/],
  ['credential', /(?:\bsk-[A-Za-z0-9_-]{16,}|\bgh[pousr]_[A-Za-z0-9]{20,}|\bAKIA[0-9A-Z]{16}\b|-----BEGIN [A-Z ]*PRIVATE KEY-----|\bBearer\s+[A-Za-z0-9._-]{12,}|(?:api[_-]?key|secret|password|passwd|auth[_-]?token|access[_-]?token)["']?\s*[:=]\s*["']?[A-Za-z0-9._\/+-]{8,})/i],
  ['raw transcript', /(?:transcript\.jsonl|"role"\s*:\s*"(?:user|assistant|system|tool)"|^(?:user|assistant):)/im],
  ['account meter', /(?:"(?:five_hour|seven_day|weekly_limit|rate_limits?|usage_limit|remaining_requests|credits_remaining)"|\b\d+(?:\.\d+)?%\s+of\s+(?:the\s+|your\s+)?(?:weekly|5-hour|five-hour|session|monthly)\b)/i],
];

function readCells() {
  const file = path.join(ROUND_DIR, 'cells.json');
  assert.ok(fs.existsSync(file), `rounds/${ROUND_ID}/cells.json is missing from the working tree`);
  return JSON.parse(fs.readFileSync(file, 'utf8')).cells;
}

function need(name) {
  const file = path.join(ROUND_DIR, name);
  assert.ok(fs.existsSync(file) && fs.statSync(file).isFile(), `rounds/${ROUND_ID}/${name} is missing; the directory holds ${JSON.stringify(fs.readdirSync(ROUND_DIR).sort())}`);
  return file;
}

// The rep of a record: a rep field, or the one standalone numeric token of cell_id.
function repOf(rec) {
  if (Number.isInteger(rec.rep)) return rec.rep;
  if (typeof rec.cell_id !== 'string') return null;
  const reps = rec.cell_id.split(/[^A-Za-z0-9]+/).map((t) => /^(?:r|rep)?(\d+)$/.exec(t)).filter(Boolean).map((m) => Number(m[1]));
  return reps.length === 1 ? reps[0] : null;
}

Given('h23-round-strict-records: the h23 round directory with its retained cells.json', function () {
  const cells = readCells();
  assert.strictEqual(cells.length, 18, `cells.json holds ${cells.length} slots; expected 18`);
  this.cells = cells;
  this.newCells = cells.filter((c) => c.reused === false);
  assert.strictEqual(this.newCells.length, 15, `cells.json holds ${this.newCells.length} new attempts; expected 15`);
});

Then('h23-round-strict-records: records.jsonl holds one line per new attempt with the slot arm, task and rep', function () {
  const lines = fs.readFileSync(need('records.jsonl'), 'utf8').split('\n');
  if (lines[lines.length - 1] === '') lines.pop();
  assert.strictEqual(lines.length, 15, `records.jsonl holds ${lines.length} lines; expected 15, one per new attempt and none for the 3 reused baseline slots`);
  const seen = new Set();
  lines.forEach((line, i) => {
    let rec;
    try { rec = JSON.parse(line); } catch (e) { assert.fail(`records.jsonl line ${i + 1} is not JSON: ${e.message}`); }
    assert.strictEqual(rec.schema_version, '1.2', `line ${i + 1} schema_version`);
    assert.strictEqual(rec.round_id, ROUND_ID, `line ${i + 1} round_id`);
    assert.strictEqual(rec.audit_round, ROUND_ID, `line ${i + 1} audit_round`);
    const taskId = rec.task && rec.task.id;
    const rep = repOf(rec);
    const hits = this.newCells.filter((c) => rec.arm === c.arm && taskId === c.task && rep === c.rep);
    assert.strictEqual(hits.length, 1, `line ${i + 1} (arm ${JSON.stringify(rec.arm)}, task ${JSON.stringify(taskId)}, rep ${JSON.stringify(rep)}, cell_id ${JSON.stringify(rec.cell_id)}) matches ${hits.length} new attempts of cells.json by arm, task and rep; expected 1`);
    seen.add(`${hits[0].arm}|${hits[0].task}|${hits[0].rep}`);
  });
  assert.strictEqual(seen.size, 15, `records.jsonl covers ${seen.size} distinct (arm, task, rep) slots; expected 15`);
});

Then('h23-round-strict-records: every missing-field declaration uses a registered reason code and matches the records', function () {
  for (const name of ADDED) need(name);
  const legend = JSON.parse(fs.readFileSync(path.join(ROOT, 'results', 'missing-reasons.json'), 'utf8')).codes;
  const decl = JSON.parse(fs.readFileSync(need('MISSING-DECLARED.json'), 'utf8'));
  assert.ok(decl.fields && typeof decl.fields === 'object', 'MISSING-DECLARED.json has no fields object');
  for (const [field, item] of Object.entries(decl.fields)) {
    assert.ok(item && typeof item.reason_code === 'string' && Object.prototype.hasOwnProperty.call(legend, item.reason_code), `field ${field} uses reason code ${JSON.stringify(item && item.reason_code)}, which is not in results/missing-reasons.json`);
    assert.ok(typeof item.note === 'string' && item.note.trim() !== '', `field ${field} has no plain-language note`);
  }
  const script = [
    'import sys, json',
    'from pathlib import Path',
    'sys.path.insert(0, "reproduce")',
    'import validate_round',
    'rid, p = sys.argv[1], sys.argv[2]',
    'rep = validate_round.validate(rid, validate_round.records(Path(p)), True)',
    'print(json.dumps({"errors": rep["errors"], "cells": rep["cells"], "missing_fields": sorted(rep["missing_fields"])}))',
  ].join('\n');
  const out = execFileSync('python3', ['-c', script, ROUND_ID, path.join(ROUND_DIR, 'records.jsonl')], { cwd: ROOT, encoding: 'utf8', timeout: 100000 });
  const rep = JSON.parse(out.trim().split('\n').pop());
  assert.deepStrictEqual(rep.errors, [], `the strict round validation of the records reports errors: ${JSON.stringify(rep.errors.slice(0, 5))}`);
  assert.strictEqual(rep.cells, 15, `the strict round validation saw ${rep.cells} records; expected 15`);
  assert.deepStrictEqual(Object.keys(decl.fields).sort(), rep.missing_fields, 'MISSING-DECLARED.json declares a different set of fields than the records leave missing');
});

Then('h23-round-strict-records: the four added files hold no home path, host name, IP address, e-mail address, credential, raw transcript or account meter', function () {
  for (const name of ADDED) {
    const text = fs.readFileSync(need(name), 'utf8');
    for (const [label, re] of LEAKS) {
      const m = re.exec(text);
      assert.ok(!m, `${name} holds a ${label}: ${m && JSON.stringify(m[0].slice(0, 40))}`);
    }
  }
});

Then('h23-round-strict-records: the h23 round directory holds each of README.md, cells.json and the four added files', function () {
  const names = fs.readdirSync(ROUND_DIR, { withFileTypes: true }).filter((e) => e.isFile()).map((e) => e.name);
  const absent = SIX.filter((n) => !names.includes(n));
  assert.deepStrictEqual(absent, [], `rounds/${ROUND_ID} lacks ${JSON.stringify(absent)}; it holds ${JSON.stringify(names.sort())}`);
});

Then('h23-round-strict-records: the h23 round directory holds no file or subdirectory besides those six', function () {
  const names = fs.readdirSync(ROUND_DIR).sort();
  const extra = names.filter((n) => !SIX.includes(n));
  assert.deepStrictEqual(extra, [], `rounds/${ROUND_ID} holds extra entries ${JSON.stringify(extra)}`);
});
