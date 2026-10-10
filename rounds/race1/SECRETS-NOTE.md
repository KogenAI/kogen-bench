# Synthetic test credentials

The suite contains synthetic test credentials (a fake key and unsigned tokens for a fake provider); they grant no access anywhere. The race 1 secret scan found no credential-shaped strings. The test token fixtures and fake provider implementation are:

- `race1/suite/cases/provider/provider-19-expired-injected-jwt.json`
- `race1/suite/kogen_conformance/fake_server.py`
- `race1-gleam/suite/cases/provider/provider-19-expired-injected-jwt.json`
- `race1-gleam/suite/kogen_conformance/fake_server.py`
