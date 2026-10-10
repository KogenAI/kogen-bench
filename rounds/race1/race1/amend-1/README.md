# Race 1 input amendments

From the kogen-bench repository root, use the public archived inputs at [KogenAI/kogen-spec, 8e28fcf](https://github.com/KogenAI/kogen-spec/tree/8e28fcf) and [KogenAI/kogen-conformance, c53cccc](https://github.com/KogenAI/kogen-conformance/tree/c53cccc), followed by the patches in this directory to reproduce the exact files agents received.

These are tree diffs from the public bases. Check each patch before applying it.

```sh
git clone https://github.com/KogenAI/kogen-spec
git -C kogen-spec checkout 8e28fcf
git -C kogen-spec apply --check ../rounds/race1/race1/amend-1/kogen-spec.patch
git -C kogen-spec apply ../rounds/race1/race1/amend-1/kogen-spec.patch

git clone https://github.com/KogenAI/kogen-conformance
git -C kogen-conformance checkout c53cccc
git -C kogen-conformance apply --check ../rounds/race1/race1/amend-1/kogen-conformance.patch
git -C kogen-conformance apply ../rounds/race1/race1/amend-1/kogen-conformance.patch
```

The conformance patch adds the five cases and other changes present in the raced suite. For the scoring copy only, run `git -C kogen-conformance apply --check ../rounds/race1/race1/amend-1/kogen-conformance-scoring.patch`, then `git -C kogen-conformance apply ../rounds/race1/race1/amend-1/kogen-conformance-scoring.patch`. It adds the per-case working-directory sweep; do not apply it to an agent's input suite.

The public repositories remain unchanged. The patches and this note document the amended race inputs.
