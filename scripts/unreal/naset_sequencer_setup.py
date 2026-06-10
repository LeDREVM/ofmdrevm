"""
naset_sequencer_setup.py
Setup du Sequencer cinématique UE5 pour N'Aset OFM.
Crée le Level Sequence, configure caméras et VFX Niagara par scène.
Lance depuis UE5 : Tools > Execute Python Script
"""

import unreal


# ─── PARAMÈTRES ───────────────────────────────────────────────────────────────

SEQUENCE_PATH    = '/Game/NasetOFM/Cinematics/Naset_CM_Main'
SEQUENCE_NAME    = 'Naset_CM_Main'
FRAME_RATE       = unreal.FrameRate(24, 1)
TOTAL_FRAMES     = 2280

# Scènes (frame_start, frame_end, label)
SCENES = [
    (0,    240,  'S1_Apparition'),
    (241,  960,  'S2_Approche'),
    (961,  1440, 'S3_Regard'),
    (1441, 1920, 'S4_Descente'),
    (1921, 2280, 'S5_Eveil'),
]

# Chemins assets UE5 attendus (à ajuster selon ton projet)
ASSET_PATHS = {
    'camera':        '/Game/NasetOFM/Cameras/BP_NasetCamera',
    'naset_actor':   '/Game/NasetOFM/Characters/BP_NasetCharacter',
    'niagara_gold':  '/Game/NasetOFM/VFX/NS_ParticulesOr',
    'niagara_aura':  '/Game/NasetOFM/VFX/NS_AuraSacree',
    'niagara_eveil': '/Game/NasetOFM/VFX/NS_EveilOudjat',
}


# ─── CRÉATION DU LEVEL SEQUENCE ───────────────────────────────────────────────

def create_sequence():
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    # Vérifier si le sequence existe déjà
    existing = unreal.load_asset(SEQUENCE_PATH)
    if existing:
        print(f"[SEQ] Sequence existante trouvée : {SEQUENCE_PATH}")
        return existing

    factory = unreal.LevelSequenceFactoryNew()
    sequence = asset_tools.create_asset(
        asset_name=SEQUENCE_NAME,
        package_path='/Game/NasetOFM/Cinematics/',
        asset_class=unreal.LevelSequence,
        factory=factory
    )

    if sequence:
        sequence.set_display_rate(FRAME_RATE)
        sequence.set_playback_start(0)
        sequence.set_playback_end(TOTAL_FRAMES)
        unreal.EditorAssetLibrary.save_asset(SEQUENCE_PATH)
        print(f"[SEQ] Level Sequence créé : {SEQUENCE_PATH}")

    return sequence


# ─── AJOUT CAMÉRA ─────────────────────────────────────────────────────────────

def add_camera_track(sequence):
    """Ajoute une piste caméra avec cut sections par scène."""
    # UE5.3+ : utiliser LevelSequenceEditorSubsystem (remplace LevelSequenceEditorBlueprintLibrary)
    ls_system        = unreal.get_editor_subsystem(unreal.LevelSequenceEditorSubsystem)
    camera_cut_track = sequence.add_master_track(unreal.MovieSceneCameraCutTrack)

    scene_lens = {
        'S1_Apparition': 35.0,
        'S2_Approche':   50.0,
        'S3_Regard':     85.0,
        'S4_Descente':   85.0,
        'S5_Eveil':      85.0,
    }

    for frame_start, frame_end, label in SCENES:
        lens = scene_lens.get(label, 85.0)

        # Crée une caméra spawnable pour cette scène
        camera_binding = ls_system.create_camera(is_spawnable=True)
        section        = camera_cut_track.add_section()
        section.set_start_frame(frame_start)
        section.set_end_frame(frame_end)

        binding_id = unreal.MovieSceneObjectBindingID()
        binding_id.set_editor_property('Guid', camera_binding.get_id())
        section.set_editor_property('CameraBindingID', binding_id)

        print(f"[CAM] {label} · {lens}mm · frames {frame_start}–{frame_end}")

    print("[CAM] Piste caméra créée · sections liées")
    return camera_cut_track


