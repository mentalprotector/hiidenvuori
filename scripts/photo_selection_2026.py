from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps


NEW_ROOT = Path(r"C:\dev\hiidenvuori task\Хийденсельга\Фото")
OLD_ROOT = Path(r"C:\dev\hiidenvuori_updated\src\assets\img")
REVIEW_ROOT = Path(r"C:\dev\hiidenvuori_updated\.photo-review-2026")
OUTPUT_ROOT = OLD_ROOT / "selected-2026"
DOC_PATH = Path(r"C:\dev\hiidenvuori_updated\PHOTO_SELECTION_2026.md")


CATEGORY_INFO = {
    "hero": {
        "title": "Главный экран и общая атмосфера территории",
        "site": "Главный экран главной страницы; широкий фон с безопасной зоной под заголовок",
    },
    "camping": {
        "title": "Кемпинг и палатки",
        "site": "Карточка и страница палаточного кемпинга; галерея размещения",
    },
    "autocamping": {
        "title": "Автокемпинг",
        "site": "Карточка и страница стоянки для автодомов; схема/галерея мест",
    },
    "beach": {
        "title": "Берег и песчаный пляж",
        "site": "Блок пляжа на странице размещения; спокойная широкая галерея",
    },
    "kitchen": {
        "title": "Общая кухня",
        "site": "Блок удобств и общая кухня; обзор пространства и предметные детали",
    },
    "sauna": {
        "title": "Баня",
        "site": "Карточка бани на странице услуг; интерьер и подтверждающие детали",
    },
    "pier": {
        "title": "Причал, слип, катера",
        "site": "Страница спуска для катеров; карточка услуги и галерея причала",
    },
    "cafe": {
        "title": "Кафе/магазин",
        "site": "Карточка и галерея кафе-магазина SAHA; витрина, интерьер и фасад",
    },
    "activity": {
        "title": "Активный отдых",
        "site": "Карточка активного отдыха; вело-, SUP- и водные активности",
    },
    "details": {
        "title": "Детали территории: лес, Ладога, навигация, уют, вечерний свет",
        "site": "Атмосферные разделители, CTA, мобильные карточки и вторичная галерея",
    },
}


