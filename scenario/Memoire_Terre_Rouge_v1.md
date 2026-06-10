# 𓂀 N'ASET OFM — La Mémoire de la Terre Rouge
**Scène narrative ancrée en Guadeloupe**
**Version :** 1.0 (fusionnée) | **Durée :** 45 secondes | **1080 frames @ 24fps**
**Pipeline :** Blender 5.0 → After Effects → Premiere Pro
**Langue :** Créole guadeloupéen + Français
**Script Blender associé :** `scripts/blender/memoire_terre_rouge_setup.py`

---

## INTENTION GLOBALE

Ce n'est pas un clip esthétique.
C'est une **transmission**.

N'Aset OFM n'est pas une guerrière qui combat.
Ici, elle est **porteuse de mémoire** — la Guadeloupe incarnée dans un corps divin.
Chaque plan est un acte de dignité.

> "On ne regarde pas N'Aset. Elle nous regarde, nous — et derrière nous, tous ceux qui ont marché avant."

---

## STRUCTURE — 6 SCÈNES / 45s

| Scène | Frames | Durée | Titre | Caméra (script) |
|-------|--------|-------|-------|-----------------|
| S1 | 1 → 168 | 0–7s | Le Sol Parle | `Cam_S1_SolMacro` (100mm) |
| S2 | 169 → 336 | 7–14s | Apparition | `Cam_S2_Apparition` (50mm) |
| S3 | 337 → 528 | 14–22s | Mémoire des Ancêtres | `Cam_S3_Memoire` (35mm) |
| S4 | 529 → 720 | 22–30s | Le Regard | `Cam_S4_Regard` (135mm) |
| S5 | 721 → 912 | 30–38s | La Force Vivante | `Cam_S5_Force` (50mm) |
| S6 | 913 → 1080 | 38–45s | Le Titre | noir/titre (post) |

> Les caméras sont **liées aux marqueurs timeline** par le script → le switch entre scènes
> se fait automatiquement à la lecture et au rendu (pas de montage caméra manuel dans Blender).

---

## VOIX OFF COMPLÈTE

> *À enregistrer d'une seule traite, flux continu, voix profonde et calme.*

```
"Tè-la ka palé…
Anba pyé nou… sé pa jis latè…
Sé memwa… sé san…
Sé vwa ki pa janmen disparèt…
Nou pa pèdi… nou té la…
Nou toujou la…
Nou sé rasin…
Nou sé flanm…"
```

**Traduction FR :**
```
"La terre parle…
Sous nos pieds… ce n'est pas juste de la terre…
C'est mémoire… c'est sang…
Ce sont des voix qui ne disparaissent jamais…
On n'a pas disparu… on était là…
On est toujours là…
Nous sommes racine…
Nous sommes flamme…"
```

---

## SCÈNE 1 — LE SOL PARLE
**Frames :** 1 → 168 | **Durée :** 0–7s

### Description Visuelle
Plan **macro** — pieds nus, sol.
La **terre rouge de Guadeloupe** (`#8B3A1A`) occupe tout le cadre.
Des pieds nus avancent **lentement** — pas de marche ordinaire, c'est un rituel.
La poussière rouge se soulève à chaque pas, retombe doucement.
Lumière : soleil en contre-jour, la terre brille.

### Voix Off
*"Tè-la ka palé…"*
→ Douce, presque chuchotée. La terre répond.

### Son
- Vent très doux de Guadeloupe
- Tambour basse — un seul battement toutes les 2s (Gwo Ka, tempo lent)
- Pas sur la terre rouge — son mat et chaud

### Intention de Mise en Scène
- **Aucun visage visible** — ce sont N'IMPORTE quels pieds guadeloupéens
- La terre rouge est un **personnage** à part entière
- Lenteur absolue — chaque grain de poussière compte
- Pas d'effets : la matière brute suffit

