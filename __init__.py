bl_info = {
    "name": "LittleHelpers Addon",
    "description": "A collection of helper functions",
    "author": "Tobias Wilhelm (biteworks)",
    "version": (1, 0, 3),
    "blender": (2, 90, 0),
    "location": "3D View > Tools > LittleHelpers",
    "category": "Generic"
}

import bpy
import addon_utils
from . props import *
from . operators import *
from . ui import *

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    LittleHelpersProperties,
    OT_DuplicateMirrorRename,
    OT_DeleteMaterialsFromSelected,
    PT_LittleHelpersPanel
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.littlehelpersprops = bpy.props.PointerProperty(type=LittleHelpersProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.littlehelpersprops


if __name__ == "__main__":
    register()