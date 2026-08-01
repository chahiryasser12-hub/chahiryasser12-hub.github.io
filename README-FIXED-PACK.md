# Fynzo corrected production pack

This package was rebuilt from `repopack-output.txt` on 2026-08-01.

## Main corrections
- Kept one production article pipeline: `scheduled_posts.json` + `weekly_publisher.py`.
- Intentionally emptied obsolete generators listed in `EMPTY_FILES.txt`.
- Added a full automated site audit (`audit_site.py`).
- Strengthened the weekly GitHub Action with syntax checks, hub refresh and audit.
- Added privacy-safe GA4 interaction events without sending inputs or results.
- Added PNG PWA icons and a corrected manifest.
- Refreshed the service-worker cache.
- Added accessible live regions to calculator results.

## Upload
Upload the contents of this ZIP to the repository root and replace existing files.
Zero-byte files are intentional. They stand in for files that should be deleted.

## After upload
1. Open the GitHub Actions tab and run `Publish one weekly Fynzo article` manually once.
2. Confirm the Action passes.
3. Open `https://fynzo.me/robots.txt` and `https://fynzo.me/sitemap.xml`.
4. Resubmit the sitemap in Google Search Console.
5. In GA4, mark `calculator_result` and `contact_submit` as key events when data begins arriving.
