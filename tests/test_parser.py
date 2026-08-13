import os

import pytest

from neogram.additions.parser import Parser

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def test_parser_reads_config(monkeypatch):
    monkeypatch.chdir(FIXTURES)
    p = Parser("test_bot")
    assert p.name_project == "test_bot"
    assert p.bot_token == "123456:TEST"


def test_parser_reads_commands(monkeypatch):
    monkeypatch.chdir(FIXTURES)
    p = Parser("test_bot")
    assert "start" in p.commands
    assert p.commands["start"]["action"] == "send_text"
    assert "help" in p.commands


def test_parser_reads_database_config(monkeypatch):
    monkeypatch.chdir(FIXTURES)
    p = Parser("test_bot")
    assert p.database["type"] == "sqlite"


def test_parser_loads_modules(monkeypatch):
    monkeypatch.chdir(FIXTURES)
    p = Parser("test_bot")
    assert "temp" in p.modules


def test_parser_missing_project_exits(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(SystemExit):
        Parser("not_exists")
