import bpy


class LBFF_OT_import_minecraft_texture(bpy.types.Operator):
    """Imports a Minecraft texture and creates a material"""
    bl_idname = "lbff.import_minecraft_texture"
    bl_label = "Import Minecraft Texture"

    def execute(self, context):
        print("Importing Minecraft Texture...")
        # TODO: Add import logic here
        return {'FINISHED'}


classes = [LBFF_OT_import_minecraft_texture]
