#!/usr/bin/env python3
"""Publish at most one due Fynzo article per run, then refresh blog.html and sitemap.xml."""
from pathlib import Path
from datetime import date
from bs4 import BeautifulSoup
from html import escape
import argparse, json, os, re

ROOT=Path(__file__).resolve().parent
DOMAIN='https://fynzo.me/'
DATA=ROOT/'scheduled_posts.json'
TEMPLATE=ROOT/'blog-compound-interest-explained.html'

def read_posts(): return json.loads(DATA.read_text(encoding='utf-8'))
def article_filename(p): return f"blog-{p['slug']}.html"

def add_text(parent, name, text, cls=None):
    tag=BeautifulSoup('', 'html.parser').new_tag(name)
    if cls: tag['class']=[cls]
    tag.string=text
    parent.append(tag)
    return tag

def render_article(p):
    soup=BeautifulSoup(TEMPLATE.read_text(encoding='utf-8'),'html.parser')
    fn=article_filename(p); url=DOMAIN+fn; desc=p['lead'][:155].rstrip()
    soup.title.string=p['title']+' | Fynzo'
    for tag in soup.find_all('meta'):
        key=tag.get('name') or tag.get('property')
        if key=='description': tag['content']=desc
        elif key in ('og:title','twitter:title'): tag['content']=p['title']+' | Fynzo'
        elif key in ('og:description','twitter:description'): tag['content']=desc
        elif key=='og:url': tag['content']=url
        elif key in ('og:image','twitter:image'): tag['content']=DOMAIN+p['image']
    canonical=soup.find('link',rel=lambda x:x and 'canonical' in x)
    if canonical: canonical['href']=url
    alternate=soup.find_all('link',rel=lambda x:x and 'alternate' in x)
    for tag in alternate: tag.decompose()
    # Article schema
    for tag in list(soup.find_all('script',attrs={'type':'application/ld+json'})): tag.decompose()
    schema=soup.new_tag('script',type='application/ld+json')
    schema.string=json.dumps({'@context':'https://schema.org','@type':'Article','headline':p['title'],'description':desc,'image':DOMAIN+p['image'],'datePublished':p['publish_date'],'dateModified':p['publish_date'],'author':{'@type':'Person','name':'Yasser Chahir'},'publisher':{'@type':'Organization','name':'Fynzo'},'mainEntityOfPage':url},ensure_ascii=False)
    soup.head.append(schema)
    article=soup.select_one('.article')
    if not article: raise RuntimeError('Article template has no .article element')
    article.clear()
    head=soup.new_tag('div'); head['class']=['article-head']
    add_text(head,'div',p['category'],'post-cat')
    add_text(head,'h1',p['title'])
    meta=soup.new_tag('div'); meta['class']=['meta']
    for value in (p['publish_date'],'9 min read','Reviewed by Yasser Chahir'):
        add_text(meta,'span',value)
    head.append(meta); article.append(head)
    figure=soup.new_tag('figure'); figure['class']=['article-cover-svg']
    cover=soup.new_tag('img',src=p.get('card_image',p['image']),alt=p['title']); cover['width']='1200'; cover['height']='630'; cover['loading']='eager'; cover['decoding']='async'
    figure.append(cover); article.append(figure)
    add_text(article,'p',p['lead'],'article-lead')
    add_text(article,'h2','The key idea')
    add_text(article,'p',p['concept'])
    add_text(article,'p','A calculator is most useful when every input uses the same units and the assumptions match the decision being considered. Keep a copy of the inputs, change one variable at a time, and compare the full result rather than one headline number.')
    add_text(article,'h2','Worked example')
    add_text(article,'p',p['example'])
    add_text(article,'p','The example is intentionally simplified so the effect of the main variable is easy to see. Real outcomes may include fees, taxes, changing rates, medical circumstances or other factors described in the calculator limitations.')
    add_text(article,'h2','Quick reference')
    table=soup.new_tag('table'); table['class']=['article-table']
    tr=soup.new_tag('tr')
    for x in ('Item','What it means'): add_text(tr,'th',x)
    table.append(tr)
    for a,b in p['table']:
        tr=soup.new_tag('tr'); add_text(tr,'td',a); add_text(tr,'td',b); table.append(tr)
    article.append(table)
    add_text(article,'h2','Common mistakes')
    ul=soup.new_tag('ul')
    for x in p['mistakes']: add_text(ul,'li',x)
    article.append(ul)
    add_text(article,'p','These mistakes usually happen when two scenarios use different assumptions or when a general estimate is treated as an official quote, diagnosis or legal determination. Write down the assumptions before comparing results.')
    add_text(article,'h2','A practical step-by-step method')
    ol=soup.new_tag('ol')
    for x in p['steps']: add_text(ol,'li',x)
    article.append(ol)
    add_text(article,'h2','How to interpret the result responsibly')
    add_text(article,'p','Use the result as a planning aid. Test a cautious scenario as well as an optimistic one, and pay attention to the limitations stated on the calculator page. Important health, borrowing, tax, legal or investment decisions deserve current official information and qualified professional advice.')
    add_text(article,'p','Review the calculation again when a rate, deadline, income, price, measurement or personal circumstance changes. A transparent estimate that is updated is more useful than a precise-looking number based on old inputs.')
    cta=soup.new_tag('div'); cta['class']=['cta-box']
    add_text(cta,'h3','Run your own numbers')
    add_text(cta,'p','Use the related Fynzo calculator, save two scenarios and compare the result.')
    a=soup.new_tag('a',href=p['calculator']); a['class']=['btn']; a.string='Open the related calculator →'; cta.append(a); article.append(cta)
    add_text(article,'h2','Sources and review note')
    ul=soup.new_tag('ul')
    for url,name in p['sources']:
        li=soup.new_tag('li'); a=soup.new_tag('a',href=url,target='_blank',rel='noopener noreferrer'); a.string=name; li.append(a); ul.append(li)
    article.append(ul)
    add_text(article,'p',p['disclaimer'])
    info=soup.new_tag('p')
    strong=soup.new_tag('strong'); strong.string='Reviewed by: '; info.append(strong); info.append(p['reviewer']+'. ')
    strong=soup.new_tag('strong'); strong.string='Last reviewed: '; info.append(strong); info.append(p['publish_date']+'.')
    article.append(info)
    related=soup.select_one('.related, .arel')
    if related:
        related.clear(); related['class']=['related','arel','related-fixed']
        add_text(related,'h3','Related tools & reads')
        links=[(p['calculator'],'Open the related calculator'),('blog.html','Browse all Fynzo guides'),('index.html','Explore all calculators')]
        for href,label in links:
            a=soup.new_tag('a',href=DOMAIN+href); a['rel']='noopener'; a.string=label; related.append(a)
    return '<!DOCTYPE html>\n'+str(soup)

