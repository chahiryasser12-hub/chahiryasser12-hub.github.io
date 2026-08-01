#!/usr/bin/env python3
"""Attach the shared result interpretation system to every catalog calculator."""
from pathlib import Path
from bs4 import BeautifulSoup, Doctype
ROOT=Path(__file__).resolve().parent
index=BeautifulSoup((ROOT/'index.html').read_text(encoding='utf-8'),'html.parser')
tools=[a.get('href') for a in index.select('#grid .tool')]
for name in tools:
    path=ROOT/name
    soup=BeautifulSoup(path.read_text(encoding='utf-8',errors='ignore'),'html.parser')
    if not soup.body or not soup.select_one('#res'): continue
    for old in soup.find_all('script',src=lambda x:x and 'result-insights.js' in x): old.decompose()
    soup.body.append(soup.new_tag('script',src='result-insights.js?v=20260801-1',defer=True))
    for node in list(soup.contents):
        if isinstance(node,Doctype): node.extract()
    path.write_text('<!DOCTYPE html>\n'+str(soup),encoding='utf-8')
print('Result insights integrated into',len(tools),'catalog tools.')
