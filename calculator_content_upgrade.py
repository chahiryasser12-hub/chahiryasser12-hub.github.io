#!/usr/bin/env python3
"""Strengthen every Fynzo calculator page with complete, useful, source-backed content."""
from pathlib import Path
from bs4 import BeautifulSoup
import json, math, re

ROOT=Path(__file__).resolve().parent
CALCS=sorted(list(ROOT.glob('*-calculator.html'))+[ROOT/'password-generator.html'])

INFO={
'mortgage-calculator.html':('Mortgage payment','Monthly payment = P × r(1+r)^n ÷ ((1+r)^n − 1). P is principal after down payment, r is the monthly interest rate, and n is the number of monthly payments.','Enter the home price, down payment, annual rate and term. Compare scenarios by changing one input at a time.','A $300,000 home with 20% down leaves a $240,000 principal. At 6% for 30 years, estimated principal and interest are about $1,439 per month.','A lower payment does not always mean a lower total cost. Review total interest, term, fees, taxes, insurance and cash needed at closing.','The example assumes a fixed rate, monthly payments, no extra payments and no fees, taxes, insurance or mortgage insurance.','This is an educational principal-and-interest estimate, not a bank quote, approval or Loan Estimate. Real products can use different fees, rate structures and payment rules.',['Mixing the home price with the loan principal','Ignoring taxes, insurance, fees and mortgage insurance','Comparing offers with different terms','Treating an unlocked rate as guaranteed'],[('https://www.consumerfinance.gov/owning-a-home/loan-estimate/','CFPB Loan Estimate explainer'),('https://www.consumerfinance.gov/owning-a-home/prepare/decide-how-much-you-want-spend/','CFPB home affordability guidance')]),
'loan-calculator.html':('Loan payment','Monthly payment = P × r(1+r)^n ÷ ((1+r)^n − 1), for a fixed-rate amortizing loan.','Enter the amount borrowed, annual rate and number of months. Save equal-amount scenarios to compare terms or rates.','A $20,000 loan at 8% for 60 months has an estimated payment of about $405.53 and about $4,331.67 in scheduled interest.','Compare monthly payment and total repaid. A longer term can reduce the payment while increasing total interest.','The model assumes a fixed rate, equal monthly payments, no fees and no missed or extra payments.','The result is not a lender offer. APR, fees, payment timing, penalties and lender allocation rules can alter the real cost.',['Comparing different principal amounts','Looking only at the monthly payment','Confusing APR with the payment rate','Assuming extra payments always reduce principal immediately'],[('https://www.consumerfinance.gov/consumer-tools/mortgages/','CFPB borrowing and mortgage resources')]),
'bmi-calculator.html':('Adult BMI','BMI = weight in kilograms ÷ height in metres².','Enter accurately measured adult height and weight in consistent units.','An adult weighing 70 kg at 1.75 m has a BMI of about 22.9.','BMI is a screening measure. It should be considered with health history, physical findings and other relevant information.','Adult categories apply to adults aged 20 and older; children and teens require age-specific interpretation.','BMI does not directly measure body fat and does not distinguish fat, muscle and bone. It is not a diagnosis or substitute for medical advice.',['Using adult categories for children','Reading BMI as a diagnosis','Ignoring measurement error','Assuming equal BMI means equal body composition'],[('https://www.cdc.gov/bmi/about/index.html','CDC About BMI'),('https://www.cdc.gov/bmi/adult-calculator/bmi-categories.html','CDC adult BMI categories')]),
'compound-interest-calculator.html':('Compound growth','Future value combines the initial principal grown over time with the future value of regular contributions.','Enter the starting amount, monthly contribution, estimated annual rate and time period. Test a cautious rate as well as an optimistic one.','Starting with $10,000 and adding $200 monthly produces a result determined by the selected rate, time and compounding assumptions.','Separate contributions from projected growth. A larger projected value is not guaranteed profit or purchasing power.','The estimate assumes a constant rate, regular contribution timing and no tax, fees, withdrawals or inflation unless separately modelled.','Investment returns vary and can be negative. This calculator is educational and does not predict or guarantee a result.',['Treating an estimated rate as guaranteed','Ignoring fees, tax and inflation','Changing several inputs at once','Comparing different contribution timing'],[('https://www.investor.gov/financial-tools-calculators/calculators/compound-interest-calculator','Investor.gov compound interest calculator')]),
'savings-goal-calculator.html':('Monthly savings target','The monthly amount is the contribution needed for the starting balance and assumed growth to reach the selected goal by the deadline.','Enter the goal, current savings, deadline and cautious estimated rate. Compare at least two deadlines.','A $12,000 gap over 24 months requires about $500 per month before any assumed growth.','Check whether the monthly target fits the budget. Extending the deadline can reduce the contribution but delays the goal.','The model assumes regular contributions, a constant estimated rate and no withdrawals, fees, tax or price changes.','Growth is not guaranteed. Near-term savings may need different risk and access considerations than long-term investing.',['Using an unrealistic return','Forgetting current savings','Choosing a deadline without checking cash flow','Ignoring inflation in a future purchase'],[('https://www.investor.gov/financial-tools-calculators/calculators/savings-goal-calculator','Investor.gov savings goal calculator')]),
}

