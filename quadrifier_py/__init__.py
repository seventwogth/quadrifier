bl_info = {
    "name": "Quadrifier",
    "author": "seventwogth (David M.)",
    "version": (0, 1, 0),
    "blender": (4, 1, 0),
    "location": "View3D > Sidebar > Quadrifier",
    "description": "Optimizes mesh topology without changing the shape.",
    "category": "Mesh",
}

import bpy
from .user_interface import RetopoPanel
from .operations import MESH_OT_remesh
from .utils import get_mesh_objects

classes = (RetopoPanel, MESH_OT_remesh)

def register():
    bpy.types.Scene.retopo_target_object = bpy.props.EnumProperty(
        name="Target Object",
        description="Mesh object to process",
        items=get_mesh_objects
    )

    bpy.types.Scene.retopo_remesh_mode = bpy.props.EnumProperty(
        name="Remesh Mode",
        description="Choose remeshing method",
        items=[
            ('QUAD', "Quads", "All-quads remesh"),
            ('TRI', "Tris", "Triangle-based remesh"),
            ('AUTO', "Auto", "Let system decide"),
        ],
        default='QUAD'
    )

    bpy.types.Scene.retopo_separate_object = bpy.props.BoolProperty(
        name="Keep Original",
        description="Output remeshed mesh as a new object",
        default=True
    )

    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.retopo_target_object
    del bpy.types.Scene.retopo_remesh_mode
    del bpy.types.Scene.retopo_separate_object


