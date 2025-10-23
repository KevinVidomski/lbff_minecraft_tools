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

- Menu wiring and TOPBAR_MT_editor_menus:

  - Common menu draw functions are appended with `bpy.types.TOPBAR_MT_editor_menus.append(draw_main_menu)` and removed with `.remove(...)` in `unregister()`.
  - When adding a new submenu, append it to `LBFF_MT_main_menu` (if present) or follow the `lbff_gaffer` fallback strategy.

- All-in-one loader behaviour
  - `ADDON_MODULES` in `lbff_all_in_one` is an explicit list. To make the all-in-one aware of a new addon, add its package name to that list.
  - The loader uses `importlib.import_module(f".{mod_name}", package)` and calls `mod.register()` if present. Errors are printed to stderr.

Developer workflows (discoverable from code / README)

- Install in Blender: install the addon by selecting the target package's `__init__.py` in Blender's Add-ons UI. The top-level `README.md` explains this.
- Prefer enabling `lbff_all_in_one` to register the main menu and the other modules in the recommended order.
- Debugging: the code uses plain `print()` for diagnostic output. Run Blender from a terminal (or open the Blender system console) to see prints and import errors.

## Quick orientation

This repository implements a small suite of Blender add-ons collected under the "LBFF" menu. The core pieces are in `addons/`:

- `addons/lbff_all_in_one/__init__.py` — an "all-in-one" loader that registers a common LBFF menu and then imports/registers other addon modules listed in `ADDON_MODULES`.
- `addons/lbff_minecraft_importer/__init__.py` — an importer operator and a submenu that appends itself into the LBFF menu.
- `addons/lbff_gaffer/__init__.py` — a lighting toolset that attempts to append a small menu into the main LBFF menu and falls back to creating that menu if it doesn't exist.

### Why this matters for code changes

- **Menu ownership:** the main LBFF menu may be created by `lbff_all_in_one` or lazily by `lbff_gaffer`. Other addons defensively try to append to `bpy.types.LBFF_MT_main_menu` and fall back if it's missing. Preserve this pattern when adding or moving code.
- **Registration model:** each addon exposes `register()` / `unregister()` functions and usually defines a `classes` list. `lbff_all_in_one` calls those `register()` functions directly when present.

### Key patterns and concrete examples

- **bl_info metadata**

  All addons include a `bl_info` dict declaring Blender version and category (e.g., `"blender": (3,0,0)`). Keep this metadata intact when editing.

  Example: `addons/lbff_minecraft_importer/__init__.py` defines `bl_info = { "name": "LBFF Minecraft Importer", ... }`.

