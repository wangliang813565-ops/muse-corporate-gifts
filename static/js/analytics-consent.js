/* Basic consent: no Google request until an explicit opt-in. */
(function () {
  'use strict';
  var panel = document.getElementById('analytics-notice');
  if (!panel || location.hostname !== 'gifts.aimuse.ae') return;
  var id = panel.dataset.measurementId;
  if (!/^G-[A-Z0-9]+$/.test(id)) return;
  var key = 'muse-gifts-analytics-consent-v1';
  var duration = 180 * 24 * 60 * 60 * 1000;
  var loaded = false;
  var settings = document.querySelector('[data-analytics-settings]');
  function readChoice() {
    try {
      var item = JSON.parse(localStorage.getItem(key));
      return item && Date.now() - item.at < duration && ['granted', 'denied'].includes(item.value) ? item.value : null;
    } catch (_) { return null; }
  }
  function clearAnalyticsCookies() {
    document.cookie.split(';').forEach(function (part) {
      var name = part.trim().split('=')[0];
      if (name !== '_ga' && name.indexOf('_ga_') !== 0) return;
      document.cookie = name + '=; Max-Age=0; Path=/; SameSite=Lax; Secure';
      document.cookie = name + '=; Max-Age=0; Path=/; Domain=gifts.aimuse.ae; SameSite=Lax; Secure';
    });
  }
  function start() {
    if (loaded) return;
    loaded = true;
    window['ga-disable-' + id] = false;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('consent', 'default', {analytics_storage:'denied', ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied'});
    window.gtag('consent', 'update', {analytics_storage:'granted'});
    window.gtag('js', new Date());
    var referrer = '';
    try { referrer = document.referrer ? new URL(document.referrer).origin + '/' : ''; } catch (_) {}
    window.gtag('config', id, {
      page_location: location.origin + location.pathname,
      page_referrer: referrer,
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
      cookie_domain: 'gifts.aimuse.ae',
      cookie_expires: 15552000,
      cookie_update: false
    });
    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(id);
    document.head.appendChild(script);
  }
  function choose(value) {
    try { localStorage.setItem(key, JSON.stringify({value:value, at:Date.now()})); } catch (_) {}
    panel.hidden = true;
    if (value === 'granted') { start(); }
    else {
      window['ga-disable-' + id] = true;
      clearAnalyticsCookies();
      // A reload also stops already-loaded analytics listeners and timers.
      if (loaded) { location.reload(); return; }
    }
    if (settings) settings.focus();
  }
  // Delegation also covers the reviewed brief after its link is populated.
  // Never collect the outbound URL: its query can contain a private brief.
  function whatsappClick(event) {
    if (!loaded || window['ga-disable-' + id] || event.defaultPrevented) return;
    if (event.type === 'auxclick' ? event.button !== 1 : event.button !== 0) return;
    var link = event.target.closest && event.target.closest('a[href]');
    if (!link) return;
    var target;
    try { target = new URL(link.href); } catch (_) { return; }
    if (target.protocol !== 'https:' || target.hostname !== 'wa.me' || target.pathname !== '/971525682660') return;
    var placement = link.matches('[data-send-link]') ? 'reviewed_brief' :
      link.matches('.vg-whatsapp-float') ? 'floating' :
      link.matches('.gk-chat') ? 'guide_article' :
      link.closest('.cg-contact') ? 'home_contact' :
      link.closest('footer') ? 'footer' : 'other';
    try {
      window.gtag('event', 'whatsapp_click', {
        send_to: id,
        cta_placement: placement,
        page_location: location.origin + location.pathname
      });
    } catch (_) { /* Analytics must never interrupt the consultation link. */ }
  }
  document.addEventListener('click', whatsappClick);
  document.addEventListener('auxclick', whatsappClick);
  panel.querySelectorAll('[data-analytics-choice]').forEach(function (button) {
    button.addEventListener('click', function () { choose(button.dataset.analyticsChoice); });
  });
  if (settings) {
    settings.hidden = false;
    settings.addEventListener('click', function () {
      panel.hidden = false;
      panel.querySelector('[data-analytics-choice]').focus();
    });
  }
  window.addEventListener('storage', function (event) {
    if (event.key === key && readChoice() !== 'granted' && loaded) {
      window['ga-disable-' + id] = true;
      clearAnalyticsCookies();
      location.reload();
    }
  });
  var choice = readChoice();
  if (choice === 'granted') start();
  else {
    window['ga-disable-' + id] = true;
    clearAnalyticsCookies();
    panel.hidden = choice === 'denied';
  }
}());
