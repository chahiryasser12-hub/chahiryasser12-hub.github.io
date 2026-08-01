# Fynzo SEO launch plan

## Completed in the codebase

- One canonical homepage catalog with 40 unique calculator destinations.
- Valid `robots.txt` and an XML sitemap containing 77 unique indexable URLs.
- Unique title, meta description, canonical URL and one H1 on every priority page.
- WebApplication and Breadcrumb structured data on calculator pages.
- Static explanations, formulas, examples, assumptions, limitations and contextual links.
- Responsive mobile layout, accessible FAQs and fresh-network HTML through the service worker.
- Automated SEO launch gate in GitHub Actions.

## Priority indexing order

1. `/`
2. `/mortgage-calculator.html`
3. `/mortgage-total-cost-calculator.html`
4. `/loan-calculator.html`
5. `/auto-loan-calculator.html`
6. `/compound-interest-calculator.html`
7. `/bmi-calculator.html`
8. `/calorie-calculator.html`
9. `/percentage-calculator.html`
10. `/savings-goal-calculator.html`
11. `/work-hours-calculator.html`

## Manual owner actions

1. Add `fynzo.me` as a Domain property in Google Search Console.
2. Verify ownership using the DNS TXT record supplied by Google.
3. Submit `https://fynzo.me/sitemap.xml` once.
4. Inspect the priority URLs above and request indexing once after deployment.
5. Confirm that the live test sees the rendered calculator, canonical URL and indexable status.
6. Review Page indexing and Core Web Vitals weekly during the first month.

Do not add a fabricated verification token to the repository. The DNS value must come from the site owner's Search Console account.

## First 90 days

### Days 1 to 14

- Deploy this package and run the GitHub Action once.
- Complete Search Console verification and submit the sitemap.
- Check the 11 priority URLs for indexing and rendering.
- Fix any live-only 404, DNS, HTTPS or canonical problem immediately.

### Days 15 to 45

- Publish two useful guides per week inside the existing Mortgage, Loan, Savings and Health clusters.
- Link every new guide to one primary calculator and two closely related pages.
- Keep examples specific, assumptions visible and claims supported by reliable sources.
- Avoid number-swapped or near-duplicate pages.

### Days 46 to 90

- Use Search Console queries rather than guessed search volume.
- Improve pages receiving impressions at positions 8 to 30.
- Rewrite weak titles only when impressions are meaningful and CTR is poor.
- Add sections that answer real queries not already covered.
- Earn a small number of relevant editorial links to the strongest calculators and guides.

## Weekly measurements

- Valid indexed pages
- Impressions and clicks
- Non-brand queries
- Average position by page and query
- CTR on pages with meaningful impressions
- Calculator-result interactions
- New relevant referring domains

## Rule for future pages

Create a new URL only when it serves a distinct user intent and offers substantial unique value. Do not generate thin pages by changing only a number, city, year or keyword.
