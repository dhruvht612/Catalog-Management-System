let catalogData = [];

// DOM Elements
const itemsList = document.getElementById('items-list');
const itemForm = document.getElementById('item-form');
const formTitle = document.getElementById('form-title');
const submitBtn = document.getElementById('submit-btn');
const cancelBtn = document.getElementById('cancel-btn');
const itemIdInput = document.getElementById('item-id');
const itemNameInput = document.getElementById('item-name');
const itemDescriptionInput = document.getElementById('item-description');
const detailsSection = document.getElementById('details-section');
const itemDetails = document.getElementById('item-details');
const closeDetailsBtn = document.getElementById('close-details');

let editingItemId = null;

async function loadData() {
    try {
        const response = await fetch('data.json');
        
        if (!response.ok) {
            throw new Error('Failed to load data.json');
        }
        
        const data = await response.json();
        
        
        catalogData = data.items || [];
        
        renderList();
        
        console.log('Data loaded successfully:', catalogData.length, 'items');
    } catch (error) {
        console.error('Error loading data:', error);
        itemsList.innerHTML = '<p style="color: red;">Error loading catalog data. Please ensure data.json exists.</p>';
    }
}

/**
 * Save data to JSON (simulated - in real app would POST to backend API)
 * Backend: Would execute INSERT/UPDATE SQL queries
 * Database: Would persist changes to database tables
 */
function saveData() {
    // In a real application:
    // 1. Frontend would send POST/PUT request to backend API
    // 2. Backend would validate and process the request
    // 3. Backend would execute SQL: INSERT INTO items ... or UPDATE items SET ...
    // 4. Database would persist the changes
    
    // For this prototype, we only update in-memory data
    // To actually save to JSON file, you would need a backend server
    console.log('Data saved (in-memory):', catalogData);
    
    // Update UI to reflect changes
    renderList();
}

// ============================================================================
// FRONTEND: UI RENDERING FUNCTIONS
// ============================================================================

/**
 * Render the list of catalog items
 * Frontend: Updates DOM to display all items
 */
function renderList() {
    if (catalogData.length === 0) {
        itemsList.innerHTML = '<p style="color: #666;">No items in catalog. Add your first item above!</p>';
        return;
    }
    
    itemsList.innerHTML = catalogData.map(item => `
        <div class="item-card" onclick="viewItemDetails(${item.id})">
            <h3>${escapeHtml(item.name)}</h3>
            <p>${escapeHtml(item.description)}</p>
            <div class="item-actions">
                <button class="btn-edit" onclick="event.stopPropagation(); editItem(${item.id})">Edit</button>
                <button class="btn-delete" onclick="event.stopPropagation(); deleteItem(${item.id})">Delete</button>
            </div>
        </div>
    `).join('');
}

/**
 * Display item details in details section
 * Frontend: Shows selected item information
 */
function viewItemDetails(id) {
    const item = catalogData.find(item => item.id === id);
    
    if (!item) {
        alert('Item not found');
        return;
    }
    
    itemDetails.innerHTML = `
        <div class="item-id">ID: ${item.id}</div>
        <h3>${escapeHtml(item.name)}</h3>
        <p><strong>Description:</strong></p>
        <p>${escapeHtml(item.description)}</p>
    `;
    
    detailsSection.style.display = 'block';
}

/**
 * Close the details section
 * Frontend: Hides details view
 */
function closeDetails() {
    detailsSection.style.display = 'none';
}

// ============================================================================
// BACKEND: BUSINESS LOGIC & VALIDATION
// ============================================================================

/**
 * Validate input fields
 * Backend: Input validation (would also happen on server-side in real app)
 * @param {string} name - Item name
 * @param {string} description - Item description
 * @returns {boolean} - True if valid, false otherwise
 */
function validateInput(name, description) {
    // Backend validation: Check for empty fields
    if (!name || name.trim() === '') {
        alert('Name field cannot be empty');
        return false;
    }
    
    if (!description || description.trim() === '') {
        alert('Description field cannot be empty');
        return false;
    }
    
    return true;
}

/**
 * Add a new item to the catalog
 * Frontend: Handles form submission
 * Backend: Validates data and processes addition
 * Database: Would execute INSERT query
 */
