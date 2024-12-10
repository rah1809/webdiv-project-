// script.js
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("research-profile-form");
  
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      
      // Gather data from the form
      const studentId = document.getElementById("student-id").value;
      const university = document.getElementById("university").value;
      const researchTopic = document.getElementById("research-topic").value;
  
      // Log to console for testing
      console.log({
        studentId,
        university,
        researchTopic
      });
  
      alert("Profile saved successfully!");
    });
  });
  