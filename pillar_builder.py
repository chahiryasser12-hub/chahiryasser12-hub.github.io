#!/usr/bin/env python3
"""Build and maintain Fynzo topic pillar pages. Safe to re-run."""
from pathlib import Path
from html import escape
from datetime import date
import re

ROOT = Path(__file__).resolve().parent
DOMAIN = "https://fynzo.me/"
TODAY = date.today().isoformat()

PILLARS = {
    "mortgage-guides.html": {
        "title": "Mortgage Guides & Calculators",
        "eyebrow": "Mortgage hub",
        "description": "Plan a home purchase with Fynzo mortgage calculators and practical guides about affordability, rates, down payments, closing costs and loan terms.",
        "intro": "Use the calculator first, then explore the guides to compare affordability, rates, upfront cash and repayment choices.",
        "calculators": [("mortgage-calculator.html", "Mortgage Calculator", "Estimate monthly payment, interest and the remaining balance.")],
        "articles": [
            ("blog-how-much-house-can-i-afford.html", "How Much House Can I Afford?", "Estimate a realistic home budget before comparing properties."),
            ("blog-compare-mortgage-rates.html", "Compare Mortgage Rates", "Compare payment, interest, fees and break-even points."),
            ("blog-down-payment-and-closing-costs.html", "Down Payment vs Closing Costs", "Separate the loan-reducing down payment from transaction costs."),
            ("blog-fixed-vs-variable-rate.html", "Fixed vs Variable Rates", "Understand payment certainty and rate-change risk."),
            ("blog-loan-term-36-vs-60-months.html", "Loan Term Comparison", "See how a shorter or longer term changes payment and interest."),
        ],
        "keywords": ("mortgage", "house", "home", "down-payment", "renting-vs-buying", "save-for-down-payment"),
    },
    "loan-guides.html": {
        "title": "Loan Guides & Calculators",
        "eyebrow": "Loan hub",
        "description": "Compare loan payments, interest rates, APR, repayment terms and extra payments with free Fynzo tools and guides.",
        "intro": "Model the payment, then use the guides to compare the full borrowing cost and repayment strategy.",
        "calculators": [("loan-calculator.html", "Loan Calculator", "Estimate monthly payment, total interest and payoff schedule.")],
        "articles": [
            ("blog-pay-off-loan-faster.html", "Pay Off a Loan Faster", "Practical ways to reduce interest and shorten repayment."),
            ("blog-fixed-vs-variable-rate.html", "Fixed vs Variable Rates", "Compare certainty with exposure to future rate changes."),
            ("blog-loan-term-36-vs-60-months.html", "36 vs 60 Months", "Compare monthly affordability with total interest."),
            ("blog-apr-vs-interest-rate.html", "APR vs Interest Rate", "Learn what each borrowing-cost number represents."),
            ("blog-extra-loan-payments.html", "Extra Principal Payments", "See how additional principal may change payoff."),
        ],
        "keywords": ("loan", "debt", "credit", "apr", "interest-rate", "pay-off"),
    },
    "savings-guides.html": {
        "title": "Savings & Investing Guides",
        "eyebrow": "Savings hub",
        "description": "Set savings goals, understand compound growth and compare investment returns with Fynzo calculators and practical guides.",
        "intro": "Choose a target and deadline, test your monthly contribution, then explore growth, inflation and return concepts.",
        "calculators": [
            ("savings-goal-calculator.html", "Savings Goal Calculator", "Calculate how much to save each month."),
            ("compound-interest-calculator.html", "Compound Interest Calculator", "Project contributions and compound growth."),
            ("roi-calculator.html", "ROI Calculator", "Measure basic profit or loss as a percentage."),
        ],
        "articles": [
            ("blog-how-much-to-save-each-month.html", "How Much Should You Save Each Month?", "Turn a goal into a realistic monthly plan."),
            ("blog-compound-interest-explained.html", "Compound Interest Explained", "Understand how time and reinvestment affect growth."),
            ("blog-emergency-fund-target.html", "Set an Emergency Fund Target", "Build a target around essential expenses and stability."),
            ("blog-choose-savings-deadline.html", "Choose a Savings Deadline", "See why the deadline changes the monthly amount."),
            ("blog-compound-frequency-explained.html", "Monthly vs Annual Compounding", "Compare compounding frequencies consistently."),
            ("blog-inflation-and-future-value.html", "Inflation and Future Value", "Separate nominal balance from buying power."),
            ("blog-roi-limitations.html", "What ROI Leaves Out", "Add time, fees, risk and tax context to ROI."),
        ],
        "keywords": ("saving", "savings", "compound", "invest", "roi", "emergency-fund", "inflation"),
    },
    "percentage-guides.html": {
        "title": "Percentage Guides & Calculators",
        "eyebrow": "Percentage hub",
        "description": "Calculate percentages, discounts and sales tax, then learn percentage change, percentage points and stacked discounts.",
        "intro": "Use the calculators for quick results and the guides to avoid common percentage and shopping-math mistakes.",
        "calculators": [
            ("percentage-calculator.html", "Percentage Calculator", "Find percentages, changes and reverse percentages."),
            ("discount-calculator.html", "Discount Calculator", "Calculate sale prices and savings."),
            ("sales-tax-calculator.html", "Sales Tax Calculator", "Estimate tax and final price."),
            ("tip-calculator.html", "Tip Calculator", "Calculate tips and split totals."),
        ],
        "articles": [
            ("blog-master-percentages.html", "Master Percentages", "Learn the core formulas with practical examples."),
            ("blog-percentage-change-vs-points.html", "Percentage Change vs Percentage Points", "Use the correct measure and label."),
            ("blog-stacked-discounts.html", "Why Discounts Do Not Simply Add", "Combine sequential discounts accurately."),
            ("blog-sales-tax-and-discounts.html", "Sales Tax and Discounts", "Understand the taxable base and calculation order."),
        ],
        "keywords": ("percentage", "percent", "discount", "sales-tax", "tip"),
    },
    "health-calculators.html": {
        "title": "Health Calculators & Guides",
        "eyebrow": "Health hub",
        "description": "Explore BMI, calorie, body-fat, ideal-weight and water-intake calculators with clear guides about their use and limitations.",
        "intro": "These estimates are educational starting points, not diagnoses. Use the guides to understand limitations and when professional advice matters.",
        "calculators": [
            ("bmi-calculator.html", "BMI Calculator", "Estimate body mass index from height and weight."),
            ("calorie-calculator.html", "Calorie Calculator", "Estimate BMR and daily energy needs."),
            ("body-fat-calculator.html", "Body Fat Calculator", "Estimate body-fat percentage from measurements."),
            ("ideal-weight-calculator.html", "Ideal Weight Calculator", "Compare several reference formulas."),
            ("water-intake-calculator.html", "Water Intake Calculator", "Estimate a general daily hydration target."),
        ],
        "articles": [
            ("blog-how-to-calculate-bmi.html", "How to Calculate BMI", "Learn the formula, categories and context."),
            ("blog-how-many-calories-should-i-eat.html", "How Many Calories Should I Eat?", "Estimate daily needs and understand activity assumptions."),
            ("blog-bmi-limitations.html", "When BMI Can Mislead", "Understand what BMI does and does not measure."),
            ("blog-measure-body-circumferences.html", "Measure Body Circumferences", "Improve consistency in circumference-based estimates."),
            ("blog-maintenance-calories.html", "Maintenance Calories", "Treat formula output as a starting estimate."),
            ("blog-hydration-needs-vary.html", "Why Water Needs Vary", "Adjust general estimates for activity, climate and health."),
            ("blog-ideal-weight-formulas.html", "Ideal-Weight Formulas", "Understand why reference equations give different answers."),
        ],
        "keywords": ("bmi", "calorie", "body-fat", "health", "weight", "hydration", "water", "nutrition"),
    },
}