HEALTH={'calorie-calculator.html','body-fat-calculator.html','ideal-weight-calculator.html','water-intake-calculator.html'}
MONEY={'income-tax-calculator.html','roi-calculator.html','hourly-to-salary-calculator.html','discount-calculator.html','sales-tax-calculator.html','tip-calculator.html','fuel-cost-calculator.html'}
DATE={'age-calculator.html','date-difference-calculator.html'}
CONVERT={'length-converter.html','temperature-converter.html'}

def generic(name):
 title=name.replace('-calculator.html','').replace('-generator.html','').replace('-',' ').title()
 if name in HEALTH:
  return (title,'The calculator applies the formula displayed with the inputs and converts units where needed.','Enter measured values carefully and choose the correct units. Recheck unusual results before using them.','Use a realistic adult example, calculate once, then change one input to understand sensitivity.','Treat the result as a general screening or planning estimate, not a diagnosis or personal prescription.','The formula uses general population assumptions and the information entered by the visitor.','Individual health circumstances can differ. Seek qualified medical guidance for symptoms, conditions or major changes.',['Mixing units','Entering estimated rather than measured values','Treating one result as a diagnosis','Ignoring the stated population and formula limits'],[('https://www.cdc.gov/healthy-weight-growth/about/index.html','CDC healthy weight and growth information')])
 if name in MONEY:
  return (title,'The calculator applies the displayed arithmetic to the entered amounts, rates and time assumptions.','Enter values in one currency and period, then change one assumption at a time.','Calculate a base case, save it, and compare a second case with the same starting amount.','Review both the headline result and the component amounts. Check the sign, units and time period.','The estimate uses the entered rates and excludes unspecified fees, taxes, timing rules or market changes.','This educational estimate is not financial, tax, legal or investment advice and may not match an official statement or quote.',['Mixing monthly and annual values','Ignoring fees or taxes','Comparing scenarios with different bases','Rounding too early'],[('https://www.consumerfinance.gov/consumer-tools/','CFPB consumer financial tools')])
 if name in DATE:
  return (title,'The result is calculated from calendar dates using the page’s stated inclusive or elapsed-time convention.','Enter valid dates in the requested order and check the counting convention.','Compare two nearby dates first to confirm whether the start or end date is included.','Label results clearly as elapsed or inclusive days, completed years, months or days.','Calendar calculations follow the browser calendar and do not determine legal deadlines.','Time zones, leap days, business-day rules and jurisdiction-specific legal rules can change an official result.',['Not stating inclusive or exclusive counting','Mixing dates and timestamps','Ignoring leap days','Using an estimate for a legal deadline'],[('https://www.nist.gov/pml/time-and-frequency-division','NIST time and frequency resources')])
 if name in CONVERT:
  return (title,'The output multiplies or offsets the input using the standard conversion shown on the page.','Choose the source and destination units, enter a value, and retain enough precision until the final step.','Convert a familiar reference value, then reverse the conversion as a reasonableness check.','Check the unit label and rounding precision before copying the result.','The conversion assumes the standard unit definitions and ordinary numerical precision.','Rounded values can differ slightly from laboratory, engineering or regulated calculations.',['Selecting the units in reverse','Dropping a temperature offset','Rounding every intermediate step','Copying a number without its unit'],[('https://www.nist.gov/pml/owm/si-units','NIST SI measurement resources')])
 return (title,'The tool applies the formula or rule displayed on the page to the values entered.','Enter the requested values, verify units and generate the result. Change one value at a time when comparing cases.','Start with a simple input whose expected result can be checked manually.','Confirm the output label, units and context before using or sharing the result.','The result depends entirely on the entered values and stated rules.','The tool is educational. Security, legal or professional decisions may require dedicated current guidance.',['Entering the wrong units','Copying an output without context','Ignoring limitations','Failing to verify important results'],[('https://www.nist.gov/','NIST measurement and standards resources')])

