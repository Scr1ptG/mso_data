'use strict';
// Учебный новостной сайт для Selenium. Разметка главных новостей и рубрик повторяет lenta.ru
// (классы card-big / card-mini / topnews / _longgrid), чтобы код с полигона легко переносился на настоящий сайт.
// Страница выбирается атрибутом <body data-page="...">.

const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const param = name => new URLSearchParams(location.search).get(name);
const app = document.getElementById('app');

function header() {
  const links = [['index.html', 'Главная'], ...Object.entries(RUBRICS).map(([k, v]) => [`rubric.html?r=${k}`, v]), ['calc.html', 'Калькулятор'], ['login.html', 'Войти']];
  const here = location.pathname.split('/').pop() + location.search;
  document.body.insertAdjacentHTML('afterbegin', `
<header class="header">
  <a id="logo" class="header__logo" href="index.html">Новости Полигона</a>
  <nav class="menu">${links.map(([h, t]) => `<a class="menu__link${h === here || (h === 'index.html' && here === '') ? ' _active' : ''}" href="${h}">${t}</a>`).join('')}</nav>
  <form class="search" onsubmit="return false"><input name="q" type="search" placeholder="Поиск по новостям"></form>
</header>`);
  document.body.insertAdjacentHTML('beforeend', `
<footer class="footer"><p class="copyright">© 2026 Новости Полигона. Учебный сайт для практики Selenium, все новости выдуманы.</p></footer>
<div id="cookie" class="cookie">
  <span>Мы используем cookie, чтобы сайт работал. Это учебный баннер: он появляется в каждом новом окне браузера.</span>
  <button id="cookie-ok" class="btn">Понятно</button>
</div>`);
  document.getElementById('cookie-ok').onclick = () => document.getElementById('cookie').remove();
}

function cardBig(n) {
  return `<a class="card-big _topnews" href="article.html?id=${n.id}">
  <div class="card-big__image-wrap"><div class="card-big__image _${n.rubric}"></div></div>
  <div class="card-big__titles"><h3 class="card-big__title">${esc(n.title)}</h3></div>
  <div class="card-big__info"><time class="card-big__date">${n.time}</time></div>
</a>`;
}

function cardMini(n, mod) {
  return `<a class="card-mini ${mod}" href="article.html?id=${n.id}">
  <div class="card-mini__text">
    <span class="card-mini__title">${esc(n.title)}</span>
    <div class="card-mini__info"><time class="card-mini__info-item">${n.time}</time></div>
  </div>
</a>`;
}

