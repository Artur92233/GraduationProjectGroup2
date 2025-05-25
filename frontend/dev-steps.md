# ✅ План розробки фронтенду для платформи нерухомості (HTML/CSS/JS)

## 🎯 Мета

Створити фронтенд для платформи нерухомості, використовуючи HTML/CSS (Tailwind або чистий CSS) та JavaScript (fetch, WebSocket), з підключенням до мікросервісів: Auth, Apartment, Favorites, Chat, File, Notification.

Дизайн натхненний **головною сторінкою ЛУН**, але реалізований без React.

## 🛠️ Технології

* **HTML/CSS** — структура та стилі
* **Tailwind CSS** *(опціонально)* — для швидкої розробки стилів
* **JavaScript** — fetch-запити до API, WebSocket (через socket.io-client)
* **Socket.IO** — чат
* **Jest** — для тестування
* **GitHub Actions** — CI/CD

## 🔁 Мапінг функціоналу ЛУН

| Елемент ЛУН        | Замінено на        |
|--------------------|--------------------|
| ЛУН Статистика     | Аналітика ринку    |
| ЖИТЛУН             | Блог               |
| Новобудови         | Фільтр seller_type=developer |
| Оренда             | Фільтр operation_type=rent   |
| Вторинка           | Фільтр seller_type=owner     |
| Обране             | Favorites Service  |
| Мій кабінет        | Профіль користувача |
| Чат                | Chat Service       |

## 👨‍💻 Роль фронтенд-розробника

Реалізувати:
* Головну сторінку з пошуком та фільтрами
* Особистий кабінет
* Сторінку "Обране"
* Статичні сторінки "Аналітика" та "Блог"
* Інтеграцію з API
* Тести, документацію, PR з рев’ю

---

## 📌 Завдання для фронтенду

### 🧩 Задача 1: Головна сторінка з пошуком

**Файли:**
* `frontend/index.html`
* `frontend/scripts/search.js`
* `frontend/tests/search.test.js`
* `docs/frontend/search.md`

**Функціонал:**
* Форма пошуку: місто, ціна, кімнати, валюта, тип операції, продавець, ремонт, розстрочка
* Запит `POST /apartments/search` (Apartment Service, ID: `3f415176-0590-4b34-ad42-a5f6a4c1d08f`)
* Відображення результатів у `<div>`-картках
* Навігація:
  * Каталог новобудов → `seller_type=developer`
  * Оренда квартир → `operation_type=rent`
  * Вторинний ринок → `seller_type=owner`
  * Аналітика ринку → `analytics.html`
  * Блог → `blog.html`
  * Обране → `favorites.html`
  * Мій кабінет → `profile.html`

**Тести:**
* Jest: перевірка форми, API-запиту, відображення карток (mock через msw)

---

### 👤 Задача 2: Сторінка особистого кабінету

**Файли:**
* `frontend/profile.html`
* `frontend/scripts/profile.js`
* `frontend/tests/profile.test.js`
* `docs/frontend/profile.md`

**Функціонал:**
* Профіль (username, email)
* Список анкет
* Форма для нової анкети (ApartmentCreate, ID: `a8ff17d3-fbc9-453b-b06a-d54ed8b02ba0`)

**Ендпоінти:**
* `GET /users/me` (Auth Service, ID: `6676805c-6305-4426-ad72-9731fa91f864`)
* `GET /users/me/apartments` (Auth Service)
* `POST /apartments` (Apartment Service)

**Тести:**
* Jest: рендеринг сторінки, помилки (401, 404)

---

### ⭐ Задача 3: Сторінка "Обране"

**Файли:**
* `frontend/favorites.html`
* `frontend/scripts/favorites.js`
* `frontend/scripts/search.js` (додати `addToFavorites`)
* `frontend/tests/favorites.test.js`
* `docs/frontend/favorites.md`

**Функціонал:**
* Перегляд обраних квартир
* Кнопка "Додати до обраного" на головній сторінці
* Можливість видалити квартиру з обраного

**Ендпоінти:**
* `GET /favorites` (Favorites Service, ID: `51eb017c-6a2d-44c5-83a7-777f73d8c595`)
* `POST /favorites/{apartment_id}`
* `DELETE /favorites/{apartment_id}`

---

## 📘 Структура репозиторію