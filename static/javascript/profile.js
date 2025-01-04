document.addEventListener("DOMContentLoaded", () => {
    const usernameDisplay = document.getElementById("username-display");
    const emailDisplay = document.getElementById("email-display");
    const tasksCountDisplay = document.getElementById("tasks-count");

    // Example data - replace with dynamic values from your app
    const userData = {
        username: "JaneDoe",
        email: "janedoe@example.com",
        tasksCount: 10,
    };

    // Update the profile section dynamically
    usernameDisplay.textContent = userData.username;
    emailDisplay.textContent = userData.email;
    tasksCountDisplay.textContent = userData.tasksCount;
});
