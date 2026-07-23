"""
naset_character.py
Genere le personnage N'Aset OFM en local, entierement par script :
  - Naset_Body        : corps procedural (stick figure + Skin + Subsurf), 1.77 m
  - Naset_Rig         : armature complete (spine, chest, head, eyelid.L/R, bras, jambes)
  - Naset_Eye_L / _R  : yeux (spheres, Mat_Yeux_Iris)
  - Naset_Hair_Curves : box braids en courbes (Mat_Cheveux_Naset)
  - Drape_Shuka       : drape rouge Maasai (vertex group 'Pin' pour le cloth)
  - Drape_Ivoire      : drape ivoire

Noms STRICTEMENT alignes sur naset_materials_rig_fx.py et
naset_animation_blender.py (chest / eyelid.L / eyelid.R / Naset_Rig / Naset_Body).

Lance depuis Blender (Alt+P) ou via naset_pipeline.py en headless.
Idempotent : supprime et recree ses propres objets a chaque run.
"""

import bpy
import bmesh
import math


HEIGHT = 1.77  # m — cf. faits canoniques N'Aset (1.75-1.80)

# Proportions verticales (fraction de HEIGHT)
Z = {
    'foot':     0.00,
    'knee':     0.29,
    'pelvis':   0.53,
    'spine_00': 0.60,
    'spine_01': 0.68,
    'spine_02': 0.76,
    'chest':    0.83,
    'neck':     0.88,
    'head':     0.93,
    'top':      1.00,
    'shoulder': 0.85,
    'elbow':    0.68,
    'hand':     0.50,
}

# Rayons Skin (silhouette elancee athletique)
RADII = {
    'foot': 0.045, 'knee': 0.055, 'pelvis': 0.105, 'spine': 0.095,
    'chest': 0.115, 'neck': 0.045, 'head': 0.105,
    'shoulder': 0.06, 'elbow': 0.04, 'hand': 0.035,
}

HIP_X = 0.085       # demi-ecart hanches
SHOULDER_X = 0.17   # demi-ecart epaules


def _delete_if_exists(*names):
    for name in names:
        obj = bpy.data.objects.get(name)
        if obj:
            bpy.data.objects.remove(obj, do_unlink=True)


def _link(obj):
    bpy.context.scene.collection.objects.link(obj)


def _get_mat(name, fallback_hex):
    """Reutilise le materiau du pipeline s'il existe, sinon placeholder simple."""
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if bsdf is None:
        bsdf = mat.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        out = next((n for n in mat.node_tree.nodes if n.type == 'OUTPUT_MATERIAL'), None)
        if out:
            mat.node_tree.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    h = fallback_hex.lstrip('#')
    rgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    bsdf.inputs['Base Color'].default_value = (*lin, 1.0)
    return mat


# ─── CORPS ───────────────────────────────────────────────────────────────────

