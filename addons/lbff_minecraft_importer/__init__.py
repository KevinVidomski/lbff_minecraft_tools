
"""Minecraft importer addon wiring for LBFF.

This module exposes the addon metadata and registers the importer operator
and its submenu. It follows the LBFF pattern: try to append to the global
`LBFF_MT_main_menu` if present, otherwise provide a small main menu so the
sub-menu can be accessed.
"""

bl_info = {
    "name": "LBFF Minecraft Importer",
    "author": "You & Gemini",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Topbar > LBFF",
    "description": "Imports Minecraft textures and creates materials.",
    "warning": "",
    "doc_url": "",
    "category": "Import-Export",
}

import bpy

# Import implementation modules
from .operators import LBFF_OT_import_minecraft_texture
from .menus import LBFF_MT_minecraft_importer_menu


# The main menu is provided by lbff_all_in_one or created lazily by other addons.
class LBFF_MT_main_menu(bpy.types.Menu):
    bl_label = "LBFF"
    bl_idname = "LBFF_MT_main_menu"

    def draw(self, context):
        layout = self.layout
        layout.menu(LBFF_MT_minecraft_importer_menu.bl_idname)


def _draw_main_menu(self, context):
    self.layout.menu(LBFF_MT_main_menu.bl_idname)


classes = [
    LBFF_OT_import_minecraft_texture,
    LBFF_MT_minecraft_importer_menu,
    LBFF_MT_main_menu,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # Append the main LBFF menu to TOPBAR and store the draw function on the class
    draw_fn = _draw_main_menu
    LBFF_MT_main_menu._draw_fn = draw_fn
    bpy.types.TOPBAR_MT_editor_menus.append(draw_fn)


def unregister():
    # Remove draw callback if stored
    if hasattr(LBFF_MT_main_menu, "_draw_fn"):
        try:
            bpy.types.TOPBAR_MT_editor_menus.remove(LBFF_MT_main_menu._draw_fn)
        except (ValueError, AttributeError):
            pass
        del LBFF_MT_main_menu._draw_fn

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
