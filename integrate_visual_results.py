#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup, Doctype
ROOT=Path(__file__).resolve().parent
s=BeautifulSoup((ROOT/'index.html').read_text(encoding='utf-8'),'html.parser')
tools=[a.get('href') for a in s.select('#grid .tool')]
for name in tools:
    p=ROOT/name; soup=BeautifulSoup(p.read_text(encoding='utf-8',errors='ignore'),'html.parser')
    if not soup.body or not soup.select_one('.result-chart'): continue
    for old in soup.find_all('script',src=lambda x:x and 'visual-results.js' in x): old.decompose()
    soup.body.append(soup.new_tag('script',src='visual-results.js?v=20260801-1',defer=True))
    for node in list(soup.contents):
        if isinstance(node,Doctype): node.extract()
    p.write_text('<!DOCTYPE html>\n'+str(soup),encoding='utf-8')
print('Tailored visual results integrated into',len(tools),'tools.')
