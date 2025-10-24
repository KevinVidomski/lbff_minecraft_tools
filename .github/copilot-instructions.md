## Copilot / AI agent quick instructions — LBFF plugins

Short practical notes to get productive editing/testing Blender add-ons in this repo.

- Repo layout: top-level `addons/` contains packages. Each addon follows the Blender contract: a `bl_info` dict, `classes = [...]`, and `register()`/`unregister()` functions.
- Key packages:

  - `addons/lbff_all_in_one/__init__.py` — explicit `ADDON_MODULES` list and loader that imports each submodule and calls `mod.register()` when present.
  - `addons/lbff_gaffer/` — creates/falls-back to the main LBFF menu; follow its defensive menu pattern when adding UI.
  - `addons/lbff_minecraft_importer/` — example operator + menu wiring; use it as a template for new addons.

- Registration pattern: use `classes = [A,B]` then
  for cls in classes: bpy.utils.register_class(cls)
  and unregister in reverse order. Keep `register()` idempotent and resilient to partial loads.

- Menu wiring: append draw callbacks to `bpy.types.TOPBAR_MT_editor_menus` and/or `bpy.types.LBFF_MT_main_menu`. Store the exact callable on the menu class so `unregister()` can remove it safely.

- All-in-one loader note: to include a new addon in the bundle, add its package name to `ADDON_MODULES` in `addons/lbff_all_in_one/__init__.py` (the loader does not auto-scan).

- Developer workflows (project-specific):

  - Install the add-on into Blender by selecting the package `__init__.py` via Edit → Preferences → Add-ons → Install...
  - Tests: run `pytest` (repository includes `tests/test_addon_template.py` which fakes `bpy`). See `pytest.ini` for config.
  - New test scaffold: `tests/test_addon_scaffold.py` is a copyable example showing the fake `bpy` pattern and import-by-path approach; copy it when adding tests for new addons.
  - Debugging in Blender: two VSCode tasks exist — "Install debugpy into Blender Python" and "Start Blender with debugpy startup script" (check `tools/start_debugpy_in_blender.py` and `tools/install_debugpy.ps1`). Use the tasks when attaching a debugger to Blender.

- Files to inspect when changing behavior:

  - `addons/lbff_all_in_one/__init__.py` — loader & ADDON_MODULES
  - `addons/*/__init__.py`, `menus.py`, `operators.py` — typical addon structure
  - `tools/` — helper scripts for debugging and CI
  - `tests/` — pytest-based unit/CI tests (mocks `bpy`)

