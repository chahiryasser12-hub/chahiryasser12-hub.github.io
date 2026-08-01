#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
import json, re
ROOT=Path(__file__).resolve().parent
DOMAIN='https://fynzo.me/'
HUBS={'mortgage-guides.html','loan-guides.html','savings-guides.html','percentage-guides.html','health-calculators.html'}

def url(p): return DOMAIN if p.name=='index.html' else DOMAIN+p.name

def set_meta(soup,key,value,prop=False):
    attrs={'property':key} if prop else {'name':key}
    tags=soup.find_all('meta',attrs=attrs); tag=tags[0] if tags else soup.new_tag('meta')
    if not tags: tag.attrs.update(attrs); soup.head.append(tag)
    tag['content']=value
    for x in tags[1:]: x.decompose()

def schema_tag(soup,data):
    tag=soup.new_tag('script',type='application/ld+json'); tag['data-seo-stage']='11-20'; tag.string=json.dumps(data,ensure_ascii=False,separators=(',',':')); soup.head.append(tag)

def image_size(src):
    src=src.split('?')[0].split('#')[0]
    if src.startswith(DOMAIN): src=src[len(DOMAIN):]
    if src.startswith(('http://','https://','data:')): return None
    p=ROOT/src.lstrip('/')
    if not p.exists(): return None
    if p.suffix.lower()=='.svg':
        text=p.read_text(encoding='utf-8',errors='ignore')
        m=re.search(r'<svg[^>]*\bwidth=["\']([0-9.]+)',text); n=re.search(r'<svg[^>]*\bheight=["\']([0-9.]+)',text)
        if m and n: return int(float(m.group(1))),int(float(n.group(1)))
        vb=re.search(r'viewBox=["\']\s*[-0-9.]+\s+[-0-9.]+\s+([0-9.]+)\s+([0-9.]+)',text,re.I)
        if vb: return int(float(vb.group(1))),int(float(vb.group(2)))
    try:
        with Image.open(p) as im: return im.size
    except Exception: return None

def hub_schema(p,soup,desc):
    items=[]
    for a in soup.select('.pillar-card[href],.silo-card[href],a[href$="calculator.html"],a[href^="blog-"]'):
        href=a.get('href',''); name=a.get_text(' ',strip=True)
        if not href or not name: continue
        full=href if href.startswith('http') else DOMAIN+href.lstrip('/')
        if full not in [x['url'] for x in items]: items.append({'url':full,'name':name})
    return {'@context':'https://schema.org','@type':'CollectionPage','name':soup.title.get_text(' ',strip=True),'description':desc,'url':url(p),'mainEntity':{'@type':'ItemList','numberOfItems':len(items),'itemListElement':[{'@type':'ListItem','position':i+1,'name':x['name'],'url':x['url']} for i,x in enumerate(items)]}}

def fix_page(p):
    soup=BeautifulSoup(p.read_text(encoding='utf-8',errors='ignore'),'html.parser')
    if not soup.body: return
    # Accessibility and semantic HTML
    main=soup.find('main')
    if main: main['id']='main-content'
    else:
        candidate=soup.select_one('.hero,.page-head,.article,.blog-hero,.wrap')
        if candidate: candidate['id']='main-content'; candidate['role']='main'
    if not soup.select_one('.skip-link'):
        skip=soup.new_tag('a',href='#main-content'); skip['class']=['skip-link']; skip.string='Skip to main content'; soup.body.insert(0,skip)
    nav=soup.find('nav')
    if nav and not nav.get('aria-label'): nav['aria-label']='Primary navigation'
    for i,img in enumerate(soup.find_all('img')):
        if not img.has_attr('alt'): img['alt']=''
        src=img.get('src',''); dims=image_size(src)
        if dims and not img.get('width') and not img.get('height'): img['width']=str(dims[0]); img['height']=str(dims[1])
        above=i==0 and (p.name=='index.html' or p.name.startswith('blog-'))
        if above:
            img['loading']='eager'; img['fetchpriority']='high'
        elif not img.get('loading'): img['loading']='lazy'
        if not img.get('decoding'): img['decoding']='async'
    for form in soup.find_all('form'):
        form['aria-label']=form.get('aria-label','Fynzo form')
        for field in form.find_all(['input','select','textarea']):
            if field.get('type')=='hidden': continue
            fid=field.get('id')
            label=soup.find('label',attrs={'for':fid}) if fid else None
            if not label and not field.get('aria-label'):
                field['aria-label']=field.get('name') or field.get('placeholder') or 'Form field'
    for n,item in enumerate(soup.select('.faq-item')):
        q=item.select_one('.faq-q'); a=item.select_one('.faq-a')
        if q and a:
            aid=a.get('id') or f'faq-answer-{n+1}'; a['id']=aid; q['role']='button'; q['tabindex']='0'; q['aria-controls']=aid; q['aria-expanded']='false'
    # Canonical and social previews
    canonical=url(p)
    link=soup.find('link',rel=lambda x:x and 'canonical' in x)
    if link: link['href']=canonical
    set_meta(soup,'og:url',canonical,True)
    og=soup.find('meta',attrs={'property':'og:image'}); image=og.get('content','') if og else ''
    if image.endswith('.svg'): image=image[:-4]+'.png'
    if not image: image=DOMAIN+'og-default.png'
    set_meta(soup,'og:image',image,True); set_meta(soup,'og:image:width','1200',True); set_meta(soup,'og:image:height','630',True); set_meta(soup,'og:image:alt',(soup.find('h1') or soup.title).get_text(' ',strip=True),True)
    set_meta(soup,'twitter:image',image); set_meta(soup,'twitter:image:alt',(soup.find('h1') or soup.title).get_text(' ',strip=True))
    # Topic hub schema
    if p.name in HUBS:
        for t in list(soup.find_all('script',attrs={'data-seo-stage':'11-20'})): t.decompose()
        d=soup.find('meta',attrs={'name':'description'}); schema_tag(soup,hub_schema(p,soup,d.get('content','') if d else ''))
    p.write_text('<!DOCTYPE html>\n'+str(soup),encoding='utf-8')

for p in sorted(ROOT.glob('*.html')): fix_page(p)
print('SEO stages 11-20 applied to',len(list(ROOT.glob('*.html'))),'HTML pages')
