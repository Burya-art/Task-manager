// HTMX event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Show loading state for HTMX requests
    document.body.addEventListener('htmx:beforeRequest', function(evt) {
        const target = evt.target;
        if (target.tagName === 'FORM') {
            const submitBtn = target.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
            }
        }
    });

    // Restore button state after request
    document.body.addEventListener('htmx:afterRequest', function(evt) {
        const target = evt.target;
        if (target.tagName === 'FORM') {
            const submitBtn = target.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = false;
                if (submitBtn.classList.contains('btn-add-task')) {
                    submitBtn.innerHTML = 'Add Task';
                } else if (submitBtn.classList.contains('input-group-text')) {
                    submitBtn.innerHTML = '<img src="/static/tasks/images/add-task-icon.png" alt="Add Task" width="20" height="20">';
                } else {
                    submitBtn.innerHTML = 'Save';
                }
            }
        }
    });

    // Handle form errors
    document.body.addEventListener('htmx:responseError', function(evt) {
        console.error('HTMX error:', evt.detail);
        alert('An error occurred. Please try again.');
    });
});

// HTMX configuration for CSRF token
document.addEventListener('DOMContentLoaded', function() {
    // Add CSRF token to headers for all HTMX requests
    document.body.addEventListener('htmx:configRequest', function(evt) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfToken) {
            evt.detail.headers['X-CSRFToken'] = csrfToken.value;
        }
    });
});