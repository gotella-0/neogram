# API reference

This page documents the public API of NeoGram. The main class is `Api`
(`neogram.Api`), which is created by `run_project` and drives the whole bot.

## `Api`

```python
from neogram import Api

api = Api(bot_token, name_project, modules, database, prefixes)
```

### Constructor parameters

| Param | Type | Description |
|-------|------|-------------|
| `bot_token` | str | Token from @BotFather. |
| `name_project` | str | Project name (also the database name). |
| `modules` | dict | Imported custom modules available in eval context. |
| `database` | dict | `{host, login, password, type, port}` database config. |
| `prefixes` | dict | Random prefixes per file type (photo, audio, ...). |

`__init__` validates the token and connects to the database (creating it and the tables
if needed).

### Registration methods

These are called by `run_project` based on the parsed config. You normally don't call
them yourself, but they are public.

```python
api.register_command("start", {"text": "Hi!", "action": "send_text"})
api.register_message("Hello", {"action": "send_text", "text": "Hi there"})
api.register_callback("help", {"action": "send_text", "text": "Help"})
api.register_file("photo", {"name": "test", "action": "get_photo"})
```

- `register_command(command, args)` — register a `/command` handler.
- `register_message(message, args)` — register a plain-text handler.
- `register_callback(data, args)` — register an inline-button callback handler.
- `register_file(type, args)` — register a media-type handler (`photo`, `audio`, ...).

Each registration builds the per-state variants (`_check_state`) and the keyboard
(`_check_buttons`).

### Runtime

```python
api.run()
```

Starts polling with aiogram (`executor.start_polling(self.dp)`). Blocks until the bot is
stopped.

### Send actions (used by the `action` config field)

All are `async` and are invoked with `(message, cmd)` where `message` is the Telegram
update and `cmd` is the handler config dict.

| Method | Purpose |
|--------|---------|
| `send_text(message, cmd)` | Send `text` / each `texts` with optional keyboard. |
| `send_photo(message, cmd)` | Send a photo from `assets/`. |
| `send_document(message, cmd)` | Send a document / documents from `assets/`. |
| `edit_text(message, cmd)` | Edit an existing message. |
| `resend_message(message, cmd)` | Echo the user's message back. |
| `get_photo(message, cmd)` | Store an incoming photo. |
| `get_audio(message, cmd)` | Store an incoming audio. |
| `get_voice(message, cmd)` | Store an incoming voice. |
| `get_document(message, cmd)` | Store an incoming document. |
| `get_video(message, cmd)` | Store an incoming video. |
| `get_location(message, cmd)` | Store an incoming location. |
| `get_contact(message, cmd)` | Store an incoming contact. |

### Handlers (internal)

These are the low-level aiogram handlers that NeoGram registers:

- `handler(message)` — the multi-handler for commands and plain messages.
- `handler_any(message)` — handler for the special `neogram_any` fallback key.
- `callback_handler(call)` — handles inline-button callbacks.
- `file_handler(message)` — handles media updates.

### Private helpers

- `set_state(command, user_id)` — set the user's state after handling.
- `_check_state(command)` — build per-state variants of a handler.
- `_check_buttons(command)` — build the keyboard markup for a handler.
- `_check_type(message)` — detect whether an update is a command, message, file or
  callback.
- `_get_state` / `_update_state` / `_add_media` — offload blocking DB calls to worker
  threads via `asyncio.to_thread`.

## `Parser`

```python
from neogram.additions.parser import Parser

data = Parser("my_bot")
```

Reads `config.toml` and exposes:

- `data.commands`, `data.messages`, `data.callbacks`, `data.files` — handler dicts.
- `data.patterns` — text patterns.
- `data.states` — collected states.
- `data.modules` — imported modules.
- `data.admins` — admin ids.
- `data.database` — database config dict.
- `data.bot_token` — the bot token.

## `Database`

```python
from neogram.additions.database import Database

db = Database(name_project, host, user, passwd, database_type, port)
```

| Method | Description |
|--------|-------------|
| `create_db()` | Create the database (MySQL) or ensure the SQLite file dir. |
| `check()` | Return whether the database exists. |
| `connect()` | Create the SQLAlchemy engine and connect. |
| `create_tables()` | Create `users`, `states`, `media` tables. |
| `del_db()` | Drop the database (or delete the SQLite file). |
| `get_state(user_id)` | Get a user's state (False if none). |
| `update_state(user_id, state)` | Set a user's state. |
| `delete_state(user_id)` | Clear a user's state. |
| `add_media(name, type, file_id, owner)` | Store a media file reference. |
| `get_media(name, type, owner)` | Retrieve a stored media file reference. |

Supported database types: `mysql`, `sqlite`.

## CLI functions (`neogram.additions.functions`)

- `create_project(name_project)` — interactive project + database creation.
- `create_default_toml(name_project, path, database_type)` — write a default `config.toml`.
- `run_project(name_project)` — parse config, build `Api`, register handlers, run.
- `remove_project(name_project)` — delete the folder and database (with confirmation).

## Related

- [Configuration](configuration.md) — how these methods are driven by TOML.
- [Actions](actions.md) — the `action` config values mapped to these methods.