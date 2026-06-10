# 𓂀 N'ASET OFM — Scénario Court Métrage
**Version :** 1.0  
**Durée :** 95 secondes · 2280 frames · 24fps  
**Format :** 4K · Cycles GPU · Filmic Medium High Contrast  
**Pipeline :** Blender 5.0 → UE5 → After Effects → Premiere Pro

---

## SYNOPSIS

Dans une savane hors du temps, une silhouette se tient immobile face à l'horizon.  
Ce n'est pas une femme. C'est une gardienne.  
N'Aset — Prêtresse de l'Ordre du Feu Mystique — s'éveille pour la dernière fois avant le combat.  
Aucun dialogue. Aucun bruit inutile. Seulement la lumière, le vent, et la puissance qui monte.

---

## SCÈNE 1 — L'APPARITION
**Frames :** 1 → 240 | **Durée :** 0 – 10s | **Caméra :** 35mm fixe

### Description Visuelle
Le cadre s'ouvre sur une savane dorée à l'heure du crépuscule.  
L'herbe haute ondule sous un vent lent et régulier.  
Au centre du plan, **de dos**, une silhouette féminine élancée.  
Le drapé blanc ivoire (`#FAFAF0`) et le Shúkà rouge (`#C0392B`) bougent avec le vent.  
Des **particules dorées** (`#C9963A`) flottent autour d'elle, presque imperceptibles.  
On ne voit pas son visage. On ne doit pas encore.

### Intention de Mise en Scène
- Silence total — pas de musique, seulement le vent
- Les particules sont là depuis toujours — elles ne s'animent pas, elles *sont*
- La silhouette ne bouge pas. C'est le monde qui bouge autour d'elle
- Lumière : soleil rasant derrière elle, contre-jour franc, silhouette quasi-noire sur or

### Notes Techniques
- Caméra : 35mm, focale large pour montrer l'espace
- Depth of field : f/8 — tout net, savane comprise
- Lumière : `Key_Light` en contre-jour bas (angle 15°), intensité 800W
- Wind : `Wind_Scene1` force 0.3 → 0.6 (rampe douce sur 240 frames)
- Particules : `Particules_Or_Emitter` émission basse, drift passif

---

## SCÈNE 2 — L'APPROCHE
**Frames :** 241 → 960 | **Durée :** 10 – 40s | **Caméra :** 50mm dolly in

### Description Visuelle
La caméra commence à avancer lentement vers elle — un travelling avant, presque rituel.  
On commence à voir ses **épaules**, les **broderies dorées** sur le drapé.  
L'Usekh (collier pectoral) capte la lumière. Un éclat d'or bref.  
La lumière rasante modèle son dos, révèle la texture du lin égyptien.  
Les particules dorées deviennent légèrement plus nombreuses, comme si sa présence les attirait.  
À 30s (frame ~720), on devine le profil droit de son visage — pas encore le regard.

### Intention de Mise en Scène
- Le travelling doit être **imperceptible** au début — on réalise qu'on avance seulement à mi-chemin
- Pas de coupes — plan séquence continu depuis S1
- La lumière commence à passer de contre-jour pur à lumière latérale gauche
- Ambiance : curiosité sacrée — le spectateur veut voir mais n'a pas encore le droit

### Notes Techniques
- Caméra : 50mm, dolly in de 8m sur 720 frames (0.011m/frame)
- DOF : f/2.8, focus sur `Naset_Body`, bokeh arrière sur savane
- `Key_Light` tourne progressivement de 180° → 135° (contre-jour → latéral)
- `Fill_Light` entre à frame 400 : intensité 80W, côté gauche, lumière chaude
- Émission bijoux `Mat_Or_Emission` : Emissive keyframe 0.0 → 0.2 entre frames 500–720

---

## SCÈNE 3 — LE REGARD
**Frames :** 961 → 1440 | **Durée :** 40 – 60s | **Caméra :** 85mm fixe

### Description Visuelle
La caméra se fixe. On est maintenant face à elle — ou presque.  
**Plan buste**, 85mm serré. Le visage de N'Aset occupe 60% du cadre.  
Les yeux amande (`#1A0D00`) regardent droit devant — pas l'objectif, mais au-delà.  
Le Khôl noir parfait. Les lèvres bordeaux (`#7B2D2D`) légèrement closes.  
Elle ne cligne pas. Elle *voit* quelque chose que nous ne voyons pas.  
**Silence absolu.** Même le vent s'est arrêté.

### Intention de Mise en Scène
- Le plan le plus long, le plus immobile — 20 secondes sans mouvement de caméra
- Ce silence est une présence, pas un vide
- Les particules s'arrêtent de dériver — elles restent suspendues dans l'air
- La lumière est frontale et douce — comme si elle venait d'elle-même
- Le spectateur doit ressentir qu'il est **évalué**, pas qu'il regarde

