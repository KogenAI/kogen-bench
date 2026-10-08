# Export a board's cards as CSV

## Public base

Fizzy is based on the public snapshot at commit `8112b3dbafeea72225c1ed09ae170e8cbe2d1195`:
`~/bench/tasks/rails-_base/hard2-fizzy-20261001`.

## Ticket

As a board member, I want to download a spreadsheet of a board's cards so I can review and share the work outside Fizzy.

**T1.** A signed-in user who can access a board may request `GET /{account_id}/boards/{board_id}/card_export.csv`; `account_id` is the account URL prefix and `board_id` is the identifier accepted by that account's normal board URL. An accessible request returns HTTP 200. A user who cannot access the board, including when it belongs to another account, receives the app's normal 404 response.

**T2.** The HTML page for an accessible board returns HTTP 200 and contains a link whose visible text is exactly `Export cards (CSV)` and whose destination is that board's account-prefixed CSV export URL. The link may omit the `.csv` suffix when the route defaults to CSV.

**T3.** A successful request downloads an attachment named `board-cards.csv` with content type `text/csv; charset=utf-8`; the body is valid UTF-8 CSV with normal CSV escaping for commas, quotes, and line breaks.

**T4.** The first CSV row has exactly these columns, in this order: `Number`, `Title`, `Status`, `Assignees`, `Tags`, `Created At`.

**T5.** The response has one data row for every published card on the requested board, including closed and postponed cards, and has no rows for draft cards or cards from another board. The response contains the full result in one CSV without pagination, regardless of filters currently selected on the board page.

**T6.** Data rows are ordered by card number in ascending numeric order.

**T7.** `Number` is the card's decimal number and `Title` is its title without transformation. `Status` is `Done` for a closed card, `Not now` for a postponed card, the current column's name for any other card with a column, and `Maybe?` for any other card without a column.

**T8.** `Assignees` contains assigned user names sorted by case-insensitive ascending name (breaking ties by the original name) and joined with `; `; it is empty when there are no assignees. `Tags` contains tag titles sorted by case-insensitive ascending title (breaking ties by the original title) and joined with `; `; it is empty when there are no tags.

**T9.** `Created At` is the card's creation time in UTC formatted as `YYYY-MM-DDTHH:MM:SSZ`.

No performance or query-count bound is part of this ticket.
