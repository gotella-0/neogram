# Файлы и медиа

NeoGram умеет принимать от пользователей медиа и сохранять его. Обработка файлов
настраивается в таблице `[files]` по типу медиа. Доступные типы: `photo`, `audio`,
`voice`, `document`, `video`, `location`, `contact`.

## Приём файла

Каждый обработчик файла требует `name` (имя, под которым сохраняется медиа) и действие
из семейства `get_*`:

```toml
[files.photo]
name = "avatar"
action = "get_photo"
```

Когда пользователь отправляет фото, NeoGram сохраняет его `file_id` в таблицу `media`
под именем `name = "avatar"`, типом `photo` и владельцем — пользователем.

## Действия по типам

| Тип медиа | Действие | Сохраняемое значение |
|-----------|----------|----------------------|
| photo | `get_photo` | `file_id` фото |
| audio | `get_audio` | `file_id` аудио |
| voice | `get_voice` | `file_id` голосового |
| document | `get_document` | `file_id` документа |
| video | `get_video` | `file_id` видео |
| location | `get_location` | объект локации |
| contact | `get_contact` | объект контакта |

## Поле `owner`

По умолчанию медиа сохраняется с владельцем `"0"`. Можно задать `owner`, чтобы
привязать медиа к конкретному id пользователя (или к вычисляемому значению):

```toml
[files.photo]
name = "selfie"
action = "get_photo"
owner = "{message.from_user.id}"
```

## Несколько действий

Как и другие обработчики, файлы поддерживают массив `actions`. Частый паттерн —
сохранить файл **и** подтвердить приём:

```toml
[files.photo]
name = "test"
actions = ["get_photo", "send_text"]
texts = ["Photo successfully accepted", "Good, multiple texts"]
```

Здесь `get_photo` сохраняет файл, затем `send_text` отвечает каждым текстом из `texts`.

## Таблица `media`

Сохранённое медиа находится в таблице `media`:

```sql
CREATE TABLE media (
  name TEXT,
  type TEXT,
  file_id TEXT,
  owner BIGINT,
  CONSTRAINT MediaObject UNIQUE (name, type, owner)
);
```

`file_id` — стабильный id Telegram, поэтому позже медиа можно отправить обратно через
`bot.send_photo(photo=file_id)` и т.п. Методы `Database.get_media` / `Database.add_media`
доступны в контексте `eval` как `database`.

## Сочетание с кнопками локации/телефона

Reply-кнопки `geolocation` и `phone_number` запускают обработчики `[files.location]`
и `[files.contact]` соответственно. См. [кнопки](buttons.md).

## Связанное

- [Конфигурация](configuration.md#files) — справочник `[files]`.
- [Действия](actions.md) — отправка медиа пользователю.
- [Справочник API](api-reference.md) — методы `get_*`.