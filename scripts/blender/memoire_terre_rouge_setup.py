"""
memoire_terre_rouge_setup.py
Setup complet de la scène narrative "La Mémoire de la Terre Rouge" (N'Aset OFM · Guadeloupe).
45 secondes · 1080 frames · 24fps · 6 scènes · 4K vertical 9:16 (2160×3840) · Cycles GPU.

Version FUSIONNÉE — combine :
  · Soleil Guadeloupe (SUN + ciel) · terre rouge riche · silhouettes translucides
  · Caméras par scène LIÉES aux marqueurs timeline (switch auto au rendu)
  · Animations narratives : silhouettes (S3), yeux (S4), or (S5)

Script autonome — aucun prérequis. Lance depuis Blender : Text Editor > Run Script (Alt+P).
Le personnage N'Aset (Naset_Body) s'importe séparément ; un placeholder est créé si absent.
Les matériaux Mat_Yeux_Iris (yeux) et Mat_Or_Emission (or) viennent idéalement de
naset_scene_setup.py ; le script crée Mat_Or_Emission lui-même et saute proprement les yeux si absents.

⚠️ Blender 5.0 : pas de blend_method, look sans préfixe "Filmic - ", inputs Principled 4.0+.
"""

import bpy
import math


# ─── PALETTE COULEUR ──────────────────────────────────────────────────────────

