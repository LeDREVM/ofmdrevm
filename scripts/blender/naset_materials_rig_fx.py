"""
naset_materials_rig_fx.py
Shading avancé + groom + simulation pour N'Aset OFM (ÉTAPES 2→9).
Construit : peau (Noise→ColorRamp→Roughness + Normal), or, tissus Shùkà/Lin,
yeux (émission keyframée), cheveux (Principled Hair), particules or, cloth/collision.

Blender 5.0 — Lance depuis Text Editor > Run Script.

⚠️ Traduction API (anciens noms → Blender 5.0) :
    Subsurface        → Subsurface Weight
    Subsurface Color  → SUPPRIMÉ (Base Color fait office ; Radius teinte le scatter)
    Specular          → Specular IOR Level
    Clearcoat         → Coat Weight
    Sheen             → Sheen Weight
    Translucent       → Transmission Weight

Rig (Rigify) et bake Cloth = étapes manuelles → voir print_manual_steps().
"""

import bpy


# ─── PALETTE ──────────────────────────────────────────────────────────────────

def hex_to_linear(hex_str):
    hex_str = hex_str.lstrip('#')
    r, g, b = (int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    def to_lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (to_lin(r), to_lin(g), to_lin(b), 1.0)

COLOR = {
    'peau_base':   hex_to_linear('#6B3D2E'),
    'peau_sss':    hex_to_linear('#8B4E35'),
    'or_sacre':    hex_to_linear('#C9963A'),
    'shuka':       hex_to_linear('#C0392B'),
    'lin_ivoire':  hex_to_linear('#FAFAF0'),
    'yeux':        hex_to_linear('#1A0D00'),
    'yeux_emit':   hex_to_linear('#C79A3C'),
    'cheveux':     hex_to_linear('#0D0A08'),
}


# ─── HELPER : set input seulement s'il existe (robuste aux versions) ───────────

def safe_set(node, input_name, value):
    """Évite un crash si le socket n'existe pas dans cette version de Blender."""
    if input_name in node.inputs:
        node.inputs[input_name].default_value = value
        return True
    print(f"   [!] socket '{input_name}' absent sur {node.name} — ignoré")
    return False


def fresh_material(name):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.node_tree.nodes.clear()
    return mat


# ─── ÉTAPE 2 — PEAU ───────────────────────────────────────────────────────────

def create_peau():
    mat   = fresh_material('Mat_Peau_Naset')
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    out   = nodes.new('ShaderNodeOutputMaterial');  out.location   = (400, 0)
    bsdf  = nodes.new('ShaderNodeBsdfPrincipled');   bsdf.location  = (100, 0)
    noise = nodes.new('ShaderNodeTexNoise');         noise.location = (-500, -200)
    ramp  = nodes.new('ShaderNodeValToRGB');         ramp.location  = (-300, -200)
    norm_tex = nodes.new('ShaderNodeTexImage');      norm_tex.location = (-500, -450)
    norm_map = nodes.new('ShaderNodeNormalMap');     norm_map.location = (-200, -450)

    # Base
    safe_set(bsdf, 'Base Color', COLOR['peau_base'])
    safe_set(bsdf, 'Subsurface Weight', 0.30)
    safe_set(bsdf, 'Subsurface Scale',  0.05)
    if 'Subsurface Radius' in bsdf.inputs:
        bsdf.inputs['Subsurface Radius'].default_value = (1.2, 0.6, 0.3)
    safe_set(bsdf, 'Metallic', 0.0)
    safe_set(bsdf, 'Specular IOR Level', 0.45)
    safe_set(bsdf, 'IOR', 1.4)
    safe_set(bsdf, 'Sheen Weight', 0.04)

    # Roughness procédurale : Noise → ColorRamp → Roughness (plage 0.45–0.55)
    noise.inputs['Scale'].default_value  = 40.0
    noise.inputs['Detail'].default_value = 6.0
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color    = (0.45, 0.45, 0.45, 1.0)
    ramp.color_ramp.elements[1].position = 1.0
    ramp.color_ramp.elements[1].color    = (0.55, 0.55, 0.55, 1.0)
    links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], bsdf.inputs['Roughness'])

    # Normal map 4K (image à assigner par l'utilisateur)
    norm_tex.label = 'NAset_Normal_4K — charge ta map ici'
    norm_tex.image = None  # → File > assigner NAset_Normal_4K.png
    if norm_tex.image:
        norm_tex.image.colorspace_settings.name = 'Non-Color'
    links.new(norm_tex.outputs['Color'], norm_map.inputs['Color'])
    links.new(norm_map.outputs['Normal'], bsdf.inputs['Normal'])

    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    print("[MAT] Mat_Peau_Naset · Noise→ColorRamp→Roughness + Normal (assigner map 4K)")


