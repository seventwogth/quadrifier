import bpy

class MESH_OT_remesh(bpy.types.Operator):
    bl_idname = "mesh.remesh_operator"
    bl_label = "Remesh Operator"
    bl_description = "Performs topology optimization"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        obj_name = scene.retopo_target_object
        obj = scene.objects.get(obj_name)

        if not obj:
            self.report({'WARNING'}, "No object selected")
            return {'CANCELLED'}

        if obj.type != 'MESH':
            self.report({'WARNING'}, f"Object '{obj.name}' is not a mesh")
            return {'CANCELLED'}
        
        #rust kernell call here later
        self.report({'INFO'}, f"Remeshing: {obj.name} (Verts: {len(obj.data.vertices)})")
        return {'FINISHED'}

