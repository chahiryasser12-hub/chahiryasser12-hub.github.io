# Upload instructions

1. Extract the ZIP.
2. Upload everything inside the extracted folder to the root of the GitHub repository.
3. Replace existing files when GitHub asks.
4. Keep zero-byte files as supplied. They intentionally neutralize obsolete generators.
5. Commit with: `Complete first 10 SEO stages`.
6. Open GitHub Actions and manually run `Publish one weekly Fynzo article` once.
7. Resubmit `sitemap.xml` in Google Search Console after deployment.

The workflow now runs `seo_first_10.py` after every weekly article and hub refresh, then runs `audit_site.py`.
