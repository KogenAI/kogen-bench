import { marked } from 'marked';
import path from 'node:path';

const GITHUB = 'https://github.com/KogenAI/kogen-bench';

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  })[char]);
}

function sourceTarget(href, sourcePath, revision) {
  if (!href || /^(?:https?:|mailto:|tel:|data:)/i.test(href)) return href || '';
  if (href.startsWith('#')) return `${GITHUB}/blob/${revision}/${sourcePath}${href}`;
  if (href.startsWith('/')) return href;
  const [relative, fragment] = href.split('#', 2);
  const resolved = path.posix.normalize(path.posix.join(path.posix.dirname(sourcePath || ''), relative));
  const clean = resolved.replace(/^\.\//, '').replace(/^\.\.\//, '');
  return `${GITHUB}/blob/${revision}/${clean}${fragment ? `#${fragment}` : ''}`;
}

export function renderMarkdown(markdown, sourcePath, revision) {
  const renderer = new marked.Renderer();
  renderer.link = ({ href, title, text }) => {
    const safeHref = sourceTarget(href, sourcePath, revision);
    const safeTitle = title ? ` title="${escapeHtml(title)}"` : '';
    const external = /^https?:/i.test(safeHref) ? ' target="_blank" rel="noopener noreferrer"' : '';
    return `<a href="${escapeHtml(safeHref)}"${safeTitle}${external}>${text}</a>`;
  };
  renderer.image = ({ href, title, text }) => {
    const safeHref = sourceTarget(href, sourcePath, revision);
    const safeTitle = title ? ` title="${escapeHtml(title)}"` : '';
    return `<img src="${escapeHtml(safeHref)}" alt="${escapeHtml(text)}"${safeTitle} loading="lazy">`;
  };
  renderer.html = ({ text }) => escapeHtml(text.replace(/<!--[\s\S]*?-->/g, ''));
  const renderTable = renderer.table.bind(renderer);
  renderer.table = token => `<div class="record-table-wrap" role="region" aria-label="Data table" tabindex="0">${renderTable(token)}</div>`;
  return marked.parse(markdown || '', { gfm: true, breaks: false, renderer });
}
