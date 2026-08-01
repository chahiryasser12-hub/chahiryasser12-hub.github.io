#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
import json, re, sys
ROOT=Path(__file__).resolve().parent
errors=[]
htmls=list(ROOT.glob('*.html'))
for p in htmls:
    text=p.read_text(encoding='utf-8',errors='ignore')
    if len(re.findall(r'<!doctype html>',text,re.I))!=1: errors.append(f'{p.name}: expected exactly one doctype')
    soup=BeautifulSoup(text,'html.parser')
    if p.name not in ('404.html','offline.html'):
        if not soup.find('link',rel=lambda x:x and 'canonical' in x): errors.append(f'{p.name}: missing canonical')
    ads=[x for x in soup.find_all('script',src=True) if 'adsbygoogle.js' in x.get('src','')]
    if len(ads)>1: errors.append(f'{p.name}: duplicate AdSense loader')
    ga=[x for x in soup.find_all('script') if 'gtag("config"' in (x.string or '')]
    if len(ga)>1: errors.append(f'{p.name}: duplicate GA4 configuration')
    for img in soup.find_all('img'):
        if not img.has_attr('alt'): errors.append(f'{p.name}: image missing alt')
        if not img.get('width') or not img.get('height'): errors.append(f'{p.name}: image missing dimensions')
        src=img.get('src','').split('?')[0]
        if src and not src.startswith(('http://','https://','data:')) and not (ROOT/src.lstrip('/')).exists(): errors.append(f'{p.name}: missing image {src}')
manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
for icon in manifest.get('icons',[]):
    if not (ROOT/icon['src'].lstrip('/')).exists(): errors.append(f'manifest missing icon {icon["src"]}')
robots=(ROOT/'robots.txt').read_text(encoding='utf-8')
if 'Sitemap: https://fynzo.me/sitemap.xml' not in robots: errors.append('robots sitemap invalid')
ads=(ROOT/'ads.txt').read_text(encoding='utf-8').strip()
if ads!='google.com, pub-8379415024436818, DIRECT, f08c47fec0942fa0': errors.append('ads.txt does not match configured publisher')
for required in ('about.html','privacy.html','terms.html','disclaimer.html','contact.html'):
    if not (ROOT/required).exists(): errors.append(f'missing trust page {required}')
print(f'Quality gate: {len(htmls)} HTML files, {len(errors)} errors.')
for e in errors: print('ERROR:',e)
raise SystemExit(1 if errors else 0)