# ─── ÉTAPE 3 — OR ─────────────────────────────────────────────────────────────

def create_or():
    mat   = fresh_material('Mat_Or_Emission')
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    out  = nodes.new('ShaderNodeOutputMaterial'); out.location  = (250, 0)
    bsdf = nodes.new('ShaderNodeBsdfPrincipled');  bsdf.location = (-400, 100)
    emit = nodes.new('ShaderNodeEmission');        emit.location = (-400, -150)
    mix  = nodes.new('ShaderNodeMixShader');       mix.location  = (-50, 0)

    safe_set(bsdf, 'Base Color', COLOR['or_sacre'])
    safe_set(bsdf, 'Metallic', 0.97)
    safe_set(bsdf, 'Roughness', 0.10)
    emit.inputs['Color'].default_value    = COLOR['or_sacre']
    emit.inputs['Strength'].default_value = 0.2
    mix.inputs['Fac'].default_value       = 0.2   # BSDF 0.8 + Emission 0.2

    links.new(bsdf.outputs['BSDF'],    mix.inputs[1])
    links.new(emit.outputs['Emission'], mix.inputs[2])
    links.new(mix.outputs['Shader'],   out.inputs['Surface'])
    print("[MAT] Mat_Or_Emission · Mix BSDF/Emission 0.8/0.2")


# ─── ÉTAPE 4 — TISSUS ─────────────────────────────────────────────────────────

def create_tissus():
    # Shùkà bordeaux
    shuka = fresh_material('Mat_Shuka')
    n, l  = shuka.node_tree.nodes, shuka.node_tree.links
    out   = n.new('ShaderNodeOutputMaterial'); out.location = (250, 0)
    bsdf  = n.new('ShaderNodeBsdfPrincipled');  bsdf.location = (-100, 0)
    safe_set(bsdf, 'Base Color', COLOR['shuka'])
    safe_set(bsdf, 'Roughness', 0.6)
    safe_set(bsdf, 'Sheen Weight', 0.3)
    safe_set(bsdf, 'Transmission Weight', 0.1)   # ancien "Translucent" lin fin
    l.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    print("[MAT] Mat_Shuka · bordeaux · sheen 0.3")

    # Lin ivoire
    lin = fresh_material('Mat_Lin')
    n, l = lin.node_tree.nodes, lin.node_tree.links
    out  = n.new('ShaderNodeOutputMaterial'); out.location = (250, 0)
    bsdf = n.new('ShaderNodeBsdfPrincipled');  bsdf.location = (-100, 0)
    safe_set(bsdf, 'Base Color', COLOR['lin_ivoire'])
    safe_set(bsdf, 'Roughness', 0.65)
    safe_set(bsdf, 'Sheen Weight', 0.25)
    l.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    print("[MAT] Mat_Lin · ivoire · sheen 0.25")


# ─── ÉTAPE 5 — YEUX (émission keyframée S5) ──────────────────────────────────

