/* =========================================================================
   Weinas — site interactions (no dependencies)
   ========================================================================= */
(function () {
  "use strict";

  var doc = document;
  var body = doc.body;
  var mqlFine = window.matchMedia("(hover: hover) and (pointer: fine)");
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  var $ = function (sel, ctx) { return (ctx || doc).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || doc).querySelectorAll(sel)); };

  /* ------------------------------------------------------- header state */
  var header = $("#header");
  var floating = $("#floating-quote");
  var lastY = window.scrollY;

  var siteFooter = $(".site-footer");

  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle("is-scrolled", y > 12);
    if (floating) {
      floating.classList.toggle("is-visible", y > 480);
      if (siteFooter) {
        var rect = siteFooter.getBoundingClientRect();
        floating.classList.toggle("on-navy", rect.top < window.innerHeight - 32);
      }
    }
    spy(y);
    lastY = y;
  }
  window.addEventListener("scroll", onScroll, { passive: true });

  /* --------------------------------------------------------- scrollspy */
  var navLinks = $$(".nav__link[data-spy]");
  var spySections = navLinks
    .map(function (link) {
      var id = link.getAttribute("href");
      var el = id && id.charAt(0) === "#" ? doc.querySelector(id) : null;
      return el ? { link: link, el: el } : null;
    })
    .filter(Boolean);

  function spy(y) {
    if (!spySections || !spySections.length) return;
    var marker = y + window.innerHeight * 0.35;
    var current = spySections[0];
    spySections.forEach(function (entry) {
      if (entry.el.offsetTop <= marker) current = entry;
    });
    spySections.forEach(function (entry) {
      entry.link.classList.toggle("is-active", entry === current);
      if (entry === current) entry.link.setAttribute("aria-current", "page");
      else entry.link.removeAttribute("aria-current");
    });
  }

  onScroll();

  /* --------------------------------------------------------- mega menus */
  var menuItems = $$(".nav__item--has-menu");

  function menuTrigger(item) {
    return $(".nav__toggle", item) || $(".nav__link", item);
  }
  function closeItem(item) {
    item.classList.remove("is-open");
    var t = menuTrigger(item);
    if (t) t.setAttribute("aria-expanded", "false");
  }
  function openItem(item) {
    menuItems.forEach(function (other) {
      if (other !== item) closeItem(other);
    });
    item.classList.add("is-open");
    var t = menuTrigger(item);
    if (t) t.setAttribute("aria-expanded", "true");
  }
  function isOpen(item) {
    return item.classList.contains("is-open");
  }

  menuItems.forEach(function (item) {
    var trigger = $(".nav__toggle", item);
    var timer = null;

    if (trigger) {
      /* button trigger: click toggles */
      trigger.addEventListener("click", function (e) {
        e.preventDefault();
        if (isOpen(item)) closeItem(item);
        else openItem(item);
      });
    } else {
      /* link trigger: click navigates, menu is hover/focus driven */
      var link = $(".nav__link", item);
      if (link) link.addEventListener("click", function () { closeItem(item); });
    }

    item.addEventListener("mouseenter", function () {
      if (!mqlFine.matches) return;
      window.clearTimeout(timer);
      openItem(item);
    });
    item.addEventListener("mouseleave", function () {
      if (!mqlFine.matches) return;
      window.clearTimeout(timer);
      timer = window.setTimeout(function () { closeItem(item); }, 160);
    });
    item.addEventListener("focusin", function () {
      if (mqlFine.matches) openItem(item);
    });
    item.addEventListener("focusout", function (e) {
      if (!item.contains(e.relatedTarget)) closeItem(item);
    });
  });

  doc.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    menuItems.forEach(function (item) {
      if (isOpen(item)) {
        closeItem(item);
        var t = menuTrigger(item);
        if (t) t.focus();
      }
    });
  });
  doc.addEventListener("click", function (e) {
    menuItems.forEach(function (item) {
      if (isOpen(item) && !item.contains(e.target)) closeItem(item);
    });
  });

  /* --------------------------------------------------------- mobile nav */
  var burger = $("#burger");
  var mobileNav = $("#mobile-nav");
  var mobileSubToggles = $$(".mobile-nav__toggle");

  function setMobileNav(open) {
    if (!mobileNav || !burger) return;
    mobileNav.classList.toggle("is-open", open);
    burger.setAttribute("aria-expanded", open ? "true" : "false");
    burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    body.classList.toggle("is-locked", open);
    if (!open) {
      mobileNav.setAttribute("aria-hidden", "true");
    } else {
      mobileNav.removeAttribute("aria-hidden");
      var first = $("a, button", mobileNav);
      if (first) first.focus({ preventScroll: true });
    }
  }

  if (burger && mobileNav) {
    mobileNav.setAttribute("aria-hidden", "true");
    burger.addEventListener("click", function () {
      setMobileNav(!mobileNav.classList.contains("is-open"));
    });
    mobileSubToggles.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var sub = doc.getElementById(btn.getAttribute("aria-controls"));
        var isOpen = btn.getAttribute("aria-expanded") === "true";
        btn.setAttribute("aria-expanded", isOpen ? "false" : "true");
        if (sub) sub.classList.toggle("is-open", !isOpen);
      });
    });
    $$("a", mobileNav).forEach(function (a) {
      a.addEventListener("click", function () { setMobileNav(false); });
    });
    doc.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && mobileNav.classList.contains("is-open")) {
        setMobileNav(false);
        burger.focus();
      }
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 980 && mobileNav.classList.contains("is-open")) setMobileNav(false);
    });
  }

  /* ------------------------------------------------------------- search */
  var search = $("#search");
  var searchOpen = $("#search-open");
  var searchClose = $("#search-close");
  var searchInput = $("#search-input");
  var searchResults = $("#search-results");
  var searchItems = searchResults ? $$("a", searchResults) : [];
  var searchEmpty = null;

  function openSearch() {
    if (!search) return;
    search.classList.add("is-open");
    search.removeAttribute("aria-hidden");
    body.classList.add("is-locked");
    window.setTimeout(function () {
      if (searchInput) searchInput.focus();
    }, 120);
  }
  function closeSearch() {
    if (!search) return;
    search.classList.remove("is-open");
    search.setAttribute("aria-hidden", "true");
    body.classList.remove("is-locked");
    if (searchOpen) searchOpen.focus({ preventScroll: true });
  }

  if (search) {
    search.setAttribute("aria-hidden", "true");
    if (searchOpen) {
      searchOpen.addEventListener("click", function (e) {
        e.preventDefault();
        openSearch();
      });
    }
    if (searchClose) searchClose.addEventListener("click", closeSearch);
    search.addEventListener("click", function (e) {
      if (e.target === search) closeSearch();
    });
    doc.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && search.classList.contains("is-open")) closeSearch();
    });
  }

  if (searchInput && searchResults) {
    searchEmpty = doc.createElement("p");
    searchEmpty.className = "search__empty";
    searchEmpty.textContent = "No system matches that term. Try “sliding”, “casement”, “folding” or “thermal”.";
    searchResults.appendChild(searchEmpty);
    searchEmpty.hidden = true;

    searchInput.addEventListener("input", function () {
      var q = searchInput.value.trim().toLowerCase();
      var shown = 0;
      searchItems.forEach(function (item) {
        var hay = (item.dataset.name || "") + " " + (item.textContent || "");
        var match = q === "" || hay.toLowerCase().indexOf(q) > -1;
        item.hidden = !match;
        if (match) shown += 1;
      });
      searchEmpty.hidden = shown > 0;
    });
  }

  /* --------------------------------------------------------------- tabs */
  $$("[data-tabs]").forEach(function (group) {
    var tabs = $$('[role="tab"]', group);
    var panels = $$("[data-panel]", group);
    function activate(tab) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        var panel = doc.getElementById(t.getAttribute("aria-controls"));
        if (panel) panel.hidden = !on;
      });
      var panel = doc.getElementById(tab.getAttribute("aria-controls"));
      var rail = panel ? $(".rail", panel) : null;
      if (rail) rail.scrollLeft = 0;
      window.setTimeout(function () { syncArrows(group); }, 30);
    }
    tabs.forEach(function (tab, i) {
      tab.addEventListener("click", function () { activate(tab); });
      tab.addEventListener("keydown", function (e) {
        var next = null;
        if (e.key === "ArrowRight") next = tabs[(i + 1) % tabs.length];
        if (e.key === "ArrowLeft") next = tabs[(i - 1 + tabs.length) % tabs.length];
        if (next) {
          e.preventDefault();
          next.focus();
          activate(next);
        }
      });
    });
  });

  /* --------------------------------------------------------- rails */
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

  /* Rails scroll with the arrow buttons, the wheel and native touch scrolling.
     The old mouse drag-to-scroll swallowed clicks on the cards (a 1-2px jitter
     counted as a drag), so it is gone - navigation wins over drag. */

  /* ------------------------------------------------------ scroll reveal */
  var revealEls = $$(".reveal");
  if (revealEls.length && "IntersectionObserver" in window && !reduceMotion.matches) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-in");
            io.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
    );
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ------------------------------------------------------------- forms */
  var fileInput = $("#f-file");
  var fileName = $("#f-file-name");
  if (fileInput && fileName) {
    fileInput.addEventListener("change", function () {
      var f = fileInput.files && fileInput.files[0];
      fileName.textContent = f ? f.name + " · " + Math.round(f.size / 1024) + " KB" : "No file selected";
    });
  }

  function fakeSubmit(form, statusEl, message) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }
      if (statusEl) {
        statusEl.hidden = false;
        statusEl.textContent = message;
      }
      form.reset();
    });
  }

  var quoteForm = $("#quote-form");
  if (quoteForm) {
    fakeSubmit(
      quoteForm,
      $("#quote-status"),
      "Thank you — your enquiry is queued. Our engineering team replies within one business day."
    );
  }
  var newsForm = $("#newsletter-form");
  if (newsForm) {
    newsForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var input = $("input", newsForm);
      var note = $("#newsletter-note");
      if (input && note) {
        note.textContent = "Subscribed — technical updates will arrive quarterly.";
        note.hidden = false;
        newsForm.reset();
      }
    });
  }

  /* ------------------------------------------------------ prototype links */
  var toast = $("#toast");
  var toastTimer = null;

  function showToast(message) {
    if (!toast) return;
    toast.textContent = message;
    toast.hidden = false;
    /* force reflow so the transition runs */
    void toast.offsetWidth;
    toast.classList.add("is-visible");
    window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(function () {
      toast.classList.remove("is-visible");
      window.setTimeout(function () { toast.hidden = true; }, 260);
    }, 3600);
  }

  doc.addEventListener("click", function (e) {
    var link = e.target.closest ? e.target.closest("[data-coming-soon]") : null;
    if (!link) return;
    e.preventDefault();
    var custom = link.getAttribute("data-toast");
    if (custom) {
      showToast(custom);
      return;
    }
    var label = (link.textContent || "").trim() || "This page";
    showToast(label + " — this inner page is not part of the homepage deliverable. Content is structured and ready to build.");
  });

  /* ------------------------------------------------------------- misc */
  var yearEl = $("#year");
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  /* close mobile nav / search when resizing up */
  window.addEventListener("resize", function () {
    if (window.innerWidth > 980 && search && search.classList.contains("is-open")) {
      /* keep search open, it is width-agnostic */
    }
  });

  /* keyboard: “/” focuses search */
  doc.addEventListener("keydown", function (e) {
    var tag = (e.target.tagName || "").toLowerCase();
    if (tag === "input" || tag === "textarea" || tag === "select") return;
    if (e.key === "/" && search && !search.classList.contains("is-open")) {
      e.preventDefault();
      openSearch();
    }
  });
})();

