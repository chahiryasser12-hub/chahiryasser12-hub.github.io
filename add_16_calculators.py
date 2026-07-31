#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import date
import json, re
ROOT=Path(__file__).resolve().parent
D='https://fynzo.me/'
TODAY='July 31, 2026'

TOOLS=[
('debt-payoff-calculator.html','Debt Payoff Calculator','finance','Estimate payoff time and interest with a fixed monthly payment.',[('balance','Debt balance ($)',10000),('rate','Interest rate (%)',18),('payment','Monthly payment ($)',350)],"debtPayoff(v.balance,v.rate,v.payment)",'credit card debt payoff snowball avalanche interest'),
('extra-mortgage-payment-calculator.html','Extra Mortgage Payment Calculator','finance','See how extra principal payments may reduce time and interest.',[('balance','Mortgage balance ($)',250000),('rate','Interest rate (%)',6),('years','Years remaining',30),('extra','Extra monthly payment ($)',200)],"extraMortgage(v.balance,v.rate,v.years,v.extra)",'mortgage extra payment principal payoff'),
('apr-calculator.html','APR Calculator','finance','Estimate APR from amount, fees, payment and term.',[('amount','Amount received ($)',10000),('fees','Upfront fees ($)',300),('payment','Monthly payment ($)',220),('months','Number of months',60)],"aprCalc(v.amount,v.fees,v.payment,v.months)",'apr annual percentage rate fees loan'),
('emergency-fund-calculator.html','Emergency Fund Calculator','finance','Estimate an emergency fund target from essential monthly expenses.',[('expenses','Essential monthly expenses ($)',2500),('months','Months of coverage',6),('saved','Already saved ($)',4000)],"simpleFund(v.expenses,v.months,v.saved)",'emergency fund savings expenses months'),
('budget-percentage-calculator.html','Budget Percentage Calculator','finance','See what percentage of income goes to each budget category.',[('income','Monthly take-home income ($)',4000),('housing','Housing ($)',1400),('needs','Other needs ($)',900),('wants','Wants ($)',700),('savings','Savings and debt ($)',1000)],"budgetPct(v)",'budget percentage 50 30 20 income expenses'),
('savings-interest-calculator.html','Savings Interest Calculator','finance','Estimate savings growth with deposits and compound interest.',[('initial','Starting balance ($)',5000),('monthly','Monthly deposit ($)',250),('rate','Annual interest rate (%)',4),('years','Years',5)],"savingsInterest(v.initial,v.monthly,v.rate,v.years)",'savings interest apy deposits compound'),
('rent-vs-buy-calculator.html','Rent vs Buy Calculator','finance','Compare simplified long-term renting and home-buying costs.',[('rent','Monthly rent ($)',1800),('price','Home price ($)',350000),('down','Down payment (%)',20),('rate','Mortgage rate (%)',6),('years','Comparison years',7)],"rentBuy(v)",'rent versus buy home mortgage comparison'),
('debt-to-income-calculator.html','Debt-to-Income Ratio Calculator','finance','Calculate monthly debt-to-income ratio from income and debt payments.',[('income','Gross monthly income ($)',6000),('housing','Housing payment ($)',1800),('debts','Other monthly debts ($)',600)],"dti(v.income,v.housing,v.debts)",'dti debt to income ratio mortgage'),
('price-per-unit-calculator.html','Price per Unit Calculator','everyday','Compare package prices using cost per unit.',[('price1','Option A price ($)',12),('qty1','Option A quantity',8),('price2','Option B price ($)',16),('qty2','Option B quantity',12)],"unitPrice(v)",'unit price grocery comparison value'),
('markup-margin-calculator.html','Markup and Margin Calculator','everyday','Calculate selling price, markup and gross margin.',[('cost','Cost ($)',60),('price','Selling price ($)',100)],"markupMargin(v.cost,v.price)",'markup margin profit selling price business'),
('grade-percentage-calculator.html','Grade Percentage Calculator','everyday','Calculate a score percentage and general letter grade.',[('earned','Points earned',82),('possible','Points possible',100)],"grade(v.earned,v.possible)",'grade percentage score marks exam'),
('time-duration-calculator.html','Time Duration Calculator','everyday','Calculate elapsed time between two times.',[('start','Start time','09:15','time'),('end','End time','17:45','time'),('breaks','Break minutes',30)],"duration(v.start,v.end,v.breaks)",'time duration hours minutes work shift'),
('business-days-calculator.html','Business Days Calculator','everyday','Count weekdays between two dates, excluding weekends.',[('start','Start date','2026-08-03','date'),('end','End date','2026-08-31','date')],"businessDays(v.start,v.end)",'business days weekdays working days date'),
('pace-calculator.html','Pace Calculator','health','Calculate running or walking pace, speed and finish-time estimates.',[('distance','Distance (km)',10),('hours','Hours',0),('minutes','Minutes',55),('seconds','Seconds',0)],"pace(v)",'running walking pace speed minutes per km'),
('waist-to-height-ratio-calculator.html','Waist-to-Height Ratio Calculator','health','Estimate waist-to-height ratio from matching units.',[('waist','Waist circumference (cm)',82),('height','Height (cm)',175)],"wthr(v.waist,v.height)",'waist height ratio health screening'),
('protein-intake-estimator.html','Protein Intake Estimator','health','Estimate a general daily protein range from body weight and activity.',[('weight','Body weight (kg)',70),('activity','Activity level','moderate','select',[('low','Low'),('moderate','Moderate'),('high','High')])],"protein(v.weight,v.activity)",'protein intake per day weight activity nutrition')]

