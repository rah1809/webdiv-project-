// script.js
document.addEventListener("DOMContentLoaded", () => {
    // Example project list
    const projects = [
      { id: 1, title: "AI in Healthcare" },
      { id: 2, title: "Climate Change Effects" },
      { id: 3, title: "Quantum Computing Applications" }
    ];
  
    // Populate the research project list
    const projectListElement = document.getElementById("project-list");
    projects.forEach(project => {
      const li = document.createElement("li");
      li.textContent = project.title;
      li.dataset.projectId = project.id;
      projectListElement.appendChild(li);
    });
  
    // Handle click events on project list items
    projectListElement.addEventListener("click", (event) => {
      if (event.target.tagName === "LI") {
        const projectTitle = event.target.textContent;
        document.getElementById("current-research-title").textContent = projectTitle;
      }
    });
  });
  