def hex_to_linear(hex_str):
    hex_str = hex_str.lstrip('#')
    r, g, b = (int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    def to_lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (to_lin(r), to_lin(g), to_lin(b), 1.0)

COLOR = {
    'terre_rouge':     hex_to_linear('#8B3A1A'),
    'terre_sombre':    hex_to_linear('#6B2A0E'),
    'or_sacre':        hex_to_linear('#C9963A'),
    'or_clair':        hex_to_linear('#E8BC6A'),
    'soleil_gwadloup': hex_to_linear('#FFD580'),
    'ciel_bleu':       hex_to_linear('#87CEEB'),
    'rouge_shuka':     hex_to_linear('#C0392B'),
    'blanc_ivoire':    hex_to_linear('#FAFAF0'),
    'accent':          hex_to_linear('#1C1A3A'),
    'peau_base':       hex_to_linear('#6B3D2E'),
    'yeux':            hex_to_linear('#1A0D00'),
}


# ─── PARAMÈTRES & DÉCOUPAGE NARRATIF ──────────────────────────────────────────

FRAME_START = 1
FRAME_END   = 1080   # 45s @ 24fps
FPS         = 24
N_ANCETRES  = 6      # silhouettes ancestrales (S3)

# (nom, frame_start, frame_end, caméra liée)
SCENES = [
    ('S1_Sol_Parle',     1,   168,  'Cam_S1_SolMacro'),
    ('S2_Apparition',    169, 336,  'Cam_S2_Apparition'),
    ('S3_Memoire',       337, 528,  'Cam_S3_Memoire'),
    ('S4_Regard',        529, 720,  'Cam_S4_Regard'),
    ('S5_Force_Vivante', 721, 912,  'Cam_S5_Force'),
    ('S6_Titre',         913, 1080, 'Cam_S5_Force'),   # S6 = noir/titre en post → réutilise S5
]

# Caméras par scène : lens, f-stop, position, rotation (degrés X), distance de mise au point (m)
# ⚠️ 'focus' est obligatoire : sans lui le DOF reste sur son défaut (10 m) et tout est flou.
# ⚠️ Cam_S1 doit rester HORS du volume de Naset_Body (cylindre r=0.30 à l'origine),
#    sinon la macro rend l'intérieur du mesh → image noire.
CAMERAS = {
    'Cam_S1_SolMacro':  {'lens': 100.0, 'fstop': 2.8, 'location': (0.0, -0.55, 0.10), 'rot_x': 80, 'focus': 0.55},
    'Cam_S2_Apparition':{'lens': 50.0,  'fstop': 2.8, 'location': (0.0, -3.0,  1.65), 'rot_x': 90, 'focus': 3.0},
    'Cam_S3_Memoire':   {'lens': 35.0,  'fstop': 8.0, 'location': (0.0, -8.0,  1.80), 'rot_x': 88, 'focus': 8.0},
    'Cam_S4_Regard':    {'lens': 135.0, 'fstop': 1.4, 'location': (0.0, -0.8,  1.68), 'rot_x': 90, 'focus': 0.8},
    'Cam_S5_Force':     {'lens': 50.0,  'fstop': 4.0, 'location': (0.0, -4.0,  1.65), 'rot_x': 90, 'focus': 4.0},
}


# ─── NETTOYAGE SCÈNE DE DÉPART ────────────────────────────────────────────────

def clean_default_objects():
    """Supprime Cube/Camera/Light du startup Blender.
    Sans ça le Cube 2m reste planté à l'origine, devant N'Aset, dans TOUS les cadres."""
    for name in ('Cube', 'Camera', 'Light'):
        obj = bpy.data.objects.get(name)
        if obj:
            bpy.data.objects.remove(obj, do_unlink=True)
            print(f"[CLEAN] {name} (startup Blender) supprimé")


# ─── CONFIGURATION SCÈNE & RENDU ──────────────────────────────────────────────

def setup_scene_render():
    scene = bpy.context.scene
    scene.frame_start = FRAME_START
    scene.frame_end   = FRAME_END
    scene.render.fps  = FPS

    scene.unit_settings.system       = 'METRIC'
    scene.unit_settings.scale_length = 0.01
    scene.unit_settings.length_unit  = 'CENTIMETERS'

    render = scene.render
    render.engine                = 'CYCLES'
    # FORMAT FINAL 9:16 vertical (réseaux sociaux) — 4K portrait
    render.resolution_x          = 2160
    render.resolution_y          = 3840
    render.resolution_percentage = 100

    # GPU Cycles — activer les devices (sinon le 'GPU' seul ne suffit pas)
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type = 'OPTIX'   # 'CUDA' / 'HIP' / 'METAL' selon GPU
        prefs.get_devices()
        for d in prefs.devices:
            d.use = True
    except Exception as e:
        print(f"[WARN] Config GPU ignorée : {e}")

    cycles = scene.cycles
    cycles.device                = 'GPU'
    cycles.samples               = 256
    cycles.use_denoising         = True
    cycles.denoiser              = 'OPENIMAGEDENOISE'
    cycles.use_adaptive_sampling = True
    cycles.adaptive_threshold    = 0.01

    scene.view_settings.view_transform = 'Filmic'
    scene.view_settings.look           = 'Medium High Contrast'   # Blender 5.0 : plus de préfixe "Filmic - "

    print(f"[SETUP] {FRAME_START}–{FRAME_END} @ {FPS}fps · 4K vertical 9:16 (2160×3840) · Cycles GPU Filmic")


# ─── MATÉRIAUX ────────────────────────────────────────────────────────────────

def create_material_terre_rouge():
    """Sol terre rouge guadeloupéenne : variation de couleur large + grain fin.

    Deux échelles de bruit obligatoires : le sol fait 200 m mais S1 le cadre en macro
    sur ~20 cm. Un seul noise basse fréquence y rend un aplat uni — le grain fin
    (noise_fin) est ce qui rend la matière lisible dans le plan « le sol parle »."""
    mat = bpy.data.materials.get('Mat_TerreRouge') or bpy.data.materials.new('Mat_TerreRouge')
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out       = nodes.new('ShaderNodeOutputMaterial')
    bsdf      = nodes.new('ShaderNodeBsdfPrincipled')
    texcoord  = nodes.new('ShaderNodeTexCoord')
    noise     = nodes.new('ShaderNodeTexNoise')
    noise_fin = nodes.new('ShaderNodeTexNoise')
    mix_grain = nodes.new('ShaderNodeMixRGB')
    mix_rgb   = nodes.new('ShaderNodeMixRGB')   # legacy mais fonctionnel en 5.0
    bump      = nodes.new('ShaderNodeBump')

    mix_rgb.blend_type = 'MIX'
    mix_rgb.inputs['Color1'].default_value = COLOR['terre_rouge']
    mix_rgb.inputs['Color2'].default_value = COLOR['terre_sombre']

    # ⚠️ Coordonnées Object (unités de la scène) et NON Generated : Generated normalise
    # sur la bounding box, donc agrandir le sol diluerait le grain jusqu'à l'aplat en S1.
    links.new(texcoord.outputs['Object'], noise.inputs['Vector'])
    links.new(texcoord.outputs['Object'], noise_fin.inputs['Vector'])

    # basse fréquence — grandes plaques de terre, ~12 m (visible en plan large S3/S5)
    noise.inputs['Scale'].default_value     = 0.08
    noise.inputs['Detail'].default_value    = 6.0
    noise.inputs['Roughness'].default_value = 0.7

    # haute fréquence — grain de terre, ~7 mm (visible en macro S1)
    noise_fin.inputs['Scale'].default_value     = 150.0
    noise_fin.inputs['Detail'].default_value    = 10.0
    noise_fin.inputs['Roughness'].default_value = 0.85

    # le grain assombrit localement la couleur, sans écraser la variation large
    mix_grain.blend_type = 'MULTIPLY'
    mix_grain.inputs['Fac'].default_value = 0.45

    bsdf.inputs['Roughness'].default_value          = 0.88
    bsdf.inputs['Metallic'].default_value           = 0.0
    bsdf.inputs['Specular IOR Level'].default_value = 0.15

    bump.inputs['Strength'].default_value = 0.45

    links.new(noise.outputs['Fac'],       mix_rgb.inputs['Fac'])
    links.new(mix_rgb.outputs['Color'],   mix_grain.inputs['Color1'])
    links.new(noise_fin.outputs['Fac'],   mix_grain.inputs['Color2'])
    links.new(mix_grain.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(noise_fin.outputs['Fac'],   bump.inputs['Height'])
    links.new(bump.outputs['Normal'],     bsdf.inputs['Normal'])
    links.new(bsdf.outputs['BSDF'],       out.inputs['Surface'])

    texcoord.location  = (-1050, -50)
    noise.location     = (-800, 100)
    noise_fin.location = (-800, -250)
    mix_rgb.location   = (-550, 150)
    mix_grain.location = (-320, 100)
    bump.location      = (-320, -250)
    bsdf.location      = (-50, 0)
    out.location       = (250, 0)
    print("[MAT] Mat_TerreRouge créé (variation large + grain macro + bump)")
    return mat


def create_material_ancetre():
    """Silhouette ancestrale : énergie translucide lumineuse, pas un fantôme réaliste.
    Retourne une COPIE unique à chaque appel pour pouvoir animer chaque ancêtre séparément."""
    base = bpy.data.materials.get('Mat_Ancetre_Base')
    if not base:
        base = bpy.data.materials.new('Mat_Ancetre_Base')
        base.use_nodes = True
        nodes = base.node_tree.nodes
        links = base.node_tree.links
        nodes.clear()

        out  = nodes.new('ShaderNodeOutputMaterial')
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        emit = nodes.new('ShaderNodeEmission')
        mix  = nodes.new('ShaderNodeMixShader')

        bsdf.inputs['Base Color'].default_value          = COLOR['blanc_ivoire']
        bsdf.inputs['Transmission Weight'].default_value = 0.9
        bsdf.inputs['Roughness'].default_value           = 0.0
        bsdf.inputs['Alpha'].default_value               = 0.25
        emit.inputs['Color'].default_value               = COLOR['or_clair']
        emit.inputs['Strength'].default_value            = 0.5
        mix.inputs['Fac'].default_value                  = 0.0   # invisible au départ (keyframé S3)

        links.new(bsdf.outputs['BSDF'],     mix.inputs[1])
        links.new(emit.outputs['Emission'], mix.inputs[2])
        links.new(mix.outputs['Shader'],    out.inputs['Surface'])

        bsdf.location = (-300, 100)
        emit.location = (-300, -100)
        mix.location  = (0, 0)
        out.location  = (250, 0)
        print("[MAT] Mat_Ancetre_Base créé (translucide émissif)")

    return base.copy()


def create_material_or():
    """Or sacré émissif de N'Aset — Mat_Or_Emission (cible de l'animation S5)."""
    mat = bpy.data.materials.get('Mat_Or_Emission') or bpy.data.materials.new('Mat_Or_Emission')
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out  = nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    emit = nodes.new('ShaderNodeEmission')
    mix  = nodes.new('ShaderNodeMixShader')

    bsdf.inputs['Base Color'].default_value = COLOR['or_sacre']
    bsdf.inputs['Metallic'].default_value   = 0.95
    bsdf.inputs['Roughness'].default_value  = 0.10
    emit.inputs['Color'].default_value      = COLOR['or_clair']
    emit.inputs['Strength'].default_value   = 0.15
    mix.inputs['Fac'].default_value         = 0.2

    links.new(bsdf.outputs['BSDF'],     mix.inputs[1])
    links.new(emit.outputs['Emission'], mix.inputs[2])
    links.new(mix.outputs['Shader'],    out.inputs['Surface'])
    print("[MAT] Mat_Or_Emission créé")
    return mat


# ─── SOL (S1) ─────────────────────────────────────────────────────────────────

def create_ground():
    if 'Sol_TerreRouge' in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects['Sol_TerreRouge'], do_unlink=True)

    # 2000 m et non 20 m : le bord du plan doit tomber SOUS l'horizon du ciel,
    # sinon une bande sombre apparaît entre les deux dans les plans larges (S3, S5).
    bpy.ops.mesh.primitive_plane_add(size=2000, location=(0, 0, 0))
    sol = bpy.context.active_object
    sol.name = 'Sol_TerreRouge'

    sub = sol.modifiers.new('Subdivision', 'SUBSURF')
    sub.levels        = 3
    sub.render_levels = 5

    sol.data.materials.append(create_material_terre_rouge())
    print("[OBJ] Sol_TerreRouge · 2000m (jusqu'à l'horizon) · subsurf 3/5")
    return sol


# ─── PLACEHOLDER PERSONNAGE ───────────────────────────────────────────────────

def ensure_naset_placeholder():
    if 'Naset_Body' in bpy.data.objects:
        print("[OBJ] Naset_Body présent — placeholder ignoré")
        return
    bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=1.75, location=(0, 0, 0.875))
    body = bpy.context.active_object
    body.name = 'Naset_Body'

    mat = bpy.data.materials.get('Mat_Peau_Naset') or bpy.data.materials.new('Mat_Peau_Naset')
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value        = COLOR['peau_base']
        bsdf.inputs['Subsurface Weight'].default_value = 0.30
        bsdf.inputs['Subsurface Scale'].default_value  = 0.05
        bsdf.inputs['Roughness'].default_value         = 0.50
    body.data.materials.append(mat)
    print("[OBJ] Naset_Body placeholder (cylindre 1.75m) — remplacer par le vrai mesh")


