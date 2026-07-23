"""
naset_cameras_cm.py
Setup caméras cinématiques du Court Métrage N'Aset OFM (95s · 2280 frames).
5 caméras dédiées (une par scène) + cibles Track To + dolly S2 + keyframes focus + 3 lumières.
Chaque caméra est activée à sa scène via un marqueur (camera bind) — comme les Camera Cuts UE5.

Lance depuis Blender : Text Editor > Run Script

Récap :
  S1  1–240    35mm f/5.6  fixe
  S2  241–960  50mm f/2.8  dolly in 8m (-12 → -4)
  S3  961–1440 85mm f/2.0  fixe
  S4  1441–1920 85mm f/1.8 fixe + defocus (0.85 → 1.20) + regard qui s'abaisse
  S5  1921–2280 85mm f/1.4 fixe + émission yeux/bijoux
"""

import bpy
import math


# ─── PARAMÈTRES GLOBAUX ───────────────────────────────────────────────────────

SENSOR_WIDTH = 36.0    # Full Frame horizontal
CLIP_START   = 0.01
CLIP_END     = 1000.0
BLADES       = 9       # bokeh à 9 lamelles (cercles réguliers sur l'or)

FRAME_START  = 1
FRAME_END    = 2280
FPS          = 24


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


def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4))


# ─── DÉFINITION DES CAMÉRAS ───────────────────────────────────────────────────
# Chaque caméra a sa propre cible (Track To) pour pouvoir viser une hauteur différente.

CAMERAS = {
    'Camera_S1': {
        'bind_frame': 1,
        'lens': 35.0, 'fstop': 5.6, 'use_dof': False,
        'location': (0.0, -8.0, 1.70),
        'focus': 8.0,
        'target': (0.0, 0.0, 1.60),   # centre masse — silhouette de dos
    },
    'Camera_S2': {
        'bind_frame': 241,
        'lens': 50.0, 'fstop': 2.8, 'use_dof': True,
        'location': (0.0, -12.0, 1.70),
        'focus': 12.0,
        'target': (0.0, 0.0, 1.65),
    },
    'Camera_S3': {
        'bind_frame': 961,
        'lens': 85.0, 'fstop': 2.0, 'use_dof': True,
        'location': (0.0, -0.85, 1.72),
        'focus': 0.85,
        'target': (0.0, 0.0, 1.72),   # yeux
    },
    'Camera_S4': {
        'bind_frame': 1441,
        'lens': 85.0, 'fstop': 1.8, 'use_dof': True,
        'location': (0.0, -0.85, 1.72),
        'focus': 0.85,
        'target': (0.0, 0.0, 1.72),
    },
    'Camera_S5': {
        'bind_frame': 1921,
        'lens': 85.0, 'fstop': 1.4, 'use_dof': True,
        'location': (0.0, -0.85, 1.72),
        'focus': 0.85,
        'target': (0.0, 0.0, 1.72),
    },
}


def setup_render():
    scene = bpy.context.scene
    scene.frame_start = FRAME_START
    scene.frame_end   = FRAME_END
    scene.render.fps  = FPS
    scene.render.resolution_x = 3840
    scene.render.resolution_y = 2160
    scene.render.resolution_percentage = 100
    scene.view_settings.view_transform = 'Filmic'
    # Blender 5.0 : plus de prefixe 'Filmic - ' dans l'enum look
    scene.view_settings.look           = 'Medium High Contrast'
    print("[RENDER] 4K · 24fps · Filmic Medium High Contrast")


def create_cameras():
    scene = bpy.context.scene

    for name, p in CAMERAS.items():
        # Nettoyage si réexécution
        for obj_name in (name, name + '_Target'):
            if obj_name in bpy.data.objects:
                bpy.data.objects.remove(bpy.data.objects[obj_name], do_unlink=True)

        # Cible Track To
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=p['target'])
        target = bpy.context.active_object
        target.name = name + '_Target'

        # Caméra
        bpy.ops.object.camera_add(location=p['location'])
        cam_obj = bpy.context.active_object
        cam_obj.name = name
        cam = cam_obj.data
        cam.name = name
        cam.lens          = p['lens']
        cam.sensor_fit    = 'HORIZONTAL'
        cam.sensor_width  = SENSOR_WIDTH
        cam.clip_start    = CLIP_START
        cam.clip_end      = CLIP_END
        cam.dof.use_dof          = p['use_dof']
        cam.dof.aperture_fstop   = p['fstop']
        cam.dof.aperture_blades  = BLADES
        cam.dof.focus_distance   = p['focus']

        # Contrainte Track To vers sa cible
        c = cam_obj.constraints.new(type='TRACK_TO')
        c.target    = target
        c.track_axis = 'TRACK_NEGATIVE_Z'
        c.up_axis    = 'UP_Y'

        # Marqueur de bind — active la caméra à sa scène
        marker = scene.timeline_markers.new(name + '_cut', frame=p['bind_frame'])
        marker.camera = cam_obj

        print(f"[CAM] {name} · {p['lens']}mm · f/{p['fstop']} · bind@{p['bind_frame']}")

    # Caméra active par défaut
    scene.camera = bpy.data.objects['Camera_S1']


