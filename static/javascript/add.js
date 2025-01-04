document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const titleInput = document.getElementById("title");
    const messageInput = document.getElementById("message");
    const startingInput = document.getElementById("starting");
    const endingInput =document.getElementById("ending")

    form.addEventListener("submit", (event) => {

        const title = titleInput.value.trim();
        const message = messageInput.value.trim();

        if (!title || !message ||) {
            alert("Please fill in both the title and description.");
            return;
        }
    });
});
