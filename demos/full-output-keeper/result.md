# Actual demo result

To run a fresh capture and read it back, create a temporary cache directory:

```sh
CACHE=$(mktemp -d)
AUNX_KEEP_CACHE="$CACHE" python3 skills/full-output-keeper/scripts/aunx-keep.py --head 3 -- python3 demos/full-output-keeper/diagnostic.py
AUNX_KEEP_CACHE="$CACHE" python3 skills/full-output-keeper/scripts/aunx-keep.py read <ID> --grep ERROR
```

Command exit: **7**. The head view showed lines 1-3 of 14. Retrieval id: `e44982caaf23448fb3d7487b5a981d54`. Full retrieval matched all original bytes.

Search returned `12:ERROR missing icon: checkout.svg`. The hidden error is on original line 12. `--lines 11:13` returned the adjacent context.

Artifacts: `short-view.txt`, `full-output.txt`, `error-match.txt`, `range.txt`.
