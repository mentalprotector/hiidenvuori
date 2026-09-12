# Hiidenvuori: рабочая памятка

## Проект

- Статический сайт на Eleventy. Исходники: `src/`.
- Сборка: `npm.cmd run build` (результат в `_site/`).
- Проверка: `npm.cmd run verify`.
- В PowerShell используйте `npm.cmd`, а не `npm`: выполнение `npm.ps1` отключено политикой системы.

## Staging-сервер

- Публичный адрес: `https://hiidenvuori.94.140.224.220.sslip.io/`.
- SSH: `matveyrl-1@192.168.28.90`.
- Каталог staging-сайта на сервере: `/home/matveyrl-1/hiidenvuori`.
- Контейнер: `hiidenvuori_site`; он собирается из Dockerfile в этом каталоге.
- Caddy (`global-proxy`) направляет staging-домен на `hiidenvuori_site:80`.

### Выкладка на staging

1. Соберите и проверьте сайт локально.
2. Перед заменой файлов сделайте резервную копию каталога `/home/matveyrl-1/hiidenvuori` с датой в имени.
3. Скопируйте содержимое локального `_site/` в `/home/matveyrl-1/hiidenvuori/` по SSH.
4. На сервере выполните:

   ```sh
   cd /home/matveyrl-1/hiidenvuori
   docker compose up -d --build
   ```

5. Убедитесь, что `hiidenvuori_site` запущен, и проверьте staging-домен.

Не используйте потоковую передачу `tar` из Windows PowerShell: в этой среде она уже приводила к ошибке распаковки. Для выкладки подходит `scp -r .\\_site\\* matveyrl-1@192.168.28.90:/home/matveyrl-1/hiidenvuori/`.

## Production

- Production публикуется отдельно через GitHub Pages: push в `main` или `master` запускает `.github/workflows/deploy-pages.yml`.
- Не путайте это с staging-деплоем по SSH и не публикуйте на production без явного запроса пользователя.
