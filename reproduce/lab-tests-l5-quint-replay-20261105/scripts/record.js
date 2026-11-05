'use strict';
// Scratch recording hook for Lab L5 (outside the repository): copies each @model:build scenario's project folder
// (git repo, run folders, facts, approvals) before the harness deletes it. Loaded last, so it runs first among After hooks.
const { After } = require('@cucumber/cucumber');
const fs = require('node:fs'), path = require('node:path');
After(async function ({ pickle, result }) {
  const rec = process.env.ACC_RECORD;
  if (!rec || !pickle.tags.some(t => t.name === '@model:build')) return;
  const p = this.project;
  if (!p || !fs.existsSync(path.join(p, '.kogen/local/runs'))) return;
  const name = `${Date.now()}-${pickle.name.replace(/[^A-Za-z0-9]+/g, '-').slice(0, 60)}`;
  fs.mkdirSync(rec, { recursive: true });
  fs.cpSync(p, path.join(rec, name), { recursive: true, filter: s => !s.includes('node_modules') });
  fs.writeFileSync(path.join(rec, `${name}.meta.json`), JSON.stringify({ scenario: pickle.name, uri: pickle.uri, status: result && result.status }));
});
