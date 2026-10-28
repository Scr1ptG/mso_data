"""Задание 6. Три рубрики, кнопка «Показать ещё» и ожидание. Сохраняем в CSV.

Тренировка к КТ «парсер трёх разделов новостей».

На странице рубрики сразу видно 6 новостей. Остальные 6 появятся после кнопки «Показать ещё»,
и не мгновенно, а через полторы секунды (как на настоящем сайте: данные идут по сети).

Если сразу после click() считать карточки — получится 6. Нужно ПОДОЖДАТЬ.
    time.sleep(3)  — работает, но ждёт всегда 3 секунды, даже если всё уже загрузилось
    WebDriverWait  — ждёт ровно столько, сколько нужно (но не дольше 10 секунд):

    wait = WebDriverWait(driver, 10)
    wait.until(EC.invisibility_of_element_located((By.ID, "loadmore")))   # ждём, пока кнопка исчезнет

Адрес рубрики: polygon("rubric.html?r=science"), рубрики: science, sport, economics.
Карточки рубрики — a.card-mini._longgrid внутри .rubric-page__container
"""
import csv

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common import start, polygon, check

driver = start()
wait = WebDriverWait(driver, 10)

rows = []
for rubric in ["science", "sport", "economics"]:
    driver.get(polygon(f"rubric.html?r={rubric}"))
    # ВАШ КОД:
    # 1. найти кнопку loadmore и нажать
    # 2. подождать, пока она исчезнет
    # 3. собрать все карточки: ссылка, заголовок, время
    # 4. добавить в rows словари {"rubric": rubric, "link": ..., "title": ..., "time": ...}
    print(rubric, "— собрано всего:", len(rows))

check("06", rows)

# Сохраняем в CSV. encoding="utf-8-sig" — чтобы Excel правильно показал русские буквы
with open("rubrics.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["rubric", "time", "title", "link"], delimiter=";")
    writer.writeheader()
    writer.writerows(rows)
print("Сохранено в rubrics.csv")

driver.quit()
