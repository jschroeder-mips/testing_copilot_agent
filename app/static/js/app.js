/**
 * CyberTODO 2077 - Client-side JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize navbar burger for mobile
    initNavbarBurger();
    
    // Initialize notification auto-hide
    initNotifications();
    
    // Initialize form enhancements
    initFormEnhancements();
    
    // Initialize cyber effects
    initCyberEffects();
});

/**
 * Initialize mobile navbar burger menu
 */
function initNavbarBurger() {
    const navbarBurger = document.getElementById('navbar-burger');
    const navbarMenu = document.getElementById('navbar-menu');
    
    if (navbarBurger && navbarMenu) {
        navbarBurger.addEventListener('click', function() {
            navbarBurger.classList.toggle('is-active');
            navbarMenu.classList.toggle('is-active');
        });
    }
}

/**
 * Initialize notification behavior
 */
function initNotifications() {
    // Auto-hide notifications after 5 seconds
    setTimeout(function() {
        const notifications = document.querySelectorAll('.notification');
        notifications.forEach(function(notification) {
            notification.style.opacity = '0';
            setTimeout(function() {
                notification.style.display = 'none';
            }, 300);
        });
    }, 5000);
    
    // Manual close notifications
    document.querySelectorAll('.notification .delete').forEach(function(button) {
        button.addEventListener('click', function() {
            const notification = this.parentElement;
            notification.style.opacity = '0';
            setTimeout(function() {
                notification.style.display = 'none';
            }, 300);
        });
    });
}

/**
 * Initialize form enhancements
 */
function initFormEnhancements() {
    // Add focus effects to form fields
    const formFields = document.querySelectorAll('.input, .textarea, .select select');
    formFields.forEach(function(field) {
        field.addEventListener('focus', function() {
            this.parentElement.classList.add('is-focused');
        });
        
        field.addEventListener('blur', function() {
            this.parentElement.classList.remove('is-focused');
        });
    });
    
    // Enhance datetime input for due date
    const dueDateInput = document.querySelector('input[name="due_date"]');
    if (dueDateInput) {
        dueDateInput.addEventListener('focus', function() {
            this.type = 'datetime-local';
        });
    }
    
    // Form validation feedback
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let hasErrors = false;
            
            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    field.classList.add('is-danger');
                    hasErrors = true;
                } else {
                    field.classList.remove('is-danger');
                }
            });
            
            if (hasErrors) {
                e.preventDefault();
                showNotification('Please fill in all required fields', 'is-danger');
            }
        });
    });
}

/**
 * Initialize cyberpunk visual effects
 */
function initCyberEffects() {
    // Add glitch effect to buttons on hover
    const buttons = document.querySelectorAll('.cyber-button-primary, .cyber-button-secondary');
    buttons.forEach(function(button) {
        button.addEventListener('mouseenter', function() {
            this.style.animation = 'cyber-glitch 0.3s ease-in-out';
        });
        
        button.addEventListener('animationend', function() {
            this.style.animation = '';
        });
    });
    
    // Add typing effect to title (if present)
    const heroTitle = document.querySelector('.hero .title.is-1');
    if (heroTitle) {
        typewriterEffect(heroTitle);
    }
    
    // Add matrix rain effect to background (subtle)
    createMatrixRain();
}

/**
 * Create typewriter effect for text
 */
function typewriterEffect(element) {
    const text = element.textContent;
    element.textContent = '';
    element.style.borderRight = '2px solid #00ffff';
    
    let i = 0;
    const timer = setInterval(function() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
        } else {
            clearInterval(timer);
            // Remove cursor after typing
            setTimeout(function() {
                element.style.borderRight = 'none';
            }, 1000);
        }
    }, 100);
}

/**
 * Create subtle matrix rain background effect
 */
function createMatrixRain() {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.zIndex = '-1';
    canvas.style.opacity = '0.1';
    canvas.style.pointerEvents = 'none';
    
    document.body.appendChild(canvas);
    
    const resizeCanvas = () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    };
    
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    const chars = '01';
    const charSize = 14;
    const columns = canvas.width / charSize;
    const drops = [];
    
    for (let i = 0; i < columns; i++) {
        drops[i] = 1;
    }
    
    const draw = () => {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = '#00ffff';
        ctx.font = charSize + 'px monospace';
        
        for (let i = 0; i < drops.length; i++) {
            const text = chars[Math.floor(Math.random() * chars.length)];
            ctx.fillText(text, i * charSize, drops[i] * charSize);
            
            if (drops[i] * charSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    };
    
    setInterval(draw, 100);
}

/**
 * Show notification message
 */
function showNotification(message, type = 'is-info') {
    const notification = document.createElement('div');
    notification.className = `notification cyber-notification ${type}`;
    notification.innerHTML = `
        <button class="delete"></button>
        ${message}
    `;
    
    // Insert at top of page
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(notification, container.firstChild);
    }
    
    // Auto-hide
    setTimeout(function() {
        notification.style.opacity = '0';
        setTimeout(function() {
            notification.remove();
        }, 300);
    }, 5000);
    
    // Manual close
    notification.querySelector('.delete').addEventListener('click', function() {
        notification.style.opacity = '0';
        setTimeout(function() {
            notification.remove();
        }, 300);
    });
}

/**
 * API Helper functions
 */
const CyberAPI = {
    /**
     * Make API request
     */
    async request(endpoint, options = {}) {
        const response = await fetch(`/api${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        
        return response.json();
    },
    
    /**
     * Get all todos
     */
    async getTodos(filters = {}) {
        const params = new URLSearchParams(filters);
        return this.request(`/todos?${params}`);
    },
    
    /**
     * Create new todo
     */
    async createTodo(todoData) {
        return this.request('/todos', {
            method: 'POST',
            body: JSON.stringify(todoData)
        });
    },
    
    /**
     * Update todo
     */
    async updateTodo(id, todoData) {
        return this.request(`/todos/${id}`, {
            method: 'PUT',
            body: JSON.stringify(todoData)
        });
    },
    
    /**
     * Delete todo
     */
    async deleteTodo(id) {
        return this.request(`/todos/${id}`, {
            method: 'DELETE'
        });
    }
};

// Export for use in other scripts
window.CyberAPI = CyberAPI;