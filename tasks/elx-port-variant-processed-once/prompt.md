Storage is filling up with duplicate picture files. An agent uploads a photograph, the background job runs and writes the derived copy — then the first reader to open its ticket triggers the same conversion again, and the second copy is kept next to the first forever.

Make an upload get derived once. After the background work has run, opening the ticket's image link and fetching the picture it links to does no image processing, and exactly one derived copy is in storage.

What a reader is served does not change — the same picture they get today, byte for byte.

The base's `Trackline.Ports.Images` models original uploads and stored derivatives in Ecto. Keep `upload(org, bytes)`, `derive(image_id)`, `reader_url(image)`, `fetch(image_id)`, the `/uploads/:id/derived` route, and `Trackline.Ports.DeriveImage` on Oban's default queue. `convert/1` is the existing transformer (`:image_transform` config, with its current default); do not change the transformation. The image URL is stable for an upload. Jobs may be retried or duplicated, and a reader may arrive while background work is underway. Persistence must survive separate runs of the job; an in-memory cache alone is insufficient. Existing application tests must keep passing.
