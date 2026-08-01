#!/usr/bin/env python3
from pathlib import Path
css=Path('styles.css').read_text(encoding='utf-8')
assert 'v19: keep calculator SVG artwork navy on hover' in css
assert '.tool:hover .ic svg [stroke="#0b1020"]' in css
assert 'stroke:#0b1020' in css
assert '.tool:hover .ic img' in css and 'filter:none' in css
sw=Path('sw.js').read_text(encoding='utf-8')
assert 'fynzo-production-v23-20260801' in sw
print('SVG hover tests: navy stroke, original image colors and cache v23 verified.')
