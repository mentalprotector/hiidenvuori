(function () {
    "use strict";

    var CONTACT_CARD_SELECTOR = [
        '.nh-horizontal-cards__item > .lazyload > a[href^="tel:"]',
        '.nh-horizontal-cards__item > .lazyload > a[href*="wa.me"]',
        '.nh-horizontal-cards__item > .lazyload > a[href*="t.me"]',
    ].join(", ");

    var CONTACT_ICONS = {
        phone: '<svg class="contact-card-icon__svg" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M6.62 10.79a15.05 15.05 0 0 0 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1C10.61 21 3 13.39 3 4c0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.24.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>',
        whatsapp: '<svg class="contact-card-icon__svg contact-card-icon__svg--whatsapp" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.33 4.95L2 22l5.28-1.38c1.45.79 3.08 1.21 4.76 1.21 5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2zm0 18.1c-1.5 0-2.96-.4-4.23-1.16l-.3-.18-3.13.82.84-3.05-.2-.31a8.14 8.14 0 0 1-1.25-4.31c0-4.56 3.71-8.27 8.27-8.27s8.27 3.71 8.27 8.27-3.71 8.19-8.27 8.19zm4.54-6.18c-.25-.12-1.47-.73-1.7-.81-.23-.08-.39-.12-.56.12-.17.25-.64.81-.79.98-.15.17-.29.19-.54.06-.25-.12-1.05-.39-2-1.23-.74-.66-1.24-1.47-1.38-1.72-.14-.25-.02-.38.11-.51.11-.11.25-.29.37-.44.12-.15.17-.25.25-.42.08-.17.04-.31-.02-.44-.06-.12-.56-1.35-.77-1.85-.2-.49-.41-.42-.56-.43h-.48c-.17 0-.44.06-.67.31-.23.25-.87.85-.87 2.07s.89 2.4 1.02 2.56c.12.17 1.75 2.67 4.24 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.68-1.18.21-.58.21-1.08.15-1.18-.06-.1-.23-.16-.48-.28z"/></svg>',
        telegram: '<svg class="contact-card-icon__svg" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M22.94 4.68 19.62 20.34c-.25 1.1-.9 1.38-1.83.86l-5.06-3.73-2.44 2.35c-.27.27-.5.5-1.02.5l.36-5.16 9.38-8.47c.4-.36-.1-.57-.64-.2l-11.59 7.3-4.99-1.57c-1.08-.34-1.1-1.08.23-1.6L21.54 3.1c.9-.34 1.7.2 1.4 1.58z"/></svg>',
    };

    function getContactType(href) {
        if (href.indexOf("wa.me") !== -1) return "whatsapp";
        if (href.indexOf("t.me") !== -1) return "telegram";
        return "phone";
    }

    function enhanceContactCards() {
        document.querySelectorAll(CONTACT_CARD_SELECTOR).forEach(function (link) {
            var iconBox = link.querySelector(".nh-horizontal-cards__picture-container");
            if (!iconBox || iconBox.dataset.contactIconApplied === "true") return;

            var iconType = getContactType(link.getAttribute("href") || "");
            iconBox.dataset.contactIconApplied = "true";
            iconBox.classList.add("contact-card-icon", "contact-card-icon--" + iconType);
            iconBox.insertAdjacentHTML("beforeend", CONTACT_ICONS[iconType]);
        });
    }

    function normalizePath(pathname) {
        if (pathname === "/" || pathname === "/index.html") return "/";
        return pathname.replace(/\.html$/, "").replace(/\/$/, "");
    }

    function markCurrentNavigation() {
        var currentPath = normalizePath(window.location.pathname);

        document.querySelectorAll(".nh-topbar-links .nh-topbar-link").forEach(function (link) {
            var href = link.getAttribute("href") || "";
            if (/^(?:https?:|tel:)/.test(href)) return;

            var targetPath = new URL(href, window.location.origin).pathname;
            link.classList.toggle("nh-topbar-link--active", normalizePath(targetPath) === currentPath);
        });
    }

    function updateCopyrightYear() {
        var currentYear = String(new Date().getFullYear());
        document.querySelectorAll("#footertext1, .nh-footer-columns__link").forEach(function (node) {
            node.textContent = node.textContent.replace(/\b2025\b/g, currentYear);
        });
    }

    function initializeMapFallbacks() {
        document.querySelectorAll(".js-map-embed, .home-location__map, .contacts-map").forEach(function (mapEmbed) {
            var iframe = mapEmbed.querySelector(".js-map-embed-frame, iframe");
            var fallback = mapEmbed.querySelector(".map-embed__fallback, .home-location__fallback, .contacts-map__fallback");
            if (!iframe) return;

            mapEmbed.classList.add("map-embed");
            iframe.classList.add("map-embed__frame");
            if (fallback) {
                fallback.classList.add("map-embed__fallback");
                fallback.setAttribute("aria-hidden", "false");
            }

            mapEmbed.classList.add("map-embed--pending");
            iframe.addEventListener("load", function () {
                // Chromium can fire load before replacing a failed frame with
                // its chrome-error page. Wait for several stable checks before
                // hiding the fallback, so a failed embed keeps the picture.
                function showFallback() {
                    mapEmbed.classList.remove("map-embed--loaded");
                    mapEmbed.classList.add("map-embed--pending");
                    if (fallback) fallback.setAttribute("aria-hidden", "false");
                }

                function monitorFrame(checksLeft) {
                    if (!iframe.contentWindow) {
                        showFallback();
                        return;
                    }
                    if (checksLeft <= 0) return;
                    window.setTimeout(function () {
                        monitorFrame(checksLeft - 1);
                    }, 1000);
                }

                function confirmFrame() {
                    if (!iframe.contentWindow) {
                        showFallback();
                        return;
                    }

                    mapEmbed.classList.remove("map-embed--pending");
                    mapEmbed.classList.add("map-embed--loaded");
                    if (fallback) fallback.setAttribute("aria-hidden", "true");
                    monitorFrame(10);
                }

                var checksLeft = 5;
                function waitForStableFrame() {
                    if (!iframe.contentWindow) return;
                    if (checksLeft <= 0) {
                        confirmFrame();
                        return;
                    }

                    checksLeft -= 1;
                    window.setTimeout(waitForStableFrame, 500);
                }

                waitForStableFrame();
            }, { once: true });
        });
    }

    function initializeCopyButtons() {
        function fallbackCopy(text) {
            var textarea = document.createElement("textarea");
            textarea.value = text;
            textarea.setAttribute("readonly", "");
            textarea.style.position = "fixed";
            textarea.style.opacity = "0";
            document.body.appendChild(textarea);
            textarea.select();

            var copied = false;
            try {
                copied = document.execCommand("copy");
            } catch (error) {
                copied = false;
            }

            document.body.removeChild(textarea);
            return copied;
        }

        document.querySelectorAll("[data-copy-text]").forEach(function (button) {
            if (button.dataset.copyButtonApplied === "true") return;

            button.dataset.copyButtonApplied = "true";
            button.addEventListener("click", function () {
                var text = button.getAttribute("data-copy-text");
                if (!text) return;

                var copyResult = window.isSecureContext && navigator.clipboard
                    ? navigator.clipboard.writeText(text).then(function () { return true; }).catch(function () { return false; })
                    : Promise.resolve(fallbackCopy(text));

                copyResult.then(function (copied) {
                    var originalText = button.textContent;
                    button.textContent = copied ? "Скопировано" : "Скопируйте вручную";
                    window.setTimeout(function () {
                        button.textContent = originalText;
                    }, copied ? 1600 : 2200);
                });
            });
        });
    }

    function initializeContactModal() {
        var modal = document.getElementById("site-contact-modal");
        var openers = document.querySelectorAll("[data-contact-modal-open]");
        if (!modal || !openers.length) return;

        var lastTrigger = null;
        var dialog = modal.querySelector('[role="dialog"]');

        function getFocusableElements() {
            if (!dialog) return [];

            return Array.prototype.slice.call(dialog.querySelectorAll(
                'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])'
            )).filter(function (element) {
                return !element.hidden && element.offsetParent !== null;
            });
        }

        function closeModal() {
            modal.classList.remove("is-open");
            modal.setAttribute("aria-hidden", "true");
            document.body.classList.remove("site-contact-modal-open");
            if (lastTrigger) lastTrigger.focus();
        }

        function openModal(event) {
            lastTrigger = event.currentTarget;
            modal.classList.add("is-open");
            modal.setAttribute("aria-hidden", "false");
            document.body.classList.add("site-contact-modal-open");

            var firstAction = getFocusableElements()[0] || modal.querySelector(".site-contact-modal__action");
            if (firstAction) firstAction.focus();
        }

        function trapFocus(event) {
            if (!dialog || !modal.classList.contains("is-open") || event.key !== "Tab") return;

            var focusable = getFocusableElements();
            if (!focusable.length) return;

            var first = focusable[0];
            var last = focusable[focusable.length - 1];
            if (event.shiftKey && document.activeElement === first) {
                event.preventDefault();
                last.focus();
            } else if (!event.shiftKey && document.activeElement === last) {
                event.preventDefault();
                first.focus();
            }
        }

        openers.forEach(function (button) { button.addEventListener("click", openModal); });
        modal.querySelectorAll("[data-contact-modal-close]").forEach(function (button) {
            button.addEventListener("click", closeModal);
        });
        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape" && modal.classList.contains("is-open")) closeModal();
        });
        document.addEventListener("keydown", trapFocus);
    }

    function initializeFooterAccordions() {
        document.querySelectorAll(".nh-footer-columns__title-container").forEach(function (titleContainer) {
            var section = titleContainer.closest(".nh-footer-columns__section");
            if (!section || titleContainer.dataset.footerAccordionApplied === "true") return;

            titleContainer.dataset.footerAccordionApplied = "true";
            titleContainer.setAttribute("role", "button");
            titleContainer.setAttribute("tabindex", "0");
            titleContainer.setAttribute("aria-expanded", "false");

            function toggleSection() {
                if (window.matchMedia("(min-width: 64rem)").matches) return;

                var isOpened = section.classList.toggle("nh-footer-columns__section--opened");
                titleContainer.setAttribute("aria-expanded", String(isOpened));
            }

            titleContainer.addEventListener("click", toggleSection);
            titleContainer.addEventListener("keydown", function (event) {
                if (event.key !== "Enter" && event.key !== " ") return;

                event.preventDefault();
                toggleSection();
            });
        });
    }

    function initializeSiteShell() {
        enhanceContactCards();
        markCurrentNavigation();
        updateCopyrightYear();
        initializeMapFallbacks();
        initializeCopyButtons();
        initializeContactModal();
        initializeFooterAccordions();
    }

    document.addEventListener("DOMContentLoaded", initializeSiteShell);
})();