/* ------------------------------------------------------ quotation modal */
(function () {
  var modal = document.getElementById("qmodal");
  if (!modal) return;
  var titleEl = modal.querySelector("[data-qm-title]");
  var codeEl = modal.querySelector("[data-qm-code]");
  var specsEl = modal.querySelector("[data-qm-specs]");
  var msg = modal.querySelector("#qm-message");
  var form = modal.querySelector("#qm-form");
  var status = modal.querySelector("#qm-status");
  var lastFocus = null;

  function open(btn) {
    var name = btn.getAttribute("data-name") || "Product";
    var code = btn.getAttribute("data-code") || "";
    var specs = [];
    try { specs = JSON.parse(btn.getAttribute("data-specs") || "[]"); } catch (e) { specs = []; }

    if (titleEl) titleEl.textContent = name;
    if (codeEl) codeEl.textContent = code;
    if (specsEl) {
      specsEl.innerHTML = specs.map(function (row) {
        return "<div><dt>" + row[0] + "</dt><dd>" + row[1] + "</dd></div>";
      }).join("");
    }
    if (msg) {
      msg.value = "Hello, I would like a quotation for the " + name + " (" + code + "). "
        + "Quantity: | Opening sizes: | Destination port:";
    }
    if (status) status.hidden = true;

    lastFocus = document.activeElement;
    modal.hidden = false;
    modal.setAttribute("aria-hidden", "false");
    document.body.classList.add("is-locked");
    var first = modal.querySelector("input, textarea, button");
    if (first) first.focus();
  }

  function close() {
    modal.hidden = true;
    modal.setAttribute("aria-hidden", "true");
    document.body.classList.remove("is-locked");
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  document.addEventListener("click", function (e) {
    if (!e.target.closest) return;
    var trigger = e.target.closest("[data-quote]");
    if (trigger) { e.preventDefault(); open(trigger); return; }
    if (e.target.closest("[data-close]")) { e.preventDefault(); close(); }
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !modal.hidden) close();
  });

  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!status) return;
      status.hidden = false;
      status.textContent = "Thank you — your enquiry for " + ((codeEl && codeEl.textContent) || "this system")
        + " is queued. Our engineering team replies within one business day.";
      form.reset();
    });
  }
})();

