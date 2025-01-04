document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.querySelector(".login form");
    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");

    loginForm.addEventListener("submit", (event) => {
        event.preventDefault(); // Prevent form submission

        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();

        if (!username || !password) {
            alert("Please enter both username and password!");
            return;
        }
        else{
            
        }
    });
});
