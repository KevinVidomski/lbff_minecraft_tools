"""LBFF Addon Template

Purpose:
- Minimal Blender addon skeleton following LBFF conventions.

Contract:
- Export `classes` list and `register()` / `unregister()` functions.
- If the addon contributes menus, append to `LBFF_MT_main_menu` when available or follow the `lbff_gaffer` fallback pattern.

Notes for Copilot/AI:
- Provide implementations for TODOs below.
- Keep functions small and document inputs/outputs.
"""

bl_info = {
    "name": "LBFF Addon Template",
    "author": "Your Name",
    "version": (0, 1),
    "blender": (3, 0, 0),
    "location": "View3D > Topbar > LBFF",
    "description": "Template addon following LBFF patterns.",
    "warning": "",
    "doc_url": "",
    "category": "Development",
}

from typing import List

if __name__ != "__main__":
    import bpy

# Example operator
class LBFF_OT_template_action(bpy.types.Operator):
    """Perform a small template action.

    AI: implement the operator body to create a simple cube and return {'FINISHED'}.

    Returns:
        set: Blender operator result set (e.g., {'FINISHED'})
    """
    bl_idname = "lbff.template_action"
    bl_label = "LBFF Template Action"

    def execute(self, context):
        # TODO: Copilot: create a cube and name it 'LBFF_Template'
        print("Template action executed")
        return {'FINISHED'}


# Example menu
class LBFF_MT_template_menu(bpy.types.Menu):
    bl_label = "Template"
    bl_idname = "LBFF_MT_template_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator(LBFF_OT_template_action.bl_idname)


# If this addon must ensure the main menu exists, follow the pattern used in repo.
classes: List[type] = [LBFF_OT_template_action, LBFF_MT_template_menu]


def register():
    """Register classes and append menu.

    This follows the LBFF pattern: register classes, then try to append to the
    global `LBFF_MT_main_menu` if present. If not present, it's fine to register
    standalone; the all-in-one loader will handle wiring when used.
    """
    for cls in classes:
        bpy.utils.register_class(cls)

    # Try to append to the global LBFF main menu draw list if it exists.
    # Store the exact draw function on the menu class so unregister can remove it cleanly.
    try:
        draw_fn = lambda self, context: self.layout.menu(LBFF_MT_template_menu.bl_idname)
        # store the draw function so unregister() can remove the same object
        LBFF_MT_template_menu._draw_fn = draw_fn
        bpy.types.TOPBAR_MT_editor_menus.append(draw_fn)
    except AttributeError:
        # TOPBAR_MT_editor_menus or LBFF main menu not present; nothing to do.
        pass


def unregister():
    """Unregister classes and remove appended menu if present."""
    # Remove the draw function from the global TOPBAR draw list if we stored it.
    try:
        if hasattr(LBFF_MT_template_menu, "_draw_fn"):
            try:
                bpy.types.TOPBAR_MT_editor_menus.remove(LBFF_MT_template_menu._draw_fn)
            except (ValueError, AttributeError):
                # not present or TOPBAR list missing — ignore
                pass
            del LBFF_MT_template_menu._draw_fn
    except AttributeError:
        # bpy or TOPBAR list not present — ignore
        pass

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
