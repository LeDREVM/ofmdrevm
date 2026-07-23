"""Mat_FX_Fog — VOLUME brume doree du matin (savane S2). Domaine = grand cube plat."""
import bpy


def _lin(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


def build():
    m = bpy.data.materials.get('Mat_FX_Fog') or bpy.data.materials.new('Mat_FX_Fog')
    m.use_nodes = True
    m.use_fake_user = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    vol = nt.nodes.new('ShaderNodeVolumeScatter')
    vol.inputs['Color'].default_value = _lin('#E8DCC0')   # brume chaude
    vol.inputs['Density'].default_value = 0.015
    if 'Anisotropy' in vol.inputs:
        vol.inputs['Anisotropy'].default_value = 0.6       # forward scatter = rayons du couchant

    # Nappe : plus dense en bas (gradient Z objet)
    coords = nt.nodes.new('ShaderNodeTexCoord')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = (1, 1, 1, 1)
    ramp.color_ramp.elements[1].position = 0.6
    ramp.color_ramp.elements[1].color = (0, 0, 0, 1)
    mul = nt.nodes.new('ShaderNodeMath')
    mul.operation = 'MULTIPLY'
    mul.inputs[1].default_value = 0.015
    nt.links.new(coords.outputs['Object'], sep.inputs['Vector'])
    nt.links.new(sep.outputs['Z'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], mul.inputs[0])
    nt.links.new(mul.outputs[0], vol.inputs['Density'])

    nt.links.new(vol.outputs['Volume'], out.inputs['Volume'])
    print('[SHADER] Mat_FX_Fog (VOLUME nappe basse)')
    return m


build()
