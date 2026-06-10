# 𓂀 N'Aset OFM — Référence Technique par Scène

Document de travail quotidien. Une section par scène, tout ce qu'il faut savoir avant d'ouvrir Blender ou UE5.

---

## SCÈNE 1 — L'Apparition
**Frames :** 1 → 240 | **Durée :** 0–10s

### Caméra Blender
| Paramètre | Valeur |
|-----------|--------|
| Nom objet | `Camera_Principale` |
| Focale | 35mm |
| Position | (0, -10, 1.65) |
| Target | `Camera_Target` (0, 0, 1.65) |
| DOF | f/8 — tout net |
| Mouvement | Fixe |

### Lumières
| Lumière | Paramètre | Valeur |
|---------|-----------|--------|
| `Key_Light` | Position | (5, -5, 3) · angle 15° bas |
| `Key_Light` | Énergie | 800W |
| `Key_Light` | Mode | Contre-jour pur |
| `Fill_Light` | Énergie | 0W (éteint S1) |
| `Rim_Light` | Énergie | 200W · `#C9963A` |

### Objets Actifs
- `Naset_Body` — position A-Pose, **de dos**
- `Drape_Shuka` — Cloth Sim actif, vent
- `Bijoux_Or` — émission 0.0
- `Wind_Scene1` — force rampe 0.3 → 0.6 sur frames 1–240
- `Particules_Or_Emitter` — drift passif, émission basse

### Matériaux — Valeurs Frame 1
| Matériau | Paramètre | Valeur |
|----------|-----------|--------|
| `Mat_Or_Emission` | Emissive Strength | 0.0 |
| `Mat_Yeux_Iris` | Emissive Strength | 0.0 |
| `Mat_Peau_Naset` | Subsurface | 0.30 |

### Checklist Avant Rendu S1
- [ ] Silhouette dos visible — visage non-visible
- [ ] Drapé blanc + Shúkà rouge animés par le vent
- [ ] Contre-jour franc — silhouette quasi-noire
- [ ] Particules visibles mais discrètes
- [ ] Aucune émission dorée active

---

## SCÈNE 2 — L'Approche
**Frames :** 241 → 960 | **Durée :** 10–40s

### Caméra Blender
| Paramètre | Valeur |
|-----------|--------|
| Focale | 50mm |
| Position départ | (0, -10, 1.65) · frame 241 |
| Position arrivée | (0, -2, 1.65) · frame 960 |
| Vitesse dolly | 0.011m/frame |
| DOF | f/2.8 · focus `Naset_Body` |
| Mouvement | Dolly in linéaire |

### Lumières
| Lumière | Transition | Valeur |
|---------|-----------|--------|
| `Key_Light` | frame 241→960 | 180°→135° rotation (contre-jour → latéral) |
| `Fill_Light` | entre frames 400–960 | 0W → 80W · côté gauche · chaud |
| `Rim_Light` | constant | 200W · `#C9963A` |

### Événements Clés
| Frame | Événement |
|-------|-----------|
| 241 | Début dolly · focale passe à 50mm |
| 400 | `Fill_Light` s'allume progressivement |
| 500 | `Mat_Or_Emission` Emissive 0.0 → 0.2 (début) |
| 720 | Profil droit visible (≈30s) |
| 960 | Fin dolly · caméra à 2m |

### Checklist Avant Rendu S2
- [ ] Dolly régulier — pas de saccade
- [ ] Lumière passe progressivement de contre-jour à latéral
- [ ] Bijoux commencent à briller légèrement à frame 500
- [ ] Profil droit visible à frame 720 — pas le regard complet
- [ ] Focus suit `Naset_Body` tout le long

---

## SCÈNE 3 — Le Regard
**Frames :** 961 → 1440 | **Durée :** 40–60s

### Caméra Blender
| Paramètre | Valeur |
|-----------|--------|
| Focale | 85mm |
| Position | (0, -1.8, 1.65) — fixe |
| DOF | f/1.8 · focus `Mat_Yeux_Iris` |
| Plongée | 5° |
| Mouvement | **Aucun** |

### Lumières
| Lumière | Paramètre | Valeur |
|---------|-----------|--------|
| `Key_Light` | Position | Frontal doux 30° · 400W · 5500K |
| `Fill_Light` | Énergie | 80W · gauche |
| `Rim_Light` | Énergie | 200W · arrière · `#C9963A` |

### Événements Clés
| Frame | Événement |
|-------|-----------|
| 961 | Vent → 0.0 (silence absolu) |
| 961 | Particules velocity → 0.0 (suspendues) |
| 961 | `Key_Light` passe frontal |
| 961–1440 | Aucune animation — plan figé |

### Matériaux — Valeurs Scène 3
| Matériau | Paramètre | Valeur |
|----------|-----------|--------|
| `Mat_Or_Emission` | Emissive Strength | 0.2 (stable) |
| `Mat_Yeux_Iris` | Emissive Strength | 0.0 |

### Checklist Avant Rendu S3
- [ ] Caméra absolument fixe — aucun micro-mouvement
- [ ] Vent arrêté — drapé immobile
- [ ] Particules suspendues dans l'air
- [ ] Focus précis sur les yeux
- [ ] Lumière frontale douce — pas de shadow dure sur le visage

