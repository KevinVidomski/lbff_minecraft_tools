
"""All-in-one addon loader for LBFF packages.

This module provides a small loader that ensures a single LBFF main menu
is available and then loads the individual LBFF addon modules listed in
`ADDON_MODULES`. Addons should expose `register()` / `unregister()` and
optionally a `classes` list; this loader will call `mod.register()` when
present and print import/register errors to stderr.

Design notes:
- Keeps registration resilient: failures in one submodule don't stop
    others from registering.
- Maintains the LBFF menu ownership pattern used across the repository.
"""

bl_info = {
    "name": "LBFF All-in-One",
    "author": "You & Gemini",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "",
    "description": "Loads all LBFF plugins.",
    "warning": "",
    "doc_url": "",
    "category": "Development",
}

import bpy
import sys
import importlib

# --- Addon Discovery & Management ---

# List of addon modules to be managed by this all-in-one addon.
# This approach is explicit and clear. For a more dynamic approach,
# you could scan the directory for other 'lbff_' packages.
ADDON_MODULES = [
    "lbff_minecraft_importer",
    "lbff_gaffer",
]

def get_addon_modules():
    """Dynamically import and return the addon modules."""
    modules = []
    # The package is '..', which is 'lbff.addons'
    package = __package__.rsplit('.', 1)[0]
    for mod_name in ADDON_MODULES:
        try:
            modules.append(importlib.import_module(f".{mod_name}", package))
        except ImportError as e:
            print(f"[{bl_info['name']}] Could not import addon '{mod_name}': {e}")
    return modules

# Define the main LBFF menu here so it's guaranteed to exist
class LBFF_MT_main_menu(bpy.types.Menu):
    bl_label = "LBFF"
    bl_idname = "LBFF_MT_main_menu"

    def draw(self, context):
        # This menu will be populated by the other addons
        pass

def draw_main_menu(self, context):
    self.layout.menu(LBFF_MT_main_menu.bl_idname)


def register():
    # Register the main menu first
    bpy.utils.register_class(LBFF_MT_main_menu)
    # Store the draw function on the menu class so unregister can remove it
    LBFF_MT_main_menu._draw_fn = draw_main_menu
    bpy.types.TOPBAR_MT_editor_menus.append(draw_main_menu)

    # Register the other addons, with error handling
    for mod in get_addon_modules():
        if hasattr(mod, "register"):
            try:
                mod.register()
            except Exception as e:
                print(f"[{bl_info['name']}] Failed to register module {mod.__name__}: {e}", file=sys.stderr)

def unregister():
    # Unregister in reverse order
    for mod in reversed(get_addon_modules()):
        if hasattr(mod, "unregister"):
            try:
                mod.unregister()
            except Exception as e:
                print(f"[{bl_info['name']}] Failed to unregister module {mod.__name__}: {e}", file=sys.stderr)

    # Remove stored draw function if present
    if hasattr(LBFF_MT_main_menu, '_draw_fn'):
        try:
            bpy.types.TOPBAR_MT_editor_menus.remove(LBFF_MT_main_menu._draw_fn)
        except (ValueError, AttributeError):
            pass
        del LBFF_MT_main_menu._draw_fn

    bpy.utils.unregister_class(LBFF_MT_main_menu)

if __name__ == "__main__":
    register()
