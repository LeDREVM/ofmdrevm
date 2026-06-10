"""Inspecte le .blend courant (lecture seule) — liste objets, meshes, matériaux."""
import bpy

print("\n==== INSPECTION N'Aset ====")
print("Objets :", len(bpy.data.objects))
for o in bpy.data.objects:
    extra = ""
    if o.type == 'MESH':
        extra = f"· {len(o.data.vertices)} verts · {len(o.data.materials)} mat"
    print(f"  [{o.type}] {o.name} {extra}")

print("\nMatériaux :", len(bpy.data.materials))
for m in bpy.data.materials:
    print(f"  - {m.name} (nodes={m.use_nodes})")

print("\nArmatures :", [o.name for o in bpy.data.objects if o.type == 'ARMATURE'])
print("Systèmes de particules/groom :",
      [(o.name, len(o.particle_systems)) for o in bpy.data.objects
       if hasattr(o, 'particle_systems') and len(o.particle_systems)])
print("Images/textures :", len(bpy.data.images), [i.name for i in bpy.data.images][:10])
print("Moteur de rendu :", bpy.context.scene.render.engine)
print("==== FIN ====\n")
