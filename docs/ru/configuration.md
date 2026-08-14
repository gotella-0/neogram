# Конфигурация (`config.toml`)

Проект NeoGram полностью описывается файлом `config.toml` в папке проекта. Эта страница —
полный справочник.

## Верхнеуровневые ключи

| Ключ | Тип | Обязательный | Описание |
|------|-----|-------------|----------|
| `name_project` | строка | да | Имя проекта. Также используется как имя БД. |
| `bot_token` | строка | да | Токен от [@BotFather](https://t.me/BotFather). |
| `admins` | массив чисел | да | Telegram id администраторов. |
| `database` | таблица | да | Подключение к БД, см. ниже. |
| `commands` | таблица | нет | Обработчики команд (`/command`). |
| `messages` | таблица | нет | Обработчики текстовых сообщений. |
| `callbacks` | таблица | нет | Обработчики колбэков инлайн-кнопок. |
| `files` | таблица | нет | Обработчики файлов (photo, audio, ...). |
| `patterns` | таблица | нет | Переиспользуемые текстовые паттерны, см. ниже. |
| `import` | таблица | нет | Кастомные модули и доп. логика, см. ниже. |

## `[database]`

| Ключ | Тип | Описание |
|------|-----|----------|
| `type` | строка | `mysql` или `sqlite`. |
| `host` | строка | MySQL host (пусто для SQLite). |
| `login` | строка | MySQL пользователь (пусто для SQLite). |
| `password` | строка | MySQL пароль (пусто для SQLite). |
| `port` | строка | MySQL порт (пусто для SQLite). |

Пример для MySQL:

```toml
[database]
type = "mysql"
host = "localhost"
login = "neogram"
password = "password"
port = "3306"
```

Пример для SQLite:

```toml
[database]
type = "sqlite"
host = ""
login = ""
password = ""
port = ""
```

## `[commands]`

Каждый ключ — это текст команды **без** ведущего слэша. Обработчик отвечает на
`/command`.

```toml
[commands.start]
text = "Hello!"
action = "send_text"
```

Простейший обработчик требует как минимум `action`. Имя действия соответствует методу
`Api` — см. [действия](actions.md).

Прочие поля обработчика:

| Ключ | Тип | Описание |
|------|-----|----------|
| `text` / `texts` | строка / массив | Текст для отправки через `send_text`. |
| `action` / `actions` | строка / массив | Метод(ы)-действия. |
| `set_state` | строка | Состояние, которое установится после обработки (см. [состояния](states.md)). |
| `state` | таблица | Обработчики по состояниям (см. [состояния](states.md)). |
| `buttons` | массив | Определение клавиатуры (см. [кнопки](buttons.md)). |
| `photo`, `document` | строка | Путь к ассету для `send_photo` / `send_document`. |

## `[messages]`

Та же схема обработчика, но ключ сопоставляется с сырым текстом сообщения.

```toml
[messages.Help]
action = "send_text"
text = "Help menu"
```

## `[callbacks]`

Та же схема обработчика, но ключ сопоставляется с `callback_data` при нажатии
инлайн-кнопки.

```toml
[callbacks.hello]
action = "send_text"
text = "You pressed the button!"
```

## `[files]`

Ключ — тип медиа. Доступные типы: `photo`, `audio`, `voice`, `document`, `video`,
`location`, `contact`.

```toml
[files.photo]
name = "test"
action = "get_photo"
```

Подробнее — в [файлы и медиа](files-media.md).

## `[patterns]`

NeoGram заменяет строку `'pattern': 'name'` внутри любого обработчика на значение
паттерна перед разбором. Это позволяет переиспользовать константу в нескольких местах.

```toml
[patterns]
main_menu = "'text': 'Main menu'"
```

```toml
[commands.start]
'pattern': 'main_menu'
action = "send_text"
```

> Примечание: `_check_patterns` выполняет текстовую замену, а затем `eval` полученного
> Python-литерала. Следите, чтобы значение замены было валидным Python-литералом.

## `[import]`

### Кастомные модули Python

Файлы в `project/modules/` импортируются и становятся доступны в контексте `eval`
под своим именем.

```toml
[import.module]
temp = []
```

```python
# modules/temp.py
def get_temp(text: str) -> str:
    return f"{text}: processed"
```

Использование в обработчике:

```toml
[commands.process]
action = "send_text"
text = "{temp.get_temp(message.text)}"
```

> Важно: модули импортируются через `__import__(i)` из `sys.path`; папка `modules/`
> вставляется в путь под индексом 1. Имена модулей должны быть уникальными.

### Дополнительные файлы логики

Логику бота можно разнести по дополнительным TOML-файлам рядом с `config.toml`. Ключи
`commands`, `messages`, `callbacks`, `files`, `patterns` из этих файлов объединяются
с основным конфигом.

```toml
[import.logic]
admin = []
```

Это объединяет `admin.toml` из папки проекта. Такой файл использует ту же схему, что
и `config.toml` (без верхнеуровневых ключей).

## Полный минимальный пример

```toml
name_project = "my_bot"
bot_token = "123456:ABC-DEF..."
admins = [ 123456789 ]

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

## Дальше

- [Состояния](states.md) — многошаговые диалоги.
- [Кнопки](buttons.md) — клавиатуры.
- [Действия](actions.md) — все действия отправки.