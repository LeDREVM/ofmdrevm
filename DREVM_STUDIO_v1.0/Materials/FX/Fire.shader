"""Mat_FX_Fire — VOLUME feu (Ordre du Feu Mystique) : densite noise +
blackbody simule par ramp or->rouge. Assigner a un domaine ferme."""
import bpy


def _lin(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


def build():
    m = bpy.data.materials.get('Mat_FX_Fire') or bpy.data.materials.new('Mat_FX_Fire')
    m.use_nodes = True
    m.use_fake_user = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    vol = nt.nodes.new('ShaderNodeVolumePrincipled')
    vol.inputs['Density'].default_value = 0.0   # le feu emet, il n'absorbe presque pas

    # Langues de feu : noise 4D etire en Z (animer W : driver #frame/25)
    coords = nt.nodes.new('ShaderNodeTexCoord')
    mapping = nt.nodes.new('ShaderNodeMapping')
    mapping.inputs['Scale'].default_value = (1.0, 1.0, 0.35)   # etirement vertical
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.noise_dimensions = '4D'
    noise.inputs['Scale'].default_value = 3.0
    noise.inputs['Detail'].default_value = 10.0
    nt.links.new(coords.outputs['Object'], mapping.inputs['Vector'])
    nt.links.new(mapping.outputs['Vector'], noise.inputs['Vector'])

    # Gradient thermique : transparent -> rouge -> or -> presque blanc
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    e0 = ramp.color_ramp.elements[0]
    e0.position = 0.45
    e0.color = (0, 0, 0, 1)
    e1 = ramp.color_ramp.elements[1]
    e1.position = 0.75
    e1.color = _lin('#C0392B')
    e2 = ramp.color_ramp.elements.new(0.92)
    e2.color = _lin('#E8BC6A')

    strength = nt.nodes.new('ShaderNodeMath')
    strength.operation = 'MULTIPLY'
    strength.inputs[1].default_value = 14.0
    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], vol.inputs['Emission Color'])
    nt.links.new(noise.outputs['Fac'], strength.inputs[0])
    nt.links.new(strength.outputs[0], vol.inputs['Emission Strength'])

    nt.links.new(vol.outputs['Volume'], out.inputs['Volume'])
    print('[SHADER] Mat_FX_Fire (VOLUME — animer noise W)')
    return m


build()
