// i18n.js — site-wide language manager for museum-as-code.
//
// One language preference is stored in localStorage and applied to every page
// via body[data-lang]. Static text-swap nodes (data-lang-en + data-lang-ko)
// have their textContent swapped on every change. Visibility-based nodes
// ([data-lang="ko"] / [data-lang="en"]) are toggled via CSS rules that already
// live in docs/style.css. Dynamic renderers (app.js, hero.js) listen for the
// 'languagechange' CustomEvent and re-render their grids on the next frame.
//
// Public API: window.MuseumI18n
//   .lang             -> 'en' | 'ko'
//   .set(next)        -> set language ('en' | 'ko')
//   .toggle()         -> swap to the other language
//   .apply()          -> force a re-apply (e.g., after dynamic DOM injection)

(function () {
  'use strict';

  var STORAGE_KEY = 'museumLang';
  var DEFAULT = 'en';
  var lang = (function () {
    try {
      var v = localStorage.getItem(STORAGE_KEY);
      return v === 'ko' || v === 'en' ? v : DEFAULT;
    } catch (e) {
      return DEFAULT;
    }
  })();

  function applyStaticTextSwap(root) {
    var scope = root || document;
    var nodes = scope.querySelectorAll('[data-lang-en][data-lang-ko]');
    Array.prototype.forEach.call(nodes, function (el) {
      var ko = el.getAttribute('data-lang-ko');
      var en = el.getAttribute('data-lang-en');
      // Swap textContent only — preserves child nodes that intentionally have
      // their own data-lang-* attrs (rare; nested swaps are handled by the
      // querySelectorAll call covering them too).
      if (lang === 'ko' && ko != null) el.textContent = ko;
      else if (en != null) el.textContent = en;
    });
  }

  function applyToggleLabel() {
    var btn = document.getElementById('lang-toggle');
    if (!btn) return;
    // Show the OTHER language as the affordance ("press here to switch to that").
    btn.textContent = lang === 'ko' ? '한 / EN' : 'EN / 한';
    btn.setAttribute('aria-pressed', lang === 'ko' ? 'true' : 'false');
    btn.setAttribute(
      'aria-label',
      lang === 'ko' ? 'Switch to English' : '한국어로 전환'
    );
  }

  function apply() {
    document.body.dataset.lang = lang;
    document.documentElement.lang = lang === 'ko' ? 'ko' : 'en';
    applyStaticTextSwap();
    applyToggleLabel();
    document.dispatchEvent(
      new CustomEvent('languagechange', { detail: { lang: lang } })
    );
  }

  function set(next) {
    if (next !== 'ko' && next !== 'en') return;
    if (next === lang) {
      apply();
      return;
    }
    lang = next;
    try {
      localStorage.setItem(STORAGE_KEY, lang);
    } catch (e) {
      // localStorage can throw in private mode / quota exceeded — non-fatal.
    }
    apply();
  }

  function toggle() {
    set(lang === 'ko' ? 'en' : 'ko');
  }

  Object.defineProperty(window, 'MuseumI18n', {
    value: {
      get lang() {
        return lang;
      },
      set: set,
      toggle: toggle,
      apply: apply
    },
    writable: false,
    configurable: false
  });

  function init() {
    apply();
    var btn = document.getElementById('lang-toggle');
    if (btn && !btn.dataset.i18nWired) {
      btn.addEventListener('click', toggle);
      btn.dataset.i18nWired = 'true';
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
