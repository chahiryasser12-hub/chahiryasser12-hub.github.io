# Calculator card design and placement fix

## Corrected issues
- Removed the plain text-heavy cards shown near the footer.
- Moved the homepage calculator discovery section directly after Popular calculators.
- Moved contextual calculator suggestions directly after the calculator/result recommendation area.
- Rebuilt cards with a single-column content flow so titles and descriptions no longer split awkwardly.

## New card design
- Unique SVG icon for each calculator
- Short category badge
- Clear title
- Compact description
- Visible Open calculator action
- Consistent spacing, border radius, shadows, hover and keyboard focus
- Responsive single-column layout on mobile

## Automation
The weekly workflow runs `improve_seo_calculator_cards.py` after the calculator integration step, preventing future rebuilds from restoring the old layout.
