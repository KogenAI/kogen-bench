# Add per-column work-in-progress limits

## Base

Implement this feature in the public Fizzy Rails application at [basecamp/fizzy](https://github.com/basecamp/fizzy), pinned to commit `8112b3dbafeea72225c1ed09ae170e8cbe2d1195`. Authenticated account routes below include Fizzy's existing `/{account_id}` path prefix.

## Requirements

1. A board column has an optional work-in-progress limit. A missing or `null` limit means the column is unlimited.
2. The existing column edit dialog has a labeled `WIP limit` number input submitted as `column[wip_limit]`. Saving it sets the limit; leaving it blank clears the limit. The input accepts positive whole numbers only.
3. `GET /{account_id}/boards/:board_id/columns.json` and `GET /{account_id}/boards/:board_id/columns/:column_id.json` return HTTP 200 and include `wip_limit` and `active_cards_count` for each returned column. `wip_limit` is an integer or JSON `null`; `active_cards_count` is an integer.
4. `PATCH /{account_id}/boards/:board_id/columns/:column_id.json` accepts `{ "column": { "wip_limit": N } }` where `N` is a positive integer, or `null` to clear the limit. If an update includes another valid column field but omits `wip_limit`, the saved limit remains unchanged. A successful update returns HTTP 200 and the updated column JSON, including both fields in requirement 3.
5. A limit of zero, a negative value, or a non-integer value is invalid. An invalid JSON update returns HTTP 422 with an object shaped `{ "errors": { "wip_limit": ["..."] } }`; the prior limit remains saved. A blank value in the edit dialog clears the limit instead of returning an error.
6. The WIP count is the number of cards assigned to that column that are published, open, and not postponed. Drafted, closed, postponed, and untriaged cards do not count. `active_cards_count` reports this count even when it is greater than the configured limit.
7. The board page returns HTTP 200. When a column has a limit, its column header displays the exact text `WIP: <active_cards_count> / <wip_limit>`; when it has no limit, the WIP text is omitted. Lowering a limit below the number already in the column leaves those cards in place and shows the over-limit count.
8. A card can be moved into a column through either `POST /{account_id}/cards/:card_number/triage.json?column_id=:column_id` or the board's existing Turbo Stream drop endpoint `POST /{account_id}/columns/cards/:card_number/drops/column.turbo_stream?column_id=:column_id`. If that move would increase the target column's active-card count above its limit, the request is rejected before changing the card's column or status.
9. A rejected JSON triage request returns HTTP 422 with exactly these keys and values: `{ "error": "wip_limit_reached", "column_id": "<target column id>", "wip_limit": <integer limit> }`. A rejected Turbo Stream drop request returns HTTP 422 and replaces `#flash` with the notice `This column has reached its WIP limit of <N>.` After either rejected move, `GET /{account_id}/cards/:card_number.json` returns HTTP 200 and reports the card's unchanged `column`, `status`, `closed`, and `postponed` values.
10. Moving a card from a limited column to another column through `POST /{account_id}/cards/:card_number/triage.json?column_id=:column_id`, or back to triage through `DELETE /{account_id}/cards/:card_number/triage.json`, remains allowed and returns any successful 2xx HTTP status. Resubmitting a card that is already active in its target column is allowed because it does not increase that column's active-card count, and returns any successful 2xx HTTP status. With no configured limit, moves into the column remain allowed and return any successful 2xx HTTP status.
11. This feature has no latency, query-count, or scaling target.
