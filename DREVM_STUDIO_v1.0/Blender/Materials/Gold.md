# Matériau — Gold (Or sacré `#C9963A`)

> Générés par `create_material_library.py` : `Mat_Gold_Sacred` + `Mat_Gold_Emission`.

## Valeurs de base (Principled BSDF — noms Blender 5.0)

| Input | Valeur | Note |
|---|---|---|
| Base Color | `#C9963A` (linéaire) | JAMAIS un jaune saturé générique |
| Metallic | 0.95 | 1.0 = trop parfait, l'or ancien vit |
| Roughness | 0.10 (poli) · 0.25 (patiné) | varier selon l'usure du bijou |
| Coat Weight | 0.0 | pas de vernis — métal brut |

## Martelage
Noise (Scale 30, Detail 6) → Bump Strength 0.08. Pour les grandes surfaces
(pectoral Usekh) monter Scale à 60 pour resserrer le grain.

## Variante émissive `Mat_Gold_Emission`
- Emission Color `#C9963A` · Strength **keyframable** 0 → 2.0 (S5)
- Piloter TOUS les bijoux par un seul Value node partagé (cf GN/Jewelry.md)

## Anti-patterns (veto DA)
- ❌ Roughness < 0.05 : effet chrome doré « bling render »
- ❌ Emission > 2.5 : l'or devient néon — l'éveil est souverain, pas criard
- ❌ Teinte décalée vers `#FFD700` (or web) : hors palette DREVM
