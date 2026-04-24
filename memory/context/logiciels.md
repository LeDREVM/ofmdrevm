# Contexte Logiciels — Paramètres & Conventions

## BLENDER 5.0

### Paramètres Projet
```
Unités         : Metric
Unit Scale     : 0.01
Échelle cible  : 1.75 m
FPS            : 24
Résolution     : 3840 × 2160 (4K UHD)
Moteur         : Cycles (GPU obligatoire pour final)
```

### Render Settings Cycles
```
Samples           : 512 – 1024 (preview 64)
Light Bounces     : 4 – 6
Denoiser          : OptiX (NVIDIA) ou OpenImageDenoise
Color Management  : Filmic · Medium High Contrast
Output Format     : PNG (séquence) ou EXR 32bit
Motion Blur       : Activé · Shutter 0.25
```

### Shader Peau — Principled BSDF
```
Base Color        : Albedo 4K (#6B3D2E)
Subsurface        : 0.25 – 0.35
Subsurface Radius : (1.2, 0.6, 0.3)
Subsurface Color  : #8B4E35
Specular          : 0.45
Roughness         : Map + Noise (0.35 – 0.55)
Normal            : Normal Map → Normal input
AO                : Multiply sur Base Color (facteur ≤ 0.5)
Fresnel           : IOR 1.4 → Multiply 0.03–0.05 → Add
```

### Shader Bijoux Or
```
Metallic   : 0.95 – 1.0
Roughness  : 0.08 – 0.15
Base Color : #C9963A
Emissive   : 0.2 (strength)
```

### Shader Cheveux — Principled Hair BSDF
```
Melanin       : 0.9
Roughness     : 0.6
Random Color  : 0.03
Root Radius   : 0.025
Tip Radius    : 0.01
Clump         : 0.6
Noise         : 0.15
```

### Cloth Simulation — Shúkà
```
Quality Steps  : 8 – 10
Bending        : 0.2
Tension        : 5 – 10
Subdivision    : 2 – 3
Bake requis    : Oui — avant tout rendu
```

### Caméras
```
Close-up (S3/S4/S5) : 85mm · f/2.8 · Focus iris
Plan poitrine (S2)  : 50mm · f/2.8
Plan large (S1)     : 35mm · f/4.0
Micro-shake         : amplitude 0.001m (S1 seulement)
```

### Lighting Setup
```
Key Light  : Area · 4800K · 45° haut gauche · 800W
Fill Light : Area · 30% key · bleu pâle · doux
Rim Light  : Area · 5500K · derrière droite · plus chaud
World HDRI : Golden Hour · Intensité 0.3 – 0.5
Eye Light  : Petite area face · clarté yeux
```

### Noms d'objets obligatoires (scripts Python)
```
Naset_Rig           : Armature principale
Naset_Body          : Mesh corps
Drape_Shuka         : Mesh drapé (Cloth Sim)
Bijoux_Or           : Mesh bijoux
Camera_Principale   : Caméra unique
Camera_Target       : Empty point de visée
Key_Light           : Area light principale
Fill_Light          : Area light fill
Rim_Light           : Area light rim
Wind_Scene1         : Force Field vent S1
Particules_Or_Emitter : Émetteur particules
Mat_Peau_Naset      : Matériau peau
Mat_Yeux_Iris       : Matériau iris
Mat_Or_Emission     : Matériau or émissif (#C9963A)
Emission_Divin      : Nœud émission dans Mat_Yeux_Iris
```

---

## UNREAL ENGINE 5

### Paramètres Projet
```
Version     : UE5.x (dernière LTS)
Base perso  : MetaHuman Creator
Éclairage   : Lumen GI activé
Géométrie   : Nanite activé
Rendu       : Path Tracing pour cinématiques
FPS         : 24 (Sequencer)
```

### Blueprints N'Aset
```
BP_NasetCharacter   : Classe principale personnage
BP_AuraEffect       : Système aura lumineuse
BP_OudjaActivation  : Pouvoir ultime Œil Oudjat
BP_ParticleGold     : Niagara particules dorées
```

### Import depuis Blender
```
Format       : FBX (.fbx) pour mesh + rig
Cheveux      : Groom Asset (.abc Alembic ou direct)
Textures     : PNG 4K (Albedo, Normal, Roughness, AO)
Cloth baked  : Alembic (.abc) séquence
Scale        : Vérifier 100x (Blender 0.01 → UE5 cm)
```

### Niagara — Particules Dorées
```
Émetteur    : Sprite ou Mesh sphère
Couleur     : #C9963A
Emissive    : Strength 0.2
Count       : 80 – 150
Lifetime    : 5 – 7 sec
Vitesse     : Ascendante · très lente (0.005 m/s)
Gravité     : Légèrement négative (-0.08)
```

