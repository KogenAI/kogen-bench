All patches are unified diffs against Fizzy commit `8112b3dbafeea72225c1ed09ae170e8cbe2d1195` and are intended to be applied at the repository root.

- `reference.patch`: complete implementation.
- `hidden_verification_test.rb`: Minitest integration coverage to add under `test/`.
- `interface-preserving.patch`: same ticket behavior using a shared HTML due-date partial.
- `plausible-wrong-missing-json-field.patch`: omits the promised `due_on` JSON property.
- `plausible-wrong-missing-published-editor.patch`: omits the due-date input on the published-card editor.

The wrong-control patches each include the rest of the feature and break one ticket requirement. None of these patches has been applied or tested against a running app.
