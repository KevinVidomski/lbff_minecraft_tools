import bpy
from .operators import LBFF_OT_import_minecraft_texture


class LBFF_MT_minecraft_importer_menu(bpy.types.Menu):
    bl_label = "Minecraft Importer"
    bl_idname = "LBFF_MT_minecraft_importer_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator(LBFF_OT_import_minecraft_texture.bl_idname)


classes = [LBFF_MT_minecraft_importer_menu]
