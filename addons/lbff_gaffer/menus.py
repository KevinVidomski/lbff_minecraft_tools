import bpy
from .operators import LBFF_OT_gaffer_create_lighting


class LBFF_MT_gaffer_menu(bpy.types.Menu):
    bl_label = "Gaffer"
    bl_idname = "LBFF_MT_gaffer_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator(LBFF_OT_gaffer_create_lighting.bl_idname)


classes = [LBFF_MT_gaffer_menu]
