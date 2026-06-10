"""Vérifie le FBX tête : import + rendu preview (headless)."""
import bpy, math
from mathutils import Vector

FBX = "C:/Users/ardja/Documents/CODING/Blendaah/ofmdrevm/.claude/worktrees/awesome-bose-7c4dc5/exports/Naset_Head_for_MetaHuman.fbx"
OUT = "C:/Users/ardja/Documents/CODING/Blendaah/ofmdrevm/.claude/worktrees/awesome-bose-7c4dc5/preview_head.png"

# Scène vide
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=FBX)
obj = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]

# Dimensions réelles (sommets, pas bbox)
mw = obj.matrix_world
zs = [(mw @ v.co).z for v in obj.data.vertices]
xs = [(mw @ v.co).x for v in obj.data.vertices]
ys = [(mw @ v.co).y for v in obj.data.vertices]
print(f"TÊTE réelle : {len(obj.data.vertices)} verts · "
      f"X={max(xs)-min(xs):.3f} Y={max(ys)-min(ys):.3f} Z={max(zs)-min(zs):.3f} m")
cx, cy, cz = (max(xs)+min(xs))/2, (max(ys)+min(ys))/2, (max(zs)+min(zs))/2

# Lumière
sun = bpy.data.lights.new("Sun", 'SUN'); sun.energy = 4
so = bpy.data.objects.new("Sun", sun); so.location = (2, -3, 3)
bpy.context.scene.collection.objects.link(so)

# Caméra face
cam_d = bpy.data.cameras.new("Cam"); cam_d.lens = 60
cam = bpy.data.objects.new("Cam", cam_d)
cam.location = (cx, cy - 0.9, cz)
cam.rotation_euler = (math.radians(90), 0, 0)
bpy.context.scene.collection.objects.link(cam)
bpy.context.scene.camera = cam

sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.samples = 24
sc.render.resolution_x = 600; sc.render.resolution_y = 600
sc.render.image_settings.file_format = 'PNG'
sc.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("Preview tête saved:", OUT)
