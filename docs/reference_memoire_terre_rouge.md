# 𓂀 Référence Technique — La Mémoire de la Terre Rouge

Document de travail scène par scène · 45s · 1080 frames @ 24fps

---

## SCÈNE 1 — Le Sol Parle (frames 1–168 · 0–7s)

| Paramètre | Valeur |
|-----------|--------|
| Caméra | `Cam_S1_SolMacro` · 100mm · f/2.8 |
| Hauteur caméra | 10cm du sol |
| Angle | 80° (quasi horizontal, voit le sol) |
| Focus | Pieds / sol à 0.30m |
| Lumière principale | `Key_Soleil_Gwadloup` SUN · contre-jour bas |
| Matériau sol | `Mat_TerreRouge` · roughness 0.88 |
| Particules | `Particules_PoussièreRouge` · burst à chaque pas |
| Voix off | *"Tè-la ka palé…"* |
| Tambour Gwo Ka | 1 battement / 2s · très bas |

**Checklist :**
- [ ] Pieds nus visibles — aucun visage
- [ ] Terre rouge `#8B3A1A` — réaliste, grain visible
- [ ] Poussière se soulève et retombe lentement
- [ ] Lumière rasante — ombres longues sur le sol
- [ ] Aucune émission or active

---

## SCÈNE 2 — Apparition de N'Aset (frames 169–336 · 7–14s)

| Paramètre | Valeur |
|-----------|--------|
| Caméra | `Cam_S2_Apparition` · 50mm · f/2.8 |
| Hauteur caméra | 1.65m (hauteur yeux) |
| Plan | Mi-corps · plongée 8° |
| Focus | `Naset_Body` |
| Lumière principale | `Key_Soleil_Gwadloup` côté gauche 45° |
| Rim | `Rim_Or_Naset` · 300W · `#C9963A` |
| Vent | `Wind_Scene1` force 0.4 · drapé animé |
| Émission bijoux | `Mat_Or_Emission` Strength 0.15 |
| Voix off | *"Anba pyé nou… sé pa jis latè…"* |

**Checklist :**
- [ ] N'Aset de face, regard horizon (pas objectif)
- [ ] Drapé rouge + ivoire animé par vent
- [ ] Or des bijoux capte la lumière soleil
- [ ] Aucune silhouette ancestrale visible encore

---

## SCÈNE 3 — Mémoire des Ancêtres (frames 337–528 · 14–22s)

| Paramètre | Valeur |
|-----------|--------|
| Caméra | `Cam_S3_Memoire` · 35mm · f/8 |
| Plan | Large — N'Aset petite au centre |
| Silhouettes | `Mat_SilhouetteAncetre` · Alpha 0.25 · Emission 0.4 |
| Nb silhouettes | 7 instances (Ancetre_01…07) |
| Animation | Fade in frames 380–420 · oscillation verticale ±0.03m |
| Radius | Scatter dans 8m autour de N'Aset |
| Voix off | *"Sé memwa… sé san… sé vwa ki pa janmen disparèt…"* |

**Checklist :**
- [ ] Silhouettes translucides — lumière pure, pas personnages réalistes
- [ ] N'Aset au centre, couleurs saturées (contraste avec silhouettes pâles)
- [ ] Savane guadeloupéenne en arrière-plan
- [ ] Apparition non-simultanée des silhouettes (décalage par instance)

---

## SCÈNE 4 — Le Regard (frames 529–720 · 22–30s)

| Paramètre | Valeur |
|-----------|--------|
| Caméra | `Cam_S4_Regard` · 135mm · f/1.4 |
| Plan | Gros plan yeux — bokeh maximal |
| Focus | `Mat_Yeux_Iris` — yeux précis |
| Émission yeux | Strength 0.0 → 0.30 · frames 529–625 |
| Silhouettes | Toujours présentes · Fac 0.6 |
| Silence Gwo Ka | Entre chaque ligne de voix off |
| Voix off | *"Nou pa pèdi… nou té la… nou toujou la…"* (espacées) |
| Tambour | Reprend fort à frame 625 sur "nou toujou la" |

**Checklist :**
- [ ] Seuls les yeux sont nets — tout le reste en bokeh
- [ ] Lueur dorée dans l'iris visible dès frame 580
- [ ] Immobilité totale — aucun micro-mouvement caméra
- [ ] Le silence entre les lignes est aussi puissant que la voix

---

## SCÈNE 5 — La Force Vivante (frames 721–912 · 30–38s)

