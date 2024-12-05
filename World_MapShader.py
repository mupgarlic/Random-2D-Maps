#Basic World Generator
#by Bunny Ash / mupgarlic
#https://neko-glitch.myportfolio.com
#---------------------------------------

import bpy
import random #In case you want to randomize values

#Clear the scene entirely
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()
bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

#Add a plane
bpy.ops.mesh.primitive_plane_add()

#Create a new material
ob = bpy.context.active_object

mat = bpy.data.materials.get("Material")
if mat is None:
    
    mat = bpy.data.materials.new(name="World Map")

if ob.data.materials:

    ob.data.materials[0] = mat
else:
    
    ob.data.materials.append(mat)

#Prepare the node tree    
bpy.context.object.active_material.use_nodes = True

nodes = mat.node_tree.nodes

#Remove Principled BSDF
principled_bsdf = mat.node_tree.nodes['Principled BSDF']
mat.node_tree.nodes.remove(principled_bsdf)

#Add the new nodes
texCoord = nodes.new(type="ShaderNodeTexCoord")
texCoord.location = (-1140, 300)

mapp = nodes.new(type="ShaderNodeMapping")
mapp.location = (-955, 300)

noise = nodes.new(type="ShaderNodeTexNoise")
noise.location = (-774, 300)

L_colorR = nodes.new(type="ShaderNodeValToRGB")
L_colorR.location = (-603, 300)

snap = nodes.new(type="ShaderNodeMath")
snap.location = (-330, 300)
snap.operation = 'SNAP'
snap.inputs[1].default_value = -0.1

R_colorR = nodes.new(type="ShaderNodeValToRGB")
R_colorR.location = (-150, 300)

diff = nodes.new(type="ShaderNodeBsdfDiffuse")
diff.location = (122, 300)

#Modify the Noise Texture
noise.noise_dimensions = '4D'
noise.inputs[2].default_value = 0.3
noise.inputs[3].default_value = 15

noise.inputs[1].default_value = 0 #Seed number

#Modify the left Color Ramp
L_colorR.color_ramp.elements.new(0.5)

L_colorR.color_ramp.elements[0].position = 0.16
L_colorR.color_ramp.elements[0].color = (255, 255, 255, 1)

L_colorR.color_ramp.elements[1].color = (0, 0, 0, 1)

L_colorR.color_ramp.elements[2].position = 0.85

#Modify the right Color Ramp
R_colorR.color_ramp.interpolation = 'CONSTANT'
R_colorR.color_ramp.elements.new(0.5)

R_colorR.color_ramp.elements[0].color = (0.054, 0.084, 0.3, 1)

R_colorR.color_ramp.elements[1].position = 0.12
R_colorR.color_ramp.elements[1].color = (0.745, 0.760, 0.054, 1)

R_colorR.color_ramp.elements[2].position = 0.2
R_colorR.color_ramp.elements[2].color = (0.076, 0.485, 0.021, 1)

#Get the 'Material Output' node
m_out = mat.node_tree.nodes['Material Output']

#Connect the nodes
mat.node_tree.links.new(texCoord.outputs[3], mapp.inputs[0])
mat.node_tree.links.new(mapp.outputs[0], noise.inputs[0])
mat.node_tree.links.new(noise.outputs[0], L_colorR.inputs[0])
mat.node_tree.links.new(L_colorR.outputs[0], snap.inputs[0])
mat.node_tree.links.new(snap.outputs[0], R_colorR.inputs[0])
mat.node_tree.links.new(R_colorR.outputs[0], diff.inputs[0])
mat.node_tree.links.new(diff.outputs[0], m_out.inputs[0])

#Mapping node Location XYZ inputs
mapp.inputs[1].default_value[0] = 0
mapp.inputs[1].default_value[1] = 0
mapp.inputs[1].default_value[2] = 0