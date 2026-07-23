# GN — Vegetation (savane sacrée)

## Herbes sèches `GN_Savanna_Grass`

```
Group Input (Geometry = sol)
  → Distribute Points on Faces (Density 60/m², Seed exposé)
  → Instance on Points
       Instance : collection « Grass_Clumps » (3 touffes de brins courbés)
  → Rotate Instances (Z random 0-360°)
  → Random Value (0.7–1.3) → Scale Instances
  → Realize Instances
```

- Touffe source : 5-9 brins = courbes bevel 0.004, pointe effilée (radius 0)
- Matériau : dégradé racine `#6B4A24` → pointe `#C9963A` (ColorRamp sur
  Spline Parameter) — la savane porte l'or sacré dans ses pointes
- **Poids de proximité** : Geometry Proximity au personnage → Density ×0.3
  dans un rayon d'1 m (elle ne piétine pas les herbes, elles s'écartent)

## Acacias `GN_Acacia`
Version simple scriptée dans `naset_environment.py` (cônes silhouettes).
Version GN :

```
Curve Line (tronc) → Curve to Mesh (profil circle 0.3, taper 0.4)
  + Cone aplati (rayon 4.5, hauteur 1.4) → parasol
  + Distribute Points sur le parasol → instances feuilles (plane 4×4 cm)
```

Ne JAMAIS détailler les acacias : ils vivent à l'horizon, en silhouette
contre-jour. 200 tris max chacun.

## Vent (les deux systèmes)
Modifier Simple Deform (Bend 4°) piloté par driver :
`0.07 * sin(frame/18 + hash(id))` — déphasage par instance via l'attribut
random du GN. Le champ de vent physique (Force Field Wind 0.4) reste réservé
aux drapés cloth.
