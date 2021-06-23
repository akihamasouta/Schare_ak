const CACHE_VERSION = 'v1';
const CACHE_NAME = `${registration.scope}!${CACHE_VERSION}`;

// キャッシュするファイルをセットする
const urlsToCache = [
  '../templates/share_calendar/account_memory.html',
  '../templates/share_calendar/account.html',
  '../templates/share_calendar/add_user.html',
  '../templates/share_calendar/balloon.html',
  '../templates/share_calendar/follow.html',
  'templates/share_calendar/follower.html',
  '../../../templates/share_calendar/index_memory.html',
  '../../templates/share_calendar/index.html',
  'templates/share_calendar/login.html',
  'templates/share_calendar/look_pic.html',
  'templates/share_calendar/member_form.html',
  'templates/share_calendar/memory_pic.html',
  'templates/share_calendar/parts_sch_content.html',
  'templates/share_calendar/parts_today_content.html',
  'templates/share_calendar/profile_edit.html',
  'templates/share_calendar/sch_detail.html',
  'templates/share_calendar/schedule_form.html',
  'templates/share_calendar/setting.html',
  'templates/share_calendar/today_form.html',
  'templates/share_calendar/today_image_form.html',
  'templates/share_calendar/today_post.html',
  'templates/share_calendar/top_page.html',
  'static/share_calendar/css/account.css',
  'static/share_calendar/css/add_user.css',
  'static/share_calendar/css/balloon.css',
  'static/share_calendar/css/base_form.css',
  'static/share_calendar/css/follow.css',
  'static/share_calendar/css/form.css',
  'static/share_calendar/css/index_memory.css',
  'static/share_calendar/css/login.css',
  'static/share_calendar/css/look_pic.css',
  'static/share_calendar/css/member_form.css',
  'static/share_calendar/css/memory_pic.css',
  'static/share_calendar/css/not_login.css',
  'static/share_calendar/css/profile_edit.css',
  'static/share_calendar/css/sidebar.css',
  'static/share_calendar/css/style_index.css',
  'static/share_calendar/css/style_schedule_ditail.css',
  'static/share_calendar/css/style_schedule_form.css',
  'static/share_calendar/css/style_today_form.css',
  'static/share_calendar/css/today_post.css',
  'static/share_calendar/js/a_scroll_none.js',
  'static/share_calendar/js/index.js',
  'static/share_calendar/js/mermoy_pic.js',
  'static/share_calendar/js/momory.js',
  'static/share_calendar/js/sch_ditail.js',
  'static/share_calendar/js/scroll_index.js',
  'static/share_calendar/js/scroll.js',
  'static/share_calendar/js/x_scroll.js',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    // キャッシュを開く
    caches.open(CACHE_NAME)
    .then((cache) => {
      // 指定されたファイルをキャッシュに追加する
      return cache.addAll(urlsToCache);
    })
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return cacheNames.filter((cacheName) => {
        // このスコープに所属していて且つCACHE_NAMEではないキャッシュを探す
        return cacheName.startsWith(`${registration.scope}!`) &&
               cacheName !== CACHE_NAME;
      });
    }).then((cachesToDelete) => {
      return Promise.all(cachesToDelete.map((cacheName) => {
        // いらないキャッシュを削除する
        return caches.delete(cacheName);
      }));
    })
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
    .then((response) => {
      // キャッシュ内に該当レスポンスがあれば、それを返す
      if (response) {
        return response;
      }

      // 重要：リクエストを clone する。リクエストは Stream なので
      // 一度しか処理できない。ここではキャッシュ用、fetch 用と2回
      // 必要なので、リクエストは clone しないといけない
      let fetchRequest = event.request.clone();

      return fetch(fetchRequest)
        .then((response) => {
          if (!response || response.status !== 200 || response.type !== 'basic') {
            // キャッシュする必要のないタイプのレスポンスならそのまま返す
            return response;
          }

          // 重要：レスポンスを clone する。レスポンスは Stream で
          // ブラウザ用とキャッシュ用の2回必要。なので clone して
          // 2つの Stream があるようにする
          let responseToCache = response.clone();

          caches.open(CACHE_NAME)
            .then((cache) => {
              cache.put(event.request, responseToCache);
            });

          return response;
        });
    })
  );
});