def create_yeux():
    mat   = fresh_material('Mat_Yeux_Iris')
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    out  = nodes.new('ShaderNodeOutputMaterial'); out.location  = (250, 0)
    bsdf = nodes.new('ShaderNodeBsdfPrincipled');  bsdf.location = (-400, 100)
    emit = nodes.new('ShaderNodeEmission');        emit.location = (-400, -150)
    mix  = nodes.new('ShaderNodeMixShader');       mix.location  = (-50, 0)

    safe_set(bsdf, 'Base Color', COLOR['yeux'])
    safe_set(bsdf, 'Coat Weight', 0.04)   # ancien "Clearcoat"
    safe_set(bsdf, 'Roughness', 0.25)
    emit.inputs['Color'].default_value    = COLOR['yeux_emit']
    emit.inputs['Strength'].default_value = 0.0
    mix.inputs['Fac'].default_value       = 0.0

    links.new(bsdf.outputs['BSDF'],    mix.inputs[1])
    links.new(emit.outputs['Emission'], mix.inputs[2])
    links.new(mix.outputs['Shader'],   out.inputs['Surface'])

    # Keyframe éveil S5 : 0.0 (frame 1921) → 0.15 (frame 2280)
    for frame, strength, fac in [(1921, 0.0, 0.0), (2280, 0.15, 0.15)]:
        bpy.context.scene.frame_set(frame)
        emit.inputs['Strength'].default_value = strength
        emit.inputs['Strength'].keyframe_insert('default_value', frame=frame)
        mix.inputs['Fac'].default_value = fac
        mix.inputs['Fac'].keyframe_insert('default_value', frame=frame)
    bpy.context.scene.frame_set(1)
    print("[MAT] Mat_Yeux_Iris · émission keyframée 0.0→0.15 (S5)")


# ─── ÉTAPE 7 — CHEVEUX (Principled Hair) ──────────────────────────────────────

def create_cheveux():
    mat   = fresh_material('Mat_Cheveux_Naset')
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    out  = nodes.new('ShaderNodeOutputMaterial');     out.location  = (250, 0)
    hair = nodes.new('ShaderNodeBsdfHairPrincipled');  hair.location = (-100, 0)

    # La param dépend du modèle de coloration (Melanin par défaut en 4.x/5.x)
    safe_set(hair, 'Roughness', 0.6)
    safe_set(hair, 'Melanin', 0.9)
    safe_set(hair, 'Random Color', 0.03)
    # Color direct si le node est en mode "Direct coloring"
    safe_set(hair, 'Color', COLOR['cheveux'])

    links.new(hair.outputs['BSDF'], out.inputs['Surface'])
    print("[MAT] Mat_Cheveux_Naset · Principled Hair (Melanin 0.9)")

    # Empty Hair sur Naset_Body si présent
    body = bpy.data.objects.get('Naset_Body')
    if body and 'Naset_Hair_Curves' not in bpy.data.objects:
        bpy.context.view_layer.objects.active = body
        body.select_set(True)
        try:
            bpy.ops.object.curves_empty_hair_add()
            hair_obj = bpy.context.active_object
            hair_obj.name = 'Naset_Hair_Curves'
            if hair_obj.data.materials:
                hair_obj.data.materials[0] = mat
            else:
                hair_obj.data.materials.append(mat)
            print("[GROOM] Naset_Hair_Curves créé sur Naset_Body — passe en Sculpt Mode pour groomer")
        except Exception as e:
            print(f"   [!] Empty Hair non créé : {e} — ajoute-le manuellement")
    else:
        print("   [i] Naset_Body absent → crée le groom manuellement (Add > Curves > Empty Hair)")


# ─── ÉTAPE 9 — PARTICULES OR ──────────────────────────────────────────────────

