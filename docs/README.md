# NeoGram Documentation

NeoGram is a low-code, config-driven Telegram bot framework. You describe a bot in a
`config.toml` file and NeoGram builds and runs the bot for you.

The documentation is split by topic. Choose what you need:

## Topics

| Topic | English | Русский |
|-------|---------|---------|
| Installation | [installation.md](installation.md) | [ru/installation.md](ru/installation.md) |
| Getting started — your first bot | [getting-started.md](getting-started.md) | [ru/getting-started.md](ru/getting-started.md) |
| Configuration (`config.toml`) | [configuration.md](configuration.md) | [ru/configuration.md](ru/configuration.md) |
| States & multi-step dialogs | [states.md](states.md) | [ru/states.md](ru/states.md) |
| Buttons & keyboards | [buttons.md](buttons.md) | [ru/buttons.md](ru/buttons.md) |
| Files & media handling | [files-media.md](files-media.md) | [ru/files-media.md](ru/files-media.md) |
| Send actions | [actions.md](actions.md) | [ru/actions.md](ru/actions.md) |
| API reference | [api-reference.md](api-reference.md) | [ru/api-reference.md](ru/api-reference.md) |
| Examples walkthrough | [examples.md](examples.md) | [ru/examples.md](ru/examples.md) |
| Docker deployment | [docker.md](docker.md) | [ru/docker.md](ru/docker.md) |

## Suggested reading order

1. [Getting started](getting-started.md) — install and run your first bot.
2. [Configuration](configuration.md) — understand the `config.toml` schema.
3. [States](states.md), [Buttons](buttons.md), [Actions](actions.md) — build real logic.
4. [API reference](api-reference.md) — all `Api` methods in detail.
5. [Examples](examples.md) — read real bots from the `examples/` folder.

## Project structure

```
neogram/            # the framework package
├── cli.py          # command-line entry point (create / run / remove)
├── Api/api.py      # the Api hub: registration, handlers, send actions
├── additions/      # Parser, functions (project lifecycle), Database
│   └── databases/  # MySQL driver
└── beauty/         # ANSI colors for the CLI
```

Back to the [project README](../README.md).
