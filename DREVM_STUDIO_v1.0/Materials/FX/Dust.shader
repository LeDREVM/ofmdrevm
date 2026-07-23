"""Mat_FX_Dust — particule de poussiere doree emissive (instances GN/particules).
Ctrl : node Value 'Dust_Ctrl' (S1-S2 : 0.8 · S5 eveil : 2.0)."""
import bpy


def _lin(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


def build():
    m = bpy.data.materials.get('Mat_FX_Dust') or bpy.data.materials.new('Mat_FX_Dust')
    m.use_nodes = True
    m.use_fake_user = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')

    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Base Color'].default_value = _lin('#C9963A')
    b.inputs['Metallic'].default_value = 0.6
    b.inputs['Roughness'].default_value = 0.4

    ctrl = nt.nodes.new('ShaderNodeValue')
    ctrl.name = ctrl.label = 'Dust_Ctrl'
    ctrl.outputs[0].default_value = 0.8
    if 'Emission Color' in b.inputs:
        b.inputs['Emission Color'].default_value = _lin('#E8BC6A')
        nt.links.new(ctrl.outputs[0], b.inputs['Emission Strength'])

    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    print('[SHADER] Mat_FX_Dust (ctrl : Dust_Ctrl)')
    return m


build()
