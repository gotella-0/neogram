import importlib
import pickle
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
    from neogram.Api import Api, Manager, Worker
    assert all(x is not None for x in (Api, Manager, Worker))


def test_import_beauty():
    from neogram.beauty import Color
    assert hasattr(Color, "Red")


def test_import_all_submodules():
    for name in [
        "neogram.additions.texts",
        "neogram.additions.functions",
        "neogram.additions.parser",
        "neogram.additions.database",
        "neogram.Api.api",
        "neogram.Api.worker",
        "neogram.Api.manager",
        "neogram.beauty.colors",
    ]:
        importlib.import_module(name)


def test_worker_pickle_roundtrip(monkeypatch, tmp_path):
    from neogram.Api.worker import Worker

    monkeypatch.chdir(tmp_path)
    os.makedirs("proj", exist_ok=True)
    db_cfg = {"host": "", "login": "", "password": "", "type": "sqlite", "port": ""}
    prefixes = {k: "p" for k in ["photo", "video", "audio", "document", "voice", "location", "contact"]}
    worker = Worker("123:TEST", "proj", {}, db_cfg, prefixes)

    blob = pickle.dumps(worker)
    restored = pickle.loads(blob)

    assert restored.token == "123:TEST"
    assert restored.bot is not None
    assert restored.loop is not None
    assert restored.database.engine is not None
    assert restored.logic_commands == worker.logic_commands
    assert restored.prefixes == worker.prefixes
    assert restored.name_project == worker.name_project
