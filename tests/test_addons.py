import importlib.util
import sys
import types
from pathlib import Path


def make_fake_bpy():
    fake_bpy = types.ModuleType("bpy")

    # Minimal types namespace
    types_mod = types.SimpleNamespace()
    setattr(fake_bpy, "types", types_mod)

    class Dummy:
        pass

    types_mod.Operator = Dummy
    types_mod.Menu = Dummy

    # Simulate TOPBAR_MT_editor_menus as a list-like structure with append/remove
    fake_bpy.types.TOPBAR_MT_editor_menus = []

    # utils namespace
    def register_class(cls):
        setattr(cls, "_registered", True)

    def unregister_class(cls):
        if hasattr(cls, "_registered"):
            delattr(cls, "_registered")

    setattr(fake_bpy, "utils", types.SimpleNamespace(register_class=register_class, unregister_class=unregister_class))

    return fake_bpy


def import_module_from_path(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module {name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


BASE = Path(__file__).resolve().parents[1] / "addons"


def test_all_in_one_register_unregister(monkeypatch):
    fake_bpy = make_fake_bpy()
    monkeypatch.setitem(sys.modules, "bpy", fake_bpy)

    sys.path.insert(0, str(BASE.parent))
    mod = import_module_from_path("lbff_all_in_one", BASE / "lbff_all_in_one" / "__init__.py")

    # register/unregister should run without exceptions
    mod.register()
    topbar = sys.modules["bpy"].types.TOPBAR_MT_editor_menus
    assert any(callable(fn) for fn in topbar)

    mod.unregister()
    assert not any(callable(fn) for fn in topbar)

    sys.path.pop(0)
    del sys.modules["bpy"]
    del sys.modules["lbff_all_in_one"]


def test_gaffer_register_unregister(monkeypatch):
    fake_bpy = make_fake_bpy()
    monkeypatch.setitem(sys.modules, "bpy", fake_bpy)

    sys.path.insert(0, str(BASE.parent))
    mod = import_module_from_path("lbff_gaffer", BASE / "lbff_gaffer" / "__init__.py")

    mod.register()
    # gaffer should append its menu draw
    topbar = sys.modules["bpy"].types.TOPBAR_MT_editor_menus
    assert any(callable(fn) for fn in topbar)

    mod.unregister()
    assert not any(callable(fn) for fn in topbar)

    sys.path.pop(0)
    del sys.modules["bpy"]
    del sys.modules["lbff_gaffer"]


def test_importer_register_unregister(monkeypatch):
    fake_bpy = make_fake_bpy()
    monkeypatch.setitem(sys.modules, "bpy", fake_bpy)

    sys.path.insert(0, str(BASE.parent))
    mod = import_module_from_path("lbff_minecraft_importer", BASE / "lbff_minecraft_importer" / "__init__.py")

    mod.register()
    topbar = sys.modules["bpy"].types.TOPBAR_MT_editor_menus
    assert any(callable(fn) for fn in topbar)

    mod.unregister()
    assert not any(callable(fn) for fn in topbar)

    sys.path.pop(0)
    del sys.modules["bpy"]
    del sys.modules["lbff_minecraft_importer"]