/* ------------------------------------------------ product grid pagination */
(function () {
  var grid = document.querySelector(".pgrid[data-per-page]");
  if (!grid) return;
  var pager = document.querySelector("[data-pager]");
  var per = parseInt(grid.getAttribute("data-per-page"), 10) || 6;
  var cards = [].slice.call(grid.children);
  var pages = Math.ceil(cards.length / per);
  if (!pager || pages < 2) { if (pager) pager.hidden = true; return; }

  var current = 1;

  function render() {
    cards.forEach(function (card, i) {
      var page = Math.floor(i / per) + 1;
      card.hidden = page !== current;
    });
    pager.innerHTML = "";
    var prev = document.createElement("button");
    prev.type = "button";
    prev.className = "ppager__step";
    prev.textContent = "← Prev";
    prev.disabled = current === 1;
    prev.addEventListener("click", function () { go(current - 1); });
    pager.appendChild(prev);

    for (var p = 1; p <= pages; p++) {
      (function (p) {
        var b = document.createElement("button");
        b.type = "button";
        b.className = "ppager__num" + (p === current ? " is-active" : "");
        b.textContent = p;
        b.setAttribute("aria-current", p === current ? "page" : "false");
        b.addEventListener("click", function () { go(p); });
        pager.appendChild(b);
      })(p);
    }

    var next = document.createElement("button");
    next.type = "button";
    next.className = "ppager__step";
    next.textContent = "Next →";
    next.disabled = current === pages;
    next.addEventListener("click", function () { go(current + 1); });
    pager.appendChild(next);
  }

  function go(page) {
    if (page < 1 || page > pages || page === current) return;
    current = page;
    render();
    var top = grid.getBoundingClientRect().top + window.scrollY - 120;
    window.scrollTo({ top: top, behavior: "smooth" });
  }

  render();
})();

