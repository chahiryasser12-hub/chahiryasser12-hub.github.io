/* Fynzo Service Worker — offline support + fast repeat visits */
const CACHE = "fynzo-v1";
const CORE = ["/", "/index.html", "/styles.css", "/fynzo.js", "/favicon.svg", "/hero.svg", "/logo-full.svg", "/blog.html", "/about.html", "/manifest.json", "/mortgage-calculator.html", "/loan-calculator.html", "/compound-interest-calculator.html", "/savings-goal-calculator.html", "/income-tax-calculator.html", "/roi-calculator.html", "/hourly-to-salary-calculator.html", "/bmi-calculator.html", "/calorie-calculator.html", "/body-fat-calculator.html", "/ideal-weight-calculator.html", "/water-intake-calculator.html"];
self.addEventListener("install", function(e){
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(function(c){ return c.addAll(CORE); }).catch(function(){}));
});
self.addEventListener("activate", function(e){
  e.waitUntil(caches.keys().then(function(keys){
    return Promise.all(keys.filter(function(k){ return k!==CACHE; }).map(function(k){ return caches.delete(k); }));
  }));
  self.clients.claim();
});
/* Stale-while-revalidate for same-origin GET; network-first fallback to cache offline */
self.addEventListener("fetch", function(e){
  const req = e.request;
  if(req.method!=="GET" || new URL(req.url).origin!==location.origin) return;
  e.respondWith(
    caches.match(req).then(function(cached){
      const net = fetch(req).then(function(res){
        if(res && res.status===200){ const copy=res.clone(); caches.open(CACHE).then(function(c){ c.put(req, copy); }); }
        return res;
      }).catch(function(){ return cached || caches.match("/index.html"); });
      return cached || net;
    })
  );
});
