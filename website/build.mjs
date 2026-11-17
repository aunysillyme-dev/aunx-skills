import { readFileSync, writeFileSync, mkdirSync, rmSync, copyFileSync, existsSync, readdirSync, statSync } from 'node:fs';
import { join, dirname, resolve, posix } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
import { buildJsonLd, buildFaqJsonLd, loadSourceFacts, visibleText, section } from './facts.mjs';
import { pages } from './pages.mjs';
import { content } from './content.mjs';
import { renderProjectsPopup } from './projects-popup-render.mjs';
import { assets, csp, fontStylesheet } from './resources.mjs';

const origin = 'https://aunx-skills.aunysillyme.dev';
const repository = 'https://github.com/aunysillyme-dev/aunx-skills';
const read = (root, file) => readFileSync(join(root, file), 'utf8');
const json = (root, file) => JSON.parse(read(root, file));
const requireValue = (ok, message) => { if (!ok) throw Error(message); };
export const escape = value => String(value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);
const slug = text => visibleText(text).toLowerCase().replace(/[^\p{L}\p{N}\s_-]/gu, '').trim().replace(/\s+/g, '-') || 'section';

function readSet(root) {
  const { rows } = json(root, 'website/set.json');
  requireValue(Array.isArray(rows) && rows.length > 0, 'Project set rows missing in website/set.json');
  return rows;
}

function projectsPopup(root) {
  return renderProjectsPopup({ rows: readSet(root), current: 'aunx-skills', id: 'projects-popup', fallbackHref: 'https://aunysillyme.dev/#projects' });
}