def article_info(path):
    s=BeautifulSoup(path.read_text(encoding='utf-8',errors='ignore'),'html.parser')
    h=s.find('h1'); title=h.get_text(' ',strip=True) if h else path.stem
    cat=s.select_one('.post-cat, .bcat'); category=cat.get_text(' ',strip=True) if cat else 'Guide'
    desc=s.find('meta',attrs={'name':'description'}); description=desc.get('content','') if desc else ''
    cover=s.select_one('.article-cover-svg img')
    if cover: image=cover.get('src','og-default.png')
    else:
        image_tag=s.find('meta',attrs={'property':'og:image'}); image=(image_tag.get('content','').split('/')[-1] if image_tag else 'og-default.png')
    schema=s.find('script',attrs={'type':'application/ld+json'}); published='2026-07-31'
    if schema:
        try: published=json.loads(schema.string or '{}').get('datePublished',published)
        except Exception: pass
    return {'file':path.name,'title':title,'category':category,'description':description[:120],'image':image,'date':published}

def rebuild_blog():
    path=ROOT/'blog.html'; soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
    grid=soup.select_one('.blog-grid, .bgrid')
    if not grid: raise RuntimeError('blog.html has no blog grid')
    items=[article_info(p) for p in ROOT.glob('blog-*.html')]
    items.sort(key=lambda x:(x['date'],x['file']),reverse=True)
    grid.clear()
    for x in items:
        card=soup.new_tag('a',href=x['file']); card['class']=['post-card']
        thumb=soup.new_tag('div'); thumb['class']=['post-thumb']; thumb['style']='height:170px;padding:0;overflow:hidden'
        img=soup.new_tag('img',src=x['image'],alt=x['title']); img['style']='width:100%;height:100%;object-fit:cover'; thumb.append(img); card.append(thumb)
        body=soup.new_tag('div'); body['class']=['post-body']
        add_text(body,'div',x['category'],'post-cat'); add_text(body,'h2',x['title']); add_text(body,'p',x['description'])
        meta=soup.new_tag('div'); meta['class']=['post-meta']; add_text(meta,'span',x['date']); body.append(meta); card.append(body); grid.append(card)
    path.write_text('<!DOCTYPE html>\n'+str(soup),encoding='utf-8')

def rebuild_sitemap():
    from xml.sax.saxutils import escape as xe
    files=[]
    for p in ROOT.glob('*.html'):
        if p.name=='404.html': continue
        s=BeautifulSoup(p.read_text(encoding='utf-8',errors='ignore'),'html.parser')
        robots=s.find('meta',attrs={'name':'robots'})
        if robots and 'noindex' in robots.get('content','').lower(): continue
        loc=DOMAIN if p.name=='index.html' else DOMAIN+p.name
        last=date.today().isoformat()
        if p.name.startswith('blog-'):
            info=article_info(p); last=info['date']
        pr='1.0' if p.name=='index.html' else ('0.8' if p.name.endswith(('calculator.html','converter.html')) or p.name=='password-generator.html' else '0.6')
        files.append((loc,last,pr))
    lines=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc,last,pr in sorted(files): lines.append(f'  <url><loc>{xe(loc)}</loc><lastmod>{last}</lastmod><priority>{pr}</priority></url>')
    lines.append('</urlset>'); (ROOT/'sitemap.xml').write_text('\n'.join(lines)+'\n',encoding='utf-8')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--date',default=os.getenv('PUBLISH_DATE',date.today().isoformat())); ap.add_argument('--rebuild-only',action='store_true'); args=ap.parse_args()
    today=date.fromisoformat(args.date); posts=read_posts(); published=None
    if not args.rebuild_only:
        due=[p for p in posts if date.fromisoformat(p['publish_date'])<=today and not (ROOT/article_filename(p)).exists()]
        due.sort(key=lambda p:p['publish_date'])
        if due:
            published=due[0]; (ROOT/article_filename(published)).write_text(render_article(published),encoding='utf-8')
            print('PUBLISHED',article_filename(published),published['publish_date'])
        else: print('NO DUE ARTICLE')
    rebuild_blog(); rebuild_sitemap()
    print('BLOG AND SITEMAP REFRESHED')
if __name__=='__main__': main()
