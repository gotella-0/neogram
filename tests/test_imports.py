import importlib
import os

import pytest


def test_import_neogram_package():
    import neogram
    assert hasattr(neogram, "check_cmd_args")


def test_import_cli():
    from neogram.cli import check_cmd_args
    assert callable(check_cmd_args)


def test_import_additions():
    import neogram.additions
    assert hasattr(neogram.additions, "create_project")
    assert hasattr(neogram.additions, "run_project")
    assert hasattr(neogram.additions, "remove_project")


def test_import_parser():
    from neogram.additions.parser import Parser
    assert Parser is not None


def test_import_database():
    from neogram.additions.database import Database
    assert Database is not None


def test_import_api():
    from neogram.Api import Api
    assert Api is not None


def test_import_beauty():
    from neogram.beauty import Color
    assert hasattr(Color, "Red")


def test_import_all_submodules():
    for name in [
        "neogram.additions.functions",
        "neogram.additions.parser",
        "neogram.additions.database",
        "neogram.Api.api",
        "neogram.beauty.colors",
    ]:
        importlib.import_module(name)


def test_api_builds_dispatcher(monkeypatch, tmp_path):
    from neogram.Api import Api

    monkeypatch.chdir(tmp_path)
    os.makedirs("proj", exist_ok=True)
    db_cfg = {"host": "", "login": "", "password": "", "type": "sqlite", "port": ""}
    prefixes = {k: "p" for k in ["photo", "video", "audio", "document", "voice", "location", "contact"]}

    api = Api("123:TEST", "proj", {}, db_cfg, prefixes)

    assert api.bot is not None
    assert api.dp is not None
    assert api.database.engine is not None
    assert api.logic_commands == {}
    assert api.menus == {}
    assert api.prefixes == prefixes
    assert api.name_project == "proj"


def test_api_registers_commands(monkeypatch, tmp_path):
    from neogram.Api import Api

    monkeypatch.chdir(tmp_path)
    os.makedirs("proj", exist_ok=True)
    db_cfg = {"host": "", "login": "", "password": "", "type": "sqlite", "port": ""}
    prefixes = {k: "p" for k in ["photo", "video", "audio", "document", "voice", "location", "contact"]}

    api = Api("123:TEST", "proj", {}, db_cfg, prefixes)
    api.register_command("start", {"text": "Hi", "action": "send_text"})

    assert "/start" in api.logic_commands
    assert api.logic_commands["/start"]["any"]["action"] == "send_text"


def test_api_registers_files(monkeypatch, tmp_path):
    from neogram.Api import Api

    monkeypatch.chdir(tmp_path)
    os.makedirs("proj", exist_ok=True)
    db_cfg = {"host": "", "login": "", "password": "", "type": "sqlite", "port": ""}
    prefixes = {k: "p" for k in ["photo", "video", "audio", "document", "voice", "location", "contact"]}

    api = Api("123:TEST", "proj", {}, db_cfg, prefixes)
    api.register_file("photo", {"action": "get_photo", "name": "test"})

    assert f"{prefixes['photo']}:photo" in api.logic_commands
