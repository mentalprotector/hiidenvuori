(function () {
  "use strict";

  function initializeEditorialMotion() {
    var page = document.querySelector("body.site_main-page");
    if (!page) return;

    var revealTargets = page.querySelectorAll(
      ".home-highlight, .home-services-heading__inner, #horizontal-cards-home .nh-horizontal-cards__item, .home-history__card, .photo-gallery__head, .photo-gallery__grid, .home-consultation__content, .home-consultation__contacts, .nh-qa-header, .nh-qa-columns, .editorial-footer-lead, .inner-editorial-hero__wrap, .stay-option, .razmeshhenie-extra__head, .razmeshhenie-extra__card, .razmeshhenie-price__inner, .razmeshhenie-included__inner, .razmeshhenie-rules__inner, .nh-cards, .contacts-hero__content, .contacts-hero__panel, .contacts-map-section, .contacts-card, .contacts-route"
    );
    var patterns = page.querySelectorAll(".editorial-pattern");
    var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if ("IntersectionObserver" in window) {
      var observer = new IntersectionObserver(function (entries, currentObserver) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("editorial-visible");
          currentObserver.unobserve(entry.target);
        });
      }, { rootMargin: "0px 0px -10% 0px", threshold: 0.08 });

      revealTargets.forEach(function (element, index) {
        element.classList.add("editorial-reveal");
        element.style.transitionDelay = Math.min(index % 4, 3) * 70 + "ms";
        observer.observe(element);
      });

      function revealScrolledPast() {
        revealTargets.forEach(function (element) {
          if (element.getBoundingClientRect().top < window.innerHeight * 1.08) {
            element.classList.add("editorial-visible");
          }
        });
      }

      revealScrolledPast();
      window.addEventListener("scroll", revealScrolledPast, { passive: true });
    }

    if (!reducedMotion && "IntersectionObserver" in window) {
      var patternObserver = new IntersectionObserver(function (entries, currentObserver) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("editorial-pattern--visible");
          currentObserver.unobserve(entry.target);
        });
      }, { rootMargin: "0px 0px -8% 0px", threshold: 0.02 });

      patterns.forEach(function (pattern) {
        pattern.classList.add("editorial-pattern--motion-ready");
        patternObserver.observe(pattern);
      });
    }

    var hero = page.querySelector("#carousel-fullscreen-16 .nh-carousel-fullscreen__relative");
    var innerHero = page.querySelector(".inner-editorial-hero__media");
    if ((!hero && !innerHero && !patterns.length) || reducedMotion) return;

    var ticking = false;
    function updateHeroPosition() {
      var amount = Math.min(window.scrollY * 0.12, 42);
      if (hero) hero.style.setProperty("--hv-hero-shift", amount + "px");
      if (innerHero) innerHero.style.setProperty("--hv-inner-hero-shift", amount * 0.55 + "px");
      patterns.forEach(function (pattern) {
        var rect = pattern.getBoundingClientRect();
        var patternShift = Math.max(-32, Math.min(32, (window.innerHeight * 0.5 - rect.top) * 0.045));
        pattern.style.setProperty("--hv-pattern-shift", patternShift + "px");
      });
      ticking = false;
    }

    window.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(updateHeroPosition);
    }, { passive: true });

    updateHeroPosition();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeEditorialMotion);
  } else {
    initializeEditorialMotion();
  }
})();
