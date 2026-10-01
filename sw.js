// Network only: prices and menus must stay current.
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(self.clients.claim()));
self.addEventListener('fetch', event => {
  if (event.request.mode === 'navigate') event.respondWith(fetch(event.request).catch(() => new Response('<!doctype html><meta name="viewport" content="width=device-width"><title>One For All</title><body style="background:#EF3D3D;color:#FFF6EE;font:18px system-ui;padding:32px"><h1>One For All</h1><p>Connect to see the current menu.</p><p lang="ar" dir="rtl">اتصل بالإنترنت لتشوف المنيو الحالي.</p><button onclick="location.reload()">Try again · جرّب مرة ثانية</button>', {headers:{'content-type':'text/html; charset=utf-8'}})));
});