def mortgage_tables(soup, parent):
 def payment(principal, annual, years):
  r=annual/1200;n=years*12
  return principal*r*(1+r)**n/((1+r)**n-1)
 h=soup.new_tag('h2');h.string='Educational mortgage payment tables';parent.append(h)
 note=soup.new_tag('p');note['class']=['calc-source-note'];note.string='The figures below estimate principal and interest only. They are educational examples, not bank offers, approvals or official Loan Estimates. Taxes, insurance, fees and mortgage insurance are excluded.';parent.append(note)
 tables=[('Estimated monthly principal and interest', [('Loan amount','15 years at 6%','30 years at 6%')]+[(f'${p:,.0f}',f'${payment(p,6,15):,.0f}',f'${payment(p,6,30):,.0f}') for p in (200000,300000)]),
 ('How a 0.5% rate change affects a $300,000, 30-year loan',[('Rate','Estimated monthly P&I','Difference from 6.0%')]+[(f'{r:.1f}%',f'${payment(300000,r,30):,.0f}',f'${payment(300000,r,30)-payment(300000,6,30):+,.0f}') for r in (5.5,6.0,6.5)])]
 for title,rows in tables:
  h3=soup.new_tag('h3');h3.string=title;parent.append(h3)
  wrap=soup.new_tag('div');wrap['class']=['table-scroll'];table=soup.new_tag('table');table['class']=['article-table','calc-example-table']
  for i,row in enumerate(rows):
   tr=soup.new_tag('tr')
   for v in row:
    cell=soup.new_tag('th' if i==0 else 'td');cell.string=v;tr.append(cell)
   table.append(tr)
  wrap.append(table);parent.append(wrap)

