document.addEventListener("DOMContentLoaded", function () {
    console.log("Ride Connect Loaded");

    // Navbar Scroll Effect
    window.addEventListener("scroll", function () {
        let navbar = document.querySelector(".navbar");
        if (window.scrollY > 50) {
            navbar.style.background = "#0056b3";
        } else {
            navbar.style.background = "rgba(0, 123, 255, 0.9)";
        }
    });
});
