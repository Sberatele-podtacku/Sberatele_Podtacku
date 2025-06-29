// sw.js

const CACHE_NAME = 'beer-mats-v1';
const ASSETS = [
  '/',                  // index.html
  '/metadata.json',
  '/index.html',
  '/sw.js',
  // pre-cache your logos and maybe a handful of thumbnails:
  '/images/logo1.png',
  '/images/logo2.png',
  // optionally add '/images/00001_front.png', etc.
];

// Install: pre-cache core assets
self.addEventListener('install', evt => {
  evt.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(ASSETS))
      .then(() => self.skipWaiting())
  );
});

// Activate: clean up old caches
self.addEventListener('activate', evt => {
  evt.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys
        .filter(k => k !== CACHE_NAME)
        .map(k => caches.delete(k))
      )
    )
  );
});

// Fetch: respond from cache first, then network & cache new
self.addEventListener('fetch', evt => {
  const url = new URL(evt.request.url);

  // only handle same-origin GET requests
  if (evt.request.method !== 'GET' || url.origin !== location.origin) {
    return;
  }

  evt.respondWith(
    caches.match(evt.request).then(cached => {
      if (cached) return cached;
      return fetch(evt.request).then(res => {
        // only cache successful responses
        if (res.ok) {
          const copy = res.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(evt.request, copy));
        }
        return res;
      });
    })
  );
});
