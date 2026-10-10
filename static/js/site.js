document.addEventListener("DOMContentLoaded", function () {

    const popup = document.getElementById("donationPopup");

    // If there is no popup on the current page, do nothing
    if (!popup) {
        return;
    }

    // -----------------------------------------------------
    // KEEP POPUP HIDDEN WHEN WEBSITE FIRST OPENS
    // -----------------------------------------------------

    popup.style.setProperty("display", "none", "important");


    // -----------------------------------------------------
    // SHOW POPUP AFTER 3 SECONDS
    // -----------------------------------------------------

    setTimeout(function () {

        const currentPopup = document.getElementById("donationPopup");

        if (currentPopup) {
            currentPopup.style.setProperty(
                "display",
                "flex",
                "important"
            );
        }

    }, 3000);

});
