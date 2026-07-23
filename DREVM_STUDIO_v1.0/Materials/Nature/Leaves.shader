"""Mat_Leaves — feuillage translucide (contre-jour savane) : Principled +
Translucent mixes par fresnel de lumiere."""
import bpy


def _lin(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


def build():
    m = bpy.data.materials.get('Mat_Leaves') or bpy.data.materials.new('Mat_Leaves')
    m.use_nodes = True
    m.use_fake_user = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')

    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Base Color'].default_value = _lin('#4E5B26')   # vert savane sec
    b.inputs['Roughness'].default_value = 0.6

    # Translucidite : la lumiere traverse la feuille au contre-jour
    trans = nt.nodes.new('ShaderNodeBsdfTranslucent')
    trans.inputs['Color'].default_value = _lin('#8FA33F')    # vert lumineux traverse

    mix = nt.nodes.new('ShaderNodeMixShader')
    mix.inputs['Fac'].default_value = 0.35
    nt.links.new(b.outputs['BSDF'], mix.inputs[1])
    nt.links.new(trans.outputs['BSDF'], mix.inputs[2])
    nt.links.new(mix.outputs['Shader'], out.inputs['Surface'])

    # Nervures : wave -> bump
    wave = nt.nodes.new('ShaderNodeTexWave')
    wave.inputs['Scale'].default_value = 30.0
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.1
    nt.links.new(wave.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    print('[SHADER] Mat_Leaves')
    return m


build()
