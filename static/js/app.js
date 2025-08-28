/**
 * Cyberpunk TODO 2077 - JavaScript Application
 * Handles all frontend interactions with the TODO API
 */

// Global variables
let currentEditTodoId = null;

// API helper functions
async function apiRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    const response = await fetch(url, { ...defaultOptions, ...options });
    
    if (!response.ok) {
        const error = await response.json().catch(() => ({ message: 'Unknown error' }));
        throw new Error(error.message || `HTTP ${response.status}`);
    }
    
    return response.status === 204 ? null : await response.json();
}

// Show notification
function showNotification(message, type = 'info') {
    const container = document.querySelector('.container');
    const notification = document.createElement('div');
    notification.className = `notification is-${type} cyberpunk-notification`;
    notification.innerHTML = `
        <button class="delete"></button>
        <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'danger' ? 'fa-exclamation-triangle' : 'fa-info-circle'}"></i>
        ${message}
    `;
    
    container.insertBefore(notification, container.firstChild);
    
    // Auto-dismiss
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
    
    // Manual dismiss
    notification.querySelector('.delete').addEventListener('click', () => {
        notification.parentNode.removeChild(notification);
    });
}

// Add loading state to element
function setLoading(element, loading = true) {
    if (loading) {
        element.classList.add('loading');
        element.disabled = true;
    } else {
        element.classList.remove('loading');
        element.disabled = false;
    }
}

