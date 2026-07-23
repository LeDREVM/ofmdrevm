# GN — Dust (poussière dorée en suspension)

> Base générée par `create_geometry_nodes.py` : `DREVM_Dust_Field` (cube wire
> 12 m + GN_Dust_Field, 800 instances icosphères `Mat_Gold_Emission`).

## Animation de dérive (à ajouter dans GN_Dust_Field)

```
Distribute Points on Faces
  → Set Position
       Offset = Combine XYZ :
         X : Noise 4D (W = Scene Time × 0.02) × 0.4   — dérive lente
         Y : idem, seed décalé                         × 0.3
         Z : Scene Time × 0.015                        — lévitation +Z
  → Instance on Points → Realize
```

Scene Time (node) remplace les drivers — tout vit dans le node tree.

## Réglages par scène (N'Aset)

| Scène | Densité | Taille | Vitesse Z | Note |
|---|---|---|---|---|
| S1-S2 | ×1.0 | 0.008 | 0.015 | dérive au vent |
| S3 | ×1.0 | 0.008 | **0** | SUSPENDUE — le temps s'arrête |
| S4 | ×1.2 | 0.010 | 0.008 | reprise à peine visible |
| S5 | ×2.0 | 0.012 | 0.04 | l'éveil — montée assumée |

## Règle DREVM
La poussière se DEVINE, elle ne se voit pas : émission `Mat_Gold_Emission` ≤ 2.0,
particules < 1 % de la surface de l'écran. Si on la remarque au premier regard,
diviser la densité par 2.
