#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup, Doctype
ROOT=Path(__file__).resolve().parent
ICONS={
'mortgage-total-cost-calculator.html':('guide-mortgage-total-cost.svg','Total housing cost'),
'mortgage-recast-calculator.html':('guide-mortgage-recast.svg','Mortgage recast'),
'pay-raise-calculator.html':('guide-pay-raise.svg','Pay raise'),
'work-hours-calculator.html':('guide-work-hours.svg','Work hours'),
'blog-why-calorie-calculators-differ.html':('guide-calorie-differences.svg','Calorie estimates'),
'blog-36-vs-60-month-loan.html':('guide-loan-terms.svg','Loan terms'),
'blog-bmi-vs-body-fat.html':('guide-bmi-body-fat.svg','BMI and body fat'),
'blog-apr-vs-interest-rate.html':('guide-apr-interest.svg','APR and interest'),
'blog-percentage-change-vs-points.html':('guide-percentage-points.svg','Percentage change'),
}
DESCRIPTIONS={
'mortgage-total-cost-calculator.html':'Add tax, insurance, PMI and HOA to estimate the full monthly housing cost.',
'mortgage-recast-calculator.html':'Estimate a new payment after a principal lump sum using the remaining term.',
'pay-raise-calculator.html':'Convert a raise into annual, monthly, biweekly and weekly gross-pay changes.',
'work-hours-calculator.html':'Calculate paid time, breaks, overnight shifts and optional gross pay.',
'blog-why-calorie-calculators-differ.html':'Understand equations, activity multipliers and why calorie estimates vary.',
'blog-36-vs-60-month-loan.html':'Compare monthly payment, total interest and total repayment across two terms.',
'blog-bmi-vs-body-fat.html':'Learn what each estimate measures and where each method has limitations.',
'blog-apr-vs-interest-rate.html':'Understand borrowing rate versus the broader annualized cost shown by APR.',
'blog-percentage-change-vs-points.html':'See the difference between relative change and percentage-point movement.',
}
PAGE_LINKS={
'mortgage-calculator.html':[
 ('mortgage-total-cost-calculator.html','Mortgage with Taxes, Insurance & PMI','Tool'),
 ('mortgage-recast-calculator.html','Mortgage Recast Calculator','Tool'),
 ('blog-36-vs-60-month-loan.html','36 vs 60 Month Loan','Guide')],
'loan-calculator.html':[
 ('blog-36-vs-60-month-loan.html','36 vs 60 Month Loan','Guide'),
 ('blog-apr-vs-interest-rate.html','APR vs Interest Rate','Guide')],
'calorie-calculator.html':[
 ('blog-why-calorie-calculators-differ.html','Why Calorie Calculators Give Different Results','Guide')],
'bmi-calculator.html':[
 ('blog-bmi-vs-body-fat.html','BMI vs Body Fat Percentage','Guide')],
'percentage-calculator.html':[
 ('blog-percentage-change-vs-points.html','Percentage Change vs Percentage Points','Guide')],
'hourly-to-salary-calculator.html':[
 ('pay-raise-calculator.html','Pay Raise Calculator','Tool'),
 ('work-hours-calculator.html','Work Hours Calculator','Tool')],
'business-days-calculator.html':[
 ('work-hours-calculator.html','Work Hours Calculator','Tool')],
}

def save(p,soup):
    for node in list(soup.contents):
        if isinstance(node,Doctype): node.extract()
    p.write_text('<!DOCTYPE html>\n'+str(soup),encoding='utf-8')

def build_section(soup,links):
    section=soup.new_tag('section'); section['class']=['focused-recommendations']; section['data-opportunity-links']='true'; section['aria-labelledby']='focused-recommendations-title'
    wrap=soup.new_tag('div'); wrap['class']=['wrap']
    head=soup.new_tag('div'); head['class']=['focused-head']
    copy=soup.new_tag('div')
    eyebrow=soup.new_tag('span'); eyebrow['class']=['focused-eyebrow']; eyebrow.string='Recommended next step'; copy.append(eyebrow)
    h=soup.new_tag('h2',id='focused-recommendations-title'); h.string='Explore a more focused tool or guide'; copy.append(h)
    p=soup.new_tag('p'); p.string='Continue with the option that best matches the decision or question behind your result.'; copy.append(p); head.append(copy); wrap.append(head)
    grid=soup.new_tag('div'); grid['class']=['focused-grid']
    for href,title,kind in links:
        a=soup.new_tag('a',href=href); a['class']=['focused-card']; a['aria-label']=f'{title}, {kind}'
        iconbox=soup.new_tag('span'); iconbox['class']=['focused-icon']; img=soup.new_tag('img',src=ICONS[href][0],alt='',width='64',height='64',loading='lazy',decoding='async'); iconbox.append(img); a.append(iconbox)
        body=soup.new_tag('span'); body['class']=['focused-card-body']
        badge=soup.new_tag('span'); badge['class']=['focused-badge',kind.lower()]; badge.string=kind; body.append(badge)
        title_el=soup.new_tag('strong'); title_el.string=title; body.append(title_el)
        desc=soup.new_tag('span'); desc['class']=['focused-description']; desc.string=DESCRIPTIONS[href]; body.append(desc)
        action=soup.new_tag('span'); action['class']=['focused-action']; action.string='Open '+kind.lower()+' →'; body.append(action); a.append(body); grid.append(a)
    wrap.append(grid); section.append(wrap); return section

for name,links in PAGE_LINKS.items():
    path=ROOT/name; soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
    old=soup.select_one('[data-opportunity-links]')
    if old: old.decompose()
    section=build_section(soup,links)
    main_calc=None
    for candidate in soup.body.find_all(recursive=False):
        if getattr(candidate,'select_one',None) and (candidate.select_one('.calc-wrap') or candidate.select_one('#fx')):
            main_calc=candidate; break
    if main_calc:
        main_calc.insert_after(section)
    else:
        page_head=soup.select_one('.page-head')
        if page_head: page_head.insert_after(section)
        else: soup.body.insert(2,section)
    save(path,soup)
print('Moved and redesigned focused recommendations on',len(PAGE_LINKS),'pages.')
