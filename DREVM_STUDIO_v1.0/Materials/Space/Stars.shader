"""Mat_Space_Stars — fond etoile : emission points blancs sur noir.
Assigner a une sphere inversee (normales vers l'interieur) englobant la scene."""
import bpy


def _lin(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


def build():
    m = bpy.data.materials.get('Mat_Space_Stars') or bpy.data.materials.new('Mat_Space_Stars')
    m.use_nodes = True
    m.use_fake_user = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')

    # Etoiles : noise haute frequence, seuil dur
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 900.0
    noise.inputs['Detail'].default_value = 0.0
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.88
    ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    ramp.color_ramp.elements[1].position = 0.92
    ramp.color_ramp.elements[1].color = _lin('#E8E8F0')

    emit = nt.nodes.new('ShaderNodeEmission')
    emit.inputs['Strength'].default_value = 2.0
    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], emit.inputs['Color'])
    nt.links.new(emit.outputs['Emission'], out.inputs['Surface'])
    print('[SHADER] Mat_Space_Stars (sphere inversee)')
    return m


build()