# ─── ANIMATION S2 — DOLLY IN ──────────────────────────────────────────────────

def animate_s2_dolly():
    cam_obj = bpy.data.objects.get('Camera_S2')
    if not cam_obj:
        print("[SKIP] Camera_S2 introuvable")
        return
    cam = cam_obj.data

    # Position : dolly avant -12 → -4 (8m sur 720 frames)
    keys_loc = [(241, (0.0, -12.0, 1.70)), (960, (0.0, -4.0, 1.65))]
    for frame, loc in keys_loc:
        bpy.context.scene.frame_set(frame)
        cam_obj.location = loc
        cam_obj.keyframe_insert('location', frame=frame)

    # Focus distance suit le dolly : 12 → 4 (interpolation linéaire)
    keys_focus = [(241, 12.0), (960, 4.0)]
    for frame, fd in keys_focus:
        bpy.context.scene.frame_set(frame)
        cam.dof.focus_distance = fd
        cam.dof.keyframe_insert('focus_distance', frame=frame)

    _set_interp(cam_obj, 'LINEAR')
    _set_interp(cam, 'LINEAR')
    print("[ANIM] S2 dolly in + focus 12→4 (linéaire)")


# ─── ANIMATION S4 — DEFOCUS + REGARD QUI S'ABAISSE ────────────────────────────

def animate_s4_close():
    cam_obj = bpy.data.objects.get('Camera_S4')
    target  = bpy.data.objects.get('Camera_S4_Target')
    if not cam_obj or not target:
        print("[SKIP] Camera_S4 / target introuvable")
        return
    cam = cam_obj.data

    # Focus : 0.85 net → 1.20 défocalisation douce (Ease In)
    for frame, fd in [(1441, 0.85), (1920, 1.20)]:
        bpy.context.scene.frame_set(frame)
        cam.dof.focus_distance = fd
        cam.dof.keyframe_insert('focus_distance', frame=frame)

    # Cible descend : regard qui s'abaisse (Z 1.72 → 1.68)
    for frame, z in [(1441, 1.72), (1920, 1.68)]:
        bpy.context.scene.frame_set(frame)
        target.location.z = z
        target.keyframe_insert('location', index=2, frame=frame)

    # Ease In sur les fcurves S4
    for holder in (cam, target):
        if holder.animation_data and holder.animation_data.action:
            for fc in _obj_fcurves(holder):
                for kp in fc.keyframe_points:
                    kp.interpolation = 'SINE'
                    kp.easing = 'EASE_IN'
    print("[ANIM] S4 defocus 0.85→1.20 + regard abaissé (Ease In)")


# ─── LUMIÈRES — 3 POINTS CINÉMATIQUES ─────────────────────────────────────────

def create_lights():
    lights = {
        'Key_Light':  {'energy': 800, 'color': hex_to_rgb('#FFD580'),
                       'location': (3.0, -3.0, 4.0), 'rotation': (45, 0, 30)},
        'Fill_Light': {'energy': 200, 'color': hex_to_rgb('#E8C49A'),
                       'location': (-4.0, -2.0, 2.5), 'rotation': (0, 0, 0)},
        'Rim_Light':  {'energy': 400, 'color': hex_to_rgb('#C9963A'),
                       'location': (0.0, 4.0, 3.0), 'rotation': (0, 0, 0)},
    }
    for name, p in lights.items():
        if name in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)
        bpy.ops.object.light_add(type='AREA', location=p['location'])
        obj = bpy.context.active_object
        obj.name = name
        obj.rotation_euler = tuple(math.radians(a) for a in p['rotation'])
        obj.data.name   = name
        obj.data.energy = p['energy']
        obj.data.color  = p['color']
        obj.data.size   = 2.0
        print(f"[LIGHT] {name} · {p['energy']}W")


# ─── UTILITAIRE INTERPOLATION ─────────────────────────────────────────────────

def _set_interp(holder, mode):
    if holder.animation_data and holder.animation_data.action:
        for fc in _obj_fcurves(holder):
            for kp in fc.keyframe_points:
                kp.interpolation = mode


# ─── POINT D'ENTRÉE ───────────────────────────────────────────────────────────

def main():
    print("\n━━━ N'Aset OFM · Camera Setup CM (5 caméras) ━━━")
    setup_render()
    create_cameras()
    animate_s2_dolly()
    animate_s4_close()
    create_lights()
    bpy.context.scene.frame_set(1)
    print("━━━ Setup caméras terminé — frame reset à 1 ━━━")
    print("Note : émissions yeux/bijoux S5 → lance naset_camera_animation.py\n")


main()