### Matériaux UE5 — Paramètres PBR
```
Peau :
  Base Color   : #6B3D2E
  Subsurface   : Activé · Profile peau brune
  Roughness    : 0.45 – 0.55
  Normal       : Normal Map 4K

Or bijoux :
  Metallic     : 0.97
  Roughness    : 0.10
  Base Color   : #C9963A
  Emissive     : 0.2 · #E8BC6A
```

---

## ADOBE AFTER EFFECTS

### Import Rendu Blender
```
Format préféré : EXR 32bit (couleurs HDR préservées)
Alternatif     : PNG séquence 16bit
Interprétation : 24fps · Conserver espace colorimétrique
```

### Effets Clés Compositing N'Aset
```
Glow          : Seuil 60% · Radius 15 · Or sur bijoux
Bloom         : CC Light Rays ou Optical Flares (or)
Lens Flare    : Knoll ou natif AE · subtil · #C9963A
Color Grading : Curves · teinte chaude highlights
LUT           : LUT cinéma chaud (Golden Hour)
Vignette      : Ellipse mask · opacité 15 – 20%
Grain         : Très léger (1 – 2%) pour texture film
```

### Structure Composition
```
Comp_S1_PlanLarge     : 0–10s   · frames 1–240
Comp_S2_Travelling    : 10–40s  · frames 241–960
Comp_S3_Regard        : 40–60s  · frames 961–1440
Comp_S4_Fermeture     : 60–80s  · frames 1441–1920
Comp_S5_Eveil         : 80–95s  · frames 1921–2280
Comp_MASTER           : Assembly toutes scènes
```

### Paramètres Export AE → PP
```
Format      : ProRes 4444 ou DNxHD 4K
Couleur     : Rec.709 ou DCI-P3
Bits        : 16bit minimum
FPS         : 24
```

---

## ADOBE PHOTOSHOP

### Textures 4K — N'Aset
```
Résolution     : 4096 × 4096 px · 72dpi (usage 3D)
Format export  : PNG 16bit (Normal, Roughness, AO)
               : JPEG 90% (Albedo · taille réduite)
Espace couleur : sRGB pour Albedo · Linear pour Maps
```

### Convention Fichiers Texture
```
NAset_Albedo_4K.png      : Couleur peau de base
NAset_Normal_4K.png      : Normales (bleu dominant)
NAset_Roughness_4K.png   : Rugosité (niveaux de gris)
NAset_AO_4K.png          : Occlusion ambiante
NAset_Skin_Detail.png    : Micro-pores, pores
NAset_Makeup_Kohl.png    : Masque khôl sur UV visage
NAset_Drape_Albedo.png   : Couleur drapé
NAset_Drape_Normal.png   : Weave tissu normal
NAset_Or_Metalness.png   : Masque métal bijoux
```

### Calques de référence à conserver
```
REF_Palette_OFM      : Charte couleurs du projet
REF_UV_Layout        : Disposition UVs pour peinture
REF_Symmetry_Guide   : Guides d'asymétrie (0.5–1%)
FINAL_Albedo         : Calque final aplati à exporter
```

---

## ADOBE PREMIERE PRO

### Séquence Principale
```
Nom         : NasetOFM_CM_v01
Preset      : UHD 4K · 24fps · Rec.709
Résolution  : 3840 × 2160
Audio       : 48000 Hz · 32bit
```

### Structure Bins (Dossiers)
```
01_RENDERS/
  ├── S1_Plan_Large/
  ├── S2_Travelling/
  ├── S3_Regard/
  ├── S4_Fermeture/
  └── S5_Eveil/
02_VFX_AE/          (comps finales AE)
03_AUDIO/           (musique + ambiances)
04_EXPORTS/         (versions finales)
```

### Paramètres Montage N'Aset
```
Rythme      : Contemplatif · coupes lentes
Transitions : Cut sec OU dissolve 8 frames max
Audio       : Musique sacrée · pas de dialogue
Étalonnage  : Teinte chaude dorée · Lumetri
Cut final   : Noir franc sur dernière frame
```

### Export Final
```
Format       : H.265 / HEVC
Profil       : Main 10
Résolution   : 3840 × 2160 (4K UHD)
Débit        : 50 – 80 Mbps (haute qualité)
Audio        : AAC 320kbps
Cible        : Instagram · TikTok · YouTube
```

### Versions Export Réseaux
```
Instagram   : 1080×1080 · 60fps · H.264 · 30s max
TikTok      : 1080×1920 (9:16) · 60fps · H.264
YouTube     : 3840×2160 (4K) · 24fps · H.265
Archive     : ProRes 4444 · 4K · Master
```

---

*→ Retour au hot cache : CLAUDE.md*  
*→ Projet complet : memory/projects/naset-ofm.md*
