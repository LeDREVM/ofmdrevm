"""
╔══════════════════════════════════════════════════════════════╗
║        𓂀  N'ASET OFM — Scripts Animation Blender 4.x        ║
║        Divine Maasaï · Ordre du Feu Mystique                ║
║        Scènes 1 & 2 — Court Métrage Sacré                   ║
╚══════════════════════════════════════════════════════════════╝

USAGE :
  1. Ouvre Blender 4.x
  2. Va dans l'éditeur Scripting (onglet en haut)
  3. Crée un nouveau script, colle le bloc voulu
  4. Lance avec le bouton ▶ Run Script

PRÉREQUIS :
  - Personnage N'Aset riggé (Armature nommée "Naset_Rig")
  - Mesh drapé avec Cloth Sim (objet nommé "Drape_Shuka")
  - Caméra principale nommée "Camera_Principale"
  - Objet vide nommé "Camera_Target" (point de visée)
  - Collection particules nommée "Particules_Or"
  - HDRI world configuré

CONVENTION :
  - FPS : 24
  - Scène 1 : frames 1  → 240  (10 sec)
  - Scène 2 : frames 241 → 960  (30 sec)
  - Scène 3 : frames 961 → 1440 (20 sec · à venir)
"""

import bpy
import mathutils
import math


# ─────────────────────────────────────────────────────────────────────────────
# UTILITAIRES COMMUNS
# ─────────────────────────────────────────────────────────────────────────────

def set_fps(fps=24):
    """Régle le projet sur 24fps cinéma."""
    bpy.context.scene.render.fps = fps
    bpy.context.scene.render.fps_base = 1.0
    print(f"[OFM] ✓ FPS = {fps}")


def _obj_fcurves(obj):
    """Fcurves de l'action d'un objet — compatible Blender 5.0 (layered actions)
    ou l'acces direct action.fcurves a ete supprime."""
    ad = obj.animation_data
    if not ad or not ad.action:
        return []
    act = ad.action
    if hasattr(act, 'fcurves'):          # Blender <= 4.x
        return act.fcurves
    fcs = []
    for layer in act.layers:             # Blender 5.0+
        for strip in layer.strips:
            cb = strip.channelbag(ad.action_slot) if ad.action_slot else None
            if cb:
                fcs.extend(cb.fcurves)
    return fcs


def clear_keyframes(obj, data_path=None, frame_start=1, frame_end=9999):
    """Supprime les keyframes d'un objet dans une plage donnée."""
    if obj.animation_data and obj.animation_data.action:
        for fc in _obj_fcurves(obj):
            if data_path is None or fc.data_path == data_path:
                kp_to_remove = [kp for kp in fc.keyframe_points
                                 if frame_start <= kp.co.x <= frame_end]
                for kp in kp_to_remove:
                    fc.keyframe_points.remove(kp)


def smooth_interpolation(obj, data_path=None, frame_start=1, frame_end=9999):
    """Passe tous les keyframes en interpolation BEZIER (mouvement fluide)."""
    if obj.animation_data and obj.animation_data.action:
        for fc in _obj_fcurves(obj):
            if data_path is None or fc.data_path == data_path:
                for kp in fc.keyframe_points:
                    if frame_start <= kp.co.x <= frame_end:
                        kp.interpolation = 'BEZIER'
                        kp.easing = 'AUTO'
    print(f"[OFM] ✓ Interpolation BEZIER appliquée → {obj.name}")


def linear_interpolation(obj, data_path=None, frame_start=1, frame_end=9999):
    """Passe les keyframes en LINEAR (vitesse constante — travelling)."""
    if obj.animation_data and obj.animation_data.action:
        for fc in _obj_fcurves(obj):
            if data_path is None or fc.data_path == data_path:
                for kp in fc.keyframe_points:
                    if frame_start <= kp.co.x <= frame_end:
                        kp.interpolation = 'LINEAR'


def insert_loc_rot(obj, frame):
    """Insère un keyframe location + rotation sur l'objet."""
    bpy.context.scene.frame_set(frame)
    obj.keyframe_insert(data_path="location", frame=frame)
    obj.keyframe_insert(data_path="rotation_euler", frame=frame)


