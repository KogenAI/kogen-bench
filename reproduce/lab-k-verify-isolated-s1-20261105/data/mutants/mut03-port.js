const { When, Then } = require('@cucumber/cucumber');
const net = require('node:net'); const fs = require('node:fs');
const sleep = ms => new Promise(r => setTimeout(r, ms));
When('the lab hazard lab03 service serves on its fixed port', { timeout: 120000 }, async function () {
  const srv = net.createServer(); await new Promise((res, rej) => { srv.once('error', rej); srv.listen(47103, 'localhost', res); });
  await sleep(2000); await new Promise(r => srv.close(r));
});
