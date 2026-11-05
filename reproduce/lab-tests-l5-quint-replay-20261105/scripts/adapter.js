'use strict';
// adapter.js <replay dir> <acceptance record dir> <out dir> [--n N]
// Lab L5 scratch adapter: each recorded acceptance project folder (a Build's git repo and run folders, kept before the harness
// deleted it) becomes one chain with ONE end-of-Build snapshot, built by the replay's own observe(); the replay's generator
// writes Quint run tests; all eligible chains go into one module. Eligible = exactly one Intent folder and exactly one run folder.
const fs = require('node:fs'), path = require('node:path'), os = require('node:os');
const [REPLAY, REC, OUT] = process.argv.slice(2, 5);
const { generate } = require(path.join(REPLAY, 'trace.js'));
const labSrc = fs.readFileSync(path.join(REPLAY, 'lab.js'), 'utf8').replace("require('./fake.js')", `require(${JSON.stringify(path.join(REPLAY, 'fake.js'))})`).replace("path.resolve(__dirname, '../../..')", `path.resolve(${JSON.stringify(REPLAY)}, '../../..')`);
fs.mkdirSync(OUT, { recursive: true });
const labs = {};
function labFor(slug) {
  if (!labs[slug]) {
    const f = path.join(OUT, `lab-${slug}.js`);
    fs.writeFileSync(f, labSrc.replace("const SLUG = 'add-greeting';", `const SLUG = ${JSON.stringify(slug)};`));
    labs[slug] = require(f);
  }
  return labs[slug];
}
const rows = [];
for (const meta of fs.readdirSync(REC).filter(f => f.endsWith('.meta.json')).sort()) {
  const id = meta.replace('.meta.json', ''), dir = path.join(REC, id), m = JSON.parse(fs.readFileSync(path.join(REC, meta), 'utf8'));
  const row = { id, scenario: m.scenario, uri: path.basename(m.uri), eligible: false, reason: null };
  rows.push(row);
  try {
    const intents = fs.existsSync(path.join(dir, '.kogen/intents')) ? fs.readdirSync(path.join(dir, '.kogen/intents')) : [];
    const runsDir = path.join(dir, '.kogen/local/runs');
    const runs = fs.existsSync(runsDir) ? fs.readdirSync(runsDir).filter(d => /^[a-f0-9]{8}$/.test(d)) : [];
    if (intents.length !== 1) { row.reason = `${intents.length} Intent folders`; continue; }
    if (runs.length !== 1) { row.reason = `${runs.length} run folders (resumed or several Builds)`; continue; }
    const { Lab, SLUG } = labFor(intents[0]);
    const home = fs.mkdtempSync(path.join(os.tmpdir(), 'l5adapter-'));
    fs.writeFileSync(path.join(home, '.gitconfig'), '[user]\n\tname = Fixture\n\temail = fixture-address\n[safe]\n\tdirectory = *\n');
    const lab = Object.assign(Object.create(Lab.prototype), { repo: dir, dir: home, cursors: new Map(), strict: false, deviations: [], snapshotErrors: [], chains: [],
      env: { HOME: home, LANG: 'C', LC_ALL: 'C', PATH: process.env.PATH, GIT_CONFIG_GLOBAL: path.join(home, '.gitconfig'), GIT_CONFIG_NOSYSTEM: '1' } });
    const chain = { name: 'build', snapshots: [] };
    chain.snapshots.push(lab.observe('end of Build', runs[0], chain));
    row.slug = SLUG; row.events = chain.snapshots[0].events.map(e => e.k).join(','); row.outcome = chain.snapshots[0].outcome; row.deviations = lab.deviations;
    row.chain = chain; row.eligible = true;
  } catch (e) { row.reason = `adapter error: ${String(e.message).split('\n')[0].slice(0, 200)}`; }
}
const elig = rows.filter(r => r.eligible);
const bodies = elig.map((r, i) => {
  const t = generate(`acc${i + 1}`, [r.chain], 'model/build');
  r.test = t.tests[0]; r.t = t;
  const lines = t.text.split('\n');
  return lines.slice(lines.findIndex(l => l.startsWith('  run ')), lines.lastIndexOf('}')).join('\n');
});
fs.mkdirSync(path.join(OUT, 'model'), { recursive: true });
fs.copyFileSync(path.join(REPLAY, '../../../spec/quint/build.qnt'), path.join(OUT, 'model/build.qnt'));
const mk = (n, name) => fs.writeFileSync(path.join(OUT, name), ['module accBatch {', '  import build.* from "model/build"', '', bodies.slice(0, n).join('\n\n'), '}', ''].join('\n'));
mk(10, 'batch10.qnt'); mk(bodies.length, 'batchAll.qnt');
const QUINT = path.join(REPLAY, '../../../spec/node_modules/@informalsystems/quint/dist/src/cli.js');
const cpx = require('node:child_process');
if (process.env.FAIL) {
  for (const i of process.env.FAIL.split(',').map(Number)) {
    const r = elig[i - 1], t = r.t, name = t.tests[0], info = t.steps[0];
    const fails = k => { const f = path.join(OUT, 'prefix.qnt'); fs.writeFileSync(f, t.only(name, k)); return cpx.spawnSync(process.execPath, [QUINT, 'test', '--backend', 'typescript', f], { cwd: OUT }).status !== 0; };
    let lo = 1, hi = info.count; if (!fails(hi)) { r.firstFail = null; continue; }
    while (lo < hi) { const mid = (lo + hi) >> 1; if (fails(mid)) hi = mid; else lo = mid + 1; }
    r.firstFail = { step: lo, of: info.count, action: info.actions[lo - 1], observed: info.comments[lo - 1] };
  }
}
fs.writeFileSync(path.join(OUT, 'rows.json'), JSON.stringify(rows.map(({ chain, t, ...r }) => r), null, 1));
console.log(JSON.stringify({ recorded: rows.length, eligible: elig.length, skipped: rows.filter(r => !r.eligible).map(r => r.reason) }));
