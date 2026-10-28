"""Задание 9 (бонус). Зайти в каждую новость и достать автора и текст.

План:
    1. На главной собрать ССЫЛКИ главных новостей (как в задании 4) — список строк.
    2. Пройти по списку: driver.get(ссылка), достать автора и первый абзац.

Ловушка: если сначала сохранить список элементов-карточек, а потом уйти на другую страницу,
старые элементы «протухнут» — StaleElementReferenceException. Поэтому сохраняем строки-ссылки, а не элементы.

На странице новости (посмотрите через F12):
    <h1 class="topic-body__title">     заголовок
    <span class="topic-authors__name"> автор
    <p class="topic-body__content-text"> абзацы текста
"""
import time

from selenium.webdriver.common.by import By

from common import start, polygon, check

driver = start()
driver.get(polygon("index.html"))

links = []  # ВАШ КОД: ссылки всех 8 главных новостей

articles = []
for link in links:
    driver.get(link)
    # ВАШ КОД: articles.append({"link": link, "title": ..., "author": ..., "text": ...})
    time.sleep(0.5)  # на настоящем сайте делайте паузу между страницами, чтобы не нагружать сервер

for a in articles:
    print(a.get("author"), "|", a.get("title"))
check("09", articles)

driver.quit()
