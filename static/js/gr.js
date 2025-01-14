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

    // Helper Functions
    const showLoading = (isLoading) => {
        const uploadButton = documentForm.querySelector('button[type="submit"]');
        uploadButton.disabled = isLoading;
        uploadButton.textContent = isLoading ? 'Uploading...' : 'Upload Files';
    };

    const showNotification = (message, type = 'info') => {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 3000);
    };

    const validateFiles = (files) => {
        const maxSize = 10 * 1024 * 1024; // 10MB
        const validMimeTypes = [
            'application/pdf',
            'application/x-pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document', // .docx
            'text/plain',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' // .xlsx
        ];
        
        const validExtensions = ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx'];
        
        for (const file of files) {
            if (file.size > maxSize) {
                throw new Error(`File ${file.name} is too large. Maximum size is 10MB`);
            }
            
            // Check both MIME type and file extension
            const fileExtension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'));
            if (!validMimeTypes.includes(file.type) && !validExtensions.includes(fileExtension)) {
                throw new Error(`File ${file.name} has invalid type. Allowed types: PDF, DOC, DOCX, TXT, XLS, XLSX`);
            }
        }
    };

    const formatFileSize = (bytes) => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    // Render Functions
    const renderProjects = () => {
        projectList.innerHTML = "";
        projects.forEach((project) => {
            const li = document.createElement("li");
            li.innerHTML = `<strong>${project.name}</strong><p>${project.description}</p>`;
            projectList.appendChild(li);
        });
    };

    const renderMessages = () => {
        messagesDiv.innerHTML = "";
        messages.forEach((msg) => {
            const p = document.createElement("p");
            p.innerHTML = `<strong>${msg.user}:</strong> ${msg.text}`;
            messagesDiv.appendChild(p);
        });
        // Auto-scroll to latest message
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    };

    // Event Listeners
    fileInput.addEventListener('change', function() {
        fileList.innerHTML = '';
        if (this.files.length > 0) {
            try {
                validateFiles(this.files);
                
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
            } catch (error) {
                showNotification(error.message, 'error');
                fileInput.value = ''; // Clear invalid selection
            }
        }
    });

    messageForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const message = messageInput.value.trim();
        if (!message) {
            showNotification('Please enter a message', 'error');
            return;
        }
        messages.push({ user: "You", text: message });
        renderMessages();
        messageInput.value = "";
    });

    documentForm.addEventListener("submit", async function(e) {
        e.preventDefault();
        
        const files = fileInput.files;
        if (files.length === 0) {
            showNotification('Please select files to upload', 'error');
            return;
        }

        try {
            validateFiles(files);
            showLoading(true);

            const formData = new FormData();
            Array.from(files).forEach(file => {
                formData.append('files[]', file);
            });

            const response = await fetch('/upload-documents', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            
            if (result.success) {
                fileInput.value = '';
                fileList.innerHTML = '';
                showNotification(`Successfully uploaded ${files.length} file(s)`, 'success');
                loadDocuments();
            } else {
                showNotification(result.message || 'Upload failed', 'error');
            }
        } catch (error) {
            console.error('Upload error:', error);
            showNotification(error.message || 'Error uploading files', 'error');
        } finally {
            showLoading(false);
        }
    });

    async function loadDocuments() {
        try {
            const response = await fetch('/get-documents');
            if (!response.ok) {
                throw new Error('Failed to fetch documents');
            }
            
            const documents = await response.json();
            
            documentsContainer.innerHTML = documents.length ? 
                documents.map(doc => `
                    <div class="document-item">
                        <span class="doc-name">${doc.name}</span>
                        <span class="doc-info">
                            Uploaded by: ${doc.uploaded_by} 
                            on ${new Date(doc.upload_date).toLocaleDateString()}
                        </span>
                        <div class="document-actions">
                            <a href="/download-document/${doc.id}" class="download-btn">Download</a>
                            ${doc.can_delete ? `<button onclick="deleteDocument('${doc.id}')" class="delete-btn">Delete</button>` : ''}
                        </div>
                    </div>
                `).join('') : 
                '<p>No documents uploaded yet</p>';
        } catch (error) {
            console.error('Error loading documents:', error);
            showNotification('Failed to load documents', 'error');
        }
    }

    // Delete document function
    window.deleteDocument = async function(docId) {
        if (!confirm('Are you sure you want to delete this document?')) {
            return;
        }

        try {
            const response = await fetch(`/delete-document/${docId}`, {
                method: 'DELETE'
            });
            
            const result = await response.json();
            
            if (result.success) {
                showNotification('Document deleted successfully', 'success');
                loadDocuments();
            } else {
                showNotification(result.message || 'Failed to delete document', 'error');
            }
        } catch (error) {
            console.error('Delete error:', error);
            showNotification('Error deleting document', 'error');
        }
    };

    // Initialize the page
    renderProjects();
    renderMessages();
    loadDocuments();
});
  