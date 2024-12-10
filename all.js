// script.js
document.addEventListener("DOMContentLoaded", () => {
    const menuLinks = document.querySelectorAll(".menu a");
    const pages = document.querySelectorAll(".page");
  
    menuLinks.forEach((link) => {
      link.addEventListener("click", (event) => {
        event.preventDefault();
  
        // Set active link
        menuLinks.forEach((link) => link.classList.remove("active"));
        link.classList.add("active");
  
        // Show corresponding page
        const pageId = link.getAttribute("data-page");
        pages.forEach((page) => {
          if (page.id === pageId) {
            page.classList.add("active");
          } else {
            page.classList.remove("active");
          }
        });
      });
    });
  });
  