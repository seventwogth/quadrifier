try:
    import quadrifier_core
except ImportError:
    print("⚠️ Rust module 'quadrifier_core' not found. Run `maturin develop` or `pip install`.")

def run_remesh(obj, mode="AUTO", keep_original=True):
    mesh = obj.data

    verts = [(v.co.x, v.co.y, v.co.z) for v in mesh.vertices]

    mesh.calc_loop_triangles()
    tris = []
    for tri in mesh.loop_triangles:
        tris.append(tuple(mesh.loops[i].vertex_index for i in tri.loops))

    if not verts or not tris:
        print("⚠️ Object has no geometry")
        return

    try:
        new_verts, new_faces = quadrifier_core.process_mesh(verts, tris)
    except Exception as e:
        print(f"Error in Rust core: {e}")
        return

    print(f"Rust returned {len(new_verts)} verts, {len(new_faces)} faces")