### Notes Techniques Blender
- Caméra : `Cam_S1_SolMacro` — **macro 100mm**, hauteur 0.10m, f/2.8
- Sol : `Sol_TerreRouge` · `Mat_TerreRouge` (terre rouge + variation sombre + bump)
- Poussière : `Particules_PoussiereRouge` — 500 particules, soulèvement lent (frames 1–168)
- Lumière : `Key_Soleil_Gwadloup` (SUN chaud) en rasant
- Grain : post-prod After Effects

---

## SCÈNE 2 — APPARITION DE N'ASET
**Frames :** 169 → 336 | **Durée :** 7–14s

### Description Visuelle
Cut sec depuis les pieds → plan **mi-corps** de N'Aset.
Elle est **immobile**, droite comme un arbre.
Drapé Shúkà rouge (`#C0392B`) + drapé ivoire (`#FAFAF0`).
L'Usekh en or (`#C9963A`) capte la lumière.
Elle regarde au loin — pas l'objectif. Elle voit **le passé derrière l'horizon**.
Le vent bouge légèrement son drapé — rien d'autre ne bouge.

### Voix Off
*"Anba pyé nou… sé pa jis latè…"*
→ Plus posée. Une vérité qu'elle sait depuis toujours.

### Son
- Le tambour Gwo Ka continue — légèrement plus présent
- Vent léger qui porte le drapé

### Intention de Mise en Scène
- N'Aset **n'arrive pas** — elle **était déjà là**
- Son immobilité = force, pas absence
- Le regard vers l'horizon = mémoire collective, pas introspection personnelle
- Elle porte l'histoire dans son corps, sans en faire de la douleur

### Notes Techniques Blender
- Caméra : `Cam_S2_Apparition` — **50mm**, hauteur yeux (1.65m), f/2.8
- `Key_Soleil_Gwadloup` : soleil chaud `#FFD580`
- `Rim_Or_Naset` : or sacré `#C9963A`, derrière droite
- Vent (à créer manuellement) : force ~0.4, latéral — drapé anime
- Bijoux `Mat_Or_Emission` : Emissive 0.15 (constant S1→S4)

---

## SCÈNE 3 — MÉMOIRE DES ANCÊTRES
**Frames :** 337 → 528 | **Durée :** 14–22s

### Description Visuelle
Plan **large**, savane guadeloupéenne.
N'Aset au centre, petite dans le cadre.
Autour d'elle : **silhouettes translucides** — hommes, femmes, enfants.
Elles n'ont pas de détails — elles sont **énergie**, pas personnages.
Couleur des silhouettes : ivoire/or lumineux, opacité 15–40%.
Apparition échelonnée → elles **étaient déjà là**, on les remarque seulement.

### Voix Off
*"Sé memwa… sé san… sé vwa ki pa janmen disparèt…"*
→ Rythme plus soutenu. Trois affirmations successives.

### Son
- Tambour Gwo Ka monte légèrement en intensité
- Harmoniques vocales graves (pad atmosphérique)

### Intention de Mise en Scène
- Les silhouettes ne sont **pas des fantômes effrayants** — elles sont **présence**
- N'Aset (corporelle, riche) vs silhouettes (lumière pure) → elle est la **jonction entre les mondes**
- Pas d'animation spectaculaire : elles ondulent très légèrement, comme de la chaleur

### Notes Techniques Blender
- Caméra : `Cam_S3_Memoire` — **35mm** grand angle, f/8
- Silhouettes : `Ancetre_01`…`Ancetre_06` · `Mat_Ancetre_Base` (Transmission 0.9 + Emission or)
- Apparition : Mix Shader Fac 0→0.6, **échelonnée** (décalage 8 frames par ancêtre, frames 380+)
- Disparition au cut S5 (frame 721)

---

## SCÈNE 4 — LE REGARD
**Frames :** 529 → 720 | **Durée :** 22–30s

