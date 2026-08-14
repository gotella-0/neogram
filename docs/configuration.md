# Configuration (`config.toml`)

A NeoGram project is described entirely by `config.toml` in the project folder. This page
is the full reference.

## Top-level keys

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `name_project` | string | yes | Project name. Also used as the database name. |
| `bot_token` | string | yes | Token from [@BotFather](https://t.me/BotFather). |
| `admins` | array of ints | yes | Telegram user ids of the admins. |
| `database` | table | yes | Database connection, see below. |
| `commands` | table | no | Command handlers (`/command`). |
| `messages` | table | no | Plain-text message handlers. |
| `callbacks` | table | no | Inline-button callback handlers. |
| `files` | table | no | File-type handlers (photo, audio, ...). |
| `patterns` | table | no | Reusable text patterns, see below. |
| `import` | table | no | Custom modules and extra logic files, see below. |

## `[database]`

| Key | Type | Description |
|-----|------|-------------|
| `type` | string | `mysql` or `sqlite`. |
| `host` | string | MySQL host (empty for SQLite). |
| `login` | string | MySQL user (empty for SQLite). |
| `password` | string | MySQL password (empty for SQLite). |
| `port` | string | MySQL port (empty for SQLite). |

Example for MySQL:

```toml
[database]
type = "mysql"
host = "localhost"
login = "neogram"
password = "password"
port = "3306"
```

Example for SQLite:

```toml
[database]
type = "sqlite"
host = ""
login = ""
password = ""
port = ""
```

## `[commands]`

Each key is the command text **without** the leading slash. The handler responds to
`/command`.

```toml
[commands.start]
text = "Hello!"
action = "send_text"
```

The simplest handler needs at least an `action`. The action name maps to a method of
`Api` — see [actions](actions.md).

Other handler fields:

| Key | Type | Description |
|-----|------|-------------|
| `text` / `texts` | string / array | Text to send with `send_text`. |
| `action` / `actions` | string / array | Action method(s) to call. |
| `set_state` | string | State to set after handling (see [states](states.md)). |
| `state` | table | Per-state handlers (see [states](states.md)). |
| `buttons` | array | Keyboard definition (see [buttons](buttons.md)). |
| `photo`, `document` | string | Asset path for `send_photo` / `send_document`. |

## `[messages]`

The same handler schema, but the key is matched against the raw message text.

```toml
[messages.Help]
action = "send_text"
text = "Help menu"
```

## `[callbacks]`

The same handler schema, but the key is matched against `callback_data` of an inline
button press.

```toml
[callbacks.hello]
action = "send_text"
text = "You pressed the button!"
```

## `[files]`

The key is a media type. Available types: `photo`, `audio`, `voice`, `document`, `video`,
`location`, `contact`.

```toml
[files.photo]
name = "test"
action = "get_photo"
```

See [files & media](files-media.md) for details.

## `[patterns]`

NeoGram replaces the string `'pattern': 'name'` inside any handler with the pattern value
before parsing. This lets you reuse a constant in multiple places.

```toml
[patterns]
main_menu = "'text': 'Main menu'"
```

```toml
[commands.start]
'pattern': 'main_menu'
action = "send_text"
```

> Note: `_check_patterns` performs a textual replacement, then `eval`s the resulting
> Python literal. Keep the replacement value a valid Python literal.

## `[import]`

### Custom Python modules

Files placed in `project/modules/` are imported and made available in `eval` context
under their module name.

```toml
[import.module]
temp = []
```

```python
# modules/temp.py
def get_temp(text: str) -> str:
    return f"{text}: processed"
```

Then use it in a handler:

```toml
[commands.process]
action = "send_text"
text = "{temp.get_temp(message.text)}"
```

> Important: modules are imported with `__import__(i)` from `sys.path`; the `modules/`
> folder is inserted at path index 1. Unique module names are required.

### Additional logic files

You can split the bot logic into additional TOML files next to `config.toml`. The keys
`commands`, `messages`, `callbacks`, `files`, `patterns` from those files are merged into
the main config.

```toml
[import.logic]
admin = []
```

This merges `admin.toml` from the project folder. Such a file uses the same schema as
`config.toml` (without the top-level keys).

## Full minimal example

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

## Next steps

- [States](states.md) — multi-step dialogs.
- [Buttons](buttons.md) — keyboards.
- [Actions](actions.md) — all send actions.