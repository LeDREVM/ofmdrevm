#!/usr/bin/env bash
# Hook: context-pin  [UNIVERSEL]
# SessionStart matcher "compact" — après une compaction du contexte, ré-injecte
# les invariants critiques du projet (CONTEXT_PIN.md à la racine).

cat >/dev/null  # vider le JSON d'event sur stdin

project_dir="${CLAUDE_PROJECT_DIR:-$(pwd)}"
pin="$project_dir/CONTEXT_PIN.md"

[ -f "$pin" ] || exit 0

echo "=== INVARIANTS CRITIQUES PROJET (ré-injectés après compaction) ==="
cat "$pin"
exit 0
