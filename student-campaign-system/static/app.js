// Real Application - Connected to Backend API
const API_BASE_URL = 'http://localhost:5000/api';

// Application State
const appState = {
    currentRole: 'student',
    currentStudentTab: 'application-form',
    currentAdminTab: 'overview',
    scoreChart: null,
    currentUser: null,
    currentApplication: null,
    currentLicense: null
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
});

async function initializeApp() {
    console.log('🚀 Initializing Real Application...');
    
    // Check if user is logged in
    const token = localStorage.getItem('authToken');
    if (!token) {
        showLoginModal();
        return;
    }
    
    // Load user data
    await loadUserData();
    
    // Update character counters
    const objectiveField = document.getElementById('objective');
    if (objectiveField) {
        objectiveField.addEventListener('input', updateCharCounter);
    }

    const projectDescField = document.getElementById('projectDesc');
    if (projectDescField) {
        projectDescField.addEventListener('input', updateProgressCharCounter);
    }
    
    // Initialize chart if on admin dashboard
    if (appState.currentRole === 'admin') {
        await loadAdminData();
        initializeChart();
    }
}

function setupEventListeners() {
    // Form submissions
    const applicationForm = document.getElementById('applicationForm');
    if (applicationForm) {
        applicationForm.addEventListener('submit', (e) => {
            e.preventDefault();
            submitApplication();
        });
    }

    const progressForm = document.getElementById('progressForm');
    if (progressForm) {
        progressForm.addEventListener('submit', (e) => {
            e.preventDefault();
            submitProgressReport();
        });
    }
}

