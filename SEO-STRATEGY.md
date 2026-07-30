# 🚀 Fynzo — SEO Strategy & Checklist

What's **already built into the site** ✅ and what **you do next** 🔜.

## ✅ Already done (in the code)
| Item | Status |
|------|--------|
| **On-page SEO** — 300–500+ words of real content on every calculator page | ✅ |
| **H1/H2/H3 structure** + internal links between all 12 calculators | ✅ |
| **Schema markup** — `WebApplication` + `FAQPage` on every calculator page | ✅ |
| **FAQ section** (3 Q&A) under each calculator + FAQ schema | ✅ |
| **Instant client-side calc** (no reload) + **Copy result / Copy link / Save PDF** | ✅ |
| **Clean UX** — no forced sign-up, minimal ads, mobile-first | ✅ |
| **Sitemap.xml (24 URLs) + robots.txt** | ✅ |
| **hreflang** tags (en / fr / ar / x-default) on every page | ✅ |
| **Multi-language** UI (EN/FR/AR) + **dark mode** (light default) | ✅ |
| **Core Web Vitals**: instant INP (client-side JS), no CLS (img width/height set, no layout jumps) | ✅ |
| **GA4 + Search Console ready** (see SETUP-GUIDE.md) | ✅ |

## 🔜 What YOU do next

### 1. Keyword research
Use **KEYWORDS.md** as your map. Verify volumes in Google Keyword Planner / Ahrefs,
then weave the primary keyword naturally into each page's title, H1 and first paragraph
(already drafted — refine with your researched terms).

### 2. Tech stack note
This is **static HTML/CSS/JS** — which is actually *ideal* for SEO: it's already
server-side rendered (plain HTML), lightning fast, and Google crawls it perfectly.
You do **not** need Next.js/React for this. If you ever scale to 100s of pages with a
database, revisit a framework — but for now, static wins on speed + simplicity + cost.
✔️ Mobile-friendly · ✔️ HTTPS (enable free SSL on your host) · ✔️ Sitemap submitted.

### 3. Off-page SEO & link building
- Answer real questions on **Reddit** (r/personalfinance, r/fitness), **Quora**, niche forums — link your calculator only when genuinely helpful.
- Share tools in **Facebook groups**, Discord servers, and on X/LinkedIn.
- List on free tool directories (e.g. "free calculator" roundups).
- Guest-post on small finance/health blogs with a link back.

### 4. Monitoring
- **Google Search Console**: track keyword rankings, impressions, clicks, indexing.
- **Google Analytics 4**: organic traffic, top pages, bounce, devices.
- Review monthly → double down on pages that gain traction.

## 💡 Optional growth ideas (later)
- **Programmatic SEO** (scaling): generate targeted variants, e.g.
  "Loan Calculator for Cars", "Mortgage Calculator 15-Year", "BMI Calculator for Women".
  ⚠️ Only if each variant has **genuinely unique content/value** — thin duplicate pages
  trigger Google's "scaled content abuse" penalty. Quality per page > quantity.
- **Export/share** (done: copy link + PDF) — encourages user-generated sharing = backlinks.
- **Localization** — you have EN/FR/AR UI. For full SEO in each language, translate the
  page *bodies* too and keep the hreflang tags (already present).
- **Core Web Vitals** — keep images sized, avoid heavy third-party scripts, lazy-load ads.

## 🗓️ Publishing rhythm (avoid penalties)
Publish **2–3 quality posts per week**, not 30 at once. Steady + high-quality =
Google trust. Add real experience/examples to any AI-drafted content before publishing.