JS=r'''
const money=n=>'$'+Number(n).toLocaleString('en-US',{maximumFractionDigits:2});
const num=n=>Number(n).toLocaleString('en-US',{maximumFractionDigits:2});
function result(big,label,rows){return {big,label,rows};}
function debtPayoff(b,rate,p){let r=rate/1200;if(p<=b*r)return result('Payment too low','Payoff warning',[['Monthly interest',money(b*r)]]);let m=r?Math.ceil(-Math.log(1-b*r/p)/Math.log(1+r)):Math.ceil(b/p),bal=b,int=0;for(let i=0;i<m&&bal>0;i++){let x=bal*r;int+=x;bal=Math.max(0,bal+x-p)}return result(m+' months','Estimated payoff time',[['Total interest',money(int)],['Total paid',money(b+int)]]);}
function extraMortgage(b,rate,y,extra){let r=rate/1200,n=y*12,base=r?b*r*Math.pow(1+r,n)/(Math.pow(1+r,n)-1):b/n;let bal=b,m=0,int=0;while(bal>0&&m<1200){let x=bal*r;int+=x;bal=Math.max(0,bal+x-base-extra);m++}let normal=base*n-b;return result(m+' months','Estimated payoff with extra',[['Regular payment',money(base)],['Interest saved',money(Math.max(0,normal-int))],['Time saved',Math.max(0,n-m)+' months']]);}
function aprCalc(amount,fees,payment,months){let net=amount-fees,lo=0,hi=1;for(let k=0;k<80;k++){let r=(lo+hi)/2,pv=r?payment*(1-Math.pow(1+r,-months))/r:payment*months;if(pv>net)lo=r;else hi=r}let apr=(Math.pow(1+(lo+hi)/2,12)-1)*100;return result(num(apr)+'%','Estimated APR',[['Amount received',money(net)],['Total payments',money(payment*months)]]);}
function simpleFund(e,m,s){let target=e*m,gap=Math.max(0,target-s);return result(money(target),'Emergency fund target',[['Funding gap',money(gap)],['Current coverage',num(s/e)+' months']]);}
function budgetPct(v){let total=v.housing+v.needs+v.wants+v.savings, pct=x=>num(x/v.income*100)+'%';return result(pct(total),'Income allocated',[['Housing',pct(v.housing)],['Other needs',pct(v.needs)],['Wants',pct(v.wants)],['Savings and debt',pct(v.savings)],['Unallocated',money(v.income-total)]]);}
function savingsInterest(initial,monthly,rate,years){let r=rate/1200,n=years*12,fv=initial*Math.pow(1+r,n)+(r?monthly*(Math.pow(1+r,n)-1)/r:monthly*n),con=initial+monthly*n;return result(money(fv),'Estimated future balance',[['Contributions',money(con)],['Interest earned',money(fv-con)]]);}
function rentBuy(v){let months=v.years*12,loan=v.price*(1-v.down/100),r=v.rate/1200,n=360,p=r?loan*r*Math.pow(1+r,n)/(Math.pow(1+r,n)-1):loan/n,rent=v.rent*months,buy=p*months+v.price*v.down/100;return result(rent<buy?'Renting costs less':'Buying cash outflow is lower','Simplified comparison',[['Rent paid',money(rent)],['Down payment + mortgage payments',money(buy)],['Important','Excludes appreciation, taxes, insurance, maintenance and selling costs']]);}
function dti(i,h,d){let front=h/i*100,back=(h+d)/i*100;return result(num(back)+'%','Total debt-to-income ratio',[['Housing ratio',num(front)+'%'],['Monthly debt payments',money(h+d)]]);}
function unitPrice(v){let a=v.price1/v.qty1,b=v.price2/v.qty2;return result(a<b?'Option A':'Option B','Lower unit price',[['Option A',money(a)+' per unit'],['Option B',money(b)+' per unit'],['Difference',money(Math.abs(a-b))+' per unit']]);}
function markupMargin(c,p){let profit=p-c;return result(num(profit/p*100)+'%','Gross margin',[['Markup',num(profit/c*100)+'%'],['Profit',money(profit)]]);}
function grade(e,p){let x=e/p*100,l=x>=90?'A':x>=80?'B':x>=70?'C':x>=60?'D':'F';return result(num(x)+'%','Grade percentage',[['General letter grade',l],['Points missing',num(Math.max(0,p-e))]]);}
function duration(s,e,b){let [sh,sm]=s.split(':').map(Number),[eh,em]=e.split(':').map(Number),mins=eh*60+em-sh*60-sm;if(mins<0)mins+=1440;mins=Math.max(0,mins-b);return result(Math.floor(mins/60)+'h '+mins%60+'m','Net duration',[['Decimal hours',num(mins/60)],['Break deducted',b+' minutes']]);}
function businessDays(a,b){let d=new Date(a+'T00:00:00'),end=new Date(b+'T00:00:00'),n=0;if(d>end)[d,end]=[end,d];while(d<=end){let x=d.getDay();if(x!==0&&x!==6)n++;d.setDate(d.getDate()+1)}return result(n+' days','Weekdays including both dates',[['Weekends','Excluded'],['Public holidays','Not automatically excluded']]);}
function pace(v){let secs=v.hours*3600+v.minutes*60+v.seconds,pk=secs/v.distance,speed=v.distance/(secs/3600);return result(Math.floor(pk/60)+':'+String(Math.round(pk%60)).padStart(2,'0')+' /km','Average pace',[['Average speed',num(speed)+' km/h'],['5 km at this pace',Math.floor(pk*5/60)+':'+String(Math.round(pk*5%60)).padStart(2,'0')]]);}
function wthr(w,h){let x=w/h;return result(num(x),'Waist-to-height ratio',[['Percentage',num(x*100)+'%'],['Interpretation','Use as general screening context, not a diagnosis']]);}
function protein(w,a){let ranges={low:[0.8,1],moderate:[1.2,1.6],high:[1.6,2.2]},r=ranges[a];return result(Math.round(w*r[0])+'–'+Math.round(w*r[1])+' g/day','General daily protein range',[['Per kilogram',r[0]+'–'+r[1]+' g/kg'],['Note','Needs vary with health, age and goals']]);}
function run(){let v={};document.querySelectorAll('#fx [data-k]').forEach(el=>v[el.dataset.k]=el.type==='number'?Number(el.value):el.value);let r=CALC(v),h='<div class="rlabel">'+r.label+'</div><div class="rbig">'+r.big+'</div>';r.rows.forEach(x=>h+='<div class="rrow"><span>'+x[0]+'</span><span>'+x[1]+'</span></div>');document.getElementById('res').innerHTML=h;window.lastResult=r;}
document.querySelectorAll('#fx [data-k]').forEach(el=>el.addEventListener('input',run));document.getElementById('cr').onclick=()=>navigator.clipboard.writeText(document.querySelector('h1').textContent+': '+window.lastResult.big);document.getElementById('pr').onclick=()=>print();run();document.querySelectorAll('.faq-item').forEach(x=>x.onclick=()=>x.classList.toggle('open'));
'''