export function rewriteUrl(href, source, root = fileURLToPath(new URL('..', import.meta.url))) {
  if (!href || /[\u0000-\u0020\u007f\\]/.test(href)) return '';
  if (href.startsWith('#')) {
    if (href === '#plugins' && source === 'README.md') return '/docs/plugins/';
    return href;
  }
  if (/^https?:\/\//i.test(href)) return href;
  if (/^(?:[a-z][a-z\d+.-]*:|\/\/)/i.test(href)) return '';
  const [file, fragment] = href.split('#');
  const normalized = posix.normalize(file.startsWith('/') ? file.slice(1) : posix.join(posix.dirname(source), file));
  if (normalized === '..' || normalized.startsWith('../')) return '';
  const suffix = fragment ? `#${fragment}` : '';
  let isDir = file.endsWith('/');
  try { isDir = statSync(join(root, normalized)).isDirectory(); } catch {}
  return `${repository}/${isDir ? 'tree' : 'blob'}/main/${normalized}${suffix}`;
}

function uniqueId(text, ids) {
  const base = slug(text);
  let id = base, count = 0;
  while (ids.has(id)) id = `${base}-${++count}`;
  ids.add(id);
  return id;
}

export function renderMarkdown(markdown, { source = 'README.md', ids = new Set() } = {}) {
  const references = new Map();
  markdown = markdown.replace(/^---\n[^]*?\n---\n/, '').replace(/<!--[^]*?-->/g, ' ');
  markdown = markdown.replace(/^\[([^\]]+)\]:\s*(\S+).*$/gm, (_, label, href) => { references.set(label.toLowerCase(), href); return ''; });
  function inline(value, tokens = []) {
    const save = html => { tokens.push(html); return `\u0000${tokens.length - 1}\u0000`; };
    value = value.replace(/`([^`]+)`/g, (_, code) => save(`<code>${escape(code)}</code>`));
    value = value.replace(/<(script|style|iframe|object|svg)\b[^>]*>[^]*?<\/\1\s*>/gi, ' ').replace(/<\/?[a-z][^>]*>/gi, ' ');
    value = value.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, () => '');
    value = value.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_, label, href) => {
      const url = rewriteUrl(href, source);
      const rendered = inline(label, tokens);
      return save(rendered.trim() && url ? `<a href="${escape(url)}">${rendered}</a>` : rendered);
    });
    value = escape(value).replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>').replace(/\*([^*\n]+)\*/g, '<em>$1</em>');
    return value.replace(/\u0000(\d+)\u0000/g, (_, index) => tokens[Number(index)]);
  }
  const lines = markdown.replace(/\r\n/g, '\n').split('\n');
  const blocks = [];
  for (let index = 0; index < lines.length;) {
    const line = lines[index];
    if (!line.trim()) { index++; continue; }
    if (/^\s*```/.test(line)) {
      const code = [];
      index++;
      while (index < lines.length && !/^\s*```/.test(lines[index])) code.push(lines[index++]);
      index++;
      blocks.push(`<pre><code>${escape(code.join('\n'))}</code></pre>`);
      continue;
    }
    const heading = line.match(/^(#{1,6})\s+(.+)$/);
    if (heading) {
      const depth = Math.max(2, heading[1].length);
      const text = inline(heading[2]);
      blocks.push(`<h${depth} id="${uniqueId(text, ids)}">${text}</h${depth}>`);
      index++; continue;
    }
    if (/^\|/.test(line) && /^\|\s*:?-{3}/.test(lines[index + 1] || '')) {
      const cells = value => value.trim().replace(/^\||\|$/g, '').split(/(?<!\\)\|/).map(cell => inline(cell.trim().replace(/\\\|/g, '|')));
      const head = cells(line);
      index += 2;
      const rows = [];
      while (index < lines.length && /^\|/.test(lines[index])) rows.push(cells(lines[index++]));
      blocks.push(`<div class="table-scroll"><table><thead><tr>${head.map(cell => `<th scope="col">${cell}</th>`).join('')}</tr></thead><tbody>${rows.map(row => `<tr>${row.map(cell => `<td>${cell}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`);
      continue;
    }
    if (/^\s*(?:[-*]|\d+\.)\s+/.test(line)) {
      const ordered = /^\s*\d+\./.test(line), items = [];
      const pattern = ordered ? /^\s*\d+\.\s+/ : /^\s*[-*]\s+/;
      while (index < lines.length && pattern.test(lines[index])) {
        let text = lines[index++].replace(pattern, '');
        while (index < lines.length && /^\s{2,}\S/.test(lines[index]) && !/^\s*(?:[-*]|\d+\.|```)/.test(lines[index])) text += ` ${lines[index++].trim()}`;
        items.push(`<li>${inline(text)}</li>`);
      }
      blocks.push(`<${ordered ? 'ol' : 'ul'}>${items.join('')}</${ordered ? 'ol' : 'ul'}>`);
      continue;
    }
    if (/^>/.test(line)) {
      const quote = [];
      while (index < lines.length && /^>/.test(lines[index])) quote.push(lines[index++].replace(/^>\s?/, ''));
      blocks.push(`<blockquote><p>${inline(quote.join('\n'))}</p></blockquote>`);
      continue;
    }
    if (/^\s*(?:---+|\*\*\*+)\s*$/.test(line)) { blocks.push('<hr>'); index++; continue; }
    const paragraph = [lines[index++]];
    while (index < lines.length && lines[index].trim() && !/^(?:#{1,6}\s|\s*```|\||>|\s*[-*]\s|\s*\d+\.\s)/i.test(lines[index])) paragraph.push(lines[index++]);
    const rendered = inline(paragraph.join('\n'));
    if (rendered.trim()) blocks.push(`<p>${rendered}</p>`);
  }
  return blocks.join('\n');
}

function cardTrace() {
  return '<svg class="card-trace" aria-hidden="true" focusable="false"><rect class="ray-tail" x=".5" y=".5" pathLength="100"/><rect class="ray-mid" x=".5" y=".5" pathLength="100"/><rect class="ray-tip" x=".5" y=".5" pathLength="100"/></svg>';
}

