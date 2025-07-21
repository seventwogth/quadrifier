import bpy

class RetopoPanel(bpy.types.Panel):
    bl_label = "Quadrifier"
    bl_idname = "VIEW3D_PT_quadrifier"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Quadrifier'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        col = layout.column()

        col.prop(scene, "retopo_target_object", text="Target")
        col.separator()
        col.label(text="Remesh Settings:")

        col.prop(scene, "retopo_remesh_mode")
        col.prop(scene, "retopo_separate_object")


        obj_name = scene.retopo_target_object
        obj = scene.objects.get(obj_name)
        if obj and obj.type == 'MESH':
            mesh = obj.data
            col.label(text=f"Vertices: {len(mesh.vertices)}")
            col.label(text=f"Edges: {len(mesh.edges)}")
            col.label(text=f"Polygons: {len(mesh.polygons)}")
        else:
            col.label(text="Select a mesh object")

        layout.operator("mesh.remesh_operator", text="Quadrify", icon="MOD_REMESH")

