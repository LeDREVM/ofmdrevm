"""
create_material_library.py — DREVM Studio
Bibliotheque de 5 materiaux studio (use_fake_user pour survivre a la sauvegarde) :
    Mat_Gold_Sacred   — or sacre #C9963A, metal martele (+ variante emissive)
    Mat_Moon_Silver   — surface lunaire #E8E8F0, craters noise + emission douce
    Mat_Skin_DREVM    — peau #6B3D2E, SSS (inputs Blender 5 : Subsurface Weight/Scale)
    Mat_Fabric_Ivory  — etoffe ivoire #FAFAF0, sheen (+ variante Shuka rouge)
    Mat_Stone_Temple  — pierre du temple, noise 2 echelles

Valeurs detaillees : ../Materials/*.md
"""

import bpy


def hex_to_linear(hex_str):
    h = hex_str.lstrip('#')
    rgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
                 for c in rgb) + (1.0,)


COLOR = {
    'or':     hex_to_linear('#C9963A'),
    'argent': hex_to_linear('#E8E8F0'),
    'peau':   hex_to_linear('#6B3D2E'),
    'sss':    hex_to_linear('#8B4E35'),
    'ivoire': hex_to_linear('#FAFAF0'),
    'shuka':  hex_to_linear('#C0392B'),
    'pierre': hex_to_linear('#8A7B63'),
}


def fresh_material(name):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.use_fake_user = True   # survit meme sans objet assigne
    mat.node_tree.nodes.clear()
    nt = mat.node_tree
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat, nt, bsdf, out


def safe_set(bsdf, input_name, value):
    """Ignore proprement un input absent (differences de version)."""
    sock = bsdf.inputs.get(input_name)
    if sock:
        sock.default_value = value
    else:
        print(f"   [!] input '{input_name}' absent — ignore")


def create_gold():
    mat, nt, bsdf, out = fresh_material('Mat_Gold_Sacred')
    safe_set(bsdf, 'Base Color', COLOR['or'])
    safe_set(bsdf, 'Metallic', 0.95)
    safe_set(bsdf, 'Roughness', 0.10)
    # Martelage : noise -> bump leger
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 30.0
    noise.inputs['Detail'].default_value = 6.0
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.08
    nt.links.new(noise.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    print("[MAT] Mat_Gold_Sacred — metal 0.95, rough 0.10, martelage bump")

    # Variante emissive (S5 eveil)
    mat_e, nt_e, bsdf_e, out_e = fresh_material('Mat_Gold_Emission')
    safe_set(bsdf_e, 'Base Color', COLOR['or'])
    safe_set(bsdf_e, 'Metallic', 0.95)
    safe_set(bsdf_e, 'Roughness', 0.15)
    safe_set(bsdf_e, 'Emission Color', COLOR['or'])
    safe_set(bsdf_e, 'Emission Strength', 2.0)
    print("[MAT] Mat_Gold_Emission — emission 2.0 (keyframable)")


def create_moon():
    mat, nt, bsdf, out = fresh_material('Mat_Moon_Silver')
    safe_set(bsdf, 'Base Color', COLOR['argent'])
    safe_set(bsdf, 'Roughness', 0.85)
    safe_set(bsdf, 'Emission Color', COLOR['argent'])
    safe_set(bsdf, 'Emission Strength', 0.4)   # lueur douce, jamais excessive
    # Crateres : voronoi -> bump
    voro = nt.nodes.new('ShaderNodeTexVoronoi')
    voro.inputs['Scale'].default_value = 8.0
    if 'Randomness' in voro.inputs:
        voro.inputs['Randomness'].default_value = 1.0
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.25
    nt.links.new(voro.outputs['Distance'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    print("[MAT] Mat_Moon_Silver — crateres voronoi, emission 0.4")


def create_skin():
    mat, nt, bsdf, out = fresh_material('Mat_Skin_DREVM')
    safe_set(bsdf, 'Base Color', COLOR['peau'])
    # Blender 5 : Subsurface Weight + Scale (plus de 'Subsurface' float unique)
    safe_set(bsdf, 'Subsurface Weight', 0.3)
    safe_set(bsdf, 'Subsurface Scale', 0.05)
    safe_set(bsdf, 'Subsurface Radius', (0.36, 0.20, 0.12))
    safe_set(bsdf, 'Roughness', 0.5)
    # Pores : noise fin -> bump tres subtil
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 150.0
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.03
    nt.links.new(noise.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    print("[MAT] Mat_Skin_DREVM — SSS Weight 0.3 Scale 0.05, pores subtils")


def create_fabric():
    mat, nt, bsdf, out = fresh_material('Mat_Fabric_Ivory')
    safe_set(bsdf, 'Base Color', COLOR['ivoire'])
    safe_set(bsdf, 'Roughness', 0.6)
    safe_set(bsdf, 'Sheen Weight', 0.3)
    print("[MAT] Mat_Fabric_Ivory — sheen 0.3")

    mat_s, nt_s, bsdf_s, out_s = fresh_material('Mat_Fabric_Shuka')
    safe_set(bsdf_s, 'Base Color', COLOR['shuka'])
    safe_set(bsdf_s, 'Roughness', 0.55)
    safe_set(bsdf_s, 'Sheen Weight', 0.3)
    print("[MAT] Mat_Fabric_Shuka — rouge Maasai, sheen 0.3")


def create_stone():
    mat, nt, bsdf, out = fresh_material('Mat_Stone_Temple')
    safe_set(bsdf, 'Base Color', COLOR['pierre'])
    safe_set(bsdf, 'Roughness', 0.95)
    # Deux echelles de noise : blocs + grain
    n1 = nt.nodes.new('ShaderNodeTexNoise')
    n1.inputs['Scale'].default_value = 3.0
    n2 = nt.nodes.new('ShaderNodeTexNoise')
    n2.inputs['Scale'].default_value = 80.0
    mix = nt.nodes.new('ShaderNodeMix')
    mix.data_type = 'FLOAT'
    mix.inputs['Factor'].default_value = 0.4
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.35
    nt.links.new(n1.outputs['Fac'], mix.inputs[2])
    nt.links.new(n2.outputs['Fac'], mix.inputs[3])
    nt.links.new(mix.outputs[0], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    print("[MAT] Mat_Stone_Temple — noise 2 echelles, rough 0.95")


def main():
    print("\n━━━ DREVM Studio · Material Library ━━━")
    create_gold()
    create_moon()
    create_skin()
    create_fabric()
    create_stone()
    print("━━━ 7 materiaux en bibliotheque (fake user) ━━━\n")


main()
