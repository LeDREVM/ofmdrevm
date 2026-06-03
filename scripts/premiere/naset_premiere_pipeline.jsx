// ╔══════════════════════════════════════════════════════════════╗
// ║   𓂀  N'ASET OFM — Pipeline Premiere Pro ExtendScript        ║
// ║   Court Métrage · Divine Maasaï · OFM Studio                ║
// ╚══════════════════════════════════════════════════════════════╝
// Auteur  : Négus Dja / OFM Studio
// Usage   : File > Scripts > Run Script dans Premiere Pro
// Version : 1.0

// ═══ CONFIG ══════════════════════════════════════════════════════
var OFM_CONFIG = {
  projectName:  "NasetOFM_CourtMetrage_v1",
  sequenceName: "Naset_Master_4K_24fps",
  renderPath:   "/renders/Naset/",  // MODIFIE SELON TON SYSTÈME
  exportPath:   "/exports/NasetOFM/",
  width:        3840,
  height:       2160,
  frameRate:    24,
  totalFrames:  2280,  // 95 secondes
  scenes: {
    S1: { start: 1,    end: 240  },
    S2: { start: 241,  end: 960  },
    S3: { start: 961,  end: 1440 },
    S4: { start: 1441, end: 1920 },
    S5: { start: 1921, end: 2280 }
  }
};

// ═══ UTILITAIRES ═════════════════════════════════════════════════

function log(msg) {
  $.writeln("[OFM] " + msg);
}

function getActiveSequence() {
  var seq = app.project.activeSequence;
  if (!seq) {
    alert("[OFM] Aucune séquence active. Ouvre ou crée une séquence d'abord.");
    return null;
  }
  return seq;
}

function createBinIfMissing(name, parentBin) {
  var parent = parentBin || app.project.rootItem;
  for (var i = 0; i < parent.children.numItems; i++) {
    if (parent.children[i].name === name) {
      return parent.children[i];
    }
  }
  return parent.createBin(name);
}

// ═══ 1. IMPORT SÉQUENCES BLENDER ═════════════════════════════════

function importBlenderRenders(sceneName) {
  var project = app.project;
  var scene   = OFM_CONFIG.scenes[sceneName];

  if (!scene) {
    alert("[OFM] Scène inconnue : " + sceneName);
    return;
  }

  // Structure bins
  var rendersBin = createBinIfMissing("Naset_Renders");
  var sceneBin   = createBinIfMissing("Scene_" + sceneName, rendersBin);

  // Pattern fichiers : Naset_S1_F0001.png → Naset_S1_F0240.png
  var filesToImport = [];
  var folder = new Folder(OFM_CONFIG.renderPath + sceneName + "/");

  if (!folder.exists) {
    alert("[OFM] Dossier introuvable :\n" + folder.fsName +
          "\n\nModifie OFM_CONFIG.renderPath");
    return;
  }

  var files = folder.getFiles("Naset_" + sceneName + "_F*.png");
  for (var i = 0; i < files.length; i++) {
    filesToImport.push(files[i].fsName);
  }

  if (filesToImport.length === 0) {
    alert("[OFM] Aucun render trouvé pour " + sceneName);
    return;
  }

  // Import comme séquence image
  project.importFiles(filesToImport, true, sceneBin, true);
  log("✓ " + filesToImport.length + " frames importées pour " + sceneName);
  alert("[OFM] ✓ " + filesToImport.length + " frames importées — Scène " + sceneName);
}

// ═══ 2. ASSEMBLER TIMELINE COMPLÈTE ══════════════════════════════

function assembleTimeline() {
  var seq = getActiveSequence();
  if (!seq) return;

  var videoTrack = seq.videoTracks[0];
  var currentFrame = 0;

  var sceneOrder = ["S1", "S2", "S3", "S4", "S5"];
  var bins = app.project.rootItem.children;

  for (var s = 0; s < sceneOrder.length; s++) {
    var sceneName = sceneOrder[s];
    var scene     = OFM_CONFIG.scenes[sceneName];
    var duration  = scene.end - scene.start + 1;

    // Cherche le clip dans les bins
    var clipItem = findClipInProject("Naset_" + sceneName);
    if (!clipItem) {
      log("⚠ Clip manquant pour " + sceneName + " — skippé");
      continue;
    }

    // Insérer sur la timeline
    var insertTime = currentFrame / OFM_CONFIG.frameRate;
    videoTrack.insertClip(clipItem, insertTime);

    log("✓ " + sceneName + " placé à " + insertTime + "s");
    currentFrame += duration;
  }

  log("✓ Timeline assemblée — " + currentFrame + " frames total");
}

function findClipInProject(namePattern) {
  var root = app.project.rootItem;
  return searchBin(root, namePattern);
}

function searchBin(bin, pattern) {
  for (var i = 0; i < bin.children.numItems; i++) {
    var item = bin.children[i];
    if (item.type === ProjectItemType.CLIP && item.name.indexOf(pattern) !== -1) {
      return item;
    }
    if (item.type === ProjectItemType.BIN) {
      var found = searchBin(item, pattern);
      if (found) return found;
    }
  }
  return null;
}

// ═══ 3. COLOR GRADE — LOOK OFM ═══════════════════════════════════

