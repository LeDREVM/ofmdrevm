"""
naset_ue_import_setup.py
Setup initial du projet UE5 NasetOFM via Python (PythonScriptPlugin).
- Crée l'arborescence /Game/NasetOFM/...
- Importe le scan Naset_Head_for_MetaHuman.fbx (pour Mesh-to-MetaHuman)

Usage : dans l'éditeur UE5 → Window > Python console (ou Tools > Execute Python Script)
        puis colle/charge ce fichier. Adapte FBX_PATH si besoin.
"""

import unreal
import os

# ─── CHEMINS ──────────────────────────────────────────────────────────────────

FBX_PATH = r"C:\Users\ardja\Documents\CODING\Blendaah\ofmdrevm\.claude\worktrees\awesome-bose-7c4dc5\exports\Naset_Head_for_MetaHuman.fbx"

DEST_SOURCE = "/Game/NasetOFM/Source"   # où atterrit le scan importé

FOLDERS = [
    "/Game/NasetOFM",
    "/Game/NasetOFM/Source",        # scans bruts (tête FBX)
    "/Game/NasetOFM/Characters",    # MH_Naset, BP_Naset
    "/Game/NasetOFM/Cameras",
    "/Game/NasetOFM/Cinematics",    # Level Sequences
    "/Game/NasetOFM/VFX",           # Niagara (NS_ParticulesOr, etc.)
    "/Game/NasetOFM/Props",         # Usekh, Ankh, tablettes (FBX depuis Blender)
    "/Game/NasetOFM/Renders",
]


# ─── ARBORESCENCE ─────────────────────────────────────────────────────────────

def create_folders():
    for path in FOLDERS:
        if not unreal.EditorAssetLibrary.does_directory_exist(path):
            unreal.EditorAssetLibrary.make_directory(path)
            unreal.log(f"[DIR] créé : {path}")
        else:
            unreal.log(f"[DIR] existe déjà : {path}")


# ─── IMPORT FBX (scan tête) ───────────────────────────────────────────────────

def import_head_scan():
    if not os.path.isfile(FBX_PATH):
        unreal.log_error(f"[IMPORT] FBX introuvable : {FBX_PATH}")
        return None

    # Options FBX : static mesh (le scan n'a pas de squelette)
    options = unreal.FbxImportUI()
    options.import_mesh      = True
    options.import_as_skeletal = False        # scan = Static Mesh
    options.import_materials  = True
    options.import_textures   = True
    options.import_animations = False
    options.static_mesh_import_data.combine_meshes = True
    options.static_mesh_import_data.generate_lightmap_u_vs = True

    task = unreal.AssetImportTask()
    task.filename          = FBX_PATH
    task.destination_path  = DEST_SOURCE
    task.destination_name  = "SM_Naset_Head"
    task.replace_existing  = True
    task.automated         = True             # pas de popup
    task.save              = True
    task.options           = options

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])

    if task.imported_object_paths:
        for p in task.imported_object_paths:
            unreal.log(f"[IMPORT] importé : {p}")
        return task.imported_object_paths[0]
    else:
        unreal.log_error("[IMPORT] échec — aucun objet importé")
        return None


# ─── ÉTAPES SUIVANTES (GUI — non scriptables) ─────────────────────────────────

def print_next_steps(imported_path):
    unreal.log("\n──── MESH-TO-METAHUMAN (étapes GUI — à faire à la souris) ────")
    unreal.log(f"1. Content Browser → {DEST_SOURCE}/SM_Naset_Head")
    unreal.log("2. Clic droit sur SM_Naset_Head → Scripted Asset Actions / MetaHuman → 'Mesh to MetaHuman'")
    unreal.log("   (ou sélectionner le mesh puis menu MetaHuman → Mesh to MetaHuman Identity)")
    unreal.log("3. Dans l'éditeur MetaHuman Identity : Track Active Frame → Identity Solve")
    unreal.log("4. 'MetaHuman Backend' → Mesh to MetaHuman (génération cloud Epic, login requis)")
    unreal.log("5. Récupérer MH_Naset via Quixel Bridge → déplacer dans /Game/NasetOFM/Characters")
    unreal.log("6. Régler la peau sur #6B3D2E (voir docs/metahuman_naset_reference.md)")
    unreal.log("7. Assemble → BP_Naset → utilisé par naset_sequencer_setup.py")
    unreal.log("──────────────────────────────────────────────────────────────\n")


# ─── POINT D'ENTRÉE ───────────────────────────────────────────────────────────

def main():
    unreal.log("\n━━━ N'Aset OFM · UE5 Import & Setup ━━━")
    create_folders()
    imported = import_head_scan()
    print_next_steps(imported)
    unreal.log("━━━ Terminé ━━━")


main()