- Agent rules (do / don't — concise):
  - DO preserve `bl_info`, `register()` / `unregister()` semantics and the `classes` list structure.
  - DO keep append/remove of menu draw callbacks paired and use the stored `_draw_fn` pattern.
  - DO add new addon names to `ADDON_MODULES` if they should be included in the all-in-one loader.
  - DO run `pytest` after substantive changes; fix tests or explain why a test change is required.
  - DON’T assume Blender APIs are available at test-time — use the existing test mocks.

### How to add a new addon (quick checklist)

- Create a new package under `addons/`, using the `lbff_` prefix (e.g. `lbff_my_feature`).
- Add `bl_info` and a `classes = [...]` list in `__init__.py`.
- Implement `register()` / `unregister()` that:
  - registers/unregisters classes via `bpy.utils.register_class` / `bpy.utils.unregister_class` (loop `classes`).
  - appends draw callbacks to `bpy.types.TOPBAR_MT_editor_menus` or `bpy.types.LBFF_MT_main_menu` for UI.
  - stores the draw callback on the menu/class (e.g. `MyMenu._draw_fn = draw_fn`) and removes it in `unregister()`.
- Add your module name to `ADDON_MODULES` in `addons/lbff_all_in_one/__init__.py` to include it in the all-in-one loader.

Sample minimal patch (example only):

```diff
*** Update File: addons/lbff_all_in_one/__init__.py
@@
 ADDON_MODULES = [
     "lbff_minecraft_importer",
     "lbff_gaffer",
+    "lbff_my_feature",
 ]
```

### Tests & mocking `bpy` (short example)

Follow the pattern in `tests/test_addon_template.py`:

- Build a minimal `fake_bpy` exposing the attributes your addon uses (`types.Operator`, `types.Menu`, `types.TOPBAR_MT_editor_menus` list, `utils.register_class`, etc.).
- Use `monkeypatch.setitem(sys.modules, 'bpy', fake_bpy)` so imports resolve to the fake module in tests.
- Import the addon (by path or via `sys.path`), then call `module.register()` and `module.unregister()`.
- Assert side effects: the fake `TOPBAR_MT_editor_menus` contains/resolves the draw callback after `register()` and is cleared after `unregister()`; `module.classes` exists and is a list.

Minimal test outline (see `tests/test_addon_template.py` for full reference):

```py
def test_register_unregister_runs_without_errors(monkeypatch):
    fake_bpy = make_fake_bpy()
    monkeypatch.setitem(sys.modules, "bpy", fake_bpy)
    module = import_module_from_path(path_to_addon)
    module.register()
    assert any(callable(fn) for fn in fake_bpy.types.TOPBAR_MT_editor_menus)
    module.unregister()
    assert not any(callable(fn) for fn in fake_bpy.types.TOPBAR_MT_editor_menus)
```

These additions should make it quick for an AI agent to add an addon and to write or update tests that validate Blender integration without running Blender.

## Quick orientation

This repository implements a small suite of Blender add-ons collected under the "LBFF" menu. The core pieces are in `addons/`:

- `addons/lbff_all_in_one/__init__.py` — an "all-in-one" loader that registers a common LBFF menu and then imports/registers other addon modules listed in `ADDON_MODULES`.
- `addons/lbff_minecraft_importer/__init__.py` — an importer operator and a submenu that appends itself into the LBFF menu.
- `addons/lbff_gaffer/__init__.py` — a lighting toolset that attempts to append a small menu into the main LBFF menu and falls back to creating that menu if it doesn't exist.

Why this matters for code changes

- Menu ownership: the main LBFF menu may be created by `lbff_all_in_one` or lazily by `lbff_gaffer`. Other addons defensively try to append to `bpy.types.LBFF_MT_main_menu` and fall back if it's missing. Agents should preserve this pattern when adding new addons or moving code between packages.
- Registration model: each addon exposes `register()` / `unregister()` functions and registers a `classes` list (or equivalent). The all-in-one loader calls these `register()` functions directly.

Key patterns and concrete examples

- bl_info metadata: all addons include a `bl_info` dict declaring Blender version and category (e.g., `"blender": (3,0,0)`). Respect and keep this metadata when editing addons.

  - Example: `addons/lbff_minecraft_importer/__init__.py` contains `bl_info = { "name": "LBFF Minecraft Importer", ... }`.

- Class lists and registration loops: follow the thin wrapper pattern:

  - Define `classes = [ClassA, ClassB, ...]` then
  - Register with `for cls in classes: bpy.utils.register_class(cls)` and unregister in reverse order.
  - Example: `lbff_minecraft_importer` and `lbff_gaffer` use this exact pattern.

## Copilot / AI agent quick instructions — LBFF plugins

Short practical notes to get productive editing/testing Blender add-ons in this repo.

- Repo layout: top-level `addons/` contains packages. Each addon follows the Blender contract: a `bl_info` dict, `classes = [...]`, and `register()`/`unregister()` functions.
- Key packages:

  - `addons/lbff_all_in_one/__init__.py` — explicit `ADDON_MODULES` list and loader that imports each submodule and calls `mod.register()` when present.
  - `addons/lbff_gaffer/` — creates/falls-back to the main LBFF menu; follow its defensive menu pattern when adding UI.
  - `addons/lbff_minecraft_importer/` — example operator + menu wiring; use it as a template for new addons.

- Registration pattern: use `classes = [A,B]` then
  for cls in classes: bpy.utils.register_class(cls)
  and unregister in reverse order. Keep `register()` idempotent and resilient to partial loads.

- Menu wiring: append draw callbacks to `bpy.types.TOPBAR_MT_editor_menus` and/or `bpy.types.LBFF_MT_main_menu`. Store the exact callable on the menu class so `unregister()` can remove it safely:
  Example:

  ```py
  draw_fn = lambda self, ctx: self.layout.menu(MyMenu.bl_idname)
  MyMenu._draw_fn = draw_fn
  bpy.types.TOPBAR_MT_editor_menus.append(draw_fn)
  # later in unregister():
  if hasattr(MyMenu, '_draw_fn'):
      bpy.types.TOPBAR_MT_editor_menus.remove(MyMenu._draw_fn)
      del MyMenu._draw_fn
  ```

- All-in-one loader note: to include a new addon in the bundle, add its package name to `ADDON_MODULES` in `addons/lbff_all_in_one/__init__.py` (the loader does not auto-scan).

- Developer workflows (project-specific):

  - Install the add-on into Blender by selecting the package `__init__.py` via Edit → Preferences → Add-ons → Install...
  - Tests: run `pytest` (repository includes `tests/test_addon_template.py` which fakes `bpy`). See `pytest.ini` for config.
  - Debugging in Blender: two VSCode tasks exist — "Install debugpy into Blender Python" and "Start Blender with debugpy startup script" (check `tools/start_debugpy_in_blender.py` and `tools/install_debugpy.ps1`). Use the tasks when attaching a debugger to Blender.

- Files to inspect when changing behavior:

  - `addons/lbff_all_in_one/__init__.py` — loader & ADDON_MODULES
  - `addons/*/__init__.py`, `menus.py`, `operators.py` — typical addon structure
  - `tools/` — helper scripts for debugging and CI
  - `tests/` — pytest-based unit/CI tests (mocks `bpy`)

- Agent rules (do / don't — concise):
  - DO preserve `bl_info`, `register()` / `unregister()` semantics and the `classes` list structure.
  - DO keep append/remove of menu draw callbacks paired and use the stored `_draw_fn` pattern shown above.
  - DO add new addon names to `ADDON_MODULES` if they should be included in the all-in-one loader.
  - DO run `pytest` after substantive changes; fix tests or explain why a test change is required.
  - DON’T assume Blender APIs are available at test-time — use the existing test mocks.

If you'd like, I can tighten any section, add specific examples for a target file, or create a short checklist for adding a new addon. What should I expand next?

- `addons/lbff_gaffer/__init__.py` — a lighting toolset that appends a submenu to the main LBFF menu and falls back to creating that menu if it doesn't exist.
