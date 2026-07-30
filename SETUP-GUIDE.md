# 📊 Search Console + Analytics Setup (after going live)

## GA4
1. analytics.google.com → Start measuring → property "Fynzo", timezone Morocco.
2. Web stream → your domain → copy Measurement ID (G-D7NJ4T2ZK4).
3. Find-and-replace G-D7NJ4T2ZK4 in ALL .html with your ID → re-upload.
4. Reports → Realtime should show you.

## Search Console
1. search.google.com/search-console (same Google account).
2. Domain property → add TXT record in your DNS → Verify.
3. Sitemaps → submit `sitemap.xml`.
4. Inspect homepage URL → Request indexing.

## Link them
Analytics → Admin → Product Links → Search Console Links → Link → pick property + web stream.
Reports → Library → publish the two "Organic Search" collections. Data ~48h later.
