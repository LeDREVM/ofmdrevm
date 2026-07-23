# GN — Jewelry (bijoux N'Aset : Usekh, manchettes, perles)

## Collier Usekh `GN_Usekh_Collar`

```
Curve Circle (Radius 0.14, arc 210° via Trim Curve 0.21–0.79)
  → dupliquer en 5 rangées : Curve Offset radial +0.018/rangée
  → Resample Curve (Count 42/rangée)
  → Instance on Points : perle (icosphere 0.006)
  → Set Material par rangée (index) :
       rangée 1,3,5 : Mat_Gold_Sacred
       rangée 2 : perles rouges #C0392B · rangée 4 : bleu nuit #1C1A3A
```

Positionnement : parent bone `neck` · léger Shrinkwrap sur Naset_Body
(offset 0.004) pour épouser les clavicules.

## Manchettes égyptiennes `GN_Arm_Cuff`
- Cylindre Ø 0.07 × h 0.09, épaisseur Solidify 0.003
- Gravures : bandes Voronoi 1D → bump strength 0.15
- Matériau `Mat_Gold_Sacred` · parent bones `forearm.L` / `forearm.R`

## Perles de tresses (box braids)
```
Naset_Hair_Curves → GN :
  Resample Curve → Endpoint Selection (fin de tresse)
  + Curve Parameter > 0.85 → 2e sélection (perle intermédiaire)
  → Instance on Points : perle rouge Ø 0.008 + or Ø 0.006
```
Référence visuelle : perles rouges de l'image Divine Maasaï.

## S5 — l'éveil des bijoux
Tous les matériaux or des bijoux partagent le même node group
`Gold_Emission_Ctrl` (Value node exposé). UNE seule valeur keyframée
anime TOUS les bijoux : 0.0 (S1-S2) → 0.2 (S3) → 0.45 (S4) → 2.0 (S5).
Jamais de flare : l'or rayonne, il n'explose pas.
