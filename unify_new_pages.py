#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup, Doctype
import copy
ROOT=Path(__file__).resolve().parent
CALCS={
'mortgage-total-cost-calculator.html':('Estimate your complete monthly housing cost, then compare the total with a simpler principal-and-interest payment.','mortgage-calculator.html','Compare principal and interest','mortgage-recast-calculator.html','Estimate a mortgage recast'),
'mortgage-recast-calculator.html':('Use the remaining balance and remaining term. A recast does not reset the loan to a new 30-year term.','mortgage-total-cost-calculator.html','Estimate total housing cost','extra-mortgage-payment-calculator.html','Compare extra payments'),
'pay-raise-calculator.html':('This is a gross-pay estimate. Taxes and payroll deductions can change the take-home difference.','hourly-to-salary-calculator.html','Convert hourly pay to salary','income-tax-calculator.html','Estimate take-home pay'),
'work-hours-calculator.html':('Paid time subtracts the entered unpaid break. Overnight shifts are treated as ending the following day.','hourly-to-salary-calculator.html','Convert hourly pay to salary','business-days-calculator.html','Count business days'),
}
CALCS.update({
'auto-loan-calculator.html':('This estimate includes the entered tax, fees, down payment and trade-in assumptions. Confirm the dealer purchase order and lender disclosure.','loan-comparison-calculator.html','Compare two loan offers','budget-percentage-calculator.html','Check your monthly budget'),
'credit-card-payoff-calculator.html':('The payoff estimate assumes no new charges or fees and a constant APR and monthly payment.','debt-payoff-calculator.html','Compare debt payoff strategies','emergency-fund-calculator.html','Build an emergency fund'),
'retirement-savings-calculator.html':('The projected return is an assumption, not a guarantee. Test multiple scenarios and consider inflation, fees and taxes.','compound-interest-calculator.html','Project compound growth','savings-goal-calculator.html','Plan a savings target'),
'home-affordability-calculator.html':('The estimated price uses the entered DTI limit and costs. A lender can apply different approval rules and rates.','mortgage-total-cost-calculator.html','Estimate full housing cost','debt-to-income-calculator.html','Check debt-to-income ratio'),
'loan-comparison-calculator.html':('Compare monthly affordability and total cost together. Include known fees and use official disclosures before deciding.','loan-calculator.html','Calculate a single loan','apr-calculator.html','Estimate APR'),
'net-worth-calculator.html':('Net worth is a point-in-time estimate. Use consistent dates and reasonable current values for assets and debts.','debt-payoff-calculator.html','Plan debt payoff','retirement-savings-calculator.html','Project retirement savings'),
'break-even-calculator.html':('Break-even assumes constant price and variable cost per unit. Real costs and capacity can change as volume grows.','markup-margin-calculator.html','Calculate markup and margin','roi-calculator.html','Calculate ROI'),
'gpa-calculator.html':('The result uses a 4.0 grade-point scale and credit weighting. Verify the official rules used by the school.','grade-percentage-calculator.html','Calculate grade percentage','percentage-calculator.html','Open percentage calculator'),
})
GUIDES=['blog-why-calorie-calculators-differ.html','blog-36-vs-60-month-loan.html','blog-bmi-vs-body-fat.html','blog-apr-vs-interest-rate.html','blog-percentage-change-vs-points.html']
base=BeautifulSoup((ROOT/'mortgage-calculator.html').read_text(encoding='utf-8'),'html.parser')
base_header=base.find('header',class_='site-header'); base_footer=base.find('footer',class_='site-footer')
actions=base.select_one('.calc-actions')

def save(p,soup):
    for n in list(soup.contents):
        if isinstance(n,Doctype): n.extract()
    p.write_text('<!DOCTYPE html>\n'+str(soup),encoding='utf-8')

def ensure_script(soup,src):
    if not soup.find('script',src=lambda x:x and x.split('?')[0]==src):
        tag=soup.new_tag('script',src=src); tag['defer']=''; soup.body.append(tag)

for name,(explain,u1,t1,u2,t2) in CALCS.items():
    p=ROOT/name; soup=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
    soup.html['data-fynzo-ui']='unified-v9'
    old=soup.find('header',class_='site-header')
    if old: old.replace_with(copy.deepcopy(base_header))
    old=soup.find('footer',class_='site-footer')
    if old: old.replace_with(copy.deepcopy(base_footer))
    # Match established calculator page heading and favorite control.
    ph=soup.select_one('.page-head .wrap')
    if ph and not ph.select_one('.favorite-tool-btn'):
        h1=soup.find('h1'); b=soup.new_tag('button',type='button'); b['class']=['favorite-tool-btn']; b['aria-pressed']='false'; b['data-title']=h1.get_text(' ',strip=True); b['data-url']=name; b.string='☆ Save this calculator'; ph.append(b)
    cw=soup.select_one('.calc-wrap'); res=soup.select_one('#res')
    if cw and res:
        res['class']=['result']
        right=res.parent
        if right==cw:
            right=soup.new_tag('div'); res.extract(); right.append(res); cw.append(right)
        # Remove any previously generated UI pieces.
        for selector in ('.calc-actions','.result-context','.result-chart-card'):
            for x in right.select(selector): x.decompose()
        right.append(copy.deepcopy(actions))
        ctx=soup.new_tag('div'); ctx['class']=['result-context']; h=soup.new_tag('h3'); h.string='How to read this result'; ctx.append(h); q=soup.new_tag('p'); q.string=explain; ctx.append(q)
        nxt=soup.new_tag('div'); nxt['class']=['result-next']; nxt['data-smart-next']='true'; strong=soup.new_tag('strong'); strong.string='Based on this result, you may also want to try:'; nxt.append(strong)
        for href,title in ((u1,t1),(u2,t2)):
            a=soup.new_tag('a',href=href); a.string=title; nxt.append(a)
        ctx.append(nxt); right.append(ctx)
        chart=soup.new_tag('div'); chart['class']=['result-chart-card']; chart.append(BeautifulSoup('<div class="advanced-title"><div><h3>Result breakdown</h3><p>A visual summary that updates with your calculation.</p></div></div><div class="result-chart" aria-label="Result breakdown chart"></div>','html.parser'))
        right.append(chart)
    ensure_script(soup,'advanced.js'); ensure_script(soup,'tool-actions.js'); ensure_script(soup,'pdf-report-v2.js')
    save(p,soup)

for name in GUIDES:
    p=ROOT/name; soup=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser'); soup.html['data-fynzo-ui']='unified-v9'
    old=soup.find('header',class_='site-header')
    if old: old.replace_with(copy.deepcopy(base_header))
    old=soup.find('footer',class_='site-footer')
    if old: old.replace_with(copy.deepcopy(base_footer))
    ensure_script(soup,'advanced.js')
    save(p,soup)
print('Unified',len(CALCS),'new calculators and',len(GUIDES),'new guides with the established Fynzo design.')
