"""Habillage S1 + rendu — s'execute apres naset_pipeline sur le blend maitre."""
import bpy
import math
import os

scene = bpy.context.scene

# N'Aset de dos : face au soleil (+Y), camera S1 derriere elle (-Y)
rig = bpy.data.objects.get('Naset_Rig')
if rig:
    rig.rotation_euler.z = math.radians(180)

# Drapes non parentes : pivoter AVEC elle autour de l'origine (rotation additive)
for name in ('Drape_Shuka', 'Drape_Ivoire'):
    obj = bpy.data.objects.get(name)
    if obj and obj.parent is None:
        obj.rotation_euler.z += math.radians(180)
        obj.location.x *= -1
        obj.location.y *= -1

# CONTRE-JOUR S1 : le soleil est DEVANT elle (+Y), il rayonne vers la camera (-Y)
sun = bpy.data.objects.get('Sun_Savane')
if sun:
    sun.rotation_euler = (math.radians(-86), 0, 0)   # lumiere voyage de +Y vers -Y
    sun.data.energy = 6.0

# Ciel : placer le disque solaire dans l'axe camera (+Y) et charger l'ambiance couchant
world = bpy.context.scene.world
if world and world.use_nodes:
    sky = next((n for n in world.node_tree.nodes if n.type == 'TEX_SKY'), None)
    if sky:
        if hasattr(sky, 'sun_rotation'):
            sky.sun_rotation = 0.0            # azimut +Y (etait 180 = -Y)
        if hasattr(sky, 'sun_elevation'):
            sky.sun_elevation = math.radians(3.0)
        if hasattr(sky, 'sun_intensity'):
            sky.sun_intensity = 0.5
        if hasattr(sky, 'dust_density'):
            sky.dust_density = 7.0            # brume doree epaisse

# Camera S1 active
cam = bpy.data.objects.get('Camera_S1')
if cam:
    scene.camera = cam

# S1 : aucune emission doree (spec : bijoux eteints)
mat = bpy.data.materials.get('Mat_Or_Emission')
if mat and mat.use_nodes:
    for n in mat.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED' and 'Emission Strength' in n.inputs:
            n.inputs['Emission Strength'].default_value = 0.0
        if n.type == 'EMISSION':
            n.inputs['Strength'].default_value = 0.0

# Crepuscule : baisser le fill ambiant pour la silhouette quasi-noire du spec
if world and world.use_nodes:
    bg = next((n for n in world.node_tree.nodes if n.type == 'BACKGROUND'), None)
    if bg:
        bg.inputs['Strength'].default_value = 0.45
if sun:
    sun.data.energy = 3.0

# CLOTH sur les deux drapes (pin = rangee haute deja en vertex group)
body = bpy.data.objects.get('Naset_Body')
if body and not any(m.type == 'COLLISION' for m in body.modifiers):
    body.modifiers.new('Collision', 'COLLISION')
for name in ('Drape_Shuka', 'Drape_Ivoire'):
    obj = bpy.data.objects.get(name)
    if not obj:
        continue
    cloth = next((m for m in obj.modifiers if m.type == 'CLOTH'), None)
    if not cloth:
        cloth = obj.modifiers.new('Cloth', 'CLOTH')
    cs = cloth.settings
    cs.quality = 8
    cs.tension_stiffness = 15
    cs.compression_stiffness = 15
    cs.bending_stiffness = 0.5
    cs.vertex_group_mass = 'Pin'
    cloth.point_cache.frame_start = 1
    cloth.point_cache.frame_end = 60

# Bake cloth 1-60 puis rendre frame 45 (drapes retombes, vent installe)
scene.frame_start, scene.frame_end = 1, 60
bpy.ops.ptcache.bake_all(bake=True)
scene.frame_set(45)

# Rendu preview solide : 720p, 64 samples, denoise, Cycles GPU deja configure
scene.render.resolution_x, scene.render.resolution_y = 1280, 720
scene.render.resolution_percentage = 100
scene.cycles.samples = 64
scene.cycles.use_denoising = True
out = os.path.join(os.path.dirname(bpy.data.filepath), 'renders', 'pipeline_test', 'Naset_S1_F0120_720p')
scene.render.filepath = out
bpy.ops.render.render(write_still=True)
print('[S1] RENDER_OK ->', out + '.png')

blend_out = os.path.join(os.path.dirname(bpy.data.filepath), 'Naset_S1_v1.blend')
bpy.ops.wm.save_as_mainfile(filepath=blend_out)
print('[S1] BLEND_OK ->', blend_out)
