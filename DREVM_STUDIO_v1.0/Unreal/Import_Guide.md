# Unreal — Import Guide (Blender → UE5)

Pipeline d'import des assets DREVM vers UE5. Deux voies selon l'asset.

## Voie 1 — send2ue (personnages riggés) ★ recommandée
Addon : `tools/BlenderTools/send2ue/` (cf dashboard Pipeline & Outils).

1. Blender : sélectionner `Naset_Body` + `Naset_Rig`
2. Paramètres (script généré par le dashboard) :
   - Mesh folder : `/Game/Characters/NasetOFM/Meshes`
   - Skeleton : `/Game/Characters/NasetOFM/SK_NasetOFM_Skeleton`
   - `import_materials_and_textures = True` ⚠ (PAS `import_textures` — n'existe pas)
3. Pipeline > Export > Send to Unreal

## Voie 2 — FBX manuel (props, temple, végétation)

| Réglage export Blender | Valeur |
|---|---|
| Scale | 1.0 · Apply Transform ✓ |
| Forward / Up | -Y Forward · Z Up |
| Armature | Only Deform Bones ✓ · Add Leaf Bones ✗ |
| Bake Animation | par action, Simplify 0.05 |

Import UE5 : Skeletal Mesh ✓ (si riggé) · Import Textures ✓ ·
Material Import Method : Create New Materials.

## Conventions UE5 (cf CLAUDE.md)

| Type | Préfixe | Exemple |
|---|---|---|
| Skeletal Mesh | `SK_` | `SK_NasetOFM` |
| Static Mesh | `SM_` | `SM_Temple_Pillar_A` |
| Material | `M_` / `MI_` | `M_Gold_Sacred`, `MI_Gold_Emissive` |
| Texture | `T_[nom]_[suffixe]` | `T_NasetSkin_BC` (BaseColor), `_N`, `_ORM` |
| Blueprint | `BP_Naset[Fonction]` | `BP_NasetAura` |

## Textures 4K
Exporter de Blender en PNG 16 bit : `NAset_[Map]_4K.png` → renommer côté UE
`T_NAset_[Map]`. ORM packé (Occlusion/Roughness/Metallic dans RGB) via
TexTools bake ou Photoshop channels.

## Vérif post-import (obligatoire avant d'annoncer « importé »)
1. Échelle : N'Aset = 177 cm dans le viewport UE (mannequin de référence à côté)
2. Matériaux : palette conforme (`#C9963A` or, `#6B3D2E` peau) sous éclairage neutre
3. Skeleton : hiérarchie pelvis→spine→chest→neck→head intacte, poids sans spikes
