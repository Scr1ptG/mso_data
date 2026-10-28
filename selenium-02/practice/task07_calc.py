"""Задание 7. Форма калькулятора: ввести, выбрать, нажать, дождаться.

    el.clear()               — очистить поле
    el.send_keys("17")       — напечатать текст в поле
    el.click()               — нажать
    Select(el).select_by_visible_text("умножить")   — выбрать пункт выпадающего списка
    Select(el).select_by_value("mul")               — то же, по атрибуту value

Ответ появляется не сразу: сначала «считаем…», потом число. Ждём, пока текст станет другим:
    wait.until(lambda d: d.find_element(By.ID, "result").text not in ("", "считаем…"))

Поля: <input id="a">, <select id="op">, <input id="b">, кнопка <button id="eq">, ответ <span id="result">
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait

from common import start, polygon, check

driver = start()
driver.get(polygon("calc.html"))
wait = WebDriverWait(driver, 10)


def calculate(a, op_text, b):
    """Вводит два числа, выбирает действие, нажимает «=» и возвращает ответ (строкой)."""
    # ВАШ КОД
    return None


check("07a", calculate(17, "умножить", 23))
check("07b", calculate(10, "разделить", 3))
check("07c", calculate(5, "разделить", 0))

input("Нажмите Enter, чтобы закрыть браузер…")
driver.quit()
