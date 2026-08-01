#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
from xml.etree import ElementTree as ET
from urllib.parse import urlparse
import json, re
ROOT=Path(__file__).resolve().parent
DOMAIN='https://fynzo.me/'
PRIORITY=[
'index.html','mortgage-calculator.html','mortgage-total-cost-calculator.html',
'loan-calculator.html','auto-loan-calculator.html','compound-interest-calculator.html',
'bmi-calculator.html','calorie-calculator.html','percentage-calculator.html',
'savings-goal-calculator.html','work-hours-calculator.html']
errors=[]
seen_titles={}; seen_desc={}
for name in PRIORITY:
    p=ROOT/name
    if not p.exists(): errors.append(f'{name}: missing priority page'); continue
    s=BeautifulSoup(p.read_text(encoding='utf-8',errors='ignore'),'html.parser')
    title=s.title.get_text(' ',strip=True) if s.title else ''
    desc=(s.find('meta',attrs={'name':'description'}) or {}).get('content','').strip()
    h1=s.find_all('h1')
    canonical=s.find('link',rel=lambda x:x and 'canonical' in x)
    robots=s.find('meta',attrs={'name':'robots'})
    if not 30 <= len(title) <= 65: errors.append(f'{name}: title length {len(title)}')
    if not 90 <= len(desc) <= 170: errors.append(f'{name}: description length {len(desc)}')
    if len(h1)!=1: errors.append(f'{name}: expected one h1, found {len(h1)}')
    if not canonical: errors.append(f'{name}: missing canonical')
    if robots and 'noindex' in robots.get('content','').lower(): errors.append(f'{name}: priority page is noindex')
    seen_titles.setdefault(title,[]).append(name); seen_desc.setdefault(desc,[]).append(name)
    if name!='index.html':
        if not s.select_one('#fx') or not s.select_one('#res'): errors.append(f'{name}: calculator UI missing')
        visible=' '.join(s.get_text(' ',strip=True).split())
        if len(visible.split()) < 300: errors.append(f'{name}: fewer than 300 visible words')
        types=[]
        for tag in s.find_all('script',attrs={'type':'application/ld+json'}):
            try: types.append(json.loads(tag.string or '{}').get('@type'))
            except Exception: errors.append(f'{name}: invalid JSON-LD')
        for required in ('WebApplication','BreadcrumbList'):
            if required not in types: errors.append(f'{name}: missing {required} schema')
for value,pages in seen_titles.items():
    if value and len(pages)>1: errors.append(f'duplicate priority title: {pages}')
for value,pages in seen_desc.items():
    if value and len(pages)>1: errors.append(f'duplicate priority description: {pages}')
root=ET.parse(ROOT/'sitemap.xml').getroot(); ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
locs={x.text for x in root.findall('.//s:loc',ns)}
for name in PRIORITY:
    url=DOMAIN if name=='index.html' else DOMAIN+name
    if url not in locs: errors.append(f'sitemap missing priority URL: {url}')
robots=(ROOT/'robots.txt').read_text(encoding='utf-8')
if 'Sitemap: https://fynzo.me/sitemap.xml' not in robots: errors.append('robots.txt sitemap directive invalid')
index=BeautifulSoup((ROOT/'index.html').read_text(encoding='utf-8'),'html.parser')
tools=index.select('#grid .tool')
hrefs=[a.get('href') for a in tools]
if len(hrefs)!=40 or len(set(hrefs))!=40: errors.append(f'catalog expected 40 unique tools, found {len(hrefs)}/{len(set(hrefs))}')
hero=index.select_one('.hero').get_text(' ',strip=True)
if '40 free, fast and private calculators.' not in hero: errors.append('homepage public tool count is not 40')
print(f'SEO launch gate: {len(PRIORITY)} priority pages, {len(locs)} sitemap URLs, {len(errors)} errors.')
for e in errors: print('ERROR:',e)
raise SystemExit(1 if errors else 0)
