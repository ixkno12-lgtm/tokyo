const C='tokyo-v7';
const FILES=['./','index.html','manifest.webmanifest','icon-192.png','icon-512.png','icon-180.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(FILES)));self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==C).map(k=>caches.delete(k)))));self.clients.claim()});
const put=(req,r)=>{if(r&&(r.ok||r.type==='opaque')){const cp=r.clone();caches.open(C).then(c=>c.put(req,cp))}return r};
self.addEventListener('fetch',e=>{
  const req=e.request;if(req.method!=='GET')return;const u=new URL(req.url);
  if(req.mode==='navigate'){e.respondWith(fetch(req).then(r=>put('./',r)).catch(()=>caches.match('./')));return}
  if(u.pathname.endsWith('news.json')||u.hostname.includes('open-meteo')||u.hostname.includes('er-api')){e.respondWith(fetch(req).catch(()=>caches.match(req,{ignoreSearch:true})));return}
  e.respondWith(caches.match(req).then(hit=>hit||fetch(req).then(r=>put(req,r))));
});
