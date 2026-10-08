import { siteData } from '../lib/data.js';

export function GET() {
  return new Response(JSON.stringify(siteData.index, null, 2) + '\n', {
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'X-Content-Type-Options': 'nosniff' },
  });
}
