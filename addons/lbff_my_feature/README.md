LBFF My Feature (scaffold)
=================================

This folder contains a minimal example addon scaffold used by the LBFF project.

Purpose
-------
- Provide a tiny, import-safe addon template that AI agents and contributors can copy when
  building new LBFF add-ons.

What is included
----------------
- `__init__.py` — the addon implementation. It is intentionally minimal and safe to import in
  test environments that inject a fake `bpy` module.

How to use this scaffold
------------------------
1. Copy this package to `addons/lbff_<your_feature>`.
2. Edit `bl_info` metadata, implement real operator/menu classes (inherit from `bpy.types.*`),
   and add them to the `classes` list.
3. Implement `register()` and `unregister()` following the repo pattern:
   - loop `for cls in classes: bpy.utils.register_class(cls)` and reverse on unregister;
   - attach draw callbacks to `bpy.types.TOPBAR_MT_editor_menus` or `bpy.types.LBFF_MT_main_menu`;
   - store draw callback on the menu/class (e.g. `MyMenu._draw_fn = draw_fn`) so `unregister()`
     can remove the same callable safely.

Testing the scaffold
--------------------
- The repository includes `tests/test_addon_scaffold.py` which shows how to create a minimal
  `fake_bpy`, inject it with `monkeypatch.setitem(sys.modules, 'bpy', fake_bpy)`, import the addon
  by path, and call `register()` / `unregister()` to assert the draw callback is added/removed.

Notes
-----
- This README is intentionally short: the scaffold is a starting point. For production addons,
  implement full operator logic, properties, and panels as required.
