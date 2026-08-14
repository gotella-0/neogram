# Docker deployment

NeoGram ships with a `Dockerfile` and a `docker-compose.yml` so you can run a bot
together with a MySQL database in containers.

## What you get

- `db` — a MySQL 8.0 container with a dedicated `neogram` database and user.
- `bot` — a container built from the `Dockerfile` that installs NeoGram and runs
  `neogram run my_bot`.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) with Docker Compose v2.

## Usage

1. Create a bot project (see [Getting started](getting-started.md)):

   ```bash
   neogram create my_bot
   ```

2. Edit `my_bot/config.toml` — set your bot token and point the database at the
   compose `db` service:

   ```toml
   [database]
   type = "mysql"
   host = "db"
   login = "neogram"
   password = "password"
   port = "3306"
   ```

3. Build and start the stack:

   ```bash
   docker compose up -d --build
   ```

4. Check the logs:

   ```bash
   docker compose logs -f bot
   ```

The `my_bot` directory is mounted into the container, so edits to `config.toml` are
picked up after `docker compose restart bot`.

## Stopping and cleanup

```bash
docker compose down            # stop the stack
docker compose down -v         # also drop the MySQL data volume
```

## CI/CD

The repository has a GitHub Actions workflow ([`.github/workflows/ci.yml`](../.github/workflows/ci.yml))
that runs on every push and pull request to `main`. It installs the package and runs
the test suite on Python 3.8, 3.9 and 3.10.
