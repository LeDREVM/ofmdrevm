"""Mat_Basalt — basalte sombre #2A2A2E, colonnes hexagonales (voronoi)."""
import bpy


def build():
    m = bpy.data.materials.get('Mat_Basalt') or bpy.data.materials.new('Mat_Basalt')
    m.use_nodes = True
    m.use_fake_user = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Base Color'].default_value = (0.026, 0.026, 0.030, 1.0)  # #2A2A2E lin
    b.inputs['Roughness'].default_value = 0.95

    # Colonnes : voronoi cellules -> aretes en creux
    voro = nt.nodes.new('ShaderNodeTexVoronoi')
    voro.feature = 'DISTANCE_TO_EDGE'
    voro.inputs['Scale'].default_value = 6.0
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[1].position = 0.08   # aretes fines
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.5
    bump.invert = True
    nt.links.new(voro.outputs['Distance'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bump.inputs['Height'])

    # Grain volcanique
    grain = nt.nodes.new('ShaderNodeTexNoise')
    grain.inputs['Scale'].default_value = 200.0
    bump2 = nt.nodes.new('ShaderNodeBump')
    bump2.inputs['Strength'].default_value = 0.08
    nt.links.new(grain.outputs['Fac'], bump2.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bump2.inputs['Normal'])
    nt.links.new(bump2.outputs['Normal'], b.inputs['Normal'])

    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    print('[SHADER] Mat_Basalt')
    return m


build()
