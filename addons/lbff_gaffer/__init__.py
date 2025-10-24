"""Lighting tools addon (LBFF Gaffer).

This addon provides small helpers to create standard lighting setups. The
module follows the LBFF pattern for menus: it attempts to append its menu
to the global `LBFF_MT_main_menu` and falls back to creating the main menu
if it's not yet present (useful when the all-in-one loader isn't enabled).
"""

bl_info = {
    "name": "LBFF Gaffer",
    "author": "You & Gemini",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Topbar > LBFF",
    "description": "Creates standard lighting setups.",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

import bpy

# Implementation modules
from .operators import LBFF_OT_gaffer_create_lighting
from .menus import LBFF_MT_gaffer_menu


def _menu_draw(self, context):
    self.layout.menu(LBFF_MT_gaffer_menu.bl_idname)


classes = [LBFF_OT_gaffer_create_lighting, LBFF_MT_gaffer_menu]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # Try to append to the main LBFF menu if it exists. Store the draw function
    # on the menu class so unregister can remove the exact same callable.
    try:
        main_menu = bpy.types.LBFF_MT_main_menu
        LBFF_MT_gaffer_menu._menu_draw = _menu_draw
        main_menu.append(_menu_draw)
    except AttributeError:
        # Main menu not registered yet, create it here and append to TOPBAR
        class LBFF_MT_main_menu(bpy.types.Menu):
            bl_label = "LBFF"
            bl_idname = "LBFF_MT_main_menu"

            def draw(self, context):
                layout = self.layout
                layout.menu(LBFF_MT_gaffer_menu.bl_idname)

        bpy.utils.register_class(LBFF_MT_main_menu)

        def draw_main_menu(self, context):
            self.layout.menu(LBFF_MT_main_menu.bl_idname)

        bpy.types.TOPBAR_MT_editor_menus.append(draw_main_menu)
        LBFF_MT_gaffer_menu._draw_main_menu = draw_main_menu


def unregister():
    # Try to remove from the main menu
    try:
        main_menu = bpy.types.LBFF_MT_main_menu
        if hasattr(LBFF_MT_gaffer_menu, '_menu_draw'):
            main_menu.remove(LBFF_MT_gaffer_menu._menu_draw)
    except (AttributeError, RuntimeError):
        pass

    if hasattr(LBFF_MT_gaffer_menu, '_draw_main_menu'):
        try:
            bpy.types.TOPBAR_MT_editor_menus.remove(LBFF_MT_gaffer_menu._draw_main_menu)
        except (ValueError, AttributeError):
            pass
        del LBFF_MT_gaffer_menu._draw_main_menu
        try:
            bpy.utils.unregister_class(bpy.types.LBFF_MT_main_menu)
        except (AttributeError, RuntimeError):
            pass

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()