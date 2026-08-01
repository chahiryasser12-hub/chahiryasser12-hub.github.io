#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup, Doctype
ROOT=Path(__file__).resolve().parent
TOOLS=[('mortgage-total-cost-calculator.html','Mortgage with Taxes, Insurance & PMI'),('mortgage-recast-calculator.html','Mortgage Recast Calculator'),('pay-raise-calculator.html','Pay Raise Calculator'),('work-hours-calculator.html','Work Hours Calculator')]
GUIDES=[('blog-why-calorie-calculators-differ.html','Why Calorie Calculators Give Different Results'),('blog-36-vs-60-month-loan.html','36 vs 60 Month Loan'),('blog-bmi-vs-body-fat.html','BMI vs Body Fat Percentage'),('blog-apr-vs-interest-rate.html','APR vs Interest Rate'),('blog-percentage-change-vs-points.html','Percentage Change vs Percentage Points')]

def save(p,soup):
 for node in list(soup.contents):
  if isinstance(node,Doctype): node.extract()
 p.write_text('<!DOCTYPE html>\n'+str(soup),encoding='utf-8')

p=ROOT/'index.html'; s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
old=s.select_one('[data-opportunity-tools]')
if old: old.decompose()
sec=s.new_tag('section'); sec['class']=['sec']; sec['data-opportunity-tools']='true'; wrap=s.new_tag('div'); wrap['class']=['wrap']; h=s.new_tag('h2'); h.string='New high-intent calculators'; wrap.append(h); lead=s.new_tag('p'); lead.string='Focused tools for total housing cost, mortgage recasting, pay raises and work hours.'; wrap.append(lead); grid=s.new_tag('div'); grid['class']=['silo-grid']
for href,title in TOOLS:
 a=s.new_tag('a',href=href); a['class']=['silo-card']; span=s.new_tag('span'); span.string=title; a.append(span); grid.append(a)
wrap.append(grid); sec.append(wrap); footer=s.find('footer'); footer.insert_before(sec) if footer else s.body.append(sec); save(p,s)

# Contextual links on existing tool pages.
LINKS={
 'mortgage-calculator.html':[TOOLS[0],TOOLS[1],GUIDES[1]],
 'loan-calculator.html':[GUIDES[1],GUIDES[3]],
 'calorie-calculator.html':[GUIDES[0]],
 'bmi-calculator.html':[GUIDES[2]],
 'percentage-calculator.html':[GUIDES[4]],
 'hourly-to-salary-calculator.html':[TOOLS[2],TOOLS[3]],
 'business-days-calculator.html':[TOOLS[3]],
}
for name,links in LINKS.items():
 p=ROOT/name; s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser'); old=s.select_one('[data-opportunity-links]')
 if old: old.decompose()
 box=s.new_tag('section'); box['class']=['sec']; box['data-opportunity-links']='true'; wrap=s.new_tag('div'); wrap['class']=['wrap']; h=s.new_tag('h2'); h.string='More focused tools and guides'; wrap.append(h); grid=s.new_tag('div'); grid['class']=['silo-grid']
 for href,title in links:
  a=s.new_tag('a',href=href); a['class']=['silo-card']; span=s.new_tag('span'); span.string=title; a.append(span); grid.append(a)
 wrap.append(grid); box.append(wrap); footer=s.find('footer'); footer.insert_before(box) if footer else s.body.append(box); save(p,s)
print('Integrated opportunity tools and guides into internal linking.')