// Authentication
function showLoginModal() {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.innerHTML = `
        <div class="modal">
            <h2>Login</h2>
            <form id="loginForm">
                <div class="form-group">
                    <label for="loginEmail">Email:</label>
                    <input type="email" id="loginEmail" placeholder="jane.doe@mit.edu" required>
                </div>
                <div class="form-group">
                    <label for="loginPassword">Password:</label>
                    <input type="password" id="loginPassword" placeholder="password" required>
                </div>
                <button type="submit" class="btn btn-primary">Login</button>
            </form>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        
        // Mock authentication - in real app, call backend
        localStorage.setItem('authToken', 'mock-token-' + Date.now());
        localStorage.setItem('userEmail', email);
        
        modal.remove();
        location.reload();
    });
}

async function loadUserData() {
    try {
        const email = localStorage.getItem('userEmail');
        appState.currentUser = { email };
        
        // In real app, fetch from backend
        console.log('✅ User loaded:', email);
    } catch (error) {
        console.error('Error loading user data:', error);
        showNotification('Error loading user data', 'error');
    }
}

async function loadAdminData() {
    try {
        const response = await fetch(`${API_BASE_URL}/admin/statistics`);
        if (!response.ok) throw new Error('Failed to load statistics');
        
        const data = await response.json();
        console.log('📊 Admin data loaded:', data);
        
        // Update UI with real data
        updateAdminUI(data);
    } catch (error) {
        console.error('Error loading admin data:', error);
        showNotification('Error loading admin data', 'error');
    }
}

function updateAdminUI(data) {
    // Update statistics cards
    const statCards = document.querySelectorAll('.stat-card');
    if (statCards.length >= 4) {
        statCards[0].querySelector('.stat-number').textContent = data.applications.total;
        statCards[1].querySelector('.stat-number').textContent = data.applications.approved;
        statCards[2].querySelector('.stat-number').textContent = data.applications.rejected;
        statCards[3].querySelector('.stat-number').textContent = data.applications.waitlisted;
    }
    
    // Update license inventory
    const inventoryRows = document.querySelectorAll('.inventory-row');
    if (inventoryRows.length >= 5) {
        inventoryRows[0].querySelector('strong').textContent = data.licenses.total_allocated;
        inventoryRows[1].querySelector('strong').textContent = data.licenses.active;
        inventoryRows[2].querySelector('strong').textContent = data.licenses.expired;
        inventoryRows[3].querySelector('strong').textContent = data.licenses.available;
    }
}

// Role Switching
function switchRole(role) {
    appState.currentRole = role;
    
    const studentPortal = document.getElementById('student-portal');
    const adminDashboard = document.getElementById('admin-dashboard');
    
    if (role === 'student') {
        studentPortal.style.display = 'block';
        adminDashboard.style.display = 'none';
        switchStudentTab('application-form');
    } else {
        studentPortal.style.display = 'none';
        adminDashboard.style.display = 'block';
        switchAdminTab('overview');
        loadAdminData();
    }
}

// Student Tab Switching
function switchStudentTab(tabName) {
    appState.currentStudentTab = tabName;
    
    // Hide all tabs
    document.querySelectorAll('#student-portal .tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('#student-portal .tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    const selectedTab = document.getElementById(tabName);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
    
    // Add active class to clicked button
    if (event && event.target) {
        event.target.classList.add('active');
    }
    
    // Load data if needed
    if (tabName === 'application-status') {
        loadApplicationStatus();
    }
}

// Admin Tab Switching
function switchAdminTab(tabName) {
    appState.currentAdminTab = tabName;
    
    // Hide all tabs
    document.querySelectorAll('#admin-dashboard .tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('#admin-dashboard .tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    const selectedTab = document.getElementById(tabName);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
    
    // Add active class to clicked button
    if (event && event.target) {
        event.target.classList.add('active');
    }
    
    // Load data if needed
    if (tabName === 'overview') {
        loadAdminData();
    }
}

// Character Counter
function updateCharCounter() {
    const objective = document.getElementById('objective');
    const charCount = document.getElementById('charCount');
    charCount.textContent = objective.value.length;
}

function updateProgressCharCounter() {
    const projectDesc = document.getElementById('projectDesc');
    const descCharCount = document.getElementById('descCharCount');
    descCharCount.textContent = projectDesc.value.length;
}

// Form Submissions
async function submitApplication() {
    const formData = {
        email: document.getElementById('email').value,
        name: document.getElementById('fullName').value,
        institution: document.getElementById('institution').value,
        degree_program: document.getElementById('degreeProgram').value,
        degree_level: document.querySelector('input[name="degreeLevel"]:checked').value,
        year: parseInt(document.querySelector('input[name="year"]:checked').value),
        objective: document.getElementById('objective').value,
        prior_claude_usage: document.querySelector('input[name="claudeExp"]:checked').value,
        financial_aid: document.getElementById('financialAid').checked,
        first_generation: document.getElementById('firstGen').checked
    };

    // Validation
    if (!formData.objective || formData.objective.length < 50) {
        showNotification('Objective must be at least 50 characters', 'error');
        return;
    }

    try {
        showNotification('Submitting application...', 'info');
        
        const response = await fetch(`${API_BASE_URL}/applications`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('authToken')}`
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to submit application');
        }

        const result = await response.json();
        appState.currentApplication = result;
        
        showNotification(
            `Application submitted successfully! Score: ${result.score}/100 - Status: ${result.status.toUpperCase()}`,
            'success'
        );
        
        // Switch to status tab
        setTimeout(() => {
            switchStudentTab('application-status');
            loadApplicationStatus();
        }, 1500);
    } catch (error) {
        console.error('Error submitting application:', error);
        showNotification(error.message, 'error');
    }
}

async function loadApplicationStatus() {
    try {
        if (!appState.currentApplication) {
            showNotification('No application found', 'error');
            return;
        }

        const appId = appState.currentApplication.application_id;
        const response = await fetch(`${API_BASE_URL}/applications/${appId}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('authToken')}`
            }
        });

        if (!response.ok) throw new Error('Failed to load application');

        const data = await response.json();
        updateApplicationStatusUI(data);
    } catch (error) {
        console.error('Error loading application status:', error);
        showNotification('Error loading application status', 'error');
    }
}

function updateApplicationStatusUI(data) {
    // Update status badge
    const statusBadge = document.querySelector('.status-badge');
    if (statusBadge) {
        statusBadge.textContent = `✅ ${data.status.toUpperCase()}`;
        statusBadge.className = `status-badge ${data.status}`;
    }

    // Update score breakdown
    const breakdown = data.score_breakdown;
    const scoreItems = document.querySelectorAll('.score-item');
    
    const items = [
        { label: 'Degree Relevance', key: 'degree_relevance', max: 30 },
        { label: 'Objective Quality', key: 'objective_quality', max: 25 },
        { label: 'Academic Standing', key: 'academic_standing', max: 20 },
        { label: 'Demonstrated Need', key: 'demonstrated_need', max: 15 },
        { label: 'Claude Familiarity', key: 'claude_familiarity', max: 10 }
    ];

    scoreItems.forEach((item, index) => {
        if (index < items.length) {
            const key = items[index].key;
            const points = breakdown[key];
            const max = items[index].max;
            const percentage = (points / max) * 100;
            
            item.querySelector('.progress-fill').style.width = percentage + '%';
            item.querySelector('.score-points').textContent = `${points}/${max} points`;
        }
    });

    // Update total score
    document.querySelector('.score-value').textContent = data.score;
}

