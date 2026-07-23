# 𓂀 DREVM STUDIO v1.0 — Boîte à outils Blender

Toolkit de production pour les projets **DREVM** : N'Aset OFM (court métrage)
et Le Voyage de Luna (série 8 épisodes). Tout est généré par script — zéro
étape manuelle pour poser une scène de travail.

## Prérequis
- **Blender 5.0+** (testé sur 5.0.1) — les scripts utilisent l'API 5.0
  (layered actions, sky MULTIPLE_SCATTERING, inputs Principled renommés)
- GPU NVIDIA (OPTIX) recommandé — fallback CPU automatique

## Démarrage rapide

```bash
# Construire une scène complète en local, sans ouvrir l'interface :
blender --background --python Python/build_scene.py -- --project luna
blender --background --python Python/build_scene.py -- --project naset --render test
```

Ou dans Blender : Text Editor → ouvrir `Python/build_scene.py` → Alt+P.

## Scripts (Python/)

| Script | Rôle |
|---|---|
| `create_project.py` | Collections, unités, fps, structure de fichier |
| `create_camera_rig.py` | Rig caméra (dolly + grue + focus target) |
| `create_material_library.py` | 5 matériaux studio : Gold, Moon, Skin, Fabric, Stone |
| `create_geometry_nodes.py` | Node groups : Moon_System, Dust_Field |
| `create_world_shader.py` | 3 mondes : Sunset (N'Aset), Night (Luna), Studio |
| `create_render_settings.py` | Presets Cycles GPU : preview / prod 4K |
| `build_scene.py` | **Orchestrateur** — enchaîne tout + save .blend |

## Recettes manuelles (markdown)
- `GeometryNodes/` — systèmes complexes à monter dans l'éditeur (doc pas-à-pas)
- `Materials/` — réglages détaillés des shaders (valeurs exactes)
- `Compositor/` — grade cinéma final

## Conventions
- Palette officielle : or `#C9963A` · nuit `#1C1A3A` · argent lune `#E8E8F0`
  · peau `#6B3D2E` · ivoire `#FAFAF0` · shúkà `#C0392B`
- Nommage : `Naset_*` / `Luna_*` / `DREVM_*` — cf `Project_Structure.md`
- Render : Cycles GPU · 4K · 24 fps · Filmic Medium High Contrast

*𓂀 DREVM Studio · Négus Dja · Guadeloupe*