SELECTIONS = [
    # category, role, source id, output stem, reason, processing profile
    ("hero", "main", "E031", "hero-main-aerial-ladoga", "Самый выразительный общий план: вода, лесной берег и теплоход; широкий формат и тёмная вода слева дают устойчивую зону под светлый текст, композиция переносит центральный кроп.", "existing_hero"),
    ("hero", "reserve-01", "E020", "hero-reserve-islands-aerial", "Чистый воздушный вид шхер без визуального шума; подходит для широкого CTA и фонового баннера.", "existing_hero"),
    ("hero", "reserve-02", "N230", "hero-reserve-territory-waterfront", "Показывает реальную береговую территорию и причал; низкий горизонт оставляет много спокойного неба под текст.", "new_outdoor"),
    ("hero", "reserve-03", "N241", "hero-reserve-rocky-shore", "Связывает каменистый берег, острова и инфраструктуру; хорошо читается в широком и мобильном центральном кропе.", "new_outdoor"),

    ("camping", "main", "E038", "camping-main-tent-platform", "Сильный существующий кадр: палатка крупно, настил читается сразу, мягкий вечерний свет создаёт уют без постановочной перегрузки.", "none"),
    ("camping", "reserve-01", "E039", "camping-reserve-tent-portrait", "Вертикальная версия того же предложения; особенно полезна для мобильной карточки и сторис-подобного блока.", "none"),
    ("camping", "reserve-02", "E040", "camping-reserve-tents-wide", "Показывает несколько мест и реальный масштаб палаточного поля; хороший горизонтальный контекстный кадр.", "none"),
    ("camping", "reserve-03", "E032", "camping-reserve-tent-front", "Фронтальный, симметричный вид палатки с читаемым входом и мебелью; удобен для карточки 4:3.", "none"),

    ("autocamping", "main", "N187", "autocamping-main-pitches-wide", "Полноразмерный честный обзор нескольких размеченных мест и подключения; лучше старого низкоразрешённого кадра для отдельной страницы.", "new_outdoor"),
    ("autocamping", "reserve-01", "N189", "autocamping-reserve-pitch-waterfront", "Показывает одно место крупнее и его связь с береговой инфраструктурой; удобен для поясняющей карточки.", "new_outdoor"),
    ("autocamping", "reserve-02", "N186", "autocamping-reserve-pitches-context", "Широкий боковой обзор рядов мест и ограждения, полезен для галереи и фактического представления планировки.", "new_outdoor"),
    ("autocamping", "reserve-03", "E013", "autocamping-reserve-existing-pitch", "Сохраняет уже работающий на сайте близкий ракурс места; невысокое разрешение ограничивает роль резервной карточкой.", "none"),

    ("beach", "main", "N173", "beach-main-sandy-shore", "Самый чистый широкий вид песчаной полосы и Ладоги; диагональ берега ведёт взгляд, детали не теряются на мобильном.", "new_outdoor"),
    ("beach", "reserve-01", "N176", "beach-reserve-wide", "Более широкий спокойный план с большим количеством воздуха, подходящий для текстового блока.", "new_outdoor"),
    ("beach", "reserve-02", "N179", "beach-reserve-open-water", "Минималистичный фронтальный вид пляжа и воды; нейтральный фон для короткой подписи.", "new_outdoor"),
    ("beach", "reserve-03", "N171", "beach-reserve-pebbles-sand", "Показывает естественный переход камней в песок и подтверждает фактуру реального берега.", "new_outdoor"),

    ("kitchen", "main", "N083", "kitchen-main-overview", "Наиболее информативный общий вид: столы, мойка, холодильник и рабочая зона читаются в одном кадре; вертикаль сильна на мобильном.", "new_indoor"),
    ("kitchen", "reserve-01", "N092", "kitchen-reserve-tables", "Перспектива вдоль длинных столов объясняет вместимость общей кухни.", "new_indoor"),
    ("kitchen", "reserve-02", "N089", "kitchen-reserve-cookware", "Аккуратная предметная деталь посуды и рабочей поверхности подтверждает оснащение.", "new_indoor"),
    ("kitchen", "reserve-03", "N094", "kitchen-reserve-dish-rack", "Читаемая бытовая деталь без постановочного декора; полезна в галерее удобств.", "new_indoor"),
    ("kitchen", "reserve-04", "E024", "kitchen-reserve-existing-wide", "Старый широкий обзор сохраняет привычный горизонтальный вариант; оставлен без усиления из-за ограниченного исходного разрешения.", "none"),

    ("sauna", "main", "N197", "sauna-main-steam-room", "Лучший кадр категории: сразу узнаваемая парная, ковш и выразительный тёплый рисунок света; предметы крупные и читаются на телефоне.", "new_sauna"),
    ("sauna", "reserve-01", "N198", "sauna-reserve-stove", "Показывает реальную печь и камни, подтверждая содержание услуги.", "new_sauna"),
    ("sauna", "reserve-02", "N200", "sauna-reserve-exterior", "Наружный вид нужен для ориентации, но оставлен резервом из-за технических деталей у входа.", "new_outdoor"),
    ("sauna", "reserve-03", "N196", "sauna-reserve-wood-detail", "Вертикальная деталь свежей деревянной отделки дополняет интерьер и подходит для узкого мобильного кропа.", "new_sauna"),

    ("pier", "main", "E016", "pier-main-boat-launch-sunset", "Сильный старый кадр лучше новых по действию и атмосфере: катер действительно сходит по слипу, вечерний свет остаётся естественным.", "none"),
    ("pier", "reserve-01", "N247", "pier-reserve-dock-front", "Симметричная перспектива настила ведёт к воде и хорошо объясняет устройство причала.", "new_outdoor"),
    ("pier", "reserve-02", "N253", "pier-reserve-slip", "Чистый документальный вид самого слипа без отвлекающих объектов.", "new_outdoor"),
    ("pier", "reserve-03", "N252", "pier-reserve-boat-at-dock", "Катер у настила добавляет масштаб и показывает готовность инфраструктуры к использованию.", "new_outdoor"),
    ("pier", "reserve-04", "N243", "pier-reserve-harbour", "Широкий контекст гавани, каменной дамбы и судна; пригоден для галереи и десктопного баннера.", "new_outdoor"),

    ("cafe", "main", "N045", "cafe-main-local-products", "Сильная предметная линия локальных продуктов и читаемая вывеска «Варенье»; кадр сразу сообщает, что здесь можно купить.", "new_indoor"),
    ("cafe", "reserve-01", "N051", "cafe-reserve-shop-wide", "Более широкий вид торговой стены показывает ассортимент и устройство магазина.", "new_indoor"),
    ("cafe", "reserve-02", "N221", "cafe-reserve-saha-exterior", "Фасад с названием SAHA обеспечивает узнаваемость и помогает посетителю найти вход.", "new_outdoor"),
    ("cafe", "reserve-03", "N224", "cafe-reserve-counter", "Показывает стойку и фактический интерьер, подходит для галереи услуги.", "new_indoor"),
    ("cafe", "reserve-04", "N049", "cafe-reserve-craft-detail", "Тактильная деталь локальных сувениров и деревянной посуды добавляет человеческий масштаб.", "new_indoor"),

    ("activity", "main", "N145", "activity-main-bicycles", "Велосипеды крупно и Ладога в фоне: активность понятна без подписи, вертикаль хорошо работает в карточке на мобильном.", "new_outdoor"),
    ("activity", "reserve-01", "N147", "activity-reserve-sup-stack", "Горизонтальный кадр инвентаря для SUP, пригодный для десктопной карточки.", "new_outdoor"),
    ("activity", "reserve-02", "N149", "activity-reserve-sup-portrait", "Вертикальный вариант SUP-проката с навигационной табличкой, полезный для мобильной галереи.", "new_outdoor"),
    ("activity", "reserve-03", "N131", "activity-reserve-boat-ride", "Живой кадр движения на воде с человеком; добавляет опыт, а не только инвентарь.", "new_outdoor"),
    ("activity", "reserve-04", "E022", "activity-reserve-existing-sup", "Сохраняет существующий узнаваемый кадр пункта SUP-проката; остаётся резервом из-за более жёсткого цвета и меньшего разрешения.", "none"),

    ("details", "main", "E034", "details-main-evening-lights", "Лучший атмосферный старый кадр: тёплые гирлянды, укрытие и вид на воду; даёт уют без потери северного окружения.", "none"),
    ("details", "reserve-01", "N154", "details-reserve-swings-ladoga", "Лаконичная деталь качелей на фоне Ладоги; много свободного пространства и хороший мобильный формат.", "new_outdoor"),
    ("details", "reserve-02", "N240", "details-reserve-rocks-flowers", "Камень, жёлтые цветы и вода собирают природные фактуры территории в одном кадре.", "new_outdoor"),
    ("details", "reserve-03", "N054", "details-reserve-people-water", "Силуэты людей в проёме с Ладогой создают живую, но спокойную атмосферу и естественную рамку.", "new_shadow"),
    ("details", "reserve-04", "N218", "details-reserve-navigation", "Жёлтый указатель «Кемпинг» показывает реальную навигацию и добавляет полезную территориальную деталь.", "new_outdoor"),
]


