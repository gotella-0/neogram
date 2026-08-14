# Справочник API

На этой странице описан публичный API NeoGram. Главный класс — `Api`
(`neogram.Api`), который создаёт `run_project` и управляет всем ботом.

## `Api`

```python
from neogram import Api

api = Api(bot_token, name_project, modules, database, prefixes)
```

### Параметры конструктора

| Параметр | Тип | Описание |
|----------|-----|----------|
| `bot_token` | str | Токен от @BotFather. |
| `name_project` | str | Имя проекта (также имя БД). |
| `modules` | dict | Импортированные кастомные модули для контекста eval. |
| `database` | dict | Конфиг БД `{host, login, password, type, port}`. |
| `prefixes` | dict | Случайные префиксы по типам файлов (photo, audio, ...). |

`__init__` проверяет токен и подключается к БД (создавая её и таблицы при необходимости).

### Методы регистрации

Их вызывает `run_project` на основе распарсенного конфига. Обычно вы не вызываете их
напрямую, но они публичные.

```python
api.register_command("start", {"text": "Hi!", "action": "send_text"})
api.register_message("Hello", {"action": "send_text", "text": "Hi there"})
api.register_callback("help", {"action": "send_text", "text": "Help"})
api.register_file("photo", {"name": "test", "action": "get_photo"})
```

- `register_command(command, args)` — обработчик команды `/command`.
- `register_message(message, args)` — обработчик текстового сообщения.
- `register_callback(data, args)` — обработчик колбэка инлайн-кнопки.
- `register_file(type, args)` — обработчик типа медиа (`photo`, `audio`, ...).

Каждая регистрация строит варианты по состояниям (`_check_state`) и клавиатуру
(`_check_buttons`).

### Рантайм

```python
api.run()
```

Запускает поллинг через aiogram (`executor.start_polling(self.dp)`). Блокирует выполнение,
пока бот не остановят.

### Действия отправки (используются полем `action` конфига)

Все — `async`, вызываются с `(message, cmd)`, где `message` — апдейт Telegram, а `cmd` —
словарь конфига обработчика.

| Метод | Назначение |
|-------|------------|
| `send_text(message, cmd)` | Отправка `text` / каждого из `texts` с клавиатурой. |
| `send_photo(message, cmd)` | Отправка фото из `assets/`. |
| `send_document(message, cmd)` | Отправка документа / документов из `assets/`. |
| `edit_text(message, cmd)` | Редактирование существующего сообщения. |
| `resend_message(message, cmd)` | Эхо-ответ пользователю. |
| `get_photo(message, cmd)` | Сохранение входящего фото. |
| `get_audio(message, cmd)` | Сохранение входящего аудио. |
| `get_voice(message, cmd)` | Сохранение входящего голосового. |
| `get_document(message, cmd)` | Сохранение входящего документа. |
| `get_video(message, cmd)` | Сохранение входящего видео. |
| `get_location(message, cmd)` | Сохранение входящей локации. |
| `get_contact(message, cmd)` | Сохранение входящего контакта. |

### Обработчики (внутренние)

Низкоуровневые обработчики aiogram, которые регистрирует NeoGram:

- `handler(message)` — мультиобработчик для команд и текстовых сообщений.
- `handler_any(message)` — обработчик для специального ключа `neogram_any`.
- `callback_handler(call)` — обработка колбэков инлайн-кнопок.
- `file_handler(message)` — обработка медиа-апдейтов.

### Приватные помощники

- `set_state(command, user_id)` — установка состояния пользователя после обработки.
- `_check_state(command)` — построение вариантов обработчика по состояниям.
- `_check_buttons(command)` — построение клавиатуры для обработчика.
- `_check_type(message)` — определение, является ли апдейт командой, сообщением, файлом
  или колбэком.
- `_get_state` / `_update_state` / `_add_media` — выносят блокирующие вызовы БД в рабочие
  потоки через `asyncio.to_thread`.

## `Parser`

```python
from neogram.additions.parser import Parser

data = Parser("my_bot")
```

Читает `config.toml` и предоставляет:

- `data.commands`, `data.messages`, `data.callbacks`, `data.files` — словари обработчиков.
- `data.patterns` — текстовые паттерны.
- `data.states` — собранные состояния.
- `data.modules` — импортированные модули.
- `data.admins` — id администраторов.
- `data.database` — словарь конфига БД.
- `data.bot_token` — токен бота.

## `Database`

```python
from neogram.additions.database import Database

db = Database(name_project, host, user, passwd, database_type, port)
```

| Метод | Описание |
|-------|----------|
| `create_db()` | Создание БД (MySQL) или папки для SQLite-файла. |
| `check()` | Возвращает, существует ли БД. |
| `connect()` | Создаёт движок SQLAlchemy и подключается. |
| `create_tables()` | Создаёт таблицы `users`, `states`, `media`. |
| `del_db()` | Удаление БД (или SQLite-файла). |
| `get_state(user_id)` | Получение состояния пользователя (False, если нет). |
| `update_state(user_id, state)` | Установка состояния пользователя. |
| `delete_state(user_id)` | Очистка состояния пользователя. |
| `add_media(name, type, file_id, owner)` | Сохранение ссылки на медиа. |
| `get_media(name, type, owner)` | Получение сохранённой ссылки на медиа. |

Поддерживаемые типы БД: `mysql`, `sqlite`.

## Функции CLI (`neogram.additions.functions`)

- `create_project(name_project)` — интерактивное создание проекта и БД.
- `create_default_toml(name_project, path, database_type)` — запись `config.toml` по умолчанию.
- `run_project(name_project)` — парсинг конфига, сборка `Api`, регистрация, запуск.
- `remove_project(name_project)` — удаление папки и БД (с подтверждением).

## Связанное

- [Конфигурация](configuration.md) — как эти методы управляются через TOML.
- [Действия](actions.md) — значения `action` в конфиге, сопоставленные с методами.