def get_obj(name):
    """Récupère un objet Blender par nom avec message d'erreur clair."""
    obj = bpy.data.objects.get(name)
    if obj is None:
        print(f"[OFM] ⚠ Objet introuvable : '{name}' — vérifie le nom dans Outliner")
    return obj


# ─────────────────────────────────────────────────────────────────────────────
# ██████████████████████████████████████████████████████████████████████████
# SCÈNE 1 · PLAN LARGE SAVANE  ·  frames 1 → 240  (0 – 10 sec @ 24fps)
# ██████████████████████████████████████████████████████████████████████████
# Description :
#   Silhouette de dos · Vent dans le drapé · Particules dorées
#   Caméra fixe 35mm · N'Aset légèrement de dos, légèrement décalée
# ─────────────────────────────────────────────────────────────────────────────

def setup_scene1_camera():
    """
    SCÈNE 1 — Caméra 35mm fixe, plan large.
    Position : légèrement derrière et à droite · sujet au tiers gauche
    """
    cam_obj = get_obj("Camera_Principale")
    if not cam_obj:
        return

    cam = cam_obj.data
    cam.lens = 35                  # Focale 35mm — plan large
    cam.dof.use_dof = True
    cam.dof.aperture_fstop = 4.0   # f/4 — profondeur plus large sur plan large
    cam.dof.focus_distance = 5.0   # Distance de mise au point (ajuste selon scène)

    # Position caméra — légèrement derrière N'Aset
    # N'Aset est à l'origine (0,0,0) en A-pose
    cam_obj.location = mathutils.Vector((-1.2, 4.5, 1.6))
    cam_obj.rotation_euler = mathutils.Euler(
        (math.radians(90), 0, math.radians(-12)), 'XYZ'
    )

    # Pas de mouvement — caméra statique sur cette scène
    bpy.context.scene.frame_set(1)
    insert_loc_rot(cam_obj, 1)
    insert_loc_rot(cam_obj, 240)

    print("[OFM] ✓ Scène 1 — Caméra 35mm posée (statique)")


def setup_scene1_wind():
    """
    SCÈNE 1 — Champ de force Wind pour le drapé Shúkà.
    Crée un Force Field 'Wind_Scene1' ou met à jour s'il existe.
    """
    wind_name = "Wind_Scene1"
    wind_obj = bpy.data.objects.get(wind_name)

    if not wind_obj:
        bpy.ops.object.effector_add(type='WIND', location=(3.0, 0.0, 1.2))
        wind_obj = bpy.context.active_object
        wind_obj.name = wind_name

    # Orientation : vent vient du côté droit, légèrement de face
    wind_obj.rotation_euler = mathutils.Euler(
        (math.radians(80), 0, math.radians(-30)), 'XYZ'
    )

    field = wind_obj.field
    field.strength = 1.5           # Intensité modérée — doux mais visible
    field.noise = 0.8              # Turbulence organique
    field.seed = 42                # Seed reproductible
    field.flow = 0.3               # Flot fluide

    # Animation du vent : légère variation en S1 pour naturel
    bpy.context.scene.frame_set(1)
    field.keyframe_insert(data_path="strength", frame=1)
    field.strength = 2.0
    field.keyframe_insert(data_path="strength", frame=120)
    field.strength = 1.2
    field.keyframe_insert(data_path="strength", frame=240)

    print("[OFM] ✓ Scène 1 — Wind Force Field configuré")


