# Деплой через Docker

NeoGram поставляется с `Dockerfile` и `docker-compose.yml`, чтобы запускать бота вместе
с базой данных MySQL в контейнерах.

## Что входит

- `db` — контейнер MySQL 8.0 с отдельной базой `neogram` и пользователем.
- `bot` — контейнер, собранный из `Dockerfile`: устанавливает NeoGram и запускает
  `neogram run my_bot`.

## Требования

- [Docker](https://docs.docker.com/get-docker/) с Docker Compose v2.

## Использование

1. Создайте проект бота (см. [Начало работы](getting-started.md)):

   ```bash
   neogram create my_bot
   ```

2. Отредактируйте `my_bot/config.toml` — укажите токен бота и подключите базу данных к
   сервису `db` из compose:

   ```toml
   [database]
   type = "mysql"
   host = "db"
   login = "neogram"
   password = "password"
   port = "3306"
   ```

3. Соберите и запустите стек:

   ```bash
   docker compose up -d --build
   ```

4. Посмотрите логи:

   ```bash
   docker compose logs -f bot
   ```

Каталог `my_bot` смонтирован в контейнер, поэтому правки `config.toml` подхватываются
после `docker compose restart bot`.

## Остановка и очистка

```bash
docker compose down            # остановить стек
docker compose down -v         # также удалить том с данными MySQL
```

## CI/CD

В репозитории есть workflow GitHub Actions ([`.github/workflows/ci.yml`](../.github/workflows/ci.yml)),
который запускается при каждом push и pull request в `main`. Он устанавливает пакет и
прогоняет тесты на Python 3.8, 3.9 и 3.10.