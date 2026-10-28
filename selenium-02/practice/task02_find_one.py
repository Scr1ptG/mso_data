"""Задание 2. Найти ОДИН элемент пятью способами.

Откройте полигон в обычном браузере, нажмите F12 → вкладка Elements.
Кнопка со стрелкой (Ctrl+Shift+C) — кликните по элементу на странице, и он подсветится в коде.

find_element возвращает первый подходящий элемент. Если ничего не нашлось — ошибка NoSuchElementException.
У элемента есть:
    .text                    — видимый текст
    .get_attribute("href")   — значение атрибута (href, placeholder, class, ...)
"""
from selenium.webdriver.common.by import By

from common import start, polygon, check

driver = start()
driver.get(polygon("index.html"))

# а) По ID. Текст логотипа: <a id="logo">
logo_text = ...  # ВАШ КОД: driver.find_element(By.ID, "...").text
check("02a", logo_text)

# б) По тексту ссылки. Адрес ссылки «Спорт» в меню
sport_href = ...  # ВАШ КОД: By.LINK_TEXT и .get_attribute("href")
check("02b", sport_href)

# в) По имени. У поля поиска name="q". Достаньте его подсказку — атрибут placeholder
search_placeholder = ...  # ВАШ КОД: By.NAME
check("02c", search_placeholder)

# г) CSS-селектор. Текст подвала: <footer> → <p class="copyright">
#    Селектор «footer .copyright» значит: элемент с классом copyright ВНУТРИ footer
footer_text = ...  # ВАШ КОД: By.CSS_SELECTOR
check("02d", footer_text)

# д) XPath. Заголовок h2, у которого текст ровно «Главные новости»
#    Подсказка: //h2[text()="..."]
h2_text = ...  # ВАШ КОД: By.XPATH
check("02e", h2_text)

input("Нажмите Enter, чтобы закрыть браузер…")
driver.quit()