def setup_scene1_particles():
    """
    SCÈNE 1 — Particules dorées flottantes autour de N'Aset.
    Utilise un système de particules sur un émetteur invisible.
    """
    emitter_name = "Particules_Or_Emitter"
    emitter = bpy.data.objects.get(emitter_name)

    if not emitter:
        bpy.ops.mesh_add(type='PLANE', size=2.0, location=(0, 0, 0.5))
        emitter = bpy.context.active_object
        emitter.name = emitter_name

    # Rendre l'émetteur invisible au rendu
    emitter.hide_render = True
    emitter.display_type = 'WIRE'

    # Créer / Récupérer le système de particules
    if len(emitter.particle_systems) == 0:
        bpy.ops.object.particle_system_add()

    ps = emitter.particle_systems[0]
    ps.name = "PS_Or"
    settings = ps.settings

    # Paramètres particules
    settings.type = 'EMITTER'
    settings.count = 80                # Peu de particules — épuré et sacré
    settings.lifetime = 120            # 5 secondes de vie à 24fps
    settings.lifetime_random = 0.3    # Variation organique
    settings.frame_start = 1
    settings.frame_end = 200
    settings.emit_from = 'FACE'
    settings.use_emit_random = True

    # Physique — montée lente
    settings.physics_type = 'NEWTON'
    settings.mass = 0.01
    settings.factor_random = 0.4

    # Gravité négative légère (flottement ascendant)
    settings.effector_weights.gravity = -0.08

    # Taille des particules
    settings.particle_size = 0.006
    settings.size_random = 0.5

    # Rendu en sphère
    settings.render_type = 'HALO'  # Blender 5.0 : 'SPHERE' supprime de l'enum

    # Matériau or émissif — à créer séparément dans le Shader Editor
    # Ou assigne un matériau existant nommé "Mat_Or_Emission"
    mat_or = bpy.data.materials.get("Mat_Or_Emission")
    if mat_or:
        if emitter.data.materials:
            emitter.data.materials[0] = mat_or
        else:
            emitter.data.materials.append(mat_or)

    print("[OFM] ✓ Scène 1 — Particules Or configurées (80 pts, montée lente)")


def scene1_run_all():
    """Lance toute la configuration Scène 1 d'un seul appel."""
    print("\n[OFM] ══ SCÈNE 1 · Plan Large Savane ══")
    set_fps(24)
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = 240
    setup_scene1_camera()
    setup_scene1_wind()
    setup_scene1_particles()
    print("[OFM] ✓ Scène 1 COMPLÈTE — Lance le rendu frames 1→240\n")


# ─────────────────────────────────────────────────────────────────────────────
# ██████████████████████████████████████████████████████████████████████████
# SCÈNE 2 · TRAVELLING AVANT  ·  frames 241 → 960  (10 – 40 sec @ 24fps)
# ██████████████████████████████████████████████████████████████████████████
# Description :
#   Caméra 50mm · Dolly lent vers N'Aset · Lumière rasante golden hour
#   Mouvement ultra-fluide — aucune secousse — cinéma contemplatif
# ─────────────────────────────────────────────────────────────────────────────

