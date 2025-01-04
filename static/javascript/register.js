document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.querySelector(".register form");

    registerForm.addEventListener("submit", (event) => {
        event.preventDefault(); // Prevent form submission

        const firstName = document.getElementById("f-name").value.trim();
        const lastName = document.getElementById("l-name").value.trim();
        const username = document.getElementById("username").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("password1").value;
        const termsChecked = registerForm.querySelector('input[type="checkbox"]').checked;

        // Validation
        if (!firstName || !lastName || !username || !email || !password || !confirmPassword) {
            alert("Please fill out all fields.");
            return;
        }

        if (!termsChecked) {
            alert("You must agree to the terms and conditions.");
            return;
        }

        if (password !== confirmPassword) {
            alert("Passwords do not match.");
            return;
        }

        // Replace the following code with an actual API call to the Django backend
        console.log({
            firstName,
            lastName,
            username,
            email,
            password,
        });

        alert("Registration successful!");
        window.location.href = "loginpage.html"; // Redirect to the login page
    });
});
