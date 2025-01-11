// script.js
document.addEventListener("DOMContentLoaded", () => {
    const libraryItems = [
      {
        title: "AI in Healthcare",
        author: "John Doe",
        description: "Exploring AI applications in healthcare diagnostics."
      },
      {
        title: "Climate Change and Its Effects",
        author: "Jane Smith",
        description: "A deep dive into climate change impacts on ecosystems."
      }
    ];
  
    const libraryList = document.getElementById("library-items");
    const addResourceForm = document.getElementById("add-resource-form");
    const searchInput = document.getElementById("search-input");
  
    // Function to display resources
    const renderLibraryItems = (items) => {
      libraryList.innerHTML = "";
      items.forEach((item, index) => {
        const li = document.createElement("li");
        li.innerHTML = `
          <strong>${item.title}</strong> by ${item.author}
          <p>${item.description}</p>
        `;
        libraryList.appendChild(li);
      });
    };
  
    // Add new resource
    addResourceForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const title = document.getElementById("resource-title").value;
      const author = document.getElementById("resource-author").value;
      const description = document.getElementById("resource-description").value;
  
      libraryItems.push({ title, author, description });
      renderLibraryItems(libraryItems);
      addResourceForm.reset();
    });
  
    // Search resources
    searchInput.addEventListener("input", (e) => {
      const query = e.target.value.toLowerCase();
      const filteredItems = libraryItems.filter(
        (item) =>
          item.title.toLowerCase().includes(query) ||
          item.author.toLowerCase().includes(query)
      );
      renderLibraryItems(filteredItems);
    });
  
    // Initial render
    renderLibraryItems(libraryItems);
  });
  