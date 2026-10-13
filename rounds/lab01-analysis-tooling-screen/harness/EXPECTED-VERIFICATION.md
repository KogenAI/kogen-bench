# Expected values verification

Both independent standard-library computations produced byte-identical CSVs.
The projection and token input have 16 one-to-one joins and no zero finals.
The published race summary check passed (22 median/spread/difference fields across 2 languages).
The token-table median check passed (40 fields across 8 language-condition rows).

| File | Data rows | SHA-256 |
|---|---:|---|
| `tables.csv` | 8 | `8b83fe07e45e9e228a50a24b4e2468b61d6b82c740b1315fd47525b845551126` |
| `bootstrap.csv` | 14 | `c0603d0e007908ff773f6a13e5d7d966de59ddb5559556c8d76eb75cbebd8000` |
| `token_cost.csv` | 16 | `98f70caadb9184612c91ae3d73777dbb9dc8df849a7e9b06c175034b9bc4e443` |
| `plot_data.csv` | 16 | `d80b32fcef610d2746c38ac19383b4138b893d988ac70ecb6f7230f8a833d1bb` |

Bootstrap expectation uses the frozen min/max endpoint rule for two observations.
Seed: `20261011`. Quantile method recorded for generated outputs: `linear (Hyndman-Fan type 7)`.
