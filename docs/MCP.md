# 𓂀 MCP — Serveurs Model Context Protocol · N'Aset OFM

Guide de configuration des serveurs **MCP** (Model Context Protocol) utilisés par
Claude Code sur le projet N'Aset OFM. Le MCP permet à l'agent de piloter des
services externes (génération d'images, pipeline n8n, déploiement Netlify…)
directement depuis la conversation, via des outils standardisés.

> **En bref** — un serveur MCP = un pont vers un service. Une fois déclaré dans
> `.mcp.json` et autorisé, Claude Code expose ses outils (préfixés `mcp__<serveur>__…`)
> et peut les appeler pour toi.

---

## 1. Fichiers de configuration

| Fichier | Rôle | Versionné ? |
|---------|------|-------------|
| `.mcp.json` | **Config réelle** avec les clés/API. Lue par Claude Code. | ❌ **Non** (gitignoré — contient des secrets) |
| `.mcp.json.example` | **Modèle** à copier. Aucune clé en dur. | ✅ Oui |
| `.claude/settings.json` | Active les serveurs via `enabledMcpjsonServers`. | ✅ Oui |
| `.env` | Valeurs des clés (`HIGGSFIELD_API_KEY`, etc.). | ❌ Non (gitignoré) |
| `.env.example` | Modèle des variables d'environnement. | ✅ Oui |

**Convention projet** — exactement comme `.env` : on ne commit **jamais** `.mcp.json`.
On versionne le modèle `.mcp.json.example`, chacun le copie et le remplit en local.

---

## 2. Installation (première fois)

```bash
# 1. Copier les modèles
cp .mcp.json.example .mcp.json
cp .env.example .env

# 2. Remplir les clés dans .env
#    HIGGSFIELD_API_KEY=...
#    N8N_HOST=... / N8N_API_KEY=...
#    NETLIFY_AUTH_TOKEN=...

# 3. Vérifier que les serveurs sont chargés
claude mcp list
```

Dans `.claude/settings.json`, la clé `enabledMcpjsonServers` liste les serveurs
autorisés à démarrer automatiquement :

```json
"enabledMcpjsonServers": ["higgsfield"]
```

> Pour activer d'autres serveurs (n8n, netlify…), ajoute leur nom à cette liste,
> ou lance-les à la demande. Au premier appel d'un outil MCP, Claude Code demande
> une **autorisation** — c'est normal.

---

## 3. Serveurs du pipeline N'Aset OFM

### 𓅃 higgsfield — Génération image / vidéo / 3D / audio

Cœur créatif du projet. Serveur **distant** (HTTP).

| Champ | Valeur |
|-------|--------|
| Type | `http` |
| URL | `https://mcp.higgsfield.ai/mcp` |
| Auth | En-tête `Authorization: Bearer ${HIGGSFIELD_API_KEY}` |
| Clé `.env` | `HIGGSFIELD_API_KEY` |

**Usage N'Aset** — génération des plans du court métrage, moodboards, textures,
assets 3D (image-to-3D), audio (Seed Audio). Voir les skills `higgsfield-*`
(`.claude/skills/`) qui s'appuient sur ce serveur.

```json
"higgsfield": {
  "type": "http",
  "url": "https://mcp.higgsfield.ai/mcp",
  "headers": { "Authorization": "Bearer ${HIGGSFIELD_API_KEY}" }
}
```

---

### 🔄 n8n — Pipeline d'automatisation AI

Orchestration des workflows de production (`workflows/*.json`). Instance
**auto-hébergée**.

| Champ | Valeur |
|-------|--------|
| Type | `sse` |
| URL | webhook du node **MCP Server Trigger** de ton instance (ex. `${N8N_HOST}/mcp/naset-pipeline/sse`) |
| Auth | `Authorization: Bearer ${N8N_API_KEY}` |
| Clés `.env` | `N8N_HOST`, `N8N_API_KEY`, `N8N_WEBHOOK_URL` |

> Pré-requis : ajouter un node **MCP Server Trigger** dans le workflow n8n
> cible ; son URL SSE devient l'`url` ci-dessus.

**Usage N'Aset** — piloter/déclencher les pipelines `NasetOFM_Story_Pipeline`,
`NasetOFM_AI_Pipeline`, `naset_ofm_pipeline`. Permet à Claude de construire,
valider et exécuter des workflows n8n.

---

### 🌐 netlify — Déploiement des sites statiques

Publie les livrables HTML (dashboard, moodboard, prompts Higgsfield).

| Champ | Valeur |
|-------|--------|
| Type | `stdio` (`npx -y @netlify/mcp`) |
| Auth | Variable `NETLIFY_AUTH_TOKEN` |
| Clés `.env` | `NETLIFY_AUTH_TOKEN`, `NETLIFY_SITE_ID` |

**Usage N'Aset** — déployer `naset_dashboard.html`, `docs/NasetOFM_Moodboard.html`,
`naset_higgsfield_prompts.html`. Le `netlify.toml` définit déjà le build ;
`NETLIFY_SITE_ID` est dans `.env.example`.

---

### 📁 google-drive — Assets sources

Lecture et dépôt des médias lourds (renders EXR, textures 4K, exports FBX)
non versionnés dans Git.

| Champ | Valeur |
|-------|--------|
| Type | `stdio` (`npx -y @modelcontextprotocol/server-gdrive`) |
| Auth | OAuth Google — créer un projet Google Cloud, activer l'API Drive, exporter les identifiants OAuth, puis authentifier au premier lancement |

**Usage N'Aset** — récupérer/archiver les fichiers de production qui restent
hors du dépôt (voir conventions de nommage dans `CLAUDE.md`).

---

## 4. Serveurs optionnels (hors pipeline)

Serveurs disponibles selon l'environnement Claude Code, non nécessaires à la
production N'Aset mais parfois utiles :

| Serveur | Usage possible |
|---------|----------------|
| **github** | PR, issues, revue de code sur `ledrevm/ofmdrevm` |
| **supabase** | Base de données (si backend web ajouté) |
| **vercel** | Analytics web (alternative Netlify) |
| **three.js** | Prévisualisation 3D dans le navigateur |

Ces serveurs ne figurent pas dans `.mcp.json.example` — ajoute-les seulement si
un besoin concret apparaît, pour garder la config minimale.

---

## 5. Dépannage

| Symptôme | Cause probable | Solution |
|----------|----------------|----------|
| Outils `mcp__higgsfield__*` absents | `.mcp.json` manquant ou serveur non activé | `cp .mcp.json.example .mcp.json` + vérifier `enabledMcpjsonServers` |
| Erreur 401 / auth | Clé absente ou expirée dans `.env` | Régénérer la clé, mettre à jour `.env` |
| `npx` échoue (netlify/drive) | Paquet non trouvé / réseau | Vérifier Node.js installé, relancer |
| Serveur distant ne répond pas | URL / proxy | Tester l'URL, vérifier la connexion |
| Secrets commités par erreur | `.mcp.json` ajouté au suivi | Il est gitignoré — ne jamais forcer son ajout |

**Commandes utiles :**

```bash
claude mcp list          # serveurs chargés + statut
claude mcp get higgsfield  # détail d'un serveur
```

---

## 6. Règles de sécurité

- ❌ **Jamais** de clé API en dur dans un fichier versionné (`.mcp.json.example`,
  docs, scripts). Toujours via `${VARIABLE}` référençant `.env`.
- ❌ Ne jamais commit `.mcp.json`, `.env`, `credentials.json` — déjà dans `.gitignore`.
- ✅ Après appel d'un service externe, garder à l'esprit que les données envoyées
  peuvent être mises en cache côté fournisseur.
- ✅ Autoriser au coup par coup les nouveaux serveurs, ne pas tout activer par défaut.

---

*𓂀 MCP · Ordre du Feu Mystique · Négus Dja · Gwadloup*