function docsBody(root, page, facts) {
  const readme = facts.readme;
  let markdown, source = 'README.md';
  if (page.key === 'overview') markdown = facts.lead + '\n\n' + section(readme, 'Choose a skill') + '\n\n' + section(readme, 'Questions people ask');
  else if (page.key === 'install') markdown = section(readme, 'Install a pack') + '\n\n' + section(readme, 'Demos and packaging');
  else if (page.key === 'plugins') markdown = section(readme, 'Plugins');
  else {
    markdown = section(readme, 'What runs and what changes') + '\n\n' + facts.credits.replace(/^# [^\n]+\n/, '## Upstream credits and licenses\n');
  }
  const ids = new Set(['main', 'page-title']);
  const body = `<p class="source-note">From <a href="${repository}/blob/main/${source}">${source}</a></p>` + renderMarkdown(markdown, { source, ids });
  return `<article class="markdown">${body}</article>`;
}

function landingBody(root, facts) {
  const heading = (title, id, label, body, extra = '') => `<section class="content ${extra}" id="${id}"><div class="section-title"><h2>${escape(title)}</h2><span>${escape(label)}</span></div>${body}</section>`;
  const graphic = `<div class="routing card">${cardTrace()}<div class="routing-head"><span>QUIET FAILURE MODES</span><span>TEN FOCUSED PACKS</span></div><div class="task-tabs" role="group" aria-label="Skill categories">${[
    ['clauses', 'Logs', 'Full Output Keeper retains complete command output and exit codes on disk.'],
    ['units', 'Math', 'Number Guard computes consequential figures and pairs exact with rounded totals.'],
    ['waves', 'Renames', 'Rename Sweep maps code, docs, settings and tickets before verifying zero leftovers.'],
    ['check', 'Rules', 'Instruction Weight and Retro to Rules require explicit approval before changing rules.']
  ].map(([key, title, caption], i) => `<button type="button" data-task="${key}" data-caption="${caption}" aria-pressed="${i === 0}">${title}</button>`).join('')}</div><div class="task" id="task-text" aria-live="polite">Full Output Keeper retains complete command output and exit codes on disk.</div><div class="stem"></div><div class="route-core selected" data-role="clauses">PLAIN SKILL.MD + OPTIONAL LOCAL HELPERS</div><div class="split"></div><div class="route-options"><div data-role="units"><b>4 Free</b>Logs, math, docs, audio</div><div data-role="waves"><b>6 Paid ($7.99 bundle)</b>Agensi + MIT repo source</div><div data-role="check"><b>Decompose</b>Bundled wave planner</div></div><p class="route-foot">Plain Markdown with YAML frontmatter.<br>Zero background services and zero telemetry.</p></div>`;
  const faq = facts.faq.map(row => `<details><summary>${escape(row.question)}</summary>${renderMarkdown(row.answerMarkdown, { source: 'README.md' })}</details>`).join('');
  return `<div class="crumb"><a href="https://aunysillyme.dev/">Home</a><span>/</span><b>aunx-skills</b></div>
<section class="hero" id="overview"><div><p class="eyebrow">${escape(content.eyebrow)}</p><h1>${escape(content.headline)}<br><em>${escape(content.headlineAccent)}</em></h1><p class="lede">${escape(facts.lead)}</p><div class="install card">${cardTrace()}<span class="dollar" aria-hidden="true">$</span><code id="install-command">${escape(content.install.command)}</code><button class="copy" type="button" data-copy="install-command" aria-label="Copy install command"><span data-button-label>⧉</span></button></div><div class="hero-actions"><a class="primary" href="#quickstart">Install a pack ↓</a><a href="${repository}">Explore the source ↗</a></div></div>${graphic}</section>
<div class="trust"><span>10 standalone skills</span><span>Claude, Codex, Cursor, Gemini</span><span>Zero telemetry</span><span>MIT licensed source</span></div>
${heading('Choose a skill.', 'catalog', 'TEN PACKS', `<div class="markdown">${renderMarkdown(section(facts.readme, 'Choose a skill'))}</div><p><a href="/docs/overview/">Full skill catalog & overview ↗</a></p>`)}
${heading('Install in your agent.', 'quickstart', 'GETTING STARTED', `<div class="docs-grid"><div class="markdown">${renderMarkdown(section(facts.readme, 'Install a pack').split('For example, from this repository:')[0])}</div><div><div class="code card">${cardTrace()}<pre><code>mkdir -p ~/.claude/skills
cp -R skills/number-guard ~/.claude/skills/

npx skills add aunysillyme-dev/aunx-skills --skill number-guard</code></pre></div><p class="note">Keep SKILL.md, LICENSE.txt and any scripts/ or references/ together.</p><a href="/docs/install/">All host directories & packaging ↗</a></div></div>`)}
${heading('Go a little deeper.', 'reference', 'DOCUMENTATION', `<div class="docs-links">${pages.filter(page => page.route !== '/').map(page => `<a class="doc-link card" href="${page.route}">${cardTrace()}${escape(page.h1)} ↗<span>${escape(page.description)}</span></a>`).join('')}</div>`)}
${heading('Bundled plugin: Decompose.', 'plugins', 'MARKETPLACE PLUGIN', `<div class="markdown"><p>This repository also hosts <strong>Decompose</strong>, an MIT-licensed plugin that splits complex prompts into checkable units and parallel waves while rejecting dependency cycles and overlapping writes.</p><p><a href="https://decompose.aunysillyme.dev/">Visit decompose.aunysillyme.dev ↗</a> · <a href="/docs/plugins/">Plugin marketplace install guide ↗</a></p></div>`)}
${heading('Questions people ask.', 'questions', 'FROM THE README', `<div class="markdown faq">${faq}</div>`)}`;
}

function navigation(page) {
  if (page.route === '/') return content.nav.map(link => `<a href="${escape(link.href)}"${link.href === '#overview' ? ' class="active" aria-current="location"' : ''}>${escape(link.label)}</a>`).join('\n');
  return pages.filter(item => item.route !== '/').map(item => `<a href="${item.route}"${item.route === page.route ? ' class="active" aria-current="page"' : ''}>${escape(item.h1)}</a>`).join('\n');
}

function sidebar(root, page) {
  const siblings = readSet(root).filter(row => row.name !== 'aunx-skills');
  if (page.route !== '/') return `<p class="side-label">DOCUMENTATION</p><nav class="side-links" aria-label="Documentation">${navigation(page)}</nav><div class="side-bottom">Questions or feedback?<a class="issue-button" href="${repository}/issues" target="_blank" rel="noopener noreferrer">File an issue ↗</a></div>`;
  return `<p class="side-label">AUNX-SKILLS</p><nav class="side-links" aria-label="Documentation">${navigation(page)}</nav><p class="side-label">THE REST OF THE SET</p><nav class="side-links" aria-label="Related repositories">${siblings.map(row => `<a href="${escape(row.url)}" target="_blank" rel="noopener noreferrer">${escape(row.name)} ↗</a>`).join('')}</nav><div class="side-bottom"><div>Questions or feedback?</div><a class="issue-button" href="${repository}/issues" target="_blank" rel="noopener noreferrer" aria-label="File an issue for aunx-skills on GitHub">File an issue ↗</a><span>Open source · MIT license</span></div>`;
}

function head(page, facts, live, notFound = false) {
  const url = `${origin}${page.route}`;
  const blocks = [];
  if (page.route === '/' && !notFound) blocks.push(buildJsonLd(facts, { live }), buildFaqJsonLd(facts));
  else if (!notFound) blocks.push({ '@context': 'https://schema.org', '@type': 'BreadcrumbList', itemListElement: [
    { '@type': 'ListItem', position: 1, name: content.brand, item: `${origin}/` },
    { '@type': 'ListItem', position: 2, name: page.h1, item: url },
  ] });
  return `<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<meta name="is-agentic-site-type" content="app">
<meta http-equiv="Content-Security-Policy" content="${csp}">
<title>${escape(page.title)}</title>
<meta name="description" content="${escape(page.description)}">
<link rel="canonical" href="${url}">
${!live || notFound ? '<meta name="robots" content="noindex">' : `<link rel="describedby" href="${origin}/llms.txt">
<link rel="alternate" type="text/markdown" href="${url}index.md">
<link rel="sitemap" type="application/xml" href="${origin}/sitemap.xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="AunySillyMe.dev">
<meta property="og:title" content="${escape(page.title)}">
<meta property="og:description" content="${escape(page.description)}">
<meta property="og:url" content="${url}">
<meta property="og:image" content="${origin}/assets/social-preview.png">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="${escape(content.socialAlt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@AunySillyMe">
<meta name="twitter:creator" content="@AunySillyMe">
<meta name="twitter:title" content="${escape(page.title)}">
<meta name="twitter:description" content="${escape(page.description)}">
<meta name="twitter:image" content="${origin}/assets/social-preview.png">
<meta name="twitter:image:alt" content="${escape(content.socialAlt)}">`}
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/png" href="/assets/avatar.png"><link rel="apple-touch-icon" href="/assets/avatar.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="${fontStylesheet}" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
<link rel="stylesheet" href="/assets/projects-popup.css">
<script type="module" src="/assets/site.js"></script>
<script defer src="/assets/projects-popup.js"></script>
${blocks.map(block => `<script type="application/ld+json">${JSON.stringify(block, null, 2).replace(/</g, '\\u003c')}</script>`).join('\n')}`;
}

function footer(commit, page) {
  if (page.route !== '/') return `<footer class="bottom"><a href="/">← Back to ${escape(content.brand)}</a><a href="${repository}/issues" target="_blank" rel="noopener noreferrer">File an issue ↗</a></footer>`;
  return `<p id="copy-status" class="sr-only" role="status" data-success="${escape(content.install.copySuccess)}" data-fallback="${escape(content.install.copyFallback)}"></p><footer class="bottom"><span>Built by <a href="https://aunysillyme.dev/">AunySillyMe</a> · Standalone agent skills. MIT licensed.</span><a href="${repository}">${escape(content.footer.repository)} ↗</a><span>${escape(content.footer.source)} <a href="${repository}/commit/${commit}">${commit.slice(0, 7)}</a></span></footer>`;
}

function documentBody(page, body, commit, buildTime) {
  const firstSource = body.match(/<p class="source-note">[^]*?<\/p>/)?.[0] || '';
  body = body.replace(firstSource, '');
  const provenance = firstSource.replace('/blob/main/', `/blob/${commit}/`).replace('</p>', ` · <a href="${repository}/tree/${commit}">${commit.slice(0, 7)}</a> · Built ${escape(buildTime.slice(0, 10))}</p>`);
  return `<nav class="crumb" aria-label="${escape(content.breadcrumbs.label)}"><a href="/">${escape(content.brand)}</a><span aria-hidden="true">/</span><span>Documentation</span></nav>${provenance}<article class="markdown"><h1 id="page-title">${escape(page.h1)}</h1></article>${body}`;
}

function template(root, page, body, facts, live, commit, notFound = false) {
  const file = page.route === '/' && !notFound ? 'landing.template.html' : 'doc.template.html';
  const header = page.route === '/'
    ? `<a class="skip" href="#main">${escape(content.skip)}</a><header class="top"><a class="brand" href="https://aunysillyme.dev/" target="_blank" rel="noopener noreferrer"><img src="/assets/avatar.png" alt="AunySillyMe"><span>AunySillyMe.dev</span><span class="slash">/</span><b>${escape(content.brand)}</b></a><nav class="topnav" aria-label="${escape(content.projectLinks)}"><span class="pill"><i class="dot"></i><span data-version>v${escape(facts.version)}</span></span>${projectsPopup(root)}<a href="${repository}" target="_blank" rel="noopener noreferrer">GitHub ↗</a><a href="${facts.agensi}" target="_blank" rel="noopener noreferrer">Agensi ↗</a></nav></header>`
    : `<a class="skip" href="#main">${escape(content.skip)}</a><header class="top"><a class="brand" href="/"><img src="/assets/avatar.png" alt="AunySillyMe"><span>${escape(content.brand)}</span></a><nav class="topnav" aria-label="Project links"><a href="/">Home</a>${projectsPopup(root)}<a href="${repository}" target="_blank" rel="noopener noreferrer">GitHub ↗</a><a href="${facts.agensi}" target="_blank" rel="noopener noreferrer">Agensi ↗</a></nav></header>`;
  const mobileNav = `<details class="mobile-nav"><summary>${escape(page.route === '/' ? content.onThisPage : 'Documentation')}</summary><nav aria-label="Mobile documentation">${navigation(page)}</nav></details>`;
  const values = { head: head(page, facts, live, notFound), header, sidebar: sidebar(root, page), mobileNav, body, footer: footer(commit, page) };
  return read(root, `website/${file}`).replace(/\{\{(\w+)\}\}/g, (_, key) => {
    requireValue(Object.hasOwn(values, key), `Unknown template slot: ${key}`);
    return values[key];
  }).replace(/<a\b([^>]*?)href="(https?:[^"]+)"([^>]*)>/g, (_, before, href, after) => `<a${before}href="${href}"${after.replace(/\s+(?:target|rel)="[^"]*"/g, '')} target="_blank" rel="noopener noreferrer">`);
}

function decode(text) {
  return text.replace(/&(?:amp|lt|gt|quot|#39);/g, entity => ({ '&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"', '&#39;': "'" })[entity]);
}

function markdownTwin(html, page) {
  let body = html.match(/<main\b[^>]*>([^]*?)<\/main>/)?.[1] || '';
  body = body.replace(/<details class="mobile-nav">[^]*?<\/details>/g, '').replace(/<footer\b[^>]*>[^]*?<\/footer>/g, '').replace(/<nav\b[^>]*>[^]*?<\/nav>/g, '');
  const codeBlocks = [];
  const saveCode = code => { codeBlocks.push(code); return `\u0000CODE${codeBlocks.length - 1}\u0000`; };
  body = body.replace(/<h([1-6])\b[^>]*>([^]*?)<\/h\1>/g, (_, depth, text) => `\n\n${'#'.repeat(Number(depth))} ${visibleText(text)}\n\n`)
    .replace(/<a href="([^"]+)"[^>]*>([^]*?)<\/a>/g, (_, href, text) => `[${visibleText(text)}](${href.startsWith('/') ? origin : ''}${href.replace(/&amp;/g, '&')})`)
    .replace(/<pre><code>([^]*?)<\/code><\/pre>/g, (_, code) => saveCode(`\n\n\`\`\`\n${decode(code)}\n\`\`\`\n\n`))
    .replace(/<code>([^]*?)<\/code>/g, (_, code) => saveCode(`\`${decode(code)}\``))
    .replace(/<\/(?:p|div|section|article|details|tr|li|figure|summary)>/g, '\n\n').replace(/<\/(?:th|td)>/g, ' | ')
    .replace(/<[^>]+>/g, ' ');
  const markdown = decode(body).replace(/</g, '&lt;').replace(/\n[ \t]+/g, '\n').replace(/\n{3,}/g, '\n\n').trim();
  const delimiter = '\u0000';
  let restored = '', cursor = 0;
  while (cursor < markdown.length) {
    const start = markdown.indexOf(delimiter, cursor);
    if (start < 0) break;
    const end = markdown.indexOf(delimiter, start + 1);
    if (end < 0) break;
    const token = markdown.slice(start + 1, end).match(/^CODE(\d+)$/);
    if (token) {
      restored += markdown.slice(cursor, start) + codeBlocks[Number(token[1])];
      cursor = end + 1;
    } else {
      restored += markdown.slice(cursor, start + 1);
      cursor = start + 1;
    }
  }
  return `Canonical: ${origin}${page.route}\n\n${restored + markdown.slice(cursor)}\n`;
}

