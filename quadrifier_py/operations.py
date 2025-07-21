import bpy

class MESH_OT_remesh(bpy.types.Operator):
    bl_idname = "mesh.remesh_operator"
    bl_label = "Remesh Operator"
    bl_description = "Perform topology optimization"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        obj_name = scene.retopo_target_object
        obj = scene.objects.get(obj_name)

        if not obj or obj.type != 'MESH':
            self.report({'WARNING'}, "No valid mesh object selected")
            return {'CANCELLED'}

        remesh_mode = scene.retopo_remesh_mode
        keep_original = scene.retopo_separate_object

        self.report({'INFO'}, f"Remeshing '{obj.name}' with mode '{remesh_mode}' (Keep original: {keep_original})")

        # rust kernel call here later

        return {'FINISHED'}