def setup_scene2_camera():
    """
    SCÈNE 2 — Travelling avant (dolly in), 50mm, très lent.
    Démarre loin, termine à distance portrait.

    Position départ  : 8m de N'Aset
    Position arrivée : 2.5m de N'Aset (plan poitrine)
    Durée            : 720 frames = 30 secondes
    """
    cam_obj = get_obj("Camera_Principale")
    if not cam_obj:
        return

    cam = cam_obj.data
    cam.lens = 50                   # Focale 50mm — plan poitrine naturel
    cam.dof.use_dof = True
    cam.dof.aperture_fstop = 2.8    # f/2.8 — bokeh doux arrière-plan
    cam.dof.focus_distance = 3.0    # Focus initial — se resserre en fin

    # ── Position départ (frame 241) ──────────────────────────────────
    START_FRAME = 241
    bpy.context.scene.frame_set(START_FRAME)

    cam_obj.location = mathutils.Vector((0.3, 8.0, 1.65))
    cam_obj.rotation_euler = mathutils.Euler(
        (math.radians(90), 0, math.radians(2)), 'XYZ'
    )
    # DoF : focus sur le visage à 8m
    cam.dof.focus_distance = 8.0
    cam_obj.keyframe_insert(data_path="location", frame=START_FRAME)
    cam_obj.keyframe_insert(data_path="rotation_euler", frame=START_FRAME)
    cam.dof.keyframe_insert(data_path="focus_distance", frame=START_FRAME)

    # ── Position intermédiaire (frame 600 = 15sec dans S2) ───────────
    MID_FRAME = 600
    bpy.context.scene.frame_set(MID_FRAME)

    cam_obj.location = mathutils.Vector((0.15, 5.0, 1.65))
    cam_obj.rotation_euler = mathutils.Euler(
        (math.radians(90), 0, math.radians(1)), 'XYZ'
    )
    cam.dof.focus_distance = 5.0
    cam_obj.keyframe_insert(data_path="location", frame=MID_FRAME)
    cam_obj.keyframe_insert(data_path="rotation_euler", frame=MID_FRAME)
    cam.dof.keyframe_insert(data_path="focus_distance", frame=MID_FRAME)

    # ── Position arrivée (frame 960) ─────────────────────────────────
    END_FRAME = 960
    bpy.context.scene.frame_set(END_FRAME)

    cam_obj.location = mathutils.Vector((0.05, 2.5, 1.65))
    cam_obj.rotation_euler = mathutils.Euler(
        (math.radians(90), 0, math.radians(0)), 'XYZ'
    )
    cam.dof.focus_distance = 2.5    # Focus serré sur iris en fin
    cam_obj.keyframe_insert(data_path="location", frame=END_FRAME)
    cam_obj.keyframe_insert(data_path="rotation_euler", frame=END_FRAME)
    cam.dof.keyframe_insert(data_path="focus_distance", frame=END_FRAME)

    # Interpolation LINEAR pour vitesse constante du travelling
    linear_interpolation(cam_obj, frame_start=241, frame_end=960)

    print("[OFM] ✓ Scène 2 — Travelling avant 50mm (8m → 2.5m, 30 sec)")


def setup_scene2_lighting_animation():
    """
    SCÈNE 2 — Animation subtile de la lumière golden hour.
    La lumière key baisse très légèrement en fin de travelling
    pour créer un effet de soleil qui descend.
    """
    key_light = get_obj("Key_Light")
    if not key_light:
        print("[OFM] ⚠ 'Key_Light' introuvable — crée une Area Light nommée Key_Light")
        return

    light_data = key_light.data

    # Début S2 : lumière pleine golden hour
    bpy.context.scene.frame_set(241)
    light_data.energy = 800
    light_data.color = (1.0, 0.82, 0.55)     # Chaud 4800K
    light_data.keyframe_insert(data_path="energy", frame=241)
    light_data.keyframe_insert(data_path="color", frame=241)

    # Fin S2 : lumière légèrement plus chaude/basse (crépuscule)
    bpy.context.scene.frame_set(960)
    light_data.energy = 650
    light_data.color = (1.0, 0.72, 0.40)     # Plus orange — soleil bas
    light_data.keyframe_insert(data_path="energy", frame=960)
    light_data.keyframe_insert(data_path="color", frame=960)

    smooth_interpolation(key_light, frame_start=241, frame_end=960)
    print("[OFM] ✓ Scène 2 — Lumière golden hour animée")


def setup_scene2_focal_breathing():
    """
    SCÈNE 2 — Micro-breathing de focale (effet 'vivant' de l'objectif).
    Très subtil — ±0.3mm sur 50mm. Imperceptible consciemment.
    """
    cam_obj = get_obj("Camera_Principale")
    if not cam_obj:
        return

    cam = cam_obj.data

    # Oscille entre 49.7 et 50.3 mm toutes les 72 frames (~3sec)
    keyframes_focal = [
        (241, 50.0),
        (313, 49.7),
        (385, 50.0),
        (457, 50.3),
        (529, 50.0),
        (601, 49.7),
        (673, 50.0),
        (745, 50.3),
        (817, 50.0),
        (889, 49.7),
        (960, 50.0),
    ]

    for frame, lens_val in keyframes_focal:
        bpy.context.scene.frame_set(frame)
        cam.lens = lens_val
        cam.keyframe_insert(data_path="lens", frame=frame)

    smooth_interpolation(cam_obj, frame_start=241, frame_end=960)
    print("[OFM] ✓ Scène 2 — Micro-breathing focale (±0.3mm)")


