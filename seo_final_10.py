#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
import re, json
ROOT=Path(__file__).resolve().parent
TODAY='August 1, 2026'
DOMAIN='https://fynzo.me/'

def paragraph(soup,text,cls=None):
    p=soup.new_tag('p'); p.string=text
    if cls: p['class']=[cls]
    return p

def section(soup,heading,paragraphs,marker):
    box=soup.new_tag('section'); box['data-trust-section']=marker
    h=soup.new_tag('h2'); h.string=heading; box.append(h)
    for text in paragraphs: box.append(paragraph(soup,text))
    return box

def clean_document(p):
    text=p.read_text(encoding='utf-8',errors='ignore')
    text=re.sub(r'^(?:\s*<!DOCTYPE html>\s*)+', '<!DOCTYPE html>\n', text, flags=re.I)
    soup=BeautifulSoup(text,'html.parser')
    from bs4 import Doctype
    for node in list(soup.contents):
        if isinstance(node, Doctype): node.extract()
    if not soup.head or not soup.body: return
    # Keep only the delayed GA4 loader. Remove old inline duplicate initialization.
    for tag in list(soup.find_all('script')):
        raw=tag.string or ''
        if 'gtag("config","G-D7NJ4T2ZK4")' in raw and not tag.get('data-fynzo-analytics'):
            tag.decompose()
    # Ensure single AdSense loader with the configured publisher.
    ads=[x for x in soup.find_all('script',src=True) if 'pagead2.googlesyndication.com/pagead/js/adsbygoogle.js' in x.get('src','')]
    for extra in ads[1:]: extra.decompose()
    # Improve E-E-A-T About page with a transparent editorial method.
    if p.name=='about.html':
        doc=soup.select_one('.doc')
        if doc and not doc.select_one('[data-trust-section="editorial"]'):
            anchor=doc.find('h2',string=re.compile('How the calculators are reviewed',re.I))
            block=section(soup,'Editorial and calculator review process',[
                'Fynzo separates calculation logic from explanatory content. Formula inputs, units, edge cases and representative examples are checked before a calculator is published or materially changed.',
                'Finance and health pages identify assumptions, exclusions and limitations. Supporting sources link to public institutions or established standards where appropriate. Content is corrected when a reliable source, calculation test or visitor report shows that an update is needed.',
                'Yasser Chahir is the named editor and site maintainer. Fynzo does not claim professional qualifications that have not been independently verified. The website provides educational information, not personalized professional advice.'
            ],'editorial')
            if anchor: anchor.insert_before(block)
            else: doc.append(block)
            doc.append(section(soup,'Corrections and update policy',[
                'Reported errors are reviewed against the page formula, test values and cited source. Substantive corrections update the displayed review date. Cosmetic edits do not receive a misleading freshness date.',
                'Visitors can report a suspected error through the contact page and should include the page URL, expected result and non-sensitive test values.'
            ],'corrections'))
            updated=doc.select_one('.updated')
            if updated: updated.clear(); strong=soup.new_tag('strong'); strong.string='Last reviewed: '; updated.append(strong); updated.append(TODAY)
    # Add explicit service transparency to legal pages without pretending to be legal advice.
    if p.name=='privacy.html':
        doc=soup.select_one('.doc')
        if doc and not doc.select_one('[data-trust-section="services"]'):
            doc.append(section(soup,'Services currently used',[
                'Fynzo uses Google Analytics 4 to measure page usage and privacy-safe interaction events. Calculator input values and calculated results are not intentionally sent as analytics event parameters.',
                'Fynzo includes the Google AdSense publisher loader and an ads.txt authorization line for publisher pub-8379415024436818. Google and its partners may use cookies or similar technologies where advertising or measurement is enabled, subject to consent and applicable settings.',
                'The contact form uses Formspree. Browser features such as favorites, recently used tools and theme preferences can use local storage on the visitor’s device.'
            ],'services'))
    if p.name=='terms.html':
        doc=soup.select_one('.doc')
        if doc and not doc.select_one('[data-trust-section="automation"]'):
            doc.append(section(soup,'Automated access and availability',[
                'Reasonable crawling by search engines is permitted. Automated activity that overloads the service, circumvents controls, extracts substantial content for republication or interferes with other visitors is prohibited.',
                'Offline and cached copies can be temporarily older than the live page. Reload the live website before relying on an important result.'
            ],'automation'))
    if p.name=='disclaimer.html':
        doc=soup.select_one('.doc')
        if doc and not doc.select_one('[data-trust-section="version"]'):
            doc.append(section(soup,'Version and review warning',[
                'A cached or offline copy may not contain the latest correction. Important calculations should be repeated on the live page and checked against current official documents or qualified guidance.',
                'A “last reviewed” date records a content review. It does not guarantee that every external rule, rate or source remains unchanged after that date.'
            ],'version'))
    p.write_text('<!DOCTYPE html>\n'+str(soup),encoding='utf-8')

for p in ROOT.glob('*.html'): clean_document(p)
print('Final SEO stages applied to',len(list(ROOT.glob('*.html'))),'HTML files')
