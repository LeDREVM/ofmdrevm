"""
isolate_middle.py — headless (v2, découpe géométrique).
Les 3 figures sont soudées → on supprime les SOMMETS des tiers gauche/droite en X,
on garde le tiers central. Puis recentre, renomme, recadre caméra.
N'enregistre PAS si le résultat reste large (sécurité). Backup .blend1 auto.
"""
import bpy, math, bmesh
from mathutils import Vector

F = "C:/Users/ardja/Documents/CODING/Blendaah/ofmdrevm/N_Aset_OFM_Character.blend"

print("\n==== ISOLATION FIGURE CENTRALE (v2) ====")
bpy.ops.wm.open_mainfile(filepath=F)

body = bpy.data.objects.get('Naset_Body') or bpy.data.objects.get('Mesh_0')
if not body:
    print("ERREUR: mesh introuvable — abandon"); raise SystemExit
print("Mesh cible :", body.name, "·", len(body.data.vertices), "verts")

mw = body.matrix_world
me = body.data
bm = bmesh.new(); bm.from_mesh(me)
bm.verts.ensure_lookup_table()

xs = [(mw @ v.co).x for v in bm.verts]
lo, hi = min(xs), max(xs)
third = (hi - lo) / 3.0
lcut, rcut = lo + third, hi - third
print(f"X total [{lo:.2f}, {hi:.2f}] · garde la bande [{lcut:.2f}, {rcut:.2f}]")

to_del = [v for v in bm.verts if not (lcut <= (mw @ v.co).x <= rcut)]
print(f"Sommets supprimés : {len(to_del)} / {len(bm.verts)}")
bmesh.ops.delete(bm, geom=to_del, context='VERTS')
bm.to_mesh(me); bm.free()
me.update()

# Recentrer XY + poser au sol
bpy.context.view_layer.update()
cs = [body.matrix_world @ Vector(c) for c in body.bound_box]
xs = [v.x for v in cs]; ys = [v.y for v in cs]; zs = [v.z for v in cs]
body.location.x -= (max(xs) + min(xs)) / 2
body.location.y -= (max(ys) + min(ys)) / 2
body.location.z -= min(zs)
bpy.context.view_layer.update()
cs = [body.matrix_world @ Vector(c) for c in body.bound_box]
dx = max(v.x for v in cs) - min(v.x for v in cs)
dz = max(v.z for v in cs) - min(v.z for v in cs)
print(f"Après découpe : largeur X={dx:.3f}  hauteur Z={dz:.3f} m")

# Sécurité : si toujours large (>1.2m), l'isolation a échoué → ne pas sauvegarder
if dx > 1.2:
    print("ATTENTION: toujours trop large — isolation ratée, RIEN sauvegardé."); raise SystemExit

body.name = 'Naset_Body'
if body.data: body.data.name = 'Naset_Body_Mesh'

# Recadrer la caméra
cam = bpy.data.objects.get('Camera_Principale')
if cam:
    for c in list(cam.constraints): cam.constraints.remove(c)
    cam.location = (0.0, -2.6, dz * 0.55)
    cam.rotation_euler = (math.radians(90), 0, 0)
    cam.data.lens = 50.0
    bpy.context.scene.camera = cam
    print("Caméra recadrée : 50mm, 2.6m, hauteur", round(dz * 0.55, 2))

bpy.context.scene.render.engine = 'CYCLES'
bpy.ops.wm.save_mainfile(filepath=F)
print("Sauvegardé :", F)
print("==== FIN ====\n")