def scene2_run_all():
    """Lance toute la configuration Scène 2 d'un seul appel."""
    print("\n[OFM] ══ SCÈNE 2 · Travelling Avant ══")
    bpy.context.scene.frame_end = max(bpy.context.scene.frame_end, 960)
    setup_scene2_camera()
    setup_scene2_lighting_animation()
    setup_scene2_focal_breathing()
    print("[OFM] ✓ Scène 2 COMPLÈTE — Travelling frames 241→960\n")


# ─────────────────────────────────────────────────────────────────────────────
# ██████████████████████████████████████████████████████████████████████████
# HELPERS ANIMATION ORGANIQUE — Communs à toutes les scènes
# ██████████████████████████████████████████████████████████████████████████
# ─────────────────────────────────────────────────────────────────────────────

def animate_breathing(rig_name="Naset_Rig",
                       bone_chest="chest",
                       frame_start=1,
                       frame_end=960,
                       amplitude=0.012,
                       cycle_frames=60):
    """
    Respiration subtile via scale de l'os 'chest' sur l'armature.
    N'Aset respire doucement — 1 respiration toutes les 2.5 secondes.

    Paramètres :
        rig_name      : nom de l'armature Blender
        bone_chest    : nom de l'os poitrine (varie selon le rig)
        frame_start   : première frame d'animation
        frame_end     : dernière frame
        amplitude     : amplitude du scale (0.012 = 1.2% — très subtil)
        cycle_frames  : longueur d'un cycle respiratoire en frames
    """
    rig = get_obj(rig_name)
    if not rig:
        return

    if rig.type != 'ARMATURE':
        print(f"[OFM] ⚠ '{rig_name}' n'est pas une Armature")
        return

    # Passer en Pose Mode pour accéder aux os
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode='POSE')

    bone = rig.pose.bones.get(bone_chest)
    if not bone:
        print(f"[OFM] ⚠ Os '{bone_chest}' introuvable — vérifie le nom dans Pose Mode")
        bpy.ops.object.mode_set(mode='OBJECT')
        return

    # Générer les keyframes de respiration
    frame = frame_start
    phase = 0  # 0 = expiration, 1 = inspiration

    while frame <= frame_end:
        bpy.context.scene.frame_set(frame)
        if phase == 0:
            bone.scale = mathutils.Vector((1.0, 1.0, 1.0))           # Expiration
        else:
            bone.scale = mathutils.Vector((1.0,
                                           1.0 + amplitude,
                                           1.0 + amplitude))           # Inspiration
        bone.keyframe_insert(data_path="scale", frame=frame)
        frame += cycle_frames // 2
        phase = 1 - phase

    bpy.ops.object.mode_set(mode='OBJECT')
    smooth_interpolation(rig, frame_start=frame_start, frame_end=frame_end)
    print(f"[OFM] ✓ Respiration animée → {rig_name}:{bone_chest} (amplitude {amplitude*100:.1f}%)")


