#!/usr/bin/env python3
"""Merge generated calculator enhancements into one non-repetitive content flow."""
from pathlib import Path
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parent
PAGES=sorted(list(ROOT.glob('*-calculator.html'))+[ROOT/'password-generator.html'])


def copy_node(node, soup):
    return BeautifulSoup(str(node), 'html.parser').find()


def extract_section(block, heading):
    h=None
    for x in block.find_all('h2', recursive=False):
        if x.get_text(' ',strip=True).lower()==heading.lower(): h=x; break
    if not h: return []
    out=[]
    for sib in h.next_siblings:
        if getattr(sib,'name',None)=='h2': break
        if getattr(sib,'name',None): out.append(sib)
    return out


def paragraph_after(block, heading):
    nodes=extract_section(block, heading)
    for n in nodes:
        if n.name=='p': return n.get_text(' ',strip=True)
    return ''


def clean(path):
    soup=BeautifulSoup(path.read_text(encoding='utf-8',errors='ignore'),'html.parser')
    complete=soup.select_one('[data-complete-calculator="true"]')
    long=soup.select_one('[data-long-tail="true"]')
    if not complete and not long: return False

    supplement=soup.new_tag('section')
    supplement['class']=['calculator-supplement']
    supplement['data-calculator-supplement']='true'

    # Keep only genuinely additive material from the generated complete block.
    if complete:
        quick=paragraph_after(complete,'Quick answer')
        if quick:
            h=soup.new_tag('h2'); h.string='Quick answer'; supplement.append(h)
            p=soup.new_tag('p'); p.string=quick; supplement.append(p)

        how=paragraph_after(complete,'How to use the calculator')
        if how:
            h=soup.new_tag('h2'); h.string='How to use the calculator'; supplement.append(h)
            p=soup.new_tag('p'); p.string=how; supplement.append(p)

    # Fold long-tail examples into one useful examples section, rather than a separate SEO block.
    if long:
        h=soup.new_tag('h2'); h.string='Practical examples and common questions'; supplement.append(h)
        lead=long.select_one('.long-tail-lead')
        if lead: supplement.append(copy_node(lead,soup))
        grid=soup.new_tag('div'); grid['class']=['practical-example-grid']
        for item in long.select('.long-tail-item'):
            grid.append(copy_node(item,soup))
        supplement.append(grid)

    # Preserve the unique mortgage tables from the generated complete block.
    if complete and path.name=='mortgage-calculator.html':
        h=soup.new_tag('h2'); h.string='Educational mortgage payment tables'; supplement.append(h)
        heading=None
        for x in complete.find_all('h2',recursive=False):
            if x.get_text(' ',strip=True)=='Educational mortgage payment tables': heading=x; break
        if heading:
            for sib in heading.next_siblings:
                if getattr(sib,'name',None)=='h2': break
                if getattr(sib,'name',None): supplement.append(copy_node(sib,soup))

    if complete:
        assumptions=paragraph_after(complete,'Assumptions')
        if assumptions:
            h=soup.new_tag('h2'); h.string='Assumptions'; supplement.append(h)
            p=soup.new_tag('p'); p.string=assumptions; supplement.append(p)

        mistakes=extract_section(complete,'Common mistakes')
        if mistakes:
            h=soup.new_tag('h2'); h.string='Common mistakes'; supplement.append(h)
            for node in mistakes: supplement.append(copy_node(node,soup))

    # Insert before the original FAQ/source/related area when possible, otherwise before footer.
    anchor=None
    for h in soup.find_all('h2'):
        if h.find_parent(attrs={'data-complete-calculator':'true'}) or h.find_parent(attrs={'data-long-tail':'true'}): continue
        if h.get_text(' ',strip=True).lower() in ('frequently asked questions','source and review information','you might also need'):
            anchor=h; break
    if anchor:
        container=anchor.parent
        if container and container.name in ('section','div','article') and container is not soup.body:
            container.insert_before(supplement)
        else: anchor.insert_before(supplement)
    else:
        footer=soup.find('footer')
        if footer: footer.insert_before(supplement)
        else: soup.body.append(supplement)

    if long: long.decompose()
    if complete: complete.decompose()
    # Remove now-unused embedded long-tail style; global supplement CSS is used.
    style=soup.select_one('#long-tail-style')
    if style: style.decompose()
    path.write_text('<!doctype html>\n'+str(soup),encoding='utf-8')
    return True


def main():
    count=sum(clean(p) for p in PAGES if p.exists())
    css=ROOT/'styles.css'; text=css.read_text(encoding='utf-8',errors='ignore')
    marker='/* Consolidated calculator supplement */'
    if marker not in text:
        text+='''\n/* Consolidated calculator supplement */\n.calculator-supplement{max-width:900px;margin:34px auto;padding:clamp(22px,4vw,36px);background:var(--card);border:1px solid var(--line);border-radius:20px}.calculator-supplement h2{font-size:24px;margin:28px 0 10px}.calculator-supplement h2:first-child{margin-top:0}.calculator-supplement h3{font-size:18px;margin:0 0 7px}.calculator-supplement p,.calculator-supplement li{color:var(--muted);line-height:1.75}.calculator-supplement ul{margin:0 0 18px 22px}.practical-example-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin-top:16px}.practical-example-grid .long-tail-item{padding:18px;background:var(--bg);border:1px solid var(--line);border-radius:14px}.practical-example-grid .long-tail-item p{margin:0}.calculator-supplement .calc-example-table{width:100%;border-collapse:collapse}.calculator-supplement .calc-example-table th,.calculator-supplement .calc-example-table td{padding:11px;border:1px solid var(--line);text-align:left}\n'''
        css.write_text(text,encoding='utf-8')
    print(f'Cleaned and merged content on {count} calculator pages.')

if __name__=='__main__': main()
