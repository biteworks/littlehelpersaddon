bl_info = {
    "name": "LittleHelpers Addon",
    "description": "A collection of little helper functions",
    "author": "Tobias Wilhelm (biteworks)",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "3D View > Tools",
    "category": "Generic"
}


import bpy

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )


# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class MyProperties(PropertyGroup):
    
    xAxis: BoolProperty(
        name="X-Axis",
        description="X-Axis",
        default = False
        )

    yAxis: BoolProperty(
        name="Y-Axis",
        description="Y-Axis",
        default = True
        )

    zAxis: BoolProperty(
        name="Z-Axis",
        description="Z-Axis",
        default = False
        )

    renamingOn: BoolProperty(
        name="Renaming",
        description="Renaming on/off",
        default = False
        )

    searchString: StringProperty(
        name="searchString",
        description="Find string",
        default="",
        maxlen=1024,
        )
    replaceString: StringProperty(
        name="replaceString",
        description="Replace with",
        default="",
        maxlen=1024,
        )

# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------

class OBJ_OT_DuplicateMirrorRename(Operator):
    bl_label = "Duplicate and mirror selected objects"
    bl_idname = "littlehelpers.duplicatemirrorrename"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = bpy.context.scene
        littlehelpersprops = scn.littlehelpersprops

        selectedObjects = bpy.context.selected_objects

        if len(selectedObjects) > 0:
            for obj in selectedObjects:
                objName = obj.name
                
                newObj = obj.copy ()
                newObj.data = obj.data.copy ()
                
                if len(obj.users_collection):
                    obj.users_collection[0].objects.link(newObj)
                else:
                    scn.collection.objects.link(newObj)
                
                if(littlehelpersprops.renamingOn) and (littlehelpersprops.searchString != '') and (littlehelpersprops.replaceString != ''):
                    newObj.name = objName.replace(duplicateMirrorTool.searchString,duplicateMirrorTool.replaceString)
                else:
                    newObj.name = objName + "_mirrored"
                
                bpy.ops.object.select_all(action='DESELECT')
                newObj.select_set(state=True)
                bpy.context.view_layer.objects.active = newObj
                bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
                bpy.ops.transform.mirror(orient_type='GLOBAL', constraint_axis=(littlehelpersprops.xAxis, littlehelpersprops.yAxis, littlehelpersprops.zAxis), use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                bpy.ops.object.select_all(action='DESELECT')

        else:
            self.report({'ERROR'}, "Nothing selected")
            print('Nothing selected')

        return {'FINISHED'}


class OBJ_OT_PurgeOrphanData(Operator):
    bl_label = "Purge Orphan Data"
    bl_idname = "littlehelpers.purgeorphandata"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.outliner.orphans_purge()

        return {'FINISHED'}


class OBJ_OT_DeleteMaterialsFromSelected(Operator):
    bl_label = "Delete Materials from selected"
    bl_idname = "littlehelpers.deletematerialsfromselected"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selectedObjects = bpy.context.selected_objects
 
        listOfObjs=[]
        for obj in selectedObjects:
            listOfObjs.append(obj)
            bpy.context.view_layer.objects.active = obj
            for slot in obj.material_slots:
                obj.active_material_index = 0
                bpy.ops.object.material_slot_remove()

        return {'FINISHED'}


# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------

class OBJECT_PT_LittleHelpersPanel(Panel):
    bl_label = "LittleHelpers Addon"
    bl_idname = "OBJECT_PT_custom_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "LittleHelpers"
    bl_context = "objectmode"

    @classmethod
    def poll(self,context):
        return context.object is not None

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
        row.prop(littlehelpersprops, "renamingOn", text="Find/Replace enabled")
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

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    MyProperties,
    OBJ_OT_DuplicateMirrorRename,
    OBJ_OT_PurgeOrphanData,
    OBJ_OT_DeleteMaterialsFromSelected,
    OBJECT_PT_LittleHelpersPanel
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.littlehelpersprops = PointerProperty(type=MyProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.littlehelpersprops


if __name__ == "__main__":
    register()