def create_body():
    _delete_if_exists('Naset_Body')

    mesh = bpy.data.meshes.new('Naset_Body')
    obj = bpy.data.objects.new('Naset_Body', mesh)
    _link(obj)

    bm = bmesh.new()
    h = HEIGHT

    def v(x, key_z):
        return bm.verts.new((x, 0, Z[key_z] * h))

    # Colonne centrale
    pelvis = v(0, 'pelvis')
    s00 = v(0, 'spine_00')
    s01 = v(0, 'spine_01')
    s02 = v(0, 'spine_02')
    chest = v(0, 'chest')
    neck = v(0, 'neck')
    head = v(0, 'head')
    top = v(0, 'top')
    for a, b in [(pelvis, s00), (s00, s01), (s01, s02), (s02, chest),
                 (chest, neck), (neck, head), (head, top)]:
        bm.edges.new((a, b))

    # Jambes
    for side in (1, -1):
        hip = bm.verts.new((HIP_X * side, 0, Z['pelvis'] * h))
        knee = bm.verts.new((HIP_X * side, 0.01, Z['knee'] * h))
        foot = bm.verts.new((HIP_X * side, -0.03, Z['foot'] * h))
        bm.edges.new((pelvis, hip))
        bm.edges.new((hip, knee))
        bm.edges.new((knee, foot))

    # Bras (legerement ecartes — A-pose)
    for side in (1, -1):
        sho = bm.verts.new((SHOULDER_X * side, 0, Z['shoulder'] * h))
        elb = bm.verts.new(((SHOULDER_X + 0.09) * side, 0, Z['elbow'] * h))
        hnd = bm.verts.new(((SHOULDER_X + 0.13) * side, 0, Z['hand'] * h))
        bm.edges.new((chest, sho))
        bm.edges.new((sho, elb))
        bm.edges.new((elb, hnd))

    bm.to_mesh(mesh)
    bm.free()

    # Skin modifier + rayons par vertex
    skin = obj.modifiers.new('Skin', 'SKIN')
    skin.use_smooth_shade = True
    subsurf = obj.modifiers.new('Subsurf', 'SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 3

    def radius_for(co):
        z = co.z / h
        x = abs(co.x)
        if z >= Z['top'] - 0.02 or (Z['head'] - 0.03 <= z <= Z['top']):
            return RADII['head']
        if z >= Z['neck'] - 0.02 and x < 0.05:
            return RADII['neck']
        if x >= SHOULDER_X + 0.10:
            return RADII['hand']
        if x >= SHOULDER_X + 0.05:
            return RADII['elbow']
        if x >= SHOULDER_X - 0.02 and z > Z['shoulder'] - 0.05:
            return RADII['shoulder']
        if z >= Z['chest'] - 0.03 and x < 0.05:
            return RADII['chest']
        if z >= Z['spine_00'] - 0.02 and x < 0.05:
            return RADII['spine']
        if z >= Z['pelvis'] - 0.03:
            return RADII['pelvis']
        if z >= Z['knee'] - 0.03:
            return RADII['knee']
        return RADII['foot']

    for i, mv in enumerate(mesh.vertices):
        r = radius_for(mv.co)
        mesh.skin_vertices[0].data[i].radius = (r, r)

    obj.data.materials.append(_get_mat('Mat_Peau_Naset', '#6B3D2E'))
    print(f"[CHAR] Naset_Body cree — {HEIGHT} m, skin+subsurf")
    return obj


# ─── YEUX ────────────────────────────────────────────────────────────────────

def create_eyes():
    _delete_if_exists('Naset_Eye_L', 'Naset_Eye_R')
    mat = _get_mat('Mat_Yeux_Iris', '#1A0D00')
    eyes = []
    head_z = Z['head'] * HEIGHT + 0.05
    for side, name in ((1, 'Naset_Eye_L'), (-1, 'Naset_Eye_R')):
        mesh = bpy.data.meshes.new(name)
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=8, radius=0.018)
        bm.to_mesh(mesh)
        bm.free()
        obj = bpy.data.objects.new(name, mesh)
        obj.location = (0.032 * side, -0.088, head_z)
        _link(obj)
        obj.data.materials.append(mat)
        for p in mesh.polygons:
            p.use_smooth = True
        eyes.append(obj)
    print("[CHAR] Yeux crees (Mat_Yeux_Iris)")
    return eyes


# ─── CHEVEUX — BOX BRAIDS ────────────────────────────────────────────────────

def create_hair():
    _delete_if_exists('Naset_Hair_Curves')
    curve = bpy.data.curves.new('Naset_Hair_Curves', 'CURVE')
    curve.dimensions = '3D'
    curve.bevel_depth = 0.006      # epaisseur tresse
    curve.bevel_resolution = 2

    head_z = Z['head'] * HEIGHT + 0.07
    n_braids = 14
    for i in range(n_braids):
        ang = (i / n_braids) * 2 * math.pi
        # Racine sur le crane (deterministe, pas de random)
        rx = 0.075 * math.cos(ang)
        ry = 0.075 * math.sin(ang) - 0.01
        length = 0.42 + 0.06 * math.sin(i * 2.1)
        sp = curve.splines.new('BEZIER')
        sp.bezier_points.add(2)
        pts = sp.bezier_points
        pts[0].co = (rx, ry, head_z)
        pts[1].co = (rx * 1.5, ry * 1.4, head_z - length * 0.5)
        pts[2].co = (rx * 1.3, ry * 1.2 + 0.02, head_z - length)
        for p in pts:
            p.handle_left_type = p.handle_right_type = 'AUTO'

    obj = bpy.data.objects.new('Naset_Hair_Curves', curve)
    _link(obj)
    obj.data.materials.append(_get_mat('Mat_Cheveux_Naset', '#0D0A08'))
    print(f"[CHAR] Naset_Hair_Curves — {n_braids} box braids")
    return obj


# ─── DRAPES ──────────────────────────────────────────────────────────────────

def _create_drape(name, mat_name, mat_hex, size_x, size_y, location, rotation):
    _delete_if_exists(name)
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=14, y_segments=24, size=1.0)
    for vtx in bm.verts:
        vtx.co.x *= size_x / 2
        vtx.co.y *= size_y / 2
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(name, mesh)
    obj.location = location
    obj.rotation_euler = rotation
    _link(obj)
    obj.data.materials.append(_get_mat(mat_name, mat_hex))

    # Vertex group 'Pin' : rangee superieure (accroche cloth)
    vg = obj.vertex_groups.new(name='Pin')
    top_y = max(v.co.y for v in mesh.vertices) - 0.001
    pin_ids = [v.index for v in mesh.vertices if v.co.y >= top_y]
    vg.add(pin_ids, 1.0, 'REPLACE')
    return obj


