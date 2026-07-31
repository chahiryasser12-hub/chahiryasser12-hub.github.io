#!/usr/bin/env python3
"""Apply concise, distinct SEO titles and answer-first meta descriptions."""
from pathlib import Path
from bs4 import BeautifulSoup
from collections import Counter
import json

ROOT=Path(__file__).resolve().parent
MARK='seo-titles-upgrade-v1'

SEO={
'index.html':('Free Finance & Health Calculators | Fynzo','Use free finance, health, percentage and everyday calculators. Get instant estimates, clear formulas, examples and practical guides.'),
'mortgage-calculator.html':('Mortgage Calculator: Payment & Total Interest | Fynzo','Estimate your monthly mortgage payment, total interest and loan balance. Compare two rates or terms and view a year-by-year schedule.'),
'loan-calculator.html':('Loan Calculator: Payments, Terms & Interest | Fynzo','Estimate loan payments and total interest. Compare rates or terms, test repayment scenarios and view a year-by-year schedule.'),
'bmi-calculator.html':('BMI Calculator for Adults: Range & Limits | Fynzo','Calculate adult BMI, view the general category and understand important limitations, including why BMI may mislead muscular adults.'),
'savings-goal-calculator.html':('Savings Goal Calculator: Monthly Amount Needed | Fynzo','Calculate how much to save each month for a target and deadline. Include current savings and an estimated growth rate.'),
'compound-interest-calculator.html':('Compound Interest Calculator: Growth Over Time | Fynzo','Project investment or savings growth from an initial amount, monthly contributions, time and an estimated annual return.'),
'calorie-calculator.html':('Maintenance Calorie Calculator: BMR & TDEE | Fynzo','Estimate maintenance calories, BMR and total daily energy needs using adult measurements and a selected activity level.'),
'body-fat-calculator.html':('Body Fat Calculator: Estimate by Measurements | Fynzo','Estimate adult body-fat percentage from body measurements and review assumptions, limitations and consistent measuring tips.'),
'ideal-weight-calculator.html':('Ideal Weight Calculator: Range by Height | Fynzo','Compare reference weight estimates by height and understand why formulas differ and should not be treated as exact targets.'),
'water-intake-calculator.html':('Water Intake Calculator: Daily Amount by Weight | Fynzo','Estimate a general daily water amount from body weight and activity, with context for exercise, climate and health limitations.'),
'percentage-calculator.html':('Percentage Calculator: Change, Difference & More | Fynzo','Calculate percentages, percentage change and reverse percentages. See clear formulas and worked examples for common questions.'),
'discount-calculator.html':('Discount Calculator: Sale Price & Savings | Fynzo','Calculate the final sale price and amount saved from an original price and discount percentage, with clear worked examples.'),
'sales-tax-calculator.html':('Sales Tax Calculator: Tax Amount & Final Price | Fynzo','Estimate sales tax and the final purchase price from a pre-tax amount and tax rate. Review rounding and local-rule limitations.'),
'tip-calculator.html':('Tip Calculator: Split Bill & Total Per Person | Fynzo','Calculate a tip, final bill and amount per person. Adjust the tip percentage and party size for an instant estimate.'),
'income-tax-calculator.html':('Income Tax Calculator: Net Pay Estimate | Fynzo','Estimate tax and take-home income from gross income and an effective tax rate. Compare annual and periodic net-pay amounts.'),
'roi-calculator.html':('ROI Calculator: Return, Profit & Loss | Fynzo','Calculate return on investment, profit or loss from initial and final values. Review time, fees, tax and risk limitations.'),
'hourly-to-salary-calculator.html':('Hourly to Salary Calculator: Annual Pay | Fynzo','Convert an hourly wage into weekly, monthly and annual gross pay using your typical hours and paid weeks.'),
'fuel-cost-calculator.html':('Fuel Cost Calculator: Trip Fuel & Budget | Fynzo','Estimate trip fuel use and cost from distance, vehicle efficiency and fuel price. Keep units consistent and include the return trip.'),
'age-calculator.html':('Age Calculator: Years, Months & Days | Fynzo','Calculate age in completed years, months and days from a birth date to a selected date, including leap-year handling.'),
'date-difference-calculator.html':('Date Difference Calculator: Days Between Dates | Fynzo','Calculate elapsed days between two dates and understand inclusive counting, calendar boundaries and leap-day differences.'),
'length-converter.html':('Length Converter: Metric & Imperial Units | Fynzo','Convert length between metric and imperial units with instant results, clear unit labels and practical precision guidance.'),
'temperature-converter.html':('Temperature Converter: Celsius, Fahrenheit & Kelvin | Fynzo','Convert temperatures between Celsius, Fahrenheit and Kelvin with standard formulas and instant results.'),
'password-generator.html':('Password Generator: Create a Strong Password | Fynzo','Generate a strong random password in your browser. Choose length and character options without sending the password to a server.'),
'mortgage-guides.html':('Mortgage Guides: Payments, Rates & Terms | Fynzo','Explore mortgage calculators and guides about payments, affordability, rates, down payments, closing costs and loan terms.'),
'loan-guides.html':('Loan Guides: Payments, APR & Repayment | Fynzo','Explore loan calculators and guides about monthly payments, APR, interest, repayment terms and extra principal payments.'),
'savings-guides.html':('Savings Guides: Goals, Growth & Returns | Fynzo','Explore savings and investing calculators with guides about monthly targets, compound growth, inflation and return on investment.'),
'percentage-guides.html':('Percentage Guides: Changes, Discounts & Tax | Fynzo','Explore percentage calculators and guides covering percentage change, percentage points, discounts, tax and shopping math.'),
'health-calculators.html':('Health Calculators: BMI, Calories & Water | Fynzo','Explore BMI, calorie, body-fat, ideal-weight and water-intake calculators with clear explanations and limitations.'),
'blog.html':('Finance & Health Guides With Examples | Fynzo','Read practical, source-backed guides about mortgages, loans, savings, percentages, income and health calculators.'),
'about.html':('About Fynzo: Calculators, Methods & Review | Fynzo','Learn how Fynzo builds educational calculators, explains assumptions and limitations, and reviews practical finance and health content.'),
'contact.html':('Contact Fynzo | Questions & Feedback','Contact Fynzo with calculator questions, corrections or feedback about the website and its educational content.'),
'privacy.html':('Privacy Policy | Fynzo','Read how Fynzo handles website usage, calculator inputs, browser storage, analytics and contact information.'),
'terms.html':('Terms of Use | Fynzo','Review the terms for using Fynzo calculators, guides and educational estimates, including responsibilities and limitations.'),
'disclaimer.html':('Calculator Disclaimer | Fynzo','Understand the educational nature and limitations of Fynzo financial, health, tax, investment and everyday calculator results.'),
}

