document.getElementById('loginForm').addEventListener('submit', async (e) => {
  e.preventDefault(); // Prevent default form submission

  // Capture username and password from form
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  try {
      // Send form data to Flask backend
      const response = await fetch('/login', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: `username=${username}&password=${password}`
      });

      const result = await response.json();
      
      if (result.status === 'success') {
          alert(result.message); // Success alert
          window.location.href = "/dashboard"; // Redirect to dashboard
      } else {
          alert(result.message); // Error alert
      }
  } catch (error) {
      console.error("Error:", error);
  }
});
