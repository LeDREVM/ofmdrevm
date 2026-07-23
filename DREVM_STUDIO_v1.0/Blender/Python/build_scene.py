"""
build_scene.py — DREVM Studio · ORCHESTRATEUR
Construit une scene de travail complete en local.

Usage headless :
  blender --background --python build_scene.py -- --project luna
  blender --background --python build_scene.py -- --project naset --quality prod
  blender --background --python build_scene.py -- --project luna --render test

Usage GUI : Text Editor > Alt+P (defaut : projet luna, preview, pas de rendu).

Etapes :
  1. create_project.py           collections + unites + fps
  2. create_render_settings.py   Cycles GPU + preset qualite
  3. create_material_library.py  7 materiaux studio
  4. create_world_shader.py      3 mondes (actif selon --project)
  5. create_camera_rig.py        rig dolly/grue/focus
  6. create_geometry_nodes.py    lune + poussiere doree
  7. Save DREVM_[projet]_build.blend (+ rendu test optionnel)
"""

import bpy
import os
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STUDIO_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))  # DREVM_STUDIO_v1.0/

STAGES = [
    'create_project.py',
    'create_render_settings.py',
    'create_material_library.py',
    'create_world_shader.py',
    'create_camera_rig.py',
    'create_geometry_nodes.py',
]

PROJECT_WORLD = {'luna': 'World_Night_Luna', 'naset': 'World_Sunset_Naset',
                 'studio': 'World_Studio'}


def parse_args():
    argv = sys.argv
    args = argv[argv.index('--') + 1:] if '--' in argv else []
    opts = {'project': 'luna', 'quality': 'preview', 'render': 'none', 'frame': 60}
    i = 0
    while i < len(args):
        key = args[i].lstrip('-')
        if key in opts and i + 1 < len(args):
            opts[key] = int(args[i + 1]) if key == 'frame' else args[i + 1]
            i += 2
        else:
            i += 1
    return opts


def run_stage(filename):
    path = os.path.join(SCRIPT_DIR, filename)
    print(f"\n[BUILD] ▶ {filename}")
    t0 = time.time()
    with open(path, encoding='utf-8') as f:
        exec(compile(f.read(), path, 'exec'), {'__name__': '__main__', '__file__': path})
    print(f"[BUILD] ✓ {filename} ({time.time() - t0:.1f}s)")


def apply_project(opts):
    """Ajustements post-etapes selon le projet et la qualite demandes."""
    world_name = PROJECT_WORLD[opts['project']]
    world = bpy.data.worlds.get(world_name)
    if world:
        bpy.context.scene.world = world
        print(f"[BUILD] World actif : {world_name}")

    if opts['quality'] == 'prod':
        scene = bpy.context.scene
        scene.render.resolution_x, scene.render.resolution_y = 3840, 2160
        scene.cycles.samples = 256
        print("[BUILD] Qualite prod : 4K · 256 samples")


def render_test(frame):
    scene = bpy.context.scene
    out_dir = os.path.join(STUDIO_DIR, 'Assets', 'build_test')
    os.makedirs(out_dir, exist_ok=True)
    keep = (scene.cycles.samples, scene.render.resolution_percentage, scene.render.filepath)
    scene.cycles.samples = 16
    scene.render.resolution_percentage = 25
    scene.frame_set(frame)
    scene.render.filepath = os.path.join(out_dir, f'DREVM_build_F{frame:04d}')
    bpy.ops.render.render(write_still=True)
    print(f"[RENDER] Test OK → {scene.render.filepath}.png")
    (scene.cycles.samples, scene.render.resolution_percentage, scene.render.filepath) = keep


def main():
    opts = parse_args()
    print('\n╔══════════════════════════════════════════════╗')
    print(f"║   DREVM STUDIO — BUILD '{opts['project'].upper()}'")
    print('╚══════════════════════════════════════════════╝')
    t0 = time.time()

    if bpy.app.background:
        bpy.ops.wm.read_factory_settings(use_empty=True)

    ok, failed = [], []
    for stage in STAGES:
        try:
            run_stage(stage)
            ok.append(stage)
        except Exception as e:
            failed.append(stage)
            print(f"[BUILD] ✗ {stage} : {e}")

    apply_project(opts)

    blend_path = os.path.join(STUDIO_DIR, f"DREVM_{opts['project']}_build.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"\n[SAVE] {blend_path}")

    if opts['render'] == 'test':
        render_test(opts['frame'])

    print('\n╔══════════════════════════════════════════════╗')
    print(f"║  Etapes OK    : {len(ok)}/{len(STAGES)}")
    for s in failed:
        print(f"║  Etape ECHEC  : {s}")
    print(f"║  Duree        : {time.time() - t0:.1f}s")
    print('╚══════════════════════════════════════════════╝')
    if failed:
        sys.exit(1)


main()
