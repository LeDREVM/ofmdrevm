# 𓂀 Référence Technique — La Mémoire de la Terre Rouge

Document de travail scène par scène · 45s · 1080 frames @ 24fps
**FORMAT FINAL : 9:16 vertical (2160×3840)** — réseaux sociaux

---

## SCÈNE 1 — Le Sol Parle (frames 1–168 · 0–7s)

| Paramètre | Valeur |
|-----------|--------|
| Caméra | `Cam_S1_SolMacro` · 100mm · f/2.8 |
| Position caméra | (0, -0.55, 0.10) — 10cm du sol, 55cm en retrait |
| Angle | 80° (quasi horizontal, voit le sol) |
| Focus | 0.55m (`dof.focus_distance`) |
| Lumière principale | `Key_Soleil_Gwadloup` SUN · contre-jour bas |
| Matériau sol | `Mat_TerreRouge` · roughness 0.88 · grain fin scale 150 (coords Object) |
| Particules | `Particules_PoussiereRouge` · burst à chaque pas |
| Voix off | *"Tè-la ka palé…"* |
| Tambour Gwo Ka | 1 battement / 2s · très bas |

**Checklist :**
- [ ] Pieds nus visibles — aucun visage
- [ ] Terre rouge `#8B3A1A` — réaliste, grain visible
- [ ] Poussière se soulève et retombe lentement
- [ ] Lumière rasante — ombres longues sur le sol
- [ ] Aucune émission or active

> ⚠️ **S1 n'est pas validable avec le placeholder.** Le cylindre `Naset_Body` (r=0.30 m)
> occupe tout le champ de la macro 100mm à 0.55 m et masque le sol. Ce plan ne peut être
> jugé qu'une fois le vrai mesh (avec jambes et pieds) importé.

---

## SCÈNE 2 — Apparition de N'Aset (frames 169–336 · 7–14s)

| Paramètre | Valeur |
|-----------|--------|
| Caméra | `Cam_S2_Apparition` · 50mm · f/2.8 |
| Hauteur caméra | 1.65m (hauteur yeux) |
| Plan | Mi-corps · plongée 8° |
| Focus | 3.0m (`dof.focus_distance`) — sur `Naset_Body` |
| Lumière principale | `Key_Soleil_Gwadloup` côté gauche 45° |
| Rim | `Rim_Or_Naset` · 300W · `#C9963A` |
| Vent | `Wind_Scene1` force 0.4 · drapé animé — **À CRÉER À LA MAIN** (hors script) |
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
| Caméra | `Cam_S3_Memoire` · 35mm · f/8 · focus 8.0m |
| Plan | Large — N'Aset petite au centre |
| Silhouettes | `Mat_Ancetre_Base` (+ 1 copie par ancêtre) · Alpha 0.25 · Emission 0.5 |
| Nb silhouettes | 6 instances (`Ancetre_01`…`Ancetre_06`) |
| Animation | Fade in Mix Fac 0→0.6, échelonné +8 frames/ancêtre : 344→388 (01) … 384→428 (06) |
| Disparition | Frame **721** pour toutes — cut net, sans décalage |
| Radius | Demi-cercle rayon ~4m, derrière N'Aset (Y+) |
| Voix off | *"Sé memwa… sé san… sé vwa ki pa janmen disparèt…"* |

**Checklist :**
- [ ] Silhouettes translucides — lumière pure, pas personnages réalistes
- [ ] N'Aset au centre, couleurs saturées (contraste avec silhouettes pâles)
- [ ] Ciel `World_Gwadloup` visible — aucune bande sombre entre le sol et l'horizon
- [ ] Apparition non-simultanée des silhouettes (décalage par instance)

---

## SCÈNE 4 — Le Regard (frames 529–720 · 22–30s)

| Paramètre | Valeur |
|-----------|--------|
| Caméra | `Cam_S4_Regard` · 135mm · f/1.4 · focus 0.8m |
| Plan | Gros plan yeux — bokeh maximal |
| Focus | 0.8m — à réajuster sur `Mat_Yeux_Iris` après import du vrai mesh |
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
| Caméra | `Cam_S5_Force` · 50mm · f/4.0 · focus 4.0m |
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
| `Mat_TerreRouge` | `memoire_terre_rouge_setup.py` | S1, S2, S3, S5 |
| `Mat_Ancetre_Base` (+ copies) | `memoire_terre_rouge_setup.py` | S3, S4 |
| `Mat_PoussiereRouge` | `memoire_terre_rouge_setup.py` | S1 |
| `Mat_Or_Emission` | `memoire_terre_rouge_setup.py` | S2, S3, S4, S5 |
| `Mat_Peau_Naset` | placeholder ici, vraie version dans `naset_scene_setup.py` | S2, S3, S4, S5 |
| `Mat_Yeux_Iris` | `naset_scene_setup.py` **uniquement** | S4 |

