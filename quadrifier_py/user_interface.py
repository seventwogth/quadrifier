import bpy

class RetopoPanel(bpy.types.Panel):
    bl_label = "Quadrifier"
    bl_idname = "VIEW3D_PT_quadrifier"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Retopo'

    def draw(self, context):
        layout = self.layout
        layout.operator("mesh.remesh_operator", text="Quadrify", icon="MOD_REMESH")

