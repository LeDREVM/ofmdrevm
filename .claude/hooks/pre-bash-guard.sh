#!/usr/bin/env bash
# Hook: pre-bash-guard  [UNIVERSEL]
# PreToolUse:Bash — refuse (exit 2) les commandes destructives AVANT exécution.

input=$(cat)

command=$(echo "$input" | python3 -c "import json, sys
try:
    data = json.load(sys.stdin)
    print(data.get('tool_input', {}).get('command', ''))
except Exception:
    print('')
" 2>/dev/null || echo "")

[ -z "$command" ] && exit 0

block() {
  echo "[pre-bash-guard] BLOQUÉ : $1" >&2
  echo "  Commande refusée : $command" >&2
  echo "  Si c'est vraiment voulu, lance-la toi-même dans ton terminal (hors Claude Code)." >&2
  exit 2
}

# 1) rm récursif visant la racine, le home, un wildcard global ou un chemin système
if echo "$command" | grep -qE '(^|[[:space:]])(sudo[[:space:]]+)?rm[[:space:]]' \
   && echo "$command" | grep -qE '[[:space:]]-[a-zA-Z]*[rR]|--recursive'; then
  if echo "$command" | grep -qE '[[:space:]](/|~|\$HOME)([[:space:]]|$)' \
     || echo "$command" | grep -qE '[[:space:]]/\*' \
     || echo "$command" | grep -qE '[[:space:]]\*([[:space:]]|$)' \
     || echo "$command" | grep -qE '[[:space:]]/(bin|boot|dev|etc|lib|proc|root|sbin|sys|usr|var|System|Library)([[:space:]]|/|$)'; then
    block "rm récursif sur la racine, le home ou un chemin système"
  fi
fi

# 2) git push vers main/master interdit
if echo "$command" | grep -qE '(^|[[:space:]])git[[:space:]]+push([[:space:]]|$)'; then
  if echo "$command" | grep -qE '([[:space:]]|:|/)(main|master)([[:space:]]|:|$)'; then
    if echo "$command" | grep -qE '(--force([[:space:]]|=|$)|[[:space:]]-f([[:space:]]|$))'; then
      block "git push --force sur main/master"
    fi
    block "git push direct sur main/master — passe par une branche puis un merge/PR"
  fi
  cur=$(cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null && git rev-parse --abbrev-ref HEAD 2>/dev/null)
  if [ "$cur" = "main" ] || [ "$cur" = "master" ]; then
    block "push depuis la branche « $cur » interdit"
  fi
fi

# 3) Redirection vers un répertoire système
if echo "$command" | grep -qE '>>?[[:space:]]*/( bin|boot|etc|lib|proc|root|sbin|sys|usr|var|System|Library)(/|[[:space:]]|$)'; then
  block "écriture redirigée vers un répertoire système"
fi

# 4) dd sur device disque
if echo "$command" | grep -qE 'dd[[:space:]]+.*of=/dev/(disk|sd|rdisk|nvme|mmcblk)'; then
  block "dd écrivant directement sur un disque"
fi

# 5) fork bomb
if echo "$command" | grep -qE ':[[:space:]]*\(\)[[:space:]]*\{[[:space:]]*:[[:space:]]*\|[[:space:]]*:'; then
  block "fork bomb"
fi

# 6) pipe direct d'un script distant vers un shell
if echo "$command" | grep -qE '(curl|wget)[[:space:]].*\|[[:space:]]*(sudo[[:space:]]+)?(ba|z)?sh([[:space:]]|$)'; then
  block "exécution directe d'un script distant"
fi

exit 0
