# 📋 Назва: [linters.yaml](..%2F..%2F.github%2Fworkflows%2Flinters.yaml)
# 🔄 Опис: Автоматичне тестування проєкту при кожному pull request.
#          Включає встановлення Python, Poetry, лінтери та запуск тестів.

name: test with poetry

# 🧪 Запускається на кожен pull request
on: pull_request

jobs:
  test:
    runs-on: ubuntu-latest  # 💻 Середовище для виконання: Ubuntu

    steps:
      # 📦 Крок 1: Клонування репозиторію
      - name: Check out repository
        uses: actions/checkout@v3

      # 🐍 Крок 2: Встановлення Python
      - name: Set up python
        id: setup-python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      # 📦 Крок 3: Встановлення Poetry
      - name: Install Poetry
        uses: snok/install-poetry@v1
        with:
          virtualenvs-create: true               # Створювати віртуальне середовище
          virtualenvs-in-project: true           # Зберігати .venv у директорії проєкту
          installer-parallel: true               # Встановлення з паралельною оптимізацією

      # 📥 Крок 4: Встановлення залежностей та інструментів для перевірки коду
      - name: Install dependencies
        run: |
          poetry init -n                         # Ініціалізація pyproject.toml, якщо не існує
          if ! grep -q 'package-mode' pyproject.toml; then
             echo '[tool.poetry]' >> pyproject.toml
             echo 'package-mode = false' >> pyproject.toml
          fi
          poetry install                         # Встановлення всіх залежностей
          poetry add black                       # Лінтер чорного стилю
          poetry add isort                       # Сортування імпортів
          poetry add flake8                      # Аналізатор коду

      # 🧪 Крок 5: Запуск тестів і перевірка стилю коду
      - name: Run tests
        run: |
          source .venv/bin/activate              # Активація віртуального середовища
          black . --check --line-length 120      # Перевірка форматування коду
          isort . --line-length 120              # Перевірка сортування імпортів
          flake8 .                               # Аналіз коду на помилки
