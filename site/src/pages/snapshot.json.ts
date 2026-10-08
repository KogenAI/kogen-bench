import { siteData } from '../lib/data.js';

export function GET() {
  return new Response(JSON.stringify({
    site: siteData.meta.site,
    data_revision: siteData.meta.revision,
    built_at: siteData.meta.built_at,
    number_policy: siteData.meta.number_policy,
    source_metadata_note: 'Byte lengths are generated file metadata, not benchmark outcomes. Benchmark numeric values follow the claim-ledger or source-reported policy.',
    source_files: siteData.meta.source_files,
    publication_status: siteData.meta.publication_status,
    publication_gates: siteData.meta.publication_gates,
    inventory_failures: siteData.meta.inventory_failures,
  }, null, 2) + '\n', {
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'X-Content-Type-Options': 'nosniff' },
  });
}