def create_drapes():
    shoulder_z = Z['shoulder'] * HEIGHT
    # Shuka rouge : epaule gauche, tombe en diagonale
    shuka = _create_drape(
        'Drape_Shuka', 'Mat_Shuka', '#C0392B',
        size_x=0.55, size_y=1.15,
        location=(0.12, 0.02, shoulder_z - 0.55),
        rotation=(math.radians(90), 0, math.radians(8)),
    )
    # Drape ivoire : hanches
    ivoire = _create_drape(
        'Drape_Ivoire', 'Mat_Lin', '#FAFAF0',
        size_x=0.62, size_y=0.95,
        location=(-0.02, 0.0, Z['pelvis'] * HEIGHT - 0.42),
        rotation=(math.radians(90), 0, 0),
    )
    print("[CHAR] Drape_Shuka + Drape_Ivoire crees (vertex group 'Pin')")
    return shuka, ivoire


# ─── ARMATURE ────────────────────────────────────────────────────────────────

def create_rig():
    _delete_if_exists('Naset_Rig')
    arm = bpy.data.armatures.new('Naset_Rig')
    rig = bpy.data.objects.new('Naset_Rig', arm)
    _link(rig)
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode='EDIT')

    h = HEIGHT
    eb = arm.edit_bones

    def bone(name, head, tail, parent=None, connect=False):
        b = eb.new(name)
        b.head, b.tail = head, tail
        if parent:
            b.parent = eb[parent]
            b.use_connect = connect
        return b

    # Colonne
    bone('pelvis', (0, 0, Z['pelvis'] * h), (0, 0, Z['spine_00'] * h))
    bone('spine_00', (0, 0, Z['spine_00'] * h), (0, 0, Z['spine_01'] * h), 'pelvis', True)
    bone('spine_01', (0, 0, Z['spine_01'] * h), (0, 0, Z['spine_02'] * h), 'spine_00', True)
    bone('spine_02', (0, 0, Z['spine_02'] * h), (0, 0, Z['chest'] * h), 'spine_01', True)
    bone('chest', (0, 0, Z['chest'] * h), (0, 0, Z['neck'] * h), 'spine_02', True)
    bone('neck', (0, 0, Z['neck'] * h), (0, 0, Z['head'] * h), 'chest', True)
    bone('head', (0, 0, Z['head'] * h), (0, 0, Z['top'] * h), 'neck', True)

    # Paupieres (pour animate_blink)
    ez = Z['head'] * h + 0.05
    bone('eyelid.L', (0.032, -0.07, ez), (0.032, -0.10, ez), 'head')
    bone('eyelid.R', (-0.032, -0.07, ez), (-0.032, -0.10, ez), 'head')

    # Bras / jambes
    for side, sfx in ((1, '.L'), (-1, '.R')):
        sx = SHOULDER_X * side
        bone('shoulder' + sfx, (0.04 * side, 0, Z['shoulder'] * h), (sx, 0, Z['shoulder'] * h), 'chest')
        bone('upper_arm' + sfx, (sx, 0, Z['shoulder'] * h),
             ((SHOULDER_X + 0.09) * side, 0, Z['elbow'] * h), 'shoulder' + sfx)
        bone('forearm' + sfx, ((SHOULDER_X + 0.09) * side, 0, Z['elbow'] * h),
             ((SHOULDER_X + 0.13) * side, 0, Z['hand'] * h), 'upper_arm' + sfx, True)
        hx = HIP_X * side
        bone('thigh' + sfx, (hx, 0, Z['pelvis'] * h), (hx, 0.01, Z['knee'] * h), 'pelvis')
        bone('shin' + sfx, (hx, 0.01, Z['knee'] * h), (hx, -0.01, 0.02), 'thigh' + sfx, True)
        bone('foot' + sfx, (hx, -0.01, 0.02), (hx, -0.09, 0.0), 'shin' + sfx, True)

    bpy.ops.object.mode_set(mode='OBJECT')
    print(f"[CHAR] Naset_Rig — {len(arm.bones)} os (chest + eyelid.L/R inclus)")
    return rig


def bind_body_to_rig(body, rig, eyes, hair):
    # Corps : skinning automatique
    bpy.ops.object.select_all(action='DESELECT')
    body.select_set(True)
    rig.select_set(True)
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')

    # Yeux + cheveux : suivent l'os head (parent_set garde la position monde)
    rig.data.bones.active = rig.data.bones['head']
    bpy.ops.object.select_all(action='DESELECT')
    for obj in [*eyes, hair]:
        obj.select_set(True)
    rig.select_set(True)
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.parent_set(type='BONE', keep_transform=True)
    print("[CHAR] Body skinne (auto weights) · yeux + cheveux parentes a 'head'")


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    print("\n━━━ N'Aset OFM · Character Builder ━━━")
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    body = create_body()
    eyes = create_eyes()
    hair = create_hair()
    create_drapes()
    rig = create_rig()
    bind_body_to_rig(body, rig, eyes, hair)
    print("━━━ Personnage genere : Naset_Body + Naset_Rig + drapes + tresses ━━━\n")


main()
