// script.js
document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("login-form");

  loginForm.addEventListener("submit", (event) => {
    event.preventDefault();

    // Capture input values
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // Log to console (replace this with server-side validation)
    console.log({
      username,
      password
    });

    // Simple validation (you should replace this with a server-side check)
    if (username === "testuser" && password === "password123") {
      alert("Login successful!");
      window.location.href = "dashboard.html";
    } else {
      alert("Invalid username or password!");
    }
  });
});
