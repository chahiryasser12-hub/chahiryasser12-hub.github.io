/* Fynzo shared UI: English navigation, search and theme controls. */
(function () {
  "use strict";

  var root = document.documentElement;
  if (localStorage.getItem("fynzo-theme") === "dark") {
    root.setAttribute("data-theme", "dark");
  }

  function toggleTheme() {
    var dark = root.getAttribute("data-theme") === "dark";
    if (dark) {
      root.removeAttribute("data-theme");
      localStorage.setItem("fynzo-theme", "light");
    } else {
      root.setAttribute("data-theme", "dark");
      localStorage.setItem("fynzo-theme", "dark");
    }
  }

  function homeUrl() {
    return "/";
  }

  function buildNavigationTools() {
    var navLinks = document.querySelector(".nav-links");
    if (!navLinks || navLinks.querySelector(".nav-tools")) return;

    var tools = document.createElement("div");
    tools.className = "nav-tools";
    tools.innerHTML =
      '<div class="nav-search" id="navSearch">' +
      '<input type="search" placeholder="Search calculators" aria-label="Search calculators">' +
      '<button class="go" type="button" aria-label="Run search">' +
      '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 12 H19 M13 6 L19 12 L13 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>' +
      '</button></div>' +
      '<button class="icon-btn" id="searchToggle" type="button" aria-label="Open search" aria-expanded="false">' +
      '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/><path d="M20 20 L16 16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>' +
      '</button>' +
      '<button class="icon-btn" id="themeToggle" type="button" aria-label="Toggle dark mode">' +
      '<svg class="sun" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="4.5" stroke="currentColor" stroke-width="2"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.5 1.5M17.5 17.5L19 19M19 5l-1.5 1.5M6.5 17.5L5 19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>' +
      '<svg class="moon" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M20 14.5 A8 8 0 1 1 9.5 4 A6.5 6.5 0 0 0 20 14.5 Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>' +
      '</button>';
    navLinks.appendChild(tools);

    var searchBox = tools.querySelector("#navSearch");
    var searchInput = searchBox.querySelector("input");
    var searchToggle = tools.querySelector("#searchToggle");

    function toggleSearch() {
      var open = searchBox.classList.toggle("open");
      searchToggle.setAttribute("aria-expanded", open ? "true" : "false");
      searchToggle.setAttribute("aria-label", open ? "Close search" : "Open search");
      if (open) searchInput.focus();
    }

    function runSearch() {
      var query = searchInput.value.trim();
      if (!query) return;
      var pageSearch = document.getElementById("calcSearch");
      var toolsSection = document.getElementById("tools");
      if (pageSearch && toolsSection) {
        pageSearch.value = query;
        pageSearch.dispatchEvent(new Event("input", { bubbles: true }));
        toolsSection.scrollIntoView({ behavior: "smooth" });
      } else {
        window.location.assign(homeUrl() + "?q=" + encodeURIComponent(query) + "#tools");
      }
    }

    searchToggle.addEventListener("click", toggleSearch);
    searchInput.addEventListener("keydown", function (event) {
      if (event.key === "Enter") runSearch();
      if (event.key === "Escape" && searchBox.classList.contains("open")) toggleSearch();
    });
    searchBox.querySelector(".go").addEventListener("click", runSearch);
    tools.querySelector("#themeToggle").addEventListener("click", toggleTheme);
  }

  function applySearchFromUrl() {
    var pageSearch = document.getElementById("calcSearch");
    var toolsSection = document.getElementById("tools");
    if (!pageSearch || !toolsSection) return;
    var query = new URLSearchParams(window.location.search).get("q");
    if (!query) return;
    pageSearch.value = query;
    pageSearch.dispatchEvent(new Event("input", { bubbles: true }));
    window.setTimeout(function () {
      toolsSection.scrollIntoView({ behavior: "smooth" });
    }, 150);
  }

  document.addEventListener("DOMContentLoaded", function () {
    buildNavigationTools();
    applySearchFromUrl();
  });
})();
