# Kogen Bench credits

Kogen Bench thanks 37signals LLC for the Fizzy, Fizzy SaaS, and Writebook code used in Rails task bases. Reference patches may have a separate source, recorded per task. Fizzy and Fizzy SaaS are distributed under the O’Saasy License; Writebook is distributed under the MIT License. Their full copyright and licence notices are preserved in [LICENSES/](LICENSES/).

Kogen Bench also thanks the Rails Foundation for commissioning [Agents on Rails](https://github.com/rails/ai-evals), built by Evil Martians. Forty-two Rails task records reuse its ideas, prompts, verification tests, and reference patches under MIT; two local activity-feed variants reuse the original activity-feed task’s test and patch with adapted prompts. Every credited task record names the upstream path and pinned commit, separates Agents on Rails materials from the Fizzy base and feature attribution, and records whether prompt text was adapted. The Rails Foundation MIT notice is preserved in [LICENSES/RAILS-AI-EVALS-MIT.txt](LICENSES/RAILS-AI-EVALS-MIT.txt).

The per-task comparison, including verification-test SHA-256 values, is recorded in [RAILS-AI-EVALS-COMPARISON.md](RAILS-AI-EVALS-COMPARISON.md). It contains no hidden test contents.

## Verified upstream feature authors

The following names are the commit-matched authors recorded for the corresponding feature lineage. The task references do not claim these authors wrote the benchmark prompts or graders.

- Jason Zimdars — https://github.com/basecamp/fizzy/commit/dc9b31b6e69c2e55fcb54510dcc60f0b8b3763a7 (task lineage: `rails-ft-web-push-device-delivery`).
- Jorge Manrubia — https://github.com/basecamp/fizzy/commit/41905068c0c1a89d001d6bbad20305bbe06ab9ca (task lineage: `rails-ft-notification-bundle-window-overlap`).
- Jorge Manrubia — https://github.com/basecamp/fizzy/commit/872537f02ca8e110610ceec10f5854627489b871 (task lineage: `elx-port-board-publish-unpublish-public-boundary`, `rails-ft-board-publish-unpublish-public-boundary`).
- Kevin McConnell — https://github.com/basecamp/fizzy/commit/e16cc21b0ad614a223d43edca1717e76e2b8f8d4 (task lineage: `rails-ft-data-export-and-import`).
- Mike Dalessio — https://github.com/basecamp/fizzy/commit/cb61b36715ac21fb06c544b1c1409d3c6044241a (task lineage: `rails-ft-card-reactions`).
- Mike Dalessio — https://github.com/basecamp/fizzy/commit/fe6df7085fa938cc15b5a802c31706893463312b (task lineage: `rails-ft-account-id-rollout`).
- Rob Zolkos — https://github.com/basecamp/fizzy/commit/6a71856b3de415027b48e9fcfda786ffa3cf7e95 (task lineage: `rails-ft-activity-feed-api`, `rails-ft-activity-feed-api-v2`, `rails-ft-activity-feed-api-v3`).

## Other credited sources

- **37signals LLC** — Fizzy project and its O’Saasy-licensed base; Writebook project and its MIT-licensed base. Project links: [Fizzy](https://github.com/basecamp/fizzy), [Writebook](https://github.com/basecamp/writebook).
- **Kogen Bench task set** — task-specific origins, prompt changes, grader sources, and reference solutions are recorded in each task’s `credits` object.
- **Kogen Bench harness bases** — bundle history identifies the Trackline, Beltway, Elixir port fixtures, and R70 fixture commits credited to Optimum Tech under Apache-2.0. Each linked task record includes the bundle, commit, author line, and date used as evidence.
- **Tally and unresolved task bases** — authorship or exact base revision is not established by the published bundle metadata. Their permission-needed flags remain in the task records.
- **37signals LLC** — Writebook is the base project for the Rails `hello-world` task, with task and benchmark materials credited to Agents on Rails as recorded in that task’s `credits` object.

Credits distinguish the task base, feature idea, and tests/grader because their sources can differ. A named upstream author is listed only when a matching upstream commit is recorded. See each `tasks/*/task.json` for its evidence, confidence, and redistribution terms.
