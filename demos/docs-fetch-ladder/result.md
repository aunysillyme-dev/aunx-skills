# Actual demo result

For HTTP 429 responses, the sample API guide says to wait for the duration in `Retry-After`. When that header is absent, use exponential backoff with jitter and stop after three retry attempts. Retry idempotent operations, or include an idempotency key. See the [retry guide](https://docs.example.test/docs/guides/retries.md).

Send the API key in the `Authorization` header using the Bearer scheme. Keep it out of URLs and query strings. See the [authentication guide](https://docs.example.test/docs/guides/authentication.md).

Retrieval: the two index locations were read in one parallel batch. The root index returned 200 and listed both Markdown guides. The alternate index returned 404. The two selected guides were read in a second parallel batch, and each returned 200. Both requested topics were covered, so retrieval stopped at the Markdown rung.

Served by: index discovery + Markdown.

Transport: local synthetic fixtures mapped to example URLs. No network requests were made. Live HTTP, crawling, and hosted scraping were not tested. The linked domain is illustrative and is not a live documentation source.

Evidence: `retrieval-trace.json` records each actual response and its body. `aunx_demo_fetch.py` implements the local transport, and `fixtures/` holds the synthetic input documentation.
