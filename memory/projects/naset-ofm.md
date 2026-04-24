# Projet N'Aset OFM — Fiche Complète

**Codename :** N'Aset OFM  
**Type :** Personnage 3D + Court Métrage Spirituel  
**Statut :** En développement actif  
**Pipeline :** 100% Blender 5 → UE5 → AE → PP

---

## Identité Personnage

| Propriété | Valeur |
|-----------|--------|
| Nom complet | N'Aset OFM |
| Titre | Divine Maasaï |
| Archétype | Prêtresse Égyptienne Futuriste |
| Univers | OFM — Ordre du Feu Mystique |
| Niveau | Divin |
| Âge apparent | 25 – 30 ans |
| Alignement | Lumière souveraine |
| Origine | Égypte antique / Futur |
| Rôle narratif | Gardienne des Savoirs |

## Personnalité

Souveraine · Mystique · Intuitive · Protectrice · Silencieuse · Lumineuse

## Pouvoirs

| Pouvoir | Type | Description |
|---------|------|-------------|
| Magie solaire dorée | Primaire | Attaque / Protection lumineuse |
| Lecture des âmes | Secondaire | Perception des intentions |
| Aura de protection | Passif | Bouclier permanent |
| Invocation Œil Oudjat `𓂀` | Ultime | Pouvoir absolu — décisif |

---

## Caractéristiques Visuelles Complètes

### Corps
- Silhouette : Élancée, athlétique, souveraine
- Taille : 175 – 180 cm
- Corpulence : Fine, athlétique
- Pose référence : A-Pose neutre (Blender) · T-Pose (UE5)
- Unit Scale Blender : 0.01 · Metric

### Peau
| Paramètre | Valeur |
|-----------|--------|
| Base Color | `#6B3D2E` |
| SSS Color | `#8B4E35` |
| Subsurface | 0.25 – 0.35 |
| Subsurface Radius | (1.2, 0.6, 0.3) |
| Roughness | 0.45 – 0.55 (map + noise) |
| Metallic | 0.0 |
| Specular | 0.45 |
| IOR Fresnel | 1.4 |
| Micro-sheen | Multiply 0.03 – 0.05 |

### Visage
| Trait | Description |
|-------|-------------|
| Forme | Ovale, traits fins |
| Yeux | Amande, coin externe relevé |
| Couleur yeux | `#1A0D00` brun très foncé |
| Maquillage | Khôl égyptien noir |
| Lèvres | `#7B2D2D` Bordeaux profond |
| Pommettes | Hautes, prononcées |
| Mâchoire | Fine, allongée |
| Ratio visage | H/L ≈ 1.35 |

### Cheveux
| Option | Description |
|--------|-------------|
| Style A | Afro long et libre |
| Style B | Carré droit égyptien |
| Couleur | `#0D0A08` Noir profond |
| Ornements | Perles dorées + symbole Ankh |
| Shader | Principled Hair BSDF |
| Melanin | 0.9 |
| Roughness | 0.6 |

### Vêtements
| Pièce | Description |
|-------|-------------|
| Drapé principal | Lin égyptien fin blanc/ivoire |
| Bordures | Broderies dorées hiéroglyphiques |
| Shúkà | Drapé rouge/bordeaux Maasaï |
| Shader | Cloth Sim + Translucent |

### Bijoux
| Bijou | Description |
|-------|-------------|
| Collier | Usekh égyptien large |
| Bras droit | Manchette or gravée |
| Bras gauche | Manchette or gravée |
| Symboles | `𓋹` Ankh + `𓂀` Oudjat |
| Matériau | Or + Lapis-lazuli |
| Metallic | 0.95 – 1.0 |
| Roughness | 0.08 – 0.15 |
| Base Color | `#C9963A` |
| Emissive | 0.2 (particules actives) |

---

## Effets Visuels Signature

| Effet | Description | Outil |
|-------|-------------|-------|
| Particules dorées | Sphères flottantes or émissif | Blender Geo Nodes / Niagara |
| Aura sacrée | Lumière cinématique autour corps | Blender Emission / UE5 |
| Émission yeux | Glow doré au moment de l'éveil | Blender Shader keyframe |
| Bloom | Halo sur bijoux et aura | AE Glow / PP Lumetri |

---

## Pipeline Technique Complet

```
Blender 5.0
  └── Modélisation (Multires Sculpt)
  └── UV Unwrap + Textures 4K (PS)
  └── Shader peau (Principled BSDF + SSS)
  └── Groom (Hair Curves)
  └── Cloth Sim (Chaos Cloth)
  └── Rigging (Control Rig)
  └── Animation (24fps)
  └── Lighting (Cycles GPU)
  └── Rendu (4K PNG Seq / EXR)
       │
       ├── UE5 (Temps réel / Jeu)
       │    └── MetaHuman base
       │    └── Import FBX + Groom
       │    └── Blueprints (BP_Naset*)
       │    └── Niagara VFX
       │    └── Sequencer cinématique
       │
       └── After Effects (Compositing)
            └── Import EXR / PNG Seq
            └── Color Grading
            └── Bloom / Glow
            └── Lens Flare
            └── Vignette
                 │
                 └── Premiere Pro (Montage final)
                      └── Assembly 95s
                      └── Color correction
                      └── Export H.265 4K
```

---

## Structure Court Métrage (95 secondes)

| Scène | Frames | Durée | Caméra | Description |
|-------|--------|-------|--------|-------------|
| S1 | 1 → 240 | 0–10s | 35mm fixe | Plan large savane · dos · vent · particules |
| S2 | 241 → 960 | 10–40s | 50mm dolly in | Travelling avant · lumière rasante |
| S3 | 961 → 1440 | 40–60s | 85mm fixe | Regard fixe · silence absolu |
| S4 | 1441 → 1920 | 60–80s | 85mm | Yeux se ferment · slow motion |
| S5 | 1921 → 2280 | 80–95s | 85mm | Éveil · émission 0→0.15 · cut noir |

---

## Nommage Objets Blender (Convention Stricte)

| Objet | Nom exact Blender |
|-------|------------------|
| Armature rig | `Naset_Rig` |
| Mesh corps | `Naset_Body` |
| Mesh drapé | `Drape_Shuka` |
| Mesh bijoux | `Bijoux_Or` |
| Caméra | `Camera_Principale` |
| Point de visée | `Camera_Target` |
| Key Light | `Key_Light` |
| Fill Light | `Fill_Light` |
| Rim Light | `Rim_Light` |
| Vent S1 | `Wind_Scene1` |
| Particules | `Particules_Or_Emitter` |
| Matériau peau | `Mat_Peau_Naset` |
| Matériau iris | `Mat_Yeux_Iris` |
| Matériau or | `Mat_Or_Emission` |

---

## Références Visuelles

Assassin's Creed Origins · Black Panther · Agatha All Along · Visions of Mana · Eternals (Phastos)

---

## Lore Complet

> "N'Aset est une entité hors du temps, née dans la lumière du Soleil de Rê. Prêtresse de l'ordre OFM — Ordre du Feu Mystique — elle traverse les âges pour protéger les savoirs sacrés de l'Égypte antique, dissimulés dans les temples oubliés du futur."

**Mission :** Protéger les tablettes sacrées  
**Ennemi :** Les Sébau — voleurs d'âmes  
**Alliés :** Les Gardiens Maasaï  
**Lieu :** Temple du Futur Doré

---

*𓂀 N'Aset OFM v1.0 · Ordre du Feu Mystique · Négus Dja*
