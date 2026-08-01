#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
root=Path(__file__).resolve().parent
index=BeautifulSoup((root/'index.html').read_text(encoding='utf-8'),'html.parser')
tools=[a.get('href') for a in index.select('#grid .tool')]
assert len(tools)==40 and len(set(tools))==40
js=(root/'visual-results.js').read_text(encoding='utf-8')
for token in ['bmi-calculator.html','waist-to-height-ratio-calculator.html','debt-to-income-calculator.html','gpa-calculator.html','grade-percentage-calculator.html','donutPages']:
    assert token in js, f'missing visual logic: {token}'
for name in tools:
    soup=BeautifulSoup((root/name).read_text(encoding='utf-8'),'html.parser')
    assert soup.select_one('.result-chart'), f'{name}: result chart container missing'
    scripts=[x for x in soup.find_all('script',src=lambda x:x and 'visual-results.js' in x)]
    assert len(scripts)==1, f'{name}: expected one visual-results.js, found {len(scripts)}'
css=(root/'styles.css').read_text(encoding='utf-8')
for token in ['.viz-gauge','.viz-donut-wrap','.viz-bars']:
    assert token in css, f'missing visual style {token}'
assert '"/visual-results.js"' in (root/'sw.js').read_text(encoding='utf-8')
print('Visual result tests: 40 calculators covered with tailored charts and indicators.')
