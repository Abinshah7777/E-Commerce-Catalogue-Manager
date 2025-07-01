function showHomeOptions() {
    const container = document.getElementById('catalogueList');
    container.innerHTML = `
        <p style="margin-top: 2rem;">Use the options above to manage catalogues.</p>
    `;
    document.getElementById('homeBtn').style.display = 'none';  // Hide Home on home page
}

function showCreateForm() {
    document.getElementById('homeBtn').style.display = 'inline-block';

    const formHtml = `
        <h3>Add New Catalogue</h3>
        <form id="catalogueForm">
            <input type="number" id="catalogue_id" placeholder="ID" required><br>
            <input type="text" id="catalogue_name" placeholder="Name" required><br>
            <input type="text" id="catalogue_version" placeholder="Version" required><br>
            <select id="is_cat_active">
                <option value="1">Active</option>
                <option value="0">Inactive</option>
            </select><br>
            <input type="date" id="catalogue_start" required><br>
            <input type="date" id="catalogue_end" required><br>
            <button type="submit">Submit</button>
        </form>
        <div id="msg" class="message-box"></div>
    `;
    document.getElementById('catalogueList').innerHTML = formHtml;

    const form = document.getElementById('catalogueForm');
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

        try {
            const res = await fetch('/api/catalogues', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await res.json();
            const msgBox = document.getElementById('msg');
            msgBox.innerText = result.message || result.error;
            msgBox.style.color = result.success ? 'green' : 'red';
            if (result.success) form.reset();
        } catch (err) {
            const msgBox = document.getElementById('msg');
            msgBox.innerText = 'Something went wrong.';
            msgBox.style.color = 'red';
        }
    });
}

function fetchAllCatalogues() {
    document.getElementById('homeBtn').style.display = 'inline-block';

    fetch('/api/catalogues')
        .then(res => res.json())
        .then(response => {
            const container = document.getElementById('catalogueList');
            container.innerHTML = '';
            if (!response.success || response.data.length === 0) {
                container.innerHTML = '<p>No catalogues found.</p>';
            } else {
                response.data.forEach(cat => {
                    const div = document.createElement('div');
                    div.className = 'catalogue';
                    div.innerHTML = `
                        <p><strong>${cat.catalogue_name}</strong> (ID: ${cat.catalogue_id})</p>
                        <p>Version: ${cat.catalogue_version}, Status: ${cat.is_cat_active ? "Active" : "Inactive"}</p>
                        <p>Start: ${cat.catalogue_start}, End: ${cat.catalogue_end}</p>
                        <button onclick="editCatalogue(${cat.catalogue_id})">✏️ Update</button>
                        <button onclick="deleteCatalogue(${cat.catalogue_id})">🗑️ Delete</button>
                        <hr>
                    `;
                    container.appendChild(div);
                });
            }
        })
        .catch(err => {
            document.getElementById('catalogueList').innerHTML = '<p>Error loading catalogues.</p>';
        });
}

function promptViewById() {
    const id = prompt("Enter Catalogue ID to view:");
    if (!id) {
        document.getElementById('homeBtn').style.display = 'none';  // Hide if cancelled
        return;
    }

    document.getElementById('homeBtn').style.display = 'inline-block';

    fetch(`/api/catalogues/${id}`)
        .then(res => res.json())
        .then(response => {
            if (!response.success) {
                alert(response.error);
            } else {
                const cat = response.data;
                document.getElementById('catalogueList').innerHTML = `
                    <h3>Catalogue Details</h3>
                    <p><strong>${cat.catalogue_name}</strong> (ID: ${cat.catalogue_id})</p>
                    <p>Version: ${cat.catalogue_version}</p>
                    <p>Status: ${cat.is_cat_active ? "Active" : "Inactive"}</p>
                    <p>Start: ${cat.catalogue_start}</p>
                    <p>End: ${cat.catalogue_end}</p>
                    <button onclick="editCatalogue(${cat.catalogue_id})">✏️ Update</button>
                    <button onclick="deleteCatalogue(${cat.catalogue_id})">🗑️ Delete</button>
                `;
            }
        });
}

function editCatalogue(id) {
    document.getElementById('homeBtn').style.display = 'inline-block';

    fetch(`/api/catalogues/${id}`)
        .then(res => res.json())
        .then(response => {
            if (!response.success) {
                alert(response.error);
                return;
            }

            const cat = response.data;

            const formHtml = `
                <h3>Update Catalogue</h3>
                <form id="catalogueForm">
                    <input type="text" id="catalogue_name" value="${cat.catalogue_name}" required><br>
                    <input type="text" id="catalogue_version" value="${cat.catalogue_version}" required><br>
                    <select id="is_cat_active">
                        <option value="1" ${cat.is_cat_active ? 'selected' : ''}>Active</option>
                        <option value="0" ${!cat.is_cat_active ? 'selected' : ''}>Inactive</option>
                    </select><br>
                    <input type="date" id="catalogue_start" value="${cat.catalogue_start}" required><br>
                    <input type="date" id="catalogue_end" value="${cat.catalogue_end}" required><br>
                    <button type="submit">Update</button>
                </form>
                <div id="msg" class="message-box"></div>
            `;
            document.getElementById('catalogueList').innerHTML = formHtml;

            const form = document.getElementById('catalogueForm');
            form.addEventListener('submit', async (e) => {
                e.preventDefault();

                const data = {
                    catalogue_name: document.getElementById('catalogue_name').value,
                    catalogue_version: document.getElementById('catalogue_version').value,
                    is_cat_active: document.getElementById('is_cat_active').value,
                    catalogue_start: document.getElementById('catalogue_start').value,
                    catalogue_end: document.getElementById('catalogue_end').value
                };

                const res = await fetch(`/api/catalogues/${id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const result = await res.json();
                const msgBox = document.getElementById('msg');
                msgBox.innerText = result.message || result.error;
                msgBox.style.color = result.success ? 'green' : 'red';
            });
        });
}

function deleteCatalogue(id) {
    document.getElementById('homeBtn').style.display = 'inline-block';

    if (!confirm(`Are you sure you want to delete catalogue ID ${id}?`)) return;

    fetch(`/api/catalogues/${id}`, {
        method: 'DELETE'
    })
        .then(res => res.json())
        .then(result => {
            alert(result.message || result.error);
            fetchAllCatalogues();
        });
}
