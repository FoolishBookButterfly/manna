/* =============================================================================
   MANNA — theme toggle
   -----------------------------------------------------------------------------
   Loaded synchronously in <head>, so the saved theme is applied to <html>
   BEFORE the first paint (no flash of the wrong colours). It then wires every
   [data-theme-toggle] button: a small moon/sun control in the cover corner and
   in the site header. The choice lives in localStorage under "manna-theme" and
   defaults to light — the OS preference is deliberately ignored.
   ============================================================================= */
(function () {
    "use strict";

    var KEY = "manna-theme";
    var root = document.documentElement;
    var timer = null;

    function read() {
        try {
            return window.localStorage.getItem(KEY) === "dark" ? "dark" : "light";
        } catch (e) {
            return "light";            /* private mode or storage disabled */
        }
    }

    function write(theme) {
        try { window.localStorage.setItem(KEY, theme); } catch (e) {}
    }

    /* Name each toggle after what it will DO: a moon while in light mode,
       a sun while in dark mode. Keeps aria-label honest without extra state. */
    function label(theme) {
        var text = theme === "dark" ? "Switch to light mode" : "Switch to dark mode";
        var buttons = document.querySelectorAll("[data-theme-toggle]");
        for (var i = 0; i < buttons.length; i++) {
            buttons[i].setAttribute("aria-label", text);
            buttons[i].setAttribute("title", text);
        }
    }

    function paint(theme) {
        root.setAttribute("data-theme", theme);   /* run before first paint */
        label(theme);
    }

    paint(read());

    function toggle() {
        var next = read() === "dark" ? "light" : "dark";

        /* Pin the current color-scheme while the switch runs. Flipping
           color-scheme mid-flight stalls Chrome's running colour transitions
           (they advance only when style is forced), so the pin is released
           together with .theme-anim once the crossfade has finished — by then
           every theme transition is complete, and CSS takes over again. */
        root.style.colorScheme = window.getComputedStyle(root).colorScheme || "light";

        /* Register the .theme-anim transition styles first (forced reflow),
           then flip the attribute, so the colours dissolve instead of snapping.
           The class is removed once the crossfade has finished, leaving
           ordinary hover/focus behaviour exactly as it was. */
        root.classList.add("theme-anim");
        void root.offsetWidth;
        root.setAttribute("data-theme", next);
        write(next);
        label(next);

        window.clearTimeout(timer);
        timer = window.setTimeout(function () {
            root.classList.remove("theme-anim");
            root.style.colorScheme = "";    /* hand the new scheme back to CSS */
        }, 800);
    }

    function wire() {
        var buttons = document.querySelectorAll("[data-theme-toggle]");
        for (var i = 0; i < buttons.length; i++) {
            buttons[i].addEventListener("click", toggle);
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", wire);
    } else {
        wire();
    }

    /* another tab switched the theme — follow along */
    window.addEventListener("storage", function (event) {
        if (event.key === KEY) { paint(read()); }
    });
}());
