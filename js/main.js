(function () {
  var root = document.documentElement;
  var reduce = root.classList.contains("reduce-motion");

  function initReducedDemos() {
    if (!reduce) return;
    document.querySelectorAll("img.demo").forEach(function (img) {
      var live = img.getAttribute("src");
      var poster = img.getAttribute("data-poster");
      if (!live || !poster) return;
      img.dataset.gif = live;
      img.setAttribute("src", poster);
      var figure = img.closest("figure");
      var button = figure && figure.querySelector(".play-demo");
      if (!button) return;
      button.hidden = false;
      button.addEventListener("click", function () {
        img.src = img.dataset.gif;
        button.hidden = true;
      });
    });
  }

  function initIntro() {
    var intro = document.getElementById("intro");
    if (!intro || !root.classList.contains("play-intro")) return;
    var page = document.getElementById("page");
    var skip = document.getElementById("skip-intro");
    var heading = document.querySelector("h1");
    if (page) page.inert = true;

    var done = false;
    function finish() {
      if (done) return;
      done = true;
      intro.classList.add("is-leaving");
      root.classList.remove("play-intro");
      if (page) page.inert = false;
      try {
        sessionStorage.setItem("lj-intro-seen", "1");
      } catch (e) {}
      window.setTimeout(function () {
        intro.hidden = true;
      }, 700);
      if (heading) {
        heading.setAttribute("tabindex", "-1");
        heading.focus({ preventScroll: true });
      }
    }

    var timer = window.setTimeout(finish, 4200);
    if (skip) {
      skip.addEventListener("click", function () {
        window.clearTimeout(timer);
        finish();
      });
    }
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && !done && root.classList.contains("play-intro")) {
        window.clearTimeout(timer);
        finish();
      }
    });
    var contentSkip = document.querySelector(".skip-link");
    if (contentSkip) contentSkip.addEventListener("click", finish);
    if (skip) skip.focus({ preventScroll: true });
  }

  function initHeader() {
    var header = document.querySelector(".site-header");
    if (!header) return;
    function onScroll() {
      header.classList.toggle("is-scrolled", window.scrollY > 12);
    }
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  function initNav() {
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.getElementById("site-nav");
    if (!toggle || !nav) return;
    var home = nav.parentElement;
    var slot = nav.nextSibling;
    function restore() {
      if (home && nav.parentElement !== home) home.insertBefore(nav, slot);
    }
    function close() {
      nav.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
      document.body.classList.remove("nav-open");
      restore();
    }
    function open() {
      document.body.appendChild(nav);
      nav.classList.add("is-open");
      toggle.setAttribute("aria-expanded", "true");
      document.body.classList.add("nav-open");
    }
    toggle.addEventListener("click", function () {
      if (nav.classList.contains("is-open")) close();
      else open();
    });
    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function (event) {
        var href = link.getAttribute("href") || "";
        if (href.charAt(0) !== "#") {
          close();
          return;
        }
        var target = document.querySelector(href);
        if (!target) return;
        event.preventDefault();
        close();
        target.scrollIntoView({ behavior: reduce ? "auto" : "smooth" });
        if (history.replaceState) history.replaceState(null, "", href);
      });
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") close();
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 760) close();
    });
  }

  function initReveal() {
    var nodes = document.querySelectorAll(".reveal");
    if (!nodes.length) return;
    if (reduce || !("IntersectionObserver" in window)) {
      nodes.forEach(function (node) {
        node.classList.add("is-in");
      });
      return;
    }
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-in");
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.14, rootMargin: "0px 0px -6% 0px" }
    );
    nodes.forEach(function (node) {
      observer.observe(node);
    });
  }

  function initNowShowing() {
    var label = document.getElementById("now-showing");
    var nav = document.getElementById("site-nav");
    if (!label || !("IntersectionObserver" in window)) return;
    var navFor = {
      top: null,
      projects: "projects",
      "credit-risk": "projects",
      "loan-approval": "projects",
      "fraud-review": "projects",
      "also-showing": "projects",
      skills: "skills",
      about: "about",
      contact: "contact"
    };
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var name = entry.target.getAttribute("data-now");
          if (name) label.textContent = "Now showing · " + name;
          if (!nav) return;
          var key = navFor[entry.target.id];
          nav.querySelectorAll("a[href^='#']").forEach(function (link) {
            if (key && link.getAttribute("href") === "#" + key) {
              link.setAttribute("aria-current", "true");
            } else {
              link.removeAttribute("aria-current");
            }
          });
        });
      },
      { rootMargin: "-45% 0px -48% 0px", threshold: 0 }
    );
    document.querySelectorAll("[data-now]").forEach(function (section) {
      observer.observe(section);
    });
  }

  function initTilt() {
    if (reduce || !window.matchMedia("(hover: hover) and (pointer: fine)").matches) return;
    document.querySelectorAll(".tilt").forEach(function (card) {
      var max = card.classList.contains("reel") ? 3.5 : 6.5;
      card.addEventListener("mousemove", function (event) {
        var rect = card.getBoundingClientRect();
        var px = (event.clientX - rect.left) / rect.width;
        var py = (event.clientY - rect.top) / rect.height;
        card.style.setProperty("--ry", ((px - 0.5) * max).toFixed(2) + "deg");
        card.style.setProperty("--rx", ((0.5 - py) * max).toFixed(2) + "deg");
        card.style.setProperty("--mx", (px * 100).toFixed(1) + "%");
        card.style.setProperty("--my", (py * 100).toFixed(1) + "%");
      });
      card.addEventListener("mouseleave", function () {
        card.style.setProperty("--ry", "0deg");
        card.style.setProperty("--rx", "0deg");
      });
    });
  }

  function initParallax() {
    if (reduce) return;
    var nodes = Array.prototype.slice.call(document.querySelectorAll("[data-parallax]"));
    if (!nodes.length) return;
    var ticking = false;
    function update() {
      ticking = false;
      var mid = window.innerHeight * 0.5;
      nodes.forEach(function (el) {
        var rect = el.getBoundingClientRect();
        var delta = (rect.top + rect.height * 0.5 - mid) / window.innerHeight;
        var shift = Math.max(-20, Math.min(20, -delta * 28));
        el.style.transform = "translate3d(0," + shift.toFixed(2) + "px,0)";
      });
    }
    function requestUpdate() {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(update);
    }
    update();
    window.addEventListener("scroll", requestUpdate, { passive: true });
    window.addEventListener("resize", requestUpdate);
  }

  initReducedDemos();
  initIntro();
  initHeader();
  initNav();
  initReveal();
  initNowShowing();
  initTilt();
  initParallax();
})();
