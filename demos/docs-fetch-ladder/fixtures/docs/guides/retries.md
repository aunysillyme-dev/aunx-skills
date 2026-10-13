# Retries

When the sample API returns HTTP 429, read the `Retry-After` response header and wait the indicated duration before retrying. If that header is absent, use exponential backoff with jitter and stop after three retry attempts. Retry only idempotent operations or operations that include an idempotency key.
