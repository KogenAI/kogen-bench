import data from '../../.generated/site-data.json';

export const siteData = data;
export const pageByRoute = new Map(data.pages.map((page) => [page.route, page]));
export const githubBlob = (path) => `https://github.com/KogenAI/kogen-bench/blob/${data.meta.revision}/${path}`;

export function recordsForFamily(familyId) {
  return data.families.find((family) => family.id === familyId);
}

export function recordsForHypothesis(id) {
  return data.hypotheses.find((hypothesis) => hypothesis.id === id);
}

export function recordsForRound(id) {
  return data.rounds.find((round) => round.id === id);
}

export function recordsForClaim(id) {
  return data.claims.find((claim) => claim.claim_id === id);
}

export function recordsForEvidence(id) {
  return data.evidence.find((clause) => clause.id === id);
}
