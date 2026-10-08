import path from 'node:path';
import { siteData } from '../lib/data.js';

function githubTarget(href: string, sourcePath: string) {
  if (!href || href.startsWith('/') || /^(?:https?:|mailto:|tel:)/i.test(href)) return href;
  if (href.startsWith('#')) return `https://github.com/KogenAI/kogen-bench/blob/${siteData.meta.revision}/${sourcePath}${href}`;
  const [relative, fragment] = href.split('#', 2);
  const resolved = path.posix.normalize(path.posix.join(path.posix.dirname(sourcePath || ''), relative)).replace(/^\.\.\//, '');
  return `https://github.com/KogenAI/kogen-bench/blob/${siteData.meta.revision}/${resolved}${fragment ? `#${fragment}` : ''}`;
}

function alternateMarkdown(page: any) {
  const body = page.markdown.replace(/\]\(([^)]+)\)/g, (_match: string, href: string) => `](${githubTarget(href, page.source_path)})`);
  const sources = page.sources.map((source: string) => `- [${source}](https://github.com/KogenAI/kogen-bench/blob/${siteData.meta.revision}/${source})`).join('\n');
  return `> Data revision: ${siteData.meta.revision}\n> Source files:\n${sources}\n\n${body}`;
}

export function getStaticPaths() {
  return siteData.pages.map((page: any) => ({
    params: { route: page.route === '/' ? 'index' : page.route.replace(/^\//, '').replace(/\/$/, '') },
    props: { page },
  }));
}

export function GET({ props }: { props: { page: any } }) {
  return new Response(alternateMarkdown(props.page), {
    headers: { 'Content-Type': 'text/markdown; charset=utf-8', 'X-Content-Type-Options': 'nosniff' },
  });
}
