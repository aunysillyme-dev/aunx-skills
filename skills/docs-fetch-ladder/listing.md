## Name

Docs Fetch Ladder: Read API Docs with llms.txt First

## Summary

Give your agent a clear path from documentation indexes to readable source pages, with a note showing how each page was fetched.

## Price

Free ($0). Also included in the ten-skill bundle priced at $7.99.

## Full description

When you ask an agent to read API documentation, it can reach for a crawler before checking whether the site already serves a useful index or clean Markdown. Docs Fetch Ladder gives it an ordered workflow: check `/llms.txt` and `/docs/llms.txt`, read relevant `.md` pages, try a plain page fetch, then use a crawler if needed. A hosted scraper is the final rung.

This skill is for developers, technical researchers, and anyone who asks an agent to read a vendor's docs. After installation, the agent has instructions to batch independent reads, check what each response contains, stop when the needed content is usable, and show which rung supplied the answer. It works with the fetch tools you already provide. Crawl4AI is named as one optional crawler.

The download contains agent instructions and a license. You supply the agent and any retrieval tools. Availability, site access, and live documentation coverage depend on those tools and the target website.

## Use cases

- Read an API guide using links from a site's llms.txt index.
- Fetch Markdown versions of integration documentation.
- Collect several independent reference pages in one batch.
- Move to a plain page fetch when a Markdown URL is unavailable.
- Explain why a crawler or hosted scraper was needed for a page.

## Demo request

"Read the documentation at the sample domain and explain how the API retries rate-limited requests and where the API key goes. Use only local fixtures, save the retrieval trace, and report the serving rung."

The run used synthetic documentation in `demos/docs-fetch-ladder/fixtures/` through a local URL-to-file transport. It did not access the network.

## Demo result

The actual run read both index locations in parallel: the root index returned 200, and the alternate index returned 404. It selected the retry and authentication Markdown links from the root index and read both in a second parallel batch. Both returned 200.

The answer explained the fixture's `Retry-After` handling, exponential backoff with jitter, three-retry limit, idempotency condition, and Bearer authorization header. It reported `Served by: index discovery + Markdown` and stopped there. The request, fixture inputs, actual response bodies, and final answer are saved under `demos/docs-fetch-ladder/`.

This demonstrates the ladder's index and Markdown selection on local fixtures. Live HTTP fetching, crawling, and hosted scraping were not tested.

## FAQ

### What is llms.txt and how does it help an AI read docs?

It is a Markdown documentation index convention that can point an agent to relevant pages. The skill checks the two common locations before selecting content pages.

### How do I make my agent read API docs before crawling?

Install this skill and give the agent the documentation URL and your question. The workflow starts with index discovery and Markdown pages, using the fetch tools available in your agent.

### Does every documentation website have llms.txt?

No. When both index locations are unavailable, the agent continues with known page URLs and the next appropriate rung. A missing index does not mean the documentation is missing.

### What if the documentation URL does not have a Markdown version?

The agent tries the plain page next. If that fetch cannot supply the content, it can use an available crawler.

### Do I need Crawl4AI to use this skill?

No. Crawl4AI is one named crawler option. Your agent can use another available crawler after the plain-page rung.

### When does the agent use a hosted scraper?

It uses one only as the final rung when the crawler fails, supplies no useful content, or lacks a needed capability, and the action fits your permissions and budget.

### Does this skill install tools or make network calls itself?

No. It provides instructions. An agent following it may use your existing tools to fetch authorized URLs; those tools control network access and any charges.

## Keywords

llms.txt, read API docs, AI documentation retrieval, Markdown documentation, docs scraping, fetch documentation, Crawl4AI, agent web research, documentation index, plain page fetch, crawler fallback, hosted scraper, batch URL fetch

## Tags

ai-agents, documentation, developer-tools, research, automation

## Compatibility

Claude Code, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Provide an HTTP or page-reading tool for live retrieval. Crawler and hosted-scraper tools are optional fallbacks. Exact skill discovery and tool availability depend on your agent installation.

## Permissions notes

Reads: the user's question, authorized documentation indexes, and selected pages. Writes: an answer and retrieval notes, plus source files only when the user requested saved output. Runs: existing fetch or crawler tools when the agent needs them. This instruction-only pack makes no network calls of its own. Agents following it may fetch websites with available tools; hosted tools may charge for use.

## Credits

- [llms.txt](https://github.com/AnswerDotAI/llms-txt) by **AnswerDotAI**, Apache-2.0: the index convention behind the first rung.
- [Crawl4AI](https://github.com/unclecode/crawl4ai) by **unclecode**, Apache-2.0: the optional crawler and Markdown output modes.

Workflow guidance is original. No upstream code is bundled. This pack is distributed under the MIT license by Auny LLC and contributors.

## Repo link

https://github.com/aunysillyme-dev/aunx-skills/tree/main/skills/docs-fetch-ladder
