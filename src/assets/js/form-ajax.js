document.addEventListener("DOMContentLoaded", function () {
    var endpoint = "https://formsubmit.co/ajax/mail@hiidenvuori.ru";

    document.querySelectorAll("form.js-conversion-form").forEach(function (form) {
        var submitButton = form.querySelector("button[type='submit'], input[type='submit']");
        var originalText = submitButton ? submitButton.textContent || submitButton.value : "";
        var status = document.createElement("div");

        status.className = "form-submit-status";
        status.setAttribute("role", "status");
        status.setAttribute("aria-live", "polite");
        status.hidden = true;
        form.insertAdjacentElement("afterend", status);

        function setButtonPending(isPending) {
            if (!submitButton) return;
            submitButton.disabled = isPending;
            submitButton.style.opacity = isPending ? "0.7" : "1";
            if (submitButton.tagName === "INPUT") {
                submitButton.value = isPending ? "Отправка..." : originalText;
            } else {
                submitButton.textContent = isPending ? "Отправка..." : originalText;
            }
        }

        form.addEventListener("submit", function (event) {
            event.preventDefault();

            if (form.dataset.submitting === "true") return;
            if (!form.checkValidity()) {
                form.reportValidity();
                return;
            }

            form.dataset.submitting = "true";
            status.hidden = true;
            status.textContent = "";
            setButtonPending(true);

            var formData = new FormData(form);
            formData.set("_captcha", "false");
            formData.set("_subject", "Новая заявка с сайта Хийденвуори");

            fetch(endpoint, {
                method: "POST",
                body: formData,
                headers: { Accept: "application/json" }
            })
                .then(function (response) {
                    if (!response.ok) throw new Error("FormSubmit returned " + response.status);
                    return response.json();
                })
                .then(function (data) {
                    if (data.success !== true && data.success !== "true") {
                        throw new Error("FormSubmit rejected the request");
                    }

                    document.dispatchEvent(new CustomEvent("hiidenvuori:form-success", {
                        detail: { formId: form.id || form.dataset.target || "" }
                    }));
                    form.hidden = true;
                    status.className = "form-submit-status form-submit-status--success";
                    status.innerHTML = "<h3>Заявка отправлена!</h3><p>Администратор свяжется с вами в ближайшее время.</p>";
                    status.hidden = false;
                })
                .catch(function (error) {
                    console.error("Form submission failed:", error);
                    document.dispatchEvent(new CustomEvent("hiidenvuori:form-error", {
                        detail: { formId: form.id || form.dataset.target || "" }
                    }));
                    status.className = "form-submit-status form-submit-status--error";
                    status.innerHTML = "<p>Не удалось отправить заявку. Позвоните <a href='tel:+79210141190'>+7 (921) 014-11-90</a> или напишите в <a href='https://wa.me/79210141190'>WhatsApp</a> / <a href='https://t.me/+79210141190'>Telegram</a>.</p>";
                    status.hidden = false;
                })
                .finally(function () {
                    form.dataset.submitting = "false";
                    if (!form.hidden) setButtonPending(false);
                });
        });
    });
});
