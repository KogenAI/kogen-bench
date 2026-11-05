const { When, Then } = require('@cucumber/cucumber');
const net = require('node:net'); const fs = require('node:fs');
const sleep = ms => new Promise(r => setTimeout(r, ms));
let prepared_lab21 = false;
When('the lab hazard lab21 fixture is prepared', function () { prepared_lab21 = true; });
Then('the lab hazard lab21 fixture is ready', function () { if (!prepared_lab21) throw new Error('fixture not prepared: depends on scenario order'); });
