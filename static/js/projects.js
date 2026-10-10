/* =========================================
   NAYAA - PROJECTS PAGE JAVASCRIPT
========================================= */

document.addEventListener("DOMContentLoaded", function () {
    "use strict";

    /* -----------------------------------------
       PROJECT CARD SCROLL ANIMATION
    ----------------------------------------- */

    const projectCards = document.querySelectorAll(".project-card");

    if (projectCards.length > 0) {

        // Initial state
        projectCards.forEach(function (card) {
            card.style.opacity = "0";
            card.style.transform = "translateY(30px)";
            card.style.transition =
                "opacity 0.6s ease, transform 0.6s ease";
        });

        // Reveal cards when they enter the screen
        const cardObserver = new IntersectionObserver(
            function (entries, observer) {

                entries.forEach(function (entry) {

                    if (entry.isIntersecting) {

                        entry.target.style.opacity = "1";
                        entry.target.style.transform = "translateY(0)";

                        observer.unobserve(entry.target);
                    }
                });

            },
            {
                threshold: 0.15
            }
        );

        projectCards.forEach(function (card) {
            cardObserver.observe(card);
        });
    }


    /* -----------------------------------------
       HERO CONTENT ANIMATION
    ----------------------------------------- */

    const heroContent = document.querySelector(".projects-hero-content");

    if (heroContent) {

        heroContent.style.opacity = "0";
        heroContent.style.transform = "translateY(25px)";
        heroContent.style.transition =
            "opacity 0.8s ease, transform 0.8s ease";

        setTimeout(function () {
            heroContent.style.opacity = "1";
            heroContent.style.transform = "translateY(0)";
        }, 150);
    }


    /* -----------------------------------------
       PROJECT CARD HOVER EFFECT
    ----------------------------------------- */

    projectCards.forEach(function (card) {

        card.addEventListener("mouseenter", function () {

            const image = card.querySelector("img");

            if (image) {
                image.style.transform = "scale(1.05)";
                image.style.transition = "transform 0.4s ease";
            }
        });


        card.addEventListener("mouseleave", function () {

            const image = card.querySelector("img");

            if (image) {
                image.style.transform = "scale(1)";
            }
        });
    });


    /* -----------------------------------------
       SUPPORT BUTTON CLICK FEEDBACK
    ----------------------------------------- */

    const supportLinks = document.querySelectorAll(
        ".project-card a, .projects-hero-btn"
    );

    supportLinks.forEach(function (link) {

        link.addEventListener("click", function () {

            link.style.opacity = "0.7";

            setTimeout(function () {
                link.style.opacity = "1";
            }, 250);
        });
    });


    /* -----------------------------------------
       SMOOTH SCROLL
    ----------------------------------------- */

    document.querySelectorAll('a[href^="#"]').forEach(function (link) {

        link.addEventListener("click", function (event) {

            const targetId = this.getAttribute("href");

            if (targetId === "#") {
                return;
            }

            const target = document.querySelector(targetId);

            if (target) {

                event.preventDefault();

                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });
            }
        });
    });

});