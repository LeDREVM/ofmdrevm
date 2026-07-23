"""Mat_Water_Ocean — ocean profond : transmission + absorption teal + houle bump."""
import bpy


def _lin(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


def build():
    m = bpy.data.materials.get('Mat_Water_Ocean') or bpy.data.materials.new('Mat_Water_Ocean')
    m.use_nodes = True
    m.use_fake_user = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')

    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
    b.inputs['Roughness'].default_value = 0.05
    b.inputs['IOR'].default_value = 1.33
    if 'Transmission Weight' in b.inputs:
        b.inputs['Transmission Weight'].default_value = 1.0

    # Profondeur : absorption teal (volume)
    absorb = nt.nodes.new('ShaderNodeVolumeAbsorption')
    absorb.inputs['Color'].default_value = _lin('#1A6B6B')
    absorb.inputs['Density'].default_value = 0.35
    nt.links.new(absorb.outputs['Volume'], out.inputs['Volume'])

    # Houle : 2 noises (grande houle + clapot)
    n1 = nt.nodes.new('ShaderNodeTexNoise')
    n1.inputs['Scale'].default_value = 0.6
    n1.inputs['Detail'].default_value = 4.0
    b1 = nt.nodes.new('ShaderNodeBump')
    b1.inputs['Strength'].default_value = 0.3
    n2 = nt.nodes.new('ShaderNodeTexNoise')
    n2.inputs['Scale'].default_value = 12.0
    b2 = nt.nodes.new('ShaderNodeBump')
    b2.inputs['Strength'].default_value = 0.08
    nt.links.new(n1.outputs['Fac'], b1.inputs['Height'])
    nt.links.new(n2.outputs['Fac'], b2.inputs['Height'])
    nt.links.new(b1.outputs['Normal'], b2.inputs['Normal'])
    nt.links.new(b2.outputs['Normal'], b.inputs['Normal'])

    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    print('[SHADER] Mat_Water_Ocean')
    return m


build()
