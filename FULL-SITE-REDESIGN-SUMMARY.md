# Fynzo full UI cleanup and catalog redesign

## Homepage cleanup
- Kept one canonical calculator discovery area: `Pick a calculator`.
- Removed duplicate `Popular calculators`, `More decision calculators`, and `New high-intent calculators` showcases.
- Integrated all 40 calculators into the canonical catalog.
- Added all 12 recently created calculators to the main catalog.

## Catalog behavior
- All displays 8 cards at a time on desktop: four columns by two rows.
- Remaining tools are available through arrow buttons, horizontal scrollbar, mouse wheel, trackpad and touch swipe.
- Tablet and mobile use responsive partial-card previews to communicate horizontal scrolling.
- Finance, Health and Everyday filters remain available.
- Search filters the complete 40-tool catalog.
- Status text announces the active result count.
- Enter opens the first visible search result.

## Card design
- Unified card height, icon treatment, title size, description length, badges, spacing and hover/focus states.
- New calculators retain their unique SVG artwork.
- Descriptions are clamped to prevent uneven cards.

## Duplicate cleanup
- Removed secondary SEO calculator blocks from internal calculator pages when a focused recommendation section already existed.
- Tested for duplicate homepage destinations, duplicate IDs and exact repeated linked sections.

## Interaction and accessibility
- Filter buttons expose `aria-pressed`.
- Catalog is keyboard focusable and has an accessible label.
- Previous and next controls have accessible labels.
- FAQ click, touch, Enter and Space behavior remains active.

## Automation
- Added `optimize_site_ui.py` after the homepage and sitemap rebuild step.
- Added `ui_consistency_tests.py` to GitHub Actions.
- Future scheduled publishing regenerates content, then reapplies the canonical catalog and duplicate cleanup before SEO checks.