CALC_FALLBACK={
'calculator':('Calculator','Get an instant estimate with clear inputs, formulas, assumptions, limitations and practical examples.'),
'converter':('Converter','Convert values instantly with clear unit labels, standard formulas, precision guidance and practical examples.')}

def clean_title(text):
    return ' '.join(text.split())[:70].rstrip()

def clean_desc(text):
    text=' '.join(text.split())
    return text[:160].rstrip(' ,;:-')

def derive(page,soup):
    h=soup.find('h1')
    label=h.get_text(' ',strip=True) if h else page.stem.replace('-',' ').title()
    if page.name.startswith('blog-'):
        title=label
        if '| Fynzo' not in title: title += ' | Fynzo'
        meta=soup.find('meta',attrs={'name':'description'})
        desc=meta.get('content','') if meta else ''
        if not desc:
            lead=soup.select_one('.lead,.article-lead')
            desc=lead.get_text(' ',strip=True) if lead else f'Read the Fynzo guide to {label.lower()}, with practical examples, limitations and related calculators.'
        return clean_title(title),clean_desc(desc)
    kind='converter' if 'converter' in page.name else 'calculator'
    if page.name.endswith(('-calculator.html','-converter.html')):
        suffix=CALC_FALLBACK[kind][0]
        title=label if suffix.lower() in label.lower() else f'{label} {suffix}'
        return clean_title(f'{title}: Formula & Examples | Fynzo'),clean_desc(CALC_FALLBACK[kind][1])
    return clean_title(f'{label} | Fynzo'),clean_desc(f'Learn about {label.lower()} on Fynzo with clear, practical information and related tools.')

def set_meta(soup,name=None,prop=None,content=''):
    attrs={'name':name} if name else {'property':prop}
    tag=soup.find('meta',attrs=attrs)
    if not tag:
        tag=soup.new_tag('meta'); tag.attrs.update(attrs); soup.head.append(tag)
    tag['content']=content

def update_schema_names(soup,title,desc):
    for tag in soup.find_all('script',attrs={'type':'application/ld+json'}):
        try: data=json.loads(tag.string or '')
        except Exception: continue
        def walk(obj):
            if isinstance(obj,dict):
                typ=obj.get('@type')
                if typ in ('WebPage','CollectionPage','WebApplication','SoftwareApplication'):
                    if 'name' in obj: obj['name']=title.replace(' | Fynzo','')
                    if 'description' in obj: obj['description']=desc
                for v in obj.values(): walk(v)
            elif isinstance(obj,list):
                for v in obj: walk(v)
        walk(data); tag.string=json.dumps(data,ensure_ascii=False,separators=(',',':'))

def main():
    records=[]
    for page in sorted(ROOT.glob('*.html')):
        if page.name=='404.html': continue
        soup=BeautifulSoup(page.read_text(encoding='utf-8',errors='ignore'),'html.parser')
        title,desc=SEO.get(page.name,derive(page,soup))
        title,desc=clean_title(title),clean_desc(desc)
        if soup.title: soup.title.string=title
        else:
            t=soup.new_tag('title');t.string=title;soup.head.append(t)
        set_meta(soup,name='description',content=desc)
        set_meta(soup,prop='og:title',content=title)
        set_meta(soup,prop='og:description',content=desc)
        set_meta(soup,name='twitter:title',content=title)
        set_meta(soup,name='twitter:description',content=desc)
        update_schema_names(soup,title,desc)
        soup.html['data-seo-titles']=MARK
        page.write_text('<!doctype html>\n'+str(soup),encoding='utf-8')
        records.append((page.name,title,desc))
    titles=Counter(t for _,t,_ in records); descs=Counter(d for *_,d in records)
    dup_titles=[t for t,n in titles.items() if n>1]
    dup_descs=[d for d,n in descs.items() if n>1]
    if dup_titles or dup_descs:
        raise SystemExit(f'Duplicates found: titles={dup_titles}, descriptions={dup_descs}')
    report=['# SEO titles and meta descriptions','',f'Updated pages: {len(records)}','', 'Every title and meta description is unique. Titles avoid repeated keyword variants and are kept concise.','']
    for file,title,desc in records:
        report += [f'## {file}',f'- Title: {title}',f'- Meta description: {desc}','']
    (ROOT/'SEO-TITLES-REPORT.md').write_text('\n'.join(report),encoding='utf-8')
    print(f'Updated {len(records)} unique titles and meta descriptions.')
if __name__=='__main__': main()
