# Kogen specification v1.2 — public snapshot

This directory is a locally sanitized, navigable **v1.2 clause-reference snapshot**. Its content baseline is [upstream revision 1118f7fc0dbb042af8c8de2ffd1b85768cf9e2a0](https://github.com/KogenAI/kogen-spec/tree/1118f7fc0dbb042af8c8de2ffd1b85768cf9e2a0). The upstream public-release revision used for publication sanitization is [30d9b25e4eefa7117121de44298fed504b429f4e](https://github.com/KogenAI/kogen-spec/commit/30d9b25e4eefa7117121de44298fed504b429f4e).

Personal filesystem locations, owner quotations, and internal attribution were removed or rewritten. Some editorial changes mean these published bytes are not claimed to be byte-identical to either upstream revision. [SOURCE.json](SOURCE.json) preserves the original source paths and hashes separately from the SHA-256 hashes of the bytes published here; [SHA256SUMS](SHA256SUMS) checks the published files.

## Included inventory

- Core v1.2 clauses: [CLI](01-cli.md), [formats](02-formats.md), [Build](03-build.md), [providers](04-provider.md), [sandbox custody](05-sandbox-custody.md), and [non-goals](06-non-goals.md).
- Conformance references: [v1.2 cases](CONFORMANCE-v1.2-CASES.md) and [conformance contract](CONFORMANCE.md).
- Public CLI command tree: [CLI-RULE.txt](CLI-RULE.txt).
- Clause classification: [Quint classification](quint/CLASSIFICATION.md).
- Normative data: [constants](data/constants.json), [lint rules](data/lint.json), [moved-command metadata](data/moved.json), and [YAML errors](data/yaml-errors.json).
- Exact CLI help pages: [kogen](data/help/kogen.txt), [version](data/help/kogen-version.txt), [status](data/help/kogen-status.txt), [intent](data/help/kogen-intent.txt), [intent shape](data/help/kogen-intent-shape.txt), [intent approve](data/help/kogen-intent-approve.txt), [intent remove](data/help/kogen-intent-remove.txt), [provider](data/help/kogen-provider.txt), [provider list](data/help/kogen-provider-list.txt), [provider login](data/help/kogen-provider-login.txt), [provider logout](data/help/kogen-provider-logout.txt), [provider use](data/help/kogen-provider-use.txt), [queue](data/help/kogen-queue.txt), [queue start](data/help/kogen-queue-start.txt), and [queue stop](data/help/kogen-queue-stop.txt).
- Provenance and published-byte integrity: [SOURCE.json](SOURCE.json) and [SHA256SUMS](SHA256SUMS).

## Omitted upstream material

This is a clause-reference excerpt, not a copy of the full upstream repository or its decision ledger. The upstream public-release revision removes the appendix reference, coverage and v1.2 drift notes, and review records from its public tree. Those historical/editorial files are not needed to resolve the clauses linked by EVIDENCE-MAP.md. The underlying decision ledger remains absent, so this snapshot does not establish comprehensive decision-to-clause coverage.

## Sources and precedence

1. The fixed public command tree is defined in [CLI-RULE.txt](CLI-RULE.txt); dated decisions in the v1.2 source clauses govern product rules.
2. Measurements inform success rate, speed, and cost; they remain distinct from normative product choices.
3. The specification records target contracts and deferred designs. A normative clause or conformance result does not establish an efficacy benefit.
4. The reference implementation supplies exact strings and constants where the sources above are silent.
