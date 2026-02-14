document.addEventListener("DOMContentLoaded", function() {
    // Настройки
    const TARGET_EMAIL = "mail@hiidenvuori.ru"; 
    const ENDPOINT = "https://formsubmit.co/ajax/" + TARGET_EMAIL;

    // Находим все формы, кроме поиска (если есть)
    const forms = document.querySelectorAll("form");

    forms.forEach(form => {
        // Пропускаем формы, которые не похожи на заявки (например, поиск)
        if (!form.querySelector("input")) return;

        form.addEventListener("submit", function(e) {
            e.preventDefault();

            const submitBtn = form.querySelector("button[type='submit']") || form.querySelector("input[type='submit']");
            let originalBtnText = "";
            
            if (submitBtn) {
                originalBtnText = submitBtn.innerText || submitBtn.value;
                submitBtn.innerText = "Отправка...";
                submitBtn.value = "Отправка...";
                submitBtn.disabled = true;
                submitBtn.style.opacity = "0.7";
            }

            const formData = new FormData(form);
            
            // Добавляем настройки для FormSubmit (JSON ответ)
            // _captcha=false (отключаем капчу для скорости)
            formData.append("_captcha", "false");
            formData.append("_subject", "Новая заявка с сайта Хийденвуори");

            fetch(ENDPOINT, {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success === "true" || data.success === true) {
                    // Успех! Заменяем содержимое формы на красивое сообщение
                    const successMessage = document.createElement("div");
                    successMessage.style.textAlign = "center";
                    successMessage.style.padding = "20px";
                    successMessage.style.color = "#27ae60";
                    successMessage.style.animation = "fadeIn 0.5s";
                    successMessage.innerHTML = `
                        <div style="font-size: 40px; margin-bottom: 10px;">✅</div>
                        <h3 style="margin: 0; color: inherit;">Заявка отправлена!</h3>
                        <p style="color: #555; margin-top: 10px;">Администратор свяжется с вами в ближайшее время.</p>
                    `;
                    
                    // Плавно скрываем форму и показываем сообщение
                    form.style.display = "none";
                    form.parentNode.insertBefore(successMessage, form);
                } else {
                    alert("Ошибка отправки. Пожалуйста, позвоните нам: +7 (921) 014-11-90");
                    resetBtn();
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("Ошибка соединения. Пожалуйста, позвоните нам: +7 (921) 014-11-90");
                resetBtn();
            });

            function resetBtn() {
                if (submitBtn) {
                    submitBtn.innerText = originalBtnText;
                    submitBtn.value = originalBtnText;
                    submitBtn.disabled = false;
                    submitBtn.style.opacity = "1";
                }
            }
        });
    });

    // Добавим стиль для анимации
    const style = document.createElement('style');
    style.innerHTML = `
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    `;
    document.head.appendChild(style);
});
