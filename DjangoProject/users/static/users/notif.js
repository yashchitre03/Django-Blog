var closeNotif = document.querySelector(".delete");
if (closeNotif !== null) {
    closeNotif.addEventListener("click", function () {
        const notif = document.querySelector(".notification");
        notif.remove();
    });
}