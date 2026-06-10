"""
N'Aset OFM Toolkit — Blender 5.0 add-on.
Panneau N-sidebar (onglet "N'Aset OFM") avec : Scene Builder, Material Library,
Render Setup, et un linter API Blender 5.0.

Installation : Blender → Édition → Préférences → Add-ons → Installer… → ce fichier → activer.
Conventions et valeurs : faits canoniques N'Aset OFM (CLAUDE.md).
"""

bl_info = {
    "name": "N'Aset OFM Toolkit",
    "author": "Negus Dja",
    "version": (1, 0, 0),
    "blender": (5, 0, 1),
    "location": "View3D > Sidebar (N) > N'Aset OFM",
    "description": "Scene builder, material library, render setup & 5.0 linter pour le projet N'Aset OFM",
    "category": "Object",
}

import bpy


# ─── PALETTE (sRGB → linéaire) ────────────────────────────────────────────────

def _hex_to_linear(hex_str):
    hex_str = hex_str.lstrip('#')
    r, g, b = (int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (lin(r), lin(g), lin(b), 1.0)

COLOR = {
    'or_sacre':     _hex_to_linear('#C9963A'),
    'or_clair':     _hex_to_linear('#E8BC6A'),
    'blanc_ivoire': _hex_to_linear('#FAFAF0'),
    'peau_base':    _hex_to_linear('#6B3D2E'),
    'cheveux':      _hex_to_linear('#0D0A08'),
    'rouge_shuka':  _hex_to_linear('#C0392B'),
    'yeux':         _hex_to_linear('#1A0D00'),
}


# ─── HELPER : réglage d'input défensif (robuste aux changements de version) ───

def _set(node, name, value):
    """Set node input default_value ONLY if the input exists — avoids KeyError
    when Blender renames Principled inputs between versions."""
    if name in node.inputs:
        try:
            node.inputs[name].default_value = value
            return True
        except Exception:
            return False
    return False


# ─── MATÉRIAUX PROCÉDURAUX (détail texture sans fichiers externes) ───────────
# Helpers de nœuds réutilisables : noise, wave, map-range, bump.

def _mul(col, k):
    """Assombrit/éclaircit une couleur linéaire (pour les variations)."""
    return (col[0] * k, col[1] * k, col[2] * k, 1.0)


def _new_mat(name):
    """Crée/réinitialise un matériau nodal, renvoie (mat, node_tree, output)."""
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    out.location = (500, 0)
    return m, nt, out


def _noise(nt, x, y, scale, detail=4.0, roughness=0.6):
    n = nt.nodes.new('ShaderNodeTexNoise')
    n.location = (x, y)
    _set(n, 'Scale', scale)
    _set(n, 'Detail', detail)
    _set(n, 'Roughness', roughness)
    return n


def _wave(nt, x, y, scale, distortion=2.0, detail=2.0):
    n = nt.nodes.new('ShaderNodeTexWave')
    n.location = (x, y)
    _set(n, 'Scale', scale)
    _set(n, 'Distortion', distortion)
    _set(n, 'Detail', detail)
    return n


def _maprange(nt, x, y, lo, hi):
    n = nt.nodes.new('ShaderNodeMapRange')
    n.location = (x, y)
    _set(n, 'To Min', lo)
    _set(n, 'To Max', hi)
    return n


def _bump_from(nt, height_node, height_socket, strength, x, y):
    b = nt.nodes.new('ShaderNodeBump')
    b.location = (x, y)
    _set(b, 'Strength', strength)
    nt.links.new(height_node.outputs[height_socket], b.inputs['Height'])
    return b


# ── Builders par matériau (chacun renvoie le matériau) ────────────────────────

def build_peau():
    """Peau : variation de teinte (blotches), roughness non-uniforme, pores (bump)."""
    m, nt, out = _new_mat('Mat_Peau_Naset')
    b = nt.nodes.new('ShaderNodeBsdfPrincipled'); b.location = (200, 0)
    _set(b, 'Subsurface Weight', 0.30)
    _set(b, 'Subsurface Scale', 0.05)
    _set(b, 'Subsurface Radius', (1.2, 0.6, 0.3))
    _set(b, 'Specular IOR Level', 0.45)
    _set(b, 'IOR', 1.4)
    _set(b, 'Coat Weight', 0.03)

    # Variation de teinte : noise large → mélange base ↔ teinte plus sombre
    n_col = _noise(nt, -700, 250, 12.0, 6.0)
    mr_col = _maprange(nt, -480, 250, 0.0, 0.30)
    nt.links.new(n_col.outputs['Fac'], mr_col.inputs['Value'])
    mix = nt.nodes.new('ShaderNodeMixRGB'); mix.location = (-250, 250)
    mix.inputs['Color1'].default_value = COLOR['peau_base']
    mix.inputs['Color2'].default_value = _mul(COLOR['peau_base'], 0.78)
    nt.links.new(mr_col.outputs['Result'], mix.inputs['Fac'])
    nt.links.new(mix.outputs['Color'], b.inputs['Base Color'])

    # Roughness non-uniforme (0.42–0.58)
    n_r = _noise(nt, -700, -40, 40.0, 4.0)
    mr_r = _maprange(nt, -480, -40, 0.42, 0.58)
    nt.links.new(n_r.outputs['Fac'], mr_r.inputs['Value'])
    nt.links.new(mr_r.outputs['Result'], b.inputs['Roughness'])

    # Pores : noise haute fréquence → bump subtil
    n_p = _noise(nt, -700, -320, 250.0, 2.0)
    bump = _bump_from(nt, n_p, 'Fac', 0.05, -250, -300)
    nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])

    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return m


