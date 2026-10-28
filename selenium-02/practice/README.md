# Практика: Selenium, поиск элементов

## Как начать
1. Распакуйте архив целиком. Рядом должны лежать папки `polygon` и `selenium-02`: задания ищут сайт-полигон по этому пути.
2. Если Selenium ещё не стоит: `pip install selenium`
3. Откройте `task01_open.py` и запустите. Откроется браузер с сайтом «Новости Полигона», в консоли будет ✅.

В каждом задании замените `...` своим кодом и запустите файл. Проверка сама напишет ✅ или ❌ и подскажет, что не так.

Chrome не запускается? В `common.py` поменяйте `BROWSER = "chrome"` на `"firefox"` или `"edge"`.

## Задания
| № | Что тренируем |
|---|---|
| 1 | Открыть сайт, `driver.title` |
| 2 | Один элемент: ID, LINK_TEXT, NAME, CSS, XPath |
| 3 | `find_elements` и поиск внутри блока |
| 4 | Главные новости полигона: ссылка, заголовок, время |
| 5 | **То же на lenta.ru — сдать в LXP** |
| 6 | 3 рубрики, «Показать ещё», ожидание → CSV (заготовка к КТ) |
| 7 | Калькулятор: `send_keys`, `Select`, ожидание ответа |
| 8 | Вход на сайт, секретный код (заготовка к КТ) |
| 9 | Бонус: зайти в каждую новость |

## Шпаргалка
```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

el = driver.find_element(By.CSS_SELECTOR, ".topnews")   # один, нет → ошибка
els = driver.find_elements(By.CSS_SELECTOR, "a")        # список, нет → []
inner = el.find_elements(By.TAG_NAME, "a")              # поиск ВНУТРИ el

el.text                       # видимый текст
el.get_attribute("href")      # атрибут (полная ссылка)

field.clear(); field.send_keys("текст"); button.click()
Select(select_el).select_by_visible_text("умножить")

wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.ID, "secret")))   # двойные скобки!
```

| CSS | Значит |
|---|---|
| `time` | тег |
| `.card-mini` | класс |
| `#logo` | id |
| `a._topnews` | тег a **и** класс _topnews |
| `.topnews a` | a **внутри** .topnews |
| `.a, .b` | .a **или** .b |
| `[name="login"]` | по атрибуту |

XPath внутри элемента начинайте с точки: `card.find_element(By.XPATH, ".//time")`.

**Проверяйте селектор в браузере до кода:** F12 → Elements → Ctrl+F → вставить селектор → справа «1 of 8».
