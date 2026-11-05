'use strict';
// batch.js <replay dir>... --out <dir> --n <count> [--times k]: one Quint module holding the recorded Build chains of the given replay outputs.
const fs = require('node:fs'), path = require('node:path');
const REPLAY = process.env.REPLAY_SRC;
const { generate } = require(path.join(REPLAY, 'trace.js'));
const args = process.argv.slice(2);
const out = args[args.indexOf('--out') + 1], n = Number(args[args.indexOf('--n') + 1]);
const times = args.includes('--times') ? Number(args[args.indexOf('--times') + 1]) : 1;
const dirs = args.filter((a, i) => !a.startsWith('--') && args[i - 1] !== '--out' && args[i - 1] !== '--n' && args[i - 1] !== '--times');
const recs = [];
for (const d of dirs) for (const c of ['approval', 'verification-review', 'interruption-resume', 'commit-recovery']) {
  const obs = JSON.parse(fs.readFileSync(path.join(d, 'cases', c, 'observations.json'), 'utf8'));
  for (const ch of obs.chains) recs.push({ id: `${path.basename(d)}-${c}-${ch.name}`, journey: c, chain: ch });
}
const picked = [];
for (let t = 0; t < times; t++) for (const r of recs.slice(0, n)) picked.push({ ...r, id: `${r.id}-x${t}` });
fs.mkdirSync(out, { recursive: true });
fs.mkdirSync(path.join(out, 'model'), { recursive: true });
fs.copyFileSync(path.join(path.dirname(path.dirname(path.dirname(REPLAY))), 'spec/quint/build.qnt'), path.join(out, 'model/build.qnt'));
const bodies = [];
for (const r of picked) {
  const t = generate(r.id, [r.chain], 'model/build');
  const lines = t.text.split('\n'), start = lines.findIndex(l => l.startsWith('  run ')), end = lines.lastIndexOf('}');
  bodies.push(lines.slice(start, end).join('\n'));
}
const text = ['// Batched: recorded Build chains of the installed kogen, one Quint module, one quint test process.', 'module batchReplay {', '  import build.* from "model/build"', '', bodies.join('\n\n'), '}', ''].join('\n');
fs.writeFileSync(path.join(out, 'batch.qnt'), text);
console.log(JSON.stringify({ chains: picked.length, runs: bodies.length, bytes: text.length }));
