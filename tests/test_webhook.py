POST http://localhost:5678/webhook/{{webhook_id}}/naset-pipeline
Content-Type: application/json

{
  "action": "generate_blender_script",
  "target": "skin_shader",
  "scene": "S2",
  "prompt": "Génère un shader de peau réaliste avec SSS et ornements dorés"
}