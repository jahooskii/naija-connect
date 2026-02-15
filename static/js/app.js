// Naija Connect JavaScript - Powered by Saint Works LTD

// Global state
let currentUser = null;
let authToken = null;

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
    loadServices();
});

// Authentication functions
function checkAuth() {
    const token = localStorage.getItem('authToken');
    const user = localStorage.getItem('currentUser');
    
    if (token && user) {
        authToken = token;
        currentUser = JSON.parse(user);
        updateAuthUI();
    }
}

function updateAuthUI() {
    const authNav = document.getElementById('authNav');
    const userNav = document.getElementById('userNav');
    const userName = document.getElementById('userName');
    
    if (currentUser) {
        authNav.style.display = 'none';
        userNav.style.display = 'block';
        userName.textContent = `Welcome, ${currentUser.full_name || currentUser.username}`;
    } else {
        authNav.style.display = 'block';
        userNav.style.display = 'none';
    }
}

// API calls
async function apiCall(endpoint, method = 'GET', data = null) {
    const headers = {
        'Content-Type': 'application/json'
    };
    
    if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`;
    }
    
    const options = {
        method,
        headers
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(`/api${endpoint}`, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.message || 'Request failed');
        }
        
        return result;
    } catch (error) {
        showAlert(error.message, 'error');
        throw error;
    }
}

// Login
async function handleLogin(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    try {
        const result = await apiCall('/login', 'POST', {
            username: formData.get('username'),
            password: formData.get('password')
        });
        
        authToken = result.token;
        currentUser = result.user;
        
        localStorage.setItem('authToken', authToken);
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
        
        updateAuthUI();
        closeModal('loginModal');
        showAlert('Login successful!', 'success');
        
        form.reset();
    } catch (error) {
        // Error already shown by apiCall
    }
}

// Register
async function handleRegister(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    try {
        await apiCall('/register', 'POST', {
            username: formData.get('username'),
            email: formData.get('email'),
            full_name: formData.get('full_name'),
            phone: formData.get('phone'),
            password: formData.get('password'),
            is_provider: formData.get('is_provider') === 'on'
        });
        
        showAlert('Registration successful! Please login.', 'success');
        closeModal('registerModal');
        showLogin();
        
        form.reset();
    } catch (error) {
        // Error already shown by apiCall
    }
}

// Logout
function logout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    authToken = null;
    currentUser = null;
    updateAuthUI();
    showAlert('Logged out successfully', 'info');
}

// Load services
async function loadServices(category = '', search = '') {
    const servicesList = document.getElementById('servicesList');
    servicesList.innerHTML = '<div class="spinner"></div>';
    
    try {
        let endpoint = '/services?';
        if (category) endpoint += `category=${category}&`;
        if (search) endpoint += `search=${search}`;
        
        const services = await apiCall(endpoint);
        
        if (services.length === 0) {
            servicesList.innerHTML = '<p style="text-align: center; padding: 2rem;">No services found</p>';
            return;
        }
        
        servicesList.innerHTML = services.map(service => `
            <div class="service-card" onclick="viewService(${service.id})">
                <div class="service-image">${getCategoryIcon(service.category)}</div>
                <div class="service-content">
                    <span class="category">${service.category}</span>
                    <h3>${service.title}</h3>
                    <p>${service.description.substring(0, 100)}...</p>
                    <div class="price">₦${service.price.toLocaleString()}</div>
                    <div class="location">📍 ${service.location || 'Nigeria'}</div>
                    <div>Provider: ${service.provider.name}</div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        servicesList.innerHTML = '<p style="text-align: center; padding: 2rem;">Error loading services</p>';
    }
}

// View service details
async function viewService(serviceId) {
    try {
        const service = await apiCall(`/services/${serviceId}`);
        const reviews = await apiCall(`/reviews/${serviceId}`);
        
        const serviceDetails = document.getElementById('serviceDetails');
        serviceDetails.innerHTML = `
            <div class="service-image" style="height: 300px; font-size: 5rem;">
                ${getCategoryIcon(service.category)}
            </div>
            <h2>${service.title}</h2>
            <span class="category">${service.category}</span>
            <div class="price">₦${service.price.toLocaleString()}</div>
            <div class="rating">⭐ ${service.rating} (${service.review_count} reviews)</div>
            <div class="location">📍 ${service.location || 'Nigeria'}</div>
            <p style="margin: 1rem 0;">${service.description}</p>
            
            <h3>Provider Information</h3>
            <p><strong>Name:</strong> ${service.provider.name}</p>
            <p><strong>Contact:</strong> ${service.provider.phone || 'Contact via booking'}</p>
            
            ${currentUser ? `
                <button class="btn btn-primary btn-block" onclick="showBookingModal(${service.id}, '${service.title}', ${service.price})">
                    Book This Service
                </button>
            ` : `
                <p class="alert alert-info">Please login to book this service</p>
            `}
            
            <h3 style="margin-top: 2rem;">Reviews</h3>
            <div>
                ${reviews.length > 0 ? reviews.map(review => `
                    <div class="review-item">
                        <div class="review-header">
                            <div>
                                <div class="review-author">${review.reviewer}</div>
                                <div class="review-rating">${'⭐'.repeat(review.rating)}</div>
                            </div>
                            <div class="review-date">${new Date(review.created_at).toLocaleDateString()}</div>
                        </div>
                        <p>${review.comment}</p>
                    </div>
                `).join('') : '<p>No reviews yet</p>'}
            </div>
        `;
        
        showModal('serviceModal');
    } catch (error) {
        // Error handled by apiCall
    }
}

