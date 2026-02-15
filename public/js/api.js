// API Configuration
const API_BASE_URL = window.location.origin;

// API Helper Functions
async function apiCall(endpoint, options = {}) {
  const token = localStorage.getItem('authToken');
  
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    }
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers
    }
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || 'Request failed');
  }

  return data;
}

// Authentication API
const authAPI = {
  register: (userData) => apiCall('/api/auth/register', {
    method: 'POST',
    body: JSON.stringify(userData)
  }),

  login: (credentials) => apiCall('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify(credentials)
  }),

  getProfile: () => apiCall('/api/auth/profile'),

  logout: () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    window.location.href = '/';
  }
};

// Services API
const servicesAPI = {
  getAll: (filters = {}) => {
    const params = new URLSearchParams(filters);
    return apiCall(`/api/services?${params}`);
  },

  getById: (id) => apiCall(`/api/services/${id}`),

  create: (serviceData) => apiCall('/api/services', {
    method: 'POST',
    body: JSON.stringify(serviceData)
  }),

  update: (id, updates) => apiCall(`/api/services/${id}`, {
    method: 'PUT',
    body: JSON.stringify(updates)
  }),

  delete: (id) => apiCall(`/api/services/${id}`, {
    method: 'DELETE'
  })
};

// Bookings API
const bookingsAPI = {
  getAll: () => apiCall('/api/bookings'),

  create: (bookingData) => apiCall('/api/bookings', {
    method: 'POST',
    body: JSON.stringify(bookingData)
  })
};

// Reviews API
const reviewsAPI = {
  getByServiceId: (serviceId) => apiCall(`/api/reviews?serviceId=${serviceId}`),

  create: (reviewData) => apiCall('/api/reviews', {
    method: 'POST',
    body: JSON.stringify(reviewData)
  })
};

// Payments API
const paymentsAPI = {
  createPaymentIntent: (paymentData) => apiCall('/api/payments/stripe', {
    method: 'POST',
    body: JSON.stringify(paymentData)
  })
};

// Admin API
const adminAPI = {
  getStats: () => apiCall('/api/admin/stats')
};
