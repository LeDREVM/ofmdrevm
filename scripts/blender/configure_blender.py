"""
configure_blender.py
Configure Blender 5.0 pour le projet N'Aset OFM — à lancer en HEADLESS :
  blender -b -P configure_blender.py

Applique et SAUVEGARDE de façon persistante :
  1. GPU de rendu (OptiX NVIDIA, repli CUDA)
  2. Add-ons : Node Wrangler + naset_ofm_toolkit (installé + activé)
  3. Performance (undo, cache mémoire)
  4. Color management Filmic + rendu 4K/24fps dans le fichier de démarrage
  -> save_userpref() (préférences) + save_homefile() (startup)

Réversible : Blender > Fichier > Valeurs par défaut > Charger les réglages d'usine.
"""

import bpy

ADDON_TOOLKIT = r"C:/Users/ardja/Documents/CODING/Blendaah/ofmdrevm/.claude/worktrees/awesome-bose-7c4dc5/addons/naset_ofm_toolkit.py"

log = []
def L(msg):
    log.append(msg)
    print("[CONFIG]", msg)


# ─── 1. GPU DE RENDU ──────────────────────────────────────────────────────────

def setup_gpu():
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
    except KeyError:
        L("Cycles indisponible — GPU ignoré")
        return

    chosen = None
    for backend in ("OPTIX", "CUDA", "HIP", "ONEAPI"):
        try:
            prefs.compute_device_type = backend
        except TypeError:
            continue
        prefs.get_devices()
        gpus = [d for d in prefs.devices if d.type == backend]
        if gpus:
            chosen = backend
            for d in prefs.devices:
                d.use = (d.type != 'CPU')   # active les GPU, laisse le CPU off
            break

    if chosen:
        names = [d.name for d in prefs.devices if d.use]
        L(f"GPU backend : {chosen} · activés : {', '.join(names) or 'aucun'}")
    else:
        L("Aucun GPU détecté (restera sur CPU)")


# ─── 2. ADD-ONS ───────────────────────────────────────────────────────────────

def enable_addon(candidates):
    """Tente d'activer le 1er module qui marche parmi des id possibles."""
    for mod in candidates:
        try:
            bpy.ops.preferences.addon_enable(module=mod)
            L(f"Add-on activé : {mod}")
            return True
        except Exception:
            continue
    L(f"Add-on non activé (essayés : {candidates})")
    return False


def setup_addons():
    # Node Wrangler (nom de module variable selon 4.x/5.0 / système d'extensions)
    enable_addon([
        "node_wrangler",
        "bl_ext.blender_org.node_wrangler",
        "bl_ext.system.node_wrangler",
    ])

    # Toolkit N'Aset : installer puis activer
    import os
    if os.path.exists(ADDON_TOOLKIT):
        try:
            bpy.ops.preferences.addon_install(filepath=ADDON_TOOLKIT, overwrite=True)
            bpy.ops.preferences.addon_enable(module="naset_ofm_toolkit")
            L("naset_ofm_toolkit installé + activé")
        except Exception as e:
            L(f"Échec install toolkit : {e}")
    else:
        L(f"Toolkit introuvable : {ADDON_TOOLKIT}")


# ─── 3. PERFORMANCE ───────────────────────────────────────────────────────────

def setup_performance():
    edit = bpy.context.preferences.edit
    syst = bpy.context.preferences.system
    edit.use_global_undo   = True
    edit.undo_steps        = 64
    edit.undo_memory_limit = 0      # 0 = illimité
    try:
        syst.memory_cache_limit = 8192   # Mo, cache séquenceur/sim
    except Exception:
        pass
    L("Performance : undo 64 pas · cache 8 Go")


# ─── 4. COLOR MANAGEMENT + RENDU (fichier de démarrage) ──────────────────────

def setup_render_defaults():
    sc = bpy.context.scene
    r = sc.render
    r.engine = 'CYCLES'
    r.resolution_x = 3840
    r.resolution_y = 2160
    r.resolution_percentage = 100
    r.fps = 24

    sc.cycles.device = 'GPU'
    sc.cycles.samples = 256
    sc.cycles.use_denoising = True

    sc.view_settings.view_transform = 'Filmic'
    try:
        sc.view_settings.look = 'Medium High Contrast'
    except TypeError:
        pass
    L("Rendu par défaut : Cycles GPU · 4K · 24fps · Filmic Medium High Contrast")


# ─── SAUVEGARDE ───────────────────────────────────────────────────────────────

def main():
    print("\n" + "=" * 56)
    print(" N'Aset OFM · Configuration Blender (headless)")
    print("=" * 56)

    setup_gpu()
    setup_addons()
    setup_performance()
    setup_render_defaults()

    # Persiste préférences + fichier de démarrage
    bpy.ops.wm.save_userpref()
    L("Préférences sauvegardées (userpref.blend)")
    bpy.ops.wm.save_homefile()
    L("Fichier de démarrage sauvegardé (startup.blend)")

    print("\n--- RÉSUMÉ ---")
    for line in log:
        print("  •", line)
    print("=" * 56)
    print(" Terminé. Redémarre Blender pour voir les réglages.")
    print("=" * 56 + "\n")


main()
