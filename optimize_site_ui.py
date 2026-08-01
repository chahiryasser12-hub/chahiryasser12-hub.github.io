#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup, Doctype
import json, re
ROOT=Path(__file__).resolve().parent
NEW={
'mortgage-total-cost-calculator.html':('finance','Mortgage Total Cost Calculator','Tax, insurance, PMI and HOA in one monthly estimate.','Housing','guide-mortgage-total-cost.svg','mortgage taxes insurance pmi hoa total housing cost'),
'mortgage-recast-calculator.html':('finance','Mortgage Recast Calculator','Estimate the payment after a lump-sum principal reduction.','Mortgage','guide-mortgage-recast.svg','mortgage recast lump sum new payment'),
'pay-raise-calculator.html':('finance','Pay Raise Calculator','Convert a raise into annual, monthly and weekly pay changes.','Income','guide-pay-raise.svg','pay raise salary increase monthly annual'),
'work-hours-calculator.html':('everyday','Work Hours Calculator','Calculate paid hours, breaks, overnight shifts and gross pay.','Work','guide-work-hours.svg','work hours shift break overnight gross pay'),
'auto-loan-calculator.html':('finance','Auto Loan Calculator','Car payment with tax, fees, down payment and trade-in.','Auto','calc-auto-loan.svg','auto car loan payment tax fees trade in'),
'credit-card-payoff-calculator.html':('finance','Credit Card Payoff Calculator','Estimate payoff time, interest and extra-payment savings.','Debt','calc-credit-card.svg','credit card payoff interest extra payment'),
'retirement-savings-calculator.html':('finance','Retirement Savings Calculator','Project contributions, growth and the target balance gap.','Savings','calc-retirement.svg','retirement savings target contributions growth'),
'home-affordability-calculator.html':('finance','Home Affordability Calculator','Estimate a home price from income, debt and housing costs.','Housing','calc-home-affordability.svg','home house affordability income debt dti'),
'loan-comparison-calculator.html':('finance','Loan Comparison Calculator','Compare two offers by payment, fees and total cost.','Loans','calc-loan-comparison.svg','loan comparison rates term fees total cost'),
'net-worth-calculator.html':('finance','Net Worth Calculator','Add assets and subtract mortgages, loans and other debts.','Planning','calc-net-worth.svg','net worth assets liabilities debts'),
'break-even-calculator.html':('everyday','Break-Even Calculator','Calculate break-even units, revenue, margin and profit.','Business','calc-break-even.svg','break even business fixed variable cost profit'),
'gpa-calculator.html':('everyday','GPA Calculator','Calculate a credit-weighted GPA on a standard 4.0 scale.','Education','calc-gpa.svg','gpa grade credits education school college')}

def save(p,s):
 for n in list(s.contents):
  if isinstance(n,Doctype): n.extract()
 p.write_text('<!DOCTYPE html>\n'+str(s),encoding='utf-8')

def new_card(s,href,data):
 cat,title,desc,badge,icon,keywords=data
 a=s.new_tag('a',href=href); a['class']=['tool']; a['data-cat']=cat; a['data-keywords']=keywords; a['data-catalog-tool']='true'
 ic=s.new_tag('div'); ic['class']=['ic']; img=s.new_tag('img',src=icon,alt='',width='40',height='40',loading='lazy',decoding='async'); ic.append(img); a.append(ic)
 h=s.new_tag('h3'); h.string=title; a.append(h); p=s.new_tag('p'); p.string=desc; a.append(p); b=s.new_tag('span'); b['class']=['badge']; b.string=badge; a.append(b); return a

p=ROOT/'index.html'; s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
# Keep one canonical calculator discovery area. Remove every secondary calculator showcase.
for sel in ['#popular-tools','[data-seo-calculator-expansion]','[data-opportunity-tools]']:
 for x in s.select(sel): x.decompose()
# Remove accidental free-standing wrap between tools and old sections if empty/utility-only.
for x in list(s.body.find_all('div',class_='wrap',recursive=False)):
 if not x.get_text(' ',strip=True): x.decompose()
sec=s.select_one('#tools'); grid=s.select_one('#grid')
# Add all new calculators to the existing canonical catalog.
existing={a.get('href') for a in grid.select('.tool')}
for href,data in NEW.items():
 if href not in existing and (ROOT/href).exists(): grid.append(new_card(s,href,data))
# Add scroll controls and compact status.
old=s.select_one('.catalog-controls')
if old: old.decompose()
controls=s.new_tag('div'); controls['class']=['catalog-controls']; status=s.new_tag('p',id='catalogStatus'); status['class']=['catalog-status']; controls.append(status)
buttons=s.new_tag('div'); buttons['class']=['catalog-arrows']
for ident,label,arrow in [('catalogPrev','Previous calculators','←'),('catalogNext','Next calculators','→')]:
 b=s.new_tag('button',id=ident,type='button'); b['class']=['catalog-arrow']; b['aria-label']=label; b.string=arrow; buttons.append(b)
