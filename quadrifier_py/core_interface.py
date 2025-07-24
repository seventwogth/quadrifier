import bpy
import traceback
import os
import sys
from mathutils import Matrix, Vector

addon_dir = os.path.dirname(__file__)
if addon_dir not in sys.path:
    sys.path.append(addon_dir)

print(f"[Quadrifier] Added to sys.path: {addon_dir}")

import quadcore

def run_quadrifier(obj: bpy.types.Object, keep_original=True):
    try:
        print(f"[Quadrifier] Start processing: {obj.name}")

        mesh = obj.data
        matrix = obj.matrix_world

        vertices_world = [tuple(matrix @ v.co) for v in mesh.vertices]
        faces = [list(p.vertices) for p in mesh.polygons]

        print(f"[Quadrifier] Vertices: {len(vertices_world)}, Faces: {len(faces)}")

        new_vertices_world, new_faces = quadcore.recalculate_quads(vertices_world, faces)

        print(f"[Quadrifier] Got result: {len(new_vertices_world)} verts, {len(new_faces)} faces")

        if keep_original:
            new_mesh = bpy.data.meshes.new(name=f"{obj.name}_quadrified")
            new_obj = bpy.data.objects.new(name=f"{obj.name}_quadrified", object_data=new_mesh)
            bpy.context.collection.objects.link(new_obj)

            new_obj.matrix_world = Matrix.Identity(4)

            vertices_to_write = new_vertices_world

        else:
            inv = matrix.inverted()
            vertices_to_write = [tuple(inv @ Vector(v)) for v in new_vertices_world]

            new_mesh = mesh
            new_obj = obj

        new_mesh.clear_geometry()
        new_mesh.from_pydata(vertices_to_write, [], new_faces)
        new_mesh.update()

        print(f"[Quadrifier] Mesh updated successfully ({new_obj.name})")

    except Exception as e:
        print(f"[Quadrifier] Error: {e}")
        traceback.print_exc()

