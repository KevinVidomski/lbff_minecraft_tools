import importlib.util
import sys
import types
from pathlib import Path

ADDON_PATH = Path(__file__).resolve().parents[1] / "addons" / "lbff_addon_template" / "__init__.py"


def make_fake_bpy():
    """Create a minimal fake `bpy` module with the pieces used by the template.

    The fake module provides `types.Operator`, `types.Menu`, `utils.register_class`,
    `utils.unregister_class`, and a placeholder `types` namespace. These are simplified
    stand-ins so the addon can import and call register/unregister in a test.
    """
    fake_bpy = types.ModuleType("bpy")

    # Minimal types namespace
    types_mod = types.SimpleNamespace()
    setattr(fake_bpy, "types", types_mod)

    class Dummy:
        pass

    # Dummy operator/menu base classes (not used directly but keeping structure)
    types_mod.Operator = Dummy
    types_mod.Menu = Dummy

    # TOPBAR_MT_editor_menus simulation: a list with append/remove
    fake_bpy.types.TOPBAR_MT_editor_menus = []

    # utils namespace with register/unregister helpers
    def register_class(cls):
        # emulate registration side effect
        setattr(cls, "_registered", True)

    def unregister_class(cls):
        if hasattr(cls, "_registered"):
            delattr(cls, "_registered")

    setattr(fake_bpy, "utils", types.SimpleNamespace(register_class=register_class, unregister_class=unregister_class))

    return fake_bpy


def import_module_from_path(path: Path):
    spec = importlib.util.spec_from_file_location("lbff_addon_template", str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_register_unregister_runs_without_errors(monkeypatch):
    fake_bpy = make_fake_bpy()
    monkeypatch.setitem(sys.modules, "bpy", fake_bpy)

    # Ensure parent package is importable
    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root))

    module = import_module_from_path(ADDON_PATH)

    # Call register/unregister, expecting no exceptions
    module.register()

    # If register appended a draw function, it should be present in the fake TOPBAR list
    topbar = sys.modules["bpy"].types.TOPBAR_MT_editor_menus
    assert any(callable(fn) for fn in topbar)

    module.unregister()

    # After unregister, the draw function should be removed
    assert not any(callable(fn) for fn in topbar)

    # Basic sanity checks: classes should exist and be Python objects
    assert hasattr(module, "classes")
    assert isinstance(module.classes, list)

    # cleanup
    sys.path.pop(0)
    del sys.modules["bpy"]
    del sys.modules["lbff_addon_template"]
