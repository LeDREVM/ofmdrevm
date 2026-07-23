"""
_loader.py — DREVM Materials Library
Charge tous les .shader (ou une categorie) dans le fichier Blender courant.

  blender --background scene.blend --python _loader.py                      # tout
  blender --background scene.blend --python _loader.py -- --category Metals # une categorie
"""

import bpy  # noqa: F401  (les .shader en ont besoin dans leur namespace)
import os
import sys

LIB_DIR = os.path.dirname(os.path.abspath(__file__))


def parse_category():
    argv = sys.argv
    args = argv[argv.index('--') + 1:] if '--' in argv else []
    if '--category' in args:
        i = args.index('--category')
        if i + 1 < len(args):
            return args[i + 1]
    return None


def load_all(category=None):
    n_before = len(bpy.data.materials)
    loaded, errors = [], []
    for root, dirs, files in os.walk(LIB_DIR):
        cat = os.path.basename(root)
        if category and cat.lower() != category.lower():
            continue
        for f in sorted(files):
            if not f.endswith('.shader'):
                continue
            path = os.path.join(root, f)
            try:
                with open(path, encoding='utf-8') as fh:
                    exec(compile(fh.read(), path, 'exec'), {'__name__': '__main__'})
                loaded.append(f'{cat}/{f}')
            except Exception as e:
                errors.append(f'{cat}/{f} : {e}')

    print('\n━━━ DREVM Materials Loader ━━━')
    for item in loaded:
        print(f'  ✓ {item}')
    for item in errors:
        print(f'  ✗ {item}')
    print(f'[LOADER] {len(loaded)} shaders charges · '
          f'{len(bpy.data.materials) - n_before} nouveaux materiaux · '
          f'{len(errors)} erreurs')
    return len(errors) == 0


if not load_all(parse_category()):
    sys.exit(1)
