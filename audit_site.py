#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
from xml.etree import ElementTree as ET
from urllib.parse import urlparse
import json, sys
ROOT=Path(__file__).resolve().parent
DOMAIN='https://fynzo.me/'
errors=[]; warnings=[]; titles={}; descs={}; incoming={p.name:0 for p in ROOT.glob('*.html')}
htmls=sorted(ROOT.glob('*.html'))
calc=lambda p: p.name.endswith(('calculator.html','converter.html','estimator.html')) or p.name=='password-generator.html'
for p in htmls:
    s=BeautifulSoup(p.read_text(encoding='utf-8',errors='ignore'),'html.parser')
    if not s.html or not s.head or not s.body: errors.append(f'{p.name}: incomplete HTML document'); continue
    if s.html.get('lang')!='en': errors.append(f'{p.name}: html lang must be en')
    robots=s.find('meta',attrs={'name':'robots'})
    if p.name in ('404.html','offline.html'):
        if not robots or 'noindex' not in robots.get('content','').lower(): errors.append(f'{p.name}: 404 must be noindex')
        continue
    expected=DOMAIN if p.name=='index.html' else DOMAIN+p.name
    ts=s.find_all('title'); title=ts[0].get_text(' ',strip=True) if len(ts)==1 else ''
    if not title: errors.append(f'{p.name}: expected one non-empty title')
    else: titles.setdefault(title,[]).append(p.name)
    ds=s.find_all('meta',attrs={'name':'description'}); desc=ds[0].get('content','').strip() if len(ds)==1 else ''
    if not desc: errors.append(f'{p.name}: expected one meta description')
    else: descs.setdefault(desc,[]).append(p.name)
    if not robots or 'index' not in robots.get('content','').lower(): errors.append(f'{p.name}: missing index robots directive')
    hs=s.find_all('h1')
    if len(hs)!=1: errors.append(f'{p.name}: expected one h1, found {len(hs)}')
    cs=s.find_all('link',rel=lambda x:x and 'canonical' in x)
    if len(cs)!=1 or cs[0].get('href')!=expected: errors.append(f'{p.name}: canonical must be {expected}')
    for key in ('og:title','og:description','og:url','og:image','og:type','og:site_name'):
        t=s.find('meta',attrs={'property':key})
        if not t or not t.get('content','').strip(): errors.append(f'{p.name}: missing {key}')
    ogurl=s.find('meta',attrs={'property':'og:url'})
    if ogurl and ogurl.get('content')!=expected: errors.append(f'{p.name}: og:url must match canonical')
    for key in ('twitter:card','twitter:title','twitter:description','twitter:image'):
        t=s.find('meta',attrs={'name':key})
        if not t or not t.get('content','').strip(): errors.append(f'{p.name}: missing {key}')
    schema_types=[]
    for tag in s.find_all('script',attrs={'type':'application/ld+json'}):
        try:
            data=json.loads(tag.string or '')
            typ=data.get('@type'); schema_types.append(typ)
        except Exception as e: errors.append(f'{p.name}: invalid JSON-LD: {e}')
    if len(schema_types)!=len(set(schema_types)): errors.append(f'{p.name}: duplicate schema types {schema_types}')
    if p.name=='index.html':
        for required in ('Organization','WebSite','ItemList'):
            if required not in schema_types: errors.append(f'{p.name}: missing {required} schema')
    elif calc(p):
        for required in ('WebApplication','BreadcrumbList'):
            if required not in schema_types: errors.append(f'{p.name}: missing {required} schema')
        visible=len(s.select('.faq-item'))+len(s.find_all('details'))
        if visible and 'FAQPage' not in schema_types: errors.append(f'{p.name}: visible FAQ without FAQPage schema')
    elif p.name.startswith('blog-'):
        for required in ('Article','BreadcrumbList'):
            if required not in schema_types: errors.append(f'{p.name}: missing {required} schema')
    for tag,attr in [('a','href'),('link','href'),('script','src'),('img','src')]:
        for el in s.find_all(tag):
            v=(el.get(attr) or '').split('#')[0].split('?')[0]
            if not v or v.startswith(('mailto:','tel:','data:','javascript:','#')): continue
            if v.startswith(('http://','https://')):
                u=urlparse(v)
                if u.netloc=='fynzo.me' and u.path not in ('','/'):
                    target=ROOT/u.path.lstrip('/')
                    if not target.exists(): errors.append(f'{p.name}: missing internal URL {v}')
                    elif target.suffix=='.html': incoming[target.name]=incoming.get(target.name,0)+1
                continue
            target=ROOT/v.lstrip('/')
            if not target.exists(): errors.append(f'{p.name}: missing local {attr} {v}')
            elif tag=='a' and target.suffix=='.html': incoming[target.name]=incoming.get(target.name,0)+1
for label,m in [('title',titles),('description',descs)]:
    for value,pages in m.items():
        if len(pages)>1: errors.append(f'duplicate {label}: {pages}')
try:
    tree=ET.parse(ROOT/'sitemap.xml'); ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}; locs=[x.text for x in tree.findall('.//s:loc',ns)]
except Exception as e: errors.append(f'sitemap.xml invalid: {e}'); locs=[]
expected=set()
for p in htmls:
    if p.name in ('404.html','offline.html'): continue
    page_soup=BeautifulSoup(p.read_text(encoding='utf-8',errors='ignore'),'html.parser')
    page_robots=page_soup.find('meta',attrs={'name':'robots'})
    if page_robots and 'noindex' in page_robots.get('content','').lower(): continue
    expected.add(DOMAIN if p.name=='index.html' else DOMAIN+p.name)
for u in sorted(expected-set(locs)): errors.append(f'sitemap missing {u}')
for u in sorted(set(locs)-expected): errors.append(f'sitemap extra/nonexistent {u}')
if len(locs)!=len(set(locs)): errors.append('sitemap has duplicate URLs')
robots_text=(ROOT/'robots.txt').read_text(encoding='utf-8',errors='ignore')
if f'Sitemap: {DOMAIN}sitemap.xml' not in robots_text: errors.append('robots.txt has invalid/missing sitemap directive')
for p in htmls:
    if p.name not in ('index.html','404.html','offline.html') and incoming.get(p.name,0)==0: warnings.append(f'{p.name}: possible orphan page')
print(f'Audited {len(htmls)} HTML files; {len(errors)} errors; {len(warnings)} warnings.')
for x in errors: print('ERROR:',x)
for x in warnings: print('WARN:',x)
raise SystemExit(1 if errors else 0)
