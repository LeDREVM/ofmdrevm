"""Mat_Water_River — riviere claire (E03/E07 Luna : le miroir).
Eau calme, reflet parfait — le bump ne s'anime QUE pour l'onde du contact."""
import bpy


def _lin(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


def build():
    m = bpy.data.materials.get('Mat_Water_River') or bpy.data.materials.new('Mat_Water_River')
    m.use_nodes = True
    m.use_fake_user = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')

    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Roughness'].default_value = 0.02   # miroir — reflet de la demi-lune
    b.inputs['IOR'].default_value = 1.33
    if 'Transmission Weight' in b.inputs:
        b.inputs['Transmission Weight'].default_value = 1.0

    absorb = nt.nodes.new('ShaderNodeVolumeAbsorption')
    absorb.inputs['Color'].default_value = _lin('#2A4A3A')
    absorb.inputs['Density'].default_value = 0.15
    nt.links.new(absorb.outputs['Volume'], out.inputs['Volume'])

    # Onde circulaire du contact (E03) : wave RINGS depuis le centre objet
    wave = nt.nodes.new('ShaderNodeTexWave')
    wave.wave_type = 'RINGS'
    wave.rings_direction = 'SPHERICAL'
    wave.inputs['Scale'].default_value = 4.0
    ctrl = nt.nodes.new('ShaderNodeValue')
    ctrl.name = ctrl.label = 'Ripple_Ctrl'   # 0 = eau parfaitement calme
    ctrl.outputs[0].default_value = 0.0
    mul = nt.nodes.new('ShaderNodeMath')
    mul.operation = 'MULTIPLY'
    bump = nt.nodes.new('ShaderNodeBump')
    nt.links.new(wave.outputs['Fac'], mul.inputs[0])
    nt.links.new(ctrl.outputs[0], mul.inputs[1])
    nt.links.new(mul.outputs[0], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])

    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    print('[SHADER] Mat_Water_River (ctrl : Ripple_Ctrl 0-0.3)')
    return m


build()