# ─── SILHOUETTES ANCÊTRES (S3) ────────────────────────────────────────────────

def create_ancestors():
    """Crée N_ANCETRES silhouettes en demi-cercle derrière N'Aset, chacune avec
    son propre matériau (copie) pour une apparition échelonnée en S3."""
    import math as _m
    for i in range(1, N_ANCETRES + 1):
        name = f'Ancetre_{i:02d}'
        if name in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)

        # demi-cercle derrière (Y+) — étalement X 2.8m : en 9:16 le champ horizontal
        # du 35mm à ~12m ne couvre que ±3.4m, un rayon de 4m coupait les extrêmes.
        angle = _m.pi * (i - 1) / (N_ANCETRES - 1)   # 0 → pi
        x = -_m.cos(angle) * 2.8
        y =  3.5 + _m.sin(angle) * 1.5
        bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=1.7, location=(x, y, 0.85))
        anc = bpy.context.active_object
        anc.name = name
        anc.data.materials.append(create_material_ancetre())
    print(f"[OBJ] {N_ANCETRES} silhouettes Ancetre_01..{N_ANCETRES:02d} (demi-cercle)")


# ─── CAMÉRAS + MARQUEURS TIMELINE ─────────────────────────────────────────────

def create_cameras():
    for name, p in CAMERAS.items():
        if name in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)
        bpy.ops.object.camera_add(location=p['location'],
                                  rotation=(math.radians(p['rot_x']), 0, 0))
        cam = bpy.context.active_object
        cam.name = name
        cam.data.name = name
        cam.data.lens = p['lens']
        cam.data.dof.use_dof = True
        cam.data.dof.aperture_fstop = p['fstop']
        cam.data.dof.focus_distance = p['focus']
        print(f"[CAM] {name} · {p['lens']}mm · f/{p['fstop']} · focus {p['focus']}m")


