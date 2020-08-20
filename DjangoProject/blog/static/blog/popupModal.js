const link = document.querySelector("#ref");
const modal = document.querySelector(".modal");
const close = document.querySelector(".modal-close");

link.addEventListener("click", function () {
    modal.classList.add("is-active");
});

close.addEventListener("click", function () {
    modal.classList.remove("is-active");
});