def create_particules():
    name = 'Particules_Or_Emitter'
    if name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)

    bpy.ops.mesh.primitive_plane_add(size=0.5, location=(0, 0, 1.0))
    emitter = bpy.context.active_object
    emitter.name = name
    emitter.hide_render = False
    emitter.show_instancer_for_render = False

    # Système de particules (plus fiable que GN à scripter)
    bpy.ops.object.particle_system_add()
    pset = emitter.particle_systems[0].settings
    pset.name           = 'PS_Or'
    pset.count          = 300
    pset.lifetime       = 120
    pset.frame_start    = 1
    pset.frame_end      = 2280
    pset.emit_from      = 'FACE'
    pset.physics_type   = 'NEWTON'
    pset.normal_factor  = 0.02          # vélocité +Z douce
    pset.factor_random  = 0.5
    pset.particle_size  = 0.001
    pset.size_random    = 0.6
    pset.use_rotations  = True
    if hasattr(pset, 'effector_weights'):
        pset.effector_weights.gravity = 0.0   # lévitation

    mat = bpy.data.materials.get('Mat_Or_Emission')
    if mat:
        if emitter.data.materials:
            emitter.data.materials[0] = mat
        else:
            emitter.data.materials.append(mat)

    print("[PART] Particules_Or_Emitter · 300 particules · lévitation +Z")
    print("   [i] Emission strength keyframée via naset_camera_animation.py (S5 éveil)")


# ─── ÉTAPE 8 — CLOTH / COLLISION ─────────────────────────────────────────────

def setup_cloth():
    body  = bpy.data.objects.get('Naset_Body')
    drape = bpy.data.objects.get('Drape_Shuka')

    if body and not any(m.type == 'COLLISION' for m in body.modifiers):
        body.modifiers.new('Collision', 'COLLISION')
        print("[CLOTH] Collision ajoutée sur Naset_Body")
    elif not body:
        print("   [i] Naset_Body absent → ajoute Collision manuellement")

    if drape:
        cloth = next((m for m in drape.modifiers if m.type == 'CLOTH'), None)
        if not cloth:
            cloth = drape.modifiers.new('Cloth', 'CLOTH')
        cs = cloth.settings
        cs.quality           = 10
        cs.tension_stiffness  = 15
        cs.compression_stiffness = 15
        cs.bending_stiffness  = 0.5
        cs.tension_damping    = 5
        print("[CLOTH] Cloth (Cotton-like) sur Drape_Shuka · stiffness 15 · bending 0.5")
        print("   [i] Bake manuel : Physics > Cache > Bake (frames 1–240)")
    else:
        print("   [i] Drape_Shuka absent → crée le drapé puis relance setup_cloth()")


# ─── ÉTAPE 6 — RIG : ÉTAPES MANUELLES ────────────────────────────────────────

def print_manual_steps():
    print("\n──── ÉTAPES MANUELLES (non scriptables proprement) ────")
    print("RIG Rigify (Naset_Rig) :")
    print("  1. Edit > Preferences > Add-ons > activer 'Rigify'")
    print("  2. Add > Armature > Human (Meta-Rig)")
    print("  3. Renommer l'armature : Naset_Rig")
    print("  4. Edit Mode : aligner les bones sur Naset_Body (étape visuelle)")
    print("  5. Properties > Armature > Generate Rig")
    print("  6. Sélection Naset_Body puis Naset_Rig > Ctrl+P > With Automatic Weights")
    print("  Bones à vérifier : spine.001/002/003, shoulder.L/R, upper_arm.L/R, thigh.L/R")
    print("  Poses : A-Pose (Blender) · T-Pose (export UE5, Rest Pose override)")
    print("CLOTH bake : Drape_Shuka > Physics > Bake frames 1–240, puis Apply > Shape Key 'S1_Wind'")
    print("PERLES Ankh : Sphere r=0.3cm > Mat_Or_Emission > Geometry Nodes Instance on Points (hair)")
    print("────────────────────────────────────────────────────────\n")


# ─── POINT D'ENTRÉE ───────────────────────────────────────────────────────────

def main():
    print("\n━━━ N'Aset OFM · Materials + Groom + FX ━━━")
    create_peau()
    create_or()
    create_tissus()
    create_yeux()
    create_cheveux()
    create_particules()
    setup_cloth()
    print_manual_steps()
    print("━━━ Terminé ━━━\n")


main()