def bind_cameras_to_markers():
    """Un marqueur par scène, lié à sa caméra → switch automatique au rendu/lecture."""
    scene = bpy.context.scene
    scene.timeline_markers.clear()
    for name, frame_start, frame_end, cam_name in SCENES:
        marker = scene.timeline_markers.new(name, frame=frame_start)
        cam = bpy.data.objects.get(cam_name)
        if cam:
            marker.camera = cam
    # caméra active par défaut = S2
    bpy.context.scene.camera = bpy.data.objects.get('Cam_S2_Apparition')
    print("[TIMELINE] 6 marqueurs liés aux caméras (switch auto)")


# ─── LUMIÈRES (ambiance Guadeloupe) ───────────────────────────────────────────

def create_lights():
    lights = {
        'Key_Soleil_Gwadloup': {'type': 'SUN',  'energy': 5.0,  'location': (10, -5, 8),  'color': COLOR['soleil_gwadloup'], 'angle': 0.05},
        'Fill_Ciel':           {'type': 'AREA', 'energy': 120,  'location': (-5, -3, 5),  'color': COLOR['ciel_bleu']},
        'Rim_Or_Naset':        {'type': 'AREA', 'energy': 300,  'location': (2, 4, 2.5),  'color': COLOR['or_sacre']},
    }
    for name, p in lights.items():
        if name in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)
        bpy.ops.object.light_add(type=p['type'], location=p['location'])
        lo = bpy.context.active_object
        lo.name = name
        lo.data.name = name
        lo.data.energy = p['energy']
        lo.data.color = p['color'][:3]
        if p['type'] == 'SUN' and 'angle' in p:
            lo.data.angle = p['angle']
        if p['type'] == 'AREA':
            lo.data.size = 2.0
    print("[LIGHT] Soleil Guadeloupe (SUN) · Ciel bleu · Rim or")


