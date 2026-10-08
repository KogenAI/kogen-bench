import { siteData } from '../lib/data.js';

export function GET() {
  const gates = siteData.meta.publication_blockers.map((item) => `${item.id} (${item.status}): ${item.summary}`).join(' ');
  const body = `# Kogen Bench

Static research site generated from KogenAI/kogen-bench.

- Home: https://bench.kogen.dev/
- Findings: https://bench.kogen.dev/findings/
- Hypothesis register: https://bench.kogen.dev/hypotheses/
- Experiment register: https://bench.kogen.dev/rounds/
- Comparisons: https://bench.kogen.dev/comparisons/
- Evidence map: https://bench.kogen.dev/evidence/
- Publication validation: https://bench.kogen.dev/publication-validation/
- Method: https://bench.kogen.dev/methods/
- Reproduce: https://bench.kogen.dev/reproduce/
- Verify published numbers: https://bench.kogen.dev/verify/
- Rerun and regrade tasks: https://bench.kogen.dev/rerun/
- Credits: https://bench.kogen.dev/credits/
- Data downloads: https://bench.kogen.dev/data/
- Full hypothesis, round, and claim index: https://bench.kogen.dev/index.json
- Search index: https://bench.kogen.dev/search-index.json
- Snapshot and source hashes: https://bench.kogen.dev/snapshot.json
- Full bounded guide: https://bench.kogen.dev/llms-full.txt

## Evidence status rules

Read the status on each claim and round. A source-reported number is not a verified result merely because it is rendered. Claim values are transcribed from results/claim-ledger.jsonl and retain evidence_status, claim_status, cohort, and unit. Outcome-only rows and captured run records are not joined by guessed keys. Missing and withheld values are not zero. The site does not pool incompatible cohorts. Auditor verdicts are not official benchmark grades.

## Publication status

Publication is ${siteData.meta.publication_status}. ${gates} The refreshed public official grade export exact-joins all 5,020 of 5,020 captured graded IDs. The 128 added post-cut rows comprise 84 model PASS, 19 model FAIL, and 25 invalid control_apply rows (result=invalid/outcome=fail); controls are not model failures. B2 locally verifies the pinned v1.2 fragments cited by EVIDENCE-MAP.md; the absent decision ledger means comprehensive decision-to-clause coverage remains limited. See https://github.com/KogenAI/kogen-bench/blob/${siteData.meta.revision}/results/GRADE-JOIN.md and the full disclosure at https://bench.kogen.dev/publication-validation/.

## Snapshot

Data revision: ${siteData.meta.revision}
`;
  return new Response(body, { headers: { 'Content-Type': 'text/plain; charset=utf-8', 'X-Content-Type-Options': 'nosniff' } });
}