/* ------------------------------------------------ product figure gallery */
(function () {
  document.querySelectorAll("[data-gallery]").forEach(function (box) {
    var imgs = [].slice.call(box.querySelectorAll("[data-gallery-stage] img"));
    if (imgs.length < 2) return;
    var count = box.querySelector("[data-gallery-count]");
    var prev = box.querySelector("[data-gallery-prev]");
    var next = box.querySelector("[data-gallery-next]");
    var i = 0;

    function show(n) {
      i = Math.max(0, Math.min(imgs.length - 1, n));
      imgs.forEach(function (img, k) { img.hidden = k !== i; });
      if (count) count.textContent = (i + 1) + " / " + imgs.length;
      if (prev) prev.disabled = i === 0;
      if (next) next.disabled = i === imgs.length - 1;
    }

    if (prev) prev.addEventListener("click", function () { show(i - 1); });
    if (next) next.addEventListener("click", function () { show(i + 1); });
    box.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") show(i - 1);
      if (e.key === "ArrowRight") show(i + 1);
    });
    show(0);
  });
})();

/* ------------------------------------------------ product media switcher */
(function () {
  var box = document.querySelector("[data-media]");
  if (!box) return;
  var stage = box.querySelector("[data-media-stage]");
  var thumbs = [].slice.call(box.querySelectorAll("[data-thumb]"));
  if (!stage || thumbs.length < 2) return;
  var imgs = [].slice.call(stage.querySelectorAll("img"));

  thumbs.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var i = parseInt(btn.getAttribute("data-thumb"), 10);
      imgs.forEach(function (img, k) { img.hidden = k !== i; });
      thumbs.forEach(function (b, k) { b.classList.toggle("is-active", k === i); });
    });
  });
})();

