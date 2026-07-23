# GN — Temple Generator (Temple du Futur Doré · N'Aset)

Générateur procédural du cercle de pierres / colonnade du temple.
À monter dans l'éditeur GN (pas encore scripté — trop de direction artistique).

## Node tree `GN_Temple_Circle`

```
Curve Circle (Radius 6m, Resolution 12)
  → Resample Curve (Count = nombre de colonnes, ex. 9)
  → Instance on Points
       Instance : collection « Temple_Pillars » (variantes de colonnes)
       Pick Instance ✓ · Instance Index : Random Value (seed exposé)
  → Rotate Instances (Z : aligner vers le centre = Align Euler to Vector)
  → Random Value → Scale Instances (0.92–1.08, seed exposé)
  → Realize Instances
```

## Inputs exposés (Group Input)
| Socket | Type | Défaut | Rôle |
|---|---|---|---|
| Radius | Float | 6.0 | Rayon du cercle sacré |
| Columns | Integer | 9 | Nombre de piliers (impair = axe central libre) |
| Seed | Integer | 42 | Variation reproducible |
| Ruin Factor | Float 0-1 | 0.15 | % de piliers penchés/brisés (Random > Rotate X) |

## Colonnes sources (collection Temple_Pillars)
- `Pillar_A` : cylindre 0.4×5 m + chapiteau lotus (2 cônes) — intact
- `Pillar_B` : idem, sommet biseauté (Boolean) — érodé
- `Pillar_C` : tronqué à 60 % — ruine
- Matériau : `Mat_Stone_Temple` + gravures : bump Voronoi bandes verticales

## Hiéroglyphes émissifs (l'éveil S5)
Sur `Pillar_A/B` : texture image alpha des glyphes `𓋹 𓂀 𓅃 𓆣` → mix
`Mat_Stone_Temple` / émission or `#C9963A` strength 0 → keyframe à 2.0 sur S5.
L'attribut GN `pillar_index` permet d'allumer les piliers un par un
(cf. E05 Luna : les pierres s'illuminent au passage).