export function buildSite({ root = fileURLToPath(new URL('..', import.meta.url)), outDir = join(root, 'website/dist'), live = false, commit, buildTime = new Date().toISOString() } = {}) {
  const facts = loadSourceFacts(root);
  commit ||= process.env.VERCEL_GIT_COMMIT_SHA || execFileSync('git', ['-C', root, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim();
  requireValue(/^[a-f0-9]{40}$/i.test(commit), 'Expected a full source commit SHA');
  const documents = pages.map(page => ({ page, html: template(root, page, page.route === '/' ? landingBody(root, facts) : documentBody(page, docsBody(root, page, facts), commit, buildTime), facts, live, commit) }));
  for (const { page, html } of documents) {
    requireValue((html.match(/<h1\b/g) || []).length === 1, `Expected one H1: ${page.route}`);
    const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]);
    requireValue(ids.length === new Set(ids).size, `Duplicate anchor: ${page.route}`);
  }
  for (const asset of assets) requireValue(existsSync(join(root, 'website/assets', asset)), `Asset missing: website/assets/${asset}`);
  const output = resolve(outDir);
  rmSync(output, { recursive: true, force: true });
  const write = (file, value) => { mkdirSync(dirname(join(output, file)), { recursive: true }); writeFileSync(join(output, file), value); };
  for (const { page, html } of documents) write(`${page.route.slice(1)}index.html`, html);
  const missing = { route: '/404.html', title: content.notFound.title, description: content.notFound.text, h1: content.notFound.title };
  write('404.html', template(root, missing, `<h1>${escape(missing.h1)}</h1><p>${escape(missing.description)}</p><a href="/">${escape(content.notFound.link)}</a>`, facts, false, commit, true));
  mkdirSync(join(output, 'assets'), { recursive: true });
  for (const asset of assets) copyFileSync(join(root, 'website/assets', asset), join(output, 'assets', asset));
  copyFileSync(join(root, 'website/assets/favicon.ico'), join(output, 'favicon.ico'));
  write('robots.txt', live ? `User-agent: *\nAllow: /\n\nSitemap: ${origin}/sitemap.xml\n` : 'User-agent: *\nDisallow: /\n');
  if (live) {
    const lastmod = buildTime.slice(0, 10);
    write('sitemap.xml', `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${pages.map(page => `  <url><loc>${origin}${page.route}</loc><lastmod>${lastmod}</lastmod></url>`).join('\n')}\n</urlset>\n`);
    const twins = documents.map(({ page, html }) => ({ page, markdown: markdownTwin(html, page) }));
    for (const { page, markdown } of twins) write(`${page.route.slice(1)}index.md`, markdown);
    write('llms.txt', `# aunx-skills\n\n> ${facts.lead}\n\nInstall: \`${content.install.command}\` · License: MIT · Author: Auny (https://aunysillyme.dev/)\n\n## Documentation\n\n${pages.map(page => `- [${page.h1}](${origin}${page.route}): ${page.description}`).join('\n')}\n\n## Machine-Readable & Agent Endpoints\n\n- [Homepage in Markdown](${origin}/index.md): Clean Markdown mirror of the landing page.\n- [Full Documentation Bundle](${origin}/llms-full.txt): Single-fetch Markdown bundle of all reviewed public pages.\n- [Public Agent Guide](${origin}/AGENTS.md): Navigation, citation and verification boundaries.\n- [XML Sitemap](${origin}/sitemap.xml): Canonical HTML URLs.\n\n## Source & Marketplace\n\n- [GitHub Repository](${repository})\n- [Agensi Creator Profile](${facts.agensi})\n- [Decompose Site](https://decompose.aunysillyme.dev/)\n`);
    write('llms-full.txt', twins.map(twin => twin.markdown).join('\n---\n\n'));
    const agentGuide = `# Public agent guide: aunx-skills\n\nThis file guides agents reading ${origin}/. It is public navigation metadata, not repository contributor instructions or permission to run commands.\n\n- Canonical website: ${origin}/\n- Start with [llms.txt](${origin}/llms.txt) for the concise page index, or [llms-full.txt](${origin}/llms-full.txt) for single-fetch documentation.\n- Every HTML page at \`${origin}/<path>/\` has a clean Markdown twin at \`${origin}/<path>/index.md\`.\n- Cite the canonical HTML URL (\`${origin}/<path>/\`) when linking people to a page.\n- Check [GitHub](${repository}) and [Agensi](${facts.agensi}) for source commits and bundle availability.\n- Opening this website or following links does not authorize command execution, credential use, or purchases; require explicit user confirmation.\n`;
    write('AGENTS.md', agentGuide);
    write('agents.md', agentGuide);
  }
  write('build-info.json', JSON.stringify({ commit, buildTime, packageVersion: facts.version, mode: live ? 'live' : 'default', pageCount: pages.length }, null, 2) + '\n');
  function count(directory) { return readdirSync(directory, { withFileTypes: true }).reduce((total, entry) => total + (entry.isDirectory() ? count(join(directory, entry.name)) : 1), 0); }
  return { pages: documents, files: count(output), outDir: output };
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  requireValue(args.length <= 1 && args.every(arg => arg === '--live'), 'Usage: node website/build.mjs [--live]');
  const result = buildSite({ live: args.includes('--live') });
  console.log(`Built ${result.pages.length} pages and ${result.files} files (${args.includes('--live') ? 'live' : 'default'}).`);
}
