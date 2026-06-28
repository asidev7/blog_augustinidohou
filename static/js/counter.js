// Compteurs de statistiques animés — déclenchés au scroll via IntersectionObserver
(function () {
  'use strict';

  function animateCounter(el) {
    const target = parseInt(el.dataset.target, 10) || 0;
    const duration = 1600;
    const start = performance.now();

    function tick(now) {
      const progress = Math.min((now - start) / duration, 1);
      // easeOutExpo
      const eased = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
      el.textContent = Math.round(eased * target).toLocaleString('fr-FR');
      if (progress < 1) requestAnimationFrame(tick);
      else el.textContent = target.toLocaleString('fr-FR');
    }
    requestAnimationFrame(tick);
  }

  function init() {
    const counters = document.querySelectorAll('.counter');
    if (!counters.length) return;

    if (!('IntersectionObserver' in window)) {
      counters.forEach(animateCounter);
      return;
    }

    const observer = new IntersectionObserver(
      function (entries, obs) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            animateCounter(entry.target);
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.4 }
    );

    counters.forEach(function (c) {
      observer.observe(c);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