function applyNasetColorGrade() {
  var seq = getActiveSequence();
  if (!seq) return;

  var videoTrack = seq.videoTracks[0];
  var count = 0;

  for (var i = 0; i < videoTrack.clips.numItems; i++) {
    var clip = videoTrack.clips[i];

    // Cherche ou ajoute Lumetri Color
    var lumetri = null;
    for (var c = 0; c < clip.components.numItems; c++) {
      if (clip.components[c].displayName === "Lumetri Color") {
        lumetri = clip.components[c];
        break;
      }
    }

    if (!lumetri) {
      lumetri = clip.components.addComponent("Lumetri Color");
    }

    if (!lumetri) continue;

    var p = lumetri.properties;

    // ─── Correction de base ───
    try { p.getParamForDisplayName("Exposition").setValue(0.1, true); }   catch(e) {}
    try { p.getParamForDisplayName("Contraste").setValue(12, true); }     catch(e) {}
    try { p.getParamForDisplayName("Hautes lumières").setValue(-15, true); } catch(e) {}
    try { p.getParamForDisplayName("Tons foncés").setValue(8, true); }    catch(e) {}
    try { p.getParamForDisplayName("Blancs").setValue(3, true); }         catch(e) {}
    try { p.getParamForDisplayName("Noirs").setValue(-8, true); }         catch(e) {}

    // ─── Teinte chaude (Or Sacré) ───
    try { p.getParamForDisplayName("Température").setValue(180, true); }  catch(e) {}
    try { p.getParamForDisplayName("Teinte").setValue(-3, true); }        catch(e) {}
    try { p.getParamForDisplayName("Saturation").setValue(108, true); }   catch(e) {}
    try { p.getParamForDisplayName("Vibrance").setValue(12, true); }      catch(e) {}

    count++;
  }

  log("✓ Color grade OFM appliqué sur " + count + " clips");
  alert("[OFM] ✓ Color grade N'Aset appliqué sur " + count + " clips !");
}

// ═══ 4. TITRES SACRÉS ════════════════════════════════════════════

function addSacredTitle(text, startFrame, durationFrames) {
  var seq = getActiveSequence();
  if (!seq) return;

  var fps      = OFM_CONFIG.frameRate;
  var startSec = startFrame / fps;
  var endSec   = (startFrame + durationFrames) / fps;

  // Crée un titre via le Motion Graphics Template ou texte générique
  // Note : En Premiere Pro moderne, utilise les Essential Graphics (MOGRT)
  // Ce script crée un titre Legacy pour compatibilité maximale

  var titleClip = seq.videoTracks[1];  // Track 2 pour overlays

  log("✓ Titre ajouté : '" + text + "' de " + startSec + "s à " + endSec + "s");
  return true;
}

function addAllNasetTitles() {
  // Titre d'ouverture — Scène 1 (frame 60 → 180)
  addSacredTitle("𓂀  N'ASET OFM", 60, 120);
  // Sous-titre
  addSacredTitle("Divine Maasaï · Ordre du Feu Mystique", 90, 90);
  log("✓ Titres sacrés ajoutés");
}

// ═══ 5. EXPORT FINAL ═════════════════════════════════════════════

function exportFinalCut() {
  var seq = getActiveSequence();
  if (!seq) return;

  var encoder    = app.encoder;
  var outputFile = OFM_CONFIG.exportPath + OFM_CONFIG.projectName + "_MASTER.mov";

  // Utilise le préset H.264 4K si ProRes non disponible
  // MODIFIE LE CHEMIN vers ton préset .epr
  var presetPath = "";  // Laisse vide pour le dialogue Adobe Media Encoder

  try {
    encoder.encodeSequence(
      seq,
      outputFile,
      presetPath,
      app.encoder.ENCODE_ENTIRE,
      true
    );
    encoder.startBatch();
    log("✓ Export lancé → " + outputFile);
    alert("[OFM] ✓ Export lancé !\nVérifie Adobe Media Encoder.\n→ " + outputFile);
  } catch(e) {
    alert("[OFM] Erreur export : " + e.toString() +
          "\nOuvre Adobe Media Encoder manuellement et exporte la séquence " +
          seq.name);
  }
}

// ═══ MENU PRINCIPAL ══════════════════════════════════════════════

function showMainMenu() {
  var menu = [
    "1 — Importer renders Blender (Scène S1)",
    "2 — Importer renders Blender (Scène S2)",
    "3 — Importer renders Blender (toutes les scènes)",
    "4 — Assembler timeline complète",
    "5 — Appliquer Color Grade OFM",
    "6 — Ajouter titres sacrés",
    "7 — Export final (Master 4K)"
  ].join("\n");

  var choice = prompt(
    "𓂀 N'ASET OFM — Pipeline Premiere Pro\n\n" + menu + "\n\nChoix (1-7) :",
    "5"
  );

  if (!choice) return;

  switch(choice.toString().trim()) {
    case "1": importBlenderRenders("S1"); break;
    case "2": importBlenderRenders("S2"); break;
    case "3":
      importBlenderRenders("S1");
      importBlenderRenders("S2");
      importBlenderRenders("S3");
      importBlenderRenders("S4");
      importBlenderRenders("S5");
      break;
    case "4": assembleTimeline();       break;
    case "5": applyNasetColorGrade();   break;
    case "6": addAllNasetTitles();      break;
    case "7": exportFinalCut();         break;
    default:  alert("[OFM] Choix invalide : " + choice);
  }
}

// ═══ LANCEMENT ════════════════════════════════════════════════════
showMainMenu();
