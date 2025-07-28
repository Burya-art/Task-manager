document.addEventListener('DOMContentLoaded', function() {

    // Автофокус на поле вводу задачі
    const taskInput = document.querySelector('input[name="name"]');
    if (taskInput) {
        taskInput.focus();
    }

    // Обробка клавіші Enter в полі задачі
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.target.matches('input[name="name"]')) {
            e.preventDefault();
            const form = e.target.closest('form');
            if (form) {
                form.dispatchEvent(new Event('submit', { bubbles: true }));
            }
        }
    });

    // Анімація нових задач
    document.body.addEventListener('htmx:afterSettle', function(evt) {
        // evt.target може бути елементом, який був вставлений HTMX
        // або батьківським елементом, якщо HTMX оновив його вміст
        const newTask = evt.target.querySelector('.task-item:last-child');

        // Перевіряємо, чи новий елемент дійсно є task-item і ще не був анімований
        if (newTask && newTask.closest('#task-list') === evt.target && !newTask.classList.contains('animated')) {
            newTask.classList.add('animated');
            newTask.style.animation = 'fadeInUp 0.3s ease-out';
        } else if (evt.target.classList.contains('task-item') && !evt.target.classList.contains('animated')) {
            // Випадок, коли HTMX оновив сам task-item (наприклад, після редагування)
            evt.target.classList.add('animated');
            evt.target.style.animation = 'fadeInUp 0.3s ease-out'; // Або інша анімація для оновлення
        }
    });

    // Обробка порожнього стану списку
    function checkEmptyState() {
        const taskList = document.getElementById('task-list');
        if (taskList && taskList.children.length === 0) {
            taskList.innerHTML = `
                <div class="p-4 text-center text-muted">
                    <i class="fas fa-tasks fa-2x mb-2"></i>
                    <p>Немає задач у цьому проекті</p>
                </div>
            `;
        }
    }

    // Перевірка порожнього стану після видалення задач
    document.body.addEventListener('htmx:afterSettle', function(evt) {
        // Перевіряємо, чи запит був успішним і чи потенційно змінився список
        // Особливо актуально після видалення
        if (evt.detail.xhr && evt.detail.xhr.status === 200) {
            // Використовуємо setTimeout, щоб дати HTMX час оновити DOM
            setTimeout(checkEmptyState, 100);
        }
    });
});