| Paramètre | Valeur |
|-----------|--------|
| Caméra | `Cam_S5_Force` · 50mm · f/4.0 |
| Plan | Mi-large — N'Aset + danseuses Gwo Ka |
| Option A | Vidéo réelle danseuses · composite AE |
| Option B | 3D · personnages Naset_Danseuse_01…06 |
| N'Aset | Immobile au centre · Cut à frame 793 |
| Émission or | `Mat_Or_Emission` Strength 0.15 → 1.20 · frames 793–840 |
| Gwo Ka | Plein tempo · drums + voix |
| Cut frame 793 | Son → tambour seul grave |
| Voix off | *"Nou sé rasin… nou sé flanm…"* |

**Checklist :**
- [ ] Énergie maximale sur les danseuses (mouvement, couleurs)
- [ ] Cut brutal vers N'Aset — contraste silence/mouvement
- [ ] Or de N'Aset monte fort après le cut → "nous sommes flamme"
- [ ] Silhouettes disparaissent à frame 721

---

## SCÈNE 6 — Le Titre (frames 913–1080 · 38–45s)

| Paramètre | Outil | Valeur |
|-----------|-------|--------|
| Fondu noir | Premiere Pro | 12 frames (0.5s) depuis frame 913 |
| Fond | — | Noir pur `#000000` |
| Symbole `𓂀` | After Effects | Noto Sans Egyptian · 120pt · `#C9963A` · Glow doux |
| Titre | After Effects | "N'ASET OFM" · Cormorant Garamond Bold · tracking +150 |
| Sous-titre | After Effects | "Mémoire Vivante — Gwadloup" · light · tracking +300 |
| Fade in titre | After Effects | 1.5s dissolve depuis frame 936 |
| Son | — | Silence 2s → 1 coup tambour grave → silence |
| Hold | — | 3.5s avant fade out final |

**Checklist :**
- [ ] Fondu noir propre — aucun résidu de lumière
- [ ] Symbole centré — pas de titre avant frame 936
- [ ] "Gwadloup" orthographe créole (pas "Guadeloupe")
- [ ] Dernier coup de tambour synchronisé avec l'apparition du symbole

---

## MATÉRIAUX REQUIS

| Matériau | Fichier | Scènes |
|----------|---------|--------|
| `Mat_TerreRouge` | `naset_memoire_terre_rouge.py` | S1, S2, S3, S5 |
| `Mat_SilhouetteAncetre` | `naset_memoire_terre_rouge.py` | S3, S4 |
| `Mat_PoussièreRouge` | `naset_memoire_terre_rouge.py` | S1 |
| `Mat_Peau_Naset` | `naset_scene_setup.py` | S2, S3, S4, S5 |
| `Mat_Or_Emission` | `naset_scene_setup.py` | S2, S3, S4, S5 |
| `Mat_Yeux_Iris` | `naset_scene_setup.py` | S4 |

## OBJETS REQUIS

| Objet | Source | Scènes |
|-------|--------|--------|
| `Sol_TerreRouge` | Script | S1, S2, S3, S5 |
| `Naset_Body` | FBX import / existant | S2, S3, S4, S5 |
| `Naset_Rig` | Import | S2, S3, S4, S5 |
| `Ancetre_01…07` | À créer (mesh basique) | S3, S4 |
| `Particules_PoussièreRouge` | Script | S1 |
| `Cam_S1_SolMacro` | Script | S1 |
| `Cam_S2_Apparition` | Script | S2 |
| `Cam_S3_Memoire` | Script | S3 |
| `Cam_S4_Regard` | Script | S4 |
| `Cam_S5_Force` | Script | S5 |

## ORDRE D'EXÉCUTION

```
1. naset_memoire_terre_rouge.py   → Sol, lumières, caméras, particules
2. naset_scene_setup.py           → Matériaux Naset (peau, or, yeux)
3. Importer Naset_Body (FBX)      → Placer dans la scène
4. Créer Ancetre_01…07            → Meshes humains basiques + Mat_SilhouetteAncetre
5. animate_silhouettes_emission() → Keyframes transparence S3
6. naset_camera_animation.py      → Adapter aux frames 1080
7. Render scène par scène         → naset_render_output.py (adapter RENDER_SCENES)
8. Compositing After Effects      → Bloom, titre, symbole
9. Montage Premiere Pro           → Assembly 45s, Gwo Ka audio
```

---

*𓂀 Référence Mémoire Terre Rouge v1.0 · Négus Dja · Gwadloup*
