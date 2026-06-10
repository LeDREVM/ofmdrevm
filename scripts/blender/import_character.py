"""
import_character.py  — headless.
Importe le mesh Meshy de N'Aset dans le fichier scène (rig lumières) et sauvegarde.

  blender -b -P import_character.py

- Ouvre N_Aset_OFM_Character.blend (caméras + lumières)
- Supprime le Cube placeholder
- Append Mesh_0 depuis le fichier Meshy (mesh + Material_0 + 4 textures)
- Pose le mesh au sol, centré en XY (sans changer son échelle — report des dimensions)
- Cycles + caméra active + sauvegarde (un backup .blend1 est créé automatiquement)
"""

import bpy
from mathutils import Vector

SCENE_FILE = "C:/Users/ardja/Documents/CODING/Blendaah/ofmdrevm/N_Aset_OFM_Character.blend"
MESHY_FILE = "C:/Users/ardja/Documents/CODING/Blendaah/ofmdrevm/Meshy_AI_N_Aset_OFM_Character_0609011204_image-to-3d-texture.blend"
MESH_NAME  = "Mesh_0"

print("\n==== IMPORT PERSONNAGE N'Aset ====")

# 1. Ouvrir la scène d'éclairage
bpy.ops.wm.open_mainfile(filepath=SCENE_FILE)
print("Scène ouverte :", SCENE_FILE)

# 2. Supprimer le cube placeholder
if "Cube" in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects["Cube"], do_unlink=True)
    print("Cube placeholder supprimé")

# 3. Append Mesh_0 depuis le fichier Meshy
with bpy.data.libraries.load(MESHY_FILE, link=False) as (src, dst):
    names = [n for n in src.objects if n == MESH_NAME] or list(src.objects)
    dst.objects = names
    print("Objets à importer :", names)

scene_coll = bpy.context.scene.collection
imported = None
for obj in dst.objects:
    if obj is not None:
        scene_coll.objects.link(obj)
        imported = obj
print("Mesh importé :", imported.name if imported else "AUCUN")

# 4. Poser au sol, centrer en XY (sans toucher l'échelle)
if imported:
    bpy.context.view_layer.update()
    corners = [imported.matrix_world @ Vector(c) for c in imported.bound_box]
    xs = [v.x for v in corners]; ys = [v.y for v in corners]; zs = [v.z for v in corners]
    dx, dy, dz = max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    imported.location.x -= cx
    imported.location.y -= cy
    imported.location.z -= min(zs)   # pose le point le plus bas à Z=0
    print(f"Dimensions du mesh (m) : X={dx:.3f}  Y={dy:.3f}  Z={dz:.3f}")
    print("Mesh centré en XY et posé au sol")

# 5. Rendu + caméra
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
cam = bpy.data.objects.get("Camera_Principale") or bpy.data.objects.get("Camera")
if cam:
    sc.camera = cam
    print("Caméra active :", cam.name)

# 6. Sauvegarde (backup .blend1 auto)
bpy.ops.wm.save_mainfile(filepath=SCENE_FILE)
print("Fichier sauvegardé :", SCENE_FILE)
print("==== FIN ====\n")
