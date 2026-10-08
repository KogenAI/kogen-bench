# Move several cards together

Board members need to reorganize a group of cards in one action after a planning meeting.

Use the existing account-scoped URL prefix for this route. Replace `{account_id}` with the account's numeric `external_account_id` (for example, an account with ID `42` uses the `/42/` prefix). Add `POST /{account_id}/boards/:board_id/cards/bulk_move.json`. Its JSON body is `{"card_numbers":[<positive integer>,...],"column_id":"<column UUID>"}`. `card_numbers` must be a nonempty array of unique positive integers. The target column must belong to the addressed board, and every card number must identify a card on that board.

For a valid request, move every named card to the target column and return status 200 with exactly `{"moved_card_numbers":[...]}`; the returned numbers are in the same order as the request. The change is all-or-nothing: if the card list is invalid, return status 422 with exactly `{"error":"card_numbers_must_be_nonempty_unique_integers"}`; if the target column is missing or belongs to another board, return status 404 with exactly `{"error":"column_not_found"}`; if any requested card is missing or belongs to another board, return status 404 with exactly `{"error":"card_not_found"}`. An error response must leave every card's column unchanged.

The resulting card locations must be observable as each named `Card.column` association. Any person who can access the addressed board may use this action.

There is no query-count or latency requirement for this feature.