def animate_blink(rig_name="Naset_Rig",
                  bone_eyelid_l="eyelid.L",
                  bone_eyelid_r="eyelid.R",
                  frame_start=1,
                  frame_end=960,
                  blink_frames=8,
                  blink_every=150):
    """
    Clignements d'yeux — naturels et irréguliers.
    1 clignement toutes les ~6 secondes avec légère variation.

    Paramètres :
        blink_frames : durée d'un clignement (8 frames = 1/3 sec)
        blink_every  : intervalle entre clignements en frames
    """
    rig = get_obj(rig_name)
    if not rig:
        return

    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode='POSE')

    bone_l = rig.pose.bones.get(bone_eyelid_l)
    bone_r = rig.pose.bones.get(bone_eyelid_r)

    if not bone_l or not bone_r:
        print(f"[OFM] ⚠ Os paupières introuvables : '{bone_eyelid_l}' / '{bone_eyelid_r}'")
        bpy.ops.object.mode_set(mode='OBJECT')
        return

    import random
    random.seed(42)  # Seed fixe — reproductible

    frame = frame_start + blink_every  # Premier clignement
    while frame + blink_frames <= frame_end:
        # Yeux ouverts — avant clignement
        for bone in [bone_l, bone_r]:
            bpy.context.scene.frame_set(frame - 1)
            bone.location.z = 0.0
            bone.keyframe_insert(data_path="location", frame=frame - 1)

        # Yeux fermés — milieu du clignement
        close_frame = frame + blink_frames // 2
        for bone in [bone_l, bone_r]:
            bpy.context.scene.frame_set(close_frame)
            bone.location.z = -0.04   # Fermeture (valeur à adapter selon rig)
            bone.keyframe_insert(data_path="location", frame=close_frame)

        # Yeux ouverts — après clignement
        open_frame = frame + blink_frames
        for bone in [bone_l, bone_r]:
            bpy.context.scene.frame_set(open_frame)
            bone.location.z = 0.0
            bone.keyframe_insert(data_path="location", frame=open_frame)

        # Prochain clignement — intervalle légèrement aléatoire
        variation = random.randint(-20, 20)
        frame += blink_every + variation

    bpy.ops.object.mode_set(mode='OBJECT')
    smooth_interpolation(rig, frame_start=frame_start, frame_end=frame_end)
    print(f"[OFM] ✓ Clignements animés → {rig_name} (tous les ~{blink_every}f)")


def animate_eye_emission(material_name="Mat_Yeux_Iris",
                          node_emission="Emission_Divin",
                          frame_start=1920,
                          frame_wake=1960,
                          frame_end=2280,
                          strength_max=0.15):
    """
    SCÈNE FINALE — Montée de l'émission divine dans les yeux.
    0.0 → strength_max sur 40 frames (~ 1.7 sec).

    Paramètres :
        material_name  : nom du matériau iris dans Blender
        node_emission  : nom du nœud Emission dans le shader
        frame_wake     : frame où commence la montée d'émission
        strength_max   : intensité maximale (0.15 recommandé)
    """
    mat = bpy.data.materials.get(material_name)
    if not mat:
        print(f"[OFM] ⚠ Matériau '{material_name}' introuvable")
        return

    if not mat.node_tree:
        print(f"[OFM] ⚠ '{material_name}' n'a pas de node tree")
        return

    emission_node = mat.node_tree.nodes.get(node_emission)
    if not emission_node:
        print(f"[OFM] ⚠ Nœud '{node_emission}' introuvable dans {material_name}")
        return

    # Intensité à 0 au départ
    bpy.context.scene.frame_set(frame_start)
    emission_node.inputs["Strength"].default_value = 0.0
    emission_node.inputs["Strength"].keyframe_insert("default_value", frame=frame_start)

    # Début de montée
    bpy.context.scene.frame_set(frame_wake)
    emission_node.inputs["Strength"].default_value = 0.0
    emission_node.inputs["Strength"].keyframe_insert("default_value", frame=frame_wake)

    # Pic d'émission — Éveil
    bpy.context.scene.frame_set(frame_end)
    emission_node.inputs["Strength"].default_value = strength_max
    emission_node.inputs["Strength"].keyframe_insert("default_value", frame=frame_end)

    print(f"[OFM] ✓ Émission yeux : 0.0 → {strength_max} (frames {frame_wake}→{frame_end})")


def animate_camera_shake_subtle(cam_name="Camera_Principale",
                                 frame_start=1,
                                 frame_end=240,
                                 amplitude=0.001,
                                 frequency=6):
    """
    MICRO-TREMBLEMENT caméra (simulation caméra à l'épaule — très subtil).
    Uniquement pour les plans fixes (Scène 1, Scène 3).
    NE PAS utiliser sur le travelling Scène 2.

    amplitude  : 0.001m = 1mm (à peine perceptible — c'est voulu)
    frequency  : changement de direction toutes les N frames
    """
    cam_obj = get_obj(cam_name)
    if not cam_obj:
        return

    import random
    random.seed(7)

    base_loc = cam_obj.location.copy()
    frame = frame_start
    while frame <= frame_end:
        bpy.context.scene.frame_set(frame)
        offset = mathutils.Vector((
            random.uniform(-amplitude, amplitude),
            random.uniform(-amplitude * 0.5, amplitude * 0.5),
            random.uniform(-amplitude * 0.3, amplitude * 0.3)
        ))
        cam_obj.location = base_loc + offset
        cam_obj.keyframe_insert(data_path="location", frame=frame)
        frame += frequency

    smooth_interpolation(cam_obj, frame_start=frame_start, frame_end=frame_end)
    print(f"[OFM] ✓ Micro-shake caméra (amplitude {amplitude*1000:.1f}mm)")


