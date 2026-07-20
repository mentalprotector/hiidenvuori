# Публикация через GitHub Pages

Сайт собирается Eleventy из каталога `src` и публикуется только из `_site`.

1. Установить Node.js 20.
2. Выполнить `npm ci`.
3. Выполнить `npm run build` и `npm run verify`.
4. Отправить проверенный коммит в `master` или `main`.
5. Workflow `.github/workflows/deploy-pages.yml` соберёт сайт и передаст `_site` в GitHub Pages.

Файлы `CNAME` и `.nojekyll` копируются в корень сборки. Реальная публикация и изменение DNS выполняются только владельцем репозитория/домена.
