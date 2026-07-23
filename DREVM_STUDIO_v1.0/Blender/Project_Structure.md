# Structure de projet DREVM Studio

## Collections Blender (créées par create_project.py)

```
Scene Collection
├── 00_CAMERAS        — rig caméra + focus targets
├── 10_CHARACTERS     — personnages (Naset_*, Luna_*)
├── 20_ENVIRONMENT    — sol, ciel, végétation, architecture
├── 30_FX             — particules, poussière, émissions
├── 40_LIGHTS         — lumières additionnelles (le soleil vit dans le World)
└── 90_HELPERS        — empties, targets, guides (exclus du rendu)
```

## Nommage

| Type | Convention | Exemple |
|---|---|---|
| Blend | `[Projet]_[Sujet]_v[N].blend` | `Luna_E01_v1.blend` |
| Objet perso | `[Projet]_[Partie]` | `Naset_Body`, `Luna_Body` |
| Caméra | `Cam_[Scène/Épisode]` | `Cam_S1`, `Cam_E01` |
| Matériau | `Mat_[Nom]` | `Mat_Gold_Sacred` |
| Node group | `GN_[Système]` | `GN_Moon_System` |
| World | `World_[Ambiance]` | `World_Night_Luna` |
| Render | `[Projet]_S[scène]_F[frame]` | `Naset_S1_F0240` |

## Cibles par projet

| | N'Aset OFM | Le Voyage de Luna |
|---|---|---|
| Format | 4K 16:9 · 24 fps | 4K 16:9 · 24 fps |
| Durée | 95 s (5 scènes) | 8 × 20-25 s |
| Ambiance | Couchant doré | Nuit indigo étoilée |
| World | `World_Sunset_Naset` | `World_Night_Luna` |
| Look | Filmic Medium High Contrast | Filmic Medium High Contrast |
