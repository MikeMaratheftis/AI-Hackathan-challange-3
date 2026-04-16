// Application State
const appState = {
    currentRole: 'student',
    currentStudentTab: 'application-form',
    currentAdminTab: 'overview',
    scoreChart: null
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
    initializeChart();
});

function initializeApp() {
    // Update character counters
    const objectiveField = document.getElementById('objective');
    if (objectiveField) {
        objectiveField.addEventListener('input', updateCharCounter);
    }

    const projectDescField = document.getElementById('projectDesc');
    if (projectDescField) {
        projectDescField.addEventListener('input', updateProgressCharCounter);
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
    event.target.classList.add('active');
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
    event.target.classList.add('active');
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
function submitApplication() {
    const formData = {
        fullName: document.getElementById('fullName').value,
        email: document.getElementById('email').value,
        institution: document.getElementById('institution').value,
        degreeProgram: document.getElementById('degreeProgram').value,
        degreeLevel: document.querySelector('input[name="degreeLevel"]:checked').value,
        year: document.querySelector('input[name="year"]:checked').value,
        objective: document.getElementById('objective').value,
        useCase: document.getElementById('useCase').value,
        claudeExp: document.querySelector('input[name="claudeExp"]:checked').value,
        financialAid: document.getElementById('financialAid').checked,
        firstGen: document.getElementById('firstGen').checked
    };

    // Validation
    if (!formData.objective || formData.objective.length < 50) {
        showNotification('Objective must be at least 50 characters', 'error');
        return;
    }

    // Show success message
    showNotification('Application submitted successfully! Your score is 78/100 and you have been APPROVED.', 'success');
    
    // Switch to status tab
    setTimeout(() => {
        switchStudentTab('application-status');
    }, 1500);
}

function submitProgressReport() {
    const formData = {
        projectDesc: document.getElementById('projectDesc').value,
        claudeUsage: document.getElementById('claudeUsage').value,
        outcomes: document.getElementById('outcomes').value
    };

    // Validation
    if (!formData.projectDesc || formData.projectDesc.length < 100) {
        showNotification('Project description must be at least 100 characters', 'error');
        return;
    }

    if (!formData.claudeUsage.trim()) {
        showNotification('Please provide Claude usage examples', 'error');
        return;
    }

    if (!formData.outcomes.trim()) {
        showNotification('Please describe outcomes achieved', 'error');
        return;
    }

    // Show success message
    showNotification('Progress report submitted successfully! Extension of 30 days has been approved.', 'success');
    
    // Reset form
    document.getElementById('progressForm').reset();
    updateProgressCharCounter();
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
`;
document.head.appendChild(style);

// Export functionality
function exportCSV() {
    showNotification('Exporting applications to CSV...', 'info');
    // Implementation would go here
}

// Bulk actions
function bulkApprove() {
    showNotification('Bulk approval initiated for selected applications', 'success');
}

function bulkReject() {
    showNotification('Bulk rejection initiated for selected applications', 'success');
}

// Configuration save
function saveConfiguration() {
    showNotification('Configuration saved successfully', 'success');
}

// Add event listeners for configuration buttons
document.addEventListener('DOMContentLoaded', () => {
    const saveButtons = document.querySelectorAll('.btn-primary');
    saveButtons.forEach(btn => {
        if (btn.textContent.includes('Save Changes')) {
            btn.addEventListener('click', saveConfiguration);
        }
    });
});
