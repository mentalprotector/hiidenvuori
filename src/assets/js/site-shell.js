document.addEventListener("DOMContentLoaded", function () {
    var contactIconSvg = {
        phone:
            '<svg class="contact-card-icon__svg contact-card-icon__svg--phone" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
            '<path fill="#fff" d="M6.62 10.79a15.05 15.05 0 0 0 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1C10.61 21 3 13.39 3 4c0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.24.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>' +
            "</svg>",
        whatsapp:
            '<svg class="contact-card-icon__svg contact-card-icon__svg--whatsapp" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
            '<path fill="#fff" d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.33 4.95L2 22l5.28-1.38c1.45.79 3.08 1.21 4.76 1.21 5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2zm0 18.1c-1.5 0-2.96-.4-4.23-1.16l-.3-.18-3.13.82.84-3.05-.2-.31a8.14 8.14 0 0 1-1.25-4.31c0-4.56 3.71-8.27 8.27-8.27s8.27 3.71 8.27 8.27-3.71 8.19-8.27 8.19zm4.54-6.18c-.25-.12-1.47-.73-1.7-.81-.23-.08-.39-.12-.56.12-.17.25-.64.81-.79.98-.15.17-.29.19-.54.06-.25-.12-1.05-.39-2-1.23-.74-.66-1.24-1.47-1.38-1.72-.14-.25-.02-.38.11-.51.11-.11.25-.29.37-.44.12-.15.17-.25.25-.42.08-.17.04-.31-.02-.44-.06-.12-.56-1.35-.77-1.85-.2-.49-.41-.42-.56-.43h-.48c-.17 0-.44.06-.67.31-.23.25-.87.85-.87 2.07s.89 2.4 1.02 2.56c.12.17 1.75 2.67 4.24 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.68-1.18.21-.58.21-1.08.15-1.18-.06-.1-.23-.16-.48-.28z"/>' +
            "</svg>",
        telegram:
            '<svg class="contact-card-icon__svg contact-card-icon__svg--telegram" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
            '<path fill="#fff" d="M22.94 4.68 19.62 20.34c-.25 1.1-.9 1.38-1.83.86l-5.06-3.73-2.44 2.35c-.27.27-.5.5-1.02.5l.36-5.16 9.38-8.47c.4-.36-.1-.57-.64-.2l-11.59 7.3-4.99-1.57c-1.08-.34-1.1-1.08.23-1.6L21.54 3.1c.9-.34 1.7.2 1.4 1.58z"/>' +
            "</svg>",
    };

    if (!document.getElementById("contact-card-icon-styles")) {
        var contactStyle = document.createElement("style");
        contactStyle.id = "contact-card-icon-styles";
        contactStyle.textContent =
            ".contact-card-icon{position:relative!important;z-index:10!important;display:flex!important;align-items:center!important;justify-content:center!important;flex:0 0 44px!important;width:44px!important;height:44px!important;overflow:visible!important;border-radius:0!important;background:transparent!important}" +
            ".contact-card-icon>picture{display:none!important}" +
            ".contact-card-icon__svg{position:relative;z-index:11;display:block;flex:0 0 auto;width:24px;height:24px}" +
            ".contact-card-icon__svg--whatsapp{width:25px;height:25px}" +
            ".contact-card-icon__svg--telegram{width:24px;height:24px}";
        document.head.appendChild(contactStyle);
    }

    document
        .querySelectorAll(
            '.nh-horizontal-cards__item > .lazyload > a[href^="tel:"], .nh-horizontal-cards__item > .lazyload > a[href*="wa.me"], .nh-horizontal-cards__item > .lazyload > a[href*="t.me"]'
        )
        .forEach(function (link) {
            var href = link.getAttribute("href") || "";
            var iconType = href.indexOf("wa.me") !== -1 ? "whatsapp" : href.indexOf("t.me") !== -1 ? "telegram" : "phone";
            var iconBox = link.querySelector(".nh-horizontal-cards__picture-container");

            if (!iconBox || iconBox.getAttribute("data-contact-icon-applied") === "true") {
                return;
            }

            iconBox.setAttribute("data-contact-icon-applied", "true");
            iconBox.classList.add("contact-card-icon", "contact-card-icon--" + iconType);
            iconBox.insertAdjacentHTML("beforeend", contactIconSvg[iconType]);
        });

    if (!document.getElementById("map-embed-fallback-styles")) {
        var style = document.createElement("style");
        style.id = "map-embed-fallback-styles";
        style.textContent =
            ".map-embed{position:relative;min-height:100%;width:100%}" +
            ".map-embed__frame{position:relative;z-index:2;border:0;background-color:#dce4ef;transition:opacity .3s ease}" +
            ".map-embed--pending .map-embed__frame{opacity:0;pointer-events:none}" +
            ".map-embed__fallback{position:absolute;inset:0;z-index:1;display:flex;align-items:flex-end;justify-content:flex-start;padding:1.25rem;overflow:hidden;border-radius:inherit;background:linear-gradient(135deg,rgba(225,232,241,.98),rgba(209,220,235,.96))}" +
            ".map-embed__fallback:before,.map-embed__fallback:after{content:\"\";position:absolute;inset:0}" +
            ".map-embed__fallback:before{background-image:linear-gradient(rgba(51,132,191,.12) 1px,transparent 1px),linear-gradient(90deg,rgba(51,132,191,.12) 1px,transparent 1px);background-size:3rem 3rem;opacity:.9}" +
            ".map-embed__fallback:after{inset:auto auto 28% 16%;width:1.25rem;height:1.25rem;border-radius:999px;background:#3384bf;box-shadow:0 0 0 .5rem rgba(51,132,191,.16),0 0 0 1.1rem rgba(51,132,191,.08)}" +
            ".map-embed__card{position:relative;z-index:2;max-width:22rem;padding:1rem 1.125rem;border-radius:1rem;background:rgba(255,255,255,.92);box-shadow:0 .75rem 2rem rgba(16,39,72,.12);color:#102748}" +
            ".map-embed__title{margin:0 0 .5rem;font-size:1rem;font-weight:700;line-height:1.35}" +
            ".map-embed__text{margin:0;font-size:.9375rem;line-height:1.5;color:rgba(16,39,72,.86)}" +
            ".map-embed__link{display:inline-flex;align-items:center;justify-content:center;margin-top:.875rem;padding:.7rem 1rem;border-radius:999px;background:#3384bf;color:#fff;font-size:.875rem;font-weight:600;line-height:1.2;text-decoration:none;transition:background-color .2s ease}" +
            ".map-embed__link:focus,.map-embed__link:hover{background:#256da3;color:#fff}" +
            ".map-embed--loaded .map-embed__fallback{display:none}" +
            "@media screen and (max-width:47.9375rem){.map-embed__fallback{padding:1rem}.map-embed__card{max-width:100%;padding:.875rem 1rem}.map-embed__title{font-size:.9375rem}.map-embed__text{font-size:.875rem}}";
        document.head.appendChild(style);
    }

    var pathname = window.location.pathname;
    var currentSlug = pathname === "/" ? "/" : pathname.replace(/\/$/, "");

    document
        .querySelectorAll(".nh-topbar-links .nh-topbar-link, .nh-burger-menu__links-list .nh-burger-menu__link")
        .forEach(function (link) {
            var href = link.getAttribute("href");

            if (!href || href.startsWith("http") || href.startsWith("tel:")) {
                return;
            }

            var linkSlug = href.replace(/\/$/, "");
            var isCurrent = linkSlug === currentSlug;

            if (isCurrent && link.classList.contains("nh-topbar-link")) {
                link.classList.add("nh-topbar-link--active");
            }
        });

    var year = new Date().getFullYear().toString();

    document.querySelectorAll("#footertext1, .nh-footer-columns__link").forEach(function (node) {
        if (node.textContent && node.textContent.includes("2025")) {
            node.textContent = node.textContent.replace("2025", year);
        }
    });

    document.querySelectorAll(".js-map-embed").forEach(function (mapEmbed) {
        var iframe = mapEmbed.querySelector(".js-map-embed-frame");

        if (!iframe) {
            return;
        }

        var markLoaded = function () {
            mapEmbed.classList.remove("map-embed--pending");
            mapEmbed.classList.add("map-embed--loaded");
        };

        mapEmbed.classList.add("map-embed--pending");
        iframe.addEventListener("load", markLoaded, { once: true });
    });

    var contactModal = document.getElementById("site-contact-modal");
    var contactModalOpeners = document.querySelectorAll("[data-contact-modal-open]");
    var contactModalClosers = document.querySelectorAll("[data-contact-modal-close]");
    var lastContactModalTrigger = null;

    if (contactModal && contactModalOpeners.length) {
        var closeContactModal = function () {
            contactModal.classList.remove("is-open");
            contactModal.setAttribute("aria-hidden", "true");
            document.body.classList.remove("site-contact-modal-open");

            if (lastContactModalTrigger) {
                lastContactModalTrigger.focus();
            }
        };

        var openContactModal = function (event) {
            lastContactModalTrigger = event.currentTarget;
            contactModal.classList.add("is-open");
            contactModal.setAttribute("aria-hidden", "false");
            document.body.classList.add("site-contact-modal-open");

            var firstAction = contactModal.querySelector(".site-contact-modal__action");
            if (firstAction) {
                firstAction.focus();
            }
        };

        contactModalOpeners.forEach(function (button) {
            button.addEventListener("click", openContactModal);
        });

        contactModalClosers.forEach(function (button) {
            button.addEventListener("click", closeContactModal);
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape" && contactModal.classList.contains("is-open")) {
                closeContactModal();
            }
        });
    }
});
