# 𓂀 N'Aset OFM — MetaHuman Reference (UE 5.7)

Pont entre les matériaux Blender (référence) et le MetaHuman créé dans l'éditeur UE5.
Projet : `C:\Users\ardja\Documents\DOCDREVM\NasetOFM\UE5\NasetOFM\NasetOFM.uproject`

---

## Décision pipeline

- **Corps / peau / cheveux / rig** → MetaHuman (créé in-editor UE 5.7, plugin MetaHumanCharacter)
- **Props** (bijoux Usekh, Ankh, tablettes) → Blender → export FBX vers UE5
- **Matériaux Blender** → référence colorimétrique uniquement (ne pas réimporter la peau)
- **Animation / rendu final** → UE5 (Sequencer + Movie Render Queue), voir `naset_sequencer_setup.py`

---

## Étapes : Mesh-to-MetaHuman depuis le scan existant

> N'Aset n'est PAS sculptée de zéro. Le visage vient de ton scan Meshy déjà préparé :
> `exports/Naset_Head_for_MetaHuman.fbx` (tête isolée, 29710 verts, échelle réelle).
> Corps de référence : `Naset_Body` dans `N_Aset_OFM_Character.blend`.

1. UE5 : importer `Naset_Head_for_MetaHuman.fbx` dans le Content Browser
2. Sélectionner le mesh → **MetaHuman → Mesh to MetaHuman** (Identity Solve)
3. Track Markers → Solve → **MetaHuman Identity** : UE reconstruit le visage de N'Aset
4. **MetaHuman Backend / cloud Epic** : génère le rig + textures depuis l'identité
5. Onglet **Body** : Height ~1.78m, build élancé/athlétique (Slender + Athletic)
6. Onglet **Skin** : caler le ton sur `#6B3D2E` (voir tableau Skin)
7. Onglet **Hair / Grooms** : Afro long OU carré droit égyptien, couleur ci-dessous
8. **Assemble** → génère le Blueprint `BP_Naset` jouable (utilisé par le Sequencer)

---

## SKIN — Mapping palette → MetaHuman

| Réglage MetaHuman | Valeur cible | Source Blender |
|-------------------|--------------|----------------|
| **Base Skin Tone** | `#6B3D2E` marron doré | `Mat_Peau_Naset` Base Color |
| **Melanin / Tone slider** | Medium-Deep (warm) | — |
| **Subsurface / SSS** | teinte chaude, scatter rouge dominant | Subsurface Radius (1.2, 0.6, 0.3) |
| **Roughness** | 0.45–0.55 | Noise→ColorRamp peau |
| **Undertone** | Warm / Golden | `#8B4E35` SSS chaud |

> ⚠️ MetaHuman gère le SSS automatiquement (shader peau dédié). Tu n'as PAS à recréer
> le node Subsurface — tu ajustes juste le **ton** et l'**undertone** pour matcher `#6B3D2E`.

---

## YEUX

| Réglage | Valeur | Source |
|---------|--------|--------|
| Iris color | `#1A0D00` brun très sombre | `Mat_Yeux_Iris` |
| Forme | Amande | CLAUDE.md |
| Khôl / eyeliner | `#1C1A3A` accent sombre | maquillage MetaHuman ou texture |
| Émission divine (éveil S5) | `#C79A3C` — ajoutée en UE5 via material override + Niagara | keyframe Blender |

> L'émission dorée des yeux (S5) n'est PAS native MetaHuman → se fait en UE5 :
> material instance avec Emissive animé dans le Sequencer (frames 1921→2280).

---

## CHEVEUX (Grooms)

| Réglage | Valeur | Source |
|---------|--------|--------|
| Couleur de base | `#0D0A08` noir profond | `Mat_Cheveux_Naset` |
| Melanin | 0.9 (très foncé) | Principled Hair |
| Roughness | 0.6 | — |
| Style | Afro long OU carré droit égyptien | CLAUDE.md |

---

## LÈVRES / MAQUILLAGE

| Réglage | Valeur |
|---------|--------|
| Lèvres | `#7B2D2D` bordeaux profond |
| Khôl égyptien | `#1C1A3A` |

---

## PROPS À FAIRE DANS BLENDER (export FBX → UE5)

| Prop | Matériau Blender | Note |
|------|------------------|------|
| Usekh (grand collier pectoral) | `Mat_Or_Emission` | hard-surface, pas MetaHuman |
| Bijoux / bracelets | `Mat_Or_Emission` | |
| Ankh `𓋹` | `Mat_Or_Emission` | porte/portail |
| Tablettes sacrées | à créer | mission du personnage |
| Drapé Shùkà + lin | `Mat_Shuka` / `Mat_Lin` | OU cloth UE5 (Chaos) |

> Or sacré `#C9963A` · Métallique 0.97 · Emissive keyframé = signature visuelle.
> Les props gardent EXACTEMENT mes valeurs Blender (ce sont elles la source de vérité).

---

## CHAÎNE DE PRODUCTION RÉVISÉE

```
1. UE5 : créer MH_Naset (MetaHuman Character)  ← corps/peau/cheveux/rig
2. Blender : modéliser les props (Usekh, Ankh, tablettes) avec Mat_Or_Emission
3. Blender : export FBX des props → UE5
4. UE5 : attacher les props au squelette MetaHuman (sockets)
5. UE5 : naset_sequencer_setup.py → Level Sequence + caméras + Niagara
6. UE5 : material instance émission yeux/or animée (S4/S5)
7. UE5 : Movie Render Queue 4K EXR
8. After Effects : compositing (bloom, titre, symbole)
9. Premiere Pro : montage final
```

---

*𓂀 MetaHuman Reference · Négus Dja · UE 5.7 · N'Aset OFM*
