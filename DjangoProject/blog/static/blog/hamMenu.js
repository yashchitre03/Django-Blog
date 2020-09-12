/**
 * Opens or closes the hamburger menu when the icon is clicked.
 */

const menuButton = document.querySelector(".navbar-burger");
const menu = document.querySelector(".navbar-menu");
menuButton.addEventListener("click", function () {
    menu.classList.toggle("is-active");
});
