(function () {
  'use strict';

  /* ── Apply Marathi ── */
  function applyMarathi() {
    document.querySelectorAll('[data-mr]').forEach(function (el) {
      if (!el.dataset.en) {
        el.dataset.en = el.textContent.trim();
      }
      el.textContent = el.dataset.mr;
    });

    // Placeholders
    document.querySelectorAll('[data-mr-ph]').forEach(function (el) {
      if (!el.dataset.enPh) el.dataset.enPh = el.placeholder;
      el.placeholder = el.dataset.mrPh;
    });

    // ✅ FIXED TITLE
    var titleEl = document.getElementById('page-title');
    if (titleEl) {
      titleEl.textContent = "फार्मरेंटल - स्मार्ट शेती उपकरण भाडे";
      document.title = titleEl.textContent;
    }

    document.documentElement.lang = 'mr';
  }

  /* ── Apply English ── */
  function applyEnglish() {
    document.querySelectorAll('[data-mr]').forEach(function (el) {
      if (el.dataset.en) el.textContent = el.dataset.en;
    });

    document.querySelectorAll('[data-mr-ph]').forEach(function (el) {
      if (el.dataset.enPh) el.placeholder = el.dataset.enPh;
    });

    // ✅ FIXED TITLE
    var titleEl = document.getElementById('page-title');
    if (titleEl) {
      titleEl.textContent = "FarmRental - Smart Agricultural Equipment Rental";
      document.title = titleEl.textContent;
    }

    document.documentElement.lang = 'en';
  }

  /* ── Smooth fade ── */
  function withFade(fn) {
    document.body.style.transition = 'opacity 0.15s ease';
    document.body.style.opacity = '0.65';
    setTimeout(function () {
      fn();
      document.body.style.opacity = '1';
      setTimeout(function () {
        document.body.style.transition = '';
      }, 200);
    }, 110);
  }

  /* ── Sync button ── */
  function syncBtn() {
    document.querySelectorAll('#lang-toggle-btn').forEach(function (btn) {
      if (localStorage.getItem('farmrental_lang') === 'mr') {
        btn.innerHTML = '<span style="font-size:1rem;">🇮🇳</span> English';
        btn.title = 'Switch to English';
      } else {
        btn.innerHTML = '<span style="font-size:1rem;">🇮🇳</span> मराठी';
        btn.title = 'मराठीत बदला';
      }
    });
  }

  /* ── Toggle ── */
  window.toggleMarathi = function () {
    var current = localStorage.getItem('farmrental_lang');

    if (current === 'mr') {
      withFade(function () {
        applyEnglish();
        localStorage.setItem('farmrental_lang', 'en');
        syncBtn();
      });
    } else {
      withFade(function () {
        applyMarathi();
        localStorage.setItem('farmrental_lang', 'mr');
        syncBtn();
      });
    }
  };

  /* ── On Load ── */
  document.addEventListener('DOMContentLoaded', function () {
    if (localStorage.getItem('farmrental_lang') === 'mr') {
      applyMarathi();
    }
    syncBtn();
  });

})();