"""
naset_scene_setup.py
Setup complet de la scène Blender pour N'Aset OFM.
Crée la structure d'objets, configure les paramètres de base et les matériaux.
Lance depuis Blender : Text Editor > Run Script
"""

import bpy
import mathutils


# ─── PARAMÈTRES GLOBAUX ───────────────────────────────────────────────────────

FRAME_START = 1
FRAME_END   = 2280
FPS         = 24

UNIT_SCALE  = 0.01   # Metric, cohérent avec UE5

# Palette officielle N'Aset OFM (valeurs linéaires, pas sRGB)
def hex_to_linear(hex_str):
    hex_str = hex_str.lstrip('#')
    r, g, b = (int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    # Conversion sRGB → Linear
    def to_lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (to_lin(r), to_lin(g), to_lin(b), 1.0)

COLOR = {
    'or_sacre':    hex_to_linear('#C9963A'),
    'or_clair':    hex_to_linear('#E8BC6A'),
    'blanc_ivoire':hex_to_linear('#FAFAF0'),
    'peau_base':   hex_to_linear('#6B3D2E'),
    'cheveux':     hex_to_linear('#0D0A08'),
    'accent':      hex_to_linear('#1C1A3A'),
    'rouge_shuka': hex_to_linear('#C0392B'),
    'yeux':        hex_to_linear('#1A0D00'),
    'levres':      hex_to_linear('#7B2D2D'),
}


# ─── CONFIGURATION SCÈNE ──────────────────────────────────────────────────────

def setup_scene():
    scene = bpy.context.scene
    scene.frame_start = FRAME_START
    scene.frame_end   = FRAME_END
    scene.render.fps  = FPS

    # Unités métriques
    scene.unit_settings.system      = 'METRIC'
    scene.unit_settings.scale_length = UNIT_SCALE
    scene.unit_settings.length_unit  = 'CENTIMETERS'

    print(f"[SETUP] Scène configurée : {FRAME_START}–{FRAME_END} frames @ {FPS}fps")


# ─── CONFIGURATION RENDU (Cycles) ─────────────────────────────────────────────

def setup_render():
    scene  = bpy.context.scene
    render = scene.render
    cycles = scene.cycles

    render.engine              = 'CYCLES'
    render.resolution_x        = 3840
    render.resolution_y        = 2160
    render.resolution_percentage = 100

    # Cycles GPU — config preferences + devices
    cycles_prefs = bpy.context.preferences.addons["cycles"].preferences
    cycles_prefs.compute_device_type = 'OPTIX'   # OptiX pour NVIDIA ; remplacer par 'CUDA' ou 'HIP' si besoin
    cycles_prefs.get_devices()
    for device in cycles_prefs.devices:
        device.use = True   # active tous les GPU détectés

    cycles.device              = 'GPU'
    cycles.samples             = 256
    cycles.use_denoising       = True
    cycles.denoiser            = 'OPENIMAGEDENOISE'
    cycles.use_adaptive_sampling = True
    cycles.adaptive_threshold  = 0.01

    # Color Management — Filmic Medium High Contrast
    scene.view_settings.view_transform = 'Filmic'
    scene.view_settings.look            = 'Medium High Contrast'   # Blender 5.0 : plus de préfixe "Filmic - "
    scene.view_settings.exposure        = 0.0
    scene.view_settings.gamma           = 1.0

    print("[SETUP] Rendu : Cycles GPU · 4K · Filmic Medium High Contrast")


# ─── CAMÉRA PRINCIPALE ────────────────────────────────────────────────────────

def create_camera():
    # Supprimer caméra existante si présent
    if 'Camera_Principale' in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects['Camera_Principale'], do_unlink=True)

    bpy.ops.object.camera_add(location=(0, -10, 1.65))
    cam_obj = bpy.context.active_object
    cam_obj.name = 'Camera_Principale'

    cam = cam_obj.data
    cam.name          = 'Camera_Principale'
    cam.lens          = 35.0    # S1 — 35mm fixe
    cam.dof.use_dof   = True
    cam.dof.aperture_fstop = 8.0

    # Point de visée
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 1.65))
    target = bpy.context.active_object
    target.name = 'Camera_Target'

    # Contrainte Track To
    constraint = cam_obj.constraints.new(type='TRACK_TO')
    constraint.target    = target
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis    = 'UP_Y'

    bpy.context.scene.camera = cam_obj
    print("[SETUP] Caméra 'Camera_Principale' créée · 35mm · f/8")


# ─── LUMIÈRES ─────────────────────────────────────────────────────────────────

