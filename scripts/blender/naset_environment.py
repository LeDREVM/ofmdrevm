"""
naset_environment.py
Environnement savane sacree pour N'Aset OFM — genere en local :
  - World : ciel Nishita coucher de soleil (contre-jour dore S1)
  - Sun   : soleil bas et chaud aligne sur le contre-jour
  - Sol   : plan savane 200x200 m, sable dore procedural (noise)
  - Herbes: particules hair sur le sol (touffes seches)
  - Acacias silhouettes : 3 arbres low-poly a l'horizon

Idempotent. Lance via naset_pipeline.py ou Alt+P.
"""

import bpy
import math


def _delete_if_exists(*names):
    for name in names:
        obj = bpy.data.objects.get(name)
        if obj:
            bpy.data.objects.remove(obj, do_unlink=True)


def hex_to_linear(hex_str):
    h = hex_str.lstrip('#')
    rgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
                 for c in rgb) + (1.0,)


OR_SACRE = hex_to_linear('#C9963A')
SABLE = hex_to_linear('#B08A50')
HERBE_SECHE = hex_to_linear('#A67F3B')


# ─── WORLD — CIEL COUCHER DE SOLEIL ─────────────────────────────────────────

def setup_world():
    world = bpy.data.worlds.get('Savane_Sky') or bpy.data.worlds.new('Savane_Sky')
    bpy.context.scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()

    sky = nt.nodes.new('ShaderNodeTexSky')
    # Blender 5.0 : 'NISHITA' supprime — nouveau modele physique
    sky.sky_type = 'MULTIPLE_SCATTERING'
    for attr, val in [('sun_elevation', math.radians(4.0)),   # rasant — contre-jour S1
                      ('sun_rotation', math.radians(180.0)),  # face a la camera (-Y)
                      ('sun_intensity', 0.35),
                      ('dust_density', 4.0)]:                 # brume doree
        if hasattr(sky, attr):
            setattr(sky, attr, val)
    sky.location = (-400, 0)

    bg = nt.nodes.new('ShaderNodeBackground')
    bg.inputs['Strength'].default_value = 0.6
    out = nt.nodes.new('ShaderNodeOutputWorld')
    nt.links.new(sky.outputs['Color'], bg.inputs['Color'])
    nt.links.new(bg.outputs['Background'], out.inputs['Surface'])
    print("[ENV] World Nishita — soleil rasant 4°, brume doree")


# ─── SOLEIL ──────────────────────────────────────────────────────────────────

def create_sun():
    _delete_if_exists('Sun_Savane')
    sun_data = bpy.data.lights.new('Sun_Savane', 'SUN')
    sun_data.energy = 3.0
    sun_data.color = OR_SACRE[:3]
    sun_data.angle = math.radians(2.0)       # ombres douces
    sun = bpy.data.objects.new('Sun_Savane', sun_data)
    bpy.context.scene.collection.objects.link(sun)
    sun.location = (0, 40, 3)
    # Pointe vers l'origine, presque horizontal (contre-jour)
    sun.rotation_euler = (math.radians(86), 0, math.radians(180))
    print("[ENV] Sun_Savane — 3.0 W, or sacre, quasi horizontal")


# ─── SOL SAVANE ──────────────────────────────────────────────────────────────

def create_ground():
    _delete_if_exists('Sol_Savane')
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, 0))
    ground = bpy.context.active_object
    ground.name = 'Sol_Savane'

    mat = bpy.data.materials.get('Mat_Sol_Savane') or bpy.data.materials.new('Mat_Sol_Savane')
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Roughness'].default_value = 0.9
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 45.0
    noise.inputs['Detail'].default_value = 8.0
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = SABLE
    ramp.color_ramp.elements[1].color = HERBE_SECHE
    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    ground.data.materials.append(mat)

    # Herbes seches — systeme hair simple
    psys_mod = ground.modifiers.new('Herbes', 'PARTICLE_SYSTEM')
    ps = psys_mod.particle_system.settings
    ps.type = 'HAIR'
    ps.count = 4000
    ps.hair_length = 0.35
    ps.brownian_factor = 0.05
    ps.render_type = 'PATH'
    ps.root_radius = 0.02
    print("[ENV] Sol_Savane 200m + 4000 herbes seches")


# ─── ACACIAS SILHOUETTES ─────────────────────────────────────────────────────

def create_acacias():
    positions = [(-35, 60, 0), (25, 75, 0), (60, 55, 0)]
    mat = bpy.data.materials.get('Mat_Acacia') or bpy.data.materials.new('Mat_Acacia')
    mat.use_nodes = True
    bsdf = next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.02, 0.015, 0.01, 1.0)
        bsdf.inputs['Roughness'].default_value = 1.0

    for i, pos in enumerate(positions):
        name = f'Acacia_{i + 1:02d}'
        _delete_if_exists(name, name + '_Feuillage')
        # Tronc : cone etire
        bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.35, radius2=0.12,
                                        depth=5.0, location=(pos[0], pos[1], 2.5))
        trunk = bpy.context.active_object
        trunk.name = name
        trunk.data.materials.append(mat)
        # Feuillage : cone aplati (parasol d'acacia)
        bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=4.5, radius2=1.2,
                                        depth=1.4, location=(pos[0], pos[1], 5.6))
        canopy = bpy.context.active_object
        canopy.name = name + '_Feuillage'
        canopy.data.materials.append(mat)
        canopy.parent = trunk
        canopy.matrix_parent_inverse = trunk.matrix_world.inverted()
    print(f"[ENV] {len(positions)} acacias silhouettes a l'horizon")


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    print("\n━━━ N'Aset OFM · Environnement Savane ━━━")
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    setup_world()
    create_sun()
    create_ground()
    create_acacias()
    print("━━━ Savane sacree prete (ciel + sol + herbes + acacias) ━━━\n")


main()
