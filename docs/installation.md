# Installation

NeoGram requires **Python 3.8+**. It runs on aiogram 2.x.

## Install from source

Clone the repository and install the package with its dependencies:

```bash
git clone <repo-url> neogram
cd neogram
pip install .
```

Or install in editable mode during development:

```bash
pip install -e .
```

This also puts the `neogram` command on your PATH (via the `[project.scripts]` entry
point in `pyproject.toml`).

## Requirements

Installed automatically by `pip install .`:

- `aiogram==2.20`
- `SQLAlchemy==1.4.39`
- `mysql-connector-python==8.0.29`
- `PyMySQL==1.0.2`
- `toml==0.10.2`

## Verify the installation

```bash
neogram
```

You should see the CLI help listing the available subcommands:

```
usage: neogram [-h] {create,run,remove} ...
```

If you are running from the repository without installing, you can invoke the same CLI
with:

```bash
python -m neogram
```

## Next steps

- [Getting started](getting-started.md) — create and run your first bot.
- [Configuration](configuration.md) — understand `config.toml`.