controls.append(buttons); grid.insert_before(controls)
grid['tabindex']='0'; grid['aria-label']='Calculator catalog. Scroll horizontally to browse more tools.'; grid['data-horizontal-catalog']='true'
# Better heading text.
head=sec.select_one('.sec-head p')
if head: head.string='Search or filter the complete calculator collection. Eight tools are visible at a time; use the arrows, swipe or horizontal scrollbar to browse the rest.'
# Replace legacy inline catalog script and remove duplicate inline FAQ click binding.
for script in s.find_all('script'):
 txt=script.string or ''
 if 'var af="all"' in txt:
  script.string='''\nvar af="all",gr=document.getElementById("grid"),si=document.getElementById("calcSearch"),sc=document.getElementById("searchClear"),nr=null;\nfunction visibleTools(){return Array.prototype.filter.call(gr.querySelectorAll(".tool"),function(t){return !t.hidden;});}\nfunction updateCatalogStatus(){var v=visibleTools(),st=document.getElementById("catalogStatus");if(st)st.textContent=v.length+" calculator"+(v.length===1?"":"s")+" available · 8 visible at a time";}\nfunction applyCatalog(){var q=(si.value||"").trim().toLowerCase(),shown=0;gr.querySelectorAll(".tool").forEach(function(t){var title=(t.querySelector("h3")?t.querySelector("h3").textContent:"").toLowerCase(),kw=(t.dataset.keywords||"").toLowerCase(),okCat=(af==="all"||t.dataset.cat===af),okQuery=(!q||title.indexOf(q)>-1||kw.indexOf(q)>-1),show=okCat&&okQuery;t.hidden=!show;if(show)shown++;});if(nr){nr.remove();nr=null;}if(!shown){nr=document.createElement("div");nr.className="no-results";nr.innerHTML='No calculator found for <b>"'+si.value+'"</b>.<br>Try another word or <a href="contact.html">suggest one</a>.';gr.appendChild(nr);}sc.classList.toggle("show",!!q);gr.scrollTo({left:0,behavior:"smooth"});updateCatalogStatus();}\ndocument.querySelectorAll(".filter").forEach(function(f){f.type="button";f.onclick=function(){document.querySelectorAll(".filter").forEach(function(x){x.classList.remove("active");x.setAttribute("aria-pressed","false");});f.classList.add("active");f.setAttribute("aria-pressed","true");af=f.dataset.filter;applyCatalog();};f.setAttribute("aria-pressed",f.classList.contains("active")?"true":"false");});\nsi.addEventListener("input",applyCatalog);sc.type="button";sc.addEventListener("click",function(){si.value="";si.focus();applyCatalog();});si.addEventListener("keydown",function(e){if(e.key==="Enter"){var first=visibleTools()[0];if(first&&first.href)location.href=first.href;}});\ndocument.getElementById("catalogPrev").addEventListener("click",function(){gr.scrollBy({left:-Math.max(320,gr.clientWidth*.85),behavior:"smooth"});});document.getElementById("catalogNext").addEventListener("click",function(){gr.scrollBy({left:Math.max(320,gr.clientWidth*.85),behavior:"smooth"});});\nupdateCatalogStatus();\n'''
# Rebuild ItemList schema from canonical catalog only.
for script in s.find_all('script',attrs={'type':'application/ld+json'}):
 try: data=json.loads(script.string or '{}')
 except: continue
 if data.get('@type')=='ItemList':
  cards=grid.select('.tool'); data['numberOfItems']=len(cards); data['itemListElement']=[{'@type':'ListItem','position':i,'name':a.select_one('h3').get_text(' ',strip=True),'url':'https://fynzo.me/'+a.get('href')} for i,a in enumerate(cards,1)]; script.string=json.dumps(data,separators=(',',':'))
save(p,s)
# Remove secondary duplicated calculator suggestion blocks across internal pages.
for p in ROOT.glob('*.html'):
 if p.name=='index.html': continue
 s=BeautifulSoup(p.read_text(encoding='utf-8',errors='ignore'),'html.parser'); changed=False
 for sel in ['[data-seo-expansion-links]']:
  for x in s.select(sel): x.decompose(); changed=True
 # Remove legacy inline FAQ handlers. Global delegated handling lives in fynzo.js.
 for script in s.find_all('script'):
  if not script.string: continue
  cleaned=re.sub(r'document\.querySelectorAll\("\.faq-item"\)\.forEach\(function\(it\)\{it\.onclick=function\(\)\{it\.classList\.toggle\("open"\);\};\}\);','',script.string)
  if cleaned!=script.string: script.string=cleaned; changed=True
 # Remove exact duplicate recommendation sections if same href set appears more than once.
 seen=set()
 for secx in list(s.select('.focused-recommendations,.seo-tool-showcase')):
  hrefs=tuple(sorted(a.get('href','') for a in secx.select('a[href]')))
  if hrefs and hrefs in seen: secx.decompose(); changed=True
  elif hrefs: seen.add(hrefs)
 if changed: save(p,s)
print('Homepage catalog rebuilt with',len(BeautifulSoup((ROOT/'index.html').read_text(),'html.parser').select('#grid .tool')),'unique tools; duplicate showcases removed.')