> Sans `naset_scene_setup.py`, l'animation des yeux S4 est **sautée** (message `[SKIP]` en console)
> — le reste de la scène se monte quand même.

## OBJETS REQUIS

| Objet | Source | Scènes |
|-------|--------|--------|
| `World_Gwadloup` | Script (Sky `MULTIPLE_SCATTERING`) | toutes |
| `Sol_TerreRouge` | Script · plan 2000m | S1, S2, S3, S5 |
| `Naset_Body` | FBX import / placeholder cylindre si absent | S2, S3, S4, S5 |
| `Naset_Rig` | Import | S2, S3, S4, S5 |
| `Ancetre_01…06` | Script (cylindres translucides) | S3, S4 |
| `Particules_PoussiereRouge` | Script | S1 |
| `Cam_S1_SolMacro` | Script | S1 |
| `Cam_S2_Apparition` | Script | S2 |
| `Cam_S3_Memoire` | Script | S3 |
| `Cam_S4_Regard` | Script | S4 |
| `Cam_S5_Force` | Script | S5 |

## ORDRE D'EXÉCUTION

```
1. memoire_terre_rouge_setup.py   → Ciel, sol, ancêtres, caméras, lumières, particules,
                                    marqueurs timeline + animations S3/S4/S5  (TOUT-EN-UN)
2. Importer Naset_Body (FBX)      → remplace le placeholder cylindre
3. naset_scene_setup.py           → Matériaux Naset (peau, or, Mat_Yeux_Iris)
4. Relancer memoire_terre_rouge_setup.py → animate_yeux_s4() s'exécute cette fois
5. Créer Wind_Scene1 (force 0.4)  → drapé S2 (manuel)
6. Danseuses Gwo Ka S5            → vidéo réelle (composite AE) ou 3D
7. Render scène par scène         → naset_render_output.py (adapter RENDER_SCENES)
8. Compositing After Effects      → Bloom, grain, symbole 𓂀, titre S6
9. Montage Premiere Pro           → Assembly 45s, Gwo Ka audio
```

**Lancement headless (vérification rapide, sans ouvrir Blender) :**

```bash
"/c/Program Files/Blender Foundation/Blender 5.0/blender.exe" --background --factory-startup --python scripts/blender/memoire_terre_rouge_setup.py
```

---

## SOUS-TITRES — CHARTE & TIMING

**Fichier timé prêt à importer :** `scenario/Memoire_Terre_Rouge_sous_titres.srt`
(Premiere Pro : Fenêtre → Texte → Légendes → Importer le fichier de légendes → SRT)

### Style visuel

| Élément | Valeur |
|---------|--------|
| Police | Montserrat (1er choix) / Poppins / Bebas Neue |
| Créole | MAJUSCULES · blanc `#FFFFFF` · léger contour noir |
| Traduction FR | En dessous, plus petit (~60% de la taille), même style |
| Mots clés | **Or `#C9963A`** (palette officielle) |
| Espacement | Tracking large (cinéma) |
| Animation | Fade in + léger zoom (scale ~103% → 100%) — subtil, jamais excessif |
| Position | Tiers inférieur, centré (au-dessus de la zone UI TikTok/Reels) |

### Mots clés en OR par réplique

| Cue | Réplique | Mot(s) en or |
|-----|----------|--------------|
| 1 | TÈ-LA KA **PALÉ** | PALÉ |
| 3 | SÉ PA JIS **LATÈ** | LATÈ |
| 4 | SÉ **MEMWA** | MEMWA |
| 5 | SÉ **SAN** | SAN |
| 6 | SÉ **VWA** KI PA JANMEN DISPARÈT | VWA |
| 9 | NOU **TOUJOU LA** | TOUJOU LA |
| 10 | NOU SÉ **RASIN** | RASIN |
| 11 | NOU SÉ **FLANM** | FLANM |
| 12 | MÉMOIRE VIVANTE — **GWADLOUP** | GWADLOUP (titre entier déjà or) |

> Le SRT ne transporte pas la couleur : les mots or se stylisent dans Premiere
> (Essential Graphics) ou After Effects après import.

### Sync audio

- Chaque phrase = 1 respiration · **0.5 s de silence** entre phrases fortes (déjà dans le SRT)
- Accents voix (appuyer à l'enregistrement) : **« TÈ-LA KA PALÉ »** · **« NOU TOUJOU LA »** · **« NOU SÉ FLANM »**
- Cue 9 « NOU TOUJOU LA » : démarre à 0:26,0 = frame 625, le coup de tambour (déjà calé dans le SRT)
- Cue 11 « NOU SÉ FLANM » : démarre à 0:33,0 = frame 793, le pic d'émission or (déjà calé dans le SRT)

---

*𓂀 Référence Mémoire Terre Rouge v1.0 · Négus Dja · Gwadloup*
