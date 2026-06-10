---
description: Review du diff courant par un subagent indépendant en lecture seule (contexte frais) avant de clôturer une tâche
---

Lance le subagent `diff-reviewer` (outil Agent, `subagent_type: diff-reviewer`) pour qu'il relise le
diff de la branche courante dans un contexte frais et en lecture seule.

Transmets-lui dans le prompt :
- L'intention de la tâche en cours (ce qu'on était censé faire).
- La branche concernée.
- Tout point d'attention spécifique (script Python Blender, convention de nommage N'Aset OFM, etc.)

Quand le subagent rend ses findings :
1. Affiche-les tels quels à l'utilisateur.
2. Pour chaque finding **bloquant** ou **à corriger**, propose le correctif.
3. Ne déclare la tâche terminée qu'une fois les findings bloquants traités.

Contexte additionnel fourni par l'utilisateur (optionnel) : $ARGUMENTS