# ─────────────────────────────────────────────────────────────────────────────
# ██████████████████████████████████████████████████████████████████████████
# MATÉRIAU OR ÉMISSIF — Créer depuis script si pas encore fait
# ██████████████████████████████████████████████████████████████████████████
# ─────────────────────────────────────────────────────────────────────────────

def create_material_or_emission():
    """
    Crée le matériau 'Mat_Or_Emission' pour les particules dorées.
    Emission très faible — or sacré flottant.
    """
    mat_name = "Mat_Or_Emission"
    mat = bpy.data.materials.get(mat_name)

    if mat:
        print(f"[OFM] ℹ Matériau '{mat_name}' déjà existant")
        return mat

    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Output
    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (400, 0)

    # Emission
    em = nodes.new("ShaderNodeEmission")
    em.location = (200, 0)
    em.inputs["Color"].default_value = (0.949, 0.588, 0.228, 1.0)  # #C9963A
    em.inputs["Strength"].default_value = 0.2      # Très léger — sacré subtil
    em.label = "Emission_Or"

    links.new(em.outputs["Emission"], out.inputs["Surface"])

    print(f"[OFM] ✓ Matériau '{mat_name}' créé (or émissif #C9963A · strength 0.2)")
    return mat


# ─────────────────────────────────────────────────────────────────────────────
# ██████████████████████████████████████████████████████████████████████████
# POINT D'ENTRÉE — Lance les deux scènes en séquence
# ██████████████████████████████████████████████████████████████████████████
# ─────────────────────────────────────────────────────────────────────────────

def run_full_pipeline():
    """
    Lance toute la configuration animation :
      - Scène 1 (Plan large)
      - Scène 2 (Travelling)
      - Helpers organiques (respiration, clignements)
    """
    print("\n╔══════════════════════════════════════════╗")
    print("║  𓂀  N'Aset OFM — Pipeline Animation     ║")
    print("╚══════════════════════════════════════════╝\n")

    set_fps(24)
    create_material_or_emission()

    # Scènes principales
    scene1_run_all()
    scene2_run_all()

    # Animations organiques globales (toutes les scènes)
    animate_breathing(frame_start=1, frame_end=960)
    animate_blink(frame_start=1, frame_end=960)
    animate_camera_shake_subtle(frame_start=1, frame_end=240)  # S1 seulement

    print("\n╔══════════════════════════════════════════╗")
    print("║  ✓ Pipeline COMPLET                      ║")
    print("║  Frames 1 → 960 configurées              ║")
    print("║  Lance F12 pour tester un rendu test     ║")
    print("╚══════════════════════════════════════════╝\n")


# ─────────────────────────────────────────────────────────────────────────────
# EXÉCUTION — Décommenter la ligne correspondante dans le Script Editor
# ─────────────────────────────────────────────────────────────────────────────

# ── Option 1 : Tout d'un coup ────────────────────────────────────────────────
run_full_pipeline()

# ── Option 2 : Scène par scène ──────────────────────────────────────────────
# scene1_run_all()
# scene2_run_all()

# ── Option 3 : Helpers individuels ──────────────────────────────────────────
# animate_breathing()
# animate_blink()
# animate_camera_shake_subtle()
# animate_eye_emission()   # Réserver pour la scène finale (frames 1920+)

# ── Option 4 : Matériau or uniquement ───────────────────────────────────────
# create_material_or_emission()