def build_or():
    """Or : roughness brossée (anisotrope-like) + micro-rayures (bump) + émission."""
    m, nt, out = _new_mat('Mat_Or_Emission')
    b = nt.nodes.new('ShaderNodeBsdfPrincipled'); b.location = (200, 0)
    _set(b, 'Base Color', COLOR['or_sacre'])
    _set(b, 'Metallic', 0.95)
    _set(b, 'Specular IOR Level', 0.5)
    _set(b, 'Emission Color', COLOR['or_clair'])
    _set(b, 'Emission Strength', 0.2)

    # Roughness brossée 0.05–0.18
    n_r = _noise(nt, -700, 100, 60.0, 8.0)
    mr_r = _maprange(nt, -480, 100, 0.05, 0.18)
    nt.links.new(n_r.outputs['Fac'], mr_r.inputs['Value'])
    nt.links.new(mr_r.outputs['Result'], b.inputs['Roughness'])

    # Micro-rayures
    n_s = _noise(nt, -700, -220, 300.0, 2.0)
    bump = _bump_from(nt, n_s, 'Fac', 0.02, -250, -200)
    nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])

    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return m


def build_yeux():
    """Yeux : iris sombre + couche humide (coat) pour le réalisme du regard."""
    m, nt, out = _new_mat('Mat_Yeux_Iris')
    b = nt.nodes.new('ShaderNodeBsdfPrincipled'); b.location = (200, 0)
    _set(b, 'Base Color', COLOR['yeux'])
    _set(b, 'Roughness', 0.08)
    _set(b, 'IOR', 1.45)
    _set(b, 'Coat Weight', 1.0)      # film lacrymal brillant
    _set(b, 'Coat Roughness', 0.0)

    # Légère variation radiale de l'iris
    n = _noise(nt, -500, 0, 50.0, 4.0)
    mr = _maprange(nt, -280, 0, 0.05, 0.14)
    nt.links.new(n.outputs['Fac'], mr.inputs['Value'])
    nt.links.new(mr.outputs['Result'], b.inputs['Roughness'])

    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return m


def build_drape():
    """Drapé lin ivoire : tissage (wave→bump), sheen, variation de teinte."""
    m, nt, out = _new_mat('Mat_Drape_Ivoire')
    b = nt.nodes.new('ShaderNodeBsdfPrincipled'); b.location = (200, 0)
    _set(b, 'Roughness', 0.60)
    _set(b, 'Sheen Weight', 0.30)

    # Variation de teinte douce
    n_c = _noise(nt, -700, 250, 10.0, 4.0)
    mr_c = _maprange(nt, -480, 250, 0.0, 0.10)
    nt.links.new(n_c.outputs['Fac'], mr_c.inputs['Value'])
    mix = nt.nodes.new('ShaderNodeMixRGB'); mix.location = (-250, 250)
    mix.inputs['Color1'].default_value = COLOR['blanc_ivoire']
    mix.inputs['Color2'].default_value = _mul(COLOR['blanc_ivoire'], 0.90)
    nt.links.new(mr_c.outputs['Result'], mix.inputs['Fac'])
    nt.links.new(mix.outputs['Color'], b.inputs['Base Color'])

    # Tissage du lin : wave → bump
    w = _wave(nt, -700, -120, 120.0, 1.0, 2.0)
    bump = _bump_from(nt, w, 'Fac', 0.25, -250, -120)
    nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])

    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return m


