/* =========================================
   NAYAA - ABOUT PAGE JAVASCRIPT
========================================= */

document.addEventListener("DOMContentLoaded", function () {
    "use strict";

    // Reveal sections as the user scrolls
    const revealElements = document.querySelectorAll(
        ".about-mission-card, .about-value-card, .about-person"
    );

    if ("IntersectionObserver" in window) {
        revealElements.forEach(function (element) {
            element.classList.add("about-reveal");
        });

        const observer = new IntersectionObserver(
            function (entries, currentObserver) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("about-visible");
                        currentObserver.unobserve(entry.target);
                    }
                });
            },
            {
                threshold: 0.15
            }
        );

        revealElements.forEach(function (element) {
            observer.observe(element);
        });
    }
});