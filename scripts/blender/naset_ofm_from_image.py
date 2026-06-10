"""
naset_ofm_from_image_pipeline.py
Pipeline MetaHuman Creator UE5.7 — N'Aset OFM
Basé sur analyse visuelle de la photo référence : N_Aset_OFM___Divine_Maasaï.jpeg

Analyse de l'image :
  - Peau : brun profond, teinte chocolat chaud, luminosité naturelle
  - Visage : ovale allongé, traits fins et définis, pommettes hautes
  - Yeux : en amande, regard intense vers le bas, légèrement bridés
  - Nez : droit, base légèrement élargie, nez est afro-égyptien
  - Lèvres : fines à moyennes, fermées, expression neutre souveraine
  - Cheveux : tresses fines (box braids) noires avec perles rouges
  - Collier : Usekh maasaï multicolore (rouge, orange, jaune, blanc, noir)
  - Manchette : bracelet doré sur le bras gauche
  - Vêtement : drapé bordeaux/bordeaux foncé (côté gauche), pull navy (côté droit)
  - Silhouette : très élancée, grande, souveraine
  - Expression : neutre, regard baissé, posture souveraine

Auteur   : Négus Dja / OFM Studio
Version  : 2.0 — Image Reference Build
Engine   : Unreal Engine 5.7+
"""

import unreal

# ═══════════════════════════════════════════════════════
#  CONFIG — CHEMINS PROJET
# ═══════════════════════════════════════════════════════
ASSET_PATH  = "/Game/Characters/Naset"
ASSET_NAME  = "MH_NasetOFM_v2"
FULL_PATH   = f"{ASSET_PATH}/{ASSET_NAME}"
OUT_DIR     = "/Game/Characters/Naset/Assembled/"

# ═══════════════════════════════════════════════════════
#  ANALYSE IMAGE → VALEURS SKIN (Linear RGB)
#  Source : photo référence Divine Maasaï
#
#  Méthode de conversion :
#    sRGB hex → Linear = (hex/255)^2.2
#    #3D1F15 → R=0.22 G=0.10 B=0.06  (ombre)
#    #5C3020 → R=0.34 G=0.16 B=0.09  (base peau)
#    #7A4030 → R=0.47 G=0.22 B=0.15  (lumière directe)
#    #9A5535 → R=0.60 G=0.30 B=0.18  (reflet chaud)
# ═══════════════════════════════════════════════════════
SKIN_PROPS = {
    # Couleur de base — brun chocolat chaud extrait de l'image
    "skin_diffuse_color":       unreal.LinearColor(0.34, 0.16, 0.09, 1.0),

    # Subsurface — teinte plus chaude sous la peau, reflet rougeâtre
    "skin_subsurface_color":    unreal.LinearColor(0.55, 0.22, 0.12, 1.0),

    # Peau naturelle légèrement luisante (pas mate)
    "skin_roughness":           0.48,
    "skin_specular":            0.40,

    # SSS fort — peau foncée a un SSS profond et chaud
    "skin_sss_strength":        0.80,
    "skin_sss_radius":          1.30,

    # Pores subtils — peau fine et lisse visible sur la photo
    "skin_pore_roughness_blend": 0.45,

    # Yeux — brun très foncé presque noir, visible sur l'image
    "eye_iris_color":           unreal.LinearColor(0.06, 0.03, 0.01, 1.0),
    "eye_iris_uv_scale":        1.08,
    "eye_sclera_brightness":    0.90,
    # Légère teinte chaude du blanc de l'œil
    "eye_sclera_color":         unreal.LinearColor(0.92, 0.89, 0.84, 1.0),

    # Maquillage khôl égyptien — visible autour des yeux sur la photo
    "makeup_eyeliner_opacity":  0.85,
    "makeup_eyeliner_color":    unreal.LinearColor(0.01, 0.01, 0.02, 1.0),

    # Lèvres — couleur naturelle légèrement rosée foncée
    "lip_color":                unreal.LinearColor(0.28, 0.09, 0.07, 1.0),
    "lip_opacity":              0.70,

    # Dents — blanc naturel, pas trop blanc
    "teeth_color":              unreal.LinearColor(0.88, 0.85, 0.78, 1.0),
}

