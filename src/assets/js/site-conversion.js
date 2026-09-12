document.addEventListener("DOMContentLoaded", function () {
    function track(eventName, payload) {
        var safePayload = payload || {};

        if (typeof window.ym === "function") {
            try {
                window.ym(103525753, "reachGoal", eventName, safePayload);
            } catch (error) {
                console.warn("ym track failed", error);
            }
        }

        window.dataLayer = window.dataLayer || [];
        window.dataLayer.push(
            Object.assign(
                {
                    event: eventName,
                },
                safePayload
            )
        );
    }

    document.querySelectorAll("a[href]").forEach(function (link) {
        var href = link.getAttribute("href") || "";
        var eventName = null;

        if (href.startsWith("tel:")) {
            eventName = "cta_phone_click";
        } else if (href.includes("wa.me")) {
            eventName = "cta_whatsapp_click";
        } else if (href.includes("t.me")) {
            eventName = "cta_telegram_click";
        }

        if (!eventName) {
            return;
        }

        link.addEventListener("click", function () {
            track(eventName, {
                href: href,
                page_path: window.location.pathname,
            });
        });
    });

    document.addEventListener("hiidenvuori:form-success", function (event) {
        track("lead_form_submit_success", {
            form_id: event.detail && event.detail.formId ? event.detail.formId : "",
            page_path: window.location.pathname,
        });
    });

    document.addEventListener("hiidenvuori:form-error", function (event) {
        track("lead_form_submit_error", {
            form_id: event.detail && event.detail.formId ? event.detail.formId : "",
            page_path: window.location.pathname,
        });
    });
});
