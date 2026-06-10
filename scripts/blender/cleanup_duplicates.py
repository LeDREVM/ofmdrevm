"""
cleanup_duplicates.py — headless.
Garde uniquement Naset_Body (figure centrale isolée), supprime tout autre mesh
(le doublon 3-figures) + purge les données orphelines (matériaux/images en double).
Sécurité : n'enregistre que si Naset_Body subsiste et est seul mesh.
"""
import bpy
from mathutils import Vector

F = "C:/Users/ardja/Documents/CODING/Blendaah/ofmdrevm/N_Aset_OFM_Character.blend"

print("\n==== NETTOYAGE DOUBLONS ====")
bpy.ops.wm.open_mainfile(filepath=F)

body = bpy.data.objects.get('Naset_Body')
if not body:
    print("ERREUR: Naset_Body absent — abandon"); raise SystemExit

# 1. Supprimer tous les mesh sauf Naset_Body
removed = []
for o in [o for o in bpy.data.objects if o.type == 'MESH' and o.name != 'Naset_Body']:
    removed.append(o.name)
    bpy.data.objects.remove(o, do_unlink=True)
print("Objets mesh supprimés :", removed or "aucun")

# 2. Purge orphelins (plusieurs passes : mesh → matériaux → images)
for _ in range(3):
    for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.images,
                 bpy.data.node_groups, bpy.data.textures):
        for blk in list(coll):
            if blk.users == 0:
                coll.remove(blk)
print("Matériaux restants :", [m.name for m in bpy.data.materials])
print("Images restantes   :", [i.name for i in bpy.data.images if i.name != 'Render Result'])

# 3. Vérif finale
meshes = [o for o in bpy.data.objects if o.type == 'MESH']
cs = [body.matrix_world @ Vector(c) for c in body.bound_box]
dx = max(v.x for v in cs) - min(v.x for v in cs)
dz = max(v.z for v in cs) - min(v.z for v in cs)
print(f"Mesh restants : {[o.name for o in meshes]} · Naset_Body {dx:.3f}×(h){dz:.3f} m · {len(body.data.vertices)} verts")

if len(meshes) != 1 or dx > 1.2:
    print("ATTENTION: état inattendu — RIEN sauvegardé."); raise SystemExit

bpy.ops.wm.save_mainfile(filepath=F)
print("Sauvegardé :", F)
print("==== FIN ====\n")
