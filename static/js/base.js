// Base JavaScript for the Website

// === Navigation Menu ===
// Highlight the active menu item based on the current URL
document.addEventListener("DOMContentLoaded", function () {
    const currentPath = window.location.pathname;
    const menuItems = document.querySelectorAll(".navbar .menu li a");

    menuItems.forEach((item) => {
        if (item.getAttribute("href") === currentPath) {
            item.classList.add("active");
        }
    });
});

// === Toggle Mobile Navigation ===
// (Optional) Add a hamburger menu toggle for mobile users
const mobileToggle = document.querySelector(".mobile-menu-toggle");
if (mobileToggle) {
    mobileToggle.addEventListener("click", function () {
        const menu = document.querySelector(".menu");
        menu.classList.toggle("open");
    });
}

// === Display Notifications (Toast System) ===
function showNotification(message, type = "info") {
    // Create notification element
    const notification = document.createElement("div");
    notification.className = `notification ${type}`;
    notification.textContent = message;

    // Append to the body
    document.body.appendChild(notification);

    // Remove the notification after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Example usage of the notification system
// showNot
