#!/usr/bin/env python3
from pathlib import Path
index=Path('index.html').read_text(encoding='utf-8')
optimizer=Path('optimize_site_ui.py').read_text(encoding='utf-8')
css=Path('styles.css').read_text(encoding='utf-8')
assert 'gr.addEventListener("wheel"' not in index, 'Homepage still intercepts mouse-wheel scrolling'
assert 'gr.addEventListener("wheel"' not in optimizer, 'Future optimizer still generates wheel interception'
assert 'touch-action:pan-x pan-y' in css, 'Touch scrolling policy missing'
assert 'overscroll-behavior-y:auto' in css, 'Vertical scrolling not explicitly allowed'
assert 'catalogPrev' in index and 'catalogNext' in index, 'Horizontal arrow navigation missing'
assert 'scrollBy({left:' in index, 'Arrow horizontal scrolling missing'
assert 'fynzo-production-v23-20260801' in Path('sw.js').read_text(), 'Cache v23 missing'
print('Interaction tests: vertical wheel/touch scrolling free; horizontal arrows and native swipe retained.')