def build_shuka():
    """Shúkà : laine rouge, tissage plus marqué, mat."""
    m, nt, out = _new_mat('Mat_Shuka_Rouge')
    b = nt.nodes.new('ShaderNodeBsdfPrincipled'); b.location = (200, 0)
    _set(b, 'Base Color', COLOR['rouge_shuka'])
    _set(b, 'Roughness', 0.62)
    _set(b, 'Sheen Weight', 0.15)

    w = _wave(nt, -700, -120, 100.0, 1.5, 2.0)
    bump = _bump_from(nt, w, 'Fac', 0.32, -250, -120)
    nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])

    # Fibres : roughness légèrement variable
    n_r = _noise(nt, -700, 120, 80.0, 4.0)
    mr_r = _maprange(nt, -480, 120, 0.55, 0.68)
    nt.links.new(n_r.outputs['Fac'], mr_r.inputs['Value'])
    nt.links.new(mr_r.outputs['Result'], b.inputs['Roughness'])

    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return m


def build_cheveux():
    """Cheveux : Principled Hair BSDF, noir profond, roughness variée."""
    m, nt, out = _new_mat('Mat_Cheveux_Naset')
    h = nt.nodes.new('ShaderNodeBsdfHairPrincipled'); h.location = (200, 0)
    _set(h, 'Color', COLOR['cheveux'])
    _set(h, 'Roughness', 0.55)
    _set(h, 'Radial Roughness', 0.40)
    nt.links.new(h.outputs['BSDF'], out.inputs['Surface'])
    return m


# Registre : clé → (label, builder)
BUILDERS = {
    'PEAU':    build_peau,
    'OR':      build_or,
    'YEUX':    build_yeux,
    'CHEVEUX': build_cheveux,
    'DRAPE':   build_drape,
    'SHUKA':   build_shuka,
}


# ═══ OPERATORS ════════════════════════════════════════════════════════════════

class NASET_OT_apply_material(bpy.types.Operator):
    """Applique un matériau canonique N'Aset aux objets sélectionnés"""
    bl_idname = "naset.apply_material"
    bl_label = "Appliquer matériau N'Aset"
    bl_options = {'REGISTER', 'UNDO'}

    mat_type: bpy.props.EnumProperty(
        items=[(k, k.capitalize(), "") for k in BUILDERS.keys()],
        name="Matériau",
    )

    def execute(self, context):
        mat = BUILDERS[self.mat_type]()      # build procédural détaillé

        targets = [o for o in context.selected_objects if o.type == 'MESH']
        if not targets:
            self.report({'WARNING'}, "Aucun objet mesh sélectionné")
            return {'CANCELLED'}

        for obj in targets:
            if obj.data.materials:
                obj.data.materials[obj.active_material_index] = mat
            else:
                obj.data.materials.append(mat)

        self.report({'INFO'}, f"{mat_name} appliqué à {len(targets)} objet(s)")
        return {'FINISHED'}


class NASET_OT_build_base_scene(bpy.types.Operator):
    """Crée la structure de base : caméra, 3 lumières, unités métriques"""
    bl_idname = "naset.build_base_scene"
    bl_label = "Construire scène de base"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        scene.unit_settings.system = 'METRIC'
        scene.unit_settings.scale_length = 0.01
        scene.render.fps = 24

        # Caméra
        if 'Camera_Principale' not in bpy.data.objects:
            bpy.ops.object.camera_add(location=(0, -5, 1.65), rotation=(1.5708, 0, 0))
            cam = context.active_object
            cam.name = cam.data.name = 'Camera_Principale'
            cam.data.lens = 50.0
            cam.data.dof.use_dof = True
            cam.data.dof.aperture_fstop = 2.8
            scene.camera = cam

        # Lumières
        lights = {
            'Key_Light':  (800, (5, -5, 3),  (1.0, 0.95, 0.85)),
            'Fill_Light': (80,  (-4, -3, 2), (1.0, 0.90, 0.80)),
            'Rim_Light':  (200, (0, 5, 2.5), COLOR['or_sacre'][:3]),
        }
        for name, (energy, loc, col) in lights.items():
            if name in bpy.data.objects:
                continue
            bpy.ops.object.light_add(type='AREA', location=loc)
            lo = context.active_object
            lo.name = lo.data.name = name
            lo.data.energy = energy
            lo.data.color = col
            lo.data.size = 2.0

        self.report({'INFO'}, "Scène de base créée (caméra + Key/Fill/Rim)")
        return {'FINISHED'}


