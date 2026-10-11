# Withheld spec trees

The primary tree is the exact B/C/D-only files removed from the condition subsets, with paths relative to the spec-subsets root: b/…, c/…, d/…. Condition A contributes no withheld files. B has 161, C has 8, and D has 232 withheld files. The source copies were byte-verified before hashing. Both Elixir and Go received the same condition subset; the shared prose exports preserve that relationship.

File count: 401
SHA-256: 06c56ea4cc4b01d7cc2e2a7b86d1be908aecf19f092d57014371e4ca3332c02b

The deduplicated union is D minus the 15 PROSE files, with original spec-relative paths. The per-file path/class/hash manifest remains withheld to avoid exposing suite inventory details.

Unique file count: 232
Unique tree SHA-256: 0464b2aa57f6f9c1597ec4b6081beeb3741191e3c80581fe76de3a5f2609b616

Both receipts use exactly this recipe, executed with the working directory at the stated tree root; the tree includes only withheld files, with no receipt or manifest inside it:

```sh
LC_ALL=C find . -type f -print0 | LC_ALL=C sort -z | xargs -0 shasum -a 256 | shasum -a 256
```

Hashes commit to original source bytes and relative filenames. They are not hashes of the sanitized public prose. Private staging preserves the two exact roots; no suite payload is in publish/. The complete suite, runner, per-file split manifest, hidden inventory and case-hash lists remain excluded separately.
