# Ledger

Ledger - учебное desktop-приложение для управления банковскими аккаунтами и транзакциями. 
Проект сделан для практики архитектуры на Python, паттерна Repository, 
работы с SQLite, PostgreSQL, PySide6, pytest и CI.

## Возможности

- Создание аккаунтов
- Пополнение баланса
- Снятие средств
- Переводы между аккаунтами
- Просмотр списка аккаунтов
- Просмотр истории транзакций
- Графический интерфейс
- Несколько вариантов хранения данных:
  - In-memory
  - SQLite
  - PostgreSQL

## Технологии

- Python 3.11+
- PySide6
- SQLite
- PostgreSQL
- psycopg
- pytest
- uv
- just
- GitHub Actions

## Архитектура

Слои проекта:

    GUI
      |
     \./
    Ledger / Service layer
      |
     \./
    LedgerRepository interface
      |
     \./
    InMemoryRepository / SQLiteRepository / PostgresRepository

`Ledger` содержит основную бизнес-логику приложения и не знает, где именно хранятся данные.

`LedgerRepository` описывает общий контракт для хранилища данных.

Благодаря этому разные реализации репозитория можно заменять без изменения бизнес-логики:

- `InMemoryRepository` хранит данные в Python-объектах
- `SQLiteRepository` хранит данные в локальной SQLite-базе
- `PostgresRepository` хранит данные в PostgreSQL


## Структура проекта

```
.
├── account.py
├── gui
│   └── window.py
├── justfile
├── ledger.py
├── main.py
├── operations.py
├── parser.py
├── pyproject.toml
├── README.md
├── repositories
│   ├── base.py
│   ├── in_memory_repository.py
│   ├── postgres_repository.py
│   └── sqlite_repository.py
├── sql
│   ├── schema_postgres.sql
│   └── schema.sql
├── tests/
├── transaction.py
└── uv.lock
```

## Установка

Клонировать репозиторий:

    git clone <repo-url>
    cd <project-directory>

Установить базовые зависимости для разработки:

    uv sync --dev

Установить зависимости для GUI:

    uv sync --group gui

Установить зависимости для PostgreSQL:

    uv sync --group postgres

Установить всё для локальной разработки:

    uv sync --dev --group gui --group postgres

## Запуск

Запуск с SQLite:

    just run --storage sqlite

Запуск с конкретным путём к SQLite-базе:

    just run --storage sqlite --db-path database.db

Запуск с хранением данных в памяти:

    just run --storage memory

Запуск с демо-данными:

    just run --demo

Запуск с хранением в памяти и демо-данными:

    just run --storage memory --demo

## Настройка PostgreSQL

Для работы с PostgreSQL нужен запущенный сервер PostgreSQL.

Пример базы для обычного запуска:

- база данных: `ledger`
- пользователь: `ledger_user`

Создай локальный файл с примером содержимого:

    export POSTGRES_DB=ledger
    export POSTGRES_USER=ledger_user
    export POSTGRES_PASSWORD=your_password
    export POSTGRES_HOST=localhost
    export POSTGRES_PORT=5432

Этот файл не должен попадать в git.

Добавь его в `.gitignore`:

    postgres.dev.env.sh
    postgres.test.env.sh

Запуск с PostgreSQL:

    just run --storage postgres

## Тестирование

Запуск тестов:

    just test

Или напрямую:

    uv run pytest

Тесты проверяют:

- поведение `Ledger`
- общий контракт репозиториев
- работу in-memory хранилища
- работу SQLite-хранилища
- работу PostgreSQL-хранилища
- историю транзакций
- сохранение данных в базе
- конвертацию enum-типов
- конвертацию даты и времени

## PostgreSQL в тестах

Для тестов PostgreSQL должна использоваться отдельная тестовая база.

Пример:

- база данных: `ledger_test`
- пользователь: `ledger_user`

Создай файл с примером содержимого:

    export POSTGRES_DB=ledger_test
    export POSTGRES_USER=ledger_user
    export POSTGRES_PASSWORD=your_password
    export POSTGRES_HOST=localhost
    export POSTGRES_PORT=5432

Важно: тесты могут очищать таблицы, поэтому не стоит использовать рабочую базу данных для тестов.

## CI

Проект использует GitHub Actions.

CI выполняет следующие шаги:

- получает код репозитория
- устанавливает Python
- устанавливает uv
- устанавливает зависимости для тестов
- запускает временный PostgreSQL service container
- запускает pytest

PostgreSQL-база в CI временная. Она создаётся только на время проверки и не связана с локальной базой разработчика.

## Схема базы данных

### accounts

| Колонка | Тип | Описание |
|---|---|---|
| id | integer | Первичный ключ |
| owner | text | Владелец аккаунта |
| balance | integer | Текущий баланс аккаунта |

### transactions

| Колонка | Тип | Описание |
|---|---|---|
| id | integer | Первичный ключ |
| type | text | Тип транзакции |
| amount | integer | Сумма транзакции |
| from_account_id | integer / null | Аккаунт-источник |
| to_account_id | integer / null | Аккаунт-получатель |
| created_at | timestamp / text | Время создания транзакции |

## Заметки по разработке

- GUI не обращается к базе данных напрямую.
- GUI работает через `Ledger`.
- `Ledger` работает через интерфейс `LedgerRepository`.
- `TransactionType` хранится в базе данных как текст.
- SQLite хранит `created_at` как ISO-строку.
- PostgreSQL использует отдельную SQL-схему.
- Разные реализации репозитория проверяются одними и теми же тестами поведения.

## Планы

- [ ] Добавить Ruff
- [ ] Добавить mypy
- [ ] Улучшить внешний вид GUI
- [ ] Улучшить обработку ошибок в GUI
- [ ] Добавить фильтрацию транзакций
- [ ] Добавить экспорт транзакций в CSV
- [ ] Добавить миграции базы данных
- [ ] Добавить инструкции по сборке приложения

## Лицензия

Учебный проект.