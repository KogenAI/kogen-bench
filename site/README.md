# Kogen Bench site

This Astro project builds the standalone research site intended for `https://bench.kogen.dev`. Content is normalized only from the repository's public source files; pages link to the corresponding GitHub source at the build's data revision.

## Build

From the repository root, run:

```sh
site/build.sh
```

The build output is `site/dist/`. Dependencies are pinned in `package.json` and `package-lock.json`. The site does not deploy or modify DNS.

## Preview

For an editable local preview, run `cd site && npm run dev`. To preview the exact static output after a build, run `python3 -m http.server 4173 --directory site/dist` from the repository root and open `http://localhost:4173/`.

For Cloudflare Pages, use `site/` as the project root and `./build.sh` as the build command; set the output directory to `dist`. Set `PUBLIC_PLAUSIBLE_SCRIPT` to the actual site-specific `https://plausible.io/js/pa-….js` URL provisioned for bench.kogen.dev. The release build rejects a missing or malformed URL. It never substitutes another domain’s tracker. Use Node.js matching `.node-version` and Python 3.

This publication build runs the fail-closed release validator first and then the complete site build/check. Its checks and historical-versus-new-round policy are documented in ../reproduce/VERIFY.md. A pass does not claim every historical round is VALID or fully reproducible.

For an archival preview while publication is blocked, run `npm run build` from `site/`. This rebuilds and validates the static archive without clearing publication blockers.

## Source and publication checks

`scripts/prepare.py` reads indexed repository sources, hashes them, and creates the static content bundle. Tracked round directories absent from `rounds/index.json` are listed in `/index.json` and omitted from the archive. `scripts/check.py` checks generated routes and anchors, source links, Markdown alternates, private paths, and number provenance. The separate release validator rejects unregistered tracked rounds before publication.

For an owner-only editorial preview, set `KOGEN_BENCH_PRIVATE_PREVIEW=true` when running `npm run build`. This emits noindex metadata and excludes the analytics bootstrap. Private hosting access is still required; noindex is not access control. Rebuild normally before production.

The site preserves authored Markdown twins and uses the shared Cloudflare Pages middleware to negotiate them through `Accept: text/markdown`. Ordinary HTML, machine files and downloads keep their own representations. About, Contact and Privacy copy lives in `content/`; data, sitemap and source hashes come from the same normalized route inventory.

JSONL downloads preserve source bytes and the per-round directory layout, so index-relative filenames resolve correctly. Source indexes record checksums and byte lengths. The build rejects assets over the static host limit.

Round badges come from the reviewed `rounds/STATUS.md` inventory. Historical source prose is retained, including qualifications. The stack comparison page abbreviates three unpublished local artifact locators for web reading; source links and hashes still identify the unmodified repository files.

## Share card

Bench uses the approved Kogen Bench card at `public/brand/kogen-bench-card.png` (1280 × 640); its outlined SVG is preserved alongside it. `public/og.png` is an identical compatibility copy. Open Graph and X metadata use the Bench-specific URL so the former product-card URL does not retain the old preview in caches. Existing social posts may retain cached cards.

The Kogen brand bundle owns the composition and generator; these are deployment copies. Approved 9 October 2026. The card preserves the existing Kogen sprue and IBM Plex Sans typography, with a decorative measurement grid rather than plotted results. To refresh, export the canonical SVG/PNG, synchronize these three files, run the normal release build, and verify image dimensions, metadata, and the saved live card. Keep the previous verified files if export or build fails. Brand and font provenance remain governed by the Kogen brand bundle; the marks are not licensed by the repository's source-code license.
