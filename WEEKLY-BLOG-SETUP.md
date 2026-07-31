# Weekly Fynzo blog automation

## Included

- 25 source-backed article packages in `scheduled_posts.json`.
- One publication every Friday at 08:00 UTC, starting August 7, 2026.
- Final scheduled publication: January 22, 2027.
- `weekly_publisher.py` publishes no more than one due article per run.
- Each generated article includes explanation, example, table, mistakes, steps, calculator link, sources, reviewer and review date.
- `blog.html` and `sitemap.xml` update automatically.

## Enable

1. Upload the complete package to the repository root.
2. Open GitHub **Actions**.
3. Enable workflows if prompted.
4. Open **Publish one weekly Fynzo article**.
5. The workflow runs automatically each Friday.

## Manual test

Use **Run workflow**. If no article is due, no content is published. Each run publishes at most one overdue or due article.

## Pause

Disable the workflow in GitHub Actions, or remove `.github/workflows/publish-weekly-blog.yml`.
