#!/usr/bin/env bash
# Hook: pre-edit-guard  [N'Aset OFM]
# PreToolUse:Edit|Write|MultiEdit — protège les secrets (clés Meshy AI, .env)
# et les fichiers de rendu générés.

input=$(cat)

file_path=$(echo "$input" | python3 -c "import json, sys
try:
    data = json.load(sys.stdin)
    print(data.get('tool_input', {}).get('file_path', ''))
except Exception:
    print('')
" 2>/dev/null || echo "")

[ -z "$file_path" ] && exit 0
base=$(basename "$file_path")

# Templates explicitement autorisés
case "$base" in
  *.example|*.sample|*.example.*|*.sample.*|*.template|*.dist) exit 0 ;;
esac

block() {
  echo "[pre-edit-guard] BLOQUÉ : $file_path" >&2
  echo "  Ce fichier peut contenir des secrets — Claude Code ne doit pas l'éditer." >&2
  echo "  Si tu dois le modifier, fais-le toi-même dans ton éditeur." >&2
  exit 2
}

# Fichiers d'environnement / secrets
case "$base" in
  .env|.env.*|.dev.vars|.dev.vars.*) block ;;
esac

# Clés privées / certificats
echo "$base" | grep -qiE '\.(pem|key|p12|pfx|keystore|jks|asc|gpg)$' && block

# Noms évoquant des secrets
echo "$base" | grep -qiE '(^|[._-])(secret|secrets|credential|credentials|passwd)([._-]|\.|$)' && block

# Clés SSH
case "$base" in
  id_rsa|id_dsa|id_ecdsa|id_ed25519) block ;;
esac

exit 0
