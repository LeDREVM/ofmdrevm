"""Mat_Skin_Dark — peau brun dore #6B3D2E, SSS chaud (base N'Aset)."""
import bpy


def _lin(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


def _mat(name):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    m.use_fake_user = True
    m.node_tree.nodes.clear()
    nt = m.node_tree
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return m, nt, b


def _set(b, k, v):
    s = b.inputs.get(k)
    if s:
        s.default_value = v


def build():
    m, nt, b = _mat('Mat_Skin_Dark')
    # Variation chaude #6B3D2E -> #8B4E35 (zones irriguees)
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 20.0
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = _lin('#6B3D2E')
    ramp.color_ramp.elements[1].color = _lin('#8B4E35')
    ramp.color_ramp.elements[1].position = 0.75
    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])

    _set(b, 'Subsurface Weight', 0.3)     # Blender 5 : Weight + Scale separes
    _set(b, 'Subsurface Scale', 0.05)
    _set(b, 'Subsurface Radius', (0.36, 0.20, 0.12))
    _set(b, 'Roughness', 0.5)
    _set(b, 'Specular IOR Level', 0.4)

    # Pores
    pores = nt.nodes.new('ShaderNodeTexNoise')
    pores.inputs['Scale'].default_value = 150.0
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.03
    nt.links.new(pores.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    print('[SHADER] Mat_Skin_Dark')
    return m


build()
