// script.js
document.addEventListener('DOMContentLoaded', function() {
    // Form submission handler
    const analysisForm = document.getElementById('analysis-form');
    if (analysisForm) {
        analysisForm.addEventListener('submit', function(e) {
            e.preventDefault();
            submitAnalysis();
        });
    }

    // Initialize analysis actions
    setupAnalysisActions();

    // Function to submit analysis
    function submitAnalysis() {
        const formData = new FormData(analysisForm);
        
        fetch('/data-analysis.html', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showMessage('Analysis created successfully!', 'success');
                location.reload(); // Reload to show new analysis
            } else {
                showMessage(data.message || 'Error creating analysis', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('Failed to create analysis', 'error');
        });
    }

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
                document.getElementById('analysis-form').style.display = 'block';
                document.getElementById('form-title').textContent = 'Edit Analysis';
                document.getElementById('submit-btn').textContent = 'Update';
            })
            .catch(error => console.error('Error:', error));
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
  