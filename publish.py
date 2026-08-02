# -*- coding: utf-8 -*-
"""
Fynzo auto-publisher. Run by GitHub Action daily (and works manually).
- Publishes any post in posts_data.py whose date <= today -> writes blog-<slug>.html
- Rebuilds blog.html listing (published posts only)
- Rebuilds sitemap.xml (core pages + published posts)
Idempotent: safe to run every day.
"""
import os, datetime
import json
from posts_data import POSTS

GAID="G-D7NJ4T2ZK4"
TODAY=datetime.date.today()

BRAND='<svg viewBox="0 0 64 64" fill="none"><rect x="6" y="6" width="52" height="52" rx="13" fill="#0b1020"/><rect x="15" y="14" width="34" height="10" rx="3.5" fill="#c8a45c"/><circle cx="21" cy="35" r="3.6" fill="#f7f8fa"/><circle cx="32" cy="35" r="3.6" fill="#f7f8fa"/><circle cx="21" cy="46" r="3.6" fill="#f7f8fa"/><path d="M28 49 L36 41 L42 46 L52 34" stroke="#c8a45c" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/><path d="M47 33 L53 34 L52 40 Z" fill="#c8a45c"/><circle cx="43" cy="46" r="4" fill="#1f8a70"/></svg>'
FBRAND='<svg viewBox="0 0 220 64" fill="none"><rect x="4" y="8" width="40" height="48" rx="9" fill="#1a2340"/><rect x="10" y="14" width="28" height="9" rx="3" fill="#c8a45c"/><circle cx="15" cy="33" r="3.2" fill="#fff"/><circle cx="24" cy="33" r="3.2" fill="#fff"/><circle cx="15" cy="43" r="3.2" fill="#fff"/><circle cx="24" cy="43" r="3.2" fill="#fff"/><path d="M30 48 L36 42 L40 46 L48 36" stroke="#c8a45c" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><path d="M44 34 L49 35 L48 40 Z" fill="#c8a45c"/><text x="60" y="42" font-family="Inter,sans-serif" font-size="30" font-weight="800"><tspan fill="#fff">Fynz</tspan><tspan fill="#c8a45c">o</tspan></text></svg>'
GA='<script async src="https://www.googletagmanager.com/gtag/js?id='+GAID+'"></script>\n<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","'+GAID+'");</script>'
HL='<link rel="alternate" hreflang="en" href="https://fynzo.me/{s}"/><link rel="alternate" hreflang="x-default" href="https://fynzo.me/{s}"/>'
NAV=('<header><nav><a class="brand" href="index.html">'+BRAND+'Fynzo</a><div class="nav-links">'
'<a href="index.html#tools">Calculators</a><a href="blog.html" style="color:var(--text)">Blog</a>'
'<a href="about.html">About</a><a href="contact.html">Contact</a>'
'<a href="index.html#tools" class="nav-btn">Start free</a></div></nav></header>')
FOOTER=('<footer><div class="wrap"><div class="foot"><div class="foot-brand">'+FBRAND+'<p>Free, fast, private calculators for the money and health decisions that matter.</p></div>'
'<div><h4>Tools</h4><a href="mortgage-calculator.html">Mortgage</a><a href="loan-calculator.html">Loan</a><a href="compound-interest-calculator.html">Compound interest</a><a href="bmi-calculator.html">BMI</a><a href="index.html#tools">All tools</a></div>'
'<div><h4>Company</h4><a href="about.html">About</a><a href="contact.html">Contact</a><a href="blog.html">Blog</a></div>'
'<div><h4>Legal</h4><a href="privacy.html">Privacy</a><a href="terms.html">Terms</a><a href="disclaimer.html">Disclaimer</a></div></div>'
'<div class="foot-bottom">&copy; 2026 Fynzo &middot; fynzo.me &middot; All calculators are educational estimates only.</div></div></footer>')
TAIL='<script defer src="fynzo.js"></script></body></html>'

def ld(*objs):
    return ''.join('<script type="application/ld+json">\n'+json.dumps(obj, ensure_ascii=False, separators=(',', ':'))+'\n</script>' for obj in objs if obj)

def head(t,d,slug,img,schema):
    # preload a WebP version of the page hero when available to improve LCP
    webp = img.rsplit('.',1)[0] + '.webp' if '.' in img else ''
    preload = f'<link rel="preload" as="image" href="https://fynzo.me/{webp}">' if webp and os.path.exists(webp) else ''
    return ('<!DOCTYPE html>\n<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">'
    f'<title>{t}</title><meta name="description" content="{d}"><meta name="robots" content="index, follow, max-image-preview:large">'
    f'<link rel="canonical" href="https://fynzo.me/{slug}">'+HL.format(s=slug)+
    '<link rel="icon" type="image/svg+xml" href="favicon.svg"><link rel="mask-icon" href="favicon.svg" color="#0b1020"><link rel="apple-touch-icon" href="favicon.svg"><link rel="manifest" href="site.webmanifest"><meta name="theme-color" content="#0b1020">'
    f'<meta property="og:type" content="article"><meta property="og:title" content="{t}"><meta property="og:description" content="{d}"><meta property="og:url" content="https://fynzo.me/{slug}"><meta property="og:image" content="https://fynzo.me/{img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">'
    +GA+'<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet"><link rel="stylesheet" href="styles.css">'
    f'\n{preload}\n{schema}\n</head><body>')