# ─── CIEL (World) ─────────────────────────────────────────────────────────────

def create_world():
    """Ciel de Guadeloupe (Sky Texture Nishita) — sans ça le fond reste le gris
    par défaut de Blender, visible dans tous les plans larges (S3, S5)."""
    world = bpy.data.worlds.get('World_Gwadloup') or bpy.data.worlds.new('World_Gwadloup')
    bpy.context.scene.world = world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    nodes.clear()

    out = nodes.new('ShaderNodeOutputWorld')
    bg  = nodes.new('ShaderNodeBackground')
    sky = nodes.new('ShaderNodeTexSky')

    # ⚠️ Blender 5.0 : 'NISHITA' renommé 'MULTIPLE_SCATTERING', 'dust_density' → 'aerosol_density'
    sky.sky_type         = 'MULTIPLE_SCATTERING'
    sky.sun_elevation    = math.radians(12)   # soleil bas — lumière rasante S1/S2
    sky.sun_rotation     = math.radians(200)
    sky.altitude         = 0
    sky.air_density      = 1.4                # atmosphère chaude, horizon doré
    sky.aerosol_density  = 2.2                # poussière — cohérent avec la terre rouge
    sky.ground_albedo    = 0.25               # rebond de la terre rouge sur le ciel bas
    sky.sun_disc         = False              # le soleil est déjà Key_Soleil_Gwadloup (SUN)
    bg.inputs['Strength'].default_value = 0.6

    world.node_tree.links.new(sky.outputs['Color'], bg.inputs['Color'])
    world.node_tree.links.new(bg.outputs['Background'], out.inputs['Surface'])

    sky.location = (-400, 0)
    bg.location  = (-150, 0)
    out.location = (100, 0)
    print("[WORLD] World_Gwadloup · Multiple Scattering · soleil 12° · horizon doré")


