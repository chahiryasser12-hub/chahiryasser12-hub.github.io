#!/usr/bin/env python3
"""Add comprehensive long-tail sections to existing Fynzo pages without creating thin URL variants."""
from pathlib import Path
from bs4 import BeautifulSoup
import json, re

ROOT=Path(__file__).resolve().parent
MARK='data-long-tail="true"'

DATA={
'mortgage-calculator.html':{
 'title':'Mortgage Payment Calculator With Down Payment and Term Comparison | Fynzo',
 'desc':'Estimate a mortgage payment on $300,000 at 6%, compare 20% down, and test 30-year vs 15-year mortgage scenarios in one calculator.',
 'heading':'Mortgage payment examples and comparisons',
 'intro':'Use the calculator above to change one assumption at a time. The examples below explain popular mortgage questions without creating a separate page for every price or rate.',
 'items':[
  ('Mortgage payment on $300,000 at 6 percent','Enter a $300,000 home price, a 0% down payment, a 6% annual rate and the selected term. For a principal-and-interest-only comparison, a 30-year term is about $1,799 per month, while a 15-year term is about $2,532 per month. Taxes, insurance, fees and other costs are separate.'),
  ('Mortgage payment with 20 percent down','On a $300,000 home, 20% down is $60,000 and leaves a $240,000 starting loan. At 6% for 30 years, principal and interest are about $1,439 per month before taxes, insurance and fees.'),
  ('30-year vs 15-year mortgage calculator','Keep the home price, down payment and rate identical, then save one 30-year scenario and one 15-year scenario. The shorter term normally has a higher monthly payment but lower total scheduled interest.'),
  ('How much house can I afford on a $60,000 salary?','A salary alone cannot determine affordability. Compare the estimated housing payment with take-home income, existing monthly debts, property costs, emergency savings and local lending rules. Use the affordability guide for a fuller checklist.'),
  ('Mortgage rate comparison calculator','Keep the amount and term fixed, then compare two rates. Review both the monthly difference and total interest, and add lender fees or points separately before deciding.')],
 'links':[('mortgage-guides.html','Explore all mortgage guides'),('blog-how-much-house-can-i-afford.html','Read the home-affordability guide')]
},
'loan-calculator.html':{
 'title':'Loan Payment and Interest Calculator With Term Comparison | Fynzo',
 'desc':'Estimate a $20,000 loan payment for five years, compare 36 vs 60 months, total interest, APR and extra-payment scenarios.',
 'heading':'Loan payment examples and comparisons','intro':'These examples answer common loan questions on one useful calculator page. Change one input at a time and compare the complete repayment cost.',
 'items':[
  ('$20,000 loan payment for 5 years','For an example $20,000 loan at 8% over 60 months, the scheduled payment is about $405.53 per month and total scheduled interest is about $4,331.67. Actual offers can include fees and different timing rules.'),
  ('36 vs 60 month loan comparison','At the same amount and rate, 36 months normally means a higher payment and less total interest. A 60-month term lowers the scheduled payment but keeps the balance outstanding longer.'),
  ('How much interest will I pay on a loan?','Enter the principal, annual interest rate and number of months. The calculator subtracts principal from total scheduled payments to estimate interest, assuming the rate and schedule remain unchanged.'),
  ('Loan payment with extra monthly payments','First save the scheduled scenario. Then model a sustainable extra principal amount and compare payoff time and interest. Confirm how the lender applies extra payments and whether any penalty exists.'),
  ('APR vs interest rate example','The interest rate is used to calculate scheduled interest. APR is a broader comparison measure that may include defined fees. Use official disclosures because APR treatment varies by product and jurisdiction.')],
 'links':[('loan-guides.html','Explore all loan guides'),('blog-pay-off-loan-faster.html','Read the faster-payoff guide')]
},
'percentage-calculator.html':{
 'title':'Percentage Calculator With Increase, Discount and Worked Examples | Fynzo',
 'desc':'Calculate what percent 25 is of 80, percentage increase from 50 to 65, discounts, stacked discounts and percentage-point changes.',
 'heading':'Percentage examples with clear formulas','intro':'Use one comprehensive percentage calculator instead of separate pages that only swap numbers. Each example shows the base value and the correct operation.',
 'items':[
  ('What percent is 25 of 80?','Divide the part by the whole and multiply by 100: 25 ÷ 80 × 100 = 31.25%.'),
  ('Percentage increase from 50 to 65','Subtract the original value, divide by the original, then multiply by 100: (65 − 50) ÷ 50 × 100 = 30%.'),
  ('20 percent off 150','Multiply 150 by 20% to find a discount of 30. Subtract it from 150 to get a final price of 120 before tax or fees.'),
  ('How to calculate stacked discounts','Apply each discount to the reduced price. For 20% off followed by 10% off, multiply 0.80 × 0.90 = 0.72, so the combined discount is 28%, not 30%.'),
  ('Percentage points vs percentage change','A rate rising from 10% to 12% increases by 2 percentage points. Relative to the original 10%, the percentage increase is 20%.')],
 'links':[('percentage-guides.html','Explore all percentage guides'),('discount-calculator.html','Open the discount calculator')]
},
'bmi-calculator.html':{
 'title':'BMI Calculator for Adults With Limitations Explained | Fynzo',
 'desc':'Calculate adult BMI and understand BMI categories, measurement limits and why muscular adults may need additional context.',
 'heading':'Adult BMI: interpretation and limitations','intro':'BMI is a screening estimate based on height and weight. It does not diagnose health or directly measure body fat.',
 'items':[
  ('BMI calculator for adults','Enter measured adult height and weight using consistent units. The result is weight in kilograms divided by height in metres squared.'),
  ('BMI limitations for muscular adults','BMI cannot distinguish muscle, fat and bone. A muscular adult may receive a higher result even when body composition differs from another adult with the same BMI.'),
  ('What should I do with a BMI result?','Use the number as general context alongside health history and other relevant measurements. Concerns about weight, nutrition or health should be discussed with a qualified healthcare professional.')],
 'links':[('health-calculators.html','Explore health calculators and guides'),('body-fat-calculator.html','Compare with the body-fat estimate')]
},
'calorie-calculator.html':{
 'title':'Maintenance Calories Calculator for Adults | Fynzo',
 'desc':'Estimate adult maintenance calories, BMR and total daily energy needs while understanding activity assumptions and calculator limitations.',
 'heading':'Maintenance calories calculator: use the estimate well','intro':'Maintenance calories are an estimate, not an exact prescription. Formula inputs, activity assumptions and individual circumstances affect the result.',
 'items':[
  ('Maintenance calories calculator','Enter the requested adult measurements and choose a realistic activity level. The calculator estimates basal metabolic rate, then applies an activity factor to estimate total daily expenditure.'),
  ('Why can real maintenance calories differ?','Daily movement, measurement error, changing routines and individual variation can make actual needs differ from the formula output.'),
  ('How should the estimate be interpreted?','Treat the result as a general educational starting point. Major dietary changes or health concerns deserve guidance from a qualified professional.')],
 'links':[('health-calculators.html','Explore health calculators and guides'),('blog-how-many-calories-should-i-eat.html','Read the calorie-needs guide')]
},
'water-intake-calculator.html':{
 'title':'Daily Water Intake Calculator by Weight | Fynzo',
 'desc':'Estimate daily water intake by weight and activity, with practical context for heat, exercise, food and health-related limitations.',
 'heading':'Daily water intake by weight and activity','intro':'Body weight can provide a general starting estimate, but daily fluid needs can change with activity, climate, food and health circumstances.',
 'items':[
  ('Daily water intake by weight','Enter current weight in the selected unit. The calculator applies a general planning estimate and shows the result in practical units.'),
  ('Why does the daily amount change?','Exercise, heat, fever, fluid loss, pregnancy, breastfeeding, food and medical circumstances can change hydration needs.'),
  ('Is the result a medical target?','No. The result is general educational information. Follow instructions from a qualified healthcare professional when a condition or medicine affects fluid intake.')],
 'links':[('health-calculators.html','Explore health calculators and guides')]
},
'ideal-weight-calculator.html':{
 'title':'Ideal Weight Range by Height Calculator | Fynzo',
 'desc':'Compare ideal-weight reference formulas and a general weight range by height while understanding their limits.',
 'heading':'Ideal weight range by height: why results differ','intro':'Ideal-weight equations provide historical reference estimates, not one required personal target.',
 'items':[
  ('Ideal weight range by height','Enter height to compare the available reference formulas. A range is more informative than treating one result as a precise requirement.'),
  ('Why do formulas give different answers?','Each formula uses different assumptions and cannot fully represent body composition, frame, age or health history.'),
  ('How should I use the range?','Use the output as general context only. A qualified healthcare professional can consider individual health information and appropriate goals.')],
 'links':[('health-calculators.html','Explore health calculators and guides'),('bmi-calculator.html','Open the BMI calculator')]
}}

