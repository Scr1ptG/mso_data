"""Общий код для заданий: запуск браузера, адрес полигона, проверки ✅/❌ и скриншоты.

Этот файл менять не нужно. В заданиях пишите:
    from common import start, polygon, check
Работает и на компьютере, и в Google Colab (там браузер без окна, смотреть через show).
"""
import os
import re
import sys
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By

# Какой браузер запускать: "chrome", "firefox" или "edge"
BROWSER = "chrome"

IN_COLAB = "google.colab" in sys.modules

# Полигон лежит рядом с заданиями (папка mso_data/polygon) и открывается без интернета.
# Если папки нет (например, в Colab), берём сайт из интернета.
_here = Path(__file__).resolve()
LOCAL = _here.parents[2] / "polygon" if len(_here.parents) > 2 else None
ONLINE = "https://scr1ptg.github.io/mso_data/polygon/"


def polygon(page="index.html"):
    """Адрес страницы полигона, например polygon("rubric.html?r=sport")."""
    name, _, query = page.partition("?")
    if LOCAL is not None and (LOCAL / name).exists():
        url = (LOCAL / name).as_uri()
    else:
        url = ONLINE + name
    return url + ("?" + query if query else "")


def _find_all(driver, selector):
    """CSS-селектор или XPath (если начинается с / или ( )."""
    by = By.XPATH if selector.lstrip().startswith(("/", "(", "./")) else By.CSS_SELECTOR
    return driver.find_elements(by, selector)


def show(driver, elements=None, width=900):
    """Скриншот страницы. Если передать элементы (или селектор), они будут обведены красным.

    show(driver)                       — что сейчас видит браузер
    show(driver, card)                 — обвести один элемент
    show(driver, cards)                — обвести список элементов
    show(driver, ".topnews a")         — обвести всё, что находит селектор
    """
    if isinstance(elements, str):
        elements = _find_all(driver, elements)
    if elements is not None and not isinstance(elements, (list, tuple)):
        elements = [elements]
    elements = list(elements or [])
    js_mark = "arguments[0].forEach(e => { e.dataset.oldOutline = e.style.outline; e.style.outline = '3px solid red'; });"
    js_unmark = "arguments[0].forEach(e => { e.style.outline = e.dataset.oldOutline || ''; });"
    if elements:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elements[0])
        driver.execute_script(js_mark, elements)
    png = driver.get_screenshot_as_png()
    if elements:
        driver.execute_script(js_unmark, elements)
    try:
        from IPython import get_ipython
        from IPython.display import Image, display
        if get_ipython() is None:
            raise ImportError
        display(Image(png, width=width))
    except ImportError:
        Path("screenshot.png").write_bytes(png)
        print("Скриншот сохранён в screenshot.png")


def try_selector(driver, selector, show_page=True):
    """Как Ctrl+F в F12: сколько элементов найдёт селектор, и где они на странице."""
    try:
        found = _find_all(driver, selector)
    except Exception as e:
        print(f"❌ Ошибка в селекторе «{selector}»: {type(e).__name__}")
        return []
    print(f"«{selector}» — найдено: {len(found)}")
    for el in found[:5]:
        print("   •", (el.text or el.get_attribute("outerHTML")[:80]).replace("\n", " / ")[:90])
    if len(found) > 5:
        print(f"   … и ещё {len(found) - 5}")
    if show_page and found:
        show(driver, found)
    return found


def start(headless=False):
    """Запускает браузер. headless=True — без окна (быстрее, но ничего не видно)."""
    headless = headless or os.environ.get("HEADLESS") == "1"
    if IN_COLAB:
        # В Colab нет экрана: только Chrome без окна и с флагами для контейнера
        opts = webdriver.ChromeOptions()
        for arg in ("--headless=new", "--no-sandbox", "--disable-dev-shm-usage", "--window-size=1280,900", "--lang=ru-RU", NO_HTTPS_UPGRADE):
            opts.add_argument(arg)
        return webdriver.Chrome(options=opts)
    if BROWSER == "firefox":
        opts = webdriver.FirefoxOptions()
        if headless:
            opts.add_argument("-headless")
        opts.set_preference("dom.security.https_first", False)
        return webdriver.Firefox(options=opts)
    if BROWSER == "edge":
        opts = webdriver.EdgeOptions()
        if headless:
            opts.add_argument("--headless=new")
        opts.add_argument(NO_HTTPS_UPGRADE)
        return webdriver.Edge(options=opts)
    opts = webdriver.ChromeOptions()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,900")
    opts.add_argument(NO_HTTPS_UPGRADE)
    return webdriver.Chrome(options=opts)


# Chrome 157+ сам переписывает http:// на https://. У сайтов без https (например, ithub.role.ru)
# страница тогда открывается ПУСТОЙ. Этот флаг выключает подмену.
NO_HTTPS_UPGRADE = "--disable-features=HttpsUpgrades,HttpsFirstBalancedModeAutoEnable"


def full_page_screenshot(driver, path):
    """Скриншот ВСЕЙ страницы, а не только видимой части (для Chrome без окна)."""
    old = driver.get_window_size()
    height = driver.execute_script("return document.documentElement.scrollHeight")
    driver.set_window_size(old["width"], height + 200)
    driver.save_screenshot(path)
    driver.set_window_size(old["width"], old["height"])
    return path


