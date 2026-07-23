# Matériau — Fabric (Drapés : ivoire `#FAFAF0` · shúkà `#C0392B`)

> Générés par `create_material_library.py` : `Mat_Fabric_Ivory` + `Mat_Fabric_Shuka`.

## Ivoire sacré (drapé)

| Input | Valeur |
|---|---|
| Base Color | `#FAFAF0` |
| Roughness | 0.6 |
| Sheen Weight | 0.3 |

Upgrade tissage : Wave Texture (Bands, Scale 250, Distortion 1.2) → Bump 0.02.
Deux passes croisées (2e Wave pivotée 90° via Mapping) = toile.

## Shúkà Maasaï (rouge)

| Input | Valeur |
|---|---|
| Base Color | `#C0392B` |
| Roughness | 0.55 |
| Sheen Weight | 0.3 |

Motif tartan authentique : 2 × Brick Texture (couleurs `#C0392B` / `#8E2A20`,
bandes fines `#1C1A3A`) mixées en damier — Scale ~12 sur l'UV du drapé.

## Translucidité au contre-jour (S1 !)
Le soleil rasant DOIT traverser les drapés :
- Transmission Weight 0.15 (ivoire) · 0.08 (shúkà)
- C'est CE détail qui vend le contre-jour de l'Apparition — vérifier en
  rendu S1 avant tout autre lookdev.

## Cloth (rappel physique)
Quality 10 · tension 15 · compression 15 · bending 0.5 · vertex group `Pin`
(rangée haute). Bake AVANT le rendu : Physics > Cache > Bake frames 1-240.
