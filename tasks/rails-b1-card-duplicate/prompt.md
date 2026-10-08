# Duplicate a card

People often need to repeat a proven piece of work. Add a JSON action that creates a fresh card from an existing card without carrying over its discussion or workflow history.

Use the existing account-scoped URL prefix for this route. Replace `{account_id}` with the account's numeric `external_account_id` (for example, an account with ID `42` uses the `/42/` prefix). `POST /{account_id}/cards/:card_number/duplicate.json` duplicates a card the signed-in person can access. On success return status 201 and exactly `{"id":<new card number>,"title":"<title>","description":"<plain-text description>"}`. The new card belongs to the same board, has the same title and plain-text description, and its creator is the signed-in person.

The new card starts open and carries no comments, reactions, steps, assignments, tags, image, or pins from the source card. The app's normal behavior that watches a card for its creator still applies; no other watcher from the source is copied. The saved state can be inspected through the named `Card` associations (`comments`, `reactions`, `steps`, `assignees`, `tags`, `pins`, and `watches`) and `Card.closed?`.

The source card is unchanged. The action returns 404 when the signed-in person cannot access the source card.

There is no query-count or latency requirement for this feature.
