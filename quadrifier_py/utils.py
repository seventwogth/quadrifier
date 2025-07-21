def get_mesh_objects(self, context):
    return [(obj.name, obj.name, "") for obj in context.scene.objects if obj.type == 'MESH']

