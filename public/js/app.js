// Main Application JavaScript

// Format currency
function formatCurrency(amount) {
  return `₦${parseFloat(amount).toLocaleString('en-NG', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

// Format date
function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-NG', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  });
}

// Show loading state
function showLoading(element, message = 'Loading...') {
  if (element) {
    element.innerHTML = `<div class="loading">${message}</div>`;
  }
}

// Show error message
function showError(element, message) {
  if (element) {
    element.innerHTML = `<div class="error">${message}</div>`;
  }
}

// Service card template
function createServiceCard(service) {
  return `
    <div class="service-card" data-id="${service._id}">
      <div class="service-image">
        <img src="${service.images[0] || '/images/placeholder.jpg'}" alt="${service.title}">
      </div>
      <div class="service-details">
        <h3>${service.title}</h3>
        <p class="service-description">${service.description.substring(0, 100)}...</p>
        <div class="service-meta">
          <span class="price">${formatCurrency(service.price)}</span>
          <span class="rating">⭐ ${service.rating || 0} (${service.reviewCount || 0})</span>
        </div>
        <div class="service-actions">
          <button onclick="viewService('${service._id}')" class="btn-primary">View Details</button>
          <button onclick="bookService('${service._id}')" class="btn-secondary">Book Now</button>
        </div>
      </div>
    </div>
  `;
}

// Booking card template
function createBookingCard(booking) {
  const statusClass = booking.status === 'completed' ? 'success' : 
                      booking.status === 'cancelled' ? 'danger' : 'warning';
  
  return `
    <div class="booking-card">
      <div class="booking-header">
        <h4>Booking #${booking._id.substring(0, 8)}</h4>
        <span class="status ${statusClass}">${booking.status}</span>
      </div>
      <div class="booking-details">
        <p><strong>Date:</strong> ${formatDate(booking.date)}</p>
        <p><strong>Time:</strong> ${booking.time}</p>
        <p><strong>Amount:</strong> ${formatCurrency(booking.totalAmount)}</p>
        <p><strong>Payment:</strong> <span class="status">${booking.paymentStatus}</span></p>
      </div>
    </div>
  `;
}

// View service details
async function viewService(serviceId) {
  window.location.href = `/pages/service-detail.html?id=${serviceId}`;
}

// Book service
async function bookService(serviceId) {
  if (!isAuthenticated()) {
    window.location.href = '/pages/login.html';
    return;
  }
  window.location.href = `/pages/booking.html?serviceId=${serviceId}`;
}

// Initialize tooltips and other UI elements
document.addEventListener('DOMContentLoaded', function() {
  // Add smooth scrolling
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
});