CSS='''<style id="long-tail-style">.long-tail-block{max-width:900px;margin:36px auto;padding:28px;background:var(--card);border:1px solid var(--line);border-radius:18px}.long-tail-block h2{font-size:clamp(23px,4vw,30px);margin-bottom:8px}.long-tail-lead{color:var(--muted);margin-bottom:22px}.long-tail-grid{display:grid;gap:14px}.long-tail-item{padding:18px;background:var(--bg);border:1px solid var(--line);border-radius:14px}.long-tail-item h3{font-size:18px;margin:0 0 7px}.long-tail-item p{color:var(--muted);margin:0}.long-tail-links{display:flex;gap:10px;flex-wrap:wrap;margin-top:19px}.long-tail-links a{color:var(--green);font-weight:700}</style>'''

def update_schema(soup, data):
    faq=[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in data['items']]
    tag=soup.new_tag('script',type='application/ld+json'); tag['data-long-tail-schema']='true'
    tag.string=json.dumps({'@context':'https://schema.org','@type':'FAQPage','mainEntity':faq},ensure_ascii=False)
    soup.head.append(tag)

def upgrade(file,data):
    p=ROOT/file
    if not p.exists(): return False
    soup=BeautifulSoup(p.read_text(encoding='utf-8',errors='ignore'),'html.parser')
    old=soup.select_one('[data-long-tail="true"]')
    if old: old.decompose()
    for old_schema in soup.select('script[data-long-tail-schema="true"]'): old_schema.decompose()
    if soup.title: soup.title.string=data['title']
    meta=soup.find('meta',attrs={'name':'description'})
    if meta: meta['content']=data['desc']
    else:
        meta=soup.new_tag('meta'); meta['name']='description'; meta['content']=data['desc']; soup.head.append(meta)
    if not soup.select_one('#long-tail-style'): soup.head.append(BeautifulSoup(CSS,'html.parser').style)
    sec=soup.new_tag('section'); sec['class']=['long-tail-block']; sec['data-long-tail']='true'
    h=soup.new_tag('h2'); h.string=data['heading']; sec.append(h)
    lead=soup.new_tag('p'); lead['class']=['long-tail-lead']; lead.string=data['intro']; sec.append(lead)
    grid=soup.new_tag('div'); grid['class']=['long-tail-grid']
    for q,a in data['items']:
        item=soup.new_tag('article'); item['class']=['long-tail-item']
        h3=soup.new_tag('h3'); h3.string=q; item.append(h3)
        para=soup.new_tag('p'); para.string=a; item.append(para); grid.append(item)
    sec.append(grid)
    links=soup.new_tag('div'); links['class']=['long-tail-links']
    for href,label in data['links']:
        a=soup.new_tag('a',href=href); a.string=label; links.append(a)
    sec.append(links)
    footer=soup.find('footer')
    if footer: footer.insert_before(sec)
    else: soup.body.append(sec)
    update_schema(soup,data)
    p.write_text('<!doctype html>\n'+str(soup),encoding='utf-8')
    return True

def main():
    count=sum(upgrade(f,d) for f,d in DATA.items())
    print(f'Upgraded {count} comprehensive calculator pages with long-tail sections; created 0 thin numeric pages.')
if __name__=='__main__': main()
