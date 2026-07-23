# 𓂀 N'Aset OFM — Divine Maasaï

Projet personnage 3D + court métrage spirituel. Pipeline **Blender 5.0 → Unreal Engine 5 → After Effects → Premiere Pro**.
Univers OFM (Ordre du Feu Mystique). Par Négus Dja · Guadeloupe.

---

## 📁 Structure du dossier

```
ofmdrevm/
│
├── addons/              🔌 TES PLUGINS BLENDER (add-ons) — voir addons/README.md
│
├── scripts/             ⚙️ Scripts d'automatisation (lancés à la demande)
│   ├── blender/         · setup scène, caméras, rendu, animation
│   ├── unreal/          · sequencer UE5
│   ├── import_workflow.py
│   └── run_production.py
│
├── scenario/            🎬 Scénarios narratifs (descriptions + mise en scène)
│
├── docs/                📖 Documentation, guides, moodboard, character DB
│
├── assets/              🎨 Médias sources
│   └── images/          · visuels, références
│
├── workflows/           🔄 Pipelines n8n (automatisation AI)
│
├── memory/              🧠 Mémoire projet (faits canoniques, glossaire)
│
├── tests/               ✅ Tests Python
│
├── CLAUDE.md            · contexte de travail pour l'agent
├── TASKS.md             · liste de tâches (système productivité)
├── dashboard.html       · tableau de bord visuel
├── requirements.txt     · dépendances Python
└── LICENSE
```

---

## 🚀 Démarrage rapide

| Je veux… | Où aller |
|----------|----------|
| **Ajouter un plugin Blender** | `addons/` (lire `addons/README.md`) |
| Lancer un script d'auto dans Blender | `scripts/blender/` → ouvrir dans l'éditeur de texte → Alt+P |
| Comprendre une scène du court métrage | `scenario/` |
| Voir les couleurs / conventions du perso | `CLAUDE.md` ou `memory/projects/naset-ofm.md` |
| Paramètres techniques par scène | `docs/reference_scenes.md` |
| **Configurer les serveurs MCP** (Higgsfield, n8n, Netlify…) | `docs/MCP.md` |

---

## 🔌 Serveurs MCP

Claude Code pilote les services externes du pipeline (Higgsfield, n8n, Netlify,
Google Drive) via des **serveurs MCP**. La config réelle `.mcp.json` contient des
clés API et n'est **pas** versionnée — copier le modèle et remplir `.env` :

```bash
cp .mcp.json.example .mcp.json
cp .env.example .env   # puis remplir les clés
```

→ Guide complet : **`docs/MCP.md`**

---

## ⚠️ Blender 5.0

La stack utilise **Blender 5.0.1**. Certains attributs de l'API Python ont changé
(enum `look`, `blend_method` supprimé, inputs Principled renommés).
→ fiche complète : mémoire `reference_blender5_api_gotchas`.

---

## 🎨 Identité (rappel)

- **Personnage :** N'Aset OFM — Prêtresse Égyptienne Futuriste, Divine Maasaï
- **Or sacré :** `#C9963A` · **Rouge Shúkà :** `#C0392B` · **Peau :** `#6B3D2E`
- **Render :** 4K · 24fps · Cycles GPU · Filmic Medium High Contrast

*𓂀 Ordre du Feu Mystique · Négus Dja · Gwadloup*
