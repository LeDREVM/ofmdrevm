"""Mat_Hair_DREVM — cheveux #0D0A08, Principled Hair BSDF (box braids / afro)."""
import bpy


def build():
    m = bpy.data.materials.get('Mat_Hair_DREVM') or bpy.data.materials.new('Mat_Hair_DREVM')
    m.use_nodes = True
    m.use_fake_user = True
    nt = m.node_tree
    nt.nodes.clear()

    out = nt.nodes.new('ShaderNodeOutputMaterial')
    hair = nt.nodes.new('ShaderNodeBsdfHairPrincipled')
    # Melanin eleve = noir profond #0D0A08 physiquement correct
    if 'Melanin' in hair.inputs:
        hair.inputs['Melanin'].default_value = 0.95
    if 'Melanin Redness' in hair.inputs:
        hair.inputs['Melanin Redness'].default_value = 0.4   # sous-ton chaud
    if 'Roughness' in hair.inputs:
        hair.inputs['Roughness'].default_value = 0.30
    if 'Radial Roughness' in hair.inputs:
        hair.inputs['Radial Roughness'].default_value = 0.25
    if 'Coat' in hair.inputs:
        hair.inputs['Coat'].default_value = 0.10             # brillance tresse huilee

    nt.links.new(hair.outputs['BSDF'], out.inputs['Surface'])
    print('[SHADER] Mat_Hair_DREVM (Principled Hair, melanin 0.95)')
    return m


build()
