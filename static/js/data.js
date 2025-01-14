// script.js
document.addEventListener('DOMContentLoaded', function() {
    // Form submission handler
    const analysisForm = document.getElementById('analysis-form');
    if (analysisForm) {
        analysisForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(analysisForm);
            const submitBtn = document.getElementById('submit-btn');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Uploading...';
            
            fetch('/data-analysis', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showMessage('Analysis created successfully!', 'success');
                    location.reload();
                } else {
                    showMessage(data.message || 'Error creating analysis', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('Failed to create analysis', 'error');
            })
            .finally(() => {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Create Analysis';
            });
        });
    }

    // Initialize analysis actions
    setupAnalysisActions();

    // Function to handle analysis actions
    function setupAnalysisActions() {
        // View Analysis
        document.querySelectorAll('.view-btn').forEach(button => {
            button.addEventListener('click', function() {
                const analysisId = this.dataset.id;
                window.location.href = `/data-analysis/view/${analysisId}`;
            });
        });

        // Edit Analysis
        document.querySelectorAll('.edit-btn').forEach(button => {
            button.addEventListener('click', function() {
                const analysisId = this.dataset.id;
                editAnalysis(analysisId);
            });
        });

        // Delete Analysis
        document.querySelectorAll('.delete-btn').forEach(button => {
            button.addEventListener('click', function() {
                const analysisId = this.dataset.id;
                if (confirm('Are you sure you want to delete this analysis?')) {
                    deleteAnalysis(analysisId);
                }
            });
        });
    }

    // Function to edit analysis
    function editAnalysis(analysisId) {
        fetch(`/data-analysis/view/${analysisId}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('title').value = data.title;
                document.getElementById('description').value = data.description;
                document.getElementById('data-type').value = data.data_type;
                
                // Show edit form
                document.getElementById('form-title').textContent = 'Edit Analysis';
                document.getElementById('submit-btn').textContent = 'Update';
                // Add analysis ID to form
                const idInput = document.createElement('input');
                idInput.type = 'hidden';
                idInput.name = 'analysis_id';
                idInput.value = analysisId;
                analysisForm.appendChild(idInput);
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('Failed to load analysis details', 'error');
            });
    }

    // Function to delete analysis
    function deleteAnalysis(analysisId) {
        fetch(`/data-analysis/${analysisId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showMessage('Analysis deleted successfully!', 'success');
                location.reload();
            } else {
                showMessage(data.message || 'Error deleting analysis', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('Failed to delete analysis', 'error');
        });
    }

    // Function to show messages
    function showMessage(message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `flash-message ${type}`;
        messageDiv.textContent = message;
        
        const container = document.querySelector('.analysis-form');
        container.insertBefore(messageDiv, container.firstChild);
        
        // Remove message after 3 seconds
        setTimeout(() => messageDiv.remove(), 3000);
    }
});
  