def build_post(p):
    slug="blog-"+p["slug"]+".html"
    d=datetime.date.fromisoformat(p["date"])
    disp=f"{d.day} {d.strftime('%B %Y')}" if hasattr(d,'strftime') else p["date"]
    schema=ld(
        {"@context":"https://schema.org","@type":"Article","headline":p["title"].replace('"',"'"),"image":"https://fynzo.me/"+p["img"],"description":p["meta"].replace('"',"'"),"author":{"@type":"Person","name":"Yasser Chahir"},"publisher":{"@type":"Organization","name":"Fynzo","url":"https://fynzo.me/","logo":{"@type":"ImageObject","url":"https://fynzo.me/logo-icon.svg"}},"datePublished":p["date"],"dateModified":str(TODAY),"mainEntityOfPage":"https://fynzo.me/"+slug,"inLanguage":"en","isAccessibleForFree":True},
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://fynzo.me/"},{"@type":"ListItem","position":2,"name":"Blog","item":"https://fynzo.me/blog.html"},{"@type":"ListItem","position":3,"name":p["title"].split(" (2026")[0].split(" (20")[0],"item":"https://fynzo.me/"+slug}]}
    )
    rel="".join('<a href="%s">%s</a>'%(u,t) for u,t in p["related"])
    html=head(p["title"],p["meta"],slug,p["img"],schema)+NAV
    html+='<article class="article"><div class="crumb"><a href="blog.html">&larr; Blog</a> &middot; '+p["cat"]+'</div>'
    html+='<div class="article-head"><div class="post-cat">'+p["cat"]+'</div><h1>'+p["title"].split(" (2026")[0].split(" (20")[0]+'</h1><div class="meta"><span>&#128197; '+disp+'</span><span>By Fynzo</span></div></div>'
    orig = p["img"]
    webp = orig.rsplit('.',1)[0]+'.webp' if '.' in orig else orig
    html += '<picture>'
    html += '<source type="image/webp" srcset="'+webp+'">'
    html += '<img class="article-hero" src="'+orig+'" alt="'+p["cat"]+'" width="1200" height="500" style="width:100%;height:auto;border-radius:18px;margin-bottom:28px">'
    html += '</picture>'
    html+='<p class="article-lead">'+p["lead"]+'</p>'+p["body"]
    html+='<div class="cta-box"><h3>Try it yourself</h3><p>Run your own numbers in seconds — free, no sign-up.</p><a href="'+p["cta_href"]+'" class="btn">'+p["cta_label"]+' &rarr;</a></div>'
    html+='<div class="callout"><p>&#9888; <strong>Remember:</strong> this is general educational information, not professional advice. See our <a href="disclaimer.html">disclaimer</a>.</p></div>'
    html+='</article><div class="related"><h3>Related tools &amp; reads</h3>'+rel+'</div>'+FOOTER+TAIL
    open(slug,"w").write(html)
    return slug

# thumbnails for blog index
def thumb(img,title):
    return '<div class="post-thumb" style="height:170px;padding:0;overflow:hidden"><img src="'+img+'" alt="'+title+'" style="width:100%;height:100%;object-fit:cover"></div>'

# original 5 posts that already exist (keep them in the listing)
ORIGINALS=[
 ("blog-how-much-house-can-i-afford.html","img/blog-mortgage.jpg","Mortgages","How much house can I afford? The honest math","The 28/36 rule, hidden costs, and your true budget."),
 ("blog-compound-interest-explained.html","img/blog-compound.jpg","Investing","Compound interest explained (with real examples)","Why starting 5 years earlier can double your money."),
 ("blog-pay-off-loan-faster.html","img/blog-loan.jpg","Loans","7 ways to pay off a loan faster","Save thousands in interest with small changes."),
 ("blog-how-to-calculate-bmi.html","img/blog-bmi.svg","Health","How to calculate your BMI","The formula, the categories, and what it means."),
 ("blog-how-many-calories-should-i-eat.html","img/blog-calorie.svg","Nutrition","How many calories should you eat?","Find your realistic daily target."),
]

