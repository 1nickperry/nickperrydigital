(function () {
  var nav = document.querySelector("[data-nav]");
  var toggle = document.querySelector("[data-nav-toggle]");
  var drawer = document.querySelector("[data-nav-drawer]");
  if (toggle && drawer) {
    toggle.addEventListener("click", function () {
      var open = drawer.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      document.body.classList.toggle("nav-open", open);
    });
    drawer.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        drawer.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        document.body.classList.remove("nav-open");
      });
    });
  }

  if (nav) {
    var onScroll = function () {
      nav.classList.toggle("is-scrolled", window.scrollY > 12);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  document.querySelectorAll("[data-accordion] .faq-q").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var item = btn.closest(".faq-item");
      var open = item.classList.contains("is-open");
      item.parentElement.querySelectorAll(".faq-item").forEach(function (el) {
        el.classList.remove("is-open");
        var q = el.querySelector(".faq-q");
        if (q) q.setAttribute("aria-expanded", "false");
      });
      if (!open) {
        item.classList.add("is-open");
        btn.setAttribute("aria-expanded", "true");
      }
    });
  });

  var settingsUrl = (document.body.getAttribute("data-root") || ".") + "/content/settings.json";
  fetch(settingsUrl)
    .then(function (res) {
      return res.ok ? res.json() : null;
    })
    .then(function (settings) {
      if (!settings) return;
      document.querySelectorAll("[data-phone-display]").forEach(function (el) {
        el.textContent = settings.phoneDisplay;
      });
      document.querySelectorAll("[data-phone-href]").forEach(function (el) {
        el.setAttribute("href", settings.phoneHref);
      });
      document.querySelectorAll("[data-booking-href]").forEach(function (el) {
        el.setAttribute("href", settings.bookingUrl);
      });
      document.querySelectorAll("[data-booking-label]").forEach(function (el) {
        el.textContent = settings.bookingLabel;
      });
      document.querySelectorAll("[data-email-display]").forEach(function (el) {
        el.textContent = settings.emailDisplay;
      });
      document.querySelectorAll("[data-email-href]").forEach(function (el) {
        el.setAttribute("href", settings.emailHref);
      });
    })
    .catch(function () {
      /* Placeholders stay visible until settings load. */
    });

  var year = document.querySelector("[data-year]");
  if (year) year.textContent = String(new Date().getFullYear());

  var form = document.querySelector("[data-contact-form]");
  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var note = form.querySelector("[data-form-note]");
      if (note) {
        note.hidden = false;
        note.textContent =
          "This form is a placeholder until a booking link and form endpoint are connected. Use the booking placeholder or phone placeholder to reach Nick.";
      }
    });
  }
})();
