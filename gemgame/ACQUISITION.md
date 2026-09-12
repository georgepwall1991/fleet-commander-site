# GemGame acquisition refresh — 12 September 2026

Prepared locally on `codex/gemgame-download-growth`. No public deployment or uplift is claimed by this file.

Six English entry pages now describe the current public 2.3.0 product: Home, No ads, Offline (new), Garden, FAQ and Press. Current supplied screenshot/icon/preview assets have provenance in `assets/2026-09/provenance.json`. The previous English homepage described handcrafted/hand-designed boards, old separate purchases and an unrestricted-session claim; these pages now explain the actual life and purchase boundaries.

Rebuild: `python3 scripts/build-gemgame-acquisition.py` from the repository root. Check: `python3 scripts/check-gemgame-acquisition.py` and `ruby scripts/check-fleet-commander-funnel.rb --root .`. The Pages workflow runs both checks. Image conversion is a one-time refresh from the checked-in GemGame storefront, recorded by source hash; the HTML builder uses the included assets and needs no other repository.

For local browser review, serve the checkout under `/fleet-commander-site/` to match the GitHub Pages base path. No tracking scripts, account credentials, fabricated campaign tokens or third-party fonts were added. Use ASC-generated campaign links with the account's real provider token before claiming campaign attribution.

Research and next metadata experiment are in the GemGame repository: `marketing/competitive-intel/source-notes/search-acquisition-2026-09.md` (CI-H0.9). Keyword demand, installs, source conversion and retention remain unmeasured. App Store keyword fields are a separate release change; deploying these web pages will not update them.

After deployment, verify all six live URLs and assets, then use the existing Search Console URL-prefix property to inspect the homepage/offline/no-ads URLs and submit the project sitemap. The origin-level robots file, not `/fleet-commander-site/robots.txt`, governs crawler access. Indexing and rich results are not guaranteed. No reviews or ratings were invented for schema eligibility.

Older translated and deeper English guides remain outside this refresh and require product-accuracy review before translation expansion. Existing locale URLs and reciprocal alternate links are preserved. The app itself currently lists English, regardless of website translations.

## Local validation

Both repository checks pass. The GemGame checker fails against the old main checkout for stale claims, missing image dimensions and the absent offline guide, then passes against the refreshed pages. The generator reproduces all six pages. Default desktop and 390-pixel mobile browser reviews verified the visible homepage, current images, download CTA and navigation into the offline table, with body width equal to viewport width. Video is 24 seconds, H.264/AAC; its web derivative normalizes repeated source frame timestamps to 30 fps and decodes without errors. `codex review --uncommitted` reported no actionable regressions; browser verification was performed separately. Live deployment, Search Console indexing and download uplift are not yet verified.