def show_image(path, width=400):
    """Показать картинку из файла прямо в ноутбуке и напечатать её размер."""
    from PIL import Image as PILImage
    with PILImage.open(path) as im:
        print(f"{path}: {im.size[0]}×{im.size[1]} px, {Path(path).stat().st_size // 1024} КБ")
    try:
        from IPython.display import Image, display
        display(Image(filename=str(path), width=width))
    except ImportError:
        pass


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


# ---------- занятие 3: картинки и файлы (проверки i01…i10 получают путь к файлу или значение) ----------

def _file_kind(path):
    p = Path(str(path))
    if not p.exists():
        return None, f"файла «{path}» нет — вы его сохранили?"
    head = p.read_bytes()[:16]
    if not head:
        return None, "файл пустой (0 байт)"
    if head.startswith(b"\xff\xd8"):
        return "jpg", None
    if head.startswith(b"\x89PNG"):
        return "png", None
    if head.startswith(b"%PDF"):
        return "pdf", None
    if head.lstrip().startswith(b"<"):
        return "html", None
    return "other", None


def _img_size(path):
    from PIL import Image as PILImage
    with PILImage.open(str(path)) as im:
        return im.size


def _rule_file(path, kind, size=None):
    k, err = _file_kind(path)
    if err:
        return err
    if k == "html" and kind != "html":
        return "в файле HTML-страница, а не картинка/документ — вы скачали адрес страницы вместо src/href?"
    if k != kind:
        return f"внутри файла не {kind.upper()}, а {k} — пишите response.content в режиме 'wb'"
    if size and _img_size(path) != size:
        return f"размер картинки {_img_size(path)}, а ожидали {size}"
    return True


def _rule_i04(path):
    base = _rule_file(path, "png")
    if base is not True:
        return base
    w, h = _img_size(path)
    if h < 1200:
        return f"высота скриншота {h} px — это только видимая часть окна, а страница выше (около 1340 px)"
    return True


def _rule_i08(links):
    if not isinstance(links, list) or not links:
        return "нужен список ссылок (строк)"
    if len(links) == 12:
        return "ссылок 12 — это только первая порция. Прокручивайте страницу вниз, пока не появится «Это все фотографии»"
    if any("placeholder" in str(x) for x in links):
        return "среди ссылок есть placeholder.svg — это src ещё не загруженных картинок. Берите href карточки"
    if any("/thumb/" in str(x) for x in links):
        return "это миниатюры (thumb). Оригиналы — в href ссылки-карточки"
    if len(links) != 72:
        return f"ссылок {len(links)}, а фотографий 72"
    if len(set(links)) != 72:
        return "есть повторы — вы собирали карточки несколько раз?"
    if not all(str(x).endswith(".jpg") and "/photos/full/" in str(x) for x in links):
        return "ожидали ссылки вида …/photos/full/ball_01.jpg"
    return True


def _rule_i09(folder):
    root = Path(str(folder))
    if not root.is_dir():
        return f"папки «{folder}» нет"
    for cls in ("ball", "box", "tree"):
        files = sorted((root / cls).glob("*.jpg"))
        if len(files) != 24:
            return f"в папке {cls} файлов {len(files)}, а должно быть 24"
        bad = [f.name for f in files if _rule_file(f, "jpg", (512, 512)) is not True]
        if bad:
            return f"в {cls} не оригиналы 512×512: {bad[:3]}"
    return True


RULES.update({
    "i01": lambda v: (str(v).startswith("http") and str(v).endswith("/img/cat-web.jpg"))
                     or f"получили «{v}» — нужен атрибут src тега img, полная ссылка",
    "i02": lambda v: _rule_file(v, "jpg", (600, 464)),
    "i03": lambda v: _rule_file(v, "png") if _rule_file(v, "png") is not True or 580 <= _img_size(v)[0] <= 620
                     else f"ширина {_img_size(v)[0]} px — это скриншот всей страницы, а нужен только элемент img",
    "i04": _rule_i04,
    "i05": lambda v: _rule_file(v, "pdf") if _rule_file(v, "pdf") is not True or Path(str(v)).stat().st_size > 400_000
                     else "PDF слишком маленький — файл скачался не целиком?",
    "i06": lambda v: _rule_file(v, "html") if _rule_file(v, "html") is not True or "Новость IT" in Path(str(v)).read_text(encoding="utf-8", errors="ignore")
                     else "в файле нет страницы с новостью — вы сохранили page_source после перехода по ссылке?",
    "i07": lambda v: tuple(map(tuple, v)) == ((128, 128), (512, 512))
                     or (f"получили {v}. Сначала размер миниатюры (src/data-src), потом оригинала (href)"
                         if tuple(map(tuple, v)) == ((512, 512), (128, 128)) else f"получили {v}, ожидали ((128, 128), (512, 512))"),
    "i08": _rule_i08,
    "i09": _rule_i09,
    "i10": lambda v: _rule_file(v, "jpg", (512, 512)),
})
