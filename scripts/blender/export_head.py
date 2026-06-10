"""
export_head.py — headless.
Exporte la TÊTE de N'Aset (depuis Naset_Body) en FBX, prête pour Mesh-to-MetaHuman (UE5).
Travaille sur un DUPLICATA : le fichier original n'est PAS modifié (pas de save).

  blender -b N_Aset_OFM_Character.blend -P export_head.py
"""
import bpy, bmesh, os
from mathutils import Vector

HEAD_HEIGHT = 0.30   # hauteur tête+cou conservée depuis le sommet (m)
OUT = "C:/Users/ardja/Documents/CODING/Blendaah/ofmdrevm/.claude/worktrees/awesome-bose-7c4dc5/exports/Naset_Head_for_MetaHuman.fbx"

print("\n==== EXPORT TÊTE POUR METAHUMAN ====")
body = bpy.data.objects.get('Naset_Body')
if not body:
    print("ERREUR: Naset_Body introuvable"); raise SystemExit

# Duplicata (l'original reste intact)
head = body.copy()
head.data = body.data.copy()
head.name = "Naset_Head"
head.data.name = "Naset_Head_Mesh"
bpy.context.scene.collection.objects.link(head)

# Borne haute
cs = [head.matrix_world @ Vector(c) for c in head.bound_box]
maxz = max(v.z for v in cs)
cut_z = maxz - HEAD_HEIGHT
print(f"Sommet Z={maxz:.3f} · coupe sous Z={cut_z:.3f} (garde tête+cou)")

# Supprime les sommets sous la ligne de coupe
mw = head.matrix_world
me = head.data
bm = bmesh.new(); bm.from_mesh(me)
to_del = [v for v in bm.verts if (mw @ v.co).z < cut_z]
bmesh.ops.delete(bm, geom=to_del, context='VERTS')
bm.to_mesh(me); bm.free(); me.update()

cs = [head.matrix_world @ Vector(c) for c in head.bound_box]
dx = max(v.x for v in cs) - min(v.x for v in cs)
dy = max(v.y for v in cs) - min(v.y for v in cs)
dz = max(v.z for v in cs) - min(v.z for v in cs)
print(f"Tête isolée : {len(me.vertices)} verts · X={dx:.3f} Y={dy:.3f} Z={dz:.3f} m")

# Normalise l'échelle : 1 BU = 1 m (évite la double conversion d'unité au FBX)
bpy.context.scene.unit_settings.scale_length = 1.0

# Sélection = uniquement la tête, puis export FBX
os.makedirs(os.path.dirname(OUT), exist_ok=True)
bpy.ops.object.select_all(action='DESELECT')
head.select_set(True)
bpy.context.view_layer.objects.active = head

bpy.ops.export_scene.fbx(
    filepath=OUT,
    use_selection=True,
    object_types={'MESH'},
    global_scale=1.0,
    apply_scale_options='FBX_SCALE_NONE',
    mesh_smooth_type='FACE',
    use_mesh_modifiers=True,
)
print("FBX exporté :", OUT)
print("==== FIN (fichier .blend NON modifié) ====\n")
