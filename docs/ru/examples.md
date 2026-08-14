# Разбор примеров

В папке `examples/` лежат готовые боты. На этой странице каждый разобран построчно.

## `examples/hello_world` — основы

Простейший бот: одна команда и сохранение файлов для всех типов медиа.

```toml
[commands.start]
text = "Hi in bot made in NeoGram"
action = "send_text"
```

- `/start` → отвечает "Hi in bot made in NeoGram".

```toml
[files.photo]
actions = ["get_photo", "send_text"]
name = "test"
texts = ["Photo successfully accepted", "good multiple texts"]
```

- Фото сохраняется под именем `name = "test"`, затем бот подтверждает приём двумя
  сообщениями (`send_text` перебирает `texts`).

```toml
[files.audio]
name = "test"
action = "get_audio"
```

- Аудио сохраняется. Тот же паттерн для `voice`, `document`, `video`, `location`,
  `contact`.

Этот пример показывает всю матрицу возможностей: одна команда плюс сохранение всех
семи типов медиа.

## `examples/test` — состояния, кнопки, модули, медиа

Самый насыщенный пример. В нём кастомный модуль `modules/temp.py`:

```python
import random

def get_temp(message) -> str:
    return f"{message}: {random.randint(0, 10)}"
```

Импорт в конфиге:

```toml
[import.module]
temp = []
```

### Команды

```toml
[commands.start]
text = "Hi in bot made in NeoGram"
action = "send_text"
```

```toml
[commands.help]
text = "This is help menu"
action = "send_text"
```

```toml
[commands.arturik]
text = "Hi, Arturik. Я поставил состояние пользователя"
action = "send_text"
set_state = "arturik"
```

`/arturik` устанавливает состояние пользователя в `"arturik"`. Состояние используется
вариантом ниже.

```toml
[commands.test_photo]
action = "send_photo"
photo = "preview.jpg"
text = "Test caption"
```

`/test_photo` отправляет `assets/preview.jpg` с подписью.

```toml
[commands.test_format]
action = "send_text"
text = "{temp.get_temp(message.text)}"
buttons = [ [{text = "test", type="text"}, {text="test2"}] ]
```

`/test_format` вызывает импортированную функцию `temp.get_temp(...)` (см. вычисление
f-строки) и рисует reply-клавиатуру с двумя кнопками.

### Вариант команды по состоянию

```toml
[commands.test_format.state.arturik]
action = "send_photo"
photo = "preview.jpg"
text = "{temp.get_temp(message.text)}"
buttons = [ [{text = "test", type="text"}, {text="test2"}] ]
```

Пока пользователь в состоянии `"arturik"`, `/test_format` отправляет фото вместо текста.

### Меню с состояниями

```toml
[commands.send_menu]
action = "send_text"
set_state = "menuProfile"
text = "It's test menu with states"
buttons = [ [{text = "Profile", type="text"}, {text="Help"}] ]
```

`/send_menu` показывает reply-клавиатуру **Profile / Help** и ставит состояние
`"menuProfile"`.

```toml
[messages.Profile.state.menuProfile]
set_state = "menuProfile"
action = "send_text"
text = "It's profile"
buttons = [ [{text = "Back", type="text"}] ]
```

Пока в `"menuProfile"`, нажатие **Profile** отвечает "It's profile" с кнопкой **Back**.

```toml
[messages.Back.state.menuProfile]
action = "send_text"
text = "It's test menu with states"
buttons = [ [{text = "Profile", type="text"}, {text="Help"}] ]
```

Нажатие **Back** возвращает в меню.

```toml
[messages.Help.state.menuProfile]
set_state = "menuProfile"
text = "This is help menu"
action = "send_text"
buttons = [ [{text = "Back", type="text"}] ]
```

Нажатие **Help** показывает справку с кнопкой **Back**.

### Эхо

```toml
[commands.resend]
action = "resend_message"
```

`/resend` пересылает пользователю его сообщение.

```toml
[messages.start]
action = "resend_message"
```

Любое сообщение, равное `"start"`, пересылается обратно.

> Примечание: `messages.start` — это буквальный текст `start`, а `commands.start` —
> команда `/start`. Они сопоставляются независимо.

## `examples/test1` — минимальный конечный автомат

Маленький пример, сфокусированный на состояниях:

```toml
[commands.start]
text = "Hi in bot made in NeoGram"
action = "send_text"
set_state = "pressed"
```

`/start` отвечает и ставит состояние `"pressed"`.

```toml
[commands.check.state.pressed]
text = "State sucessfully checked!"
action = "send_text"
```

Пока пользователь в состоянии `"pressed"`, `/check` отвечает "State successfully checked!".

Это минимальный паттерн поведения, зависящего от состояния.

## Связанное

- [Начало работы](getting-started.md) — создание собственного бота.
- [Состояния](states.md), [Кнопки](buttons.md), [Действия](actions.md) — функции,
  использованные выше.