# L4 deterministic context packet

## Status

**DESCRIPTIVE**

### Why not VALID
- **POST_HOC_AMENDMENT:** Amendment 1 was written after 6 of 12 packet outcomes were known.
- **CONDITIONS_MISMATCH:** The US controls were not interleaved with packet cells.
- **relabelled 2026-10-08 after scrutiny:** Previously labelled VALID; the README documents a post-result amendment and non-interleaved controls.


STATUS: **DESCRIPTIVE**

<!-- L4-COMPUTED:BEGIN -->
Pre-registered: yes; original design frozen 7 October 2026 before the first scored packet cell. Amendment 1 was written after 6 of 12 packet outcomes were known; its disclosure is retained in the decision rule.
Label: descriptive pilot; n=3 per arm per variant. The thresholds are coarse and support no general claim.
Question: Do frozen public context packets increase official full-suite passes over same-seed contemporaneous no-packet controls on four L1-admitted variants?
n: 24 official scored cells (12 packet, 12 control; 4 variants × 3 seeds per arm); 20 historical cells are context only.
Headline (descriptive; not a validated registered finding): observed **KEEP** for packets in specification sections 3.2 and 4.9: packet-minus-control = +6 passes, 6 paired rescues, 0 losses, and no regression. The US controls were not interleaved.
Configuration: direct Codex, `gpt-6-luna` at `max`, 3,600-second cap, zero retries; Elixir and Rust on EU, Go on US; official `r70-macbook-window-v1` grades. Tokens are uncached input + cached input + output; total is their sum.
Official runner wrapper: Codex 0.159.3, SHA-256 `08019d8aab7c15481f6d14126645eebd7b2c2c98025f94118baeee2167e4a300`; this same fingerprint appears on all scored cells.
Limit: outcome-selected tasks, n=3 per arm per variant, coarse thresholds, and mixed scheduling; the result supports no general claim.

| Lifecycle count | Count |
| --- | ---: |
| Planned scored cells | 24 |
| Started scored cells | 24 |
| Finished scored cells | 24 |
| Officially graded scored cells | 24 |
| ITT denominator for scored cells | 24 |
<!-- L4-COMPUTED:END -->

Sources: [decision rule and Amendment 1](DECISION-RULE.md), [results](RESULTS.md), [paired-cell data](data/paired-cells.csv), [historical baseline data](data/historical-baselines.csv), and [reproducer](reproduce/l4-context-packet.py).

## Reproduce

### Public base revisions

| Packet task | Source public base | Packet public base |
| --- | --- | --- |
| `r70-2-elixir-l4pk` | [470ba65c1d3c19191a2190a032cd9ebf24e71975](https://github.com/KogenAI/kogen-ex/commit/470ba65c1d3c19191a2190a032cd9ebf24e71975) | [08a1ca88b8dfd67760586f433fc773a6b23842bb](https://github.com/KogenAI/kogen-ex/commit/08a1ca88b8dfd67760586f433fc773a6b23842bb) |
| `r70-2-go-l4pk` | [13a08875ea5e1fd0a3debc6f0b8c6b98a4b37a82](https://github.com/KogenAI/kogen-ex/commit/13a08875ea5e1fd0a3debc6f0b8c6b98a4b37a82) | [8b8c92e8d0f09d406f328e5426c839b8a47fe2a2](https://github.com/KogenAI/kogen-ex/commit/8b8c92e8d0f09d406f328e5426c839b8a47fe2a2) |
| `r70-4-elixir-fe2-l4pk` | [5ccd0bf1e816e2b2f5b2694861f8596402409f52](https://github.com/KogenAI/kogen-ex/commit/5ccd0bf1e816e2b2f5b2694861f8596402409f52) | [8f85ca4d634373c2417a1f16e7649e031e8f7027](https://github.com/KogenAI/kogen-ex/commit/8f85ca4d634373c2417a1f16e7649e031e8f7027) |
| `r70-7-rust-l4pk` | [111a0c776ae6d93f6e7fccd3fc694d5f4fa26838](https://github.com/KogenAI/kogen-ex/commit/111a0c776ae6d93f6e7fccd3fc694d5f4fa26838) | [6e5af6a2e14c8f64eb88ced5d04a223bcd2c4b94](https://github.com/KogenAI/kogen-ex/commit/6e5af6a2e14c8f64eb88ced5d04a223bcd2c4b94) |

Kogen commit: source `470ba65c1d3c19191a2190a032cd9ebf24e71975` and packet `08a1ca88b8dfd67760586f433fc773a6b23842bb` are exact linked examples; all per-task source and packet SHAs are listed above.

Harness commit: not recorded as a Git commit in the official aggregate grade rows. The lane dispatcher SHA-256 is `f23824e32fb74f42e95e3a0c106df4070fac5425b9c8981dfbd293859acfdfee`; the common wrapper fingerprint recorded on all scored rows is SHA-256 `08019d8aab7c15481f6d14126645eebd7b2c2c98025f94118baeee2167e4a300`.

Model and effort: direct Codex, `gpt-6-luna` at `max`; official grade route `r70-macbook-window-v1`; 3,600-second cap and zero retries. The lane handoff lists worker Codex CLI pin `0.160.0` and Python `3.14.7`. Packet authoring used `codex-cli 0.160.1` in an ephemeral public-only workspace. The reported runner wrapper version and fingerprint appear in the CSV-backed summary above.

Task IDs: packet tasks `r70-2-elixir-l4pk`, `r70-2-go-l4pk`, `r70-4-elixir-fe2-l4pk`, and `r70-7-rust-l4pk`; control tasks `r70-2-elixir`, `r70-2-go`, `r70-4-elixir-fe2`, and `r70-7-rust`. Exact cell IDs, reps, and seeds are in the paired-cell CSV.

Historical execution command: not recorded as a shell transcript. Reproduction command, run from the SOT repository root:

```sh
python3 rounds/l4-context-packet/reproduce/l4-context-packet.py
```

The script uses only the standard library and checks every reported outcome number against `rounds/l4-context-packet/data/paired-cells.csv` and `rounds/l4-context-packet/data/historical-baselines.csv`.

Raw records: these two CSV files contain the latest official aggregate row for each exact scored cell ID and the registered historical baseline cell IDs. The token total per cell is uncached input + cached input + output; arm totals sum all cell totals.
