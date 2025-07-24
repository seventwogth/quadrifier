import bpy
import bmesh
import traceback
import os
import sys
from mathutils import Matrix, Vector

addon_dir = os.path.dirname(__file__)
if addon_dir not in sys.path:
    sys.path.append(addon_dir)
print(f"[Quadrifier] Added to sys.path: {addon_dir}")

import quadcore

def find_boundary_loops(bm):
    boundary_edges = {e for e in bm.edges if len(e.link_faces) == 1}
    loops = []

    while boundary_edges:
        start = next(iter(boundary_edges))
        loop = [start]
        boundary_edges.remove(start)

        v_start = start.verts[0]
        v_next = start.verts[1]
        current = v_next

        while True:
            found = False
            for e in current.link_edges:
                if e in boundary_edges:
                    loop.append(e)
                    boundary_edges.remove(e)
                    current = e.other_vert(current)
                    found = True
                    break
            if not found or current == v_start:
                break

        if len(loop) >= 3:
            loops.append(loop)

    return loops

def run_quadrifier(obj: bpy.types.Object, keep_original=True):
    try:
        print(f"[Quadrifier] Start processing: {obj.name}")

        mesh = obj.data
        matrix = obj.matrix_world

        vertices_world = [tuple(matrix @ v.co) for v in mesh.vertices]
        faces = [list(p.vertices) for p in mesh.polygons]

        print(f"[Quadrifier] Input: {len(vertices_world)} verts, {len(faces)} faces")

        new_vertices_world, new_faces = quadcore.recalculate_quads(vertices_world, faces)
        print(f"[Quadrifier] Rust returned: {len(new_vertices_world)} verts, {len(new_faces)} faces")

        if keep_original:
            new_mesh = bpy.data.meshes.new(name=f"{obj.name}_quadrified")
            new_obj  = bpy.data.objects.new(name=f"{obj.name}_quadrified", object_data=new_mesh)
            bpy.context.collection.objects.link(new_obj)
            new_obj.matrix_world = Matrix.Identity(4)
            vertices_to_write = new_vertices_world
        else:
            inv = matrix.inverted()
            vertices_to_write = [tuple(inv @ Vector(v)) for v in new_vertices_world]
            new_mesh = mesh
            new_obj  = obj

        new_mesh.clear_geometry()
        new_mesh.from_pydata(vertices_to_write, [], new_faces)
        new_mesh.update()

        print(f"[Quadrifier] Mesh base written")

        bm = bmesh.new()
        bm.from_mesh(new_mesh)
        bm.faces.ensure_lookup_table()
        bm.edges.ensure_lookup_table()

        loops = find_boundary_loops(bm)
        print(f"[Quadrifier] Found {len(loops)} boundary loops")

        for loop_edges in loops:
            if len(loop_edges) >= 3:
                try:
                    bmesh.ops.grid_fill(bm, edges=loop_edges)
                except Exception as fill_err:
                    print(f"[Quadrifier] Grid fill failed on loop ({len(loop_edges)} edges): {fill_err}")

        bm.to_mesh(new_mesh)
        new_mesh.update()
        bm.free()

        print(f"[Quadrifier] Grid fill complete")

    except Exception as e:
        print(f"[Quadrifier] Error: {e}")
        traceback.print_exc()

