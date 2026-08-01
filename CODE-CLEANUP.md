# Code and automation cleanup

- One publisher remains active: `weekly_publisher.py` with `scheduled_posts.json`.
- Obsolete generators remain zero-byte so GitHub uploads neutralize the old code.
- One weekly workflow publishes, rebuilds hubs, applies SEO stages, runs audits and commits.
- `audit_site.py` validates search structure and internal discovery.
- `quality_gate.py` validates doctypes, analytics duplication, AdSense consistency, images, PWA assets and trust pages.
- `sw.js` uses fresh network HTML with cached offline fallback and cache-first static assets.