### Notes Techniques
- Caméra : 85mm fixe, hauteur yeux (1.65m), légère plongée 5°
- DOF : f/1.8, focus sur `Mat_Yeux_Iris`, tout le reste en bokeh
- `Key_Light` frontal doux, angle 30°, intensité 400W, température 5500K
- `Rim_Light` derrière : or chaud `#C9963A`, intensité 200W
- Particules figées : `Particules_Or_Emitter` velocity keyframe → 0.0 à frame 961
- Vent : `Wind_Scene1` force keyframe → 0.0 à frame 961

---

## SCÈNE 4 — LA DESCENTE
**Frames :** 1441 → 1920 | **Durée :** 60 – 80s | **Caméra :** 85mm, léger zoom in

### Description Visuelle
Les **yeux de N'Aset se ferment** — lentement, avec une gravité souveraine.  
La scène passe en **slow motion** — le temps se dilate.  
Les cheveux bougent imperceptiblement (un souffle invisible).  
L'Usekh capte une lumière plus intense — comme si quelque chose se préparait.  
Une légère **émission commence dans ses yeux** : un or très discret sous les paupières fermées.  
Les particules autour d'elle descendent d'un millimètre — et remontent.  
Ce n'est pas une fin. C'est une concentration.

### Intention de Mise en Scène
- Slow motion ≠ effets spectaculaires — c'est une dilatation intérieure
- L'émission des yeux doit être à peine visible à l'œil nu — on *ressent* plus qu'on ne *voit*
- La musique (si présente) atteint son point de tension maximum ici — mais ne l'explose pas encore
- Le spectateur retient son souffle

### Notes Techniques
- Caméra : 85mm, zoom in subtil f/1.8 → f/1.4 sur 480 frames
- Animation yeux : keyframe paupières ouvertes → fermées entre frames 1441–1600 (6.6s)
- Slow motion : interpolation clé → ralenti 50% via Premiere Pro (pas en rendu)
- `Mat_Yeux_Iris` Emissive : keyframe 0.0 → 0.08 entre frames 1600–1920
- `Mat_Or_Emission` bijoux : Emissive 0.2 → 0.45 entre frames 1600–1920
- Particules : micro-oscillation Y ±0.02m sur 480 frames

---

## SCÈNE 5 — L'ÉVEIL
**Frames :** 1921 → 2280 | **Durée :** 80 – 95s | **Caméra :** 85mm fixe

### Description Visuelle
Les yeux de N'Aset **s'ouvrent d'un coup**.  
L'iris émet une **lumière dorée** (`#C9963A`) franche — l'Œil Oudjat `𓂀` s'active.  
Les particules **explosent** doucement autour d'elle — pas une explosion violente, une **irradiation**.  
Le drapé blanc devient lumineux par transparence.  
La **totalité du plan est baigné d'or** pendant 2 secondes.  
Puis — **cut sec vers le noir.**  
Silence.  
En surimpression, sur fond noir : `𓂀`

### Intention de Mise en Scène
- L'ouverture des yeux = le seul mouvement vif de tout le film
- Tout ce qui suit est la conséquence — pas l'acte
- L'irradiation dorée ne doit jamais paraître agressive — elle est **souveraine**
- Le cut vers le noir doit être **instantané** — pas de fondu
- Le symbole `𓂀` reste à l'écran 3–4 secondes sur fond noir pur

### Notes Techniques
- Animation yeux : keyframe paupières fermées → ouvertes en 4 frames (frame 1921–1925)
- `Mat_Yeux_Iris` Emissive : keyframe 0.08 → 1.2 entre frames 1921–1960
- `Particules_Or_Emitter` : burst à frame 1921, radius 0→3m sur 120 frames
- `Mat_Or_Emission` bijoux : 0.45 → 2.0 entre frames 1921–1980 (bloom géré en AE)
- Aura body : Emission shader sur `Naset_Body` : 0.0 → 0.15 entre frames 1960–2100
- Cut noir : frame 2200 exact (AE/PP — pas dans Blender)
- Symbole `𓂀` : compositing AE, fonte Noto Sans Egyptian, fade in 2s après cut

---

## AMBIANCE SONORE (référence)

| Scène | Son |
|-------|-----|
| S1 | Vent naturel · Herbe · Silence |
| S2 | Vent léger · Début d'une drone musicale (très basse) |
| S3 | Silence total · Tension |
| S4 | Drone monte · Fréquence 432Hz |
| S5 | Explosion sonore courte · Cut silence · Symbole |

---

*𓂀 Scénario N'Aset OFM v1.0 · Négus Dja · Ordre du Feu Mystique*
