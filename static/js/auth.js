// ===========================
// AUTHENTICATION JAVASCRIPT
// ===========================

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('loginForm') || document.getElementById('registerForm');
    
    if (form) {
        if (form.id === 'loginForm') {
            setupLogin();
        } else if (form.id === 'registerForm') {
            setupRegister();
        }
    }
});

function setupLogin() {
    const form = document.getElementById('loginForm');
    const errorMessage = document.getElementById('errorMessage');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });
            
            const text = await response.text();
            const data = text ? JSON.parse(text) : {};
            
            if (response.ok) {
                // Login successful
                window.location.href = '/home';
            } else {
                // Show error
                showError(errorMessage, data.message || 'Login failed. Please try again.');
            }
        } catch (error) {
            showError(errorMessage, 'An error occurred. Please try again.');
            console.error('Error:', error);
        }
    });
}

function setupRegister() {
    const form = document.getElementById('registerForm');
    const errorMessage = document.getElementById('errorMessage');
    const successMessage = document.getElementById('successMessage');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        // Client-side validation
        if (password !== confirmPassword) {
            showError(errorMessage, 'Passwords do not match');
            return;
        }
        
        if (password.length < 6) {
            showError(errorMessage, 'Password must be at least 6 characters long');
            return;
        }
        
        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, email, password, confirm_password: confirmPassword })
            });
            
            const text = await response.text();
            const data = text ? JSON.parse(text) : {};
            
            if (response.ok) {
                // Show success message
                showSuccess(successMessage, data.message || 'Registration successful!');
                // Clear form
                form.reset();
                // Redirect to login after 2 seconds
                setTimeout(() => {
                    window.location.href = '/login';
                }, 2000);
            } else {
                // Show error
                showError(errorMessage, data.message || 'Registration failed. Please try again.');
            }
        } catch (error) {
            showError(errorMessage, 'An error occurred. Please try again.');
            console.error('Error:', error);
        }
    });
}

function showError(element, message) {
    element.textContent = message;
    element.classList.add('show');
    element.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        element.classList.remove('show');
        element.style.display = 'none';
    }, 5000);
}

function showSuccess(element, message) {
    element.textContent = message;
    element.classList.add('show');
    element.style.display = 'block';
}
