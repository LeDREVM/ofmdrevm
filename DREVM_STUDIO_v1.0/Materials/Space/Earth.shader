"""Mat_Space_Earth — Terre procedurale : oceans/continents/nuages par noise."""
import bpy


def _lin(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


def build():
    m = bpy.data.materials.get('Mat_Space_Earth') or bpy.data.materials.new('Mat_Space_Earth')
    m.use_nodes = True
    m.use_fake_user = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Roughness'].default_value = 0.45

    # Continents : noise seuil ocean/terre
    conti = nt.nodes.new('ShaderNodeTexNoise')
    conti.inputs['Scale'].default_value = 2.2
    conti.inputs['Detail'].default_value = 12.0
    ramp_c = nt.nodes.new('ShaderNodeValToRGB')
    ramp_c.color_ramp.elements[0].position = 0.48
    ramp_c.color_ramp.elements[0].color = _lin('#123A6B')   # ocean profond
    ramp_c.color_ramp.elements[1].position = 0.55
    ramp_c.color_ramp.elements[1].color = _lin('#4E6B2A')   # terres

    # Nuages : 2e noise ajoute en blanc
    clouds = nt.nodes.new('ShaderNodeTexNoise')
    clouds.inputs['Scale'].default_value = 5.0
    clouds.inputs['Detail'].default_value = 10.0
    ramp_n = nt.nodes.new('ShaderNodeValToRGB')
    ramp_n.color_ramp.elements[0].position = 0.62
    ramp_n.color_ramp.elements[0].color = (0, 0, 0, 1)
    ramp_n.color_ramp.elements[1].position = 0.75
    ramp_n.color_ramp.elements[1].color = (1, 1, 1, 1)

    mix = nt.nodes.new('ShaderNodeMix')
    mix.data_type = 'RGBA'
    mix.blend_type = 'SCREEN'
    mix.inputs['Factor'].default_value = 0.85
    nt.links.new(conti.outputs['Fac'], ramp_c.inputs['Fac'])
    nt.links.new(clouds.outputs['Fac'], ramp_n.inputs['Fac'])
    nt.links.new(ramp_c.outputs['Color'], mix.inputs[6])
    nt.links.new(ramp_n.outputs['Color'], mix.inputs[7])
    nt.links.new(mix.outputs[2], b.inputs['Base Color'])
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    print('[SHADER] Mat_Space_Earth')
    return m


build()
