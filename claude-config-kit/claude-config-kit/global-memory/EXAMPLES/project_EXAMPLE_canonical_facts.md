---
name: project_EXAMPLE_canonical_facts
description: Modèle — les faits canoniques d'un projet que Claude ne doit jamais déformer
metadata:
  type: project
---

> EXEMPLE de mémoire `project`. C'est ainsi qu'on « grave » les vérités d'un projet pour que Claude
> ne les réinvente jamais. Crée un fichier comme celui-ci pour CHAQUE projet à faits sensibles.

Faits canoniques de {{PROJECT_NAME}} ({{PROJECT_DESC}}) :

- (Fait 1 — ex. « Le produit s'appelle exactement X, jamais Y. »)
- (Fait 2 — ex. « L'équipe est composée de A, B, C — pas de D. »)
- (Fait 3 — ex. « La valeur de référence pour Z est {{DOMAIN_CANONICAL_FACT}}. »)

**Why:** ces faits sont la vérité du projet. Les déformer (mauvais nom, mauvaise composition,
mauvais chiffre) crée des erreurs qui se propagent dans tout le contenu.

**How to apply:** consulter ces faits avant toute affirmation les concernant. En cas de doute, ne
pas inventer — demander ou sourcer. Voir [[feedback_no_invented_facts]].
