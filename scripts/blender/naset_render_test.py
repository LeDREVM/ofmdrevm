"""
naset_render_test.py
Test de rendu rapide : construit les matériaux N'Aset puis les applique
à 2 sphères témoins (peau + or) et rend une frame.
But : vérifier que les scripts tournent SANS erreur API + voir peau/or à l'écran.

Usage headless :
  blender --background --factory-startup --python naset_render_test.py
"""

import bpy
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# ── 1. Construire les matériaux (exécute le script avancé) ────────────────────
mat_script = os.path.join(HERE, 'naset_materials_rig_fx.py')
with open(mat_script, encoding='utf-8') as f:
    exec(compile(f.read(), mat_script, 'exec'))

# ── 2. Nettoyer la scène par défaut (cube) ────────────────────────────────────
for obj in list(bpy.data.objects):
    if obj.type == 'MESH' and obj.name.startswith('Cube'):
        bpy.data.objects.remove(obj, do_unlink=True)

# ── 3. Sphères témoins ────────────────────────────────────────────────────────
def add_preview_sphere(name, mat_name, location):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=location)
    sph = bpy.context.active_object
    sph.name = name
    bpy.ops.object.shade_smooth()
    mat = bpy.data.materials.get(mat_name)
    if mat:
        sph.data.materials.append(mat)
        print(f"[TEST] {name} ← {mat_name}")
    else:
        print(f"[TEST][!] matériau {mat_name} introuvable")
    return sph

add_preview_sphere('Preview_Skin', 'Mat_Peau_Naset', (-1.3, 0, 1.0))
add_preview_sphere('Preview_Gold', 'Mat_Or_Emission', (1.3, 0, 1.0))

# ── 4. Caméra ─────────────────────────────────────────────────────────────────
bpy.ops.object.camera_add(location=(0, -9, 1.0), rotation=(1.5708, 0, 0))  # 90° X, droit devant
cam = bpy.context.active_object
cam.name = 'TestCam'
cam.data.lens = 50
bpy.context.scene.camera = cam

# ── 5. Éclairage simple (en plus des lumières créées par le script) ───────────
bpy.ops.object.light_add(type='AREA', location=(3, -3, 4))
key = bpy.context.active_object
key.data.energy = 1200
key.data.size = 5

# Fond légèrement sombre pour faire ressortir l'émission de l'or
world = bpy.context.scene.world or bpy.data.worlds.new('World')
bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get('Background')
if bg:
    bg.inputs['Color'].default_value = (0.02, 0.02, 0.03, 1.0)
    bg.inputs['Strength'].default_value = 0.3

# ── 6. Réglages rendu rapide (CPU, fiable en headless) ────────────────────────
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'            # CPU = robuste sans config GPU en background
scene.cycles.samples = 48
scene.cycles.use_denoising = True
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.view_settings.view_transform = 'Filmic'
try:
    scene.view_settings.look = 'Medium High Contrast'   # nom court Blender 5.0
except Exception:
    pass

# Frame 2280 = éveil S5 (émission yeux/or au max) pour bien voir l'or briller
scene.frame_set(2200)

out_dir = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'renders')
os.makedirs(out_dir, exist_ok=True)
scene.render.filepath = os.path.join(out_dir, 'test_peau_or.png')
scene.render.image_settings.file_format = 'PNG'

print(f"\n[TEST] Rendu → {scene.render.filepath}")
bpy.ops.render.render(write_still=True)
print("[TEST] Rendu terminé ✓")
