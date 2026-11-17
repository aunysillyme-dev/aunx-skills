const page = (key, route, h1, title, description, sources) => ({ key, route, h1, title, description, sources });
export const pages = [
  page('landing', '/', 'aunx-skills', 'aunx-skills | 10 Standalone Skills for AI Coding Agents', 'Ten MIT-licensed agent skills for Claude Code, Codex, Cursor and Gemini CLI: full output keeper, number guard, docs fetch ladder, rename sweep & more.', ['README.md', 'CREDITS.md']),
  page('overview', '/docs/overview/', 'Skill Catalog & Overview', 'Skill Catalog & Overview | aunx-skills', 'Compare all 10 standalone skills in aunx-skills: what each pack fixes, free vs Agensi bundle options, local helpers and MIT source rights.', ['README.md']),
  page('install', '/docs/install/', 'Install Skills', 'Install Skills for Claude, Codex & Gemini | aunx-skills', 'Copy individual skill folders or install via skills.sh and plugin marketplaces into Claude Code, Codex CLI, Cursor and Gemini CLI skill directories.', ['README.md']),
  page('plugins', '/docs/plugins/', 'Bundled Plugins', 'Bundled Plugins & Decompose Marketplace | aunx-skills', 'Install agent-native plugin bundles from aunx-skills, including the Decompose task planner for Claude Code, Codex CLI, Cursor and Gemini CLI.', ['README.md']),
  page('permissions', '/docs/permissions/', 'Runtime Permissions', 'Runtime Permissions & Local Helpers | aunx-skills', 'Review what runs locally across all 10 aunx-skills packs: markdown-only rules, the Python aunx-keep log helper, space-tape CLI and zero telemetry.', ['README.md', 'CREDITS.md']),
];
export default pages;