function addItem(name, description) {
    // Backend: Validate input
    if (!validateInput(name, description)) {
        return;
    }
    
    // Database: Generate new ID (simulates AUTO_INCREMENT in database)
    const newId = catalogData.length > 0 
        ? Math.max(...catalogData.map(item => item.id)) + 1 
        : 1;
    
    // Database: Create new record (simulates INSERT INTO items VALUES ...)
    const newItem = {
        id: newId,
        name: name.trim(),
        description: description.trim()
    };
    
    // Database: Add to in-memory storage (simulates database insert)
    catalogData.push(newItem);
    
    // Backend: Save changes (in real app, would call API endpoint)
    saveData();
    
    // Frontend: Reset form
    resetForm();
    
    console.log('Item added:', newItem);
}

/**
 * Edit an existing item
 * Frontend: Populates form with item data
 * Backend: Validates and processes update
 * Database: Would execute UPDATE query
 */
function editItem(id) {
    const item = catalogData.find(item => item.id === id);
    
    if (!item) {
        alert('Item not found');
        return;
    }
    
    // Frontend: Populate form with item data
    editingItemId = id;
    itemIdInput.value = id;
    itemNameInput.value = item.name;
    itemDescriptionInput.value = item.description;
    
    // Frontend: Update form UI
    formTitle.textContent = 'Edit Item';
    submitBtn.textContent = 'Update Item';
    cancelBtn.style.display = 'inline-block';
    
    // Scroll to form
    document.querySelector('.form-section').scrollIntoView({ behavior: 'smooth' });
}

/**
 * Update an existing item
 * Frontend: Handles form submission for edits
 * Backend: Validates and processes update
 * Database: Would execute UPDATE query
 */
function updateItem(id, name, description) {
    // Backend: Validate input
    if (!validateInput(name, description)) {
        return;
    }
    
    // Database: Find item (simulates SELECT * FROM items WHERE id = ?)
    const itemIndex = catalogData.findIndex(item => item.id === id);
    
    if (itemIndex === -1) {
        alert('Item not found');
        return;
    }
    
    // Database: Update record (simulates UPDATE items SET name=?, description=? WHERE id=?)
    catalogData[itemIndex] = {
        id: id,
        name: name.trim(),
        description: description.trim()
    };
    
    // Backend: Save changes (in real app, would call API endpoint)
    saveData();
    
    // Frontend: Reset form
    resetForm();
    
    console.log('Item updated:', catalogData[itemIndex]);
}

/**
 * Delete an item from the catalog
 * Frontend: Confirms deletion
 * Backend: Processes deletion
 * Database: Would execute DELETE query
 */
function deleteItem(id) {
    // Frontend: Confirm deletion
    if (!confirm('Are you sure you want to delete this item?')) {
        return;
    }
    
    // Database: Find item index
    const itemIndex = catalogData.findIndex(item => item.id === id);
    
    if (itemIndex === -1) {
        alert('Item not found');
        return;
    }
    
    // Database: Remove from array (simulates DELETE FROM items WHERE id = ?)
    catalogData.splice(itemIndex, 1);
    
    // Backend: Save changes (in real app, would call API endpoint)
    saveData();
    
    // Frontend: Close details if viewing deleted item
    if (detailsSection.style.display !== 'none') {
        closeDetails();
    }
    
    console.log('Item deleted:', id);
}

/**
 * Reset the form to initial state
 * Frontend: Clears form fields and resets UI
 */
function resetForm() {
    editingItemId = null;
    itemIdInput.value = '';
    itemNameInput.value = '';
    itemDescriptionInput.value = '';
    formTitle.textContent = 'Add New Item';
    submitBtn.textContent = 'Add Item';
    cancelBtn.style.display = 'none';
}

/**
 * Utility function to escape HTML (prevent XSS attacks)
 * Backend: Security measure for user input
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ============================================================================
// EVENT LISTENERS (Frontend: User Interaction Handling)
// ============================================================================

// Form submission handler
itemForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const name = itemNameInput.value;
    const description = itemDescriptionInput.value;
    
    // Backend: Route to add or update based on editing state
    if (editingItemId) {
        updateItem(editingItemId, name, description);
    } else {
        addItem(name, description);
    }
});

// Cancel button handler
cancelBtn.addEventListener('click', () => {
    resetForm();
});

// Close details button handler
closeDetailsBtn.addEventListener('click', closeDetails);

// ============================================================================
// INITIALIZATION (Frontend: Page Load)
// ============================================================================

// Load data when page loads (simulates database connection on app startup)
document.addEventListener('DOMContentLoaded', () => {
    console.log('Catalog Management System initialized');
    loadData();
});