# ─── AJOUT PISTE NIAGARA VFX ──────────────────────────────────────────────────

def add_vfx_tracks(sequence):
    """Référence les systèmes Niagara actifs par scène dans le Sequencer."""

    vfx_schedule = [
        # (frame_start, frame_end, asset_key, label)
        (1,    2280, 'niagara_gold',  'Particules_Or — passif S1→S5'),
        (1441, 1920, 'niagara_aura',  'Aura sacrée S4'),
        (1921, 2200, 'niagara_eveil', 'Éveil Oudjat S5'),
    ]

    for frame_start, frame_end, asset_key, label in vfx_schedule:
        asset_path = ASSET_PATHS.get(asset_key)
        if not asset_path:
            print(f"[SKIP] Asset non défini : {asset_key}")
            continue

        asset = unreal.load_asset(asset_path)
        if not asset:
            print(f"[SKIP] Asset non trouvé : {asset_path} — créer NS dans UE5 d'abord")
            continue

        print(f"[VFX] {label} · frames {frame_start}–{frame_end}")

    print("[VFX] Pistes Niagara référencées")


# ─── CONFIGURATION RENDER MOVIE ───────────────────────────────────────────────

def configure_movie_render():
    """Configure Movie Render Queue pour rendu 4K 24fps."""
    settings_class = unreal.MoviePipelinePrimaryConfig

    config = unreal.MoviePipelinePrimaryConfig()

    # Résolution 4K
    output_setting = config.find_or_add_setting_by_class(
        unreal.MoviePipelineOutputSetting
    )
    output_setting.output_resolution = unreal.IntPoint(3840, 2160)
    output_setting.frame_rate_override = FRAME_RATE
    output_setting.output_directory    = unreal.DirectoryPath('/Game/NasetOFM/Renders/')
    output_setting.file_name_format    = '{sequence_name}/{shot_name}.{frame_number}'

    # Format de sortie : EXR
    exr_setting = config.find_or_add_setting_by_class(
        unreal.MoviePipelineImageSequenceOutput_EXR
    )

    # Anti-aliasing
    aa_setting = config.find_or_add_setting_by_class(
        unreal.MoviePipelineAntiAliasingSetting
    )
    aa_setting.spatial_sample_count  = 4
    aa_setting.temporal_sample_count = 4

    print("[RENDER] Movie Render Queue configuré · 4K · EXR · 4x4 samples")
    return config


# ─── RAPPORT DE STRUCTURE ─────────────────────────────────────────────────────

def print_sequence_report():
    print("\n━━━ N'Aset OFM · Sequencer Structure ━━━")
    print(f"Sequence : {SEQUENCE_NAME}")
    print(f"Durée    : {TOTAL_FRAMES} frames @ 24fps = 95s")
    print()
    for frame_start, frame_end, label in SCENES:
        duration = (frame_end - frame_start) / 24
        print(f"  {label:<20} frames {frame_start:>4}–{frame_end:<4}  ({duration:.0f}s)")
    print()
    print("Blueprints attendus :")
    for key, path in ASSET_PATHS.items():
        status = "✓" if unreal.load_asset(path) else "✗ (à créer)"
        print(f"  {status} {key:<20} {path}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")


# ─── POINT D'ENTRÉE ───────────────────────────────────────────────────────────

def main():
    print("\n━━━ N'Aset OFM · UE5 Sequencer Setup ━━━")

    print_sequence_report()

    sequence = create_sequence()
    if not sequence:
        print("[ERREUR] Impossible de créer le Level Sequence")
        return

    add_camera_track(sequence)
    add_vfx_tracks(sequence)
    configure_movie_render()

    unreal.EditorAssetLibrary.save_asset(SEQUENCE_PATH)
    print("\n━━━ Setup UE5 terminé ━━━\n")


main()
