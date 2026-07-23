# Compositor — Cinema Nodes (grade final DREVM)

Chaîne compositor pour les rendus N'Aset et Luna. À monter dans le
Compositing workspace (Use Nodes ✓).

## Chaîne complète

```
Render Layers
  → Color Balance (Lift/Gamma/Gain — voir tables)
  → Glare (Fog Glow · Threshold 1.2 · Size 7) — halo doux hautes lumières
  → Lens Distortion (Dispersion 0.004) — aberration chromatique subtile
  → Vignette : Ellipse Mask (0.85×0.65, Blur 0.35) → Multiply 0.92
  → Film Grain : Noise Texture (Scale 800) → Overlay 0.02
  → Composite
```

## Grade N'Aset (couchant doré)

| Étage | Valeur | Effet |
|---|---|---|
| Lift (ombres) | +0.01 vers `#1C1A3A` | ombres indigo, jamais noires |
| Gamma (mids) | +0.02 vers `#C9963A` | l'or dans les demi-tons |
| Gain (hautes) | 1.03 vers `#E8BC6A` | couchant chaud |

## Grade Luna (nuit argentée)

| Étage | Valeur | Effet |
|---|---|---|
| Lift | +0.015 vers `#1C1A3A` | la nuit indigo signature |
| Gamma | neutre | |
| Gain | 1.02 vers `#E8E8F0` | clair de lune froid |
| Glare Threshold | 0.9 | Luna et les lueurs d'or accrochent le halo |

## Règles
- Le look Filmic Medium High Contrast est DÉJÀ dans le render — le compositor
  affine, il ne re-grade pas. Si tu pousses le Color Balance > ±0.05, le
  problème est dans l'éclairage, pas dans la compo.
- Grain 0.02 max — texture de peau du film, pas un filtre Instagram.
- Export : PNG 16 bit (préviz) · EXR MultiLayer (étalonnage Premiere/Resolve).
- Cut noir : géré au montage, JAMAIS en compo (fade node interdit).