STYLE = """
.pillar-intro{max-width:780px;margin:0 auto 28px;text-align:center;color:var(--muted);font-size:17px}
.pillar-section{margin:34px 0}.pillar-section h2{font-size:26px;margin-bottom:14px}
.pillar-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
.pillar-card{display:block;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:20px;transition:.2s}
.pillar-card:hover{transform:translateY(-3px);box-shadow:var(--shadow);border-color:var(--green)}
.pillar-card strong{display:block;font-size:17px;margin-bottom:6px}.pillar-card span{color:var(--muted);font-size:14px}
.pillar-note{margin-top:30px;padding:18px;border-left:4px solid var(--green);background:var(--bg);border-radius:0 12px 12px 0;color:var(--muted)}
""".strip()


def exists(href):
    return (ROOT / href).exists()


def card(href, title, desc, upcoming=False):
    label = "Coming soon: " if upcoming else ""
    attrs = ' aria-disabled="true" class="pillar-card"' if upcoming else ' class="pillar-card"'
    target = href if not upcoming else "blog.html"
    return f'<a href="{escape(target)}"{attrs}><strong>{label}{escape(title)}</strong><span>{escape(desc)}</span></a>'


def schema_for(page, cfg, live_items):
    import json
    items = [{"@type":"ListItem","position":i+1,"name":t,"url":DOMAIN+h} for i,(h,t,_) in enumerate(live_items)]
    return json.dumps({"@context":"https://schema.org","@type":"CollectionPage","name":cfg["title"],"description":cfg["description"],"url":DOMAIN+page,"mainEntity":{"@type":"ItemList","itemListElement":items}}, ensure_ascii=False)


