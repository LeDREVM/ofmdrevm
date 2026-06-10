"""
naset_render_output.py
Configure les sorties de rendu par scène et lance le batch render.
Format : PNG 16bit (prévisu) ou EXR MultiLayer (prod).
Lance depuis Blender : Text Editor > Run Script
"""

import bpy
import os


# ─── PARAMÈTRES ───────────────────────────────────────────────────────────────

OUTPUT_BASE = "//renders/"   # Chemin relatif au .blend

# Passes de rendu activées
RENDER_PASSES = {
    'combined':     True,
    'z':            True,
    'diffuse_color':True,
    'glossy_direct':True,
    'emission':     True,
    'shadow_catcher':False,
}

# Scènes à rendre (frame_start, frame_end, sous-dossier)
RENDER_SCENES = [
    (1,    240,  'S1_Apparition'),
    (241,  960,  'S2_Approche'),
    (961,  1440, 'S3_Regard'),
    (1441, 1920, 'S4_Descente'),
    (1921, 2280, 'S5_Eveil'),
]


# ─── CONFIGURATION PASSES ─────────────────────────────────────────────────────

def setup_render_passes():
    view_layer = bpy.context.view_layer

    view_layer.use_pass_z                  = RENDER_PASSES['z']
    view_layer.use_pass_diffuse_color      = RENDER_PASSES['diffuse_color']
    view_layer.use_pass_glossy_direct      = RENDER_PASSES['glossy_direct']
    view_layer.use_pass_emit               = RENDER_PASSES['emission']

    print("[RENDER] Passes configurées")


# ─── NŒUDS COMPOSITING ────────────────────────────────────────────────────────

def setup_compositor(output_dir, use_exr=False):
    scene = bpy.context.scene
    scene.use_nodes = True
    tree  = scene.node_tree
    nodes = tree.nodes
    links = tree.links
    nodes.clear()

    render_layers = nodes.new('CompositorNodeRLayers')
    composite     = nodes.new('CompositorNodeComposite')
    file_output   = nodes.new('CompositorNodeOutputFile')

    render_layers.location = (-400, 0)
    composite.location     = (200, 100)
    file_output.location   = (200, -100)

    links.new(render_layers.outputs['Image'], composite.inputs['Image'])

    # Sortie fichier
    file_output.base_path = output_dir
    if use_exr:
        file_output.format.file_format        = 'OPEN_EXR_MULTILAYER'
        file_output.format.color_depth        = '32'
        file_output.format.exr_codec          = 'ZIP'
        links.new(render_layers.outputs['Image'], file_output.inputs['Image'])
    else:
        file_output.format.file_format        = 'PNG'
        file_output.format.color_depth        = '16'
        file_output.format.color_mode         = 'RGBA'
        file_output.format.compression        = 15
        links.new(render_layers.outputs['Image'], file_output.inputs['Image'])

    print(f"[RENDER] Compositor configuré → {output_dir}")


# ─── RENDER PAR SCÈNE ─────────────────────────────────────────────────────────

def render_scene(frame_start, frame_end, scene_name, use_exr=False):
    scene  = bpy.context.scene
    render = scene.render

    output_dir = os.path.join(OUTPUT_BASE, scene_name)
    render.filepath = output_dir + "/Naset_" + scene_name + "_"

    # Nommage fichier : Naset_S[scene]_F[frame]
    render.use_file_extension   = True
    render.use_overwrite         = False

    scene.frame_start = frame_start
    scene.frame_end   = frame_end

    setup_compositor(output_dir, use_exr)

    print(f"\n[RENDER] ▶ {scene_name} · frames {frame_start}–{frame_end}")
    bpy.ops.render.render(animation=True, write_still=False)
    print(f"[RENDER] ✓ {scene_name} terminé")


# ─── RENDER COMPLET ───────────────────────────────────────────────────────────

def render_all(use_exr=False):
    print("\n━━━ N'Aset OFM · Batch Render ━━━")
    setup_render_passes()

    for frame_start, frame_end, scene_name in RENDER_SCENES:
        render_scene(frame_start, frame_end, scene_name, use_exr)

    print("\n━━━ Batch Render terminé ━━━")
    print(f"Fichiers dans : {OUTPUT_BASE}")


# ─── RENDER SCÈNE UNIQUE (debug rapide) ───────────────────────────────────────

def render_single_scene(scene_index=0, use_exr=False):
    """Lance uniquement une scène. scene_index : 0=S1, 1=S2, 2=S3, 3=S4, 4=S5"""
    setup_render_passes()
    fs, fe, name = RENDER_SCENES[scene_index]
    render_scene(fs, fe, name, use_exr)


# ─── POINT D'ENTRÉE ───────────────────────────────────────────────────────────
# Modifier ici pour cibler une scène ou lancer tout

# Option A : render toutes les scènes en PNG
# render_all(use_exr=False)

# Option B : render toutes les scènes en EXR (prod)
# render_all(use_exr=True)

# Option C : render une scène unique (index 0=S1 … 4=S5)
render_single_scene(scene_index=0, use_exr=False)
