# -*- coding: utf-8 -*-
"""Replace the rail logic with a group-aware version."""
import io

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
JS = ROOT + r"\assets\js\main.js"

s = io.open(JS, encoding="utf-8").read()

start = s.index("  /* --------------------------------------------------------- rails */")
end = s.index("  /* ------------------------------------------------------ scroll reveal */")

new = '''  /* --------------------------------------------------------- rails */
  function activeRail(group) {
    var panel = group.querySelector("[data-panel]:not([hidden])");
    return panel ? $(".rail", panel) : null;
  }

  function syncArrows(group) {
    var rail = activeRail(group);
    if (!rail) return;
    var prev = $('[data-rail="prev"]', group);
    var next = $('[data-rail="next"]', group);
    var max = rail.scrollWidth - rail.clientWidth - 2;
    if (prev) prev.disabled = rail.scrollLeft <= 2;
    if (next) next.disabled = rail.scrollLeft >= max;
  }

  function railStep(rail) {
    var card = $(".rail-card", rail);
    return card ? card.getBoundingClientRect().width + 22 : rail.clientWidth * 0.8;
  }

  $$("[data-tabs]").forEach(function (group) {
    var prev = $('[data-rail="prev"]', group);
    var next = $('[data-rail="next"]', group);
    if (prev) {
      prev.addEventListener("click", function () {
        var rail = activeRail(group);
        if (rail) rail.scrollBy({ left: -railStep(rail) * 2, behavior: "smooth" });
      });
    }
    if (next) {
      next.addEventListener("click", function () {
        var rail = activeRail(group);
        if (rail) rail.scrollBy({ left: railStep(rail) * 2, behavior: "smooth" });
      });
    }
    group.addEventListener("scroll", function () { syncArrows(group); }, true);
    window.addEventListener("resize", function () { syncArrows(group); });
    syncArrows(group);
  });

  /* pointer drag for every rail */
  $$(".rail").forEach(function (rail) {
    var group = rail.closest("[data-tabs]") || doc;
    var down = false, startX = 0, startLeft = 0, moved = false;

    rail.addEventListener("pointerdown", function (e) {
      if (e.pointerType === "touch") return;
      down = true;
      moved = false;
      startX = e.clientX;
      startLeft = rail.scrollLeft;
      rail.classList.add("is-dragging");
    });
    window.addEventListener("pointermove", function (e) {
      if (!down) return;
      var dx = e.clientX - startX;
      if (Math.abs(dx) > 4) moved = true;
      rail.scrollLeft = startLeft - dx;
    });
    window.addEventListener("pointerup", function () {
      if (!down) return;
      down = false;
      rail.classList.remove("is-dragging");
      syncArrows(group);
    });
    rail.addEventListener("click", function (e) {
      if (moved) {
        e.preventDefault();
        e.stopPropagation();
      }
    }, true);
  });

'''

s = s[:start] + new + s[end:]

# tab activation should resync the group's arrows
s = s.replace('''      var panel = doc.getElementById(tab.getAttribute("aria-controls"));
      var rail = panel ? $(".rail", panel) : null;
      if (rail) {
        rail.scrollLeft = 0;
        window.setTimeout(function () { updateRailButtons(rail); }, 30);
      }''',
'''      var panel = doc.getElementById(tab.getAttribute("aria-controls"));
      var rail = panel ? $(".rail", panel) : null;
      if (rail) rail.scrollLeft = 0;
      window.setTimeout(function () { syncArrows(group); }, 30);''')

io.open(JS, "w", encoding="utf-8").write(s)
print("rails rewritten", len(s))
