# Unreal — Lumen (éclairage DREVM temps réel)

Reproduire les deux ambiances signature en GI temps réel.

## Réglages projet (une fois)
Project Settings > Rendering :
- Global Illumination : **Lumen** · Reflections : **Lumen**
- Software Ray Tracing (défaut) — passer Hardware RT si GPU RTX et scène temple
  (réflexions or plus propres sur les bijoux)
- Post Process Volume (Infinite Extent ✓) : Lumen Scene Detail 2.0 ·
  Final Gather Quality 2.0 (cinématique, pas gameplay)

## Ambiance N'Aset — couchant doré
| Acteur | Réglage |
|---|---|
| Directional Light | Intensity 6 lux · couleur `#E8BC6A` · angle 4° au-dessus de l'horizon · Source Angle 1.5 (ombres douces) |
| SkyLight | Real Time Capture ✓ |
| Sky Atmosphere | Mie Scattering ×3 (brume dorée) · Rayleigh baissé 20 % |
| Exponential Height Fog | Density 0.02 · couleur `#C9963A` à 10 % · Volumetric ✓ |

Le contre-jour S1 : caméra face au soleil, personnage entre les deux.
Lumen gère le bounce doré du sol sur les drapés — c'est LE gain vs Blender.

## Ambiance Luna — nuit argentée
| Acteur | Réglage |
|---|---|
| Directional Light (lune) | 0.5 lux · `#E8E8F0` · Source Angle 0.8 |
| Sky Atmosphere | nuit : multipliers au plancher, ciel `#1C1A3A` |
| Luna (perso) | matériau émissif 0.15-0.8 → **Emissive Light Source ✓** — Lumen fait de Luna une vraie source : elle éclaire l'herbe en marchant (E02 !) |
| Lueurs d'or déposées | émissif `#C9963A` strength 2 — chaque don illumine son rocher |

## Pièges
- Émissif < 0.05 : invisible pour le Final Gather — rester ≥ 0.1
- Translucent (drapés) : pas de GI reçue par défaut → Volumetric / Per-Vertex
  lighting mode sur le matériau
- Ombres du couchant qui « rampent » : Shadow Bias 0.3 → 0.5 sur la
  Directional, jamais désactiver Contact Shadows (0.02)
- `r.Lumen.ScreenProbeGather.RadianceCache 1` si scintillement dans la savane
