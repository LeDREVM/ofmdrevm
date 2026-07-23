"""Mat_FX_Smoke — VOLUME fumee sombre (encens du temple). Domaine ferme."""
import bpy


def build():
    m = bpy.data.materials.get('Mat_FX_Smoke') or bpy.data.materials.new('Mat_FX_Smoke')
    m.use_nodes = True
    m.use_fake_user = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    vol = nt.nodes.new('ShaderNodeVolumePrincipled')
    vol.inputs['Color'].default_value = (0.06, 0.055, 0.07, 1.0)   # gris indigo
    if 'Anisotropy' in vol.inputs:
        vol.inputs['Anisotropy'].default_value = 0.2

    # Volutes : noise 4D etire vertical (animer W + monter le mapping en Z)
    coords = nt.nodes.new('ShaderNodeTexCoord')
    mapping = nt.nodes.new('ShaderNodeMapping')
    mapping.inputs['Scale'].default_value = (1.0, 1.0, 0.4)
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.noise_dimensions = '4D'
    noise.inputs['Scale'].default_value = 2.5
    noise.inputs['Detail'].default_value = 12.0
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.45
    ramp.color_ramp.elements[1].position = 0.8
    mul = nt.nodes.new('ShaderNodeMath')
    mul.operation = 'MULTIPLY'
    mul.inputs[1].default_value = 0.35
    nt.links.new(coords.outputs['Object'], mapping.inputs['Vector'])
    nt.links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], mul.inputs[0])
    nt.links.new(mul.outputs[0], vol.inputs['Density'])

    nt.links.new(vol.outputs['Volume'], out.inputs['Volume'])
    print('[SHADER] Mat_FX_Smoke (VOLUME volutes)')
    return m


build()
