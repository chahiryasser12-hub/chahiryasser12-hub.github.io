#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
 Fynzo — SEO + Design AUTO-FIX  (2026)
============================================================
Run this ONCE inside your repo folder (where index.html lives):

    python seo-autofix.py

What it does to EVERY .html file (safe + idempotent — you can
re-run it any time, it never double-inserts):

  1. Canonical URL            -> stops duplicate-content loss
  2. Open Graph tags          -> clean previews on FB/LinkedIn/WhatsApp/Slack
  3. Twitter Card tags        -> clean previews on X
  4. hreflang (en/fr/ar + x-default) -> correct language targeting
  5. <meta name="robots">     -> index,follow, rich snippets
  6. theme-color              -> branded mobile browser bar
  7. Links styles-premium.css -> premium design layer
  8. Skip-to-content link     -> accessibility (E-E-A-T trust)
  9. lang/dir on <html>       -> RTL for /ar/, correct lang for /fr/

It DOES NOT touch your content, calculators, JS logic or schema.
Make a git commit before running so you can review the diff.
============================================================
"""
import os, re, sys

# ---- CONFIG ----------------------------------------------------
DOMAIN     = "https://fynzo.me"          # <-- change if your domain changes
DEFAULT_OG = "/og-default.svg"           # fallback share image (1200x630 ideally: use .png)
BRAND      = "Fynzo"
LANGS      = []                 # sub-folder languages that mirror the root (EN)
MARK       = "<!-- fynzo-seo v1 -->"      # idempotency marker
# ---------------------------------------------------------------

def read(p):
    with open(p, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def write(p, s):
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)

def get_tag(html, pattern):
    m = re.search(pattern, html, re.I | re.S)
    return m.group(1).strip() if m else ""

def rel_url(path, root):
    """Return site-absolute path like /bmi-calculator.html or /fr/bmi-calculator.html"""
    rel = os.path.relpath(path, root).replace(os.sep, "/")
    return "/" + rel

def lang_of(rel):
    parts = rel.strip("/").split("/")
    if parts and parts[0] in LANGS:
        return parts[0]
    return "en"

def page_name(rel):
    """filename only, e.g. bmi-calculator.html"""
    return rel.strip("/").split("/")[-1]

def hreflang_block(rel):
    """Build en/fr/ar/x-default alternates for this page."""
    name = page_name(rel)
    en = f"{DOMAIN}/{name}"
    out = [f'<link rel="alternate" hreflang="en" href="{en}">']
    for lg in LANGS:
        out.append(f'<link rel="alternate" hreflang="{lg}" href="{DOMAIN}/{lg}/{name}">')
    out.append(f'<link rel="alternate" hreflang="x-default" href="{en}">')
    return "\n".join(out)

def build_head_block(html, rel):
    title = get_tag(html, r"<title[^>]*>(.*?)</title>")
    if not title:
        title = BRAND
    desc = get_tag(html, r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']')
    canonical = f"{DOMAIN}{rel}"
    og_img = DOMAIN + DEFAULT_OG
    # try to reuse a page-specific og image if one is already referenced
    m = re.search(r'og-([a-z0-9]+)\.(svg|png|jpg)', html, re.I)
    if m:
        og_img = f"{DOMAIN}/og-{m.group(1)}.{m.group(2)}"

    lg = lang_of(rel)
    esc = lambda s: s.replace('"', "&quot;")

    b = [MARK]
    # robots + theme-color (only if not already present)
    if not re.search(r'name=["\']robots["\']', html, re.I):
        b.append('<meta name="robots" content="index, follow, max-image-preview:large">')
    if not re.search(r'name=["\']theme-color["\']', html, re.I):
        b.append('<meta name="theme-color" content="#0b1020">')
    # canonical (only if not present)
    if not re.search(r'rel=["\']canonical["\']', html, re.I):
        b.append(f'<link rel="canonical" href="{canonical}">')
    # hreflang (only if not present)
    if not re.search(r'hreflang=', html, re.I):
        b.append(hreflang_block(rel))
    # Open Graph (only if not present)
    if not re.search(r'property=["\']og:title["\']', html, re.I):
        b += [
            f'<meta property="og:type" content="website">',
            f'<meta property="og:site_name" content="{BRAND}">',
            f'<meta property="og:locale" content="{ {"en":"en_US","fr":"fr_FR","ar":"ar_MA"}[lg] }">',
            f'<meta property="og:title" content="{esc(title)}">',
            f'<meta property="og:description" content="{esc(desc)}">',
            f'<meta property="og:url" content="{canonical}">',
            f'<meta property="og:image" content="{og_img}">',
            f'<meta property="og:image:width" content="1200">',
            f'<meta property="og:image:height" content="630">',
        ]
    # Twitter Card (only if not present)
    if not re.search(r'name=["\']twitter:card["\']', html, re.I):
        b += [
            f'<meta name="twitter:card" content="summary_large_image">',
            f'<meta name="twitter:title" content="{esc(title)}">',
            f'<meta name="twitter:description" content="{esc(desc)}">',
            f'<meta name="twitter:image" content="{og_img}">',
        ]
    # premium css link (only if not already linked)
    if "styles-premium.css" not in html:
        b.append('<link rel="stylesheet" href="/styles-premium.css">')
    return "\n".join(b) + "\n"

def fix_html_attrs(html, rel):
    lg = lang_of(rel)
    # set lang + dir on <html>
    if re.search(r"<html[^>]*>", html, re.I):
        def repl(m):
            tag = m.group(0)
            tag = re.sub(r'\slang=["\'][^"\']*["\']', "", tag, flags=re.I)
            tag = re.sub(r'\sdir=["\'][^"\']*["\']', "", tag, flags=re.I)
            attrs = f' lang="{lg}"'
            if lg == "ar":
                attrs += ' dir="rtl"'
            return tag[:-1] + attrs + ">"
        html = re.sub(r"<html[^>]*>", repl, html, count=1, flags=re.I)
    return html

def add_skip_link(html):
    if "skip-link" in html:
        return html
    m = re.search(r"<body[^>]*>", html, re.I)
    if not m:
        return html
    link = '\n<a href="#main" class="skip-link">Skip to content</a>'
    i = m.end()
    return html[:i] + link + html[i:]

def process(path, root):
    html = read(path)
    if MARK in html:
        return "skipped (already done)"
    rel = rel_url(path, root)
    block = build_head_block(html, rel)

    # inject block right before </head>
    if re.search(r"</head>", html, re.I):
        html = re.sub(r"</head>", block + "</head>", html, count=1, flags=re.I)
    else:  # no head? prepend
        html = block + html

    html = fix_html_attrs(html, rel)
    html = add_skip_link(html)
    write(path, html)
    return "fixed"

def main():
    root = os.getcwd()
    n_fixed = n_skip = 0
    for dirpath, _, files in os.walk(root):
        for fn in files:
            if fn.lower().endswith(".html"):
                p = os.path.join(dirpath, fn)
                res = process(p, root)
                print(f"  [{res:>22}]  {rel_url(p, root)}")
                if res == "fixed":
                    n_fixed += 1
                else:
                    n_skip += 1
    print(f"\nDone. {n_fixed} pages fixed, {n_skip} already up-to-date.")
    print("Tip: run `git diff` to review, then commit.")

if __name__ == "__main__":
    main()
