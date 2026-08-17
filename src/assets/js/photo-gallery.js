(function () {
  "use strict";

  var galleryElements = document.querySelectorAll("[data-photo-gallery]");
  if (!galleryElements.length) return;

  var activeItems = [];
  var activeIndex = 0;
  var lastTrigger = null;
  var touchStartX = 0;

  var modal = document.createElement("div");
  modal.className = "photo-lightbox";
  modal.setAttribute("role", "dialog");
  modal.setAttribute("aria-modal", "true");
  modal.setAttribute("aria-label", "Просмотр фотографий");
  modal.setAttribute("aria-hidden", "true");
  modal.innerHTML =
    '<div class="photo-lightbox__top">' +
      '<span class="photo-lightbox__count"></span>' +
      '<button class="photo-lightbox__close" type="button" aria-label="Закрыть">&times;</button>' +
    '</div>' +
    '<div class="photo-lightbox__stage">' +
      '<button class="photo-lightbox__nav photo-lightbox__nav--prev" type="button" aria-label="Предыдущее фото">&#8249;</button>' +
      '<img class="photo-lightbox__image" src="" alt="">' +
      '<button class="photo-lightbox__nav photo-lightbox__nav--next" type="button" aria-label="Следующее фото">&#8250;</button>' +
    '</div>' +
    '<p class="photo-lightbox__caption"></p>';
  document.body.appendChild(modal);

  var image = modal.querySelector(".photo-lightbox__image");
  var caption = modal.querySelector(".photo-lightbox__caption");
  var count = modal.querySelector(".photo-lightbox__count");
  var closeButton = modal.querySelector(".photo-lightbox__close");
  var previousButton = modal.querySelector(".photo-lightbox__nav--prev");
  var nextButton = modal.querySelector(".photo-lightbox__nav--next");

  function render() {
    var item = activeItems[activeIndex];
    image.src = item.src;
    image.alt = item.alt;
    caption.textContent = item.alt;
    count.textContent = (activeIndex + 1) + " / " + activeItems.length;
  }

  function open(items, index, trigger) {
    activeItems = items;
    activeIndex = index;
    lastTrigger = trigger;
    render();
    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");
    document.body.classList.add("photo-lightbox-open");
    closeButton.focus();
  }

  function close() {
    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
    document.body.classList.remove("photo-lightbox-open");
    image.removeAttribute("src");
    if (lastTrigger) lastTrigger.focus();
  }

  function move(direction) {
    activeIndex = (activeIndex + direction + activeItems.length) % activeItems.length;
    render();
  }

  function trapFocus(event) {
    if (event.key !== "Tab") return;
    var controls = [closeButton, previousButton, nextButton];
    var currentIndex = controls.indexOf(document.activeElement);
    var direction = event.shiftKey ? -1 : 1;
    var nextIndex = (currentIndex + direction + controls.length) % controls.length;
    event.preventDefault();
    controls[nextIndex].focus();
  }

  Array.prototype.forEach.call(galleryElements, function (gallery) {
    var triggers = Array.prototype.slice.call(gallery.querySelectorAll("[data-photo-src]"));
    var items = triggers.map(function (trigger) {
      return {
        src: trigger.getAttribute("data-photo-src"),
        alt: trigger.getAttribute("data-photo-alt") || "Фотография Хийденвуори"
      };
    });

    triggers.forEach(function (trigger, index) {
      trigger.addEventListener("click", function () {
        open(items, index, trigger);
      });
    });
  });

  previousButton.addEventListener("click", function () { move(-1); });
  nextButton.addEventListener("click", function () { move(1); });
  closeButton.addEventListener("click", close);

  modal.addEventListener("click", function (event) {
    if (event.target === modal || event.target.classList.contains("photo-lightbox__stage")) close();
  });
  modal.addEventListener("touchstart", function (event) {
    touchStartX = event.changedTouches[0].clientX;
  }, { passive: true });
  modal.addEventListener("touchend", function (event) {
    var delta = event.changedTouches[0].clientX - touchStartX;
    if (Math.abs(delta) > 50) move(delta > 0 ? -1 : 1);
  }, { passive: true });
  modal.addEventListener("keydown", trapFocus);

  document.addEventListener("keydown", function (event) {
    if (!modal.classList.contains("is-open")) return;
    if (event.key === "Escape") close();
    if (event.key === "ArrowLeft") move(-1);
    if (event.key === "ArrowRight") move(1);
  });
})();
