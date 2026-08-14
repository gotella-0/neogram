# NeoGram Documentation — Русский

NeoGram — это low-code фреймворк для Telegram-ботов, управляемый конфигом. Вы описываете
бота в файле `config.toml`, а NeoGram собирает и запускает его за вас.

Документация разбита по темам:

## Темы

| Тема | Английский | Русский |
|------|-----------|---------|
| Установка | [installation.md](../installation.md) | [installation.md](installation.md) |
| Начало работы — первый бот | [getting-started.md](../getting-started.md) | [getting-started.md](getting-started.md) |
| Конфигурация (`config.toml`) | [configuration.md](../configuration.md) | [configuration.md](configuration.md) |
| Состояния и многошаговые диалоги | [states.md](../states.md) | [states.md](states.md) |
| Кнопки и клавиатуры | [buttons.md](../buttons.md) | [buttons.md](buttons.md) |
| Файлы и медиа | [files-media.md](../files-media.md) | [files-media.md](files-media.md) |
| Действия отправки | [actions.md](../actions.md) | [actions.md](actions.md) |
| Справочник API | [api-reference.md](../api-reference.md) | [api-reference.md](api-reference.md) |
| Разбор примеров | [examples.md](../examples.md) | [examples.md](examples.md) |

## Рекомендуемый порядок чтения

1. [Начало работы](getting-started.md) — установка и запуск первого бота.
2. [Конфигурация](configuration.md) — схема `config.toml`.
3. [Состояния](states.md), [Кнопки](buttons.md), [Действия](actions.md) — реальная логика.
4. [Справочник API](api-reference.md) — все методы `Api`.
5. [Примеры](examples.md) — разбор реальных ботов из папки `examples/`.

## Структура проекта

```
neogram/            # пакет фреймворка
├── cli.py          # точка входа CLI (create / run / remove)
├── Api/api.py      # хаб Api: регистрация, обработчики, действия отправки
├── additions/      # Parser, functions (жизненный цикл проекта), Database
│   └── databases/  # MySQL драйвер
└── beauty/         # ANSI-цвета для CLI
```

Назад к [README проекта](../../README.md).
