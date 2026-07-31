# Mobile performance optimization

- Removed Google Fonts and switched to a native system font stack.
- Delayed Google Analytics until 1.5 seconds after the window load event.
- Preloaded the homepage hero and marked it high-priority, eager and asynchronously decoded.
- Added content visibility for long below-the-fold sections.
- Hid Favorites/Recently Used when both lists are empty.
- Removed unused styles-premium.css and Python cache files.
- Updated the service-worker cache to fynzo-v9.
