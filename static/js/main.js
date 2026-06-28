// =====================================================================
//  main.js — AOS init, curseur personnalisé, scroll reveals, skill bars
// =====================================================================
(function () {
  'use strict';

  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function initAOS() {
    if (window.AOS) {
      window.AOS.init({
        duration: 700,
        easing: 'ease-out-cubic',
        once: true,
        offset: 80,
        disable: reduceMotion,
      });
    }
  }

  // ---------------------------------------------------------------
  // Curseur personnalisé (souris uniquement)
  // ---------------------------------------------------------------
  function initCursor() {
    if (!finePointer) return;
    const dot = document.getElementById('cursor-dot');
    const ring = document.getElementById('cursor-ring');
    if (!dot || !ring) return;

    let ringX = 0, ringY = 0, mouseX = 0, mouseY = 0;

    document.addEventListener('mousemove', function (e) {
      mouseX = e.clientX;
      mouseY = e.clientY;
      dot.style.left = mouseX - 5 + 'px';
      dot.style.top = mouseY - 5 + 'px';
    });

    // Mouvement fluide de l'anneau (lerp)
    function loop() {
      ringX += (mouseX - ringX) * 0.18;
      ringY += (mouseY - ringY) * 0.18;
      ring.style.left = ringX - 18 + 'px';
      ring.style.top = ringY - 18 + 'px';
      requestAnimationFrame(loop);
    }
    loop();

    document.querySelectorAll('a, button, input, textarea, select').forEach(function (el) {
      el.addEventListener('mouseenter', function () {
        ring.classList.add('scale-150', 'bg-accent/10');
      });
      el.addEventListener('mouseleave', function () {
        ring.classList.remove('scale-150', 'bg-accent/10');
      });
    });
  }

  // ---------------------------------------------------------------
  // Barres de compétences (page à-propos)
  // ---------------------------------------------------------------
  function initSkillBars() {
    const bars = document.querySelectorAll('.skill-bar');
    if (!bars.length) return;

    const reveal = function (bar) {
      bar.style.width = (bar.dataset.level || 0) + '%';
    };

    if (!('IntersectionObserver' in window)) {
      bars.forEach(reveal);
      return;
    }

    const observer = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          reveal(entry.target);
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    bars.forEach(function (b) { observer.observe(b); });
  }

  // ---------------------------------------------------------------
  // GSAP : léger parallax sur les halos (si dispo, hors reduce-motion)
  // ---------------------------------------------------------------
  function initGsap() {
    if (reduceMotion || !window.gsap || !window.ScrollTrigger) return;
    window.gsap.registerPlugin(window.ScrollTrigger);
    window.gsap.utils.toArray('.animate-float').forEach(function (el) {
      window.gsap.to(el, {
        yPercent: -12,
        ease: 'none',
        scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: true },
      });
    });
  }

  function init() {
    initAOS();
    initCursor();
    initSkillBars();
    initGsap();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