def head_simple(t,d,slug):
    return ('<!DOCTYPE html>\n<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">'
    f'<title>{t}</title><meta name="description" content="{d}"><meta name="robots" content="index, follow, max-image-preview:large">'
    f'<link rel="canonical" href="https://fynzo.me/{slug}">'+HL.format(s=slug)+
    '<link rel="icon" type="image/svg+xml" href="favicon.svg"><link rel="mask-icon" href="favicon.svg" color="#0b1020"><link rel="apple-touch-icon" href="favicon.svg"><link rel="manifest" href="site.webmanifest"><meta name="theme-color" content="#0b1020">'
    +GA+'<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet"><link rel="stylesheet" href="styles.css">'
    f'<script type="application/ld+json">\n{json.dumps({"@context":"https://schema.org","@type":"WebPage","name":t,"description":d,"url":"https://fynzo.me/"+slug,"isPartOf":{"@type":"WebSite","name":"Fynzo","url":"https://fynzo.me/"}} , ensure_ascii=False, separators=(",", ":"))}\n</script></head><body>')

def rebuild_blog(published):
    # featured = newest published (from POSTS) or first original
    cards=""
    # newest first: published new posts reversed, then originals
    items=[]
    for p in reversed(published):
        items.append(("blog-"+p["slug"]+".html",p["img"],p["cat"],p["title"].split(" (20")[0],p["meta"][:90]+"..."))
    for o in ORIGINALS:
        items.append(o)
    # featured = first item
    feat=items[0] if items else None
    body=head_simple("Fynzo Blog - Money & Health Guides You Can Use","Practical, jargon-free guides on mortgages, loans, saving, investing and health, updated regularly.","blog.html")+NAV
    body+='<div class="page-head"><div class="wrap"><div class="eyebrow">The Fynzo Blog</div><h1>Money &amp; health, made simple.</h1><p class="updated">Practical guides - no jargon, just the numbers that matter. New posts every few days.</p></div></div>'
    body+='<div class="content">'
    if feat:
        body+='<div class="featured"><div><div class="post-cat">Featured &middot; '+feat[2]+'</div><h2>'+feat[3]+'</h2><p>'+feat[4]+'</p><a href="'+feat[0]+'" class="btn">Read the guide &rarr;</a></div><div class="featured-art" style="padding:0;overflow:hidden"><img src="'+feat[1]+'" alt="'+feat[3]+'" style="width:100%;height:100%;object-fit:cover;border-radius:18px"></div></div>'
    body+='<div class="blog-grid">'
    for it in items[1:]:
        body+='<a class="post-card" href="'+it[0]+'">'+thumb(it[1],it[3])+'<div class="post-body"><div class="post-cat">'+it[2]+'</div><h2>'+it[3]+'</h2><p>'+it[4]+'</p><div class="post-meta"><span>&#128197; 2026</span></div></div></a>'
    body+='</div></div>'+FOOTER+TAIL
    open("blog.html","w").write(body)

def rebuild_sitemap(published):
    core=['about.html','age-calculator.html','blog.html','bmi-calculator.html','body-fat-calculator.html','calorie-calculator.html','compound-interest-calculator.html','contact.html','date-difference-calculator.html','disclaimer.html','discount-calculator.html','fuel-cost-calculator.html','hourly-to-salary-calculator.html','ideal-weight-calculator.html','income-tax-calculator.html',"",'length-converter.html','loan-calculator.html','mortgage-calculator.html','password-generator.html','percentage-calculator.html','privacy.html','roi-calculator.html','sales-tax-calculator.html','savings-goal-calculator.html','temperature-converter.html','terms.html','tip-calculator.html','water-intake-calculator.html','blog-compound-interest-explained.html','blog-create-strong-passwords.html','blog-how-many-calories-should-i-eat.html','blog-how-much-house-can-i-afford.html','blog-how-much-to-save-each-month.html','blog-how-to-calculate-bmi.html','blog-master-percentages.html','blog-metric-vs-imperial.html','blog-pay-off-loan-faster.html','blog-understand-your-take-home-pay.html']
    urls=core+["blog-"+p["slug"]+".html" for p in published]
    sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        pr="1.0" if u=="" else ("0.8" if u.endswith("calculator.html") else "0.6")
        sm+=f'  <url><loc>https://fynzo.me/{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n'
    open("sitemap.xml","w").write(sm+'</urlset>\n')

def main():
    published=[p for p in POSTS if datetime.date.fromisoformat(p["date"])<=TODAY]
    new=0
    for p in published:
        slug="blog-"+p["slug"]+".html"
        if not os.path.exists(slug):
            build_post(p); new+=1; print("PUBLISHED:",slug)
    # always refresh listing + sitemap to reflect current published set
    rebuild_blog(published)
    rebuild_sitemap(published)
    print(f"Done. {len(published)} live, {new} newly published today ({TODAY}).")

if __name__=="__main__":
    main()
