# Matériau — Moon (Lune argentée `#E8E8F0`)

> Généré par `create_material_library.py` : `Mat_Moon_Silver`.

## Valeurs de base

| Input | Valeur | Note |
|---|---|---|
| Base Color | `#E8E8F0` | argent froid, jamais blanc pur `#FFFFFF` |
| Roughness | 0.85 | régolithe mat |
| Emission Color | `#E8E8F0` | |
| Emission Strength | 0.4 | lueur douce — la VRAIE lumière vient de Moon_Sun |

## Cratères
- Base scriptée : Voronoi Distance (Scale 8) → Bump 0.25
- Upgrade : ajouter un 2e Voronoi Scale 25 mixé 40 % (petits impacts)
- Prod héro (gros plan E05) : displacement réel via GN (cf Moon_System.md)

## Le secret du rendu lune
La phase vient de `Moon_Sun` (lumière physique), PAS du shader. Ne jamais
peindre d'ombre dans le matériau — le terminateur doit bouger avec le
Moon_Phase_Ctrl. L'émission 0.4 sert uniquement à garder la face sombre
à peine lisible (earthshine).

## Luna (le personnage)
La peau lumineuse de Luna réutilise cette base : Roughness 0.5,
Subsurface Weight 0.6, Emission Strength 0.15 → 0.8 selon l'épisode
(E01 naissance 0.15 · E05 plénitude 0.8 · E08 extinction 0.1).