def build_page(page, cfg):
    calculators = [x for x in cfg["calculators"] if exists(x[0])]
    live_articles = [x for x in cfg["articles"] if exists(x[0])]
    all_live = calculators + live_articles
    calc_html = "".join(card(*x) for x in calculators)
    article_html = "".join(card(*x, upcoming=not exists(x[0])) for x in cfg["articles"])
    schema = schema_for(page, cfg, all_live)
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(cfg['title'])} | Fynzo</title><meta name="description" content="{escape(cfg['description'])}">
<meta name="robots" content="index,follow"><link rel="canonical" href="{DOMAIN}{page}">
<meta property="og:type" content="website"><meta property="og:title" content="{escape(cfg['title'])} | Fynzo"><meta property="og:description" content="{escape(cfg['description'])}"><meta property="og:url" content="{DOMAIN}{page}"><meta property="og:image" content="{DOMAIN}og-default.png">
<link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="styles-premium.css"><script type="application/ld+json">{schema}</script><script src="fynzo.js" defer></script>
<style>{STYLE}</style></head><body>
<a class="skip-link" href="#main">Skip to content</a>
<header><nav><a class="brand" href="index.html">Fynzo</a><div class="nav-links"><a href="index.html#tools">Calculators</a><a href="blog.html">Blog</a><a href="about.html">About</a><a class="nav-btn" href="index.html#tools">Start free</a></div></nav></header>
<main id="main"><section class="page-head"><div class="wrap"><div class="eyebrow">{escape(cfg['eyebrow'])}</div><h1>{escape(cfg['title'])}</h1><p class="updated">Last updated: {TODAY}</p></div></section>
<nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a> › {escape(cfg['title'])}</nav>
<section class="content"><div class="wrap"><p class="pillar-intro">{escape(cfg['intro'])}</p>
<div class="pillar-section"><h2>Start with a calculator</h2><div class="pillar-grid">{calc_html}</div></div>
<div class="pillar-section"><h2>Learn with practical guides</h2><div class="pillar-grid">{article_html}</div></div>
<p class="pillar-note">Fynzo calculators provide educational estimates. Check current official information and qualified professional advice for important financial or health decisions.</p>
</div></section></main>
<footer><div class="wrap"><div class="foot"><div class="foot-brand"><strong>Fynzo</strong><p>Free, fast and private calculators for everyday decisions.</p></div><div><h4>Guides</h4><a href="mortgage-guides.html">Mortgage</a><a href="loan-guides.html">Loans</a><a href="savings-guides.html">Savings</a></div><div><h4>More</h4><a href="percentage-guides.html">Percentages</a><a href="health-calculators.html">Health</a><a href="blog.html">All guides</a></div><div><h4>Legal</h4><a href="privacy.html">Privacy</a><a href="terms.html">Terms</a><a href="disclaimer.html">Disclaimer</a></div></div><div class="foot-bottom">© 2026 Fynzo</div></div></footer></body></html>'''
    (ROOT / page).write_text(html, encoding="utf-8")


def choose_pillar(filename, text=""):
    hay = (filename + " " + text).lower()
    scores = []
    for page,cfg in PILLARS.items():
        score = sum(1 for k in cfg["keywords"] if k in hay)
        if filename in [x[0] for x in cfg["calculators"] + cfg["articles"]]: score += 10
        scores.append((score,page))
    score,page = max(scores)
    return page if score else None


def inject_backlink(path):
    if path.name in PILLARS or path.name in ("index.html","blog.html","404.html"): return
    text = path.read_text(encoding="utf-8", errors="ignore")
    if 'data-pillar-link="true"' in text: return
    pillar = choose_pillar(path.name, re.sub(r"<[^>]+>", " ", text)[:5000])
    if not pillar: return
    title = PILLARS[pillar]["title"]
    block = f'<p class="pillar-backlink" data-pillar-link="true"><a href="{pillar}">Explore all {escape(title)}</a></p>'
    for marker in ('</main>', '</article>', '</body>'):
        if marker in text:
            text = text.replace(marker, block + marker, 1)
            path.write_text(text, encoding="utf-8")
            return


def update_sitemap():
    path = ROOT / "sitemap.xml"
    if not path.exists(): return
    text = path.read_text(encoding="utf-8", errors="ignore")
    for page in PILLARS:
        url = DOMAIN + page
        if url not in text:
            node = f'  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n'
            text = text.replace('</urlset>', node + '</urlset>')
    path.write_text(text, encoding="utf-8")


def update_global_styles():
    path = ROOT / 'styles.css'
    if not path.exists(): return
    text = path.read_text(encoding='utf-8', errors='ignore')
    if 'Fynzo pillar pages' not in text:
        text += '\n/* Fynzo pillar pages */\n' + STYLE + '\n.pillar-backlink{max-width:940px;margin:24px auto;padding:14px 22px;text-align:center}.pillar-backlink a{color:var(--green);font-weight:700}\n'
        path.write_text(text, encoding='utf-8')

def update_index():
    path = ROOT / "index.html"
    if not path.exists(): return
    text = path.read_text(encoding="utf-8", errors="ignore")
    if 'data-pillar-directory="true"' in text: return
    links = ''.join(f'<a class="pillar-card" href="{p}"><strong>{escape(c["title"])}</strong><span>{escape(c["description"])}</span></a>' for p,c in PILLARS.items())
    block = f'<section class="sec" data-pillar-directory="true"><div class="wrap"><div class="sec-head"><h2>Explore our guide hubs</h2><p>Calculators and articles organized by topic.</p></div><div class="pillar-grid">{links}</div></div></section>'
    marker = '<footer' if '<footer' in text else ('</main>' if '</main>' in text else '</body>')
    if marker == '<footer':
        text = text.replace(marker, block + marker, 1)
    else:
        text = text.replace(marker, block + marker, 1)
    path.write_text(text, encoding="utf-8")


def update_workflow():
    path = ROOT / '.github/workflows/publish-weekly-blog.yml'
    if not path.exists(): return
    text = path.read_text(encoding='utf-8', errors='ignore')
    if 'python pillar_builder.py' not in text:
        needle = 'run: python weekly_publisher.py'
        if needle in text:
            text = text.replace(needle, needle + '\n      - name: Refresh pillar pages and links\n        run: python pillar_builder.py')
            path.write_text(text, encoding='utf-8')


def main():
    for page,cfg in PILLARS.items(): build_page(page,cfg)
    update_global_styles()
    update_index()
    for path in ROOT.glob('*.html'): inject_backlink(path)
    update_sitemap()
    update_workflow()
    print('Built 5 pillar pages, added contextual backlinks, updated homepage, sitemap and workflow.')

if __name__ == '__main__': main()
