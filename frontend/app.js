// Configuration
const API_URL = 'https://tasky-961y.onrender.com';
// const API_URL = 'http://localhost:8000'; // For local development

// Global State
let authToken = localStorage.getItem('authToken');
let apiKey = localStorage.getItem('apiKey');
let currentUser = localStorage.getItem('username');

// DOM Elements
const authSection = document.getElementById('authSection');
const tasksSection = document.getElementById('tasksSection');
const logoutBtn = document.getElementById('logoutBtn');
const alertContainer = document.getElementById('alertContainer');
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const taskForm = document.getElementById('taskForm');
const tasksList = document.getElementById('tasksList');
const refreshBtn = document.getElementById('refreshBtn');
const taskDetailModal = new bootstrap.Modal(document.getElementById('taskDetailModal'));
const taskDetailContent = document.getElementById('taskDetailContent');

// Utility Functions
function showAlert(message, type = 'danger') {
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            <i class="bi bi-${type === 'success' ? 'check-circle' : 'exclamation-triangle'}"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    alertContainer.innerHTML = alertHtml;
    
    setTimeout(() => {
        const alert = alertContainer.querySelector('.alert');
        if (alert) {
            alert.classList.remove('show');
            setTimeout(() => alert.remove(), 150);
        }
    }, 5000);
}

function showSection(section) {
    if (section === 'auth') {
        authSection.style.display = 'block';
        tasksSection.style.display = 'none';
        logoutBtn.style.display = 'none';
    } else {
        authSection.style.display = 'none';
        tasksSection.style.display = 'block';
        logoutBtn.style.display = 'block';
        loadTasks();
    }
}

function showSpinner(spinnerId, show = true) {
    const spinner = document.getElementById(spinnerId);
    if (spinner) {
        spinner.classList.toggle('hidden', !show);
    }
}

// API Functions
async function apiCall(endpoint, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    // Add API key if available and not auth endpoints
    if (apiKey && endpoint !== '/signup' && endpoint !== '/token') {
        headers['X-API-Key'] = apiKey;
    }

    if (authToken && endpoint !== '/signup' && endpoint !== '/token') {
        headers['Authorization'] = `Bearer ${authToken}`;
    }

    try {
        const response = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            headers
        });

        const text = await response.text();
        const data = text ? JSON.parse(text) : null;

        if (!response.ok) {
            throw new Error(data?.detail || `Request failed: ${response.status}`);
        }

        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Authentication Functions
async function handleLogin(e) {
    e.preventDefault();
    showSpinner('loginSpinner', true);

    const formData = new URLSearchParams();
    formData.append('username', document.getElementById('loginUsername').value);
    formData.append('password', document.getElementById('loginPassword').value);

    try {
        const data = await apiCall('/token', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        });

        authToken = data.access_token;
        currentUser = document.getElementById('loginUsername').value;
        localStorage.setItem('authToken', authToken);
        localStorage.setItem('username', currentUser);

        // Save the API key from login response
        if (data.api_key) {
            apiKey = data.api_key;
            localStorage.setItem('apiKey', data.api_key);
        }

        showAlert('Login successful! Welcome back!', 'success');
        showSection('tasks');
        loginForm.reset();
    } catch (error) {
        showAlert(error.message);
    } finally {
        showSpinner('loginSpinner', false);
    }
}

async function handleRegister(e) {
    e.preventDefault();
    showSpinner('regSpinner', true);

    const userData = {
        username: document.getElementById('regUsername').value,
        email: document.getElementById('regEmail').value,
        password: document.getElementById('regPassword').value
    };

    try {
        const response = await apiCall('/signup', {
            method: 'POST',
            body: JSON.stringify(userData)
        });

        // Save the API key
        localStorage.setItem('apiKey', response.api_key);
        
        showAlert('Registration successful!', 'success');
        
        // Switch to login tab
        const loginTab = document.querySelector('[href="#login"]');
        const loginTabContent = document.getElementById('login');
        const registerTabContent = document.getElementById('register');
        
        loginTab.classList.add('active');
        document.querySelector('[href="#register"]').classList.remove('active');
        loginTabContent.classList.add('show', 'active');
        registerTabContent.classList.remove('show', 'active');
        
        registerForm.reset();
    } catch (error) {
        showAlert(error.message);
    } finally {
        showSpinner('regSpinner', false);
    }
}

function handleLogout() {
    authToken = null;
    apiKey = null;
    currentUser = null;
    localStorage.removeItem('authToken');
    localStorage.removeItem('apiKey');
    localStorage.removeItem('username');
    showSection('auth');
    showAlert('Logged out successfully', 'info');
}

// Task Functions
async function handleCreateTask(e) {
    e.preventDefault();

    const taskData = {
        title: document.getElementById('taskTitle').value,
        description: document.getElementById('taskDescription').value,
        status: document.getElementById('taskStatus').value
    };

    try {
        await apiCall('/tasks', {
            method: 'POST',
            body: JSON.stringify(taskData)
        });

        showAlert('Task created successfully!', 'success');
        taskForm.reset();
        loadTasks();
    } catch (error) {
        showAlert(error.message);
    }
}

async function loadTasks() {
    try {
        tasksList.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"></div></div>';
        
        const tasks = await apiCall('/tasks');
        displayTasks(tasks);
    } catch (error) {
        tasksList.innerHTML = '<p class="text-danger text-center">Failed to load tasks</p>';
        showAlert('Failed to load tasks: ' + error.message);
    }
}

