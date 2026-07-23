"""Mat_Space_Nebula — VOLUME nebuleuse or/indigo DREVM.
Assigner a un CUBE domaine englobant. Densite pilotee par noise 4D."""
import bpy


def _lin(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


def build():
    m = bpy.data.materials.get('Mat_Space_Nebula') or bpy.data.materials.new('Mat_Space_Nebula')
    m.use_nodes = True
    m.use_fake_user = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')

    vol = nt.nodes.new('ShaderNodeVolumePrincipled')
    vol.inputs['Density'].default_value = 0.02

    # Structure : noise -> ramp densite (poches vides)
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 1.4
    noise.inputs['Detail'].default_value = 12.0
    ramp_d = nt.nodes.new('ShaderNodeValToRGB')
    ramp_d.color_ramp.elements[0].position = 0.42
    ramp_d.color_ramp.elements[1].position = 0.75
    math_mul = nt.nodes.new('ShaderNodeMath')
    math_mul.operation = 'MULTIPLY'
    math_mul.inputs[1].default_value = 0.08
    nt.links.new(noise.outputs['Fac'], ramp_d.inputs['Fac'])
    nt.links.new(ramp_d.outputs['Color'], math_mul.inputs[0])
    nt.links.new(math_mul.outputs[0], vol.inputs['Density'])

    # Couleur : indigo -> or dans les zones denses
    ramp_col = nt.nodes.new('ShaderNodeValToRGB')
    ramp_col.color_ramp.elements[0].color = _lin('#1C1A3A')
    ramp_col.color_ramp.elements[1].color = _lin('#C9963A')
    nt.links.new(noise.outputs['Fac'], ramp_col.inputs['Fac'])
    nt.links.new(ramp_col.outputs['Color'], vol.inputs['Color'])

    # Emission douce des coeurs denses
    if 'Emission Strength' in vol.inputs:
        nt.links.new(ramp_d.outputs['Color'], vol.inputs['Emission Strength'])
        vol.inputs['Emission Color'].default_value = _lin('#E8BC6A')

    nt.links.new(vol.outputs['Volume'], out.inputs['Volume'])
    print('[SHADER] Mat_Space_Nebula (VOLUME — cube domaine)')
    return m


build()
