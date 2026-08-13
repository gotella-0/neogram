import os

import pytest

from neogram.additions.database import Database


@pytest.fixture
def sqlite_db(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    db = Database("test_proj", "", "", "", "sqlite", "")
    db.create_db()
    db.connect()
    db.create_tables()
    yield db
    db.del_db()


def test_sqlite_db_file_created(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    db = Database("test_proj", "", "", "", "sqlite", "")
    db.create_db()
    db.connect()
    assert os.path.exists(tmp_path / "test_proj" / "test_proj.db")


def test_create_tables(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    db = Database("test_proj", "", "", "", "sqlite", "")
    db.create_db()
    db.connect()
    db.create_tables()
    with db.engine.connect() as conn:
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    names = {row[0] for row in tables}
    assert {"users", "states", "media"} <= names
    db.del_db()


def test_check_returns_true_when_db_exists(sqlite_db):
    assert sqlite_db.check() is True


def test_check_returns_false_when_db_missing(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    db = Database("ghost_proj", "", "", "", "sqlite", "")
    assert db.check() is False


def test_update_and_get_state(sqlite_db):
    sqlite_db.update_state(1001, "menu")
    assert sqlite_db.get_state(1001) == "menu"


def test_update_state_overwrites(sqlite_db):
    sqlite_db.update_state(1001, "menu")
    sqlite_db.update_state(1001, "profile")
    assert sqlite_db.get_state(1001) == "profile"


def test_delete_state(sqlite_db):
    sqlite_db.update_state(1001, "menu")
    sqlite_db.delete_state(1001)
    assert sqlite_db.get_state(1001) is False


def test_get_state_missing(sqlite_db):
    assert sqlite_db.get_state(9999) is False


def test_add_and_get_media(sqlite_db):
    sqlite_db.add_media("photo1", "photo", "FILE_ID", 42)
    result = sqlite_db.get_media("photo1", "photo", 42)
    assert result is None


def test_add_media_is_idempotent(sqlite_db):
    sqlite_db.add_media("photo1", "photo", "FILE_ID", 42)
    sqlite_db.add_media("photo1", "photo", "FILE_ID", 42)
    with sqlite_db.engine.connect() as conn:
        rows = conn.execute("SELECT COUNT(*) FROM media").fetchone()
    assert rows[0] == 1


def test_del_db_removes_file(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    db = Database("test_proj", "", "", "", "sqlite", "")
    db.create_db()
    db.connect()
    db.create_tables()
    path = tmp_path / "test_proj" / "test_proj.db"
    assert os.path.exists(path)
    db.del_db()
    assert not os.path.exists(path)


def test_mysql_unsupported_type_exits():
    db = Database("test_proj", "localhost", "user", "pass", "nosql", "3306")
    with pytest.raises(SystemExit):
        db.create_db()