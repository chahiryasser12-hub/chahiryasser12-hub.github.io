#!/usr/bin/env python3
"""Add static, search-friendly numerical examples to Fynzo's five priority calculators."""
from pathlib import Path
from bs4 import BeautifulSoup
import math
ROOT=Path(__file__).resolve().parent

def money(x): return f'${x:,.2f}'
def payment(principal, annual_rate, years):
    r=annual_rate/1200; n=years*12
    return principal/n if r==0 else principal*r*(1+r)**n/((1+r)**n-1)
def fv(principal,monthly,annual_rate,years):
    r=annual_rate/1200; n=years*12
    return principal*(1+r)**n + (monthly*n if r==0 else monthly*((1+r)**n-1)/r)
def bmi(weight,height_cm): return weight/((height_cm/100)**2)
def mifflin(weight,height,age,sex): return 10*weight+6.25*height-5*age+(5 if sex=='male' else -161)

DATA={
'mortgage-calculator.html':{
 'heading':'Popular mortgage payment examples',
 'lead':'These fixed examples answer common searches and show principal-and-interest estimates only. Property tax, insurance, mortgage insurance, maintenance and lender fees are excluded.',
 'examples':[
  ('$300,000 mortgage at 6% for 30 years',f'The estimated monthly principal-and-interest payment is {money(payment(300000,6,30))}. Total scheduled interest is about {money(payment(300000,6,30)*360-300000)}.'),
  ('$300,000 home with 20% down at 6%',f'A 20% down payment is $60,000, leaving a $240,000 principal. The estimated 30-year payment is {money(payment(240000,6,30))} per month.'),
  ('15-year vs 30-year mortgage on $300,000 at 6%',f'The estimated payment is {money(payment(300000,6,15))} for 15 years and {money(payment(300000,6,30))} for 30 years. The shorter term has the higher payment but much lower scheduled interest.'),
  ('5.5% vs 6.5% on a $300,000 30-year mortgage',f'The estimated monthly payment changes from {money(payment(300000,5.5,30))} at 5.5% to {money(payment(300000,6.5,30))} at 6.5%, before excluded housing costs.')],
 'queries':['mortgage calculator with down payment','mortgage payment on $300,000','15-year vs 30-year mortgage calculator','mortgage payment at 6 percent']},
'loan-calculator.html':{
 'heading':'Popular loan payment examples',
 'lead':'These examples assume a fixed rate, equal monthly payments and no fees, missed payments or extra payments.',
 'examples':[
  ('$20,000 loan at 8% for 60 months',f'The estimated monthly payment is {money(payment(20000,8,5))}. Total scheduled interest is about {money(payment(20000,8,5)*60-20000)}.'),
  ('$10,000 loan at 7% for 36 months',f'The estimated monthly payment is {money(payment(10000,7,3))}, with about {money(payment(10000,7,3)*36-10000)} in scheduled interest.'),
  ('36 vs 60 months for $20,000 at 8%',f'The estimated payment is {money(payment(20000,8,3))} over 36 months and {money(payment(20000,8,5))} over 60 months. The longer term lowers the payment but increases total interest.')],
 'queries':['$20,000 loan payment for 5 years','loan calculator with total interest','36 vs 60 month loan','personal loan monthly payment calculator']},
'bmi-calculator.html':{
 'heading':'BMI examples in kilograms and centimetres',
 'lead':'The examples use the adult BMI formula: weight in kilograms divided by height in metres squared. BMI is a screening measure, not a diagnosis.',
 'examples':[
  ('BMI for 70 kg and 175 cm',f'The calculated BMI is {bmi(70,175):.1f}.'),
  ('BMI for 80 kg and 180 cm',f'The calculated BMI is {bmi(80,180):.1f}.'),
  ('BMI for 60 kg and 165 cm',f'The calculated BMI is {bmi(60,165):.1f}. Adult categories require context and are not suitable for children or teenagers.')],
 'queries':['BMI calculator kg and cm','BMI for 70 kg and 175 cm','adult BMI calculator','BMI limitations for muscular adults']},
'calorie-calculator.html':{
 'heading':'Maintenance calorie examples for adults',
 'lead':'These examples use the Mifflin-St Jeor BMR equation and common activity multipliers. They are general starting estimates, not personal dietary prescriptions.',
 'examples':[
  ('Adult male, 30 years, 72 kg, 175 cm',f'Estimated BMR is {mifflin(72,175,30,"male"):.0f} kcal/day. With moderate activity (1.55), estimated maintenance is {mifflin(72,175,30,"male")*1.55:.0f} kcal/day.'),
  ('Adult female, 30 years, 60 kg, 165 cm',f'Estimated BMR is {mifflin(60,165,30,"female"):.0f} kcal/day. With light activity (1.375), estimated maintenance is {mifflin(60,165,30,"female")*1.375:.0f} kcal/day.'),
  ('Why the actual amount can differ','Daily movement, formula error, food tracking, sleep, health and changing routines can make real energy needs differ from the estimate.')],
 'queries':['maintenance calorie calculator','BMR and TDEE calculator','how many calories should I eat','daily calorie needs calculator']},
'compound-interest-calculator.html':{
 'heading':'Compound growth examples with monthly contributions',
 'lead':'The examples assume a constant annual rate compounded monthly, regular end-of-month contributions, and no tax, fees, withdrawals or inflation.',
 'examples':[
  ('$5,000 plus $200 monthly at 8% for 20 years',f'The projected future value is {money(fv(5000,200,8,20))}. Contributions total $53,000; the remainder is projected growth, not guaranteed profit.'),
  ('$10,000 plus $300 monthly at 6% for 10 years',f'The projected future value is {money(fv(10000,300,6,10))} under the stated assumptions.'),
  ('$10,000 with no contributions at 5% for 10 years',f'The projected future value is {money(fv(10000,0,5,10))} with monthly compounding.')],
 'queries':['compound interest calculator with monthly contributions','monthly compound interest calculator','future value of monthly savings','investment growth calculator']}}

for name,data in DATA.items():
    p=ROOT/name; soup=BeautifulSoup(p.read_text(encoding='utf-8',errors='ignore'),'html.parser')
    from bs4 import Doctype
    for node in list(soup.contents):
        if isinstance(node, Doctype): node.extract()
    old=soup.select_one('[data-search-examples="true"]')
    if old: old.decompose()
    sec=soup.new_tag('section'); sec['class']=['search-example-block']; sec['data-search-examples']='true'
    h=soup.new_tag('h2'); h.string=data['heading']; sec.append(h)
    lead=soup.new_tag('p'); lead['class']=['search-example-lead']; lead.string=data['lead']; sec.append(lead)
    grid=soup.new_tag('div'); grid['class']=['search-example-grid']
    for head,text in data['examples']:
        card=soup.new_tag('article'); card['class']=['search-example-card']; h3=soup.new_tag('h3'); h3.string=head; card.append(h3); q=soup.new_tag('p'); q.string=text; card.append(q); grid.append(card)
    sec.append(grid)
    sr=soup.new_tag('div'); sr['class']=['related-searches']; h3=soup.new_tag('h3'); h3.string='Related searches this calculator answers'; sr.append(h3); ul=soup.new_tag('ul')
    for query in data['queries']:
        li=soup.new_tag('li'); li.string=query; ul.append(li)
    sr.append(ul); sec.append(sr)
    target=soup.select_one('.calculator-supplement') or soup.find('footer')
    if target: target.insert_before(sec)
    else: soup.body.append(sec)
    p.write_text('<!DOCTYPE html>\n'+str(soup),encoding='utf-8')
print('Added static search examples to',len(DATA),'priority calculators.')
