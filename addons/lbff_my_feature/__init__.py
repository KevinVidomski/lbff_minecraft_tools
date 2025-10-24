bl_info = {
    "name": "LBFF My Feature",
    "author": "Contributor",
    "version": (0, 1),
    "blender": (3, 0, 0),
    "location": "",
    "description": "Example addon scaffold for LBFF (safe to import in tests).",
    "category": "Development",
}

import sys

try:
    import bpy
except Exception:
    # Allow import-time in test environments that inject a fake 'bpy'
    bpy = sys.modules.get("bpy")


class LBFF_OT_my_action:
    """Placeholder operator (kept as simple object because tests inject fake bpy)."""


class LBFF_MT_my_menu:
    """Placeholder menu class used for draw callback naming.

    In a real Blender environment these would inherit from `bpy.types.Operator`/`bpy.types.Menu`.
    Tests use a fake `bpy` so this module keeps a minimal, import-safe shape.
    """


# For runtime in Blender, provide simple classes using bpy.types when available.
classes = []

if bpy:
    class LBFF_OT_my_action(bpy.types.Operator):
        bl_idname = "lbff.my_action"
        bl_label = "LBFF My Action"

        def execute(self, context):
            return {"FINISHED"}

    class LBFF_MT_my_menu(bpy.types.Menu):
        bl_label = "My Feature"
        bl_idname = "LBFF_MT_my_feature"

        def draw(self, context):
            self.layout.operator(LBFF_OT_my_action.bl_idname)

    classes = [LBFF_OT_my_action, LBFF_MT_my_menu]


def _make_draw_fn():
    return lambda self, context: self.layout.menu(LBFF_MT_my_menu.bl_idname)


def register():
    # Register classes if bpy is the real module
    if not bpy:
        return

    for cls in classes:
        bpy.utils.register_class(cls)

    draw_fn = _make_draw_fn()
    LBFF_MT_my_menu._draw_fn = draw_fn

    # Prefer attaching to the main LBFF menu if present, otherwise topbar
    try:
        bpy.types.LBFF_MT_main_menu.append(draw_fn)
    except Exception:
        bpy.types.TOPBAR_MT_editor_menus.append(draw_fn)


def unregister():
    if not bpy:
        return

    # Remove draw callback if stored
    if hasattr(LBFF_MT_my_menu, "_draw_fn"):
        fn = LBFF_MT_my_menu._draw_fn
        for container in (getattr(bpy.types, "LBFF_MT_main_menu", None), getattr(bpy.types, "TOPBAR_MT_editor_menus", None)):
            try:
                if container is not None:
                    container.remove(fn)
            except Exception:
                pass
        del LBFF_MT_my_menu._draw_fn

    # Unregister classes in reverse order
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except Exception:
            pass


if __name__ == "__main__":
    register()
