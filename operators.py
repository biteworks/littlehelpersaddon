import bpy
import addon_utils

# ------------------------------------------------------------------------
#    Duplicate, Mirror and Rename - Operator
# ------------------------------------------------------------------------

class OT_DuplicateMirrorRename(bpy.types.Operator):
    bl_label = "Duplicate and mirror selected objects"
    bl_idname = "littlehelpers.duplicatemirrorrename"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = bpy.context.scene
        littlehelpersprops = scn.littlehelpersprops

        selectedObjects = bpy.context.selected_objects

        # Set axis variables for Blender 2.92 and higher
        if littlehelpersprops.xAxis:
            xAxis = -1.0
        else:
            xAxis = 1.0

        if littlehelpersprops.yAxis:
            yAxis = -1.0
        else:
            yAxis = 1.0

        if littlehelpersprops.zAxis:
            zAxis = -1.0
        else: 
            zAxis = 1.0

        if len(selectedObjects) > 0:
            for obj in selectedObjects:
                if obj.type == "MESH":
                    objName = obj.name
                    
                    newObj = obj.copy ()
                    newObj.data = obj.data.copy ()
                    
                    if len(obj.users_collection):
                        obj.users_collection[0].objects.link(newObj)
                    else:
                        scn.collection.objects.link(newObj)
                    
                    if(littlehelpersprops.renamingOn) and (littlehelpersprops.searchString != '') and (littlehelpersprops.replaceString != ''):
                        newObj.name = objName.replace(littlehelpersprops.searchString,littlehelpersprops.replaceString)
                    else:
                        newObj.name = objName + "_mirrored"
                    
                    bpy.ops.object.select_all(action='DESELECT')
                    newObj.select_set(state=True)
                    bpy.context.view_layer.objects.active = newObj
                    bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
                    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

                    # Switch for Blender 2.92 and higher
                    if bpy.app.version[0] >= 2 and bpy.app.version[1] < 92:
                        bpy.ops.transform.mirror(orient_type='GLOBAL', constraint_axis=(littlehelpersprops.xAxis, littlehelpersprops.yAxis, littlehelpersprops.zAxis), use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                    else:
                        bpy.ops.transform.resize(value=(xAxis, yAxis, zAxis), orient_type='GLOBAL', use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                    
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    bpy.ops.object.select_all(action='DESELECT')

        else:
            self.report({'ERROR'}, "Nothing selected")
            print('Nothing selected')

        return {'FINISHED'}

# ------------------------------------------------------------------------
#    Delete all matrials from selected object - Operator
# ------------------------------------------------------------------------

class OT_DeleteMaterialsFromSelected(bpy.types.Operator):
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