/* ------------------------------------------------ mobile swipe rows (cases, catalogue) */
(function () {
  var MQ = window.matchMedia("(max-width: 760px)");
  var containers = [].slice.call(document.querySelectorAll("[data-swipe]"));

  function build(box) {
    if (box.dataset.swipeReady === "1") return;
    box.classList.add("swipe");
    box.dataset.swipeReady = "1";

    var items = [].slice.call(box.children);
    var dots = document.createElement("div");
    dots.className = "swipe-dots";
    dots.setAttribute("role", "tablist");
    dots.setAttribute("aria-label", "Scroll items");

    var buttons = items.map(function (item, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.setAttribute("aria-label", "Item " + (i + 1));
      if (i === 0) b.classList.add("is-active");
      b.addEventListener("click", function () {
        box.scrollTo({ left: item.offsetLeft - box.offsetLeft, behavior: "smooth" });
      });
      dots.appendChild(b);
      return b;
    });

    box.parentNode.insertBefore(dots, box.nextSibling);

    var ticking = false;
    box.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(function () {
        var center = box.scrollLeft + box.clientWidth / 2;
        var best = 0, bestDist = Infinity;
        items.forEach(function (item, i) {
          var mid = item.offsetLeft - box.offsetLeft + item.offsetWidth / 2;
          var d = Math.abs(mid - center);
          if (d < bestDist) { bestDist = d; best = i; }
        });
        buttons.forEach(function (b, i) { b.classList.toggle("is-active", i === best); });
        ticking = false;
      });
    }, { passive: true });
  }

  function teardown(box) {
    if (box.dataset.swipeReady !== "1") return;
    box.classList.remove("swipe");
    box.dataset.swipeReady = "0";
    var next = box.nextSibling;
    if (next && next.classList && next.classList.contains("swipe-dots")) {
      next.parentNode.removeChild(next);
    }
  }

  function sync() {
    containers.forEach(function (box) {
      if (MQ.matches) build(box);
      else teardown(box);
    });
  }

  sync();
  if (MQ.addEventListener) MQ.addEventListener("change", sync);
  else MQ.addListener(sync);
})();

