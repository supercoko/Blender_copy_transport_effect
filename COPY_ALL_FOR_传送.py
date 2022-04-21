import bpy


obs = bpy.context.selected_objects
# 复制属性
# bpy.data.objects['展示模型'].select = True
bpy.context.view_layer.objects.active = bpy.data.objects['展示模型']
bpy.ops.object.modifier_copy_to_selected(modifier="VertexWeightProximity")
bpy.ops.object.modifier_copy_to_selected(modifier="VertexWeightProximity.001")
bpy.ops.object.modifier_copy_to_selected(modifier="置换")
bpy.ops.object.modifier_copy_to_selected(modifier="置换.001")
bpy.ops.object.modifier_copy_to_selected(modifier="传送")
#for ob in obs:
#    if ob.type == 'MESH':
for ob in obs:
    ob.select = False
for ob in obs:
    bpy.context.view_layer.objects.active = ob
    ob.select = True
    bpy.ops.object.mode_set(mode='EDIT') 
    
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.context.object.vertex_groups.new(name='A')
    bpy.ops.object.vertex_group_assign()
    bpy.context.object.vertex_groups.new(name='B')
    bpy.ops.object.vertex_group_assign()
    
    bpy.ops.object.mode_set(mode='OBJECT')
    ob.select = False

    nodes = bpy.context.active_object.active_material.node_tree.nodes
    links = bpy.context.active_object.active_material.node_tree.links
    
    # 获取当前激活的objdect 的 material
    material_act = bpy.context.active_object.active_material
    # 改变透明方法
    material_act.blend_method = 'HASHED'
    material_act.shadow_method = 'HASHED'

    # 添加要用的组
    new_group = material_act.node_tree.nodes.new(type='ShaderNodeGroup')
    # 获取要添加的组
    
    for ng in bpy.data.node_groups:
        if ng.name == "传送shader":
            new_group.node_tree = ng
            break
    
    # 获取link
    # 材质输出 Material Output
    for l in material_act.node_tree.links:
        if l.to_node.name == 'Material Output':# or 
            link_AB = l
            break

    # 获取link_A 的 from node 并找到其连接端点
        # from 的node是out put 找到其连接的点
    for i in link_AB.from_node.outputs:
        if i.is_linked:
            link_node_A = i
            break
    # 连接 
    # 材质输出 Material Output
    links.new(link_node_A, new_group.inputs[0])
    links.new(new_group.outputs[0], nodes.get('Material Output').inputs[0])


    bpy.context.object.particle_systems["传送"].vertex_group_density = "A"
    bpy.context.object.particle_systems["传送"].vertex_group_length = "A"
    bpy.context.object.particle_systems["传送"].vertex_group_clump = "A"
    bpy.context.object.particle_systems["传送"].vertex_group_kink = "A"
    bpy.context.object.particle_systems["传送"].vertex_group_roughness_1 = "A"
    bpy.context.object.particle_systems["传送"].vertex_group_roughness_2 = "A"
    bpy.context.object.particle_systems["传送"].vertex_group_roughness_end = "A"
    bpy.context.object.particle_systems["传送"].vertex_group_twist = "A"






