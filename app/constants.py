from typing import Any

TOP_SLIDER_ITEMS = [
    ["Постные рецепты", "/catalog/postnye-bluda", "/images/sliders/post-1.webp"],
    [
        "Постные блюда",
        "/article/all?catalog_id=8",
        "/images/sliders/post-2.webp",
    ],
    # ["Рецепты на 8 марта", "/holiday/8-march", "/images/sliders/8-march.webp"],
    ["Первые блюда", "/catalog/pervye-bluda", "/images/sliders/sup.webp"],
    ["Вторые блюда", "/catalog/vtorye-bluda", "/images/sliders/second.webp"],
    ["Салаты", "/catalog/salaty", "/images/sliders/salad.webp"],
    ["Закуски", "/catalog/zakuski", "/images/sliders/zakuski.webp"],
    ["Десерты", "/catalog/deserty", "/images/sliders/desserts.webp"],
    ["Выпечка", "/catalog/izdeliya-iz-testa", "/images/sliders/bake.webp"],
    ["Напитки", "/catalog/napitki", "/images/sliders/drinks.webp"],
    ["Супы", "/catalog/supy", "/images/sliders/sup-1.webp"],
    [
        "Салаты для похудения",
        "/catalog/salat-dlya-pohudeniya",
        "/images/sliders/salad-1.webp",
    ],
    ["Паста", "/catalog/pasta", "/images/sliders/pasta.webp"],
    ["Ризотто", "/catalog/rizotto", "/images/sliders/rizotto.webp"],
    [
        "Диетические рецепты",
        "/catalog/dieticheskie-retsepty",
        "/images/sliders/diet.webp",
    ],
    ["Пирожное", "/catalog/pirozhnoe", "/images/sliders/pirozhnoe.webp"],
    [
        "Горячие бутерброды",
        "/catalog/goryachie-buterbrody",
        "/images/sliders/goryachie-buterbrody.webp",
    ],
    [
        "Блюда из мяса",
        "/catalog/bluda-iz-myasa",
        "/images/sliders/bluda-iz-myasa.webp",
    ],
    ["Блюда из рыбы", "/catalog/bluda-iz-ryby", "/images/sliders/fish.webp"],
    ["Фунчоза", "/ingredient/funchoza", "/images/sliders/funchoza.webp"],
    ["Сырники", "/catalog/syrniki", "/images/sliders/syrniki.webp"],
    ["Чечевица", "/ingredient/chechevitsa", "/images/sliders/chechevitsa.webp"],
    [
        "Печенье",
        "/catalog/pechene-i-drugaya-melkaya-vypechka",
        "/images/sliders/pechene.webp",
    ],
    [
        "Свиная грудинка",
        "/ingredient/svinaya-grudinka",
        "/images/sliders/svinaya-grudinka.webp",
    ],
    [
        "Морские гребешки",
        "/ingredient/morskie-grebeshki",
        "/images/sliders/morskie-grebeshki.webp",
    ],
    ["Простые рецепты", "/collection/show/11646", "/images/sliders/simple.webp"],
    [
        "Блюда за 20 минут",
        "/collection/show/9990",
        "/images/sliders/20-minutes.webp",
    ],
    [
        "Быстрая выпечка",
        "/collection/show/9256",
        "/images/sliders/fast-bake.webp",
    ],
    [
        "Домашнее тесто",
        "/catalog/domashnee-testo",
        "/images/sliders/home-testo.webp",
    ],
    ["Цыпленок", "/ingredient/tsyplenok", "/images/sliders/tsyplenok.webp"],
    ["Канапе", "/catalog/kanape", "/images/sliders/kanape.webp"],
    [
        "Рисовая мука",
        "/ingredient/muka-risovaya",
        "/images/sliders/muka-risovaya.webp",
    ],
    [
        "Соленья и маринады",
        "/catalog/solenya-i-marinady",
        "/images/sliders/solenya.webp",
    ],
    [
        "Овощные гарниры",
        "/collection/show/8912",
        "/images/sliders/vegetable-side-dishes.webp",
    ],
    ["Лазанья", "/catalog/lazanya", "/images/sliders/lazanya.webp"],
]


# Глобальные атрибуты, которые разрешаем на всех тегах (как all: %w[id class style])
GLOBAL_ATTRIBUTES: set[str] = {"id", "class", "style"}

