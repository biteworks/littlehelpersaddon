import bpy
import addon_utils

class OBJ_OT_DuplicateMirrorRename(bpy.types.Operator):
    bl_label = "Duplicate and mirror selected objects"
    bl_idname = "littlehelpers.duplicatemirrorrename"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = bpy.context.scene
        littlehelpersprops = scn.littlehelpersprops

        selectedObjects = bpy.context.selected_objects

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
                    bpy.ops.transform.mirror(orient_type='GLOBAL', constraint_axis=(littlehelpersprops.xAxis, littlehelpersprops.yAxis, littlehelpersprops.zAxis), use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    bpy.ops.object.select_all(action='DESELECT')

        else:
            self.report({'ERROR'}, "Nothing selected")
            print('Nothing selected')

        return {'FINISHED'}


class OBJ_OT_PurgeOrphanData(bpy.types.Operator):
    bl_label = "Purge Orphan Data"
    bl_idname = "littlehelpers.purgeorphandata"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.outliner.orphans_purge()

        return {'FINISHED'}


class OBJ_OT_DeleteMaterialsFromSelected(bpy.types.Operator):
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