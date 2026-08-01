#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup, Doctype
ROOT=Path(__file__).resolve().parent
ART={
'blog-why-calorie-calculators-differ.html':('guide-calorie-differences.svg','Calorie estimate comparison illustration'),
'blog-36-vs-60-month-loan.html':('guide-loan-terms.svg','36 month and 60 month loan comparison illustration'),
'blog-bmi-vs-body-fat.html':('guide-bmi-body-fat.svg','BMI and body fat comparison illustration'),
'blog-apr-vs-interest-rate.html':('guide-apr-interest.svg','APR and interest rate illustration'),
'blog-percentage-change-vs-points.html':('guide-percentage-points.svg','Percentage change and percentage points illustration'),
}
for name,(src,alt) in ART.items():
    p=ROOT/name; soup=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
    old=soup.select_one('.guide-hero-art')
    if old: old.decompose()
    article=soup.select_one('article.article')
    head=soup.select_one('.article-head')
    if article and head:
        figure=soup.new_tag('figure'); figure['class']=['guide-hero-art']
        img=soup.new_tag('img',src=src,alt=alt,width='160',height='160',loading='eager',decoding='async',fetchpriority='high')
        figure.append(img); head.insert_after(figure)
    for node in list(soup.contents):
        if isinstance(node,Doctype): node.extract()
    p.write_text('<!DOCTYPE html>\n'+str(soup),encoding='utf-8')
print('Added SVG hero artwork to',len(ART),'new guides.')
