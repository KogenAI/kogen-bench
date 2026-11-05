const { When, Then } = require('@cucumber/cucumber');
const net = require('node:net'); const fs = require('node:fs');
const sleep = ms => new Promise(r => setTimeout(r, ms));
When('the lab hazard lab32 step waits 13 seconds', { timeout: 180000 }, async function () { await sleep(13000); });