---

## SCÈNE 4 — La Descente
**Frames :** 1441 → 1920 | **Durée :** 60–80s

### Caméra Blender
| Paramètre | Valeur |
|-----------|--------|
| Focale | 85mm (fixe) |
| Position | (0, -1.8, 1.65) — fixe |
| DOF f/stop | 1.8 → 1.4 progressif |
| Mouvement | Zoom DOF uniquement (pas de mouvement physique) |

### Animation Paupières
| Frame | État |
|-------|------|
| 1441 | Paupières ouvertes |
| 1600 | Fermeture début |
| 1650 | Paupières fermées (50%) |
| 1700 | Paupières fermées (100%) |

*Animation dans l'armature `Naset_Rig` — Shape Keys ou bones `eye_close_L/R`*

### Émissions
| Frame | Matériau | Valeur |
|-------|----------|--------|
| 1600 | `Mat_Yeux_Iris` Emissive | 0.0 → 0.08 |
| 1600 | `Mat_Or_Emission` Emissive | 0.2 → 0.45 |
| 1920 | Les deux | valeurs finales atteintes |

### Particules
| Frame | Comportement |
|-------|-------------|
| 1441–1920 | Micro-oscillation Y ±0.02m (respiration subtile) |

### Checklist Avant Rendu S4
- [ ] Fermeture des yeux fluide — 4.4s (frames 1600–1707)
- [ ] Lueur dorée sous paupières à peine visible
- [ ] Bijoux : montée émission visible mais subtile
- [ ] DOF f-stop s'ouvre progressivement (flou arrière augmente)
- [ ] Particules micro-oscillation visible

---

## SCÈNE 5 — L'Éveil
**Frames :** 1921 → 2280 | **Durée :** 80–95s

### Caméra Blender
| Paramètre | Valeur |
|-----------|--------|
| Focale | 85mm (fixe) |
| Position | (0, -1.8, 1.65) — fixe |
| DOF | f/1.4 |
| Mouvement | **Aucun** |

### Animation Paupières
| Frame | État |
|-------|------|
| 1921 | Paupières fermées |
| 1925 | Paupières ouvertes — 4 frames = mouvement vif |

### Émissions — Chronologie
| Frame | Matériau | Paramètre | Valeur |
|-------|----------|-----------|--------|
| 1921 | `Mat_Yeux_Iris` | Emissive Strength | 0.08 |
| 1960 | `Mat_Yeux_Iris` | Emissive Strength | 1.2 |
| 1921 | `Mat_Or_Emission` | Emissive Strength | 0.45 |
| 1980 | `Mat_Or_Emission` | Emissive Strength | 2.0 |
| 1960 | `Mat_Peau_Naset` | Emission (body aura) | 0.0 → 0.15 |
| 2100 | `Mat_Peau_Naset` | Emission (body aura) | 0.15 (stable) |

### Particules
| Frame | Comportement |
|-------|-------------|
| 1921 | Burst · radius 0 → 3m · 120 frames |
| 2280 | Drift naturel repris |

### Post-Production (AE / PP)
| Étape | Outil | Paramètre |
|-------|-------|-----------|
| Bloom bijoux | After Effects | Glow · Threshold 80 · Radius 25 · Intensity 0.8 |
| Bloom yeux | After Effects | Glow · Threshold 70 · Radius 15 · Intensity 1.2 |
| Cut noir | Premiere Pro | Cut sec frame 2200 — aucun fondu |
| Symbole `𓂀` | After Effects | Noto Sans Egyptian · fade in 2s · 3–4s display |
| Color grade | Premiere Pro | Lumetri · shadows froides · highlights chauds |

### Checklist Avant Rendu S5
- [ ] Ouverture des yeux en 4 frames — mouvement vif et précis
- [ ] Émission yeux atteint 1.2 à frame 1960
- [ ] Burst particules visible — irradiation, pas explosion
- [ ] Aura body subtile — `#C9963A` très transparent
- [ ] Bloom géré en AE — pas sur-exposé dans Blender
- [ ] Cut noir frame 2200 exact

---

## RÉSUMÉ PIPELINE COMPLET

```
Blender (naset_scene_setup.py)
  ├── Setup scène, render, matériaux
  ├── (naset_camera_animation.py)
  │    └── Caméra keyframes · Émissions matériaux
  └── (naset_render_output.py)
       └── Batch render par scène → renders/S1…S5/

UE5 (naset_sequencer_setup.py)
  ├── Level Sequence Naset_CM_Main
  ├── Camera cuts par scène
  └── Niagara VFX timeline

After Effects
  ├── Import EXR séquences
  ├── Bloom / Glow · Lens flare
  ├── Symbole 𓂀 S5
  └── Export PNG/ProRes

Premiere Pro
  ├── Assembly 95s
  ├── Color correction Lumetri
  └── Export H.265 4K
```

---

*𓂀 Référence Scènes v1.0 · Négus Dja · Ordre du Feu Mystique*
