"""Задание 1. Открыть полигон.

Проверяем, что Selenium и браузер работают.
1. Запустите файл. Должно открыться окно браузера с сайтом «Новости Полигона».
2. Сохраните в переменную title заголовок вкладки: driver.title
"""
from common import start, polygon, check

driver = start()
driver.get(polygon("index.html"))

title = ...  # ВАШ КОД

print("Заголовок вкладки:", title)
check("01", title)

input("Нажмите Enter, чтобы закрыть браузер…")
driver.quit()
