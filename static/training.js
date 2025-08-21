// Training Dashboard JavaScript
let currentStats = {};

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadStats();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // CSV Import Form
    document.getElementById('csvImportForm').addEventListener('submit', function(e) {
        e.preventDefault();
        importCSV();
    });

    // Text Import Form
    document.getElementById('textImportForm').addEventListener('submit', function(e) {
        e.preventDefault();
        importText();
    });

    // URL Import Form
    document.getElementById('urlImportForm').addEventListener('submit', function(e) {
        e.preventDefault();
        importURL();
    });
}

// Navigation functions
function showSection(sectionName) {
    // Hide all sections
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => section.classList.remove('active'));

    // Show selected section
    document.getElementById(sectionName).classList.add('active');

    // Update navigation
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => link.classList.remove('active'));
    
    // Find and activate the clicked nav link
    const activeLink = document.querySelector(`[onclick="showSection('${sectionName}')"]`);
    if (activeLink) {
        activeLink.classList.add('active');
    }

    // Load section-specific data
    switch(sectionName) {
        case 'examples':
            loadExamples();
            break;
        case 'documents':
            loadDocuments();
            break;
        case 'export':
            populateExportCategories();
            break;
    }
}

// Load dashboard statistics
async function loadStats() {
    try {
        const response = await fetch('/training/api/stats');
        const data = await response.json();
        
        if (data.error) {
            showAlert('Error loading stats: ' + data.error, 'error');
            return;
        }

        currentStats = data;

        // Update dashboard cards
        document.getElementById('totalExamples').textContent = data.total_examples;
        document.getElementById('totalDocuments').textContent = data.total_documents;
        
        const totalCategories = new Set([...Object.keys(data.example_categories), ...Object.keys(data.document_categories)]).size;
        document.getElementById('totalCategories').textContent = totalCategories;

        // Update category filters
        updateCategoryFilters(data);

    } catch (error) {
        showAlert('Error loading statistics: ' + error.message, 'error');
    }
}

// Update category filter dropdowns
function updateCategoryFilters(stats) {
    const categories = new Set([...Object.keys(stats.example_categories), ...Object.keys(stats.document_categories)]);
    
    // Update example category filter
    const exampleFilter = document.getElementById('exampleCategoryFilter');
    exampleFilter.innerHTML = '<option value="">All Categories</option>';
    categories.forEach(cat => {
        exampleFilter.innerHTML += `<option value="${cat}">${cat}</option>`;
    });

    // Update document category filter
    const documentFilter = document.getElementById('documentCategoryFilter');
    documentFilter.innerHTML = '<option value="">All Categories</option>';
    categories.forEach(cat => {
        documentFilter.innerHTML += `<option value="${cat}">${cat}</option>`;
    });

    // Update export category filter
    const exportFilter = document.getElementById('exportCategory');
    if (exportFilter) {
        exportFilter.innerHTML = '<option value="">All Categories</option>';
        categories.forEach(cat => {
            exportFilter.innerHTML += `<option value="${cat}">${cat}</option>`;
        });
    }
}

// Load training examples
async function loadExamples() {
    const category = document.getElementById('exampleCategoryFilter').value;
    const tbody = document.getElementById('examplesTableBody');
    
    try {
        tbody.innerHTML = '<tr><td colspan="4" class="text-center">Loading...</td></tr>';
        
        const response = await fetch(`/training/api/examples${category ? '?category=' + category : ''}`);
        const data = await response.json();
        
        if (data.error) {
            tbody.innerHTML = `<tr><td colspan="4" class="text-center text-danger">${data.error}</td></tr>`;
            return;
        }

        if (data.examples.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="text-center">No examples found</td></tr>';
        } else {
            tbody.innerHTML = data.examples.map(ex => `
                <tr>
                    <td style="max-width: 300px;">
                        <div class="text-truncate" title="${escapeHtml(ex.input)}">
                            ${escapeHtml(ex.input.substring(0, 100))}${ex.input.length > 100 ? '...' : ''}
                        </div>
                    </td>
                    <td style="max-width: 300px;">
                        <div class="text-truncate" title="${escapeHtml(ex.output)}">
                            ${escapeHtml(ex.output.substring(0, 100))}${ex.output.length > 100 ? '...' : ''}
                        </div>
                    </td>
                    <td><span class="badge bg-secondary">${ex.category}</span></td>
                    <td><span class="badge bg-info">${ex.source}</span></td>
                </tr>
            `).join('');
        }

        document.getElementById('exampleCount').textContent = `${data.examples.length} examples`;

    } catch (error) {
        tbody.innerHTML = `<tr><td colspan="4" class="text-center text-danger">Error: ${error.message}</td></tr>`;
    }
}

