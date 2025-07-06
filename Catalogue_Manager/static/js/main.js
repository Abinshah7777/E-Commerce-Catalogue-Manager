document.addEventListener('DOMContentLoaded', () => {
    fetchAllCatalogues(); // Load all catalogues when the page loads
});

function showCreateForm() {
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

        const msgBox = document.getElementById('msg');

        try {
            const res = await fetch('/api/catalogues', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            let result;
            try {
                result = await res.json();
            } catch {
                msgBox.innerText = 'Invalid response from server.';
                msgBox.style.color = 'red';
                return;
            }

            if (res.status === 201 || result.success) {
                msgBox.innerText = result.message || 'Catalogue created successfully.';
                msgBox.style.color = 'green';
                form.reset();
                fetchAllCatalogues();
            } else {
                msgBox.innerText = result.error || 'Something went wrong.';
                msgBox.style.color = 'red';
            }

        } catch (err) {
            msgBox.innerText = 'Something went wrong while connecting to the server.';
            msgBox.style.color = 'red';
            console.error(err);
        }

        setTimeout(() => {
            msgBox.innerText = '';
        }, 4000);
    });
}


let allCataloguesData = [];
let currentPage = 1;
const itemsPerPage = 5;

function fetchAllCatalogues() {
    fetch('/api/catalogues')
        .then(res => res.json())
        .then(response => {
            const container = document.getElementById('catalogueList');
            container.innerHTML = '';

            if (!response.success || response.data.length === 0) {
                container.innerHTML = '<p>No catalogues found.</p>';
                return;
            }

            allCataloguesData = response.data;

            const resultWrapper = document.createElement('div');
            resultWrapper.id = 'resultWrapper';
            container.appendChild(resultWrapper);

            const paginationWrapper = document.createElement('div');
            paginationWrapper.id = 'paginationWrapper';
            paginationWrapper.className = 'pagination-controls';
            container.appendChild(paginationWrapper);

            function getFilteredData() {
                const query = document.getElementById('searchInput').value.toLowerCase();
                const filter = document.getElementById('statusFilter').value;

                let filtered = allCataloguesData;

                if (filter === 'active') {
                    filtered = filtered.filter(c => c.is_cat_active);
                } else if (filter === 'inactive') {
                    filtered = filtered.filter(c => !c.is_cat_active);
                }

                if (query) {
                    filtered = filtered.filter(cat =>
                        cat.catalogue_name.toLowerCase().includes(query) ||
                        cat.catalogue_id.toString().includes(query)
                    );
                }

                // Sort by ID ascending or descending
                const sortOrder = document.getElementById('sortOrder').value;
                if (sortOrder === 'asc') {
                    filtered.sort((a, b) => a.catalogue_id - b.catalogue_id);
                } else {
                    filtered.sort((a, b) => b.catalogue_id - a.catalogue_id);
                }

                return filtered;
            }

            function renderPagination(filtered) {
                const totalPages = Math.ceil(filtered.length / itemsPerPage);
                const pagination = document.getElementById('paginationWrapper');
                pagination.innerHTML = '';

                const prevBtn = document.createElement('button');
                prevBtn.textContent = '⏮ Prev';
                prevBtn.disabled = currentPage === 1;
                prevBtn.onclick = () => {
                    currentPage--;
                    renderCatalogues(getFilteredData());
                };

                const nextBtn = document.createElement('button');
                nextBtn.textContent = 'Next ⏭';
                nextBtn.disabled = currentPage === totalPages;
                nextBtn.onclick = () => {
                    currentPage++;
                    renderCatalogues(getFilteredData());
                };

                pagination.appendChild(prevBtn);
                pagination.appendChild(document.createTextNode(` Page ${currentPage} of ${totalPages} `));
                pagination.appendChild(nextBtn);
            }

            function renderCatalogues(data) {
                const wrapper = document.getElementById('resultWrapper');
                wrapper.innerHTML = '';

                const start = (currentPage - 1) * itemsPerPage;
                const paginatedData = data.slice(start, start + itemsPerPage);

                paginatedData.forEach(cat => {
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
                    wrapper.appendChild(div);
                });

                renderPagination(data);
            }

            document.getElementById('searchInput').addEventListener('input', () => {
                currentPage = 1;
                renderCatalogues(getFilteredData());
            });

            document.getElementById('statusFilter').addEventListener('change', () => {
                currentPage = 1;
                renderCatalogues(getFilteredData());
            });

            document.getElementById('sortOrder').addEventListener('change', () => {
                currentPage = 1;
                renderCatalogues(getFilteredData());
            });

            renderCatalogues(getFilteredData());
        })
        .catch(err => {
            document.getElementById('catalogueList').innerHTML = '<p>Error loading catalogues.</p>';
        });
}

function promptViewById() {
    const id = prompt("Enter Catalogue ID to view:");
    if (!id) return;

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
                msgBox.innerText = result.message || result.error || "Unknown response.";
                msgBox.style.color = result.success ? 'green' : 'red';

                setTimeout(() => {
                    msgBox.innerText = '';
                }, 4000);
            });

        });
}

function deleteCatalogue(id) {
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