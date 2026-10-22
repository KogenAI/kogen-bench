const assert = require('node:assert/strict');
const { execFileSync, spawnSync } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { Before, Given, When, Then } = require('@cucumber/cucumber');

const projectRoot = path.resolve(__dirname, '../..');
let built = false;

Before(function () {
  if (!built) {
    execFileSync('make', ['build'], { cwd: projectRoot, stdio: 'pipe' });
    built = true;
  }
  this.scratch = fs.mkdtempSync(path.join(os.tmpdir(), 'kogen-cli-'));
  this.input = Buffer.alloc(0);
});

Given('the input text:', function (text) {
  this.input = Buffer.from(text + '\n', 'ascii');
});

Given('the input bytes {string}', function (escaped) {
  this.input = Buffer.from(JSON.parse(`"${escaped}"`), 'latin1');
});

Given('a file {string} containing:', function (name, text) {
  fs.writeFileSync(path.join(this.scratch, name), text + '\n');
});

When('I run kogen with no arguments', function () {
  this.result = run(this, []);
});

When('I run kogen with {string}', function (args) {
  const argv = args.split(' ').map(token =>
    token.startsWith('@') ? path.join(this.scratch, token.slice(1)) : token);
  this.result = run(this, argv);
});

Then('the exit status is {int}', function (code) {
  assert.equal(this.result.status, code, this.result.stderr.toString());
});

Then('stdout is:', function (text) {
  assert.equal(this.result.stdout.toString('latin1'), text + '\n');
});

Then('stdout is empty', function () {
  assert.equal(this.result.stdout.toString('latin1'), '');
});

Then('stderr is {string}', function (line) {
  assert.equal(this.result.stderr.toString('latin1'), line + '\n');
});

Then('stderr is empty', function () {
  assert.equal(this.result.stderr.toString('latin1'), '');
});

function run(world, argv) {
  return spawnSync(path.join(projectRoot, 'run'), argv, {
    cwd: world.scratch,
    input: world.input,
    timeout: 15000,
  });
}