# ─── POUSSIÈRE ROUGE (S1) ─────────────────────────────────────────────────────

def create_dust():
    if 'Particules_PoussiereRouge' in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects['Particules_PoussiereRouge'], do_unlink=True)

    bpy.ops.mesh.primitive_plane_add(size=0.5, location=(0, 0, 0.02))
    emitter = bpy.context.active_object
    emitter.name = 'Particules_PoussiereRouge'

    ps = emitter.modifiers.new(name='PoussiereRouge', type='PARTICLE_SYSTEM')
    s  = ps.particle_system.settings
    s.count          = 500
    s.lifetime       = 120
    s.frame_start    = 1
    s.frame_end      = 168
    s.emit_from      = 'FACE'
    s.physics_type   = 'NEWTON'
    s.normal_factor  = 0.2
    s.factor_random  = 0.5
    s.particle_size  = 0.008
    s.size_random    = 0.6
    s.effector_weights.gravity = -0.05   # léger soulèvement (PAS settings.gravity — n'existe pas)

    # matériau émissif rouge
    mat = bpy.data.materials.get('Mat_PoussiereRouge') or bpy.data.materials.new('Mat_PoussiereRouge')
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    out  = nodes.new('ShaderNodeOutputMaterial')
    emit = nodes.new('ShaderNodeEmission')
    emit.inputs['Color'].default_value    = COLOR['terre_rouge']
    emit.inputs['Strength'].default_value = 0.3
    mat.node_tree.links.new(emit.outputs['Emission'], out.inputs['Surface'])
    emitter.data.materials.append(mat)

    print("[FX] Particules_PoussiereRouge · 500 · soulèvement lent")


# ─── ANIMATION : SILHOUETTES (S3) ─────────────────────────────────────────────

def animate_ancestors():
    """Apparition échelonnée des ancêtres en S3 via le Mix Shader (fade émission)."""
    for i in range(1, N_ANCETRES + 1):
        anc = bpy.data.objects.get(f'Ancetre_{i:02d}')
        if not anc or not anc.data.materials:
            continue
        mat = anc.data.materials[0]
        mix = next((n for n in mat.node_tree.nodes if n.type == 'MIX_SHADER'), None)
        if not mix:
            continue
        offset = i * 8   # apparition non-simultanée
        # L'offset ne s'applique QU'À l'apparition. Le cut S5 (721) est net pour tous :
        # décaler la disparition les laisserait traîner jusqu'à la frame 769 dans S5.
        keys = [
            (336 + offset, 0.0),   # fin S2 — invisible
            (380 + offset, 0.6),   # S3 — apparition échelonnée
            (720,          0.6),   # S4 — encore là
            (721,          0.0),   # cut S5 — disparaissent toutes ensemble
        ]
        for f, fac in keys:
            bpy.context.scene.frame_set(f)
            mix.inputs['Fac'].default_value = fac
            mix.inputs['Fac'].keyframe_insert('default_value', frame=f)

        # ⚠️ Fac 0 ≠ invisible : la branche BSDF (Transmission 0.9) reste rendue en
        # « verre fantôme » dans S1/S2/S5. On masque donc l'objet au rendu hors de
        # sa fenêtre S3–S4 (les keyframes booléens sont steppés → pas d'interpolation).
        vis_keys = [
            (1,            True),    # S1/S2 — masqué
            (336 + offset, False),   # entrée S3 (échelonnée) — visible
            (720,          False),   # fin S4 — visible
            (721,          True),    # cut S5 — masqué
        ]
        for f, hidden in vis_keys:
            anc.hide_render = hidden
            anc.keyframe_insert('hide_render', frame=f)
            anc.hide_viewport = hidden
            anc.keyframe_insert('hide_viewport', frame=f)
    print("[ANIM] Silhouettes ancêtres — apparition échelonnée S3")


