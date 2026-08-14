# Состояния и многошаговые диалоги

Состояния позволяют строить многошаговые диалоги. Состояние — это строка, которая
хранится для каждого пользователя в таблице БД `states`. Когда обработчик срабатывает,
NeoGram узнаёт текущее состояние пользователя и выбирает подходящий вариант обработчика.

## Как работает выбор состояния

Каждый обработчик в `logic_commands` преобразуется функцией `_check_state` в:

```python
{
    "any":  <сам обработчик>,
    "<state1>": <вариант обработчика для state1>,
    "<state2>": <вариант обработчика для state2>,
    ...
}
```

Когда приходит сообщение/команда/колбэк, NeoGram:

1. Получает текущее состояние пользователя (`get_state` из БД).
2. Если существует вариант для этого состояния — использует его.
3. Иначе возвращается к `"any"`.

## Установка состояния: `set_state`

После выполнения обработчика можно переключить пользователя в новое состояние через
`set_state`:

```toml
[commands.start]
text = "Welcome! Choose an option:"
action = "send_text"
set_state = "menu"
```

Теперь этот пользователь находится в состоянии `"menu"`.

## Варианты по состояниям: `state.<name>`

Можно задать разное поведение **одного и того же** обработчика в зависимости от
состояния пользователя. Синтаксис: `[commands.<name>.state.<state_name>]`:

```toml
[commands.start]
text = "You are in the default state"
action = "send_text"

[commands.start.state.pressed]
text = "You already pressed start!"
action = "send_text"
```

Здесь пользователь в состоянии `"pressed"`, отправив `/start`, получит второй текст
вместо первого.

## Полный двухшаговый диалог

```toml
[commands.start]
text = "What is your name?"
action = "send_text"
set_state = "await_name"

[messages.await_name.state.await_name]
action = "send_text"
text = "Nice to meet you!"
set_state = "done"

[messages.done.state.done]
action = "send_text"
text = "We already know your name :)"
```

Разберём по шагам:

1. Пользователь отправляет `/start` → NeoGram отвечает "What is your name?" и
   устанавливает состояние `"await_name"`.
2. Пользователь пишет любое сообщение → обработчик `[messages.await_name]` существует
   только для состояния `"await_name"`, поэтому он срабатывает только пока пользователь
   в этом состоянии. Он отвечает и ставит состояние `"done"`.
3. Пользователь отправляет ещё одно сообщение → срабатывает обработчик
   `[messages.done]` (состояние `"done"`) и отвечает.

> Совет: так как варианты сопоставляются по состоянию, обработчик, определённый только
> под конкретным `state.<name>`, в других состояниях просто ничего не делает — не нужно
> ничего проверять вручную.

## Хранение состояний

Состояния хранятся в таблице `states`:

```sql
CREATE TABLE states (user_id BIGINT PRIMARY KEY, state TEXT);
```

Методы `Database.get_state` / `Database.update_state` / `Database.delete_state` доступны
в контексте `eval` как `database`, поэтому кастомные модули могут читать и писать
состояния напрямую.

## Связанное

- [Кнопки](buttons.md) — сочетайте состояния с клавиатурами для меню.
- [Конфигурация](configuration.md) — справочник полей обработчика.
- [Справочник API](api-reference.md) — `set_state`, `_check_state`.