class NASET_OT_render_setup(bpy.types.Operator):
    """Configure Cycles GPU · 4K · Filmic Medium High Contrast · 24fps"""
    bl_idname = "naset.render_setup"
    bl_label = "Setup rendu 4K"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        r = scene.render
        r.engine = 'CYCLES'
        r.resolution_x = 3840
        r.resolution_y = 2160
        r.resolution_percentage = 100
        r.fps = 24

        # GPU (toléré si indisponible)
        try:
            prefs = context.preferences.addons["cycles"].preferences
            prefs.compute_device_type = 'OPTIX'
            prefs.get_devices()
            for d in prefs.devices:
                d.use = True
        except Exception as e:
            self.report({'WARNING'}, f"GPU non configuré : {e}")

        c = scene.cycles
        c.device = 'GPU'
        c.samples = 256
        c.use_denoising = True
        c.denoiser = 'OPENIMAGEDENOISE'
        c.use_adaptive_sampling = True

        # Filmic — Blender 5.0 : look SANS préfixe "Filmic - "
        scene.view_settings.view_transform = 'Filmic'
        try:
            scene.view_settings.look = 'Medium High Contrast'
        except TypeError:
            pass  # config OCIO différente

        self.report({'INFO'}, "Rendu : Cycles GPU · 4K · Filmic Medium High Contrast")
        return {'FINISHED'}


# Pièges API Blender 5.0 : (sous-chaîne, message)
LINT_RULES = [
    ("blend_method",            "material.blend_method supprimé en 5.0 (EEVEE Next)"),
    ("show_transparent_back",   "material.show_transparent_back supprimé en 5.0"),
    ("Filmic - ",               "look : enlever le préfixe 'Filmic - '"),
    ("'Subsurface Color'",      "input 'Subsurface Color' supprimé (utiliser Base Color)"),
    ("inputs['Subsurface']",    "input renommé → 'Subsurface Weight'"),
    ("inputs['Specular']",      "input renommé → 'Specular IOR Level'"),
    ("inputs['Transmission']",  "input renommé → 'Transmission Weight'"),
    ("inputs['Clearcoat']",     "input renommé → 'Coat Weight'"),
    ("settings.gravity",        "ParticleSettings n'a pas .gravity → effector_weights.gravity"),
    ("pset.gravity",            "ParticleSettings n'a pas .gravity → effector_weights.gravity"),
]


class NASET_OT_lint_50(bpy.types.Operator):
    """Scanne les scripts de l'éditeur de texte pour les pièges API Blender 5.0"""
    bl_idname = "naset.lint_50"
    bl_label = "Vérifier scripts 5.0"

    def execute(self, context):
        issues = []
        for text in bpy.data.texts:
            src = text.as_string()
            for needle, msg in LINT_RULES:
                if needle in src:
                    issues.append(f"[{text.name}] {msg}")

        if not issues:
            self.report({'INFO'}, "Aucun piège 5.0 détecté")
        else:
            for i in issues:
                print("[NASET LINT]", i)
            self.report({'WARNING'}, f"{len(issues)} piège(s) 5.0 — voir la console")

        def draw(self_menu, ctx):
            col = self_menu.layout.column()
            if not issues:
                col.label(text="✅ Aucun piège Blender 5.0 détecté", icon='CHECKMARK')
            else:
                col.label(text=f"{len(issues)} problème(s) :", icon='ERROR')
                for i in issues:
                    col.label(text=i)
        context.window_manager.popup_menu(draw, title="Linter Blender 5.0", icon='SCRIPT')
        return {'FINISHED'}


# ═══ PANNEAU UI ═══════════════════════════════════════════════════════════════

class NASET_PT_panel(bpy.types.Panel):
    bl_label = "N'Aset OFM Toolkit"
    bl_idname = "NASET_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "N'Aset OFM"

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Scène", icon='SCENE_DATA')
        box.operator("naset.build_base_scene", icon='OUTLINER_OB_CAMERA')
        box.operator("naset.render_setup", icon='RENDER_STILL')

        box = layout.box()
        box.label(text="Matériaux", icon='MATERIAL')
        labels = {
            'PEAU': "Peau SSS", 'OR': "Or sacré", 'YEUX': "Yeux iris",
            'CHEVEUX': "Cheveux", 'DRAPE': "Drapé ivoire", 'SHUKA': "Shúkà rouge",
        }
        for key, label in labels.items():
            op = box.operator("naset.apply_material", text=label, icon='SHADING_RENDERED')
            op.mat_type = key
        box.label(text="→ sélectionne un mesh d'abord", icon='INFO')

        box = layout.box()
        box.label(text="Outils", icon='TOOL_SETTINGS')
        box.operator("naset.lint_50", icon='SCRIPT')


# ═══ REGISTER ═════════════════════════════════════════════════════════════════

CLASSES = (
    NASET_OT_apply_material,
    NASET_OT_build_base_scene,
    NASET_OT_render_setup,
    NASET_OT_lint_50,
    NASET_PT_panel,
)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
