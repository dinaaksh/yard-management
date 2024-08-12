document.addEventListener('DOMContentLoaded', function() {
    // Fetch and display analytics data
    fetchAnalyticsData();

    // Fetch and display truck list
    fetchTruckList();

    // Fetch and display store details
    fetchStoreDetails();

    // Fetch and display SKU list
    fetchSKUList();
});

function fetchAnalyticsData() {
    // Example of an API call
    fetch('/api/analytics')
        .then(response => response.json())
        .then(data => {
            document.getElementById('avg-waiting-time-value').textContent = data.avg_waiting_time;
            document.getElementById('turnaround-time-value').textContent = data.turnaround_time;
            document.getElementById('loading-time-value').textContent = data.loading_time;
            document.getElementById('trucks-count-value').textContent = data.trucks_in_warehouse;
        });
}

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
            data.stores.forEach(store => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${store.id}</td>
                    <td>${store.name}</td>
                    <td>${store.contact_address}</td>
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
            data.skus.forEach(sku => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${sku.id}</td>
                    <td>${sku.name}</td>
                    <td>${sku.warehouse}</td>
                    <td><button class="manage-sku-btn" data-sku-id="${sku.id}">Manage</button></td>
                `;
                skuListTableBody.appendChild(row);
            });
        });
}
