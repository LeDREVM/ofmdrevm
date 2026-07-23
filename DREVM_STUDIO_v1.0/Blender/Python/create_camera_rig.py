"""
create_camera_rig.py — DREVM Studio
Rig camera studio dans 00_CAMERAS :
    Cam_Main            — camera 35mm, DOF actif
    CamRig_Dolly        — empty parent : animer sa position = travelling
    CamRig_Crane        — empty intermediaire : animer sa hauteur/rotation = grue
    Cam_Focus_Target    — empty cible : Track To + focus object DOF

Hierarchie : CamRig_Dolly > CamRig_Crane > Cam_Main → track Cam_Focus_Target
Idempotent.
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


def create_rig(lens=35.0, location=(0, -8, 1.6)):
    cams = _coll('00_CAMERAS')
    _delete_if_exists('Cam_Main', 'CamRig_Dolly', 'CamRig_Crane', 'Cam_Focus_Target')

    # Empties du rig
    dolly = bpy.data.objects.new('CamRig_Dolly', None)
    dolly.empty_display_type = 'ARROWS'
    dolly.location = location
    cams.objects.link(dolly)

    crane = bpy.data.objects.new('CamRig_Crane', None)
    crane.empty_display_type = 'SINGLE_ARROW'
    crane.parent = dolly
    cams.objects.link(crane)

    # Camera
    cam_data = bpy.data.cameras.new('Cam_Main')
    cam_data.lens = lens
    cam_data.dof.use_dof = True
    cam_data.dof.aperture_fstop = 2.8
    cam = bpy.data.objects.new('Cam_Main', cam_data)
    cam.parent = crane
    cams.objects.link(cam)

    # Cible focus + regard
    target = bpy.data.objects.new('Cam_Focus_Target', None)
    target.empty_display_type = 'SPHERE'
    target.empty_display_size = 0.15
    target.location = (0, 0, 1.4)
    cams.objects.link(target)

    tc = cam.constraints.new('TRACK_TO')
    tc.target = target
    tc.track_axis = 'TRACK_NEGATIVE_Z'
    tc.up_axis = 'UP_Y'
    cam_data.dof.focus_object = target

    bpy.context.scene.camera = cam
    print(f"[CAMRIG] Cam_Main {lens}mm f/2.8 · Dolly>Crane>Cam · focus target OK")
    return dolly, crane, cam, target


# ─── PRESETS DE MOUVEMENT ────────────────────────────────────────────────────

def preset_dolly_in(frame_start, frame_end, y_from=-10.0, y_to=-2.0):
    """Travelling avant lineaire (S2 N'Aset / E02 Luna)."""
    dolly = bpy.data.objects.get('CamRig_Dolly')
    if not dolly:
        return
    for frame, y in ((frame_start, y_from), (frame_end, y_to)):
        bpy.context.scene.frame_set(frame)
        dolly.location.y = y
        dolly.keyframe_insert('location', index=1, frame=frame)
    print(f"[CAMRIG] Dolly in {y_from}→{y_to} (frames {frame_start}-{frame_end})")


def preset_crane_down(frame_start, frame_end, z_from=6.0, z_to=0.0):
    """Grue descendante (ouverture E05 Luna)."""
    crane = bpy.data.objects.get('CamRig_Crane')
    if not crane:
        return
    for frame, z in ((frame_start, z_from), (frame_end, z_to)):
        bpy.context.scene.frame_set(frame)
        crane.location.z = z
        crane.keyframe_insert('location', index=2, frame=frame)
    print(f"[CAMRIG] Crane down {z_from}→{z_to} (frames {frame_start}-{frame_end})")


def main():
    print("\n━━━ DREVM Studio · Camera Rig ━━━")
    create_rig()
    print("━━━ Rig camera pret (presets : preset_dolly_in / preset_crane_down) ━━━\n")


main()
