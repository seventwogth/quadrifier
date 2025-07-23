import bpy
import bmesh
import traceback
from mathutils import Vector
import os
import sys

addon_dir = os.path.dirname(__file__)
if addon_dir not in sys.path:
    sys.path.append(addon_dir)

print(f"[Quadrifier] Added to sys.path: {addon_dir}")

import quadcore

def run_quadrifier(obj: bpy.types.Object, keep_original=True):
    try:
        print(f"[Quadrifier] Start processing: {obj.name}")
        
        mesh = obj.data
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bm.verts.ensure_lookup_table()
        bm.faces.ensure_lookup_table()

        vertices = [tuple(v.co) for v in bm.verts]
        faces = [[v.index for v in f.verts] for f in bm.faces]

        print(f"[Quadrifier] Vertices: {len(vertices)}, Faces: {len(faces)}")

        new_vertices, new_faces = quadcore.recalculate_quads(vertices, faces)

        print(f"[Quadrifier] Got result: {len(new_vertices)} verts, {len(new_faces)} faces")

        if keep_original:
            new_mesh = bpy.data.meshes.new(name=f"{obj.name}_quadrified")
            new_obj = bpy.data.objects.new(name=f"{obj.name}_quadrified", object_data=new_mesh)
            bpy.context.collection.objects.link(new_obj)
        else:
            new_mesh = mesh
            new_obj = obj

        new_mesh.from_pydata(new_vertices, [], new_faces)
        new_mesh.update()

        print(f"[Quadrifier] Mesh updated successfully")

    except Exception as e:
        print(f"[Quadrifier] Error: {e}")
        traceback.print_exc()