# ═══════════════════════════════════════════════════════
#  MORPHOLOGIE VISAGE — extraite de la photo
#
#  Observations précises :
#    - Visage ovale très allongé, crâne haut
#    - Pommettes hautes et saillantes
#    - Mâchoire fine, définition nette
#    - Yeux en amande, légèrement inclinés vers le bas latéralement
#    - Nez droit, narines légèrement évasées
#    - Lèvres fines, bouche de taille moyenne
#    - Cou long et élancé
#    - Front légèrement bombé, large
# ═══════════════════════════════════════════════════════
FACE_CONTROLS = {
    # Forme générale
    "face_shape_oval":          0.78,   # très ovale allongé
    "face_length":              0.72,   # visage long

    # Pommettes — hautes et marquées (trait distinctif image)
    "cheekbone_width":          0.58,
    "cheekbone_height":         0.75,   # très hautes
    "cheekbone_prominence":     0.62,

    # Mâchoire fine
    "jaw_width":                0.38,   # mâchoire étroite
    "jaw_definition":           0.65,
    "jaw_angle":                0.45,

    # Menton
    "chin_projection":          0.42,
    "chin_width":               0.40,
    "chin_height":              0.45,

    # Front — large, légèrement bombé
    "forehead_width":           0.62,
    "forehead_height":          0.58,

    # Nez — droit avec base afro-égyptienne
    "nose_bridge_height":       0.52,
    "nose_bridge_width":        0.45,
    "nose_width":               0.62,   # narines légèrement évasées
    "nose_tip_projection":      0.38,
    "nose_tip_width":           0.55,

    # Yeux en amande — trait très marqué sur la photo
    "eye_size":                 0.55,
    "eye_depth":                0.48,
    "eye_tilt":                 -0.12,  # légèrement inclinés
    "eye_spacing":              0.50,
    "eye_height":               0.52,
    "brow_height":              0.55,
    "brow_thickness":           0.45,   # sourcils fins, dessinés
    "brow_arch":                0.50,

    # Lèvres — fines à moyennes
    "lip_fullness":             0.48,
    "lip_width":                0.52,
    "upper_lip_height":         0.45,
    "lower_lip_height":         0.50,
    "mouth_width":              0.52,

    # Corps — grande et très élancée
    "body_height":              177.0,  # cm estimé sur la photo
    "body_muscle":              0.25,   # très fine
    "body_weight":              0.20,
}

# ═══════════════════════════════════════════════════════
#  CHEVEUX — Box braids noires avec perles rouges
#  Visible clairement sur la photo
# ═══════════════════════════════════════════════════════
GROOM_CONFIG = {
    "slot_name":    "Hair",
    "asset_name":   "BraidedLong",  # groom tresses longues
    "params": {
        "HairColor":    unreal.LinearColor(0.03, 0.02, 0.01, 1.0),  # noir profond
        "Melanin":      1.0,
        "Roughness":    0.65,
        "Scatter":      0.50,
        "Width":        0.15,   # tresses fines (box braids)
        "Density":      0.80,
    }
}

# ═══════════════════════════════════════════════════════
#  VÊTEMENT — Drapé bordeaux (côté visible sur photo)
# ═══════════════════════════════════════════════════════
CLOTHING_CONFIG = {
    "slot_name":  "Outfit",
    "asset_name": "Dress_Drape",
    "params": {
        # Bordeaux profond extrait de l'image : #6B1A1A → Lin
        "ClothColor":   unreal.LinearColor(0.36, 0.06, 0.06, 1.0),
        "ClothOpacity": 0.95,
        "ClothRoughness": 0.70,
    }
}

