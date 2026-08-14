# Кнопки и клавиатуры

Клавиатуры задаются декларативно в поле `buttons` любого обработчика. NeoGram
поддерживает **inline**-клавиатуры (кнопки прикреплены к сообщению) и **reply**-
клавиатуры (кнопки в поле ввода).

## Структура

`buttons` — это список **рядов**. Каждый ряд — список кнопок.

```toml
buttons = [ [button1, button2], [button3] ]
```

- Внешний список → ряды (каждый ряд — отдельная строка).
- Внутренний список → кнопки в этом ряду.

## Inline-кнопки

Inline-кнопка имеет `type = "inline"`, `text` и `data` (значение `callback_data`,
отправляемое при нажатии):

```toml
[commands.menu]
action = "send_text"
text = "Choose:"
buttons = [ [{text = "Profile", type = "inline", data = "profile"}, {text = "Help", type = "inline", data = "help"}] ]
```

Нажатие кнопки с `data = "help"` вызывает обработчик колбэка с ключом `"help"`:

```toml
[callbacks.help]
action = "send_text"
text = "This is the help section"
```

> `data` соответствует ключу обработчика `[callbacks.<data>]`. См.
> [конфигурацию](configuration.md#callbacks).

## Reply-кнопки

Reply-кнопка имеет `type = "text"` (или не имеет типа — текст по умолчанию). Можно также
запросить у пользователя **геолокацию** или **номер телефона**.

```toml
[commands.start]
action = "send_text"
text = "Use the buttons below"
buttons = [ [{text = "Profile", type = "text"}, {text = "Help"}] ]
```

Текст reply-кнопки сопоставляется с обработчиками `[messages.<text>]`:

```toml
[messages.Profile]
action = "send_text"
text = "Your profile"
```

### Кнопки запроса локации и телефона

```toml
[commands.start]
action = "send_text"
text = "Send your location or phone:"
buttons = [ [{text = "Send location", type = "geolocation"}, {text = "Send phone", type = "phone_number"}] ]
```

- `geolocation` → запрашивает локацию пользователя (обрабатывается `[files.location]`).
- `phone_number` → запрашивает контакт пользователя (обрабатывается `[files.contact]`).

См. [файлы и медиа](files-media.md).

## Кнопки по состояниям

Так как кнопки находятся внутри обработчика, можно задать разные клавиатуры для разных
состояний через варианты `state.<name>`:

```toml
[commands.menu]
action = "send_text"
text = "Main menu"
buttons = [ [{text = "Profile", type = "text"}, {text = "Help", type = "text"}] ]

[commands.menu.state.menuProfile]
action = "send_text"
text = "Profile menu"
buttons = [ [{text = "Back", type = "text"}] ]
```

## Примечание о смешивании

Каждый ряд использует один тип клавиатуры (inline или reply), определяемый первой
кнопкой ряда. Для предсказуемого результата держите кнопки в ряду одного типа.

## Связанное

- [Действия](actions.md) — `send_text`, `send_photo` и т.д. рендерят `markup`.
- [Состояния](states.md) — сочетайте кнопки с вариантами состояний для меню.