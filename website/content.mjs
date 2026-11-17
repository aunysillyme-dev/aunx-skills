import { loadSourceFacts } from './facts.mjs';
const facts = loadSourceFacts();
export const content = {
  brand: 'aunx-skills',
  eyebrow: 'TEN STANDALONE AGENT SKILLS',
  headline: 'Fix what agents quietly get wrong.',
  headlineAccent: 'Logs, math, docs fetch, renames and rule gates.',
  heroLede: facts.lead,
  install: {
    command: 'npx skills add aunysillyme-dev/aunx-skills --skill number-guard',
    copy: 'Copy install command',
    copySuccess: 'Install command copied.',
    copyFallback: 'Select the install command to copy it.'
  },
  nav: [
    { label: 'Overview', href: '#overview' },
    { label: 'Skill catalog', href: '#catalog' },
    { label: 'Install', href: '#quickstart' },
    { label: 'Documentation', href: '#reference' },
    { label: 'Plugins', href: '#plugins' },
    { label: 'Questions', href: '#questions' }
  ],
  docsLabel: 'DOCUMENTATION',
  onThisPage: 'On this page',
  projectLinks: 'Project links',
  skip: 'Skip to content',
  sourceLabel: 'From',
  footer: { repository: 'View on GitHub', source: 'Source' },
  breadcrumbs: { label: 'Breadcrumb' },
  socialAlt: 'aunx-skills: ten standalone agent skills for Claude Code, Codex, Cursor and Gemini CLI.',
  notFound: { title: 'Page not found', text: 'Open the overview or choose a page from the documentation.', link: 'Open the overview' }
};
export default content;
