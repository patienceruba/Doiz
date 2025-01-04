document.addEventListener('DOMContentLoaded', () => {
    const viewList = document.querySelector('.view-list ul');

    // Handle delete button click
    viewList.addEventListener('click', (event) => {
        if (event.target.classList.contains('del-btn')) {
            const listItem = event.target.closest('li');
            listItem.remove();
            alert('Item deleted successfully!');
        }
    });

    // Handle update button click
    viewList.addEventListener('click', (event) => {
        if (event.target.classList.contains('up-btn')) {
            const listItem = event.target.closest('li');
            const newName = prompt('Enter new name:', listItem.textContent.trim());
            if (newName) {
                listItem.firstChild.textContent = newName;
                alert('Item updated successfully!');
            }
        }
    });
});
document.addEventListener("DOMContentLoaded", function () {
    // Simulate the login state (replace this with actual logic to check login state)
    const isLoggedIn = true; // Change to false to simulate a logged-out user

    const loginLink = document.getElementById("login-btn");
    const logoutLink = document.getElementById("logout-btn");

    if (isLoggedIn) {
        // Hide the login link if the user is logged in
        loginLink.style.display = "none";
    } else {
        // Hide the logout link if the user is not logged in
        logoutLink.style.display = "none";
    }
});
