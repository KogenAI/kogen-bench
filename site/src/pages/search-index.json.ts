import { siteData } from '../lib/data.js';

const entries = [
  ...siteData.hypotheses.map((item) => ({ id: item.id, title: item.id, text: item.proposition, url: `/hypotheses/${item.slug}/`, kind: 'hypothesis', status: item.status, family: item.family_id })),
  ...siteData.rounds.map((item) => ({ id: item.id, title: item.title, text: `${item.id} ${item.hypothesis_ids.join(' ')} ${item.family_ids.join(' ')}`, url: `/rounds/${item.slug}/`, kind: 'round', status: item.status, family: item.family_ids.join(' ') })),
  ...siteData.claims.map((item) => ({ id: item.claim_id, title: item.claim_id, text: `${item.metric || ''} ${item.evidence_status || ''} ${item.interpretation || ''}`, url: `/claims/${item.claim_id.toLowerCase()}/`, kind: 'claim', status: item.claim_status, family: '' })),
  ...siteData.evidence.map((item) => ({ id: item.id, title: item.title, text: `${item.hypothesis_ids.join(' ')} ${item.round_ids.join(' ')} ${item.claim_ids.join(' ')}`, url: `/evidence/${item.id}/`, kind: 'evidence', status: 'source map', family: '' })),
];

export function GET() {
  return new Response(JSON.stringify({ data_revision: siteData.meta.revision, entries }, null, 2) + '\n', {
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'X-Content-Type-Options': 'nosniff' },
  });
}
