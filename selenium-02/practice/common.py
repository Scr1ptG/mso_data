"""Общий код для заданий: запуск браузера, адрес полигона и проверки ✅/❌.

Этот файл менять не нужно. В заданиях пишите:
    from common import start, polygon, check
"""
import os
import re
from pathlib import Path

from selenium import webdriver

# Какой браузер запускать: "chrome", "firefox" или "edge"
BROWSER = "chrome"

# Полигон лежит рядом с заданиями (папка mso_data/polygon) и открывается без интернета.
# Если папки нет, берём сайт из интернета.
LOCAL = Path(__file__).resolve().parents[2] / "polygon"
ONLINE = "https://scr1ptg.github.io/mso_data/polygon/"


def polygon(page="index.html"):
    """Адрес страницы полигона, например polygon("rubric.html?r=sport")."""
    name, _, query = page.partition("?")
    if (LOCAL / name).exists():
        url = (LOCAL / name).as_uri()
    else:
        url = ONLINE + name
    return url + ("?" + query if query else "")


def start(headless=False):
    """Запускает браузер. headless=True — без окна (быстрее, но ничего не видно)."""
    headless = headless or os.environ.get("HEADLESS") == "1"
    if BROWSER == "firefox":
        opts = webdriver.FirefoxOptions()
        if headless:
            opts.add_argument("-headless")
        return webdriver.Firefox(options=opts)
    if BROWSER == "edge":
        opts = webdriver.EdgeOptions()
        if headless:
            opts.add_argument("--headless=new")
        return webdriver.Edge(options=opts)
    opts = webdriver.ChromeOptions()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,900")
    return webdriver.Chrome(options=opts)


def _ok(name, msg=""):
    print(f"✅ {name}" + (f" — {msg}" if msg else ""))
    return True


def _bad(name, msg):
    print(f"❌ {name} — {msg}")
    return False


def check(name, value, hint=""):
    """Сравнивает ваш ответ с правильным. name — номер проверки, например "03a"."""
    if value is None or value is ...:
        return _bad(name, "переменная ещё не заполнена (там None или ...)")
    rule = RULES.get(name)
    if rule is None:
        return _bad(name, f"нет такой проверки «{name}»")
    try:
        verdict = rule(value)
    except Exception as e:  # студент передал не тот тип
        verdict = f"не получилось проверить: {type(e).__name__}: {e}"
    if verdict is True:
        return _ok(name)
    return _bad(name, (verdict or "ответ не совпал") + (f". Подсказка: {hint}" if hint else ""))


# ---------- правила проверки ----------

TIME_RE = re.compile(r"^\d{1,2}:\d{2}$")


def _news_list(items, n=None, need_time=True):
    """Проверка списка новостей: [{"link": ..., "title": ..., "time": ...}, ...]."""
    if not isinstance(items, list):
        return "нужен список (list) словарей"
    if n is not None and len(items) != n:
        return f"новостей {len(items)}, а должно быть {n}"
    if not items:
        return "список пустой — селектор ничего не нашёл?"
    for i, it in enumerate(items):
        if not isinstance(it, dict):
            return f"элемент №{i} — не словарь"
        missing = [k for k in ("link", "title", "time") if k not in it]
        if missing:
            return f"в новости №{i} нет ключей {missing}"
        if not str(it["link"]).startswith(("http", "file:")):
            return f"в новости №{i} ссылка «{it['link']}» — нужна полная ссылка: get_attribute('href')"
        if not str(it["title"]).strip():
            return f"в новости №{i} пустой заголовок — проверьте селектор заголовка"
        if need_time and not TIME_RE.match(str(it["time"]).strip()):
            return f"в новости №{i} время «{it['time']}» — ожидали формат ЧЧ:ММ"
    return True


def _rule_04(items):
    base = _news_list(items, 8)
    if base is not True:
        return base
    if items[0]["title"] != "Цены на видеокарты снизились впервые за полгода":
        return "первая новость не та — большая карточка (card-big) должна идти первой"
    if items[0]["time"] != "23:55" or "id=301" not in items[0]["link"]:
        return "у первой новости не совпали время или ссылка"
    if items[-1]["title"] != "Спрос на программистов вырос на 12 процентов":
        return "последняя новость не та"
    return True


def _rule_06(rows):
    if not isinstance(rows, list):
        return "нужен список словарей"
    by_rubric = {}
    for r in rows:
        by_rubric.setdefault(r.get("rubric"), []).append(r)
    for k in ("science", "sport", "economics"):
        got = len(by_rubric.get(k, []))
        if got == 6:
            return f"в рубрике {k} только 6 новостей — нажмите «Показать ещё» и дождитесь остальных"
        if got != 12:
            return f"в рубрике {k} новостей {got}, а должно быть 12"
    return _news_list(rows, 36)


RULES = {
    "01": lambda v: v == "Новости Полигона" or f"получили «{v}»",
    "02a": lambda v: v == "Новости Полигона" or f"получили «{v}» — это текст логотипа с id=logo?",
    "02b": lambda v: str(v).endswith("rubric.html?r=sport") or f"получили «{v}» — нужен href ссылки «Спорт»",
    "02c": lambda v: v == "Поиск по новостям" or f"получили «{v}» — нужен атрибут placeholder",
    "02d": lambda v: "Учебный сайт для практики Selenium" in str(v) or f"получили «{v}»",
    "02e": lambda v: v == "Главные новости" or f"получили «{v}»",
    "03a": lambda v: v == 8 or (f"{v} — вы считали карточки на всей странице, а не внутри .topnews?" if v in (16, 17, 18) else f"получили {v}"),
    "03b": lambda v: v == 7 or f"получили {v}",
    "03c": lambda v: (isinstance(v, list) and len(v) == 7 and v[0] == "Студенты IThub научили робота-пылесоса объезжать рюкзаки") or "нужен список из 7 заголовков маленьких карточек, по порядку",
    "04": _rule_04,
    "05": lambda v: _news_list(v) if (isinstance(v, list) and len(v) >= 5) else "на главной lenta.ru главных новостей обычно 10–20, у вас меньше 5",
    "06": _rule_06,
    "07a": lambda v: str(v) == "391" or f"17 умножить на 23 — ожидали 391, получили «{v}»",
    "07b": lambda v: str(v) == "3.33" or f"10 разделить на 3 — ожидали 3.33, получили «{v}». Дождались ответа?",
    "07c": lambda v: "деление на ноль" in str(v) or f"получили «{v}»",
    "08a": lambda v: v == "SEL-4729" or f"получили «{v}» — вы точно вошли в кабинет?",
    "08b": lambda v: v == "Неверный логин или пароль" or f"получили «{v}» — дождитесь появления ошибки",
    "09": lambda v: (isinstance(v, list) and len(v) == 8 and all(r.get("author") for r in v) and v[0]["author"] == "Елена Соколова")
                    or "нужно 8 словарей с ключом author, первым — автор новости про видеокарты",
}
