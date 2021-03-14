import bpy
import addon_utils

class OBJECT_PT_LittleHelpersPanel(bpy.types.Panel):
    bl_label = "LittleHelpers Addon"
    bl_idname = "OBJECT_PT_custom_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "LittleHelpers"

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        littlehelpersprops = scn.littlehelpersprops
        
        # Duplicat/Mirror/Rename box
        self.layout.label(text="Duplicate/Mirror/Rename", icon='MOD_MIRROR')
        box = layout.box()
        row = box.row()
        row.label(text="Select mirror axis")
        row = box.row()
        row.prop(littlehelpersprops, "xAxis", text="X", toggle=True)
        row.prop(littlehelpersprops, "yAxis", text="Y", toggle=True)
        row.prop(littlehelpersprops, "zAxis", text="Z", toggle=True)
        row = box.row()
        row.prop(littlehelpersprops, "renamingOn", text="Find/Replace")
        if littlehelpersprops.renamingOn:
            row = box.row()
            row.prop(littlehelpersprops, "searchString", text="Find")
            row = box.row()
            row.prop(littlehelpersprops, "replaceString", text="Replace")
        row = box.row()
        row.operator("littlehelpers.duplicatemirrorrename")
        
        # Scene cleaning box
        self.layout.label(text="Scene cleanup", icon="SCENE_DATA")
        box = layout.box()
        row = box.row()
        row.operator("littlehelpers.deletematerialsfromselected")
        row = box.row()
        row.operator("littlehelpers.purgeorphandata")