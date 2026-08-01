#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
root=Path(__file__).resolve().parent
js=(root/'fynzo.js').read_text(encoding='utf-8')
assert 'function toggleFaq(q)' in js, 'Delegated FAQ toggle missing'
assert 'document.addEventListener("click"' in js, 'Delegated FAQ click handler missing'
assert 'document.addEventListener("keydown"' in js, 'FAQ keyboard handler missing'
legacy='document.querySelectorAll(".faq-item").forEach(function(it){it.onclick'
count=0
for p in root.glob('*.html'):
    text=p.read_text(encoding='utf-8',errors='ignore')
    assert legacy not in text, f'{p.name}: duplicate legacy FAQ click handler remains'
    s=BeautifulSoup(text,'html.parser')
    for i,item in enumerate(s.select('.faq-item'),1):
        q=item.select_one('.faq-q'); a=item.select_one('.faq-a')
        assert q and a, f'{p.name}: incomplete FAQ item {i}'
        assert q.get('role')=='button', f'{p.name}: FAQ question missing button role'
        assert q.get('tabindex')=='0', f'{p.name}: FAQ question not keyboard focusable'
        assert q.get('aria-expanded') in ('false','true'), f'{p.name}: missing aria-expanded'
        assert q.get('aria-controls')==a.get('id'), f'{p.name}: aria-controls mismatch'
        count+=1
print(f'FAQ tests: one delegated click/keyboard system; {count} accessible FAQ items validated.')
