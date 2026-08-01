#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
root=Path(__file__).resolve().parent
index=BeautifulSoup((root/'index.html').read_text(encoding='utf-8'),'html.parser')
tools=[a.get('href') for a in index.select('#grid .tool')]
assert len(tools)==40 and len(set(tools))==40
js=(root/'result-insights.js').read_text(encoding='utf-8')
for required in ['bmi-calculator.html','waist-to-height-ratio-calculator.html','debt-to-income-calculator.html','gpa-calculator.html','Result interpretation']:
    assert required in js, f'missing interpretation logic: {required}'
for name in tools:
    soup=BeautifulSoup((root/name).read_text(encoding='utf-8'),'html.parser')
    scripts=[s.get('src','') for s in soup.find_all('script') if 'result-insights.js' in s.get('src','')]
    assert len(scripts)==1, f'{name}: expected one result-insights.js, found {len(scripts)}'
    assert soup.select_one('#res'), f'{name}: result container missing'
css=(root/'styles.css').read_text(encoding='utf-8')
assert '.result-insight' in css and '.result-insight.caution' in css
assert '"/result-insights.js"' in (root/'sw.js').read_text(encoding='utf-8')
print('Result insight tests: 40 calculators covered with dynamic interpretation UI.')