PROCESSING_NOTES = {
    "none": "Обработка не выполнялась: исходный WebP скопирован без повторного кодирования, чтобы не ухудшать уже удачный файл.",
    "existing_hero": "Мягко снижена избыточная насыщенность синего и зелёного, слегка подняты тени и сдержаны светлые участки; сохранён исходный характер аэрофото.",
    "new_outdoor": "Сдержаны светлые участки неба и воды, немного уменьшена общая насыщенность, зелёные и голубые приведены к нейтрально-холодной северной гамме, тени слегка раскрыты.",
    "new_indoor": "Ослаблен тёплый/оранжевый сдвиг, приподняты тени и защищены яркие окна; дерево оставлено натуральным, металл — нейтральным.",
    "new_sauna": "Умерена чрезмерная оранжевая насыщенность, выровнен баланс между тёплым деревом и нейтральными тенями, сохранён локальный рисунок света.",
    "new_shadow": "Точечно раскрыты глубокие тени без потери силуэтов, приглушён тёплый сдвиг, яркий проём сохранён без агрессивного HDR-эффекта.",
}


def image_files(root: Path, source: str) -> list[Path]:
    extensions = {".jpg", ".jpeg", ".png", ".webp"}
    files = [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in extensions]
    if source == "existing-site-assets":
        files = [
            p
            for p in files
            if "selected-2026" not in p.parts
            and not p.stem.startswith("favicon-")
            and p.name not in {"favicon.webp"}
        ]
    return sorted(files, key=lambda p: str(p).casefold())


