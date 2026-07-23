"""Mat_Sand — sable savane #B08A50, grain fin + ondulations de vent."""
import bpy


def _lin(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


def build():
    m = bpy.data.materials.get('Mat_Sand') or bpy.data.materials.new('Mat_Sand')
    m.use_nodes = True
    m.use_fake_user = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Roughness'].default_value = 0.9

    # Couleur : sable -> or clair dans les hautes zones du noise
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 45.0
    noise.inputs['Detail'].default_value = 8.0
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = _lin('#B08A50')
    ramp.color_ramp.elements[1].color = _lin('#C9A365')
    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])

    # Ondulations de vent (grandes vagues) + grain (petit bump)
    wave = nt.nodes.new('ShaderNodeTexWave')
    wave.inputs['Scale'].default_value = 2.0
    wave.inputs['Distortion'].default_value = 6.0
    bump1 = nt.nodes.new('ShaderNodeBump')
    bump1.inputs['Strength'].default_value = 0.15
    nt.links.new(wave.outputs['Fac'], bump1.inputs['Height'])
    grain = nt.nodes.new('ShaderNodeTexNoise')
    grain.inputs['Scale'].default_value = 400.0
    bump2 = nt.nodes.new('ShaderNodeBump')
    bump2.inputs['Strength'].default_value = 0.05
    nt.links.new(grain.outputs['Fac'], bump2.inputs['Height'])
    nt.links.new(bump1.outputs['Normal'], bump2.inputs['Normal'])
    nt.links.new(bump2.outputs['Normal'], b.inputs['Normal'])

    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    print('[SHADER] Mat_Sand')
    return m


build()
