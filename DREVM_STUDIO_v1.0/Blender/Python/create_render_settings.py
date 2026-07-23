"""
create_render_settings.py — DREVM Studio
Presets Cycles GPU. Deux modes :
    apply_preset('preview')  — 1080p 64 samples, iteration rapide
    apply_preset('prod')     — 4K 256 samples, denoise, sortie finale
Par defaut : preview (build_scene passe 'prod' via --quality prod).
Compatible Blender 5.0 (look sans prefixe 'Filmic - ').
"""

import bpy

PRESETS = {
    'preview': {'res': (1920, 1080), 'samples': 64, 'denoise': True},
    'prod':    {'res': (3840, 2160), 'samples': 256, 'denoise': True},
}


def setup_gpu():
    """OPTIX > CUDA > HIP, fallback CPU. Retourne True si GPU actif."""
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
                    print(f"[RENDER] GPU {backend} — {len(gpus)} device(s)")
                    return True
            except TypeError:
                continue
    except Exception as e:
        print(f"[RENDER] Config GPU impossible ({e})")
    bpy.context.scene.cycles.device = 'CPU'
    print("[RENDER] Fallback CPU")
    return False


def apply_preset(name='preview'):
    p = PRESETS[name]
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.render.resolution_x, scene.render.resolution_y = p['res']
    scene.render.resolution_percentage = 100
    scene.render.fps = 24
    scene.cycles.samples = p['samples']
    scene.cycles.use_denoising = p['denoise']

    # Colorimetrie DREVM — Blender 5.0 : pas de prefixe 'Filmic - ' dans look
    scene.view_settings.view_transform = 'Filmic'
    scene.view_settings.look = 'Medium High Contrast'

    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_depth = '16'
    scene.render.film_transparent = False

    print(f"[RENDER] Preset '{name}' : {p['res'][0]}x{p['res'][1]} · "
          f"{p['samples']} samples · Filmic Medium High Contrast")


def main(preset='preview'):
    print("\n━━━ DREVM Studio · Render Settings ━━━")
    apply_preset(preset)
    setup_gpu()
    print("━━━ Rendu configure ━━━\n")


main()
