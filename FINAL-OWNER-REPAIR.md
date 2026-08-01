# Fynzo owner-reported repair

## Fixed
- Homepage count corrected from 28 to 40 in the hero and trust statistic.
- Canonical catalog verified at 40 unique tools with 40 unique destinations.
- All 40 tools verified with the Save PDF control and shared report script.
- Missing `og-default.png` generated at 1200 x 630.
- Missing PWA icons generated at 192 x 192, 512 x 512, and maskable 512 x 512.
- `robots.txt` sitemap syntax corrected to a plain absolute URL.
- Catalog instructions corrected so they no longer claim that the vertical mouse wheel browses horizontally.
- Service-worker cache bumped to v21.
- Regression tests strengthened so the public tool count cannot silently return to 28.

## Validation
Run `python audit_site.py`, `python quality_gate.py`, `python formula_tests.py`, `python faq_tests.py`, `python interaction_tests.py`, and `python ui_consistency_tests.py`.
