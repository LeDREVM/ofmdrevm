"""
naset_camera_animation.py
Anime la caméra sur les 5 scènes du CM N'Aset OFM.
Keyframes : position, focale, DOF aperture.
Prérequis : naset_scene_setup.py déjà lancé (Camera_Principale doit exister).
Lance depuis Blender : Text Editor > Run Script
"""

import bpy
import mathutils


# ─── DONNÉES PAR SCÈNE ────────────────────────────────────────────────────────
#
# Structure Court Métrage :
# S1 :  frames   1 –  240  (35mm fixe, f/8)
# S2 :  frames 241 –  960  (50mm dolly in, f/2.8)
# S3 :  frames 961 – 1440  (85mm fixe, f/1.8)
# S4 :  frames 1441 – 1920  (85mm, zoom subtil f/1.8 → f/1.4)
# S5 :  frames 1921 – 2280  (85mm fixe, f/1.4)

SCENES = {
    'S1_start': {
        'frame':    1,
        'location': (0.0, -10.0, 1.65),
        'target':   (0.0,   0.0, 1.65),
        'lens':     35.0,
        'fstop':    8.0,
    },
    'S2_start': {
        'frame':    241,
        'location': (0.0, -10.0, 1.65),
        'target':   (0.0,   0.0, 1.65),
        'lens':     50.0,
        'fstop':    2.8,
    },
    'S2_end': {
        'frame':    960,
        'location': (0.0, -2.0, 1.65),  # dolly in 8m sur 720 frames
        'target':   (0.0,  0.0, 1.65),
        'lens':     50.0,
        'fstop':    2.8,
    },
    'S3_start': {
        'frame':    961,
        'location': (0.0, -1.8, 1.65),
        'target':   (0.0,  0.0, 1.65),
        'lens':     85.0,
        'fstop':    1.8,
    },
    'S4_start': {
        'frame':    1441,
        'location': (0.0, -1.8, 1.65),
        'target':   (0.0,  0.0, 1.65),
        'lens':     85.0,
        'fstop':    1.8,
    },
    'S4_end': {
        'frame':    1920,
        'location': (0.0, -1.8, 1.65),
        'target':   (0.0,  0.0, 1.65),
        'lens':     85.0,
        'fstop':    1.4,
    },
    'S5_start': {
        'frame':    1921,
        'location': (0.0, -1.8, 1.65),
        'target':   (0.0,  0.0, 1.65),
        'lens':     85.0,
        'fstop':    1.4,
    },
    'S5_end': {
        'frame':    2280,
        'location': (0.0, -1.8, 1.65),
        'target':   (0.0,  0.0, 1.65),
        'lens':     85.0,
        'fstop':    1.4,
    },
}


# ─── UTILITAIRES ──────────────────────────────────────────────────────────────

def set_keyframe(obj, frame, location=None, data_path=None, value=None, index=-1):
    bpy.context.scene.frame_set(frame)
    if location is not None:
        obj.location = location
        obj.keyframe_insert(data_path='location', frame=frame)
    if data_path is not None:
        # data_path = chemin relatif à obj.data
        exec(f"obj.data.{data_path} = {value}")
        obj.data.keyframe_insert(data_path=data_path, frame=frame, index=index)


def set_interpolation(obj, interpolation='BEZIER'):
    if obj.animation_data and obj.animation_data.action:
        for fcurve in obj.animation_data.action.fcurves:
            for keyframe in fcurve.keyframe_points:
                keyframe.interpolation = interpolation


# ─── ANIMATION CAMÉRA ─────────────────────────────────────────────────────────

