#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup, Doctype
ROOT=Path(__file__).resolve().parent
TOOLS=[
('auto-loan-calculator.html','Auto Loan Calculator','Car payment with tax, fees and trade-in.'),
('credit-card-payoff-calculator.html','Credit Card Payoff Calculator','Payoff time, interest and extra-payment savings.'),
('retirement-savings-calculator.html','Retirement Savings Calculator','Projection, contributions, growth and target gap.'),
('home-affordability-calculator.html','Home Affordability Calculator','Estimate a home price from income, debt and DTI.'),
('loan-comparison-calculator.html','Loan Comparison Calculator','Compare payment, fees and total cost.'),
('net-worth-calculator.html','Net Worth Calculator','Add assets and subtract liabilities.'),
('break-even-calculator.html','Break-Even Calculator','Units, revenue, contribution margin and profit.'),
('gpa-calculator.html','GPA Calculator','Credit-weighted GPA on a 4.0 scale.')]

def save(p,s):
 for n in list(s.contents):
  if isinstance(n,Doctype): n.extract()
 p.write_text('<!DOCTYPE html>\n'+str(s),encoding='utf-8')

p=ROOT/'index.html'; s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
old=s.select_one('[data-seo-calculator-expansion]')
if old: old.decompose()
sec=s.new_tag('section'); sec['class']=['sec']; sec['data-seo-calculator-expansion']='true'; wrap=s.new_tag('div'); wrap['class']=['wrap']; h=s.new_tag('h2'); h.string='More decision calculators'; wrap.append(h); lead=s.new_tag('p'); lead.string='Focused tools for cars, credit cards, retirement, home affordability, loan comparison, net worth, business and education.'; wrap.append(lead); grid=s.new_tag('div'); grid['class']=['silo-grid']
for href,title,desc in TOOLS:
 a=s.new_tag('a',href=href); a['class']=['silo-card']; strong=s.new_tag('strong'); strong.string=title; a.append(strong); small=s.new_tag('small'); small.string=desc; a.append(small); grid.append(a)
wrap.append(grid); sec.append(wrap); footer=s.find('footer'); footer.insert_before(sec); save(p,s)

links={
'loan-calculator.html':[TOOLS[0],TOOLS[4]],'debt-payoff-calculator.html':[TOOLS[1]],'compound-interest-calculator.html':[TOOLS[2]],'mortgage-calculator.html':[TOOLS[3]],'budget-percentage-calculator.html':[TOOLS[5]],'markup-margin-calculator.html':[TOOLS[6]],'grade-percentage-calculator.html':[TOOLS[7]]}
for name,items in links.items():
 p=ROOT/name; s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser'); box=s.select_one('[data-seo-expansion-links]')
 if box: box.decompose()
 sec=s.new_tag('section'); sec['class']=['sec']; sec['data-seo-expansion-links']='true'; wrap=s.new_tag('div'); wrap['class']=['wrap']; h=s.new_tag('h2'); h.string='Try a focused calculator'; wrap.append(h); grid=s.new_tag('div'); grid['class']=['silo-grid']
 for href,title,desc in items:
  a=s.new_tag('a',href=href); a['class']=['silo-card']; strong=s.new_tag('strong'); strong.string=title; a.append(strong); small=s.new_tag('small'); small.string=desc; a.append(small); grid.append(a)
 wrap.append(grid); sec.append(wrap); main=s.find('footer'); main.insert_before(sec); save(p,s)
print('Integrated 8 SEO-focused calculators into homepage and contextual links.')