# Разрешённые теги — почти как в твоём RELAXED + расширенные
ALLOWED_TAGS: set[str] = {
    "a",
    "abbr",
    "b",
    "img",
    "blockquote",
    "br",
    "cite",
    "code",
    "dd",
    "dfn",
    "dl",
    "dt",
    "em",
    "i",
    "kbd",
    "li",
    "mark",
    "ol",
    "p",
    "pre",
    "q",
    "s",
    "small",
    "strike",
    "strong",
    "sub",
    "sup",
    "time",
    "u",
    "ul",
    "var",
    "div",
    "span",
    "hr",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "table",
    "tr",
    "td",
}

# Атрибуты по тегам (расширяем дефолтные + твои из примера)
ALLOWED_ATTRIBUTES: dict[str, set[str]] = {
    "*": GLOBAL_ATTRIBUTES,  # ← на все теги (аналог all)
    "img": {"src", "alt", "title"},
    "a": {"href", "target"},
    "table": {
        "style",
        "background",
        "bgcolor",
        "border",
        "bordercolor",
        "cellpadding",
        "cellspacing",
        "cols",
        "height",
        "width",
        "align",
    },
    "tr": {"style", "align", "bgcolor", "bordercolor", "char", "charoff", "valign"},
    "td": {
        "style",
        "align",
        "background",
        "bgcolor",
        "bordercolor",
        "colspan",
        "height",
        "nowrap",
        "rowspan",
        "valign",
        "width",
    },
}

# Фиксированные добавляемые атрибуты (аналог add_attributes)
FIXED_ATTRIBUTES: dict[str, dict[str, str]] = {
    "a": {"rel": "nofollow"},
    "img": {
        "class": "img-fluid image-resize",
        "style": "max-width: 100%",
        "loading": "lazy",
    },
}

CONFIG_SANITIZE: dict[str, Any] = {
    "tags": ALLOWED_TAGS.copy(),
    "attributes": ALLOWED_ATTRIBUTES.copy(),
    "set_tag_attribute_values": FIXED_ATTRIBUTES.copy(),
    # Дополнительные полезные настройки (рекомендую):
    "link_rel": None,  # отключаем авто-добавление rel, т.к. мы сами добавляем nofollow
    "strip_comments": True,
    "url_schemes": {"http", "https", "mailto", "data"},
}

# Добавляем iframe в теги и атрибуты
ALLOWED_TAGS_ARTICLE = ALLOWED_TAGS | {"iframe"}

ALLOWED_ATTRIBUTES_ARTICLE = ALLOWED_ATTRIBUTES.copy()
ALLOWED_ATTRIBUTES_ARTICLE["iframe"] = {"style", "src", "class"}

# Фиксированные атрибуты для article-варианта
FIXED_ATTRIBUTES_ARTICLE = FIXED_ATTRIBUTES.copy()
FIXED_ATTRIBUTES_ARTICLE["iframe"] = {"class": "article-video"}
# img здесь без 'img-fluid image-resize' — как в твоём примере
del FIXED_ATTRIBUTES_ARTICLE["img"]["class"]  # если хочешь убрать, или переопредели
FIXED_ATTRIBUTES_ARTICLE["img"] = {"loading": "lazy"}

CONFIG_SANITIZE_ARTICLE: dict[str, Any] = {
    "tags": ALLOWED_TAGS_ARTICLE,
    "attributes": ALLOWED_ATTRIBUTES_ARTICLE,
    "set_tag_attribute_values": FIXED_ATTRIBUTES_ARTICLE,
    "link_rel": None,
    "strip_comments": True,
    "url_schemes": {"http", "https", "mailto", "data"},
}

TAGS_WITHOUT_ANCHORS = ALLOWED_TAGS_ARTICLE.copy()
TAGS_WITHOUT_ANCHORS.discard("a")
CONFIG_SANITIZE_WITHOUT_ANCHORS: dict[str, Any] = {
    "tags": TAGS_WITHOUT_ANCHORS,
    "attributes": ALLOWED_ATTRIBUTES_ARTICLE,
    "set_tag_attribute_values": FIXED_ATTRIBUTES_ARTICLE,
    "link_rel": None,
    "strip_comments": True,
    "url_schemes": {"http", "https", "mailto", "data"},
}