// Load documents
async function loadDocuments() {
    const category = document.getElementById('documentCategoryFilter').value;
    const tbody = document.getElementById('documentsTableBody');
    
    try {
        tbody.innerHTML = '<tr><td colspan="4" class="text-center">Loading...</td></tr>';
        
        const response = await fetch(`/training/api/documents${category ? '?category=' + category : ''}`);
        const data = await response.json();
        
        if (data.error) {
            tbody.innerHTML = `<tr><td colspan="4" class="text-center text-danger">${data.error}</td></tr>`;
            return;
        }

        if (data.documents.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="text-center">No documents found</td></tr>';
        } else {
            tbody.innerHTML = data.documents.map(doc => `
                <tr>
                    <td><strong>${escapeHtml(doc.title)}</strong></td>
                    <td style="max-width: 400px;">
                        <div class="text-truncate">${escapeHtml(doc.content)}</div>
                    </td>
                    <td><span class="badge bg-secondary">${doc.category}</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary" onclick="viewDocument('${escapeHtml(doc.title)}', \`${escapeHtml(doc.full_content)}\`)">
                            <i class="fas fa-eye"></i> View
                        </button>
                    </td>
                </tr>
            `).join('');
        }

        document.getElementById('documentCount').textContent = `${data.documents.length} documents`;

    } catch (error) {
        tbody.innerHTML = `<tr><td colspan="4" class="text-center text-danger">Error: ${error.message}</td></tr>`;
    }
}

// View document in modal
function viewDocument(title, content) {
    document.getElementById('viewDocTitle').textContent = title;
    document.getElementById('viewDocContent').textContent = content;
    new bootstrap.Modal(document.getElementById('viewDocumentModal')).show();
}

// Add training example
async function addExample() {
    const input = document.getElementById('exampleInput').value.trim();
    const output = document.getElementById('exampleOutput').value.trim();
    const category = document.getElementById('exampleCategory').value.trim() || 'general';

    if (!input || !output) {
        showAlert('Please fill in both input and output fields', 'warning');
        return;
    }

    try {
        const response = await fetch('/training/api/examples', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                input: input,
                output: output,
                category: category
            })
        });

        const data = await response.json();

        if (data.error) {
            showAlert('Error: ' + data.error, 'error');
            return;
        }

        showAlert('Training example added successfully!', 'success');
        
        // Clear form and close modal
        document.getElementById('addExampleForm').reset();
        bootstrap.Modal.getInstance(document.getElementById('addExampleModal')).hide();
        
        // Refresh data
        loadStats();
        if (document.getElementById('examples').classList.contains('active')) {
            loadExamples();
        }

    } catch (error) {
        showAlert('Error adding example: ' + error.message, 'error');
    }
}

// Add document
async function addDocument() {
    const title = document.getElementById('docTitle').value.trim();
    const content = document.getElementById('docContent').value.trim();
    const category = document.getElementById('docCategory').value.trim() || 'general';

    if (!title || !content) {
        showAlert('Please fill in both title and content fields', 'warning');
        return;
    }

    try {
        const response = await fetch('/training/api/documents', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: title,
                content: content,
                category: category
            })
        });

        const data = await response.json();

        if (data.error) {
            showAlert('Error: ' + data.error, 'error');
            return;
        }

        showAlert('Document added successfully!', 'success');
        
        // Clear form and close modal
        document.getElementById('addDocumentForm').reset();
        bootstrap.Modal.getInstance(document.getElementById('addDocumentModal')).hide();
        
        // Refresh data
        loadStats();
        if (document.getElementById('documents').classList.contains('active')) {
            loadDocuments();
        }

    } catch (error) {
        showAlert('Error adding document: ' + error.message, 'error');
    }
}

// Build RAG knowledge base
async function buildRAG() {
    try {
        showAlert('Building RAG knowledge base...', 'info');
        
        const response = await fetch('/training/api/rag/build');
        const data = await response.json();

        if (data.error) {
            showAlert('Error: ' + data.error, 'error');
            return;
        }

        showAlert(data.message, 'success');
        
        // Update RAG status
        document.getElementById('ragStatus').textContent = 'Built';
        document.getElementById('ragStatusText').textContent = 'Ready';
        document.getElementById('ragStatusIcon').className = 'fas fa-database fa-3x mb-3 text-success';

    } catch (error) {
        showAlert('Error building RAG: ' + error.message, 'error');
    }
}

