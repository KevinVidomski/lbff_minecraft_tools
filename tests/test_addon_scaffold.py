from pathlib import Path
import importlib.util
import sys
import types


ADDON_PATH = Path(__file__).resolve().parents[1] / "addons" / "lbff_addon_template" / "__init__.py"


def make_fake_bpy():
    """Minimal fake `bpy` for testing addon registration/unregistration.

    This mirrors the pattern used elsewhere in the repo and is intentionally small
    so new tests can copy it directly.
    """
    fake_bpy = types.ModuleType("bpy")
    types_mod = types.SimpleNamespace()
    fake_bpy.types = types_mod

    class Dummy:
        pass

    types_mod.Operator = Dummy
    types_mod.Menu = Dummy
    types_mod.TOPBAR_MT_editor_menus = []

    def register_class(cls):
        setattr(cls, "_registered", True)

    def unregister_class(cls):
        if hasattr(cls, "_registered"):
            delattr(cls, "_registered")

    fake_bpy.utils = types.SimpleNamespace(register_class=register_class, unregister_class=unregister_class)
    return fake_bpy


def import_module_from_path(path: Path):
    spec = importlib.util.spec_from_file_location("lbff_addon_template_example", str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_scaffold_register_unregister(monkeypatch):
    """Example test showing the fake `bpy` pattern for new addons.

    Copy this file when creating tests for a new addon. It demonstrates:
    - creating a minimal `fake_bpy`
    - injecting it into `sys.modules` for imports
    - importing an addon by path and calling `register()`/`unregister()`
    - asserting that a draw callback was added/removed
    """
    fake_bpy = make_fake_bpy()
    monkeypatch.setitem(sys.modules, "bpy", fake_bpy)

    # Ensure parent package is importable
    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root))

    module = import_module_from_path(ADDON_PATH)

    # Call register/unregister, expecting no exceptions
    module.register()

    topbar = sys.modules["bpy"].types.TOPBAR_MT_editor_menus
    assert any(callable(fn) for fn in topbar)

    module.unregister()

    assert not any(callable(fn) for fn in topbar)

    # sanity
    assert hasattr(module, "classes") and isinstance(module.classes, list)

    # cleanup
    sys.path.pop(0)
    del sys.modules["bpy"]
    del sys.modules["lbff_addon_template_example"]
