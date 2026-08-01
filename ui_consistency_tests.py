#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parent
s=BeautifulSoup((ROOT/'index.html').read_text(encoding='utf-8'),'html.parser')
cards=s.select('#grid .tool')
assert len(cards)==40, f'Expected 40 homepage tools, found {len(cards)}'
hrefs=[a.get('href') for a in cards]
assert len(hrefs)==len(set(hrefs)), 'Duplicate calculator cards in canonical catalog'
for href in hrefs: assert (ROOT/href).exists(), f'Missing tool destination: {href}'
assert not s.select('#popular-tools,[data-seo-calculator-expansion],[data-opportunity-tools]'), 'Duplicate homepage calculator showcase remains'
assert s.select_one('#grid[data-horizontal-catalog="true"]'), 'Horizontal catalog missing'
assert s.select_one('#catalogPrev') and s.select_one('#catalogNext'), 'Catalog arrows missing'
assert s.select_one('#catalogStatus'), 'Catalog status missing'
# Confirm new SEO and opportunity tools are inside Pick a calculator.
required=['auto-loan-calculator.html','credit-card-payoff-calculator.html','retirement-savings-calculator.html','home-affordability-calculator.html','loan-comparison-calculator.html','net-worth-calculator.html','break-even-calculator.html','gpa-calculator.html','mortgage-total-cost-calculator.html','mortgage-recast-calculator.html','pay-raise-calculator.html','work-hours-calculator.html']
for href in required: assert href in hrefs, f'New calculator not integrated: {href}'
# Global structural checks.
ids={}
duplicate_ids=[]
exact_duplicate_sections=[]
for p in ROOT.glob('*.html'):
    doc=BeautifulSoup(p.read_text(encoding='utf-8',errors='ignore'),'html.parser')
    seen=set()
    for el in doc.select('[id]'):
        value=el.get('id')
        if value in seen: duplicate_ids.append((p.name,value))
        seen.add(value)
    fingerprints=set()
    for sec in doc.find_all('section'):
        links=tuple(sorted(a.get('href','') for a in sec.select('a[href]')))
        heading=sec.find(['h1','h2'])
        fp=((heading.get_text(' ',strip=True).lower() if heading else ''),links)
        if links and fp in fingerprints: exact_duplicate_sections.append((p.name,fp[0]))
        fingerprints.add(fp)
assert not duplicate_ids, f'Duplicate IDs: {duplicate_ids[:10]}'
assert not exact_duplicate_sections, f'Exact duplicate sections: {exact_duplicate_sections[:10]}'
print(f'UI consistency tests: {len(cards)} unique catalog tools, no duplicate showcases, IDs or exact linked sections.')

# Homepage public count must match the canonical catalog.
from bs4 import BeautifulSoup as _BeautifulSoup
_index_soup=_BeautifulSoup(Path('index.html').read_text(encoding='utf-8'),'html.parser')
_hero_text=_index_soup.select_one('.hero').get_text(' ',strip=True)
assert '40 free, fast and private calculators.' in _hero_text, 'Homepage hero still advertises the old 28-tool count'
_trust=[x.get_text(' ',strip=True) for x in _index_soup.select('.trust > div')]
assert any(x.startswith('40') and 'Free tools' in x for x in _trust), 'Homepage trust statistic does not show 40 tools'
