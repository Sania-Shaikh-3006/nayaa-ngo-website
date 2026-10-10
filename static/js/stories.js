/* ==========================================
   NAYAA - PEOPLE'S STORIES
   Card entrance animation
========================================== */

document.addEventListener("DOMContentLoaded", function () {
    "use strict";

    const storyCards = document.querySelectorAll(".people-story-card");

    if (!storyCards.length) {
        return;
    }

    // Add a small stagger between cards.
    storyCards.forEach(function (card, index) {
        card.style.animationDelay = `${index * 120}ms`;
        card.classList.add("story-visible");
    });

    // Check for missing images and mark them for debugging.
    const storyImages = document.querySelectorAll(".people-story-photo img");

    storyImages.forEach(function (img) {
        img.addEventListener("error", function () {
            img.parentElement.classList.add("image-missing");
            console.warn("Story image could not be loaded:", img.src);
        });
    });
});