# 🔌 Plugins / Add-ons Blender — N'Aset OFM

C'est **ici que tu déposes tes plugins Blender** (que Blender appelle « add-ons »).

---

## Deux formats possibles

| Format | À quoi ça ressemble | Où le mettre |
|--------|---------------------|--------------|
| **Fichier simple** | `mon_plugin.py` | directement dans `addons/` |
| **Plugin en dossier** | `mon_plugin/` contenant `__init__.py` | un sous-dossier dans `addons/` |

> Un add-on Blender = un script Python qui contient un dictionnaire `bl_info` en haut.
> C'est ce `bl_info` qui le fait apparaître dans la liste des add-ons de Blender.

---

## Installer un plugin dans Blender (2 méthodes)

### Méthode A — Installation classique (la plus simple)
1. Blender → **Édition → Préférences → Add-ons**
2. Bouton **Installer…** (en haut à droite)
3. Choisis le fichier `.py` (ou le `.zip` du plugin) depuis ce dossier `addons/`
4. Coche la case pour l'**activer**

### Méthode B — Charger tout le dossier `addons/` automatiquement (pour le dev)
Pratique quand tu développes plusieurs plugins : tu pointes Blender vers ce dossier une seule fois.
1. Blender → **Édition → Préférences → Système (File Paths) → Scripts**
2. Mets le chemin du **dossier parent** :
   `C:\Users\ardja\Documents\CODING\Blendaah\ofmdrevm\scripts_blender_root\`
   *(voir note ci-dessous)*
3. Redémarre Blender → tous les plugins du sous-dossier `addons/` apparaissent dans la liste

> **Note :** Blender cherche les add-ons dans `<chemin_scripts>/addons/`.
> Donc si tu pointes File Paths → Scripts vers la **racine du projet**, Blender lira automatiquement ce dossier `addons/`. C'est déjà la bonne structure.

---

## Différence plugin vs script

- **Plugin (add-on)** → s'installe, s'active, ajoute des boutons/menus permanents dans Blender. Reste actif entre les sessions. → **ce dossier `addons/`**
- **Script** → se lance une fois à la demande (Alt+P dans l'éditeur de texte), fait son travail, c'est fini. → dossier `scripts/blender/`

---

## Squelette minimal d'un add-on (à copier pour démarrer)

```python
bl_info = {
    "name": "Mon Plugin Naset",
    "author": "Negus Dja",
    "version": (1, 0),
    "blender": (5, 0, 0),
    "category": "Object",
    "description": "Ce que fait le plugin",
}

import bpy

class NASET_OT_exemple(bpy.types.Operator):
    bl_idname = "naset.exemple"
    bl_label  = "Action Naset"

    def execute(self, context):
        self.report({'INFO'}, "Plugin Naset exécuté")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(NASET_OT_exemple)

def unregister():
    bpy.utils.unregister_class(NASET_OT_exemple)

if __name__ == "__main__":
    register()
```

> ⚠️ Blender 5.0 : vérifie les pièges API avant de coder un plugin
> (voir la fiche mémoire `reference_blender5_api_gotchas`).

---

*𓂀 Dossier plugins · N'Aset OFM · Négus Dja*
