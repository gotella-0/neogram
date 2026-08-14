# Examples walkthrough

The `examples/` folder contains ready-made bots. This page explains each one line by line.

## `examples/hello_world` — the basics

The simplest bot: one command and file storage for every media type.

```toml
[commands.start]
text = "Hi in bot made in NeoGram"
action = "send_text"
```

- `/start` → replies "Hi in bot made in NeoGram".

```toml
[files.photo]
actions = ["get_photo", "send_text"]
name = "test"
texts = ["Photo successfully accepted", "good multiple texts"]
```

- A photo is stored under `name = "test"`, then the bot confirms with two messages
  (`send_text` iterates `texts`).

```toml
[files.audio]
name = "test"
action = "get_audio"
```

- Audio is stored. Same pattern for `voice`, `document`, `video`, `location`, `contact`.

This example shows the whole feature matrix: one command plus storage of all seven media
types.

## `examples/test` — states, buttons, modules, media

The richest example. It has a custom module `modules/temp.py`:

```python
import random

def get_temp(message) -> str:
    return f"{message}: {random.randint(0, 10)}"
```

Imported in config:

```toml
[import.module]
temp = []
```

### Commands

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

`/arturik` sets the user's state to `"arturik"`. The state is used by the per-state
variant below.

```toml
[commands.test_photo]
action = "send_photo"
photo = "preview.jpg"
text = "Test caption"
```

`/test_photo` sends `assets/preview.jpg` with a caption.

```toml
[commands.test_format]
action = "send_text"
text = "{temp.get_temp(message.text)}"
buttons = [ [{text = "test", type="text"}, {text="test2"}] ]
```

`/test_format` calls the imported `temp.get_temp(...)` function (see the f-string
evaluation) and renders a reply keyboard with two buttons.

### Per-state command variant

```toml
[commands.test_format.state.arturik]
action = "send_photo"
photo = "preview.jpg"
text = "{temp.get_temp(message.text)}"
buttons = [ [{text = "test", type="text"}, {text="test2"}] ]
```

While the user is in state `"arturik"`, `/test_format` sends a photo instead of text.

### A menu with states

```toml
[commands.send_menu]
action = "send_text"
set_state = "menuProfile"
text = "It's test menu with states"
buttons = [ [{text = "Profile", type="text"}, {text="Help"}] ]
```

`/send_menu` shows a reply keyboard **Profile / Help** and sets state `"menuProfile"`.

```toml
[messages.Profile.state.menuProfile]
set_state = "menuProfile"
action = "send_text"
text = "It's profile"
buttons = [ [{text = "Back", type="text"}] ]
```

While in `"menuProfile"`, pressing **Profile** replies "It's profile" with a **Back**
button.

```toml
[messages.Back.state.menuProfile]
action = "send_text"
text = "It's test menu with states"
buttons = [ [{text = "Profile", type="text"}, {text="Help"}] ]
```

Pressing **Back** returns to the menu.

```toml
[messages.Help.state.menuProfile]
set_state = "menuProfile"
text = "This is help menu"
action = "send_text"
buttons = [ [{text = "Back", type="text"}] ]
```

Pressing **Help** shows the help text with a **Back** button.

### Echo

```toml
[commands.resend]
action = "resend_message"
```

`/resend` echoes the user's message back.

```toml
[messages.start]
action = "resend_message"
```

Any message equal to `"start"` is echoed back.

> Note: `messages.start` is the literal message text `start`, while `commands.start` is
> the command `/start`. They are matched independently.

## `examples/test1` — minimal state machine

A tiny example focused on states:

```toml
[commands.start]
text = "Hi in bot made in NeoGram"
action = "send_text"
set_state = "pressed"
```

`/start` replies and sets state `"pressed"`.

```toml
[commands.check.state.pressed]
text = "State sucessfully checked!"
action = "send_text"
```

While the user is in state `"pressed"`, `/check` replies "State successfully checked!".

This is the minimal pattern for state-dependent behavior.

## Related

- [Getting started](getting-started.md) — build your own bot.
- [States](states.md), [Buttons](buttons.md), [Actions](actions.md) — the features used
  above.