# ═══════════════════════════════════════════════════════
#  MATÉRIAUX POST-ASSEMBLY (à appliquer sur le BP)
#  Ces paramètres sont à passer en Material Instance
#  après l'assembly, via le Blueprint
# ═══════════════════════════════════════════════════════
POST_ASSEMBLY_MATERIALS = {
    # Collier Usekh Maasaï — rouge/orange/jaune/blanc/noir
    "MI_NasetUsekh": {
        "BaseColor_Red":   unreal.LinearColor(0.73, 0.05, 0.05, 1.0),
        "BaseColor_Gold":  unreal.LinearColor(0.79, 0.59, 0.23, 1.0),
        "Metallic":        0.0,   # perles matte
        "Roughness":       0.75,
    },
    # Manchette dorée bras gauche
    "MI_NasetBracer": {
        "BaseColor":  unreal.LinearColor(0.79, 0.59, 0.23, 1.0),
        "Metallic":   0.97,
        "Roughness":  0.10,
        "Emissive":   0.2,
    },
    # Perles cheveux — rouges et noires (visibles sur photo)
    "MI_NasetHairBeads": {
        "BaseColor_Red":  unreal.LinearColor(0.73, 0.05, 0.05, 1.0),
        "BaseColor_Black": unreal.LinearColor(0.02, 0.02, 0.02, 1.0),
        "Metallic":   0.0,
        "Roughness":  0.80,
    }
}

# ═══════════════════════════════════════════════════════
#  FONCTIONS UTILITAIRES
# ═══════════════════════════════════════════════════════
def log(step, total, msg):
    print(f"[{step}/{total}] {msg}")

def safe_set_prop(obj, key, value):
    try:
        obj.set_editor_property(key, value)
        return True
    except Exception as e:
        print(f"   [skip] {key}: {e}")
        return False

def safe_set_head(subsys, mh, key, value):
    try:
        subsys.set_head_control(mh, key, value)
        return True
    except Exception as e:
        print(f"   [skip] {key}: {e}")
        return False

