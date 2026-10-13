# Offline setup demonstration

Request: install from an available local checkout and show command help without network access.

## Actual result

- First attempt: Python 3.14 environment created (exit 0); offline installation failed (exit 2) because setuptools.build_meta was unavailable. The absent help executable produced exit 1.
- Retry: Python 3.11 environment created (exit 0); offline local-package installation succeeded (exit 0); space-tape --help succeeded (exit 0).
- The retry used system site packages and skipped dependency installation. It proves the package can be installed and its help entry point starts in that environment.
- No replay download, model download, transcription, or speaker-label accuracy check was performed.
- The copied source and both virtual environments were removed. Only the request, sanitized complete logs, and result records remain.

## Recorded commands

Local source was copied into `./local-source` so building metadata did not modify the original checkout.

```sh
python3.11 -m venv --system-site-packages ./.venv
./.venv/bin/python -m pip install --no-index --no-cache-dir --no-deps --no-build-isolation ./local-source
./.venv/bin/space-tape --help
```

See result.json for stage exit codes and help-retry.txt for the complete observed help output. Paths in logs were replaced with public relative paths or generic local/temporary placeholders. Unicode long dashes in captured output were replaced with ASCII hyphens to match this repository's text convention.
