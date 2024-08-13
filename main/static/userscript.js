document.addEventListener('DOMContentLoaded', function() {
    // Fetch and display truck list
    fetchTruckList();

    // Fetch and display store details
    fetchStoreDetails();

    // Fetch and display SKU list
    fetchSKUList();

    // Setup dialog box functionality for SKU
    const assignSkuBtn = document.getElementById('assign-sku-btn');
    const assignSkuDialog = document.getElementById('assign-sku-dialog');
    const closeSkuBtn = assignSkuDialog.querySelector('.close-btn');
    const assignSkuForm = document.getElementById('assign-sku-form');

    assignSkuBtn.addEventListener('click', function() {
        assignSkuDialog.style.display = 'block';
    });

    closeSkuBtn.addEventListener('click', function() {
        assignSkuDialog.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target === assignSkuDialog) {
            assignSkuDialog.style.display = 'none';
        }
    });

    assignSkuForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const skuId = document.getElementById('sku-id').value;
        const truckId = document.getElementById('truck-id').value;
        const skuName = document.getElementById('sku-name').value;
        const warehouse = document.getElementById('warehouse').value;

        fetch('/api/assign-sku', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                sku_id: skuId,
                truck_id: truckId,
                sku_name: skuName,
                warehouse: warehouse
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('SKU assigned successfully!');
                assignSkuDialog.style.display = 'none';
                fetchSKUList(); // Refresh SKU list
            } else {
                alert('Failed to assign SKU.');
            }
        });
    });

    // Setup dialog box functionality for Store
    const assignStoreBtn = document.getElementById('assign-store-btn');
    const assignStoreDialog = document.getElementById('assign-store-dialog');
    const closeStoreBtn = assignStoreDialog.querySelector('.close-btn');
    const assignStoreForm = document.getElementById('assign-store-form');

    assignStoreBtn.addEventListener('click', function() {
        assignStoreDialog.style.display = 'block';
    });

    closeStoreBtn.addEventListener('click', function() {
        assignStoreDialog.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target === assignStoreDialog) {
            assignStoreDialog.style.display = 'none';
        }
    });

    assignStoreForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const storeId = document.getElementById('store-id').value;
        const truckId = document.getElementById('truck-id-store').value;
        const storeName = document.getElementById('store-name').value;
        const contact = document.getElementById('contact').value;
        const address = document.getElementById('address').value;

        fetch('/api/assign-store', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                store_id: storeId,
                truck_id: truckId,
                store_name: storeName,
                contact: contact,
                address: address
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Store assigned successfully!');
                assignStoreDialog.style.display = 'none';
                fetchStoreDetails(); // Refresh store details
            } else {
                alert('Failed to assign store.');
            }
        });
    });
});

function fetchTruckList() {
    fetch('/api/trucks')
        .then(response => response.json())
        .then(data => {
            const truckListTableBody = document.getElementById('truck-list-table').querySelector('tbody');
            data.trucks.forEach(truck => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${truck.id}</td>
                    <td>${truck.number_plate}</td>
                    <td>${truck.driver_info}</td>
                    <td>${truck.entry_time}</td>
                    <td>${truck.exit_time}</td>
                `;
                truckListTableBody.appendChild(row);
            });
        });
}

function fetchStoreDetails() {
    fetch('/api/stores')
        .then(response => response.json())
        .then(data => {
            const storeTableBody = document.getElementById('store-table').querySelector('tbody');
            storeTableBody.innerHTML = ''; // Clear previous rows
            data.stores.forEach(store => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${store.id}</td>
                    <td>${store.name}</td>
                    <td>${store.contact}</td> <!-- Separated Contact -->
                    <td>${store.address}</td> <!-- Separated Address -->
                    <td>${store.manager}</td>
                    <td><button class="assign-truck-btn" data-store-id="${store.id}">Assign Truck</button></td>
                `;
                storeTableBody.appendChild(row);
            });
        });
}

function fetchSKUList() {
    fetch('/api/skus')
        .then(response => response.json())
        .then(data => {
            const skuListTableBody = document.getElementById('sku-list-table').querySelector('tbody');
            skuListTableBody.innerHTML = ''; // Clear previous rows
            data.skus.forEach(sku => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${sku.id}</td>
                    <td>${sku.name}</td>
                    <td>${sku.warehouse}</td>
                    <td>${sku.truckid || 'Not Assigned'}</td>
                `;
                skuListTableBody.appendChild(row);
            });
        });
}