# ═══════════════════════════════════════════════════════
#  PIPELINE PRINCIPAL
# ═══════════════════════════════════════════════════════
def run_naset_pipeline():
    print("=" * 55)
    print("  N'Aset OFM — Pipeline from Image Reference")
    print("  OFM Studio / Négus Dja")
    print("=" * 55)

    subsys      = unreal.get_editor_subsystem(
                      unreal.MetaHumanCharacterEditorSubsystem)
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    lib         = unreal.EditorAssetLibrary

    TOTAL = 8

    # ── 1. Créer ou charger l'asset ──────────────────────
    log(1, TOTAL, "Initialisation asset MH_NasetOFM_v2...")
    if lib.does_asset_exist(FULL_PATH):
        mh = unreal.load_asset(FULL_PATH)
        print("   Asset existant chargé")
    else:
        if not lib.does_directory_exist(ASSET_PATH):
            lib.make_directory(ASSET_PATH)
        mh = asset_tools.create_asset(
            ASSET_NAME, ASSET_PATH,
            unreal.MetaHumanCharacter,
            unreal.MetaHumanCharacterFactory()
        )
        print(f"   Asset créé → {FULL_PATH}")

    if not mh:
        print("[FATAL] Impossible de créer l'asset. Arrêt.")
        return

    # ── 2. Appliquer les propriétés skin ─────────────────
    log(2, TOTAL, "Application skin (peau image référence)...")
    ok = 0
    for k, v in SKIN_PROPS.items():
        if safe_set_prop(mh, k, v):
            ok += 1
    print(f"   {ok}/{len(SKIN_PROPS)} propriétés skin appliquées")

    # ── 3. Ouvrir l'éditeur + morphologie visage ─────────
    log(3, TOTAL, "Morphologie visage (analyse image)...")
    subsys.open_editor_for_asset(mh)
    ok = 0
    for k, v in FACE_CONTROLS.items():
        if safe_set_head(subsys, mh, k, v):
            ok += 1
    subsys.commit_changes(mh)
    print(f"   {ok}/{len(FACE_CONTROLS)} contrôles morpho appliqués")

    # ── 4. Corps élancé ──────────────────────────────────
    log(4, TOTAL, "Configuration corps élancé (177cm)...")
    try:
        subsys.set_body_control(mh, "height", 177.0)
        subsys.set_body_control(mh, "muscle", 0.25)
        subsys.set_body_control(mh, "weight", 0.20)
        subsys.commit_changes(mh)
        print("   Corps configuré")
    except Exception as e:
        print(f"   [skip] Body controls: {e}")

    # ── 5. Groom — box braids ────────────────────────────
    log(5, TOTAL, "Groom — box braids noires + perles...")
    try:
        gs = unreal.MetaHumanPipelineSlotSelection()
        gs.slot_name  = GROOM_CONFIG["slot_name"]
        gs.asset_name = GROOM_CONFIG["asset_name"]
        subsys.set_groom(mh, gs)
        subsys.asset_for_preview(mh)
        for k, v in GROOM_CONFIG["params"].items():
            try:
                subsys.set_groom_instance_parameter(
                    mh, GROOM_CONFIG["slot_name"], k, v)
            except Exception:
                pass
        subsys.commit_changes(mh)
        print("   Groom configuré")
    except Exception as e:
        print(f"   [skip] Groom: {e}")

    # ── 6. Clothing — drapé bordeaux ────────────────────
    log(6, TOTAL, "Clothing — drapé bordeaux...")
    try:
        cs = unreal.MetaHumanPipelineSlotSelection()
        cs.slot_name  = CLOTHING_CONFIG["slot_name"]
        cs.asset_name = CLOTHING_CONFIG["asset_name"]
        subsys.set_clothing(mh, cs)
        subsys.asset_for_preview(mh)
        for k, v in CLOTHING_CONFIG["params"].items():
            try:
                subsys.set_clothing_instance_parameter(
                    mh, CLOTHING_CONFIG["slot_name"], k, v)
            except Exception:
                pass
        subsys.commit_changes(mh)
        print("   Clothing configuré")
    except Exception as e:
        print(f"   [skip] Clothing: {e}")

    # ── 7. Textures cloud + Auto-rig ─────────────────────
    log(7, TOTAL, "Textures cloud + auto-rigging...")
    try:
        tp = unreal.MetaHumanRequestTextureSourcesParams()
        tp.blocking = True
        tp.report_progress = True
        subsys.request_texture_sources(mh, tp)
        print("   Textures OK")
    except Exception as e:
        print(f"   [skip] Textures: {e}")

    try:
        rp = unreal.MetaHumanRequestAutoRiggingParams()
        rp.blocking = True
        rp.report_progress = True
        subsys.request_auto_rigging(mh, rp)
        print("   Auto-rig OK")
    except Exception as e:
        print(f"   [skip] Auto-rig: {e}")

    # ── 8. Assembly UE Cine ──────────────────────────────
    log(8, TOTAL, "Assembly UE Cine → BP_NasetOFM_v2...")
    try:
        ap = unreal.MetaHumanAssemblyParams()
        ap.pipeline            = unreal.MetaHumanPipeline.UE_CINE
        ap.blueprint_name      = "BP_NasetOFM_v2"
        ap.output_directory    = OUT_DIR
        ap.overwrite_existing  = True
        result = subsys.assemble_character(mh, ap)
        if result:
            print(f"   Blueprint → {OUT_DIR}BP_NasetOFM_v2")
        else:
            print("   [WARN] Assembly retourné None — vérifier l'éditeur")
    except Exception as e:
        print(f"   [skip] Assembly: {e}")

    # ── Sauvegarde finale ────────────────────────────────
    lib.save_asset(mh.get_path_name())

    print("\n" + "=" * 55)
    print("  DONE — N'Aset OFM pipeline terminé")
    print(f"  Asset     : {FULL_PATH}")
    print(f"  Blueprint : {OUT_DIR}BP_NasetOFM_v2")
    print("=" * 55)
    print("\nPost-assembly manuel requis :")
    print("  1. Attacher SM_NasetUsekh_Necklace → socket neck_01")
    print("  2. Attacher SM_NasetBracer_Left    → socket lowerarm_l")
    print("  3. Ajouter NS_NasetAura            → socket spine_03")
    print("  4. Appliquer MI_NasetSkin sur SKM_Face (pores, SSS)")
    print("  5. Ajouter perles cheveux (SM_NasetHairBead × 12)")
    print("  6. Configurer PostProcessVolume → Bloom 0.85, Lens Flare or")

# ── POINT D'ENTRÉE ─────────────────────────────────────
if __name__ == "__main__":
    run_naset_pipeline()
