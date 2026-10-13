# Actual demo result

Command: `AUNX_KEEP_CACHE=demos/full-output-keeper/cache python3 skills/full-output-keeper/scripts/aunx-keep --head 3 -- python3 demos/full-output-keeper/diagnostic.py`

Command exit: **7**. The head view showed lines 1-3 of 14. Retrieval id: `e44982caaf23448fb3d7487b5a981d54`. Full retrieval matched all original bytes.

Search returned `12:ERROR missing icon: checkout.svg`. The hidden error is on original line 12. `--lines 11:13` returned the adjacent context.

Artifacts: `short-view.txt`, `full-output.txt`, `error-match.txt`, `range.txt`.