def upgrade(path):
 name=path.name; d=INFO.get(name,generic(name)); quick,formula,use,example,interpret,assume,limits,mistakes,sources=d
 soup=BeautifulSoup(path.read_text(encoding='utf-8',errors='ignore'),'html.parser')
 old=soup.select_one('[data-complete-calculator="true"]')
 if old: old.decompose()
 sec=soup.new_tag('section');sec['class']=['complete-calculator-content'];sec['data-complete-calculator']='true'
 h=soup.new_tag('h2');h.string='Quick answer';sec.append(h);p=soup.new_tag('p');p.string=quick+' calculator gives an instant estimate from the values entered above. Use the result as a starting point and review the assumptions and limits below.';sec.append(p)
 sections=[('Formula',formula),('How to use the calculator',use),('Worked example',example),('Result interpretation',interpret),('Assumptions',assume),('Limitations',limits)]
 for title,text in sections:
  h=soup.new_tag('h2');h.string=title;sec.append(h);p=soup.new_tag('p');p.string=text;sec.append(p)
 if name=='mortgage-calculator.html': mortgage_tables(soup,sec)
 h=soup.new_tag('h2');h.string='Common mistakes';sec.append(h);ul=soup.new_tag('ul')
 for x in mistakes: li=soup.new_tag('li');li.string=x;ul.append(li)
 sec.append(ul)
 h=soup.new_tag('h2');h.string='FAQ';sec.append(h)
 faq=[('Is the result exact?','No. It is an educational estimate based on the entered values and stated assumptions.'),('What should I verify?','Verify units, timing, rates and any excluded fees or circumstances before relying on the result.'),('Can I use this for an important decision?','Use it for initial planning, then check current official documents or qualified professional guidance when the decision is consequential.')]
 for q,a in faq:
  item=soup.new_tag('details');item['class']=['calc-content-faq'];summary=soup.new_tag('summary');summary.string=q;item.append(summary);p=soup.new_tag('p');p.string=a;item.append(p);sec.append(item)
 h=soup.new_tag('h2');h.string='Sources';sec.append(h);ul=soup.new_tag('ul')
 for url,label in sources:
  li=soup.new_tag('li');a=soup.new_tag('a',href=url,target='_blank',rel='noopener noreferrer');a.string=label;li.append(a);ul.append(li)
 sec.append(ul)
 h=soup.new_tag('h2');h.string='Related guides';sec.append(h);links=soup.new_tag('p')
 pillar='health-calculators.html' if name in HEALTH or name=='bmi-calculator.html' else ('mortgage-guides.html' if name=='mortgage-calculator.html' else ('loan-guides.html' if name=='loan-calculator.html' else ('percentage-guides.html' if name in {'percentage-calculator.html','discount-calculator.html','sales-tax-calculator.html','tip-calculator.html'} else 'savings-guides.html')))
 for href,label in [(pillar,'Browse the related topic hub'),('blog.html','Browse all practical guides')]:
  a=soup.new_tag('a',href=href);a.string=label;links.append(a);links.append(' · ')
 sec.append(links)
 footer=soup.find('footer')
 if footer: footer.insert_before(sec)
 else: soup.body.append(sec)
 path.write_text('<!doctype html>\n'+str(soup),encoding='utf-8')
 return len(faq)

def main():
 css=ROOT/'styles.css';text=css.read_text(encoding='utf-8',errors='ignore')
 if 'Complete calculator content' not in text:
  text+='''\n/* Complete calculator content */\n.complete-calculator-content{max-width:900px;margin:38px auto;padding:clamp(22px,4vw,38px);background:var(--card);border:1px solid var(--line);border-radius:20px}.complete-calculator-content h2{font-size:24px;margin:30px 0 10px}.complete-calculator-content h2:first-child{margin-top:0}.complete-calculator-content h3{font-size:18px;margin:22px 0 9px}.complete-calculator-content p,.complete-calculator-content li{color:var(--muted);line-height:1.75}.complete-calculator-content ul{margin:0 0 18px 22px}.calc-source-note{padding:14px 16px;border-left:4px solid var(--gold);background:var(--bg);border-radius:0 10px 10px 0}.calc-example-table{width:100%;border-collapse:collapse}.calc-example-table th,.calc-example-table td{padding:11px;border:1px solid var(--line);text-align:left}.calc-content-faq{border-bottom:1px solid var(--line);padding:13px 0}.calc-content-faq summary{font-weight:700;cursor:pointer}.calc-content-faq p{padding-top:8px}\n'''
  css.write_text(text,encoding='utf-8')
 total=0
 for p in CALCS:
  if p.exists(): total+=1;upgrade(p)
 print(f'Complete content added to {total} calculators.')
if __name__=='__main__':main()
