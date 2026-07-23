"""Mat_Space_Moon — regolithe #E8E8F0, crateres 2 echelles, earthshine 0.4."""
import bpy


def _lin(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


def build():
    m = bpy.data.materials.get('Mat_Space_Moon') or bpy.data.materials.new('Mat_Space_Moon')
    m.use_nodes = True
    m.use_fake_user = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Base Color'].default_value = _lin('#E8E8F0')
    b.inputs['Roughness'].default_value = 0.85
    if 'Emission Color' in b.inputs:
        b.inputs['Emission Color'].default_value = _lin('#E8E8F0')
        b.inputs['Emission Strength'].default_value = 0.4   # earthshine — jamais plus

    # Crateres : grands (Scale 8) + petits impacts (Scale 25) mixes
    v1 = nt.nodes.new('ShaderNodeTexVoronoi')
    v1.inputs['Scale'].default_value = 8.0
    v2 = nt.nodes.new('ShaderNodeTexVoronoi')
    v2.inputs['Scale'].default_value = 25.0
    mix = nt.nodes.new('ShaderNodeMix')
    mix.data_type = 'FLOAT'
    mix.inputs['Factor'].default_value = 0.4
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.25
    nt.links.new(v1.outputs['Distance'], mix.inputs[2])
    nt.links.new(v2.outputs['Distance'], mix.inputs[3])
    nt.links.new(mix.outputs[0], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    print('[SHADER] Mat_Space_Moon')
    return m


build()