// Create todo item HTML
function createTodoItemHTML(todo) {
    const priorityClass = `priority-${todo.priority}`;
    const completedClass = todo.completed ? 'todo-completed' : '';
    const titleContent = todo.completed ? `<del>${todo.title}</del>` : todo.title;
    const descriptionContent = todo.description ? 
        (todo.completed ? `<del>${todo.description}</del>` : todo.description) : '';
    const icon = todo.completed ? 'fa-check-circle has-text-success' : `fa-circle ${priorityClass}`;
    const dateLabel = todo.completed ? 'fa-flag-checkered' : 'fa-clock';
    const dateValue = todo.completed ? todo.updated_at : todo.created_at;
    
    const toggleButton = todo.completed ? 
        '<button class="button is-warning is-small cyberpunk-button-small" onclick="toggleTodo(' + todo.id + ')"><i class="fas fa-undo"></i></button>' :
        '<button class="button is-success is-small cyberpunk-button-small" onclick="toggleTodo(' + todo.id + ')"><i class="fas fa-check"></i></button>';
    
    const editButton = todo.completed ? '' :
        '<button class="button is-info is-small cyberpunk-button-small" onclick="editTodo(' + todo.id + ')"><i class="fas fa-edit"></i></button>';
    
    return `
        <div class="todo-item cyberpunk-todo-item ${completedClass}" data-todo-id="${todo.id}">
            <div class="level is-mobile">
                <div class="level-left">
                    <div class="level-item">
                        <div>
                            <p class="todo-title">
                                <i class="fas ${icon}"></i>
                                ${titleContent}
                            </p>
                            ${descriptionContent ? `<p class="todo-description has-text-grey-light">${descriptionContent}</p>` : ''}
                            <p class="todo-meta has-text-grey-lighter">
                                <small>
                                    <i class="fas ${dateLabel}"></i> ${new Date(dateValue).toLocaleString()}
                                    ${!todo.completed ? `<span class="tag is-small is-${todo.priority === 'critical' ? 'danger' : todo.priority === 'high' ? 'warning' : todo.priority === 'medium' ? 'info' : 'light'}">${todo.priority.toUpperCase()}</span>` : ''}
                                </small>
                            </p>
                        </div>
                    </div>
                </div>
                <div class="level-right">
                    <div class="level-item">
                        <div class="buttons">
                            ${toggleButton}
                            ${editButton}
                            <button class="button is-danger is-small cyberpunk-button-small" onclick="deleteTodo(${todo.id})">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Add new todo
async function addTodo(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitButton = form.querySelector('button[type="submit"]');
    const title = document.getElementById('todoTitle').value.trim();
    const description = document.getElementById('todoDescription').value.trim();
    const priority = document.getElementById('todoPriority').value;
    
    if (!title) {
        showNotification('Task title is required', 'danger');
        return;
    }
    
    setLoading(submitButton);
    
    try {
        const newTodo = await apiRequest('/api/todos', {
            method: 'POST',
            body: JSON.stringify({
                title,
                description,
                priority
            })
        });
        
        // Add to pending todos list
        const pendingTodos = document.getElementById('pendingTodos');
        const todoHTML = createTodoItemHTML(newTodo);
        
        // Check if there's a "no tasks" message and remove it
        const emptyMessage = pendingTodos.querySelector('.has-text-centered');
        if (emptyMessage) {
            emptyMessage.remove();
        }
        
        pendingTodos.insertAdjacentHTML('afterbegin', todoHTML);
        
        // Clear form
        form.reset();
        
        // Update stats
        updateStats();
        
        showNotification('Task added successfully!', 'success');
        
    } catch (error) {
        console.error('Error adding todo:', error);
        showNotification('Failed to add task: ' + error.message, 'danger');
    } finally {
        setLoading(submitButton, false);
    }
}

// Toggle todo completion
async function toggleTodo(todoId) {
    try {
        const updatedTodo = await apiRequest(`/api/todos/${todoId}/toggle`, {
            method: 'PATCH'
        });
        
        // Remove from current list
        const todoElement = document.querySelector(`[data-todo-id="${todoId}"]`);
        if (todoElement) {
            todoElement.remove();
        }
        
        // Add to appropriate list
        const targetList = updatedTodo.completed ? 
            document.getElementById('completedTodos') : 
            document.getElementById('pendingTodos');
        
        // Check if list is empty and remove empty message
        const emptyMessage = targetList.querySelector('.has-text-centered');
        if (emptyMessage) {
            emptyMessage.remove();
        }
        
        const todoHTML = createTodoItemHTML(updatedTodo);
        targetList.insertAdjacentHTML('afterbegin', todoHTML);
        
        // Update stats
        updateStats();
        
        const message = updatedTodo.completed ? 'Task completed!' : 'Task reactivated!';
        showNotification(message, 'success');
        
    } catch (error) {
        console.error('Error toggling todo:', error);
        showNotification('Failed to update task: ' + error.message, 'danger');
    }
}

// Delete todo
async function deleteTodo(todoId) {
    if (!confirm('Are you sure you want to delete this task? This action cannot be undone.')) {
        return;
    }
    
    try {
        await apiRequest(`/api/todos/${todoId}`, {
            method: 'DELETE'
        });
        
        // Remove from UI
        const todoElement = document.querySelector(`[data-todo-id="${todoId}"]`);
        if (todoElement) {
            todoElement.style.opacity = '0';
            setTimeout(() => {
                todoElement.remove();
                
                // Check if list is empty and show empty message
                const pendingTodos = document.getElementById('pendingTodos');
                const completedTodos = document.getElementById('completedTodos');
                
                if (pendingTodos && pendingTodos.children.length === 0) {
                    pendingTodos.innerHTML = `
                        <div class="has-text-centered has-text-grey-light py-6">
                            <i class="fas fa-robot fa-3x mb-3"></i>
                            <p>No active processes. System idle.</p>
                        </div>
                    `;
                }
                
                if (completedTodos && completedTodos.children.length === 0) {
                    completedTodos.innerHTML = `
                        <div class="has-text-centered has-text-grey-light py-6">
                            <i class="fas fa-battery-empty fa-3x mb-3"></i>
                            <p>No completed tasks yet.</p>
                        </div>
                    `;
                }
                
                // Update stats
                updateStats();
            }, 300);
        }
        
        showNotification('Task deleted successfully!', 'success');
        
    } catch (error) {
        console.error('Error deleting todo:', error);
        showNotification('Failed to delete task: ' + error.message, 'danger');
    }
}

// Edit todo
async function editTodo(todoId) {
    try {
        const todo = await apiRequest(`/api/todos/${todoId}`);
        
        // Populate edit form
        document.getElementById('editTodoId').value = todo.id;
        document.getElementById('editTodoTitle').value = todo.title;
        document.getElementById('editTodoDescription').value = todo.description || '';
        document.getElementById('editTodoPriority').value = todo.priority;
        
        // Show modal
        document.getElementById('editTodoModal').classList.add('is-active');
        currentEditTodoId = todoId;
        
    } catch (error) {
        console.error('Error loading todo for edit:', error);
        showNotification('Failed to load task details: ' + error.message, 'danger');
    }
}

// Save edited todo
async function saveEditTodo() {
    const todoId = currentEditTodoId;
    const title = document.getElementById('editTodoTitle').value.trim();
    const description = document.getElementById('editTodoDescription').value.trim();
    const priority = document.getElementById('editTodoPriority').value;
    
    if (!title) {
        showNotification('Task title is required', 'danger');
        return;
    }
    
    try {
        const updatedTodo = await apiRequest(`/api/todos/${todoId}`, {
            method: 'PUT',
            body: JSON.stringify({
                title,
                description,
                priority
            })
        });
        
        // Update in UI
        const todoElement = document.querySelector(`[data-todo-id="${todoId}"]`);
        if (todoElement) {
            todoElement.outerHTML = createTodoItemHTML(updatedTodo);
        }
        
        // Close modal
        closeEditModal();
        
        showNotification('Task updated successfully!', 'success');
        
    } catch (error) {
        console.error('Error updating todo:', error);
        showNotification('Failed to update task: ' + error.message, 'danger');
    }
}

// Close edit modal
function closeEditModal() {
    document.getElementById('editTodoModal').classList.remove('is-active');
    currentEditTodoId = null;
}

// Update statistics
async function updateStats() {
    try {
        const stats = await apiRequest('/api/stats');
        
        // Update stat boxes
        document.querySelectorAll('.cyberpunk-stat-box').forEach((box, index) => {
            const title = box.querySelector('.title');
            if (title) {
                switch (index) {
                    case 0: title.textContent = stats.total; break;
                    case 1: title.textContent = stats.pending; break;
                    case 2: title.textContent = stats.completed; break;
                    case 3: title.textContent = stats.completion_rate + '%'; break;
                }
            }
        });
        
        // Update progress bar
        const progressBar = document.querySelector('.cyberpunk-progress');
        if (progressBar) {
            progressBar.value = stats.completion_rate;
        }
        
        // Update tags
        const pendingTag = document.querySelector('#pendingTodos').parentElement.querySelector('.tag');
        const completedTag = document.querySelector('#completedTodos').parentElement.querySelector('.tag');
        
        if (pendingTag) pendingTag.textContent = stats.pending;
        if (completedTag) completedTag.textContent = stats.completed;
        
    } catch (error) {
        console.error('Error updating stats:', error);
    }
}

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    // Add todo form handler
    const addTodoForm = document.getElementById('addTodoForm');
    if (addTodoForm) {
        addTodoForm.addEventListener('submit', addTodo);
    }
    
    // Edit todo form handler
    const editTodoForm = document.getElementById('editTodoForm');
    if (editTodoForm) {
        editTodoForm.addEventListener('submit', function(e) {
            e.preventDefault();
            saveEditTodo();
        });
    }
    
    // Modal close handlers
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal-background') || 
            e.target.classList.contains('modal-close')) {
            closeEditModal();
        }
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Escape key closes modals
        if (e.key === 'Escape') {
            closeEditModal();
        }
        
        // Ctrl/Cmd + Enter submits forms
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const activeElement = document.activeElement;
            if (activeElement && activeElement.form) {
                activeElement.form.dispatchEvent(new Event('submit'));
            }
        }
    });
    
    // Focus management
    const titleInput = document.getElementById('todoTitle');
    if (titleInput) {
        titleInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                const form = this.closest('form');
                if (form) {
                    form.dispatchEvent(new Event('submit'));
                }
            }
        });
    }
    
    // Auto-resize textareas
    document.querySelectorAll('textarea').forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    });
    
    // Add cyberpunk effects
    addCyberpunkEffects();
    
    console.log('🔮 Cyberpunk TODO 2077 initialized successfully');
});

// Add cyberpunk visual effects
function addCyberpunkEffects() {
    // Random glitch effect on title
    const titles = document.querySelectorAll('.cyberpunk-title');
    titles.forEach(title => {
        setInterval(() => {
            if (Math.random() < 0.1) { // 10% chance
                title.classList.add('glitch');
                setTimeout(() => {
                    title.classList.remove('glitch');
                }, 300);
            }
        }, 2000);
    });
    
    // Particle effect for successful actions
    window.createParticleEffect = function(x, y, color = '#00ffff') {
        const particle = document.createElement('div');
        particle.style.position = 'fixed';
        particle.style.left = x + 'px';
        particle.style.top = y + 'px';
        particle.style.width = '4px';
        particle.style.height = '4px';
        particle.style.backgroundColor = color;
        particle.style.pointerEvents = 'none';
        particle.style.zIndex = '9999';
        particle.style.borderRadius = '50%';
        particle.style.boxShadow = `0 0 10px ${color}`;
        document.body.appendChild(particle);
        
        // Animate particle
        const angle = Math.random() * Math.PI * 2;
        const velocity = 50 + Math.random() * 50;
        const vx = Math.cos(angle) * velocity;
        const vy = Math.sin(angle) * velocity;
        
        let px = x, py = y;
        let opacity = 1;
        
        const animate = () => {
            px += vx * 0.02;
            py += vy * 0.02;
            opacity -= 0.02;
            
            particle.style.left = px + 'px';
            particle.style.top = py + 'px';
            particle.style.opacity = opacity;
            
            if (opacity > 0) {
                requestAnimationFrame(animate);
            } else {
                document.body.removeChild(particle);
            }
        };
        
        requestAnimationFrame(animate);
    };
}