def metrics(image: Image.Image) -> dict[str, float]:
    preview = image.copy()
    preview.thumbnail((640, 640), Image.Resampling.LANCZOS)
    rgb = np.asarray(preview.convert("RGB"))
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    return {
        "brightness": round(float(np.mean(gray)) / 255, 4),
        "contrast": round(float(np.std(gray)) / 255, 4),
        "saturation": round(float(np.mean(hsv[:, :, 1])) / 255, 4),
        "sharpness": round(float(cv2.Laplacian(gray, cv2.CV_64F).var()), 2),
    }


def build_inventory() -> list[dict]:
    records: list[dict] = []
    for prefix, source, root in (
        ("N", "new-photo-session", NEW_ROOT),
        ("E", "existing-site-assets", OLD_ROOT),
    ):
        for index, path in enumerate(image_files(root, source), start=1):
            with Image.open(path) as raw:
                image = ImageOps.exif_transpose(raw)
                width, height = image.size
                record = {
                    "id": f"{prefix}{index:03d}",
                    "source": source,
                    "path": str(path),
                    "relative_path": str(path.relative_to(root)),
                    "width": width,
                    "height": height,
                    "orientation": "landscape" if width > height else "portrait" if height > width else "square",
                    "aspect_ratio": round(width / height, 4),
                }
                record.update(metrics(image))
                records.append(record)
    return records