// Search services
function searchServices() {
    const search = document.getElementById('searchInput').value;
    const category = document.getElementById('categoryFilter').value;
    loadServices(category, search);
}

// Filter by category
function filterByCategory(category) {
    document.getElementById('categoryFilter').value = category;
    loadServices(category);
    document.getElementById('services').scrollIntoView({ behavior: 'smooth' });
}

// Show booking modal
function showBookingModal(serviceId, title, price) {
    if (!currentUser) {
        showAlert('Please login to book services', 'info');
        showLogin();
        return;
    }
    
    document.getElementById('bookingServiceId').value = serviceId;
    document.getElementById('bookingServiceDetails').innerHTML = `
        <h3>${title}</h3>
        <div class="price">₦${price.toLocaleString()}</div>
    `;
    
    showModal('bookingModal');
}

// Handle booking
async function handleBooking(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    try {
        const result = await apiCall('/bookings', 'POST', {
            service_id: parseInt(formData.get('service_id')),
            booking_date: formData.get('booking_date'),
            notes: formData.get('notes')
        });
        
        showAlert('Booking created successfully! Redirecting to payment...', 'success');
        closeModal('bookingModal');
        
        // Simulate payment
        setTimeout(() => {
            showPaymentModal(result.booking_id);
        }, 1000);
        
        form.reset();
    } catch (error) {
        // Error handled by apiCall
    }
}

// Show payment modal
function showPaymentModal(bookingId) {
    const confirmed = confirm('Proceed to payment? (This is a demo - no actual payment will be processed)');
    
    if (confirmed) {
        processPayment(bookingId);
    }
}

// Process payment
async function processPayment(bookingId) {
    try {
        const result = await apiCall('/payment', 'POST', {
            booking_id: bookingId,
            payment_method: 'card'
        });
        
        showAlert(`Payment successful! Transaction ID: ${result.transaction_id}`, 'success');
    } catch (error) {
        // Error handled by apiCall
    }
}

// Get category icon
function getCategoryIcon(category) {
    const icons = {
        home: '🏠',
        professional: '💼',
        beauty: '💅',
        tech: '💻',
        events: '🎉',
        transport: '🚗'
    };
    return icons[category] || '📦';
}

// Modal functions
function showModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

function showLogin() {
    closeModal('registerModal');
    showModal('loginModal');
}

function showRegister() {
    closeModal('loginModal');
    showModal('registerModal');
}

function showProviderRegistration() {
    showRegister();
    setTimeout(() => {
        document.getElementById('isProvider').checked = true;
    }, 100);
}

// Close modal when clicking outside
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
}

// Toggle mobile menu
function toggleMobileMenu() {
    const nav = document.getElementById('mainNav');
    nav.classList.toggle('active');
}

// Show alert
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    alertDiv.style.position = 'fixed';
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '3000';
    alertDiv.style.maxWidth = '400px';
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Dashboard
async function showDashboard() {
    if (!currentUser) {
        showLogin();
        return;
    }
    
    try {
        const bookings = await apiCall('/bookings');
        
        const dashboardContent = document.getElementById('dashboardContent');
        dashboardContent.innerHTML = `
            <h3>My Bookings</h3>
            <div class="bookings-list">
                ${bookings.length > 0 ? bookings.map(booking => `
                    <div class="booking-item">
                        <div>
                            <strong>${booking.service.title}</strong><br>
                            <small>Provider: ${booking.service.provider}</small><br>
                            <small>Date: ${new Date(booking.booking_date).toLocaleString()}</small>
                        </div>
                        <div>
                            <div class="booking-status status-${booking.status}">${booking.status}</div>
                            <div style="margin-top: 0.5rem;">₦${booking.total_amount.toLocaleString()}</div>
                        </div>
                    </div>
                `).join('') : '<p>No bookings yet</p>'}
            </div>
        `;
        
        showModal('dashboardModal');
    } catch (error) {
        // Error handled by apiCall
    }
}
