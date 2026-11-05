const { When, Then } = require('@cucumber/cucumber');
const net = require('node:net'); const fs = require('node:fs');
const sleep = ms => new Promise(r => setTimeout(r, ms));
When('the lab hazard lab10 step uses its fixed directory', { timeout: 120000 }, async function () {
  fs.mkdirSync('/tmp/lab-s1-fixed-0');
  try { await sleep(2000); } finally { fs.rmSync('/tmp/lab-s1-fixed-0', { recursive: true, force: true }); }
});