- **Class lists and registration loops**

  Pattern: define `classes = [ClassA, ClassB, ...]` then register with:

  ````py
  ## Quick orientation

  This repository implements a small suite of Blender add-ons collected under the "LBFF" menu. The core pieces are in `addons/`:

  - `addons/lbff_all_in_one/__init__.py` — an all-in-one loader that registers a common LBFF menu and imports/registers other addon modules listed in `ADDON_MODULES`.
  - `addons/lbff_minecraft_importer/__init__.py` — an importer operator and a submenu that appends itself into the LBFF menu.
  - `addons/lbff_gaffer/__init__.py` — a lighting toolset that appends a submenu to the main LBFF menu and falls back to creating that menu if it doesn't exist.

  ### Why this matters for code changes

  - **Menu ownership:** The main LBFF menu may be created by `lbff_all_in_one` or lazily by `lbff_gaffer`. Other addons defensively append to `bpy.types.LBFF_MT_main_menu` when available. Preserve this pattern when adding or moving code.
  - **Registration model:** Each addon exposes `register()` / `unregister()` and usually defines a `classes` list; `lbff_all_in_one` calls these `register()` functions directly.

  ### Key patterns and concrete examples

  - **bl_info metadata**

    All addons include a `bl_info` dict declaring Blender version and category (e.g., `"blender": (3,0,0)`). Keep this metadata intact.

    Example: `addons/lbff_minecraft_importer/__init__.py` defines `bl_info = { "name": "LBFF Minecraft Importer", ... }`.

  - **Class lists and registration loops**

    Pattern: define `classes = [ClassA, ClassB, ...]` then register with:

    ```py
    for cls in classes:
        bpy.utils.register_class(cls)
  ````

  Unregister in reverse order.

  - **Menu wiring and TOPBAR_MT_editor_menus**

    - Common menu draw functions are appended with `bpy.types.TOPBAR_MT_editor_menus.append(draw_fn)` and removed in `unregister()` with `.remove(...)`.
    - When adding a new submenu, append it to `LBFF_MT_main_menu` if available; otherwise follow the `lbff_gaffer` fallback strategy (create the main menu and append a draw function).

  - **Draw-callback storage standard (new / recommended)**

    Store the exact draw callback on the menu class so `unregister()` can remove the same callable. This prevents accidental removal of other addons' callbacks.

    Pattern example:

    ```py
    # register()
    draw_fn = lambda self, context: self.layout.menu(MyMenu.bl_idname)
    MyMenu._draw_fn = draw_fn
    bpy.types.TOPBAR_MT_editor_menus.append(draw_fn)

    # unregister()
    if hasattr(MyMenu, '_draw_fn'):
        try:
            bpy.types.TOPBAR_MT_editor_menus.remove(MyMenu._draw_fn)
        except (ValueError, AttributeError):
            pass
        del MyMenu._draw_fn
    ```

  - **All-in-one loader behaviour**

    - `ADDON_MODULES` in `lbff_all_in_one` is an explicit list. Add new addon module names there to include them in the bundle.
    - The loader uses `importlib.import_module(f".{mod_name}", package)` and calls `mod.register()` when present. Import/register errors are printed to stderr.

  ### Developer workflows (found in code / README)

  - Install in Blender: install the addon's `__init__.py` via `Edit > Preferences > Add-ons > Install...` (see `README.md`).
  - Prefer enabling `lbff_all_in_one` to register the main menu and modules in the recommended order.
  - Debugging: code uses `print()` for diagnostic output. Run Blender from a terminal (or open the Blender system console) to see prints and import errors.

  ### Tests & CI

  - Template tests: see `tests/test_addon_template.py` — it fakes `bpy` and validates `register()`/`unregister()` behavior.
  - CI: a GitHub Actions workflow has been added at `.github/workflows/pytest.yml` to run `pytest` on push and PR.

  ### Files of interest

  - `README.md` — user install instructions
  - `addons/lbff_all_in_one/__init__.py` — main menu & loader
  - `addons/lbff_minecraft_importer/__init__.py` — importer operator and menu
  - `addons/lbff_gaffer/__init__.py` — lighting toolset and fallback main menu creation (now follows draw-callback storage standard)
  - `addons/lbff_addon_template/__init__.py` — template showing docstrings, type hints, and draw-callback storage
  - `tests/test_addon_template.py` — smoke test used by CI

  ### Agent rules and do/don't checklist (specific to this repo)

  - DO preserve `bl_info` metadata and `register()`/`unregister()` functions; these are the integration contract with Blender.
  - DO keep menu append/remove calls paired in `register()` / `unregister()` and store draw callbacks on the menu class per the standard above.
  - DO respect the explicit `ADDON_MODULES` list when updating `lbff_all_in_one` — do not auto-scan without updating the list.
  - DO NOT assume the main menu always exists; use the `lbff_gaffer` try/fallback pattern.
  - DO keep `register()` idempotent and resilient to partial loads; follow the existing pattern of printing import/register failures.
  - DO NOT run multiple terminal commands in one line. i.e. don't use ``;``

  If anything above is unclear or missing, tell me what you want the agent to be able to do first (e.g., add a new addon, refactor menu wiring, or migrate the loader to dynamic discovery) and I'll iterate.
