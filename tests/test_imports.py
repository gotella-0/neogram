import importlib


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
