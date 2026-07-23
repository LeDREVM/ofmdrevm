"""
create_geometry_nodes.py — DREVM Studio
Deux systemes generes par script (objets prets dans 30_FX / 20_ENVIRONMENT) :

    Luna_Moon        — lune : sphere + Mat_Moon_Silver + empty de phase.
                       La rotation Z de 'Moon_Phase_Ctrl' pilote l'eclairage
                       (sun lamp enfant) → cycle lunaire animable (8 episodes).
    DREVM_Dust_Field — champ de poussiere doree : GN distribute points
                       dans un cube volume, instances icospheres emissives.

Les recettes completes a monter a la main : ../GeometryNodes/*.md
"""

import bpy
import math


def _coll(name):
    coll = bpy.data.collections.get(name)
    if not coll:
        coll = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(coll)
    return coll


def _delete_if_exists(*names):
    for name in names:
        obj = bpy.data.objects.get(name)
        if obj:
            bpy.data.objects.remove(obj, do_unlink=True)


# ─── LUNE + CONTROLEUR DE PHASE ──────────────────────────────────────────────

def create_moon(radius=1.0, location=(0, 30, 12)):
    env = _coll('20_ENVIRONMENT')
    _delete_if_exists('Luna_Moon', 'Moon_Phase_Ctrl', 'Moon_Sun')

    # Controleur de phase : sa rotation Z = angle d'eclairage de la lune
    ctrl = bpy.data.objects.new('Moon_Phase_Ctrl', None)
    ctrl.empty_display_type = 'CIRCLE'
    ctrl.location = location
    env.objects.link(ctrl)

    # La lune
    mesh = bpy.data.meshes.new('Luna_Moon')
    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=48, v_segments=24, radius=radius)
    bm.to_mesh(mesh)
    bm.free()
    moon = bpy.data.objects.new('Luna_Moon', mesh)
    moon.parent = ctrl
    env.objects.link(moon)
    for p in mesh.polygons:
        p.use_smooth = True
    mat = bpy.data.materials.get('Mat_Moon_Silver')
    if mat:
        moon.data.materials.append(mat)

    # Lumiere de phase : sun enfant du controleur, decalee — tourner le
    # controleur change le cote eclaire => phases nouvelles lune → pleine lune
    sun_data = bpy.data.lights.new('Moon_Sun', 'SUN')
    sun_data.energy = 2.0
    sun_data.color = (0.91, 0.91, 0.94)
    sun = bpy.data.objects.new('Moon_Sun', sun_data)
    sun.parent = ctrl
    sun.location = (0, -5, 0)
    sun.rotation_euler = (math.radians(90), 0, 0)
    env.objects.link(sun)

    print("[GN] Luna_Moon + Moon_Phase_Ctrl — rotation Z du ctrl = phase lunaire")
    return ctrl, moon


def keyframe_phase(episode, frame_start=1, frame_end=480):
    """Phase lunaire d'un episode Luna (1=NewMoon ... 5=FullMoon ... 8=NewBeginning)."""
    ctrl = bpy.data.objects.get('Moon_Phase_Ctrl')
    if not ctrl:
        return
    # 8 episodes = cycle complet 360°, nouvelle lune = lumiere derriere (180°)
    angle = math.radians(180 + (episode - 1) * 45)
    for frame in (frame_start, frame_end):
        bpy.context.scene.frame_set(frame)
        ctrl.rotation_euler.z = angle
        ctrl.keyframe_insert('rotation_euler', index=2, frame=frame)
    print(f"[GN] Phase episode {episode} : {math.degrees(angle):.0f}°")


# ─── CHAMP DE POUSSIERE DOREE (GEOMETRY NODES) ───────────────────────────────

def create_dust_field(size=12.0, count=800):
    fx = _coll('30_FX')
    _delete_if_exists('DREVM_Dust_Field', 'DREVM_Dust_Particle')

    # Instance source : icosphere minuscule emissive
    import bmesh
    mesh = bpy.data.meshes.new('DREVM_Dust_Particle')
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.008)
    bm.to_mesh(mesh)
    bm.free()
    particle = bpy.data.objects.new('DREVM_Dust_Particle', mesh)
    fx.objects.link(particle)
    particle.hide_render = True
    particle.hide_set(True)
    mat = bpy.data.materials.get('Mat_Gold_Emission')
    if mat:
        particle.data.materials.append(mat)

    # Hote du champ : cube -> GN distribute + instance
    host_mesh = bpy.data.meshes.new('DREVM_Dust_Field')
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=size)
    bm.to_mesh(host_mesh)
    bm.free()
    host = bpy.data.objects.new('DREVM_Dust_Field', host_mesh)
    host.display_type = 'WIRE'
    fx.objects.link(host)

    mod = host.modifiers.new('DustGN', 'NODES')
    ng = bpy.data.node_groups.new('GN_Dust_Field', 'GeometryNodeTree')
    mod.node_group = ng

    # Interface in/out
    ng.interface.new_socket('Geometry', in_out='INPUT', socket_type='NodeSocketGeometry')
    ng.interface.new_socket('Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    n_in = ng.nodes.new('NodeGroupInput')
    n_out = ng.nodes.new('NodeGroupOutput')

    dist = ng.nodes.new('GeometryNodeDistributePointsOnFaces')
    dist.inputs['Density'].default_value = count / (size * size * 6)
    inst = ng.nodes.new('GeometryNodeInstanceOnPoints')
    obj_info = ng.nodes.new('GeometryNodeObjectInfo')
    obj_info.inputs['Object'].default_value = particle
    real = ng.nodes.new('GeometryNodeRealizeInstances')

    ng.links.new(n_in.outputs['Geometry'], dist.inputs['Mesh'])
    ng.links.new(dist.outputs['Points'], inst.inputs['Points'])
    ng.links.new(obj_info.outputs['Geometry'], inst.inputs['Instance'])
    ng.links.new(inst.outputs['Instances'], real.inputs['Geometry'])
    ng.links.new(real.outputs['Geometry'], n_out.inputs['Geometry'])

    print(f"[GN] DREVM_Dust_Field — ~{count} particules or dans {size}m³")
    return host


def main():
    print("\n━━━ DREVM Studio · Geometry Nodes ━━━")
    create_moon()
    create_dust_field()
    print("━━━ Moon System + Dust Field prets ━━━\n")


main()
