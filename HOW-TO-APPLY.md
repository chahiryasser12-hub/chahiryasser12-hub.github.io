# 🔧 How to apply this SEO kit to your EXISTING repo (nothing gets deleted)

Your GitHub repo (blog, auto-publisher, 22 tools × 3 languages, content) stays exactly as it is.
You only **ADD** or **tweak** a few files. Do these in GitHub directly (Add file → Upload / Edit).

---

## 1) ADD these new files (drag into repo root)
- `404.html`  → nice not-found page that keeps visitors on-site.
- `ads.txt`   → required for AdSense (edit your publisher ID after approval).
- `robots.txt` → REPLACE your current one with this version (it now welcomes AI crawlers so
  ChatGPT / Perplexity / Google AI Overviews can cite you — a real 2026 ranking edge).

## 2) TWO tiny edits (find & replace across all files in a code editor)
- `chahiryasser12@gmail.com` → your real email.
- In `contact.html`: `formspree.io/f/configured Formspree form ID` → your real Formspree endpoint
  (free at formspree.io) so the contact form actually sends.

## 3) The ONE bug fix (language switcher going back to EN)
Open `fynzo.js`, find the language-switch function, and make sure it uses **absolute** paths so
the language sticks. It should look like this:

```javascript
function slug(){return location.pathname.split("/").pop()||"index.html";}
function sw(to){window.location=(to==="en"?"/":"/"+to+"/")+slug();}
```

That keeps you on the same page in the same language. Commit → fixed.

## 4) Add a visible "Last updated" line (freshness = trust = E-E-A-T)
On calculator pages, near the `<h1>` intro, you can add:
```html
<p style="color:var(--muted);font-size:13px">Last updated: July 2026</p>
```
Small signal, real trust boost with Google.

---

## 5) After the site is live — do these in order
1. **Google Search Console** → add property `https://fynzo.me` → verify → submit `sitemap.xml`.
2. **URL Inspection** → Request indexing for your top 5 pages (mortgage, loan, bmi, calorie, percentage).
3. Wait for HTTPS green + first impressions (days).
4. Start **directory submissions + Reddit/Quora answers** (biggest untapped lever).
5. Keep your **blog auto-publisher** running — steady content is exactly what 2026 rewards.
6. When you have ~15–20 solid pages + some traffic → **apply for AdSense**, then paste your
   publisher line into `ads.txt`.

---

## ✅ What you already have (don't touch — it's good!)
- 22 calculators × EN/FR/AR (hreflang) ✅
- Blog + auto-publish workflow ✅
- WebApplication + FAQPage + Organization schema ✅
- Internal-linking silo + breadcrumbs ✅
- PWA (installable + offline) + real PNG icons ✅
- GA4 + sitemap + CNAME ✅
- Legal pages (privacy/terms/about/contact/disclaimer) — AdSense-ready ✅

**You are 90% there.** This kit closes the last 10%: AI-crawler access, 404, ads.txt,
the switcher fix, and a weekly authority routine. Follow MASTER-SEO-2026.md and stay consistent.
