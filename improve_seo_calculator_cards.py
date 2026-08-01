#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup, Doctype
ROOT=Path(__file__).resolve().parent
TOOLS={
'auto-loan-calculator.html':('Auto Loan Calculator','Car payment with tax, fees and trade-in.','calc-auto-loan.svg','Auto'),
'credit-card-payoff-calculator.html':('Credit Card Payoff Calculator','Payoff time, interest and extra-payment savings.','calc-credit-card.svg','Debt'),
'retirement-savings-calculator.html':('Retirement Savings Calculator','Project contributions, growth and the target gap.','calc-retirement.svg','Savings'),
'home-affordability-calculator.html':('Home Affordability Calculator','Estimate a home price from income, debt and DTI.','calc-home-affordability.svg','Home'),
'loan-comparison-calculator.html':('Loan Comparison Calculator','Compare monthly payment, fees and total cost.','calc-loan-comparison.svg','Loans'),
'net-worth-calculator.html':('Net Worth Calculator','Add assets and subtract liabilities.','calc-net-worth.svg','Planning'),
'break-even-calculator.html':('Break-Even Calculator','Calculate units, revenue, contribution margin and profit.','calc-break-even.svg','Business'),
'gpa-calculator.html':('GPA Calculator','Calculate a credit-weighted GPA on a 4.0 scale.','calc-gpa.svg','Education')}
CONTEXT={
'loan-calculator.html':['auto-loan-calculator.html','loan-comparison-calculator.html'],
'debt-payoff-calculator.html':['credit-card-payoff-calculator.html'],
'compound-interest-calculator.html':['retirement-savings-calculator.html'],
'mortgage-calculator.html':['home-affordability-calculator.html'],
'budget-percentage-calculator.html':['net-worth-calculator.html'],
'markup-margin-calculator.html':['break-even-calculator.html'],
'grade-percentage-calculator.html':['gpa-calculator.html']}

def save(p,s):
 for n in list(s.contents):
  if isinstance(n,Doctype): n.extract()
 p.write_text('<!DOCTYPE html>\n'+str(s),encoding='utf-8')

def card(s,href):
 title,desc,icon,badge=TOOLS[href]
 a=s.new_tag('a',href=href); a['class']=['seo-tool-card']; a['aria-label']=title
 ib=s.new_tag('span'); ib['class']=['seo-tool-icon']; img=s.new_tag('img',src=icon,alt='',width='64',height='64',loading='lazy',decoding='async'); ib.append(img); a.append(ib)
 body=s.new_tag('span'); body['class']=['seo-tool-copy']; b=s.new_tag('span'); b['class']=['seo-tool-badge']; b.string=badge; body.append(b); strong=s.new_tag('strong'); strong.string=title; body.append(strong); p=s.new_tag('span'); p['class']=['seo-tool-description']; p.string=desc; body.append(p); action=s.new_tag('span'); action['class']=['seo-tool-action']; action.string='Open calculator →'; body.append(action); a.append(body); return a

def section(s,hrefs,home=False):
 sec=s.new_tag('section'); sec['class']=['seo-tool-showcase']; sec['data-seo-calculator-expansion']='true' if home else None
 if not home: sec['data-seo-expansion-links']='true'
 wrap=s.new_tag('div'); wrap['class']=['wrap']; head=s.new_tag('div'); head['class']=['seo-tool-head']; eyebrow=s.new_tag('span'); eyebrow['class']=['seo-tool-eyebrow']; eyebrow.string='Recommended calculators' if not home else 'Explore more decisions'; head.append(eyebrow); h=s.new_tag('h2'); h.string='Choose your next calculator' if not home else 'More calculators for real decisions'; head.append(h); p=s.new_tag('p'); p.string='Continue with a focused tool that matches what you want to calculate next.' if not home else 'Cars, debt, retirement, home affordability, comparisons, personal finance, business and education.'; head.append(p); wrap.append(head); grid=s.new_tag('div'); grid['class']=['seo-tool-grid']
 for href in hrefs: grid.append(card(s,href))
 wrap.append(grid); sec.append(wrap); return sec

# Homepage: place immediately after Popular calculators, not near footer.
p=ROOT/'index.html'; s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
old=s.select_one('[data-seo-calculator-expansion]')
if old: old.decompose()
sec=section(s,list(TOOLS),True); anchor=s.select_one('#popular-tools') or s.select_one('#tools'); anchor.insert_after(sec); save(p,s)

# Context pages: remove the old bottom block and insert after calculator result / existing recommendation block.
for name,hrefs in CONTEXT.items():
 p=ROOT/name; s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser'); old=s.select_one('[data-seo-expansion-links]')
 if old: old.decompose()
 sec=section(s,hrefs,False)
 existing=s.select_one('.focused-recommendations')
 if existing: existing.insert_after(sec)
 else:
  calc=None
  for child in s.body.find_all(recursive=False):
   if getattr(child,'select_one',None) and (child.select_one('.calc-wrap') or child.select_one('#fx')): calc=child; break
  (calc or s.select_one('.page-head')).insert_after(sec)
 save(p,s)
print('Redesigned and repositioned SEO calculator cards on homepage and',len(CONTEXT),'calculator pages.')
