# Начало работы — первый бот

Это руководство проведёт вас через создание, настройку и запуск бота на NeoGram.

## 1. Создание проекта

```bash
neogram create hello_world
```

Вас спросят о выборе базы данных:

```
[Database] Choose database (default - mysql):
1.Mysql
2.Postgresql
3.SQLite

Answer:
```

Введите `3` для SQLite (сервер не нужен) или `1` для MySQL. Для MySQL также спросят
host, port, login и password; оставьте их пустыми, чтобы использовать значения по
умолчанию (`localhost`, `3306`, `neogram`).

Команда создаёт:

```
hello_world/
├── assets/        # файлы для send_photo / send_document
├── modules/       # необязательные кастомные модули Python
└── config.toml    # логика бота
```

и саму базу данных (файл `.db` для SQLite или схему в MySQL).

## 2. Настройка бота

Откройте `hello_world/config.toml`:

```toml
name_project = "hello_world"
bot_token = "write_here_bot_api_token"
admins = [ "write_here_id",]

[database]
type = "sqlite"
host = ""
login = ""
password = ""
port = ""

[commands.start]
text = "Hi in bot made in NeoGram"
action = "send_text"
```

Замените `bot_token` на токен, полученный от [@BotFather](https://t.me/BotFather),
и укажите свой Telegram id в `admins`.

## 3. Запуск бота

```bash
neogram run hello_world
```

Отправьте `/start` вашему боту. В ответ он пришлёт:

> Hi in bot made in NeoGram

## 4. Удаление проекта

```bash
neogram remove hello_world
```

NeoGram проверяет, что папка и база данных существуют, запрашивает подтверждение
и удаляет их.

## Что произошло под капотом?

1. `Parser` читает `config.toml` и собирает команды, сообщения, колбэки, файлы,
   настройки БД и импорты.
2. Создаётся `Api` с токеном, именем проекта, модулями, конфигом БД и случайными
   префиксами для типов файлов.
3. Каждая команда/сообщение/колбэк/файл регистрируется как обработчик.
4. `Api.run()` запускает поллинг через aiogram.

## Дальше

- [Конфигурация](configuration.md) — полный справочник по `config.toml`.
- [Действия](actions.md) — все действия отправки.
- [Примеры](examples.md) — готовые боты в `examples/`.