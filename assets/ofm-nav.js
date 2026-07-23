/* ============================================================
   𓂀 N'Aset OFM — Barre de navigation inter-pages (partagée)
   ------------------------------------------------------------
   Source UNIQUE de la nav. Incluse par les 6 pages via :
     <script defer src="/assets/ofm-nav.js"></script>
   S'auto-injecte en haut du <body>, surligne la page courante.
   Chemins ABSOLUS (racine) -> marchent sur Netlify + serveur local.
   Pour ajouter/retirer une page : éditer le tableau PAGES ci-dessous.
   ============================================================ */
(function () {
  "use strict";

  var PAGES = [
    { href: "/naset_dashboard.html",                 label: "Dashboard" },
    { href: "/production_dashboard.html",            label: "Production" },
    { href: "/docs/NasetOFM_Moodboard.html",         label: "Mood Board" },
    { href: "/docs/naset_full_technical_guide.html", label: "Guide Technique" },
    { href: "/docs/naset_ofm_character_database.html", label: "Base de Données" },
    { href: "/naset_higgsfield_prompts.html",        label: "Prompts" }
  ];

  var BASE   = "padding:5px 14px;border-radius:6px;text-decoration:none;" +
               "font-family:'Inter',system-ui,sans-serif;font-size:13px;" +
               "white-space:nowrap;transition:all .15s;";
  var IDLE   = BASE + "border:1px solid rgba(201,150,58,0.2);color:#8A8478;";
  var ACTIVE = BASE + "background:rgba(201,150,58,0.18);border:1px solid #C9963A;" +
               "color:#E8BC6A;font-weight:500;";

  function currentPath() {
    var p = location.pathname;
    if (p === "/" || p === "") p = "/naset_dashboard.html"; // accueil -> dashboard
    return p;
  }

  function build() {
    var here = currentPath();
    var links = PAGES.map(function (pg) {
      var on = here === pg.href || here.slice(-pg.href.length) === pg.href;
      return '<a href="' + pg.href + '" style="' + (on ? ACTIVE : IDLE) + '"' +
             ' onmouseover="this.style.color=\'#E8BC6A\'"' +
             ' onmouseout="if(!/E8BC6A/.test(this.getAttribute(\'style\')))this.style.color=\'#8A8478\'">' +
             pg.label + "</a>";
    }).join("");

    return '<nav id="ofm-nav-bar" aria-label="Navigation N\'Aset OFM" style="' +
             "position:sticky;top:0;z-index:9999;display:flex;align-items:center;" +
             "gap:8px;flex-wrap:wrap;padding:10px 24px;" +
             "background:rgba(10,10,15,0.95);backdrop-filter:blur(8px);" +
             "-webkit-backdrop-filter:blur(8px);" +
             'border-bottom:1px solid rgba(201,150,58,0.2);">' +
             '<a href="/naset_dashboard.html" aria-label="Accueil" ' +
             'style="color:#C9963A;font-size:18px;margin-right:8px;text-decoration:none;">𓂀</a>' +
             links +
           "</nav>";
  }

  function inject() {
    if (!document.body || document.getElementById("ofm-nav-bar")) return;
    document.body.insertAdjacentHTML("afterbegin", build());
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", inject);
  } else {
    inject();
  }
})();