/* ------------------------------------------------ videos page: filter + light box */
(function () {
  var grid = document.querySelector("[data-video-grid]");
  if (!grid) return;

  var cards = [].slice.call(grid.querySelectorAll(".video-card"));
  var tabs = [].slice.call(document.querySelectorAll(".video-tabs .tab"));

  tabs.forEach(function (tab) {
    tab.addEventListener("click", function () {
      var filter = tab.getAttribute("data-filter");
      tabs.forEach(function (t) { t.classList.toggle("is-active", t === tab); });
      cards.forEach(function (card) {
        card.hidden = !(filter === "All" || card.getAttribute("data-cat") === filter);
      });
    });
  });

  var modal = document.getElementById("vmodal");
  var stage = document.getElementById("vstage");
  var cap = document.getElementById("vcap");
  if (!modal || !stage) return;

  function open(card) {
    var id = card.getAttribute("data-video") || "";
    var title = card.getAttribute("data-title") || "";
    var poster = card.querySelector("img");
    stage.innerHTML = "";

    if (id) {
      var frame = document.createElement("iframe");
      frame.src = "https://www.youtube.com/embed/" + id + "?autoplay=1&rel=0";
      frame.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
      frame.allowFullscreen = true;
      stage.appendChild(frame);
    } else {
      if (poster) {
        var img = document.createElement("img");
        img.src = poster.src;
        img.alt = "";
        stage.appendChild(img);
      }
      var note = document.createElement("p");
      note.className = "vmodal__pending";
      note.textContent = "Clip not uploaded yet — ask us on WhatsApp and we will send it.";
      stage.appendChild(note);
    }

    cap.textContent = title;
    modal.hidden = false;
    document.body.style.overflow = "hidden";
  }

  function close() {
    modal.hidden = true;
    stage.innerHTML = "";
    document.body.style.overflow = "";
  }

  cards.forEach(function (card) {
    card.addEventListener("click", function () { open(card); });
  });

  modal.addEventListener("click", function (e) {
    if (e.target.hasAttribute("data-vclose")) close();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !modal.hidden) close();
  });
})();

/* ------------------------------------------------ global quotation modal */
(function () {
  var modal = document.getElementById("gquote");
  if (!modal) return;

  var form = document.getElementById("gquote-form");
  var status = document.getElementById("gquote-status");
  var endpoint = (window.weinasData && window.weinasData.endpoint) || "/wp-json/weinas/v1/enquiry";
  var isLocal = window.location.protocol === "file:";

  function open(source) {
    modal.hidden = false;
    document.body.style.overflow = "hidden";
    if (source) {
      var note = form.querySelector("[data-gq-source]");
      if (note) note.value = source;
    }
    var first = form.querySelector("input[name=name]");
    if (first) setTimeout(function () { first.focus(); }, 60);
  }

  function close() {
    modal.hidden = true;
    document.body.style.overflow = "";
  }

  document.addEventListener("click", function (e) {
    var trigger = e.target.closest("[data-quote-open], a[href$='#quote']");
    if (trigger) {
      e.preventDefault();
      open(trigger.getAttribute("data-quote-open") || "");
      return;
    }
    if (e.target.closest("[data-gq-close]")) close();
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !modal.hidden) close();
  });

  if (!form || !status) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!form.checkValidity()) { form.reportValidity(); return; }

    var payload = {};
    [].slice.call(form.querySelectorAll("input, select, textarea")).forEach(function (f) {
      if (f.name) payload[f.name] = f.value;
    });
    payload.page_url = window.location.href;

    var btn = form.querySelector("[type=submit]");
    if (btn) btn.disabled = true;
    status.hidden = false;
    status.classList.remove("is-error");
    status.textContent = "Sending…";

    function done(ok, message) {
      status.textContent = message;
      if (!ok) status.classList.add("is-error");
      if (btn) btn.disabled = false;
      if (ok) form.reset();
    }

    if (isLocal) {
      setTimeout(function () {
        done(true, "Thank you — your enquiry is in. Our engineering team replies within one business day. (Local preview: nothing was sent.)");
      }, 400);
      return;
    }

    fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
      .then(function (r) { return r.json().catch(function () { return {}; }); })
      .then(function (res) {
        done(!!(res && res.ok), (res && res.ok)
          ? "Thank you — your enquiry is in. Our engineering team replies within one business day."
          : ((res && res.error) || "Something went wrong — please email us instead."));
      })
      .catch(function () {
        done(false, "Network error — please email liangjinhao0213@gmail.com instead.");
      });
  });
})();

