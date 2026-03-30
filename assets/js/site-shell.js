document.addEventListener("DOMContentLoaded", function () {
    var currentPath = window.location.pathname.split("/").pop() || "index.html";
    var normalizedCurrent = currentPath === "" ? "index.html" : currentPath;

    document
        .querySelectorAll(".nh-topbar-links .nh-topbar-link, .nh-burger-menu__links-list .nh-burger-menu__link")
        .forEach(function (link) {
            var href = link.getAttribute("href");

            if (!href || href.startsWith("http") || href.startsWith("tel:")) {
                return;
            }

            var normalizedHref = href.replace(/^\.\//, "");
            var isCurrent = normalizedHref === normalizedCurrent;

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
});
