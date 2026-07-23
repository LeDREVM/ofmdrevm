# 𓂀 DREVM Materials Library v1

27 matériaux Cycles en fichiers `.shader` (Python bpy autonomes, API Blender 5.0).
Chaque fichier crée son matériau avec `use_fake_user` → il survit dans le .blend
même sans objet assigné.

## Charger

**Tout charger** (headless ou GUI) :
```bash
blender --background monfichier.blend --python Materials/_loader.py
```

**Une catégorie** :
```bash
blender --background monfichier.blend --python Materials/_loader.py -- --category Metals
```

**Un seul matériau** (GUI) : ouvrir le `.shader` dans le Text Editor → Alt+P.

## Catalogue

| Catégorie | Matériau | Nom Blender | Type |
|---|---|---|---|
| Characters | Skin_Dark | `Mat_Skin_Dark` | Surface SSS |
| | Eyes_Glow | `Mat_Eyes_Glow` | Surface + émission pilotable |
| | Hair | `Mat_Hair_DREVM` | Principled Hair BSDF |
| | Fabric_Maasai | `Mat_Fabric_Maasai` | Tartan shúkà procédural |
| Metals | Gold_24K | `Mat_Gold_24K` | Or sacré `#C9963A` |
| | Bronze | `Mat_Bronze` | + patine vert-de-gris |
| | Copper | `Mat_Copper` | |
| | Silver | `Mat_Silver` | |
| Nature | Sand | `Mat_Sand` | Sable savane |
| | Rock | `Mat_Rock` | Grès chaud |
| | Basalt | `Mat_Basalt` | Colonnes voronoi |
| | Moss | `Mat_Moss` | |
| | Leaves | `Mat_Leaves` | Translucide contre-jour |
| | Bark | `Mat_Bark` | Écorce acacia |
| Space | Moon | `Mat_Space_Moon` | Régolithe + earthshine |
| | Earth | `Mat_Space_Earth` | Continents procéduraux |
| | Nebula | `Mat_Space_Nebula` | **VOLUME** (cube domaine) |
| | Stars | `Mat_Space_Stars` | Fond étoilé (sphère inversée) |
| | Atmosphere | `Mat_Space_Atmosphere` | Rim fresnel (sphère ×1.03) |
| FX | Energy | `Mat_FX_Energy` | Émission fresnel animée |
| | Fire | `Mat_FX_Fire` | **VOLUME** feu |
| | Fog | `Mat_FX_Fog` | **VOLUME** brume |
| | Smoke | `Mat_FX_Smoke` | **VOLUME** fumée |
| | Dust | `Mat_FX_Dust` | Particule d'or émissive |
| Water | Ocean | `Mat_Water_Ocean` | Transmission + absorption |
| | River | `Mat_Water_River` | |
| | Ice | `Mat_Water_Ice` | |

## Conventions
- Palette DREVM prioritaire : or `#C9963A` · nuit `#1C1A3A` · argent `#E8E8F0`
- Les matériaux **VOLUME** s'assignent à un mesh fermé (cube/sphère domaine)
- Émissions pilotables : chercher le node `Value` nommé `*_Ctrl` dans le
  node tree — une seule valeur à keyframer
- Inputs Blender 5.0 : `Subsurface Weight`, `Transmission Weight`,
  `Specular IOR Level`, `Coat Weight` (anciens noms = KeyError)