/* ------------------------------------------------ ordering process (section 02) */
(function () {
  var root = document.querySelector("[data-flow]");
  if (!root) return;

  var nodes = [].slice.call(root.querySelectorAll("[data-flow-step]"));
  var panels = [].slice.call(root.querySelectorAll("[data-flow-panel]"));
  var shots = [].slice.call(root.querySelectorAll("[data-flow-shot]"));
  var fill = root.querySelector(".flow__rail-fill");
  var counter = root.querySelector("[data-flow-count]");
  var total = nodes.length;
  var index = 0;
  var timer = null;
  var DELAY = 4800;
  var paused = false;

  function render(next) {
    index = (next + total) % total;
    nodes.forEach(function (node, i) {
      node.classList.toggle("is-active", i === index);
      node.classList.toggle("is-done", i < index);
      node.setAttribute("aria-selected", i === index ? "true" : "false");
    });
    panels.forEach(function (panel, i) { panel.classList.toggle("is-active", i === index); });
    shots.forEach(function (shot, i) { shot.classList.toggle("is-active", i === index); });
    if (fill) fill.style.width = (total === 1 ? 0 : (index / (total - 1)) * 100) + "%";
    if (counter) counter.textContent = String(index + 1).padStart(2, "0") + " / " + String(total).padStart(2, "0");
  }

  function schedule() {
    window.clearInterval(timer);
    if (paused) return;
    timer = window.setInterval(function () { render(index + 1); }, DELAY);
  }

  nodes.forEach(function (node, i) {
    node.addEventListener("click", function () {
      render(i);
      schedule();
    });
  });

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!reduce) schedule();

  root.addEventListener("mouseenter", function () { paused = true; schedule(); });
  root.addEventListener("mouseleave", function () { paused = false; schedule(); });
  root.addEventListener("focusin", function () { paused = true; schedule(); });
  root.addEventListener("focusout", function () { paused = false; schedule(); });

  document.addEventListener("visibilitychange", function () {
    paused = document.hidden;
    schedule();
  });

  render(0);
})();

/* ------------------------------------------------ keep the spec bar inside the fold */
(function () {
  var bar = document.querySelector(".specbar");
  var hero = document.querySelector(".hero");
  var header = document.querySelector(".site-header");
  if (!bar) return;

  var ticking = false;

  function measure() {
    var barH = Math.round(bar.getBoundingClientRect().height);
    if (barH > 0) {
      document.documentElement.style.setProperty("--specbar-h", barH + "px");
    }
    if (hero) {
      var headerH = header ? Math.round(header.getBoundingClientRect().height) : 76;
      var target = Math.min(940, Math.max(440, window.innerHeight - headerH - barH));
      hero.style.minHeight = target + "px";
    }
    ticking = false;
  }

  function sync() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(measure);
  }

  sync();
  window.addEventListener("resize", sync, { passive: true });
  window.addEventListener("orientationchange", sync, { passive: true });
  window.addEventListener("load", sync);
  if ("ResizeObserver" in window) {
    new ResizeObserver(sync).observe(bar);
  }
})();
