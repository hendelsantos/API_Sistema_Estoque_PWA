// Service Worker para PWA - Versão Mobile Otimizada
const CACHE_NAME = 'gestao-estoque-mobile-v2';
const urlsToCache = [
  '/',
  '/static/manifest.json',
  '/produtos/',
  '/buscar-qr/',
  '/movimentacoes/',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
  'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css',
  'https://unpkg.com/htmx.org@1.9.6/dist/htmx.min.js',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
  'https://unpkg.com/html5-qrcode@2.3.8/html5-qrcode.min.js'
];

// Instalar Service Worker
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Cache aberto');
        return cache.addAll(urlsToCache);
      })
  );
});

// Interceptar requisições
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // Cache hit - retorna resposta do cache
        if (response) {
          return response;
        }

        return fetch(event.request).then(
          function(response) {
            // Verificar se recebemos uma resposta válida
            if(!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // IMPORTANTE: Clona a resposta. Uma resposta é um stream
            // e pode ser consumida apenas uma vez. Precisamos de uma cópia
            // para colocar no cache e outra para retornar ao navegador.
            var responseToCache = response.clone();

            caches.open(CACHE_NAME)
              .then(function(cache) {
                cache.put(event.request, responseToCache);
              });

            return response;
          }
        );
      })
    );
});

// Atualizar Service Worker
self.addEventListener('activate', function(event) {
  var cacheWhitelist = [CACHE_NAME];

  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(cacheName) {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Sincronização em background
self.addEventListener('sync', function(event) {
  if (event.tag == 'background-sync') {
    event.waitUntil(doBackgroundSync());
  }
});

function doBackgroundSync() {
  // Implementar sincronização de dados quando voltar online
  return Promise.resolve();
}

// Notificações push (para futuras implementações)
self.addEventListener('push', function(event) {
  const options = {
    body: event.data ? event.data.text() : 'Notificação do Gestão de Estoque',
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/icon-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore', 
        title: 'Abrir App',
        icon: '/static/icons/icon-72x72.png'
      },
      {
        action: 'close', 
        title: 'Fechar',
        icon: '/static/icons/icon-72x72.png'
      },
    ]
  };

  event.waitUntil(
    self.registration.showNotification('Gestão de Estoque', options)
  );
});

// Clique em notificação
self.addEventListener('notificationclick', function(event) {
  event.notification.close();

  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/')
    );
  } else if (event.action === 'close') {
    event.notification.close();
  } else {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});