async function submitProgressReport() {
    const formData = {
        description: document.getElementById('projectDesc').value,
        claude_usage_examples: document.getElementById('claudeUsage').value,
        outcomes: document.getElementById('outcomes').value
    };

    // Validation
    if (!formData.description || formData.description.length < 100) {
        showNotification('Project description must be at least 100 characters', 'error');
        return;
    }

    if (!formData.claude_usage_examples.trim()) {
        showNotification('Please provide Claude usage examples', 'error');
        return;
    }

    if (!formData.outcomes.trim()) {
        showNotification('Please describe outcomes achieved', 'error');
        return;
    }

    try {
        showNotification('Submitting progress report...', 'info');
        
        if (!appState.currentLicense) {
            showNotification('No active license found', 'error');
            return;
        }

        const response = await fetch(
            `${API_BASE_URL}/licenses/${appState.currentLicense.id}/progress-reports`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('authToken')}`
                },
                body: JSON.stringify(formData)
            }
        );

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to submit progress report');
        }

        const result = await response.json();
        
        showNotification(
            `Progress report submitted! Extension: ${result.extension_days} days approved.`,
            'success'
        );
        
        // Reset form
        document.getElementById('progressForm').reset();
        updateProgressCharCounter();
    } catch (error) {
        console.error('Error submitting progress report:', error);
        showNotification(error.message, 'error');
    }
}

// Notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        font-weight: 500;
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        animation: slideInRight 0.3s ease-out;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Filtering
function filterApplications() {
    const statusFilter = document.getElementById('statusFilter').value;
    const degreeFilter = document.getElementById('degreeFilter').value;
    const searchInput = document.getElementById('searchInput').value.toLowerCase();

    const rows = document.querySelectorAll('.applications-table tbody tr');
    
    rows.forEach(row => {
        let show = true;

        if (statusFilter) {
            const status = row.querySelector('td:nth-child(6)').textContent.toLowerCase();
            if (!status.includes(statusFilter.toLowerCase())) {
                show = false;
            }
        }

        if (degreeFilter && show) {
            const degree = row.querySelector('td:nth-child(4)').textContent.toLowerCase();
            if (!degree.includes(degreeFilter.toLowerCase())) {
                show = false;
            }
        }

        if (searchInput && show) {
            const student = row.querySelector('td:nth-child(2)').textContent.toLowerCase();
            if (!student.includes(searchInput)) {
                show = false;
            }
        }

        row.style.display = show ? '' : 'none';
    });
}

// Chart Initialization
function initializeChart() {
    const ctx = document.getElementById('scoreChart');
    if (!ctx) return;

    const data = {
        labels: ['10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100'],
        datasets: [{
            label: 'Number of Applications',
            data: [5, 15, 35, 65, 120, 180, 250, 180, 80],
            backgroundColor: 'rgba(99, 102, 241, 0.5)',
            borderColor: 'rgba(99, 102, 241, 1)',
            borderWidth: 2,
            borderRadius: 4
        }]
    };

    appState.scoreChart = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 50
                    }
                }
            }
        }
    });
}

// Logout
function logout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userEmail');
    location.reload();
}

// Animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }

    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 2000;
    }

    .modal {
        background: white;
        padding: 2rem;
        border-radius: 0.5rem;
        box-shadow: 0 20px 25px rgba(0, 0, 0, 0.15);
        max-width: 400px;
        width: 90%;
    }

    .modal h2 {
        margin-bottom: 1.5rem;
    }

    .modal .form-group {
        margin-bottom: 1rem;
    }

    .modal .btn {
        width: 100%;
    }
`;
document.head.appendChild(style);
