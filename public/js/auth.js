// Authentication Management

function saveAuthData(token, user) {
  localStorage.setItem('authToken', token);
  localStorage.setItem('user', JSON.stringify(user));
}

function getAuthData() {
  const token = localStorage.getItem('authToken');
  const userStr = localStorage.getItem('user');
  const user = userStr ? JSON.parse(userStr) : null;
  return { token, user };
}

function isAuthenticated() {
  const { token } = getAuthData();
  return !!token;
}

function requireAuth() {
  if (!isAuthenticated()) {
    window.location.href = '/pages/login.html';
    return false;
  }
  return true;
}

function isAdmin() {
  const { user } = getAuthData();
  return user && user.role === 'admin';
}

function requireAdmin() {
  if (!requireAuth()) return false;
  if (!isAdmin()) {
    alert('Admin access required');
    window.location.href = '/pages/dashboard.html';
    return false;
  }
  return true;
}

// Handle registration
async function handleRegister(event) {
  event.preventDefault();
  
  const form = event.target;
  const submitBtn = form.querySelector('button[type="submit"]');
  const errorDiv = form.querySelector('.error-message');
  
  try {
    submitBtn.disabled = true;
    submitBtn.textContent = 'Creating Account...';
    
    const userData = {
      email: form.email.value,
      password: form.password.value,
      firstName: form.firstName.value,
      lastName: form.lastName.value,
      phone: form.phone?.value || '',
      role: form.role?.value || 'user',
      referralCode: form.referralCode?.value || ''
    };

    const response = await authAPI.register(userData);
    
    saveAuthData(response.token, response.user);
    
    window.location.href = '/pages/dashboard.html';
    
  } catch (error) {
    if (errorDiv) {
      errorDiv.textContent = error.message;
      errorDiv.style.display = 'block';
    } else {
      alert(error.message);
    }
    submitBtn.disabled = false;
    submitBtn.textContent = 'Create Account';
  }
}

// Handle login
async function handleLogin(event) {
  event.preventDefault();
  
  const form = event.target;
  const submitBtn = form.querySelector('button[type="submit"]');
  const errorDiv = form.querySelector('.error-message');
  
  try {
    submitBtn.disabled = true;
    submitBtn.textContent = 'Signing In...';
    
    const credentials = {
      email: form.email.value,
      password: form.password.value
    };

    const response = await authAPI.login(credentials);
    
    saveAuthData(response.token, response.user);
    
    // Redirect based on role
    if (response.user.role === 'admin') {
      window.location.href = '/pages/admin-dashboard.html';
    } else {
      window.location.href = '/pages/dashboard.html';
    }
    
  } catch (error) {
    if (errorDiv) {
      errorDiv.textContent = error.message;
      errorDiv.style.display = 'block';
    } else {
      alert(error.message);
    }
    submitBtn.disabled = false;
    submitBtn.textContent = 'Sign In';
  }
}

// Logout function
function logout() {
  authAPI.logout();
}

// Display user info
function displayUserInfo(elementId) {
  const { user } = getAuthData();
  const element = document.getElementById(elementId);
  
  if (element && user) {
    element.textContent = `${user.firstName} ${user.lastName}`;
  }
}
