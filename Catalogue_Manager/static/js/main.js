document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('catalogueForm');
    const msg = document.getElementById('msg');
    const action = window.action || null;
    const catalogue = window.catalogueData || null;

    // Prefill form in update mode
    if (action === 'Update' && catalogue) {
        document.getElementById('catalogue_id').value = catalogue.catalogue_id;
        document.getElementById('catalogue_name').value = catalogue.catalogue_name;
        document.getElementById('catalogue_version').value = catalogue.catalogue_version;
        document.getElementById('is_cat_active').value = catalogue.is_cat_active ? '1' : '0';
        document.getElementById('catalogue_start').value = catalogue.catalogue_start;
        document.getElementById('catalogue_end').value = catalogue.catalogue_end;
    }

    // Handle form submit for Create/Update
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const data = {
                catalogue_id: document.getElementById('catalogue_id').value,
                catalogue_name: document.getElementById('catalogue_name').value,
                catalogue_version: document.getElementById('catalogue_version').value,
                is_cat_active: document.getElementById('is_cat_active').value,
                catalogue_start: document.getElementById('catalogue_start').value,
                catalogue_end: document.getElementById('catalogue_end').value
            };

            const method = action === 'Update' ? 'PUT' : 'POST';
            const url = method === 'PUT'
                ? `/api/catalogues/${data.catalogue_id}`
                : `/api/catalogues`;

            try {
                const res = await fetch(url, {
                    method,
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const result = await res.json();
                msg.innerText = result.message || result.error;
                msg.style.color = result.message ? 'green' : 'red';
                if (method === 'POST' && result.message) form.reset();
            } catch (err) {
                msg.innerText = 'Something went wrong.';
                msg.style.color = 'red';
            }
        });
    }

    // Load all catalogues on the index page
 const indexContainer = document.getElementById('catalogueList');
    if (indexContainer) {
        fetch('/api/catalogues')
            .then(res => res.json())
            .then(data => {
                indexContainer.innerHTML = '';
                if (data.length === 0) {
                    indexContainer.innerHTML = '<p>No catalogues found.</p>';
                } else {
                    data.forEach(cat => {
                        const item = document.createElement('div');
                        item.className = 'catalogue';
                        item.innerHTML = `
                            <span><strong>${cat.catalogue_name}</strong> (ID: ${cat.catalogue_id})</span>
                            <span>
                                <a href="/view/${cat.catalogue_id}" class="btn btn-info">View</a>
                                <a href="/update/${cat.catalogue_id}" class="btn btn-warning">Update</a>
                                <button class="btn btn-danger" onclick="deleteCatalogue(${cat.catalogue_id})">Delete</button>
                            </span>
                        `;
                        indexContainer.appendChild(item);
                    });
                }
            })
            .catch(err => {
                console.error("Failed to load catalogues:", err);
                indexContainer.innerHTML = '<p>Error loading catalogues. Please ensure the backend is running.</p>';
            });
    }
});


// Delete handler
function deleteCatalogue(id) {
    if (!confirm("Are you sure you want to delete this catalogue?")) return;
    fetch(`/api/catalogues/${id}`, { method: 'DELETE' })
        .then(res => res.json())
        .then(result => {
            alert(result.message || result.error);
            window.location.reload();
        });
}
