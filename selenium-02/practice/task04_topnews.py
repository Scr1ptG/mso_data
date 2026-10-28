"""Задание 4. Главные новости полигона: ссылка, заголовок, время.

Это тренировка перед заданием LXP. Схема «группа → каждая новость в группе»:
    1. найти блок .topnews
    2. внутри него найти все карточки
    3. у каждой карточки достать ссылку, заголовок и время

Ловушка: первая карточка большая (card-big), остальные маленькие (card-mini).
Заголовки у них в РАЗНЫХ классах: card-big__title и card-mini__title.
CSS умеет «или» через запятую: ".card-big__title, .card-mini__title"

Где что лежит в карточке (посмотрите сами через F12):
    <a class="card-mini _topnews" href="article.html?id=101">   ← ссылка — атрибут href самой карточки
        <span class="card-mini__title">Заголовок</span>
        <time class="card-mini__info-item">23:40</time>         ← время — тег time
    </a>
"""
from selenium.webdriver.common.by import By

from common import start, polygon, check

driver = start()
driver.get(polygon("index.html"))

group = ...  # ВАШ КОД: блок главных новостей
cards = []   # ВАШ КОД: все карточки внутри group

news = []
for card in cards:
    link = ...   # ВАШ КОД: card.get_attribute(...)
    title = ...  # ВАШ КОД: card.find_element(...).text
    time = ...   # ВАШ КОД
    news.append({"link": link, "title": title, "time": time})

for n in news:
    print(n["time"], n["title"], n["link"], sep=" | ")
check("04", news)

input("Нажмите Enter, чтобы закрыть браузер…")
driver.quit()
