"""Mat_Fabric_Maasai — tartan shuka procedural : damier #C0392B / #8E2A20
+ fines bandes #1C1A3A, sheen coton, translucidite contre-jour."""
import bpy


def _lin(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


def build():
    m = bpy.data.materials.get('Mat_Fabric_Maasai') or bpy.data.materials.new('Mat_Fabric_Maasai')
    m.use_nodes = True
    m.use_fake_user = True
    nt = m.node_tree
    nt.nodes.clear()

    out = nt.nodes.new('ShaderNodeOutputMaterial')
    b = nt.nodes.new('ShaderNodeBsdfPrincipled')

    # Tartan : 2 vagues carrees croisees (X et Y) via Brick
    coords = nt.nodes.new('ShaderNodeTexCoord')
    mapping = nt.nodes.new('ShaderNodeMapping')
    mapping.inputs['Scale'].default_value = (12.0, 12.0, 12.0)
    nt.links.new(coords.outputs['UV'], mapping.inputs['Vector'])

    brick_h = nt.nodes.new('ShaderNodeTexBrick')
    brick_h.inputs['Color1'].default_value = _lin('#C0392B')
    brick_h.inputs['Color2'].default_value = _lin('#8E2A20')
    brick_h.inputs['Mortar'].default_value = _lin('#1C1A3A')
    brick_h.inputs['Mortar Size'].default_value = 0.01
    brick_h.inputs['Scale'].default_value = 1.0
    nt.links.new(mapping.outputs['Vector'], brick_h.inputs['Vector'])

    brick_v = nt.nodes.new('ShaderNodeTexBrick')
    for k in ('Color1', 'Color2', 'Mortar'):
        brick_v.inputs[k].default_value = brick_h.inputs[k].default_value
    brick_v.inputs['Mortar Size'].default_value = 0.01
    rot = nt.nodes.new('ShaderNodeMapping')
    rot.inputs['Rotation'].default_value = (0, 0, 1.5708)   # 90 deg
    nt.links.new(mapping.outputs['Vector'], rot.inputs['Vector'])
    nt.links.new(rot.outputs['Vector'], brick_v.inputs['Vector'])

    mix = nt.nodes.new('ShaderNodeMix')
    mix.data_type = 'RGBA'
    mix.blend_type = 'MULTIPLY'
    mix.inputs['Factor'].default_value = 0.5
    nt.links.new(brick_h.outputs['Color'], mix.inputs[6])
    nt.links.new(brick_v.outputs['Color'], mix.inputs[7])
    nt.links.new(mix.outputs[2], b.inputs['Base Color'])

    b.inputs['Roughness'].default_value = 0.55
    if 'Sheen Weight' in b.inputs:
        b.inputs['Sheen Weight'].default_value = 0.3
    if 'Transmission Weight' in b.inputs:
        b.inputs['Transmission Weight'].default_value = 0.08   # contre-jour S1

    # Tissage : wave fine -> bump
    wave = nt.nodes.new('ShaderNodeTexWave')
    wave.inputs['Scale'].default_value = 250.0
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.02
    nt.links.new(wave.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])

    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    print('[SHADER] Mat_Fabric_Maasai (tartan procedural)')
    return m


build()