function displayTasks(tasks) {
    if (tasks.length === 0) {
        tasksList.innerHTML = `
            <div class="text-center text-muted p-5">
                <i class="bi bi-inbox" style="font-size: 3rem;"></i>
                <p class="mt-3">No tasks yet. Create your first task!</p>
            </div>
        `;
        return;
    }

    const tasksHtml = tasks.map(task => `
        <div class="card task-card ${task.status === 'completed' ? 'border-success' : ''}" 
             data-task-id="${task.id}" 
             onclick="showTaskDetails(${task.id})">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <h6 class="card-title ${task.status === 'completed' ? 'completed' : ''}">
                            ${escapeHtml(task.title)}
                        </h6>
                        <p class="card-text small ${task.status === 'completed' ? 'completed' : ''}">
                            ${escapeHtml(task.description)}
                        </p>
                        <small class="text-muted">
                            <i class="bi bi-clock"></i> ${formatDate(task.created_at)}
                        </small>
                    </div>
                    <div class="d-flex gap-2">
                        <button class="btn btn-sm ${task.status === 'completed' ? 'btn-warning' : 'btn-success'}" 
                                onclick="event.stopPropagation(); toggleTask(${task.id}, '${task.status}')"
                                title="${task.status === 'completed' ? 'Mark as pending' : 'Mark as completed'}">
                            <i class="bi ${task.status === 'completed' ? 'bi-arrow-counterclockwise' : 'bi-check-lg'}"></i>
                        </button>
                        <button class="btn btn-sm btn-danger" 
                                onclick="event.stopPropagation(); deleteTask(${task.id})"
                                title="Delete task">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `).join('');

    tasksList.innerHTML = tasksHtml;
}

async function showTaskDetails(taskId) {
    try {
        taskDetailContent.innerHTML = `
            <div class="text-center">
                <div class="spinner-border" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2">Loading task details...</p>
            </div>
        `;
        
        taskDetailModal.show();
        
        const task = await apiCall(`/tasks/${taskId}`);
        
        const statusBadge = task.status === 'completed' 
            ? '<span class="badge bg-success"><i class="bi bi-check-circle"></i> Completed</span>'
            : '<span class="badge bg-warning"><i class="bi bi-clock"></i> Pending</span>';
        
        taskDetailContent.innerHTML = `
            <div class="task-detail">
                <div class="d-flex justify-content-between align-items-start mb-3">
                    <h6 class="mb-0">Task Information</h6>
                    ${statusBadge}
                </div>
                
                <h4 class="mb-3">${escapeHtml(task.title)}</h4>
                
                <div class="mb-3">
                    <strong>Description:</strong>
                    <p class="mt-2">${escapeHtml(task.description)}</p>
                </div>
                
                <div class="task-meta">
                    <div class="row">
                        <div class="col-sm-6">
                            <strong>ID:</strong> ${task.id}
                        </div>
                        <div class="col-sm-6">
                            <strong>Status:</strong> ${task.status}
                        </div>
                        <div class="col-sm-6">
                            <strong>Created:</strong> ${formatDate(task.created_at)}
                        </div>
                        <div class="col-sm-6">
                            <strong>Updated:</strong> ${formatDate(task.updated_at)}
                        </div>
                    </div>
                </div>
                
                <div class="d-flex gap-2 mt-3">
                    <button class="btn ${task.status === 'completed' ? 'btn-warning' : 'btn-success'}" 
                            onclick="toggleTask(${task.id}, '${task.status}'); taskDetailModal.hide()">
                        <i class="bi ${task.status === 'completed' ? 'bi-arrow-counterclockwise' : 'bi-check-lg'}"></i>
                        ${task.status === 'completed' ? 'Mark as Pending' : 'Mark as Completed'}
                    </button>
                    <button class="btn btn-danger" 
                            onclick="deleteTask(${task.id}); taskDetailModal.hide()">
                        <i class="bi bi-trash"></i> Delete Task
                    </button>
                </div>
            </div>
        `;
    } catch (error) {
        taskDetailContent.innerHTML = `
            <div class="alert alert-danger">
                <i class="bi bi-exclamation-triangle"></i>
                Failed to load task details: ${error.message}
            </div>
        `;
    }
}

async function toggleTask(taskId, currentStatus) {
    const newStatus = currentStatus === 'completed' ? 'pending' : 'completed';
    
    try {
        await apiCall(`/tasks/${taskId}`, {
            method: 'PUT',
            body: JSON.stringify({ status: newStatus })
        });
        
        showAlert(`Task marked as ${newStatus}!`, 'success');
        loadTasks();
    } catch (error) {
        showAlert('Failed to update task: ' + error.message);
    }
}

async function deleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this task?')) return;

    try {
        await apiCall(`/tasks/${taskId}`, {
            method: 'DELETE'
        });
        
        showAlert('Task deleted successfully!', 'success');
        loadTasks();
    } catch (error) {
        showAlert('Failed to delete task: ' + error.message);
    }
}

// Helper Functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    // Handle null/undefined dates
    if (!dateString) return 'No date';
    
    // Parse as UTC to avoid timezone issues
    const date = new Date(dateString + (dateString.includes('Z') ? '' : 'Z'));
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
    if (diffMins < 1440) return `${Math.floor(diffMins / 60)} hour${Math.floor(diffMins / 60) > 1 ? 's' : ''} ago`;
    
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// Event Listeners
loginForm.addEventListener('submit', handleLogin);
registerForm.addEventListener('submit', handleRegister);
taskForm.addEventListener('submit', handleCreateTask);
logoutBtn.addEventListener('click', handleLogout);
refreshBtn.addEventListener('click', loadTasks);

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    if (authToken) {
        showSection('tasks');
    } else {
        showSection('auth');
    }
});