### Description Visuelle
**Gros plan** serré sur les yeux de N'Aset.
Les yeux amande, le khôl noir parfait.
Dans le reflet de ses yeux : **lumière dorée** — pas un reflet réaliste, un symbole.
L'Oudjat `𓂀` se dessine très subtilement dans la lumière de l'iris.
Elle ne cligne pas. Elle **contient tout**.

### Voix Off
*"Nou pa pèdi… nou té la… nou toujou la…"*
→ Les trois plus importantes lignes. Chacune espacée. Affirmation après affirmation.

### Son
- Pause du tambour entre chaque ligne — le silence est aussi la voix
- Quand elle dit "nou toujou la" : le tambour reprend, plus fort

### Intention de Mise en Scène
- Ce plan doit **rester** longtemps — 8 secondes sur les yeux
- Le spectateur doit sentir qu'il est **regardé en retour**
- La lumière dans les yeux n'est pas magie : c'est **clarté intérieure**
- Pas d'animation du visage : la puissance vient de l'**immobilité totale**

### Notes Techniques Blender
- Caméra : `Cam_S4_Regard` — **135mm** macro, f/1.4 (tout flou sauf les yeux)
- `Mat_Yeux_Iris` : Emissive 0.0 → 0.30 sur frames 529–625 (pic sur "nou toujou la")
  → animé par `animate_yeux_s4()` ; nécessite d'avoir lancé `naset_scene_setup.py`
- Symbole Oudjat : plan en émission doré, opacité 0→0.25, centré iris (compositing AE)
- `Rim_Or_Naset` : halo or chaud `#E8BC6A` autour du visage

---

## SCÈNE 5 — LA FORCE VIVANTE
**Frames :** 721 → 912 | **Durée :** 30–38s

### Description Visuelle
**Rupture de rythme** — cut dynamique.
Femmes qui dansent le **Gwo Ka** — robes colorées, pieds dans la terre rouge.
Énergie pure. Sueur. Force ancestrale.
*Note : ces plans peuvent être des images réelles / vidéo intégrée, pas forcément 3D.*
Puis : cut brutal → **N'Aset immobile** au milieu du mouvement qui continue autour d'elle.
Elle est le **centre calme** de la tempête vivante.

### Voix Off
*"Nou sé rasin… nou sé flanm…"*
→ Les deux dernières lignes. Courtes. Définitives.

### Son
- Gwo Ka en plein — tempo fort, peau du tambour, voix
- Le cut vers N'Aset coupe TOUT le son sauf le tambour grave seul

### Intention de Mise en Scène
- Contraste maximal entre l'**explosion de vie** des danseuses et la **sérénité souveraine** de N'Aset
- Elle n'est pas au-dessus de la danse — elle **est** la danse, distillée
- "Rasin" = racine : elle est dans la terre
- "Flanm" = flamme : l'or sur elle brille en réponse

### Notes Techniques Blender/Compositing
- Caméra : `Cam_S5_Force` — **50mm**, f/4
- Plans Gwo Ka : vidéo réelle recommandée (composite AE par-dessus la scène 3D)
- Si full 3D : danseuses secondaires `Naset_Danseuse_01…06` (à créer), cycles de danse baked
- N'Aset cut : `Mat_Or_Emission` Emissive monte à 1.2 au pic "flanm" (frame 793)
  → animé par `animate_or_s5()`
- Lumière ambiante : bascule vers rouge chaud `#C0392B` + or `#C9963A`

---

## SCÈNE 6 — LE TITRE
**Frames :** 913 → 1080 | **Durée :** 38–45s

### Description Visuelle
**Fondu vers le noir** — 12 frames (0.5s).
Fond noir absolu.
Apparition du **symbole Oudjat** `𓂀` en or — lumineux, simple, centré.
Puis le texte :

```
N'ASET OFM
Mémoire Vivante — Gwadloup
```

Typographie : Noto Sans Egyptian Hieroglyphics + serif élégant.
Couleur : `#C9963A` or sacré sur noir `#000000`.
Apparition : fade in lettre par lettre ou simple dissolve.

