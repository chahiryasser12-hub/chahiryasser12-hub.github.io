# Final interaction repair

## FAQ root cause and fix
- Removed legacy page-level FAQ click handlers from 22 pages. Those handlers ran together with the global handler and could toggle an answer twice, making some FAQs appear unresponsive.
- Replaced per-item listeners with one delegated FAQ system in `fynzo.js`.
- Click, touch, Enter and Space now use the same toggle function.
- `aria-expanded` updates on every toggle.
- The symbol changes between plus and minus.
- All 171 FAQ items were structurally validated.

## Calculator catalog scrolling fix
- Removed the mouse-wheel handler that called `preventDefault()` over the tools catalog.
- Vertical mouse-wheel and touch scrolling now continue down the page normally, even when the pointer is over a calculator card.
- Horizontal browsing remains available with previous/next arrows, the native horizontal scrollbar, trackpad horizontal gestures and touch swipe.
- Added explicit `touch-action: pan-x pan-y` and vertical overscroll behavior.

## Future build protection
- Updated `optimize_site_ui.py` so rebuilt pages do not restore legacy FAQ handlers or wheel interception.
- Added `interaction_tests.py` to the GitHub workflow.
- Strengthened `faq_tests.py` to reject duplicate page-level FAQ handlers.
- Service-worker cache updated to v20.
