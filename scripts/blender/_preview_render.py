"""Rendu preview rapide pour vérifier l'import (headless)."""
import bpy
sc = bpy.context.scene
sc.render.resolution_x = 720
sc.render.resolution_y = 720
sc.render.resolution_percentage = 100
sc.cycles.samples = 16
sc.cycles.use_denoising = True
sc.render.image_settings.file_format = 'PNG'
sc.render.filepath = "C:/Users/ardja/Documents/CODING/Blendaah/ofmdrevm/.claude/worktrees/awesome-bose-7c4dc5/preview_character.png"
print("Caméra :", sc.camera.name if sc.camera else "AUCUNE")
bpy.ops.render.render(write_still=True)
print("Preview rendue.")