def fields_html(fields):
 out=[]
 for f in fields:
  k,label,val=f[:3];typ=f[3] if len(f)>3 else 'number'
  if typ=='select':
   opts=''.join(f'<option value="{v}"'+(' selected' if v==val else '')+f'>{t}</option>' for v,t in f[4])
   out.append(f'<div class="field"><label for="{k}">{label}</label><select id="{k}" data-k="{k}">{opts}</select></div>')
  else:
   step=' step="any"' if typ=='number' else ''
   out.append(f'<div class="field"><label for="{k}">{label}</label><input id="{k}" data-k="{k}" type="{typ}" value="{val}"{step}></div>')
 return ''.join(out)

def page_html(t):
 fn,name,cat,desc,fields,call,keywords=t
 category={'finance':'Finance','everyday':'Everyday math','health':'General health'}[cat]
 caution=' This is an educational estimate, not professional advice.' if cat in ('finance','health') else ''
 schema=json.dumps({'@context':'https://schema.org','@type':'WebApplication','name':name,'url':D+fn,'applicationCategory':'FinanceApplication' if cat=='finance' else 'UtilitiesApplication','operatingSystem':'Any','offers':{'@type':'Offer','price':'0','priceCurrency':'USD'},'description':desc})
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{name}: Instant Estimate | Fynzo</title><meta name="description" content="{desc} Get an instant result with formulas, assumptions, limitations and examples."><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{D}{fn}"><meta property="og:type" content="website"><meta property="og:title" content="{name}: Instant Estimate | Fynzo"><meta property="og:description" content="{desc}"><meta property="og:url" content="{D}{fn}"><link rel="icon" href="favicon.svg"><link rel="stylesheet" href="styles.css"><script type="application/ld+json">{schema}</script></head><body>
<header><nav><a class="brand" href="index.html">🧮 Fynzo</a><div class="nav-links"><a href="index.html#tools">Calculators</a><a href="blog.html">Blog</a><a href="about.html">About</a><a class="nav-btn" href="index.html#tools">All tools</a></div></nav></header>
<nav class="crumb"><a href="index.html">Home</a> · <a href="index.html#tools">{category}</a> · {name}</nav><div class="page-head"><div class="wrap"><div class="eyebrow">{category} tool</div><h1>{name}</h1><p class="updated">{desc} No sign-up, and the calculation stays in your browser.</p></div></div>
<main><section class="sec" style="padding-top:36px"><div class="wrap"><div class="calc-wrap"><div id="fx">{fields_html(fields)}</div><div><div class="result" id="res" aria-live="polite"></div><div class="calc-actions"><button class="act-btn" id="cr">Copy result</button><button class="act-btn" id="pr">Save PDF</button></div><div class="result-context"><h3>How to read this result</h3><p>The estimate changes immediately when an input changes.{caution}</p></div></div></div></div></section>
<section class="sec" style="padding-top:10px"><div class="wrap prose"><h2>Quick answer</h2><p>{desc}</p><h2>How to use the calculator</h2><p>Enter the requested values using consistent units. Change one input at a time when comparing scenarios.</p><h2>Formula and assumptions</h2><p>The calculator applies the standard arithmetic represented by the inputs above. Results assume the entered values remain constant and exclude costs or circumstances that are not requested.</p><h2>Worked example</h2><p>The default values provide a complete example. Adjust any field to create a scenario that matches your question.</p><h2>Limitations</h2><p>Results are general educational estimates. Verify consequential financial or health decisions using current official information and qualified professional guidance.</p><h2>Common mistakes</h2><ul><li>Mixing monthly and annual values or different units.</li><li>Leaving out fees, taxes, breaks or other relevant inputs.</li><li>Treating an estimate as a quote, diagnosis or guarantee.</li></ul><h2>Sources and method</h2><p>The method and assumptions are stated on this page so the result can be checked independently. Last reviewed: {TODAY}.</p></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="sec-head"><h2>Frequently asked questions</h2></div><div class="faq"><div class="faq-item"><div class="faq-q"><h3>Is this calculator free?</h3><span>+</span></div><div class="faq-a">Yes. It runs in the browser with no sign-up.</div></div><div class="faq-item"><div class="faq-q"><h3>Is the result exact?</h3><span>+</span></div><div class="faq-a">No. The result depends on the inputs and stated assumptions.</div></div><div class="faq-item"><div class="faq-q"><h3>Is my data stored?</h3><span>+</span></div><div class="faq-a">The calculation runs in the browser. Do not enter sensitive personal information.</div></div></div></div></section></main>
<footer><div class="wrap"><div class="foot"><div class="foot-brand"><strong>Fynzo</strong><p>Free, fast and private calculators for everyday decisions.</p></div><div><h4>Tools</h4><a href="index.html#tools">All tools</a><a href="mortgage-guides.html">Mortgage</a><a href="loan-guides.html">Loans</a></div><div><h4>Guides</h4><a href="savings-guides.html">Savings</a><a href="percentage-guides.html">Percentages</a><a href="health-calculators.html">Health</a></div><div><h4>Legal</h4><a href="privacy.html">Privacy</a><a href="terms.html">Terms</a><a href="disclaimer.html">Disclaimer</a></div></div><div class="foot-bottom">© 2026 Fynzo · Educational estimates only.</div></div></footer>
<script>{JS}\nconst CALC=v=>{call};</script><script>run();</script><script defer src="fynzo.js"></script></body></html>'''

def card(t):
 fn,name,cat,desc,fields,call,keywords=t
 return f'<a class="tool" data-cat="{cat}" data-keywords="{keywords}" href="{fn}"><div class="ic new-tool-ic">+</div><h3>{name}</h3><p>{desc}</p><span class="badge">New</span></a>'

def update_index():
 p=ROOT/'index.html';soup=BeautifulSoup(p.read_text(encoding='utf-8',errors='ignore'),'html.parser')
 grid=soup.select_one('#grid')
 for old in grid.select('[data-new-tool="true"]'):old.decompose()
 for t in TOOLS:
  node=BeautifulSoup(card(t),'html.parser').a;node['data-new-tool']='true';grid.append(node)
 filters=soup.select_one('.filters')
 if filters and not filters.select_one('[data-filter="everyday"]'):
  b=soup.new_tag('button');b['class']=['filter'];b['data-filter']='everyday';b.string='Everyday';filters.append(b)
 # Update visible counts accurately for homepage cards.
 text=str(soup)
 text=re.sub(r'12 free, fast and private calculators', '28 free, fast and private calculators', text)
 text=re.sub(r'<b>12\+</b><small>Free tools</small>', '<b>28+</b><small>Free tools</small>', text)
 p.write_text('<!doctype html>\n'+text,encoding='utf-8')

def update_sitemap():
 p=ROOT/'sitemap.xml';text=p.read_text(encoding='utf-8',errors='ignore')
 for fn,*_ in TOOLS:
  url=D+fn
  if url not in text:text=text.replace('</urlset>',f'  <url><loc>{url}</loc><lastmod>2026-07-31</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n</urlset>')
 p.write_text(text,encoding='utf-8')

def update_pillars():
 groups={'loan-guides.html':TOOLS[:3]+[TOOLS[7]],'savings-guides.html':TOOLS[3:7],'percentage-guides.html':TOOLS[8:13],'health-calculators.html':TOOLS[13:]}
 for page,tools in groups.items():
  p=ROOT/page
  if not p.exists():continue
  soup=BeautifulSoup(p.read_text(encoding='utf-8',errors='ignore'),'html.parser')
  grid=soup.select_one('.pillar-grid')
  for t in tools:
   if soup.find('a',href=t[0]):continue
   a=soup.new_tag('a',href=t[0]);a['class']=['pillar-card'];st=soup.new_tag('strong');st.string=t[1];sp=soup.new_tag('span');sp.string=t[3];a.extend([st,sp]);grid.append(a)
  p.write_text('<!doctype html>\n'+str(soup),encoding='utf-8')

def main():
 for t in TOOLS:(ROOT/t[0]).write_text(page_html(t),encoding='utf-8')
 update_index();update_sitemap();update_pillars()
 css=ROOT/'styles.css';text=css.read_text(encoding='utf-8',errors='ignore')
 if 'new-tool-ic' not in text:text+='\n.new-tool-ic{font-size:25px;font-weight:800;color:var(--green);display:grid;place-items:center}.field select{width:100%;padding:13px 14px;border:1px solid var(--line);border-radius:10px;background:var(--card);color:var(--text);font:inherit}\n'
 css.write_text(text,encoding='utf-8')
 print('Created and listed 16 functional calculators.')
if __name__=='__main__':main()
