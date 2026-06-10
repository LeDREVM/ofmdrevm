---
description: Fait critiquer le plan courant par un subagent « directeur artistique sceptique » en lecture seule, avant toute implémentation
---

Avant d'implémenter, fais relire le plan par le subagent `plan-reviewer` (outil Agent,
`subagent_type: plan-reviewer`).

Transmets-lui dans le prompt :
- Le plan complet tel qu'il existe (étapes, fichiers visés, décisions).
- La demande d'origine (le besoin réel à satisfaire).
- Les contraintes N'Aset OFM pertinentes (conventions de nommage, palette officielle, invariants du personnage).

Quand il rend sa revue :
1. Affiche-la telle quelle à l'utilisateur.
2. Adresse chaque point **🔴 Bloquant** dans le plan.
3. N'implémente qu'une fois les bloquants traités et le plan validé.

Plan ou contexte fourni par l'utilisateur (optionnel) : $ARGUMENTS
