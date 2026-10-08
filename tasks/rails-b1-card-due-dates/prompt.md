# Add optional due dates to cards

**Base application:** Fizzy, [basecamp/fizzy](https://github.com/basecamp/fizzy) at commit `8112b3dbafeea72225c1ed09ae170e8cbe2d1195`.

Fizzy cards can have an optional calendar due date. The existing card record exposes this value as `Card#due_on`, a date or `nil`.

## JSON behavior

Use the existing account-scoped card routes. Create cards with `POST /{account_id}/boards/:board_id/cards.json` and update them with `PATCH /{account_id}/cards/:number.json`; the JSON request body uses a top-level `card` object. In either request, `card.due_on` accepts a calendar date formatted as `YYYY-MM-DD`. A valid card create returns a successful 2xx HTTP response; no particular 2xx status is required.

On create, omitting `due_on` leaves it unset. On update, omitting `due_on` preserves its current value. Sending `due_on: null` or `due_on: ""` clears it.

The create response, `GET /{account_id}/cards/:number.json`, and `GET /{account_id}/cards.json` always include a `due_on` property for every card. Its value is the date as `YYYY-MM-DD`, or JSON `null` when the card has no due date.

## HTML behavior

The draft composer and the published-card edit screen each have a date input labeled “Due date” with the submitted name `card[due_on]`. The input shows the card's current due date when one is set. Saving a chosen date stores it on that card; saving the field blank clears it.

When a card has a due date, both its compact preview in the `/cards` list and its detail page render that date as a `<time>` element whose `datetime` attribute is `YYYY-MM-DD` and whose visible text is `Due YYYY-MM-DD`. Cards without a due date show no due-date time element.
