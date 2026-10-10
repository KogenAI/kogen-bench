# Assembly manifest-aware deduplication

Reran t2_dedupe.py after T1. Ignore id/seed, including the seed tokens in itf_file, command_line and witnesses. Preserve every other manifest field, notably all fixtures, tools/seams, fake scripts/digests and limits.

- Drop quint.approve.seed-20270013: duplicate of quint.approve.seed-20270012; manifests equal apart from id/seed.
- Drop quint.approve.seed-20270015: duplicate of quint.approve.seed-20270014; manifests equal apart from id/seed.
- Drop quint.build.seed-20271014: duplicate of quint.build.seed-20271010; manifests equal apart from id/seed.
- Drop quint.build.seed-20271016: duplicate of quint.build.seed-20271013; manifests equal apart from id/seed.
- Drop quint.build.seed-20271017: duplicate of quint.build.seed-20271013; manifests equal apart from id/seed.
- Drop quint.check.seed-20272014: duplicate of quint.check.seed-20272010; manifests equal apart from id/seed.
- Drop quint.check.seed-20272015: duplicate of quint.check.seed-20272010; manifests equal apart from id/seed.
- Drop quint.check.seed-20272017: duplicate of quint.check.seed-20272010; manifests equal apart from id/seed.
- Drop quint.check.seed-20272012: duplicate of quint.check.seed-20272011; manifests equal apart from id/seed.
- Drop quint.git.seed-20262014: duplicate of quint.git.seed-20262012; manifests equal apart from id/seed.
- Drop quint.init.seed-20267014: duplicate of quint.init.seed-20267011; manifests equal apart from id/seed.
- Drop quint.intent.seed-20268011: duplicate of quint.intent.seed-20268010; manifests equal apart from id/seed.
- Drop quint.intent.seed-20268012: duplicate of quint.intent.seed-20268010; manifests equal apart from id/seed.
- Drop quint.intent.seed-20268013: duplicate of quint.intent.seed-20268010; manifests equal apart from id/seed.
- Drop quint.intent.seed-20268014: duplicate of quint.intent.seed-20268010; manifests equal apart from id/seed.
- Drop quint.intent.seed-20268015: duplicate of quint.intent.seed-20268010; manifests equal apart from id/seed.
- Drop quint.intent.seed-20268016: duplicate of quint.intent.seed-20268010; manifests equal apart from id/seed.
- Drop quint.intent.seed-20268017: duplicate of quint.intent.seed-20268010; manifests equal apart from id/seed.
- Drop quint.landing.seed-20273014: duplicate of quint.landing.seed-20273010; manifests equal apart from id/seed.
- Drop quint.landing.seed-20273015: duplicate of quint.landing.seed-20273010; manifests equal apart from id/seed.
- Drop quint.landing.seed-20273016: duplicate of quint.landing.seed-20273010; manifests equal apart from id/seed.
- Drop quint.landing.seed-20273017: duplicate of quint.landing.seed-20273010; manifests equal apart from id/seed.
- Drop quint.process.seed-20263014: duplicate of quint.process.seed-20263012; manifests equal apart from id/seed.
- Drop quint.process.seed-20263016: duplicate of quint.process.seed-20263013; manifests equal apart from id/seed.
- Drop quint.process.seed-20263017: duplicate of quint.process.seed-20263013; manifests equal apart from id/seed.
- Drop quint.queue.seed-20274012: duplicate of quint.queue.seed-20274010; manifests equal apart from id/seed.
- Drop quint.queue.seed-20274013: duplicate of quint.queue.seed-20274010; manifests equal apart from id/seed.
- Drop quint.queue.seed-20274014: duplicate of quint.queue.seed-20274010; manifests equal apart from id/seed.
- Drop quint.queue.seed-20274016: duplicate of quint.queue.seed-20274010; manifests equal apart from id/seed.
- Drop quint.queue.seed-20274017: duplicate of quint.queue.seed-20274010; manifests equal apart from id/seed.
- Drop quint.queue.seed-20274015: duplicate of quint.queue.seed-20274011; manifests equal apart from id/seed.
- Drop quint.recovery.seed-20266013: duplicate of quint.recovery.seed-20266010; manifests equal apart from id/seed.
- Drop quint.recovery.seed-20266015: duplicate of quint.recovery.seed-20266014; manifests equal apart from id/seed.
- Drop quint.shape.seed-20269013: duplicate of quint.shape.seed-20269011; manifests equal apart from id/seed.
- Drop quint.shape.seed-20269017: duplicate of quint.shape.seed-20269016; manifests equal apart from id/seed.
- Drop quint.status.seed-20265015: duplicate of quint.status.seed-20265013; manifests equal apart from id/seed.
- Drop quint.status.seed-20265016: duplicate of quint.status.seed-20265013; manifests equal apart from id/seed.
- Drop quint.status.seed-20265017: duplicate of quint.status.seed-20265013; manifests equal apart from id/seed.

Accepted duplicate exclusions: 38; retained pairs with differing manifests: 0.
