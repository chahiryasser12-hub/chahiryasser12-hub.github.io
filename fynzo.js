/* ============================================================
   Fynzo — core script  (FIXED + IMPROVED, 2026)
   ✔ Theme toggle (light/dark) with localStorage — no flash
   ✔ Language switcher EN / FR / AR  — BUG FIXED: uses ABSOLUTE
     paths so the chosen language STICKS on every page
   ✔ Auto RTL + lang attribute for Arabic
   ✔ Accessible: aria-labels, keyboard & focus friendly
   Replace your old fynzo.js with this file.
   ============================================================ */
(function () {
  "use strict";

  var FL = (window.FL || document.documentElement.lang || "en").slice(0, 2);

  /* ---- Apply saved theme immediately (prevents flash of wrong theme) ---- */
  if (localStorage.getItem("ft") === "dark") {
    document.documentElement.setAttribute("data-theme", "dark");
  }

  /* ---- Theme toggle ---- */
  function toggleTheme() {
    var isDark = document.documentElement.getAttribute("data-theme") === "dark";
    if (isDark) {
      document.documentElement.removeAttribute("data-theme");
      localStorage.setItem("ft", "light");
    } else {
      document.documentElement.setAttribute("data-theme", "dark");
      localStorage.setItem("ft", "dark");
    }
  }

  /* ---- Current page filename e.g. "bmi-calculator.html" ---- */
  function slug() {
    return location.pathname.split("/").pop() || "index.html";
  }

  /* ---- FIXED language switch: ABSOLUTE paths keep you on the
         same page in the chosen language (EN=/, FR=/fr/, AR=/ar/) ---- */
  function switchLang(to) {
    var page = slug();
    var base = to === "en" ? "/" : "/" + to + "/";
    window.location.href = base + page;
  }

  /* ---- Build nav tools (theme button + language select) ---- */
  function build() {
    var nl = document.querySelector(".nav-links");
    if (!nl) return;

    var wrap = document.createElement("div");
    wrap.className = "nav-tools";
    wrap.innerHTML =
      '<button id="ft-theme" class="icon-btn" type="button" ' +
      'aria-label="Toggle dark mode" title="Toggle dark mode">' +
      '<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
      'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
      '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>' +
      '<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
      'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
      '<circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.2 4.2l1.4 1.4' +
      'M18.4 18.4l1.4 1.4M1 12h2M21 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/></svg>' +
      "</button>" +
      '<select id="ft-lang" class="lang-select" aria-label="Choose language">' +
      '<option value="en">EN</option>' +
      '<option value="fr">FR</option>' +
      '<option value="ar">AR</option>' +
      "</select>";
    nl.appendChild(wrap);

    wrap.querySelector("#ft-theme").addEventListener("click", toggleTheme);
    var sel = wrap.querySelector("#ft-lang");
    sel.value = FL;
    sel.addEventListener("change", function () { switchLang(sel.value); });
  }

  /* ---- Auto RTL for Arabic ---- */
  function applyDir() {
    if (FL === "ar") {
      document.documentElement.setAttribute("dir", "rtl");
      document.documentElement.setAttribute("lang", "ar");
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    applyDir();
    build();
  });
})();
