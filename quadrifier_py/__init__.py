bl_info = {
    "name": "Quadrifier",
    "author": "seventwogth",
    "version": (0, 1, 0),
    "blender": (4, 1, 0),
    "location": "View3D > Sidebar > Retopo",
    "description": "Optimizes mesh topology without changing the shape.",
    "category": "Mesh",
}

import bpy
from .user_interface import RetopoPanel
from .operations import MESH_OT_remesh

classes = (RetopoPanel, MESH_OT_remesh)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