def create_lights():
    lights = {
        'Key_Light':  {'type': 'AREA',  'energy': 800,  'location': (5, -5, 3),   'color': (1.0, 0.95, 0.85, 1.0)},
        'Fill_Light': {'type': 'AREA',  'energy': 80,   'location': (-4, -3, 2),  'color': (1.0, 0.90, 0.80, 1.0)},
        'Rim_Light':  {'type': 'AREA',  'energy': 200,  'location': (0, 5, 2.5),  'color': COLOR['or_sacre']},
    }
    for name, params in lights.items():
        if name in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)

        bpy.ops.object.light_add(type=params['type'], location=params['location'])
        light_obj = bpy.context.active_object
        light_obj.name     = name
        light_data         = light_obj.data
        light_data.name    = name
        light_data.energy  = params['energy']
        light_data.color   = params['color'][:3]

        if params['type'] == 'AREA':
            light_data.size = 2.0

    print("[SETUP] Lumières créées : Key / Fill / Rim")


# ─── MATÉRIAUX ────────────────────────────────────────────────────────────────

def create_material_peau():
    mat = bpy.data.materials.get('Mat_Peau_Naset') or bpy.data.materials.new('Mat_Peau_Naset')
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out    = nodes.new('ShaderNodeOutputMaterial')
    bsdf   = nodes.new('ShaderNodeBsdfPrincipled')

    bsdf.inputs['Base Color'].default_value         = COLOR['peau_base']
    # Blender 4.0+ : Subsurface Color supprimé (Base Color fait office)
    bsdf.inputs['Subsurface Weight'].default_value  = 0.30
    bsdf.inputs['Subsurface Scale'].default_value   = 0.05   # multiplicateur sur Radius (nouveau 4.0+)
    bsdf.inputs['Subsurface Radius'].default_value  = (1.2, 0.6, 0.3)
    bsdf.inputs['Roughness'].default_value          = 0.50
    bsdf.inputs['Metallic'].default_value           = 0.0
    bsdf.inputs['Specular IOR Level'].default_value = 0.45
    bsdf.inputs['IOR'].default_value                = 1.4
    bsdf.inputs['Coat Weight'].default_value        = 0.03

    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    bsdf.location = (-300, 0)
    out.location  = (0, 0)

    print("[MAT] Mat_Peau_Naset créé")
    return mat


def create_material_or():
    mat = bpy.data.materials.get('Mat_Or_Emission') or bpy.data.materials.new('Mat_Or_Emission')
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out    = nodes.new('ShaderNodeOutputMaterial')
    bsdf   = nodes.new('ShaderNodeBsdfPrincipled')
    emit   = nodes.new('ShaderNodeEmission')
    mix    = nodes.new('ShaderNodeMixShader')

    bsdf.inputs['Base Color'].default_value  = COLOR['or_sacre']
    bsdf.inputs['Metallic'].default_value    = 0.95
    bsdf.inputs['Roughness'].default_value   = 0.10
    bsdf.inputs['Specular IOR Level'].default_value = 0.5

    emit.inputs['Color'].default_value    = COLOR['or_clair']
    emit.inputs['Strength'].default_value = 0.2   # keyframé en animation

    mix.inputs['Fac'].default_value = 0.2

    links.new(bsdf.outputs['BSDF'],   mix.inputs[1])
    links.new(emit.outputs['Emission'], mix.inputs[2])
    links.new(mix.outputs['Shader'],   out.inputs['Surface'])

    bsdf.location  = (-400, 100)
    emit.location  = (-400, -100)
    mix.location   = (-100, 0)
    out.location   = (150, 0)

    print("[MAT] Mat_Or_Emission créé")
    return mat


def create_material_yeux():
    mat = bpy.data.materials.get('Mat_Yeux_Iris') or bpy.data.materials.new('Mat_Yeux_Iris')
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out    = nodes.new('ShaderNodeOutputMaterial')
    bsdf   = nodes.new('ShaderNodeBsdfPrincipled')
    emit   = nodes.new('ShaderNodeEmission')
    mix    = nodes.new('ShaderNodeMixShader')

    bsdf.inputs['Base Color'].default_value  = COLOR['yeux']
    bsdf.inputs['Roughness'].default_value   = 0.05
    bsdf.inputs['Metallic'].default_value    = 0.0
    bsdf.inputs['IOR'].default_value         = 1.45

    emit.inputs['Color'].default_value    = COLOR['or_sacre']
    emit.inputs['Strength'].default_value = 0.0   # keyframé S4→S5

    mix.inputs['Fac'].default_value = 0.0

    links.new(bsdf.outputs['BSDF'],    mix.inputs[1])
    links.new(emit.outputs['Emission'], mix.inputs[2])
    links.new(mix.outputs['Shader'],   out.inputs['Surface'])

    bsdf.location  = (-400, 100)
    emit.location  = (-400, -100)
    mix.location   = (-100, 0)
    out.location   = (150, 0)

    print("[MAT] Mat_Yeux_Iris créé")
    return mat


# ─── POINT D'ENTRÉE ───────────────────────────────────────────────────────────

def main():
    print("\n━━━ N'Aset OFM · Scene Setup ━━━")
    setup_scene()
    setup_render()
    create_camera()
    create_lights()
    create_material_peau()
    create_material_or()
    create_material_yeux()
    print("━━━ Setup terminé ━━━\n")


main()
