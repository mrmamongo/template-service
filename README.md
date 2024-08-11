# Template Service 🚀

#### Используемый стек:

🐍 Python3.11  
🐍 FastAPI  
🐍 SQLAlchemy2  
🐍 Dishka
🐍 Adaptix
🐍 Pytest
🏷️ Postgres

----------------------  

# 📗 1. Установка

## При первом запуске необходимо настроить переменные окружения:

Для этого необходимо скопировать файл .env.example в .env

```bash
cp example.env env
```

### Описание ENV параметров

| Переменная | Описание |      
|------------|----------|

Примеры значений можно найти в example.env

# 📗 2. Запуск проекта

## 2.1. Запуск проекта при помощи докера

```bash
docker compose up -d
```

> флаг `--build` перебилдит текущий проект

## 2.2. Запуск проекта в виртуальном окружении Poetry (без Docker)

Ставим флаг `virtualenvs.in-project`, если хотим создавать .venv в  
текущей папки проекта (_опционально_)

```bash
poetry config virtualenvs.in-project true
```

- Активируем окружение;

```bash
poetry shell 
```

- Устанавливаем зависимости;

```bash
poetry install 
```

- Ставим pre-commit для линта кода;

```bash
pre-commit install
```

- Запускам миграции `alembic` вместе с миграцией данных;

```bash
make migrate_with_data
```

- Запускаем стек (PostgreSQL).

- Запускаем приложение

```bash
make run
```

# 📗 3. Использование

## 3.1 Запуск тестов

Обычный запуск тестов:

```bash
make test
```

Запуск тестов с включением "долгих" тестов:

```bash
make test_long
```

## 3.2 Линтеры

Запуск линтеров по всему проекту:

```bash
make lint
```

Запуск линтеров вручную через Ruff:

```bash
ruff check --fix .
ruff format
```

## 3.3 Миграции

- Генерация новой миграции

```bash
make makemigrations "migration_name"
```

- Применение миграций

```bash
make migrate
```

- Применение миграций вместе с данными. Выполняется функция `data_upgrades()` в файле миграции.

```bash
make migrate_with_data
```

- Генерация SQL файла с миграциями.

```bash
make dump_migrations
```

- Откат миграции на `n` версий назад

```bash
make downgrade -n
```

# 📗 4. Команды Makefile

```bash 
make run # Запуск приложения
make migrations_init # Инициализация нулевой миграции алембика
make makemigrations # Создание миграции алембика
make migrate # Применить миграции алембика
make migrate_with_data # Применить миграции алембика вместе с data миграциями
make downgrade # откат на одну миграцию
make test_long # Запуск тестирования с долгими тестами
make test # Запуск тестирования
make lint # Проверить файлы проекта при помощи линтера Ruff
``` 

# 📗 4. Minio

### создать bucket через интерфейс с именем assistants
### создать bucket через интерфейс с именем users