// Test RAG system
async function testRAG() {
    const query = document.getElementById('ragQuery').value.trim();
    
    if (!query) {
        showAlert('Please enter a test query', 'warning');
        return;
    }

    try {
        const response = await fetch('/training/api/rag/test', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        });

        const data = await response.json();

        if (data.error) {
            showAlert('Error: ' + data.error, 'error');
            return;
        }

        // Show results
        document.getElementById('enhancedPrompt').textContent = data.enhanced_prompt;
        
        const docsContainer = document.getElementById('relevantDocs');
        if (data.relevant_documents.length === 0) {
            docsContainer.innerHTML = '<p class="text-muted">No relevant documents found</p>';
        } else {
            docsContainer.innerHTML = data.relevant_documents.map(doc => `
                <div class="card mb-2">
                    <div class="card-body p-3">
                        <h6 class="card-title">${escapeHtml(doc.title)}</h6>
                        <p class="card-text text-muted small">${escapeHtml(doc.content)}</p>
                        <span class="badge bg-secondary">${doc.category}</span>
                    </div>
                </div>
            `).join('');
        }

        document.getElementById('ragResults').style.display = 'block';

    } catch (error) {
        showAlert('Error testing RAG: ' + error.message, 'error');
    }
}

// Create sample data
async function createSampleData() {
    try {
        showAlert('Creating sample data...', 'info');
        
        const response = await fetch('/training/api/create-sample-data');
        const data = await response.json();

        if (data.error) {
            showAlert('Error: ' + data.error, 'error');
            return;
        }

        showAlert(data.message, 'success');
        loadStats();

    } catch (error) {
        showAlert('Error creating sample data: ' + error.message, 'error');
    }
}

// Import CSV
async function importCSV() {
    const fileInput = document.getElementById('csvFile');
    const file = fileInput.files[0];

    if (!file) {
        showAlert('Please select a CSV file', 'warning');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('input_column', document.getElementById('inputColumn').value);
    formData.append('output_column', document.getElementById('outputColumn').value);
    formData.append('category_column', document.getElementById('categoryColumn').value);
    formData.append('category_default', 'imported');

    try {
        showAlert('Importing CSV file...', 'info');
        
        const response = await fetch('/training/api/import/csv', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            showAlert('Error: ' + data.error, 'error');
            return;
        }

        showAlert(data.message, 'success');
        document.getElementById('csvImportForm').reset();
        loadStats();

    } catch (error) {
        showAlert('Error importing CSV: ' + error.message, 'error');
    }
}

// Import text file
async function importText() {
    const fileInput = document.getElementById('textFile');
    const file = fileInput.files[0];

    if (!file) {
        showAlert('Please select a text file', 'warning');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', document.getElementById('documentTitle').value || file.name);
    formData.append('category', document.getElementById('documentCategory').value);

    try {
        showAlert('Importing text file...', 'info');
        
        const response = await fetch('/training/api/import/text', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            showAlert('Error: ' + data.error, 'error');
            return;
        }

        showAlert(data.message, 'success');
        document.getElementById('textImportForm').reset();
        loadStats();

    } catch (error) {
        showAlert('Error importing text file: ' + error.message, 'error');
    }
}

// Import from URL
async function importURL() {
    const url = document.getElementById('webUrl').value.trim();
    const title = document.getElementById('urlTitle').value.trim();
    const category = document.getElementById('urlCategory').value.trim();

    if (!url) {
        showAlert('Please enter a URL', 'warning');
        return;
    }

    try {
        showAlert('Importing from URL...', 'info');
        
        const response = await fetch('/training/api/import/url', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: url,
                title: title || url,
                category: category || 'web'
            })
        });

        const data = await response.json();

        if (data.error) {
            showAlert('Error: ' + data.error, 'error');
            return;
        }

        showAlert(data.message, 'success');
        document.getElementById('urlImportForm').reset();
        loadStats();

    } catch (error) {
        showAlert('Error importing from URL: ' + error.message, 'error');
    }
}

// Export data
function exportData(format) {
    const category = document.getElementById('exportCategory').value;
    const url = `/training/api/export/${format}${category ? '?category=' + category : ''}`;
    
    // Create temporary link to download file
    const link = document.createElement('a');
    link.href = url;
    link.download = '';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showAlert(`Exporting data in ${format.toUpperCase()} format...`, 'info');
}

// Populate export categories
function populateExportCategories() {
    if (currentStats && Object.keys(currentStats).length > 0) {
        updateCategoryFilters(currentStats);
    }
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showAlert(message, type = 'info') {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert');
    existingAlerts.forEach(alert => alert.remove());

    // Create new alert
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    // Insert at the top of main content
    const mainContent = document.querySelector('.col-md-9 .p-4');
    mainContent.insertBefore(alertDiv, mainContent.firstChild);

    // Auto-hide after 5 seconds for non-error messages
    if (type !== 'error') {
        setTimeout(() => {
            if (alertDiv && alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}
