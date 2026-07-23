# Matériau — Skin (Peau N'Aset `#6B3D2E`)

> Généré par `create_material_library.py` : `Mat_Skin_DREVM`.

## Valeurs de base (noms d'inputs Blender 5.0 !)

| Input | Valeur | Note |
|---|---|---|
| Base Color | `#6B3D2E` | marron doré canonique |
| **Subsurface Weight** | 0.3 | ⚠ plus de float `Subsurface` unique en 5.0 |
| **Subsurface Scale** | 0.05 | |
| Subsurface Radius | (0.36, 0.20, 0.12) | rouge dominant = chaleur sous la peau |
| Roughness | 0.45–0.55 | zone canonique DREVM |
| Specular IOR Level | 0.4 | ⚠ ex-`Specular` renommé en 5.0 |

## SSS — la teinte `#8B4E35`
Blender 5 n'a plus de `Subsurface Color` : c'est la Base Color qui irrigue le
SSS. Pour retrouver la chaleur `#8B4E35` : ColorRamp Noise (Scale 20) mixant
`#6B3D2E` → `#8B4E35` à 25 % dans Base Color — les zones chaudes (joues,
oreilles, doigts) vivent d'elles-mêmes avec le Radius rouge.

## Détail
- Pores : Noise Scale 150 → Bump 0.03 (scripté)
- Prod 4K : remplacer par les maps `NAset_Albedo_4K.png` + `NAset_Normal_4K.png`
  (slots prévus : brancher Image Texture sur Base Color / Normal Map)

## Éclairage de contrôle
Valider la peau UNIQUEMENT sous `World_Sunset_Naset` ET `World_Studio`.
Le SSS qui flatte au couchant peut virer cireux en lumière neutre.
