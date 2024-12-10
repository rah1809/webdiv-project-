document.addEventListener("DOMContentLoaded", () => {
  const projects = [];
  const projectList = document.getElementById("project-list");
  const form = document.getElementById("add-project-form");

  const renderProjects = () => {
    projectList.innerHTML = "";
    projects.forEach((project) => {
      const li = document.createElement("li");
      li.textContent = ${project.title}: ${project.description};
      projectList.appendChild(li);
    });
  };

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const title = document.getElementById("project-title").value;
    const description = document.getElementById("project-description").value;
    projects.push({ title, description });
    renderProjects();
    form.reset();
  });
});
