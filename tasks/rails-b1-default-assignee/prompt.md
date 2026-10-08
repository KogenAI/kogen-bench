# Board default assignee

When a board receives a steady stream of similar work, its owner should be able to route new cards to the person who normally handles it.

Use Fizzy's existing account URL prefix for these routes. `{account_slug}` is the same prefix already present on normal board and card URLs.

Add a JSON endpoint at the literal account-scoped path `GET /{account_slug}/boards/:board_id/default_assignee.json`. For a board the signed-in person can access, return status 200 and exactly `{"board_id":"<board UUID>","default_assignee_id":"<user UUID or null>"}`.

Add `PATCH /{account_slug}/boards/:board_id/default_assignee.json`. The JSON request body is `{"default_assignee_id":"<user UUID>"}` to select a default or `{"default_assignee_id":null}` to clear it. Only a board administrator may change this setting. A selected person must be active and have access to that board. On success return status 200 with the same two-key JSON object described above. If the selected person is inactive or has no access to the board, return status 422 with exactly `{"error":"default_assignee_must_be_active_board_user"}` and leave the existing setting unchanged. A non-administrator receives status 403 and no change is made.

When a published card is created with `POST /{account_slug}/boards/:board_id/cards.json`, assign the board's configured default assignee. If the board has no default, create the card without an assignee. A valid JSON card create returns a successful 2xx HTTP response; no particular 2xx status is required. This automatic assignment applies to JSON card creation only. An HTML draft create may render a successful response or redirect; either way, the new draft remains unassigned. The persisted preference must be visible as `Board.default_assignee_id`, and the resulting assignment must be visible through `Card.assignees`.

There is no query-count or latency requirement for this feature.
