"""Mat_FX_Energy — energie sacree or : emission fresnel + noise anime.
Ctrl : node Value 'Energy_Ctrl' (0 = eteint, 2 = eveil S5)."""
import bpy


def _lin(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


def build():
    m = bpy.data.materials.get('Mat_FX_Energy') or bpy.data.materials.new('Mat_FX_Energy')
    m.use_nodes = True
    m.use_fake_user = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')

    # Rim fresnel : l'energie vit sur les bords
    fresnel = nt.nodes.new('ShaderNodeFresnel')
    fresnel.inputs['IOR'].default_value = 1.2

    # Flux : noise 4D (W anime a la main ou par driver #frame/40)
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.noise_dimensions = '4D'
    noise.inputs['Scale'].default_value = 6.0

    combine = nt.nodes.new('ShaderNodeMath')
    combine.operation = 'MULTIPLY'
    nt.links.new(fresnel.outputs['Fac'], combine.inputs[0])
    nt.links.new(noise.outputs['Fac'], combine.inputs[1])

    ctrl = nt.nodes.new('ShaderNodeValue')
    ctrl.name = ctrl.label = 'Energy_Ctrl'
    ctrl.outputs[0].default_value = 1.0
    power = nt.nodes.new('ShaderNodeMath')
    power.operation = 'MULTIPLY'
    nt.links.new(combine.outputs[0], power.inputs[0])
    nt.links.new(ctrl.outputs[0], power.inputs[1])

    emit = nt.nodes.new('ShaderNodeEmission')
    emit.inputs['Color'].default_value = _lin('#E8BC6A')
    transp = nt.nodes.new('ShaderNodeBsdfTransparent')
    mix = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(power.outputs[0], emit.inputs['Strength'])
    nt.links.new(power.outputs[0], mix.inputs['Fac'])
    nt.links.new(transp.outputs['BSDF'], mix.inputs[1])
    nt.links.new(emit.outputs['Emission'], mix.inputs[2])
    nt.links.new(mix.outputs['Shader'], out.inputs['Surface'])
    print('[SHADER] Mat_FX_Energy (ctrl : Energy_Ctrl · animer noise W)')
    return m


build()
