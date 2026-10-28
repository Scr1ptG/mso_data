"""Задание 8. Вход на сайт и данные из личного кабинета.

Тренировка к КТ «Авторизуйтесь с помощью Selenium в любом из сервисов».

Страница входа: polygon("login.html"). Учебный логин student, пароль polygon2026 (написаны на странице).
Поля: name="login", name="password", кнопка id="submit".
После входа откроется кабинет с секретным кодом <b id="secret">.

Подсказки:
    • после click() страница меняется не сразу — дождитесь элемента #secret:
      wait.until(EC.visibility_of_element_located((By.ID, "secret")))
    • ошибка входа показывается в <p id="error">
    • на настоящем сайте логин и пароль НЕ пишут прямо в коде:
      используйте input() или getpass, а для КТ — тестовый аккаунт, не основной
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common import start, polygon, check

driver = start()
wait = WebDriverWait(driver, 10)


def login(user, password):
    driver.get(polygon("login.html"))
    # ВАШ КОД: заполнить поля и нажать «Войти»


# а) Неверный пароль — достаньте текст ошибки
login("student", "12345")
error_text = ...  # ВАШ КОД: дождаться, пока #error станет видимым, и взять .text
check("08b", error_text)

# б) Правильный вход — достаньте секретный код
login("student", "polygon2026")
secret = ...  # ВАШ КОД
check("08a", secret)

# в) Бонус: выведите таблицу оценок #grades построчно (теги tr и td)

input("Нажмите Enter, чтобы закрыть браузер…")
driver.quit()
