"""Mat_Space_Atmosphere — halo atmospherique : rim fresnel bleu + transparent.
Assigner a une sphere x1.03 autour de la planete (Terre) ou x1.15 (lune, halo argent)."""
import bpy


def _lin(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


def build():
    m = bpy.data.materials.get('Mat_Space_Atmosphere') or bpy.data.materials.new('Mat_Space_Atmosphere')
    m.use_nodes = True
    m.use_fake_user = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')

    # Rim : fresnel -> le bord de la sphere s'illumine, le centre est transparent
    fresnel = nt.nodes.new('ShaderNodeFresnel')
    fresnel.inputs['IOR'].default_value = 1.05
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.55
    ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    ramp.color_ramp.elements[1].position = 1.0
    ramp.color_ramp.elements[1].color = _lin('#6FA8DC')   # bleu atmosphere

    emit = nt.nodes.new('ShaderNodeEmission')
    emit.inputs['Strength'].default_value = 1.2
    transp = nt.nodes.new('ShaderNodeBsdfTransparent')
    mix = nt.nodes.new('ShaderNodeMixShader')

    nt.links.new(fresnel.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], emit.inputs['Color'])
    nt.links.new(ramp.outputs['Color'], mix.inputs['Fac'])
    nt.links.new(transp.outputs['BSDF'], mix.inputs[1])
    nt.links.new(emit.outputs['Emission'], mix.inputs[2])
    nt.links.new(mix.outputs['Shader'], out.inputs['Surface'])
    print('[SHADER] Mat_Space_Atmosphere (sphere x1.03)')
    return m


build()
