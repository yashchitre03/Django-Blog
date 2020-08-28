const title = document.querySelector(".message-header");
if (title !== null) {
    title.innerHTML = "<p>Invalid credentials</p>" + title.innerHTML
}

const closeMsg = document.querySelector(".delete");
if (closeMsg !== null) {
    closeMsg.addEventListener("click", function () {
        const msg = document.querySelector(".message");
        msg.remove();
    });
}

