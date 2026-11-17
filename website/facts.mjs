import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

export const rootDir = fileURLToPath(new URL('..', import.meta.url));
export const visibleText = value => String(value).replace(/<[^>]*>/g, '').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'");

export function section(markdown, heading) {
  const lines = markdown.split('\n');
  const start = lines.findIndex(line => line === `## ${heading}`);
  if (start < 0) throw Error(`Missing source section: ${heading}`);
  let end = start + 1;
  while (end < lines.length && !lines[end].startsWith('## ')) end++;
  return lines.slice(start, end).join('\n').trim();
}

export function loadSourceFacts(root = rootDir) {
  const read = file => readFileSync(join(root, file), 'utf8').replace(/\s*\u2014\s*/g, ', ');
  const readme = read('README.md');
  const credits = read('CREDITS.md');
  const market = JSON.parse(read('.claude-plugin/marketplace.json'));
  const version = market.metadata?.version || market.plugins?.[0]?.version || '1.0.1';
  const lead = readme.split('\n\n').find(text => text.startsWith('Ten standalone agent skills'));
  if (!lead) throw Error('README introduction missing');
  const questions = section(readme, 'Questions people ask');
  const faq = [...questions.matchAll(/^### (.+)\n\n([^]*?)(?=\n### |$)/gm)].map(match => ({ question: match[1], answerMarkdown: match[2].trim() }));
  return {
    name: 'aunx-skills',
    version,
    description: 'Ten MIT-licensed agent skills for Claude Code, Codex, Cursor and Gemini CLI: full output keeper, number guard, docs fetch ladder, rename sweep & more.',
    lead,
    faq,
    readme,
    credits,
    agensi: 'https://agensi.io/creators/aunysillyme',
    repository: 'https://github.com/aunysillyme-dev/aunx-skills'
  };
}

export function buildJsonLd(facts, { live = false } = {}) {
  if (!live) {
    return {
      '@context': 'https://schema.org',
      '@type': 'SoftwareApplication',
      name: 'aunx-skills',
      description: facts.description,
      applicationCategory: 'DeveloperApplication',
      softwareRequirements: 'Markdown-capable AI coding agent; Python 3.9+ for local helpers',
      license: 'https://spdx.org/licenses/MIT.html',
      url: 'https://aunx-skills.aunysillyme.dev/'
    };
  }
  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'SoftwareSourceCode',
        '@id': 'https://aunx-skills.aunysillyme.dev/#source',
        name: 'aunx-skills',
        description: facts.description,
        url: 'https://aunx-skills.aunysillyme.dev/',
        codeRepository: facts.repository,
        programmingLanguage: ['Markdown', 'Python'],
        runtimePlatform: 'Claude Code, Codex CLI, Cursor, Gemini CLI',
        version: facts.version,
        license: 'https://spdx.org/licenses/MIT.html',
        author: { '@id': 'https://aunysillyme.dev/#person' },
        sameAs: [facts.repository, facts.agensi]
      },
      {
        '@type': 'SoftwareApplication',
        '@id': 'https://aunx-skills.aunysillyme.dev/#software',
        name: 'aunx-skills',
        description: facts.description,
        url: 'https://aunx-skills.aunysillyme.dev/',
        applicationCategory: 'DeveloperApplication',
        operatingSystem: 'macOS, Linux, Windows',
        softwareRequirements: 'Markdown-capable AI coding agent; Python 3.9+ for local helpers',
        softwareVersion: facts.version,
        isAccessibleForFree: true,
        license: 'https://spdx.org/licenses/MIT.html',
        offers: { '@type': 'Offer', price: '0', priceCurrency: 'USD' },
        author: { '@id': 'https://aunysillyme.dev/#person' },
        sameAs: [facts.repository, facts.agensi]
      },
      {
        '@type': 'Person',
        '@id': 'https://aunysillyme.dev/#person',
        name: 'Auny Hossain',
        alternateName: ['Auny', 'AunySillyMe'],
        url: 'https://aunysillyme.dev/',
        sameAs: [
          'https://www.aunysillyme.com/#person',
          'https://aunysillyme.com/',
          'https://github.com/aunysillyme',
          'https://github.com/aunysillyme-dev',
          'https://www.npmjs.com/~aunysillyme',
          'https://x.com/AunySillyMe'
        ]
      }
    ]
  };
}

export function buildFaqJsonLd(facts) {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: facts.faq.map(row => ({
      '@type': 'Question',
      name: row.question,
      acceptedAnswer: { '@type': 'Answer', text: row.answerMarkdown.replace(/`|\*\*/g, '') }
    }))
  };
}
