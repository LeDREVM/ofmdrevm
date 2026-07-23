"""
create_world_shader.py — DREVM Studio
Cree les 3 mondes DREVM et applique celui demande :
    World_Sunset_Naset — couchant dore, soleil rasant (court metrage N'Aset)
    World_Night_Luna   — nuit indigo etoilee sans lune (serie Luna)
    World_Studio       — gris neutre pour lookdev matieres

apply_world('night') / apply_world('sunset') / apply_world('studio')
Compatible Blender 5.0 : sky_type MULTIPLE_SCATTERING (NISHITA supprime).
"""

import bpy
import math


def hex_to_linear(hex_str):
    h = hex_str.lstrip('#')
    rgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
                 for c in rgb) + (1.0,)


NUIT = hex_to_linear('#1C1A3A')


def _fresh_world(name):
    world = bpy.data.worlds.get(name) or bpy.data.worlds.new(name)
    world.use_nodes = True
    world.node_tree.nodes.clear()
    return world


def create_sunset():
    """Ciel physique couchant — contre-jour dore N'Aset."""
    world = _fresh_world('World_Sunset_Naset')
    nt = world.node_tree
    sky = nt.nodes.new('ShaderNodeTexSky')
    sky.sky_type = 'MULTIPLE_SCATTERING'  # Blender 5.0
    for attr, val in [('sun_elevation', math.radians(4.0)),
                      ('sun_rotation', math.radians(180.0)),
                      ('sun_intensity', 0.35),
                      ('dust_density', 4.0)]:
        if hasattr(sky, attr):
            setattr(sky, attr, val)
    bg = nt.nodes.new('ShaderNodeBackground')
    bg.inputs['Strength'].default_value = 0.6
    out = nt.nodes.new('ShaderNodeOutputWorld')
    nt.links.new(sky.outputs['Color'], bg.inputs['Color'])
    nt.links.new(bg.outputs['Background'], out.inputs['Surface'])
    return world


def create_night():
    """Nuit Luna : indigo profond + etoiles procedurales (noise fin)."""
    world = _fresh_world('World_Night_Luna')
    nt = world.node_tree

    # Etoiles : noise haute frequence -> seuil dur -> points blancs
    coords = nt.nodes.new('ShaderNodeTexCoord')
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 900.0
    noise.inputs['Detail'].default_value = 0.0
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.88   # seuil : ~2% de points
    ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    ramp.color_ramp.elements[1].position = 0.92
    ramp.color_ramp.elements[1].color = hex_to_linear('#E8E8F0')

    # Fond indigo + etoiles additionnees
    mix = nt.nodes.new('ShaderNodeMix')
    mix.data_type = 'RGBA'
    mix.blend_type = 'ADD'
    mix.inputs['Factor'].default_value = 1.0
    mix.inputs[6].default_value = tuple(c * 0.35 for c in NUIT[:3]) + (1.0,)

    bg = nt.nodes.new('ShaderNodeBackground')
    bg.inputs['Strength'].default_value = 1.0
    out = nt.nodes.new('ShaderNodeOutputWorld')

    nt.links.new(coords.outputs['Generated'], noise.inputs['Vector'])
    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], mix.inputs[7])
    nt.links.new(mix.outputs[2], bg.inputs['Color'])
    nt.links.new(bg.outputs['Background'], out.inputs['Surface'])
    return world


def create_studio():
    """Gris 18% uniforme — lookdev."""
    world = _fresh_world('World_Studio')
    nt = world.node_tree
    bg = nt.nodes.new('ShaderNodeBackground')
    bg.inputs['Color'].default_value = (0.18, 0.18, 0.18, 1.0)
    bg.inputs['Strength'].default_value = 1.0
    out = nt.nodes.new('ShaderNodeOutputWorld')
    nt.links.new(bg.outputs['Background'], out.inputs['Surface'])
    return world


WORLDS = {'sunset': create_sunset, 'night': create_night, 'studio': create_studio}


def apply_world(key='night'):
    world = WORLDS[key]()
    bpy.context.scene.world = world
    print(f"[WORLD] Actif : {world.name}")
    return world


def main(active='night'):
    print("\n━━━ DREVM Studio · World Shaders ━━━")
    for creator in WORLDS.values():
        creator()          # cree les 3, disponibles dans le dropdown
    apply_world(active)
    print("━━━ 3 mondes crees ━━━\n")


main()
