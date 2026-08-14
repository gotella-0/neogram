# Установка

Для работы NeoGram требуется **Python 3.8+**. Фреймворк работает на aiogram 2.x.

## Установка из исходников

Клонируйте репозиторий и установите пакет вместе с зависимостями:

```bash
git clone <repo-url> neogram
cd neogram
pip install .
```

Или установите в режиме редактирования для разработки:

```bash
pip install -e .
```

Это также добавляет команду `neogram` в PATH (через точку входа `[project.scripts]`
в `pyproject.toml`).

## Требования

Устанавливаются автоматически командой `pip install .`:

- `aiogram==2.20`
- `SQLAlchemy==1.4.39`
- `mysql-connector-python==8.0.29`
- `PyMySQL==1.0.2`
- `toml==0.10.2`

## Проверка установки

```bash
neogram
```

Вы должны увидеть справку CLI со списком подкоманд:

```
usage: neogram [-h] {create,run,remove} ...
```

Если вы работаете из репозитория без установки, ту же команду можно вызвать так:

```bash
python -m neogram
```

## Дальше

- [Начало работы](getting-started.md) — создание и запуск первого бота.
- [Конфигурация](configuration.md) — устройство `config.toml`.
