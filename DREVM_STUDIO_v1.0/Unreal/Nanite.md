# Unreal — Nanite (géométrie DREVM)

## Quoi activer

| Asset | Nanite | Pourquoi |
|---|---|---|
| Temple (piliers, dalles, ruines) | ✅ | statique dense — le cas d'école |
| Sol savane displacé | ✅ | millions de tris sans LOD à gérer |
| Acacias silhouettes | ✅ si mesh · ✗ si cartes alpha | masked = coût Nanite inutile |
| `SK_NasetOFM` (personnage) | ✗ | skeletal — pipeline classique + LODs |
| Drapés cloth simulés | ✗ | déformation dynamique |
| Végétation à cartes alpha | ✗ | overdraw masked > gain Nanite |

Activation : Static Mesh Editor > Details > Nanite Settings > Enable ✓
(ou clic droit sur une sélection d'assets > Nanite > Enable).

## Réglages DREVM
- **Keep Triangle Percent** : 100 % (le temple est le décor héro)
- **Fallback Relative Error** : 1.0 — le fallback ne sert qu'aux reflets
  Lumen, inutile de le raffiner
- Displacement sol : importer le mesh déjà displacé de Blender (GN appliqué),
  Nanite digère — pas de tessellation runtime

## Pièges
- Nanite ignore le Vertex Paint animé — les hiéroglyphes qui s'allument
  passent par un Material Parameter (scalar `EmissiveStrength`), pas par la géo
- Un mesh Nanite avec matériau Translucent tombe en fallback silencieux →
  les drapés translucides du contre-jour restent NON-Nanite
- Vérifier le budget : `stat nanite` — triangle count visible < 25 M sur la
  scène temple complète
