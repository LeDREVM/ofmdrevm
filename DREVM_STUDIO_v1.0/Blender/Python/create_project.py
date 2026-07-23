"""
create_project.py — DREVM Studio
Pose les fondations d'une scene : collections, unites, fps, timeline.
Idempotent : reutilise les collections existantes.
"""

import bpy

COLLECTIONS = [
    '00_CAMERAS',
    '10_CHARACTERS',
    '20_ENVIRONMENT',
    '30_FX',
    '40_LIGHTS',
    '90_HELPERS',
]

FPS = 24


def get_or_create_collection(name, parent=None):
    coll = bpy.data.collections.get(name)
    if not coll:
        coll = bpy.data.collections.new(name)
    parent = parent or bpy.context.scene.collection
    if name not in [c.name for c in parent.children]:
        try:
            parent.children.link(coll)
        except RuntimeError:
            pass  # deja liee ailleurs
    return coll


def setup_units_and_time():
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0
    scene.render.fps = FPS
    scene.frame_start = 1
    print(f"[PROJECT] Unites metriques · {FPS} fps · frame_start 1")


def main():
    print("\n━━━ DREVM Studio · Create Project ━━━")
    setup_units_and_time()
    for name in COLLECTIONS:
        get_or_create_collection(name)
    # 90_HELPERS exclu du rendu
    helpers = bpy.data.collections.get('90_HELPERS')
    if helpers:
        helpers.hide_render = True
    print(f"[PROJECT] {len(COLLECTIONS)} collections pretes")
    print("━━━ Projet initialise ━━━\n")


main()
