"""Задание 3. Найти МНОГО элементов и искать внутри блока.

find_elements (с буквой s!) возвращает СПИСОК. Если ничего не нашлось — пустой список [], без ошибки.

Главная мысль задания: искать можно не только во всём driver, но и внутри найденного элемента:
    group = driver.find_element(By.CLASS_NAME, "topnews")
    cards = group.find_elements(...)     # ищет только внутри group
"""
from selenium.webdriver.common.by import By

from common import start, polygon, check

driver = start()
driver.get(polygon("index.html"))

# Сначала для сравнения: все ссылки-карточки на всей странице.
# Классы card-big и card-mini есть и в «Главных новостях», и в «По рубрикам».
everywhere = driver.find_elements(By.CSS_SELECTOR, ".card-big, .card-mini")
print("Карточек на всей странице:", len(everywhere))

# а) Найдите блок главных новостей (class="topnews") и посчитайте карточки ТОЛЬКО в нём.
#    Карточки — это ссылки <a> внутри блока.
group = ...  # ВАШ КОД: driver.find_element(...)
count_top = ...  # ВАШ КОД: len(group.find_elements(...))
check("03a", count_top)

# б) Сколько в этом блоке маленьких карточек (class="card-mini")?
count_mini = ...  # ВАШ КОД
check("03b", count_mini)

# в) Соберите заголовки маленьких карточек в список.
#    Заголовок маленькой карточки — <span class="card-mini__title">
titles = []
# ВАШ КОД: цикл for по карточкам, titles.append(...)

print(*titles, sep="\n")
check("03c", titles)

input("Нажмите Enter, чтобы закрыть браузер…")
driver.quit()