# ─── ANIMATION : YEUX (S4) ────────────────────────────────────────────────────

def animate_yeux_s4():
    """Émission dorée des yeux sur 'nou toujou la'. Nécessite Mat_Yeux_Iris (naset_scene_setup.py)."""
    mat = bpy.data.materials.get('Mat_Yeux_Iris')
    if not mat or not mat.use_nodes:
        print("[SKIP] Mat_Yeux_Iris absent — lance naset_scene_setup.py pour les yeux")
        return
    emit = next((n for n in mat.node_tree.nodes if n.type == 'EMISSION'), None)
    mix  = next((n for n in mat.node_tree.nodes if n.type == 'MIX_SHADER'), None)
    if not emit or not mix:
        print("[SKIP] Nœuds Emission/Mix absents dans Mat_Yeux_Iris")
        return
    keys = [
        (528, 0.0,  0.0),
        (529, 0.0,  0.0),
        (625, 0.30, 0.30),   # "nou toujou la" — montée
        (720, 0.30, 0.30),
        (721, 0.0,  0.0),
    ]
    for frame, strength, fac in keys:
        bpy.context.scene.frame_set(frame)
        emit.inputs['Strength'].default_value = strength
        emit.inputs['Strength'].keyframe_insert('default_value', frame=frame)
        mix.inputs['Fac'].default_value = fac
        mix.inputs['Fac'].keyframe_insert('default_value', frame=frame)
    print("[ANIM] Émission yeux S4 — 'nou toujou la'")


# ─── ANIMATION : OR (S5) ──────────────────────────────────────────────────────

def animate_or_s5():
    """L'or monte au pic 'nou sé flanm' (S5)."""
    mat = bpy.data.materials.get('Mat_Or_Emission')
    if not mat or not mat.use_nodes:
        print("[SKIP] Mat_Or_Emission absent")
        return
    emit = next((n for n in mat.node_tree.nodes if n.type == 'EMISSION'), None)
    if not emit:
        return
    keys = [
        (1,   0.15),   # S1→S4 : or subtil constant
        (720, 0.15),
        (721, 0.15),
        (793, 1.20),   # cut N'Aset immobile — "flanm" — or maximal
        (912, 1.20),
        (913, 0.0),    # S6 : fade out (noir)
    ]
    for frame, strength in keys:
        bpy.context.scene.frame_set(frame)
        emit.inputs['Strength'].default_value = strength
        emit.inputs['Strength'].keyframe_insert('default_value', frame=frame)
    print("[ANIM] Or N'Aset S5 — flanm")


# ─── POINT D'ENTRÉE ───────────────────────────────────────────────────────────

def main():
    print("\n━━━ N'Aset OFM · La Mémoire de la Terre Rouge (fusion) ━━━")
    print("Guadeloupe · Mémoire ancestrale · 45s · 1080 frames\n")

    clean_default_objects()
    setup_scene_render()
    create_world()
    create_ground()
    ensure_naset_placeholder()
    create_material_or()
    create_ancestors()
    create_cameras()
    bind_cameras_to_markers()
    create_lights()
    create_dust()

    animate_ancestors()
    animate_yeux_s4()    # sauté proprement si le perso n'est pas chargé
    animate_or_s5()

    bpy.context.scene.frame_set(1)
    print("\n━━━ Setup terminé — 1080 frames prêtes ━━━")
    for name, fs, fe, cam in SCENES:
        print(f"  {name:<18} {fs:>4}–{fe:<4} ({(fe-fs)/FPS:.1f}s) · {cam}")
    print("\nProchaines étapes :")
    print("  1. Importer Naset_Body + lancer naset_scene_setup.py (matériaux perso → yeux dorés S4)")
    print("  2. Vérifier S1 en macro (terre rouge) · presser Espace pour voir le switch caméras")


main()
