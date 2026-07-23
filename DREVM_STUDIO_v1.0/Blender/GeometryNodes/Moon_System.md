# GN — Moon System (Le Voyage de Luna)

> Base générée par `create_geometry_nodes.py` (`Luna_Moon` + `Moon_Phase_Ctrl` +
> `Moon_Sun`). Ce doc couvre le pilotage des phases et les upgrades manuels.

## Principe
La lune est une sphère à matériau `Mat_Moon_Silver`. Un empty `Moon_Phase_Ctrl`
porte un Sun (`Moon_Sun`) : **tourner l'empty en Z change le côté éclairé** =
la phase. Aucun shader de phase à tricher — c'est de la vraie lumière, les
terminateurs sont physiquement corrects.

## Phases par épisode (rotation Z du ctrl)

| Épisode | Phase | Angle Z |
|---|---|---|
| E01 New Moon | Nouvelle lune | 180° |
| E02 Crescent | Croissant | 225° |
| E03 First Quarter | Premier quartier | 270° |
| E04 Gibbous | Gibbeuse | 315° |
| E05 Full Moon | Pleine lune | 0° (360°) |
| E06 Waning Gibbous | Gibbeuse décr. | 45° |
| E07 Last Quarter | Dernier quartier | 90° |
| E08 New Beginning | Nouvelle lune | 135° → 180° |

En script : `keyframe_phase(episode, frame_start, frame_end)` (create_geometry_nodes.py).

## Upgrades manuels (éditeur GN)
1. **Cratères displacés** : GN sur Luna_Moon → `Set Position` + Voronoi
   (Scale 8, offset le long des normales × 0.02). Plus riche que le bump seul.
2. **Halo atmosphérique** : sphère englobante ×1.15, matériau Principled
   Transmission 1.0 + Volume Scatter density 0.02, couleur `#E8E8F0`.
3. **Libration subtile** : noise sur la rotation X du ctrl (±0.5°) via driver
   `0.008 * sin(frame/97)` — la lune « respire ».

## Règle DREVM
Émission de la lune ≤ 0.5. Si le halo « bave » dans le ciel → baisser la
density du volume, jamais monter le bloom en compo.
