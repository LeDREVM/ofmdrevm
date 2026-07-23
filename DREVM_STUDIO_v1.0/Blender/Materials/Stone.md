# Matériau — Stone (Pierre du temple `#8A7B63`)

> Généré par `create_material_library.py` : `Mat_Stone_Temple`.

## Valeurs de base

| Input | Valeur |
|---|---|
| Base Color | `#8A7B63` (grès chaud) |
| Roughness | 0.95 |

## Structure (scriptée)
Noise Scale 3 (blocs) + Noise Scale 80 (grain) mixés 40 % → Bump 0.35.

## Upgrades prod
1. **Stratification** : Wave Texture (Bands X, Scale 6, Distortion 4) mixée
   15 % dans Base Color — les strates du grès.
2. **Érosion des arêtes** : Bevel node (0.02, 8 samples) → dot Normal →
   ColorRamp → éclaircir les arêtes usées (+ Roughness 1.0 dessus).
3. **Gravures hiéroglyphes** : image alpha `𓋹 𓂀 𓅃 𓆣` → Bump -0.4 (creusé)
   + slot émission or pour l'éveil (cf GeometryNodes/Temple_Generator.md).
4. **Vieillissement bas** : Gradient Z (0-0.5 m) → assombrir 20 % + poussière
   `#B08A50` — la pierre boit le sol.

## Ambiance
La pierre du Temple du Futur Doré n'est pas grise : elle a bu 3000 ans de
couchants. Toujours vérifier sous `World_Sunset_Naset` que les hautes lumières
tirent vers l'or `#C9963A`, jamais vers le blanc.