### Son
- Fondu sonore complet
- Silence 2 secondes
- Un dernier coup de tambour grave — unique, résonnant
- Silence final

### Notes Compositing After Effects
- Fond noir : cut sec à frame 924 depuis la scène 5
- Symbole `𓂀` : font Noto Sans Egyptian, ~120pt, émission dorée, glow doux
- Titre "N'ASET OFM" : Cormorant Garamond Bold ou Trajan Pro, tracking +150
- Sous-titre "Mémoire Vivante — Gwadloup" : light, tracking +300
- Fade in titre : 1.5s dissolve · Hold 3.5s avant fade out final

---

## PALETTE COULEUR DE CETTE SCÈNE

| Couleur | Hex | Rôle dans le récit |
|---------|-----|-------------------|
| Terre rouge | `#8B3A1A` | Guadeloupe · Ancêtres · Sol |
| Or sacré | `#C9963A` | N'Aset · Mémoire divine |
| Rouge Shúkà | `#C0392B` | Vie · Force · Gwo Ka |
| Blanc ivoire | `#FAFAF0` | Silhouettes · Lumière ancestrale |
| Noir absolu | `#000000` | Titre · Silence · Espace sacré |
| Lumière soleil | `#FFD580` | Guadeloupe · Chaleur |

---

## AMBIANCE SONORE — TIMELINE

| Frame | Son |
|-------|-----|
| 1 | Vent léger · Tambour Gwo Ka très bas |
| 1–168 | Pas sur terre rouge · Poussière |
| 169 | Cut son pur → ambiance savane |
| 337 | Harmoniques vocales graves entrent |
| 529 | Silence entre les lignes de voix off |
| 625 | Tambour reprend fort sur "nou toujou la" |
| 721 | Gwo Ka plein — énergie maximale |
| 793 | Cut → tambour seul grave |
| 912 | Fondu sonore vers silence |
| 936 | Silence complet |
| 1032 | Un coup de tambour grave unique |
| 1080 | Silence final |

---

## CORRESPONDANCE SCRIPT BLENDER

Ce que `memoire_terre_rouge_setup.py` crée **automatiquement** :

| Élément | Nom dans Blender |
|---------|------------------|
| Sol terre rouge | `Sol_TerreRouge` · `Mat_TerreRouge` |
| Placeholder perso | `Naset_Body` (cylindre — à remplacer) |
| Silhouettes ancêtres | `Ancetre_01`…`Ancetre_06` · `Mat_Ancetre_Base` |
| Caméras (liées marqueurs) | `Cam_S1_SolMacro` … `Cam_S5_Force` |
| Lumières | `Key_Soleil_Gwadloup`, `Fill_Ciel`, `Rim_Or_Naset` |
| Poussière | `Particules_PoussiereRouge` · `Mat_PoussiereRouge` |
| Or sacré | `Mat_Or_Emission` (animé S5) |

À faire **manuellement** (hors script) :
- Importer le vrai `Naset_Body` + lancer `naset_scene_setup.py` (→ `Mat_Yeux_Iris` pour les yeux dorés S4)
- Créer le vent du drapé S2
- Danseuses Gwo Ka S5 (ou vidéo réelle en composite AE)
- Symbole `𓂀` + titre S6 (After Effects)

---

## CONNEXION AU PROJET N'ASET OFM

Cette scène ajoute une **dimension géographique et historique** à l'univers OFM :

- N'Aset n'est plus seulement prêtresse de l'Égypte ancienne
- Elle est aussi **mémoire de la Guadeloupe** — les deux se rejoignent
- L'Ordre du Feu Mystique traverse les continents et les siècles
- La terre rouge guadeloupéenne = les sables dorés égyptiens = même sacré

> **N'Aset OFM : née à Memphis. Enracinée à Gwadloup. Vivante partout.**

---

*𓂀 Scénario Mémoire Terre Rouge v1.0 (fusionné) · Négus Dja · Ordre du Feu Mystique · Guadeloupe*
