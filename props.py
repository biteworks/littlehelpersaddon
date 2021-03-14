import bpy
import addon_utils

class LittleHelpersProperties(bpy.types.PropertyGroup):
    xAxis: bpy.props.BoolProperty(
        name="X-Axis",
        description="X-Axis",
        default = False
        )

    yAxis: bpy.props.BoolProperty(
        name="Y-Axis",
        description="Y-Axis",
        default = True
        )

    zAxis: bpy.props.BoolProperty(
        name="Z-Axis",
        description="Z-Axis",
        default = False
        )

    renamingOn: bpy.props.BoolProperty(
        name="Renaming",
        description="Renaming on/off",
        default = False
        )

    searchString: bpy.props.StringProperty(
        name="searchString",
        description="Find string",
        default="",
        maxlen=1024,
        )
    replaceString: bpy.props.StringProperty(
        name="replaceString",
        description="Replace with",
        default="",
        maxlen=1024,
        )