#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json, re
ROOT=Path(__file__).resolve().parent
DOMAIN='https://fynzo.me/'
CALC_SUFFIXES=('calculator.html','converter.html','estimator.html')
SPECIAL_TOOLS={'password-generator.html'}

def page_url(p): return DOMAIN if p.name=='index.html' else DOMAIN+p.name

def set_meta(soup,key,value,prop=False):
    attrs={'property':key} if prop else {'name':key}
    tags=soup.find_all('meta',attrs=attrs)
    tag=tags[0] if tags else soup.new_tag('meta')
    if not tags: tag.attrs.update(attrs)
    tag['content']=value
    if not tags: soup.head.append(tag)
    for extra in tags[1:]: extra.decompose()

def set_link(soup,rel,href):
    tags=soup.find_all('link',rel=lambda x:x and rel in x)
    tag=tags[0] if tags else soup.new_tag('link',rel=rel)
    tag['href']=href
    if not tags: soup.head.append(tag)
    for extra in tags[1:]: extra.decompose()

def visible_faq(soup):
    out=[]
    for item in soup.select('.faq-item'):
        q=item.select_one('.faq-q h3,.faq-q,.question,h3')
        a=item.select_one('.faq-a,.answer')
        if q and a:
            qt=q.get_text(' ',strip=True).rstrip('+').strip(); at=a.get_text(' ',strip=True)
            if qt and at: out.append((qt,at))
    for item in soup.find_all('details'):
        q=item.find('summary');
        if q:
            qt=q.get_text(' ',strip=True); at=' '.join(x.get_text(' ',strip=True) for x in item.find_all(['p','div'],recursive=False))
            if qt and at: out.append((qt,at))
    seen=set(); clean=[]
    for q,a in out:
        key=q.casefold()
        if key not in seen: seen.add(key); clean.append((q,a))
    return clean

def bread_schema(p,soup):
    title=(soup.find('h1') or soup.title).get_text(' ',strip=True)
    if p.name=='index.html': return None
    parent=('blog.html','Guides') if p.name.startswith('blog-') else ('index.html','Calculators')
    return {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[
      {'@type':'ListItem','position':1,'name':'Home','item':DOMAIN},
      {'@type':'ListItem','position':2,'name':parent[1],'item':DOMAIN+parent[0]},
      {'@type':'ListItem','position':3,'name':title,'item':page_url(p)}]}

def replace_managed_schema(soup,items):
    for t in list(soup.find_all('script',attrs={'type':'application/ld+json'})): t.decompose()
    for data in items:
        if not data: continue
        t=soup.new_tag('script',type='application/ld+json'); t['data-seo-managed']='true'; t.string=json.dumps(data,ensure_ascii=False,separators=(',',':')); soup.head.append(t)

def calculator_schema(p,soup,title,desc):
    h1=soup.find('h1').get_text(' ',strip=True)
    cat='HealthApplication' if any(x in p.name for x in ('bmi','calorie','body-fat','ideal-weight','water','waist','protein','pace')) else ('FinanceApplication' if any(x in p.name for x in ('mortgage','loan','interest','savings','tax','roi','salary','debt','budget','rent','apr','fund')) else 'UtilitiesApplication')
    return {'@context':'https://schema.org','@type':'WebApplication','name':h1,'description':desc,'url':page_url(p),'applicationCategory':cat,'operatingSystem':'Any','browserRequirements':'Requires JavaScript','isAccessibleForFree':True,'offers':{'@type':'Offer','price':'0','priceCurrency':'USD'},'publisher':{'@type':'Organization','name':'Fynzo','url':DOMAIN}}

def homepage_schema(soup,desc):
    links=[]
    for a in soup.select('a[href$="calculator.html"],a[href$="converter.html"],a[href="password-generator.html"]'):
        href=a.get('href'); name=a.get_text(' ',strip=True)
        if href and name and href not in [x[0] for x in links]: links.append((href,name))
    return [
      {'@context':'https://schema.org','@type':'Organization','name':'Fynzo','url':DOMAIN,'logo':DOMAIN+'logo-icon.svg','description':desc},
      {'@context':'https://schema.org','@type':'WebSite','name':'Fynzo','url':DOMAIN,'description':desc,'potentialAction':{'@type':'SearchAction','target':DOMAIN+'?q={search_term_string}','query-input':'required name=search_term_string'}},
      {'@context':'https://schema.org','@type':'ItemList','name':'Fynzo calculators','numberOfItems':len(links),'itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'url':DOMAIN+href} for i,(href,name) in enumerate(links)]}
    ]

def normalize_page(p):
    soup=BeautifulSoup(p.read_text(encoding='utf-8',errors='ignore'),'html.parser')
    if not soup.html or not soup.head: return
    soup.html['lang']='en'
    url=page_url(p)
    if p.name=='index.html':
        title='Free Finance, Health & Everyday Calculators | Fynzo'
        desc='Use free finance, health, percentage and everyday calculators with instant results, clear formulas, worked examples and practical guides.'
        soup.title.string=title
        h=soup.find('h1')
        if h: h.string='Free Finance, Health and Everyday Calculators'
    else:
        title=soup.title.get_text(' ',strip=True)
        desc=(soup.find('meta',attrs={'name':'description'}) or {}).get('content','').strip()
    set_meta(soup,'description',desc)
    set_meta(soup,'robots','index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1')
    set_link(soup,'canonical',url)
    set_meta(soup,'og:type','website',prop=True); set_meta(soup,'og:site_name','Fynzo',prop=True)
    set_meta(soup,'og:title',title,prop=True); set_meta(soup,'og:description',desc,prop=True); set_meta(soup,'og:url',url,prop=True)
    og=soup.find('meta',attrs={'property':'og:image'})
    image=og.get('content') if og and og.get('content') else DOMAIN+'og-default.png'
    if not image.startswith('http'): image=DOMAIN+image.lstrip('/')
    set_meta(soup,'og:image',image,prop=True)
    set_meta(soup,'twitter:card','summary_large_image'); set_meta(soup,'twitter:title',title); set_meta(soup,'twitter:description',desc); set_meta(soup,'twitter:image',image)
    schemas=[]
    if p.name=='index.html': schemas=homepage_schema(soup,desc)
    elif p.name.endswith(CALC_SUFFIXES) or p.name in SPECIAL_TOOLS:
        schemas=[calculator_schema(p,soup,title,desc),bread_schema(p,soup)]
        faq=visible_faq(soup)
        if faq: schemas.append({'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faq]})
    elif p.name.startswith('blog-'):
        h1=soup.find('h1').get_text(' ',strip=True); date='2026-07-31'
        schemas=[{'@context':'https://schema.org','@type':'Article','headline':h1,'description':desc,'image':image,'datePublished':date,'dateModified':date,'author':{'@type':'Person','name':'Yasser Chahir'},'publisher':{'@type':'Organization','name':'Fynzo','url':DOMAIN},'mainEntityOfPage':url},bread_schema(p,soup)]
    else:
        schemas=[{'@context':'https://schema.org','@type':'WebPage','name':title,'description':desc,'url':url,'isPartOf':{'@type':'WebSite','name':'Fynzo','url':DOMAIN}},bread_schema(p,soup)]
    replace_managed_schema(soup,schemas)
    p.write_text('<!DOCTYPE html>\n'+str(soup),encoding='utf-8')

for p in sorted(ROOT.glob('*.html')):
    if p.name not in ('404.html','offline.html'): normalize_page(p)
print('SEO first 10 normalized on',len(list(ROOT.glob('*.html')))-1,'indexable HTML pages')
