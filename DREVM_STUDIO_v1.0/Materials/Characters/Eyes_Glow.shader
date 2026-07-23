"""Mat_Eyes_Glow — iris sombre #1A0D00 + emission or pilotable (S5 eveil).
Keyframer le node Value 'EyesGlow_Ctrl' : 0.0 (normal) -> 1.2 (iris or fondu)."""
import bpy


def _lin(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


def build():
    m = bpy.data.materials.get('Mat_Eyes_Glow') or bpy.data.materials.new('Mat_Eyes_Glow')
    m.use_nodes = True
    m.use_fake_user = True
    nt = m.node_tree
    nt.nodes.clear()

    out = nt.nodes.new('ShaderNodeOutputMaterial')
    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Base Color'].default_value = _lin('#1A0D00')
    b.inputs['Roughness'].default_value = 0.05          # cornee humide
    if 'Coat Weight' in b.inputs:
        b.inputs['Coat Weight'].default_value = 1.0     # vernis lacrymal

    # Emission or pilotee par UN node Value
    ctrl = nt.nodes.new('ShaderNodeValue')
    ctrl.name = ctrl.label = 'EyesGlow_Ctrl'
    ctrl.outputs[0].default_value = 0.0
    if 'Emission Color' in b.inputs:
        b.inputs['Emission Color'].default_value = _lin('#C9963A')
        nt.links.new(ctrl.outputs[0], b.inputs['Emission Strength'])

    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    print('[SHADER] Mat_Eyes_Glow (ctrl : EyesGlow_Ctrl 0.0-1.2)')
    return m


build()
