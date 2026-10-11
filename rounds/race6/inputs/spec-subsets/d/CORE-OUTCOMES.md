## OUTCOMES

The questions-only exit code is unscored in race 3.

The table fixes command outcomes. Status names refer to the lifecycle or diagnostic category;
where a case does not inspect a status row or text, that limitation is stated. A required
text token is a literal substring, not a requirement to reproduce the entire diagnostic.

| Situation | Exit code | Status | Required text token |
|---|---:|---|---|
| Absolute Build deadline expires | 1 | `failed` (Build model; status row not asserted) | None asserted |
| Candidate is tampered with before the final recheck | 1 | `failed` (landing model; status row not asserted) | None asserted |
| Invalid project config | 3 | `environment/project_config_invalid`; no Intent status asserted | `environment/project_config_invalid` on stdout in diagnostic cases |
| Could-not-check because a check times out | 1 | `blocked` (Intent); check result `could-not-check` | `could-not-check` on stdout |
| Questions-only shape, Quint fixture (unscored) (unscored) | 5 | `questions`; no Intent or acceptance source | `Choose the greeting language?` on stdout |
| Questions-only shape, Gherkin fixture (unscored) (unscored) | 0 | Questions only; no Intent or acceptance source | `tone` on stdout |
| User pre-commit hook rejects landing | 1 | `failed` (landing model; status row not asserted) | `landing-hook-denied` on stderr in the Quint hook case; no text asserted by the Gherkin case |

Sources: `conformance/cases/quint/build/trace-20271011.itf.json` (deadline),
`conformance/cases/quint/landing/trace-20273013.itf.json` (tampering),
`conformance/cases/quint/config/trace-20264016.itf.json`, `trace-20264017.itf.json`
and `trace-20264047.itf.json` (invalid-config diagnostics),
`conformance/cases/quint/shape/trace-20269010.itf.json` (questions), and
`conformance/cases/quint/landing/trace-20273011.itf.json` (hook).
The source Gherkin scenarios in `conformance/features-src/04-lifecycle.feature`
supply the timeout status/token and the conflicting questions exit;
`conformance/features-src/07-commits.feature` supplies hook exit 1.

The questions-only exit expectations conflict (5 versus 0); neither value is a resolved
universal rule. Other invalid-config cases assert exit 3 without asserting diagnostic text.
All three Build/landing failures above leave the target unpublished; timeout cannot land.
