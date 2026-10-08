We want to make it possible to publish Trackline boards, so anyone with a secret public URL (`/public/boards/:key`) can see them. Only organization owners can publish/unpublish boards (`POST`/`DELETE` on `/boards/:id/publication`).

Columns and published cards of a public board can also be opened directly at `/public/boards/:key/columns/:id` and `/public/boards/:key/cards/:number`.
We also want to add a `public_url` attribute to the board's JSON response (`nil` by default).

The existing Phoenix routes delegate to `Trackline.Ports.Publication`: keep `publish(board, user)`, `unpublish(board, user)` returning `{:ok, board}` or `{:error, :forbidden}`, `board_json/1`, and `public_board/1`, `public_column/2`, `public_card/2` returning a resource or nil. Board owners are the owners of its organization; agents and viewers are not owners. The task base includes boards, columns and draft/published cards, with numbers local to each board. Existing application behavior and tests must keep working.
