"""Mat_Gold_24K — or sacre #C9963A poli, martelage subtil (bijoux N'Aset)."""
import bpy


def _lin(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


def _metal(name, hex_color, roughness, bump_scale=30.0, bump_strength=0.08):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    m.use_fake_user = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Base Color'].default_value = _lin(hex_color)
    b.inputs['Metallic'].default_value = 0.95
    b.inputs['Roughness'].default_value = roughness
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = bump_scale
    noise.inputs['Detail'].default_value = 6.0
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = bump_strength
    nt.links.new(noise.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return m, nt, b


def build():
    m, nt, b = _metal('Mat_Gold_24K', '#C9963A', 0.08)
    print('[SHADER] Mat_Gold_24K')
    return m


build()
