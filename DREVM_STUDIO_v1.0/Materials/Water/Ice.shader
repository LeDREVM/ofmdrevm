"""Mat_Water_Ice — glace : transmission + rough 0.15, fissures voronoi internes."""
import bpy


def _lin(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


def build():
    m = bpy.data.materials.get('Mat_Water_Ice') or bpy.data.materials.new('Mat_Water_Ice')
    m.use_nodes = True
    m.use_fake_user = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')

    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Base Color'].default_value = _lin('#DCEBF0')
    b.inputs['Roughness'].default_value = 0.15
    b.inputs['IOR'].default_value = 1.31
    if 'Transmission Weight' in b.inputs:
        b.inputs['Transmission Weight'].default_value = 0.9
    if 'Subsurface Weight' in b.inputs:
        b.inputs['Subsurface Weight'].default_value = 0.15   # coeur laiteux
        if 'Subsurface Radius' in b.inputs:
            b.inputs['Subsurface Radius'].default_value = (0.3, 0.35, 0.4)

    # Fissures : voronoi aretes -> bump inverse + roughness locale
    voro = nt.nodes.new('ShaderNodeTexVoronoi')
    voro.feature = 'DISTANCE_TO_EDGE'
    voro.inputs['Scale'].default_value = 4.0
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[1].position = 0.05
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.25
    bump.invert = True
    nt.links.new(voro.outputs['Distance'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])

    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    print('[SHADER] Mat_Water_Ice')
    return m


build()
