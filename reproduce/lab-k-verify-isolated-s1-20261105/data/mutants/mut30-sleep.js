const { When, Then } = require('@cucumber/cucumber');
const net = require('node:net'); const fs = require('node:fs');
const sleep = ms => new Promise(r => setTimeout(r, ms));
When('the lab hazard lab30 step waits 11 seconds', { timeout: 180000 }, async function () { await sleep(11000); });
