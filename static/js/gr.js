// script.js
document.addEventListener("DOMContentLoaded", () => {
    // Initial data structures
    const projects = [
        { name: "AI in Healthcare", description: "Collaboration on healthcare solutions using AI." },
        { name: "Climate Change Analysis", description: "Studying the impacts of global warming." }
    ];
    
    const messages = [
        { user: "Alice", text: "Welcome to the group!" },
        { user: "Bob", text: "Thanks, Alice. Glad to be here." }
    ];

    // DOM Elements
    const projectList = document.getElementById("group-projects");
    const messageForm = document.getElementById("message-form");
    const messageInput = document.getElementById("message-input");
    const messagesDiv = document.getElementById("messages");
    const documentForm = document.getElementById("document-form");
    const fileInput = document.getElementById("file-upload");
    const fileList = document.getElementById("file-list");
    const documentsContainer = document.getElementById("documents");

    // Render group projects
    const renderProjects = () => {
        projectList.innerHTML = "";
        projects.forEach((project) => {
            const li = document.createElement("li");
            li.innerHTML = `<strong>${project.name}</strong><p>${project.description}</p>`;
            projectList.appendChild(li);
        });
    };

    // Render messages
    const renderMessages = () => {
        messagesDiv.innerHTML = "";
        messages.forEach((msg) => {
            const p = document.createElement("p");
            p.innerHTML = `<strong>${msg.user}:</strong> ${msg.text}`;
            messagesDiv.appendChild(p);
        });
    };

    // Helper function to format file size
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // Show selected files preview
    fileInput.addEventListener('change', function() {
        fileList.innerHTML = '';
        if (this.files.length > 0) {
            const list = document.createElement('ul');
            list.className = 'selected-files';
            
            Array.from(this.files).forEach(file => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <span class="file-name">${file.name}</span>
                    <span class="file-size">(${formatFileSize(file.size)})</span>
                `;
                list.appendChild(li);
            });
            
            fileList.appendChild(list);
        }
    });

    // Add message
    messageForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const message = messageInput.value;
        messages.push({ user: "You", text: message });
        renderMessages();
        messageInput.value = "";
    });

    // Handle document upload
    documentForm.addEventListener("submit", async function(e) {
        e.preventDefault();
        
        const files = fileInput.files;
        if (files.length === 0) {
            alert('Please select files to upload');
            return;
        }

        const formData = new FormData();
        Array.from(files).forEach(file => {
            formData.append('files[]', file);
        });

        try {
            const response = await fetch('/upload-documents', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            
            if (result.success) {
                fileInput.value = '';
                fileList.innerHTML = '';
                alert(`Successfully uploaded ${files.length} file(s)`);
                loadDocuments();
            } else {
                alert('Error uploading files: ' + result.message);
            }
        } catch (error) {
            console.error('Upload error:', error);
            alert('Error uploading files');
        }
    });

    // Load existing documents
    async function loadDocuments() {
        try {
            const response = await fetch('/get-documents');
            const documents = await response.json();
            
            documentsContainer.innerHTML = documents.length ? 
                documents.map(doc => `
                    <div class="document-item">
                        <span class="doc-name">${doc.name}</span>
                        <span class="doc-info">
                            Uploaded by: ${doc.uploaded_by} 
                            on ${new Date(doc.upload_date).toLocaleDateString()}
                        </span>
                        <a href="/download-document/${doc.id}" class="download-btn">Download</a>
                    </div>
                `).join('') : 
                '<p>No documents uploaded yet</p>';
        } catch (error) {
            console.error('Error loading documents:', error);
        }
    }

    // Initialize the page
    renderProjects();
    renderMessages();
    loadDocuments();
});
  