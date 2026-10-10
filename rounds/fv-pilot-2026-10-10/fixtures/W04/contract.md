# Preserve before cleanup

`Preservation.init/0` has a sole work copy (`work=true`), no preserved copy
(`saved=false`), and no pending cleanup. The fields are booleans. `preserve_ok`
sets saved to `saved or work` and sets pending to work. `preserve_fail` keeps
work and saved unchanged and sets pending to work. A failed preservation with
no saved copy must retain the sole work copy through subsequent cleanup.
`cleanup` and `retry` perform the same idempotent operation: only when pending
and saved are both true may they clear work and pending; saved is retained.
Otherwise they retain all fields, including pending after failure. Retrying
does not simulate a successful storage operation; `preserve_ok` reports that
operation separately. Other events leave state unchanged. Check all boolean
states as well as all sequences through six events from init; real filesystem
durability is outside this contract.
