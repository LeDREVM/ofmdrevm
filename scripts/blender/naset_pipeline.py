"""
naset_pipeline.py — ORCHESTRATEUR du pipeline Blender N'Aset OFM.

Enchaine automatiquement, en local :
  1. naset_scene_setup.py        (scene, render Cycles, materiaux de base)
  2. naset_character.py          (Naset_Body + Naset_Rig + drapes + tresses)
  3. naset_materials_rig_fx.py   (materiaux complets, particules, cloth)
  4. naset_cameras_cm.py         (5 cameras du court metrage + lumieres)
  5. naset_animation_blender.py  (S1-S2, respiration, clignements)
  6. Sauvegarde Naset_Master_v1.blend (+ rendu test optionnel)

Usage headless (local, sans ouvrir l'interface) :
  blender --background --python scripts/blender/naset_pipeline.py
  blender --background --python scripts/blender/naset_pipeline.py -- --render test
  blender --background --python scripts/blender/naset_pipeline.py -- --render test --frame 120

Usage GUI : ouvrir dans le Text Editor > Alt+P (sans rendu test par defaut).
"""

import bpy
import os
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
BLEND_OUT = os.path.join(PROJECT_DIR, 'Naset_Master_v1.blend')
TEST_OUT = os.path.join(PROJECT_DIR, 'renders', 'pipeline_test')

# Ordre d'execution — chaque script lance son main() a l'import
STAGES = [
    'naset_scene_setup.py',
    'naset_environment.py',
    'naset_character.py',
    'naset_materials_rig_fx.py',
    'naset_cameras_cm.py',
    'naset_animation_blender.py',
]


def parse_args():
    """Recupere les args apres '--' (convention Blender)."""
    argv = sys.argv
    args = argv[argv.index('--') + 1:] if '--' in argv else []
    opts = {'render': 'none', 'frame': 120}
    i = 0
    while i < len(args):
        if args[i] == '--render' and i + 1 < len(args):
            opts['render'] = args[i + 1]
            i += 2
        elif args[i] == '--frame' and i + 1 < len(args):
            opts['frame'] = int(args[i + 1])
            i += 2
        else:
            i += 1
    return opts


def setup_gpu():
    """Cycles GPU (OPTIX > CUDA > HIP), fallback CPU si aucun device."""
    try:
        prefs = bpy.context.preferences.addons['cycles'].preferences
        for backend in ('OPTIX', 'CUDA', 'HIP'):
            try:
                prefs.compute_device_type = backend
                prefs.get_devices()
                gpus = [d for d in prefs.devices if d.type != 'CPU']
                if gpus:
                    for d in prefs.devices:
                        d.use = True
                    bpy.context.scene.cycles.device = 'GPU'
                    print(f"[GPU] Cycles {backend} — {len(gpus)} device(s)")
                    return True
            except TypeError:
                continue
    except Exception as e:
        print(f"[GPU] Echec config ({e})")
    bpy.context.scene.cycles.device = 'CPU'
    print("[GPU] Aucun GPU — fallback CPU")
    return False


def run_stage(filename):
    path = os.path.join(SCRIPT_DIR, filename)
    if not os.path.exists(path):
        print(f"[PIPELINE] ⚠ ABSENT : {filename} — etape sautee")
        return False
    print(f"\n[PIPELINE] ▶ {filename}")
    t0 = time.time()
    with open(path, encoding='utf-8') as f:
        code = f.read()
    exec(compile(code, path, 'exec'), {'__name__': '__main__', '__file__': path})
    print(f"[PIPELINE] ✓ {filename} ({time.time() - t0:.1f}s)")
    return True


def render_test(frame):
    """1 frame en basse qualite — preuve que la scene rend sans erreur."""
    scene = bpy.context.scene
    os.makedirs(TEST_OUT, exist_ok=True)
    keep = (scene.cycles.samples, scene.render.resolution_percentage,
            scene.render.filepath)
    scene.cycles.samples = 16
    scene.render.resolution_percentage = 25
    scene.frame_set(frame)
    scene.render.filepath = os.path.join(TEST_OUT, f'Naset_test_F{frame:04d}')
    bpy.ops.render.render(write_still=True)
    print(f"[RENDER] Test OK → {scene.render.filepath}.png")
    (scene.cycles.samples, scene.render.resolution_percentage,
     scene.render.filepath) = keep


def main():
    opts = parse_args()
    print('\n╔══════════════════════════════════════════════╗')
    print('║   N\'ASET OFM — PIPELINE LOCAL COMPLET       ║')
    print('╚══════════════════════════════════════════════╝')
    t0 = time.time()

    # Scene vierge en headless pour un resultat deterministe
    if bpy.app.background:
        bpy.ops.wm.read_factory_settings(use_empty=True)

    ok, failed = [], []
    for stage in STAGES:
        try:
            if run_stage(stage):
                ok.append(stage)
            else:
                failed.append(stage)
        except Exception as e:
            failed.append(stage)
            print(f"[PIPELINE] ✗ {stage} : {e}")

    setup_gpu()

    bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
    print(f"\n[SAVE] {BLEND_OUT}")

    if opts['render'] == 'test':
        render_test(opts['frame'])

    print('\n╔══════════════════════════════════════════════╗')
    print(f"║  Etapes OK     : {len(ok)}/{len(STAGES)}")
    for s in failed:
        print(f"║  Etape ECHEC   : {s}")
    print(f"║  Duree totale  : {time.time() - t0:.1f}s")
    print(f"║  Fichier       : Naset_Master_v1.blend")
    print('╚══════════════════════════════════════════════╝')
    if failed:
        sys.exit(1)


main()
