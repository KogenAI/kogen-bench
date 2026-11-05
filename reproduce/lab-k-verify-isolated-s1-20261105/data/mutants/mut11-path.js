const { When, Then } = require('@cucumber/cucumber');
const net = require('node:net'); const fs = require('node:fs');
const sleep = ms => new Promise(r => setTimeout(r, ms));
When('the lab hazard lab11 step uses its fixed directory', { timeout: 120000 }, async function () {
  fs.mkdirSync('/tmp/lab-s1-fixed-1');
  try { await sleep(2000); } finally { fs.rmSync('/tmp/lab-s1-fixed-1', { recursive: true, force: true }); }
});
