# Getting started — your first bot

This guide walks you through creating, configuring and running a bot with NeoGram.

## 1. Create a project

```bash
neogram create hello_world
```

You will be asked to choose a database:

```
[Database] Choose database (default - mysql):
1.Mysql
2.Postgresql
3.SQLite

Answer:
```

Type `3` for SQLite (no server required) or `1` for MySQL. For MySQL you will also be
asked for host, port, login and password; leave them empty to use the defaults
(`localhost`, `3306`, `neogram`).

The command creates:

```
hello_world/
├── assets/        # files for send_photo / send_document
├── modules/       # optional custom Python modules
└── config.toml    # the bot logic
```

and the database itself (the `.db` file for SQLite, or the schema in MySQL).

## 2. Configure the bot

Open `hello_world/config.toml`:

```toml
name_project = "hello_world"
bot_token = "write_here_bot_api_token"
admins = [ "write_here_id",]

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

Change `bot_token` to the token you received from [@BotFather](https://t.me/BotFather)
and put your Telegram user id into `admins`.

## 3. Run the bot

```bash
neogram run hello_world
```

Message `/start` to your bot. It will reply:

> Hi in bot made in NeoGram

## 4. Remove a project

```bash
neogram remove hello_world
```

NeoGram checks that both the folder and the database exist, asks for confirmation, and
deletes them.

## What just happened?

1. `Parser` reads `config.toml` and collects commands, messages, callbacks, files,
   database settings, and imports.
2. `Api` is created with the token, project name, modules, database config and random
   prefixes for file types.
3. Each command/message/callback/file is registered as a handler.
4. `Api.run()` starts polling with aiogram.

## Next steps

- [Configuration](configuration.md) — full reference of `config.toml`.
- [Actions](actions.md) — all the send actions you can use.
- [Examples](examples.md) — read the ready-made bots in `examples/`.