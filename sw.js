/* Fynzo Service Worker: resilient offline shell with fresh HTML. */
const CACHE_VERSION="fynzo-production-v24-20260802";
const STATIC_CACHE=CACHE_VERSION+"-static";
const PAGE_CACHE=CACHE_VERSION+"-pages";
const OFFLINE_URL="/offline.html";
const STATIC_ASSETS=["/styles.css","/fynzo.js","/advanced.js","/tool-actions.js","/pdf-report-v2.js","/result-insights.js","/visual-results.js","/favicon.svg","/icon-192.png","/icon-512.png","/icon-maskable-512.png","/manifest.json","/og-default.png"];
const CORE_PAGES=["/","/index.html","/blog.html","/about.html","/contact.html","/mortgage-calculator.html","/loan-calculator.html","/bmi-calculator.html",OFFLINE_URL];
self.addEventListener("install",event=>{event.waitUntil(Promise.all([caches.open(STATIC_CACHE).then(c=>c.addAll(STATIC_ASSETS)),caches.open(PAGE_CACHE).then(c=>c.addAll(CORE_PAGES))]).then(()=>self.skipWaiting()));});
self.addEventListener("activate",event=>{event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(key=>!key.startsWith(CACHE_VERSION)).map(key=>caches.delete(key)))).then(()=>self.clients.claim()));});
self.addEventListener("fetch",event=>{
  const request=event.request;
  if(request.method!=="GET")return;
  const target=new URL(request.url);
  if(target.origin!==self.location.origin)return;
  const acceptsHTML=request.mode==="navigate"||(request.headers.get("accept")||"").includes("text/html");
  if(acceptsHTML){
    event.respondWith(fetch(request).then(response=>{if(response&&response.ok)caches.open(PAGE_CACHE).then(c=>c.put(request,response.clone()));return response;}).catch(()=>caches.match(request).then(cached=>cached||caches.match(OFFLINE_URL))));
    return;
  }
  event.respondWith(caches.match(request).then(cached=>cached||fetch(request).then(response=>{if(response&&response.ok)caches.open(STATIC_CACHE).then(c=>c.put(request,response.clone()));return response;})));
});
