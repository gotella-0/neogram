# Действия отправки

`action` (или несколько в `actions`) говорит NeoGram, что делать при срабатывании
обработчика. Действия соответствуют методам `Api`. Эта страница описывает каждое
действие.

## Как работают действия

```toml
[commands.start]
action = "send_text"
text = "Hello!"
```

NeoGram ищет имя действия как метод на `Api` и вызывает его с сообщением и конфигом
обработчика. Если действие отсутствует, используется `actions` (массив), и каждое
пробуется по очереди.

## `send_text`

Отправляет текстовое сообщение. Использует `text` (одно) или `texts` (несколько —
по одному сообщению каждое). Текст вычисляется как f-строка, поэтому можно
подставлять переменные.

```toml
[commands.start]
action = "send_text"
text = "Hello, {message.from_user.first_name}!"
```

Несколько сообщений:

```toml
[commands.info]
action = "send_text"
texts = ["First message", "Second message"]
```

Отрисовывает клавиатуру из `buttons` (если есть).

## `send_photo`

Отправляет фото из папки `assets/` проекта с необязательной подписью.

```toml
[commands.pic]
action = "send_photo"
photo = "preview.jpg"
text = "Here is the preview"
```

- `photo` — имя файла внутри `assets/`.
- `text` — подпись (поддерживается f-строка).

## `send_document`

Отправляет документ из `assets/`. Поддерживает один документ или список.

```toml
[commands.file]
action = "send_document"
document = { name = "report.pdf", text = "Your report" }
```

Несколько документов:

```toml
[commands.files]
action = "send_document"
documents = [ { name = "a.pdf", text = "Doc A" }, { name = "b.pdf", text = "Doc B" } ]
```

## `edit_text`

Редактирует существующее сообщение (работает в обработчиках колбэков, где сообщение
для редактирования — то, к которому прикреплена кнопка).

```toml
[callbacks.next]
action = "edit_text"
text = "Updated text"
```

Для колбэков редактирует сообщение, к которому прикреплена кнопка; для команд —
последнее сообщение пользователя.

## `resend_message`

Пересылает пользователю то, что он отправил (текст, фото или документ).

```toml
[commands.resend]
action = "resend_message"
```

Полезно для эхо-ботов.

## Цепочка действий `actions`

Несколько действий выполняются по порядку:

```toml
[files.photo]
name = "test"
actions = ["get_photo", "send_text"]
texts = ["Photo successfully accepted"]
```

`get_photo` сохраняет файл, затем `send_text` подтверждает приём.

## Справочная таблица

| Действие | Параметры | Описание |
|----------|-----------|----------|
| `send_text` | `text` / `texts` | Отправка текстового сообщения. |
| `send_photo` | `photo`, `text` | Отправка фото из `assets/` с подписью. |
| `send_document` | `document` / `documents` | Отправка документа(ов) из `assets/`. |
| `edit_text` | `text` | Редактирование существующего сообщения. |
| `resend_message` | — | Эхо-ответ пользователю. |
| `get_photo` | `name`, `owner` | Сохранение входящего фото. |
| `get_audio` | `name`, `owner` | Сохранение входящего аудио. |
| `get_voice` | `name`, `owner` | Сохранение входящего голосового. |
| `get_document` | `name`, `owner` | Сохранение входящего документа. |
| `get_video` | `name`, `owner` | Сохранение входящего видео. |
| `get_location` | `name`, `owner` | Сохранение входящей локации. |
| `get_contact` | `name`, `owner` | Сохранение входящего контакта. |

## Связанное

- [Конфигурация](configuration.md) — поля обработчика.
- [Файлы и медиа](files-media.md) — действия `get_*` подробно.
- [Справочник API](api-reference.md) — полные сигнатуры методов.