def fit_crop(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return ImageOps.fit(image.convert("RGB"), size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        Path(r"C:\Windows\Fonts\arial.ttf"),
        Path(r"C:\Windows\Fonts\segoeui.ttf"),
        Path(r"C:\Windows\Fonts\calibri.ttf"),
    )
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default(size=size)


def contact_sheets(records: list[dict], per_sheet: int = 35) -> None:
    REVIEW_ROOT.mkdir(parents=True, exist_ok=True)
    font = load_font(18)
    small = load_font(14)
    cell_w, image_h, label_h = 340, 226, 62
    cols = 5
    for source in ("new-photo-session", "existing-site-assets"):
        subset = [r for r in records if r["source"] == source]
        for page, start in enumerate(range(0, len(subset), per_sheet), start=1):
            chunk = subset[start : start + per_sheet]
            rows = math.ceil(len(chunk) / cols)
            sheet = Image.new("RGB", (cols * cell_w, rows * (image_h + label_h)), "#e7e9e8")
            draw = ImageDraw.Draw(sheet)
            for pos, record in enumerate(chunk):
                x = (pos % cols) * cell_w
                y = (pos // cols) * (image_h + label_h)
                with Image.open(record["path"]) as raw:
                    image = ImageOps.exif_transpose(raw)
                    thumb = fit_crop(image, (cell_w, image_h))
                sheet.paste(thumb, (x, y))
                draw.rectangle((x, y + image_h, x + cell_w, y + image_h + label_h), fill="#f8f8f5")
                draw.text((x + 8, y + image_h + 5), record["id"], font=font, fill="#122018")
                rel = record["relative_path"]
                if len(rel) > 43:
                    rel = "..." + rel[-40:]
                draw.text((x + 8, y + image_h + 30), rel, font=small, fill="#435048")
            out = REVIEW_ROOT / f"review-{source}-{page:02d}.jpg"
            sheet.save(out, "JPEG", quality=90, optimize=True)


def write_inventory(records: list[dict]) -> None:
    REVIEW_ROOT.mkdir(parents=True, exist_ok=True)
    with (REVIEW_ROOT / "inventory.json").open("w", encoding="utf-8") as handle:
        json.dump(records, handle, ensure_ascii=False, indent=2)
    with (REVIEW_ROOT / "inventory.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)


def apply_profile(image: Image.Image, profile: str) -> Image.Image:
    if profile == "none":
        return image
    presets = {
        "existing_hero": {"shadow": 0.030, "highlight": 0.025, "contrast": 1.015, "saturation": 0.84, "channels": (0.995, 1.0, 1.01)},
        "new_outdoor": {"shadow": 0.018, "highlight": 0.040, "contrast": 1.020, "saturation": 0.90, "channels": (0.995, 1.0, 1.012)},
        "new_indoor": {"shadow": 0.045, "highlight": 0.045, "contrast": 1.015, "saturation": 0.90, "channels": (0.965, 1.0, 1.035)},
        "new_sauna": {"shadow": 0.030, "highlight": 0.030, "contrast": 1.010, "saturation": 0.84, "channels": (0.950, 1.0, 1.050)},
        "new_shadow": {"shadow": 0.080, "highlight": 0.050, "contrast": 1.010, "saturation": 0.90, "channels": (0.975, 1.0, 1.030)},
    }
    preset = presets[profile]
    rgb = np.asarray(image.convert("RGB"), dtype=np.float32) / 255.0
    lum = 0.2126 * rgb[:, :, 0] + 0.7152 * rgb[:, :, 1] + 0.0722 * rgb[:, :, 2]
    lift = preset["shadow"] * (1.0 - lum) ** 2
    pull = preset["highlight"] * lum**2
    rgb = np.clip(rgb + lift[:, :, None] - pull[:, :, None], 0.0, 1.0)
    rgb = np.clip((rgb - 0.5) * preset["contrast"] + 0.5, 0.0, 1.0)
    gray = np.sum(rgb * np.array([0.2126, 0.7152, 0.0722], dtype=np.float32), axis=2, keepdims=True)
    rgb = gray + (rgb - gray) * preset["saturation"]
    rgb *= np.array(preset["channels"], dtype=np.float32)
    rgb = np.clip(rgb, 0.0, 1.0)
    return Image.fromarray(np.round(rgb * 255).astype(np.uint8), "RGB")


def selection_records(inventory: list[dict]) -> list[dict]:
    by_id = {record["id"]: record for record in inventory}
    selected: list[dict] = []
    for category, role, source_id, stem, reason, profile in SELECTIONS:
        original = by_id[source_id]
        selected.append(
            {
                **original,
                "category": category,
                "role": role,
                "stem": stem,
                "filename": f"{stem}.webp",
                "reason": reason,
                "profile": profile,
                "processed": profile != "none",
            }
        )
    return selected


def export_selected(selected: list[dict]) -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    for record in selected:
        source = Path(record["path"])
        destination = OUTPUT_ROOT / record["filename"]
        if record["profile"] == "none":
            destination.write_bytes(source.read_bytes())
            continue
        with Image.open(source) as raw:
            image = ImageOps.exif_transpose(raw).convert("RGB")
        image = apply_profile(image, record["profile"])
        if max(image.size) > 2400:
            scale = 2400 / max(image.size)
            image = image.resize(
                (round(image.width * scale), round(image.height * scale)),
                Image.Resampling.LANCZOS,
            )
        image.save(destination, "WEBP", quality=88, method=6)


def role_label(role: str) -> str:
    return "основной" if role == "main" else "резерв"


def build_final_contact_sheet(selected: list[dict]) -> None:
    cols = 5
    cell_w, image_h, label_h = 360, 236, 70
    rows = math.ceil(len(selected) / cols)
    sheet = Image.new("RGB", (cols * cell_w, rows * (image_h + label_h)), "#dfe4e1")
    draw = ImageDraw.Draw(sheet)
    font = load_font(16)
    small = load_font(13)
    for index, record in enumerate(selected):
        x = (index % cols) * cell_w
        y = (index // cols) * (image_h + label_h)
        with Image.open(OUTPUT_ROOT / record["filename"]) as raw:
            thumb = fit_crop(ImageOps.exif_transpose(raw), (cell_w, image_h))
        sheet.paste(thumb, (x, y))
        draw.rectangle((x, y + image_h, x + cell_w, y + image_h + label_h), fill="#f7f7f3")
        category = CATEGORY_INFO[record["category"]]["title"]
        draw.text((x + 7, y + image_h + 5), f"{category} · {role_label(record['role'])}", font=font, fill="#17231c")
        draw.text((x + 7, y + image_h + 34), record["filename"], font=small, fill="#4b574f")
    sheet.save(OUTPUT_ROOT / "contact-final-selection.jpg", "JPEG", quality=91, optimize=True)


def build_before_after_contact_sheet(selected: list[dict]) -> None:
    processed = [record for record in selected if record["processed"]]
    cols = 3
    cell_w, image_h, label_h = 620, 210, 54
    rows = math.ceil(len(processed) / cols)
    sheet = Image.new("RGB", (cols * cell_w, rows * (image_h + label_h)), "#dfe4e1")
    draw = ImageDraw.Draw(sheet)
    font = load_font(14)
    small = load_font(12)
    half_w = cell_w // 2
    for index, record in enumerate(processed):
        x = (index % cols) * cell_w
        y = (index // cols) * (image_h + label_h)
        with Image.open(record["path"]) as raw:
            before = fit_crop(ImageOps.exif_transpose(raw), (half_w, image_h))
        with Image.open(OUTPUT_ROOT / record["filename"]) as raw:
            after = fit_crop(ImageOps.exif_transpose(raw), (half_w, image_h))
        sheet.paste(before, (x, y))
        sheet.paste(after, (x + half_w, y))
        draw.rectangle((x, y, x + 72, y + 22), fill="#17231c")
        draw.text((x + 6, y + 3), "ДО", font=small, fill="white")
        draw.rectangle((x + half_w, y, x + half_w + 92, y + 22), fill="#17231c")
        draw.text((x + half_w + 6, y + 3), "ПОСЛЕ", font=small, fill="white")
        draw.rectangle((x, y + image_h, x + cell_w, y + image_h + label_h), fill="#f7f7f3")
        draw.text((x + 7, y + image_h + 5), record["filename"], font=font, fill="#17231c")
        draw.text((x + 7, y + image_h + 29), record["profile"], font=small, fill="#4b574f")
    sheet.save(OUTPUT_ROOT / "contact-before-after.jpg", "JPEG", quality=91, optimize=True)


def write_document(selected: list[dict]) -> None:
    new_count = sum(record["source"] == "new-photo-session" for record in selected)
    old_count = len(selected) - new_count
    processed_count = sum(record["processed"] for record in selected)
    lines = [
        "# PHOTO SELECTION 2026",
        "",
        "Единая фотобиблиотека собрана из новой фотосессии и существующих ассетов сайта. Исходники не изменялись; шаблоны, тексты и опубликованный сайт не затрагивались.",
        "",
        "## Итог",
        "",
        f"- Всего отобрано фотографий: {len(selected)}.",
        f"- Новая съёмка: {new_count}; существующие ассеты: {old_count}.",
        f"- Обработано: {processed_count}; сохранено без повторного кодирования: {len(selected) - processed_count}.",
        "- Формат новых и переобработанных файлов: WebP, качество 88, длинная сторона не более 2400 px.",
        "- Папка экспорта: `src/assets/img/selected-2026/`.",
        "- Контактные листы: `contact-final-selection.jpg` и `contact-before-after.jpg`.",
        "",
        "## Цветовая и тональная система",
        "",
        "Базовая подача — реалистичная северная атмосфера: нейтрально-холодные небо и вода, сдержанные зелёные, натуральная фактура дерева и камня. Коррекция применялась по типу сцены, а не одинаковым пресетом: у наружных кадров мягко удерживались светлые участки, у интерьеров нейтрализовался избыток оранжевого, а тёплый вечерний свет и естественная теплота бани сохранялись. Сильные старые изображения оставлены без обработки, если вмешательство не давало явного выигрыша.",
        "",
    ]
    for category in CATEGORY_INFO:
        info = CATEGORY_INFO[category]
        lines.extend([f"## {info['title']}", ""])
        for record in [item for item in selected if item["category"] == category]:
            source_ru = "новая съёмка" if record["source"] == "new-photo-session" else "существующий ассет"
            processed_ru = "да" if record["processed"] else "нет"
            lines.extend(
                [
                    f"### `{record['filename']}`",
                    "",
                    f"- Исходный путь: `{record['path']}`",
                    f"- Источник: {source_ru} (`{record['source']}`)",
                    f"- Обработка: {processed_ru}",
                    f"- Категория: {info['title']}",
                    f"- Рекомендуемое место на сайте: {info['site']}",
                    f"- Статус: {role_label(record['role'])}",
                    f"- Причины выбора: {record['reason']}",
                    f"- Что исправлено: {PROCESSING_NOTES[record['profile']]}",
                    "",
                ]
            )
    lines.extend(
        [
            "## Ограничения применения",
            "",
            "Основные кадры выбраны под заявленную роль, но интеграция в шаблоны намеренно не выполнялась. Перед публикацией рекомендуется проверить фактический `object-position` на ключевых брейкпоинтах; особенно это важно для вертикальных основных кадров кухни, бани и активного отдыха.",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def load_or_build_inventory() -> list[dict]:
    inventory_path = REVIEW_ROOT / "inventory.json"
    if inventory_path.exists():
        return json.loads(inventory_path.read_text(encoding="utf-8"))
    inventory = build_inventory()
    write_inventory(inventory)
    return inventory


def export_library() -> None:
    inventory = load_or_build_inventory()
    selected = selection_records(inventory)
    export_selected(selected)
    build_final_contact_sheet(selected)
    build_before_after_contact_sheet(selected)
    write_document(selected)
    print(f"Exported {len(selected)} photographs to {OUTPUT_ROOT}")


def rebuild_contacts() -> None:
    inventory = load_or_build_inventory()
    selected = selection_records(inventory)
    build_final_contact_sheet(selected)
    build_before_after_contact_sheet(selected)
    print(f"Rebuilt contact sheets in {OUTPUT_ROOT}")


def validate_library() -> None:
    inventory = load_or_build_inventory()
    selected = selection_records(inventory)
    expected = {record["filename"] for record in selected}
    actual = {path.name for path in OUTPUT_ROOT.glob("*.webp")}
    if actual != expected:
        raise RuntimeError(f"WebP set mismatch: missing={sorted(expected - actual)}, extra={sorted(actual - expected)}")
    for record in selected:
        destination = OUTPUT_ROOT / record["filename"]
        with Image.open(destination) as image:
            image.verify()
        if record["profile"] == "none":
            source_hash = hashlib.sha256(Path(record["path"]).read_bytes()).digest()
            output_hash = hashlib.sha256(destination.read_bytes()).digest()
            if source_hash != output_hash:
                raise RuntimeError(f"Unprocessed file changed: {record['filename']}")
    for contact_name in ("contact-final-selection.jpg", "contact-before-after.jpg"):
        with Image.open(OUTPUT_ROOT / contact_name) as image:
            image.verify()
    document = DOC_PATH.read_text(encoding="utf-8")
    if document.count("### `") != len(selected):
        raise RuntimeError("Documentation entry count does not match selection count")
    print(f"Validated {len(selected)} photographs, two contact sheets, and documentation")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("review", "export", "contacts", "validate"))
    args = parser.parse_args()
    if args.command == "review":
        records = build_inventory()
        write_inventory(records)
        contact_sheets(records)
        print(f"Indexed {len(records)} images in {REVIEW_ROOT}")
    elif args.command == "export":
        export_library()
    elif args.command == "contacts":
        rebuild_contacts()
    elif args.command == "validate":
        validate_library()


if __name__ == "__main__":
    main()
