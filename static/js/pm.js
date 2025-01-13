document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('participant-search');
    const searchResults = document.getElementById('search-results');
    const selectedParticipants = document.getElementById('selected-participants');
    const participantIds = document.getElementById('participant-ids');
    
    let selectedUsers = new Set();

    searchInput.addEventListener('input', debounce(async function() {
        if (this.value.length < 2) {
            searchResults.innerHTML = '';
            return;
        }

        try {
            const response = await fetch(`/search-researchers?q=${encodeURIComponent(this.value)}`);
            const researchers = await response.json();
            
            searchResults.innerHTML = researchers.map(r => `
                <div class="researcher-item" data-id="${r.personal_info.researcher_id}">
                    <span class="name">${r.personal_info.full_name}</span>
                    <span class="id">(${r.personal_info.researcher_id})</span>
                    <span class="position">${r.academic_info.academic_position}</span>
                </div>
            `).join('');
        } catch (error) {
            console.error('Error searching researchers:', error);
        }
    }, 300));

    searchResults.addEventListener('click', function(e) {
        const item = e.target.closest('.researcher-item');
        if (!item) return;

        const id = item.dataset.id;
        if (selectedUsers.has(id)) return;

        selectedUsers.add(id);
        const name = item.querySelector('.name').textContent;
        
        selectedParticipants.insertAdjacentHTML('beforeend', `
            <div class="selected-participant" data-id="${id}">
                ${name}
                <button type="button" class="remove-participant">&times;</button>
            </div>
        `);
        
        participantIds.value = Array.from(selectedUsers).join(',');
        searchInput.value = '';
        searchResults.innerHTML = '';
    });

    selectedParticipants.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-participant')) {
            const participant = e.target.parentElement;
            selectedUsers.delete(participant.dataset.id);
            participant.remove();
            participantIds.value = Array.from(selectedUsers).join(',');
        }
    });
});

function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
} 