def animate_camera():
    cam_obj = bpy.data.objects.get('Camera_Principale')
    if not cam_obj:
        print("[ERREUR] Camera_Principale introuvable — lance naset_scene_setup.py d'abord")
        return

    target_obj = bpy.data.objects.get('Camera_Target')
    if not target_obj:
        print("[ERREUR] Camera_Target introuvable — lance naset_scene_setup.py d'abord")
        return

    cam = cam_obj.data

    # Effacer les animations existantes
    cam_obj.animation_data_clear()
    cam.animation_data_clear()
    target_obj.animation_data_clear()

    for key, params in SCENES.items():
        frame = params['frame']
        bpy.context.scene.frame_set(frame)

        # Position caméra
        cam_obj.location = params['location']
        cam_obj.keyframe_insert(data_path='location', frame=frame)

        # Position target
        target_obj.location = params['target']
        target_obj.keyframe_insert(data_path='location', frame=frame)

        # Focale
        cam.lens = params['lens']
        cam.keyframe_insert(data_path='lens', frame=frame)

        # Ouverture DOF
        cam.dof.aperture_fstop = params['fstop']
        cam.dof.keyframe_insert(data_path='aperture_fstop', frame=frame)

        print(f"[CAM] {key} · frame {frame} · {params['lens']}mm · f/{params['fstop']}")

    # Interpolation douce
    set_interpolation(cam_obj, 'BEZIER')
    print("[CAM] Animation caméra terminée")


# ─── ANIMATION ÉMISSION YEUX ──────────────────────────────────────────────────
# Keyframes d'émission sur Mat_Yeux_Iris (nœud Emission > Strength)

def animate_eye_emission():
    mat = bpy.data.materials.get('Mat_Yeux_Iris')
    if not mat or not mat.use_nodes:
        print("[SKIP] Mat_Yeux_Iris introuvable")
        return

    emit_node = next((n for n in mat.node_tree.nodes if n.type == 'EMISSION'), None)
    mix_node  = next((n for n in mat.node_tree.nodes if n.type == 'MIX_SHADER'), None)
    if not emit_node or not mix_node:
        print("[SKIP] Nœuds Emission/Mix introuvables dans Mat_Yeux_Iris")
        return

    keyframes = [
        (1,    0.0, 0.0),   # début : yeux normaux
        (1600, 0.0, 0.0),   # S4 début
        (1920, 0.08, 0.08), # S4 fin — lueur subtile
        (1921, 0.08, 0.08), # S5 début
        (1960, 1.2,  0.9),  # S5 — éveil complet
        (2280, 1.2,  0.9),  # fin
    ]
    for frame, strength, mix_fac in keyframes:
        bpy.context.scene.frame_set(frame)
        emit_node.inputs['Strength'].default_value = strength
        emit_node.inputs['Strength'].keyframe_insert('default_value', frame=frame)
        mix_node.inputs['Fac'].default_value = mix_fac
        mix_node.inputs['Fac'].keyframe_insert('default_value', frame=frame)

    print("[ANIM] Émission yeux keyframée")


# ─── ANIMATION ÉMISSION BIJOUX ────────────────────────────────────────────────

def animate_gold_emission():
    mat = bpy.data.materials.get('Mat_Or_Emission')
    if not mat or not mat.use_nodes:
        print("[SKIP] Mat_Or_Emission introuvable")
        return

    emit_node = next((n for n in mat.node_tree.nodes if n.type == 'EMISSION'), None)
    mix_node  = next((n for n in mat.node_tree.nodes if n.type == 'MIX_SHADER'), None)
    if not emit_node or not mix_node:
        print("[SKIP] Nœuds introuvables dans Mat_Or_Emission")
        return

    keyframes = [
        (1,    0.0,  0.0),
        (500,  0.2,  0.2),   # S2 — première lueur
        (1600, 0.45, 0.35),  # S4 — montée
        (1921, 0.45, 0.35),
        (1980, 2.0,  0.8),   # S5 — irradiation
        (2200, 2.0,  0.8),
    ]
    for frame, strength, mix_fac in keyframes:
        bpy.context.scene.frame_set(frame)
        emit_node.inputs['Strength'].default_value = strength
        emit_node.inputs['Strength'].keyframe_insert('default_value', frame=frame)
        mix_node.inputs['Fac'].default_value = mix_fac
        mix_node.inputs['Fac'].keyframe_insert('default_value', frame=frame)

    print("[ANIM] Émission bijoux keyframée")


# ─── POINT D'ENTRÉE ───────────────────────────────────────────────────────────

def main():
    print("\n━━━ N'Aset OFM · Camera & FX Animation ━━━")
    animate_camera()
    animate_eye_emission()
    animate_gold_emission()
    bpy.context.scene.frame_set(1)
    print("━━━ Animation terminée — frame reset à 1 ━━━\n")


main()
