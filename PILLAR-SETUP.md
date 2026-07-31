# Fynzo pillar pages setup

1. Copy `pillar_builder.py` to the root of the Fynzo repository.
2. From the repository root, run:

```bash
python pillar_builder.py
```

3. Review the changes:

```bash
git diff
```

4. Commit and push:

```bash
git add -A
git commit -m "Add topic pillar pages and internal linking"
git push
```

The script is idempotent and safe to re-run. It creates:

- `mortgage-guides.html`
- `loan-guides.html`
- `savings-guides.html`
- `percentage-guides.html`
- `health-calculators.html`

It also:

- adds the five hubs to the homepage;
- adds one relevant pillar backlink to calculators and articles;
- links every pillar to its related calculators and published articles;
- marks scheduled articles as coming soon until they exist;
- adds the pillar URLs to `sitemap.xml`;
- updates the weekly publishing workflow so pillar links refresh after future articles are published.