const pages = {
  index() {
    document.title = 'Новости Полигона';
    const top = TOPNEWS.map(byId);
    const left = top.slice(0, 4), right = top.slice(4);
    const rub = Object.entries(RUBRICS).map(([k, v]) => {
      const items = NEWS.filter(x => x[1] === k).slice(0, 3).map(x => byId(x[0]));
      return `<div class="rubric-box">
  <a class="rubric-box__title" href="rubric.html?r=${k}">${v}</a>
  ${items.map(n => cardMini(n, '_rubric')).join('')}
</div>`;
    }).join('');
    app.innerHTML = `
<div class="main-page">
  <section class="main-page__section">
    <h2 class="section-title topnews__title">Главные новости</h2>
    <div class="topnews">
      <div class="topnews__column">${cardBig(left[0])}${left.slice(1).map(n => cardMini(n, '_topnews')).join('')}</div>
      <div class="topnews__column">${right.map(n => cardMini(n, '_topnews')).join('')}</div>
    </div>
  </section>
  <section class="main-page__section">
    <h2 class="section-title">По рубрикам</h2>
    <div class="rubrics">${rub}</div>
  </section>
</div>`;
  },

  rubric() {
    const r = param('r');
    if (!RUBRICS[r]) {
      document.title = 'Рубрика не найдена';
      app.innerHTML = `<p class="empty">Рубрика не найдена. Есть такие: ${Object.keys(RUBRICS).map(k => `<a href="rubric.html?r=${k}">${k}</a>`).join(', ')}.</p>`;
      return;
    }
    document.title = `${RUBRICS[r]} — Новости Полигона`;
    const items = NEWS.filter(x => x[1] === r).map(x => byId(x[0]));
    const FIRST = 6;
    app.innerHTML = `
<div class="rubric-page">
  <h1 class="rubric-header__title">${RUBRICS[r]}</h1>
  <div class="rubric-page__container">${items.slice(0, FIRST).map(n => cardMini(n, '_longgrid')).join('')}</div>
  <button id="loadmore" class="btn loadmore">Показать ещё</button>
</div>`;
    const btn = document.getElementById('loadmore');
    btn.onclick = () => {
      // Как на настоящих сайтах: новости приходят не сразу, а через сеть
      btn.disabled = true;
      btn.textContent = 'Загружаем…';
      setTimeout(() => {
        document.querySelector('.rubric-page__container').insertAdjacentHTML('beforeend', items.slice(FIRST).map(n => cardMini(n, '_longgrid')).join(''));
        btn.remove();
      }, 1500);
    };
  },

  article() {
    const n = byId(+param('id'));
    if (!n) {
      document.title = 'Новость не найдена';
      app.innerHTML = '<p class="empty">Новость не найдена. <a href="index.html">На главную</a></p>';
      return;
    }
    document.title = `${n.title} — Новости Полигона`;
    const paras = n.text.match(/[^.!?]+[.!?]+/g) || [n.text];
    app.innerHTML = `
<article class="topic-page">
  <div class="topic-header">
    <a class="topic-header__rubric" href="rubric.html?r=${n.rubric}">${RUBRICS[n.rubric]}</a>
    <time class="topic-header__time">${n.time}, ${DATE}</time>
  </div>
  <h1 class="topic-body__title">${esc(n.title)}</h1>
  <div class="topic-authors">Автор: <span class="topic-authors__name">${esc(n.author)}</span></div>
  <div class="topic-body__content">${paras.map(p => `<p class="topic-body__content-text">${esc(p.trim())}</p>`).join('')}</div>
</article>`;
  },

  login() {
    document.title = 'Вход — Новости Полигона';
    app.innerHTML = `
<form id="login-form" class="form">
  <h1>Вход в личный кабинет</h1>
  <label class="form__row">Логин <input id="login" name="login" type="text" autocomplete="off"></label>
  <label class="form__row">Пароль <input id="password" name="password" type="password"></label>
  <label class="form__check"><input id="remember" name="remember" type="checkbox"> Запомнить меня</label>
  <button id="submit" class="btn primary" type="submit">Войти</button>
  <p id="error" class="error" hidden></p>
  <div class="hint">Учебный вход: логин <code>student</code>, пароль <code>polygon2026</code></div>
</form>`;
    const form = document.getElementById('login-form'), err = document.getElementById('error'), btn = document.getElementById('submit');
    form.onsubmit = e => {
      e.preventDefault();
      err.hidden = true;
      btn.disabled = true;
      btn.textContent = 'Проверяем…';
      const login = form.login.value.trim(), pass = form.password.value;
      setTimeout(() => {
        btn.disabled = false;
        btn.textContent = 'Войти';
        if (login === 'student' && pass === 'polygon2026') {
          location.href = `cabinet.html?user=${encodeURIComponent(login)}&token=${token(login)}`;
        } else {
          err.textContent = 'Неверный логин или пароль';
          err.hidden = false;
        }
      }, 700);
    };
  },

  cabinet() {
    const user = param('user');
    if (!user || param('token') !== token(user)) {
      document.title = 'Нужен вход — Новости Полигона';
      app.innerHTML = '<p class="empty">Сначала войдите: <a href="login.html">страница входа</a>.</p>';
      return;
    }
    document.title = 'Личный кабинет — Новости Полигона';
    const grades = [['Методы сбора данных', 5], ['Базы данных', 4], ['Английский язык', 5], ['Физкультура', 3]];
    app.innerHTML = `
<div class="cabinet">
  <h1 class="cabinet__hello">Привет, ${esc(user)}!</h1>
  <p>Ваш секретный код: <b id="secret">SEL-4729</b></p>
  <h2 class="section-title">Мои оценки</h2>
  <table id="grades" class="table">
    <tr><th>Предмет</th><th>Оценка</th></tr>
    ${grades.map(([s, g]) => `<tr><td>${s}</td><td class="grade">${g}</td></tr>`).join('')}
  </table>
  <p><a id="logout" href="login.html">Выйти</a></p>
</div>`;
  },

  calc() {
    document.title = 'Калькулятор — Новости Полигона';
    app.innerHTML = `
<div class="calc">
  <h1>Калькулятор</h1>
  <form id="calc-form" class="calc__row" onsubmit="return false">
    <input id="a" name="a" type="number" placeholder="первое число">
    <select id="op" name="op">
      <option value="add">плюс</option>
      <option value="sub">минус</option>
      <option value="mul">умножить</option>
      <option value="div">разделить</option>
    </select>
    <input id="b" name="b" type="number" placeholder="второе число">
    <button id="eq" class="btn primary" type="button">=</button>
  </form>
  <p class="calc__result">Ответ: <span id="result"></span></p>
  <h2 class="section-title">История</h2>
  <ul id="history"></ul>
</div>`;
    const res = document.getElementById('result');
    document.getElementById('eq').onclick = () => {
      const a = parseFloat(document.getElementById('a').value), b = parseFloat(document.getElementById('b').value);
      const op = document.getElementById('op');
      res.textContent = 'считаем…';
      setTimeout(() => {
        let out;
        if (isNaN(a) || isNaN(b)) out = 'Ошибка: введите два числа';
        else if (op.value === 'div' && b === 0) out = 'Ошибка: деление на ноль';
        else {
          const v = { add: a + b, sub: a - b, mul: a * b, div: a / b }[op.value];
          out = String(Math.round(v * 100) / 100);
        }
        res.textContent = out;
        document.getElementById('history').insertAdjacentHTML('afterbegin', `<li>${a} ${op.selectedOptions[0].text} ${b} = ${esc(out)}</li>`);
      }, 800);
    };
  },
};

function token(user) {
  let h = 7;
  for (const c of user + 'polygon') h = (h * 31 + c.charCodeAt(0)) % 1000003;
  return 't' + h;
}

header();
(pages[document.body.dataset.page] || pages.index)();
