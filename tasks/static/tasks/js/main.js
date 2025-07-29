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

    // Drag & Drop функціональність
    let draggedElement = null;

    // Коли починається перетягування
    document.addEventListener('dragstart', function(e) {
        if (e.target.classList.contains('draggable-task')) {
            draggedElement = e.target;
            e.target.style.opacity = '0.5';
        }
    });

    // Коли перетягування закінчується
    document.addEventListener('dragend', function(e) {
        if (e.target.classList.contains('draggable-task')) {
            e.target.style.opacity = '1';
        }
    });

    // Дозволяємо скидати елементи
    document.addEventListener('dragover', function(e) {
        e.preventDefault();
    });

    // Обробка скидання елемента
    document.addEventListener('drop', function(e) {
        e.preventDefault();
        if (draggedElement) {
            // Шукаємо найближчу задачу або список задач
            let dropTarget = e.target.closest('.draggable-task');
            let taskList = document.getElementById('task-list');
            
            if (dropTarget && draggedElement !== dropTarget) {
                // Скидаємо на іншу задачу - вставляємо перед нею
                taskList.insertBefore(draggedElement, dropTarget);
                updateTaskOrder();
            } else if (!dropTarget && e.target.closest('#task-list')) {
                // Скидаємо в порожнє місце списку - додаємо в кінець
                taskList.appendChild(draggedElement);
                updateTaskOrder();
            }
        }
    });

    // Функція оновлення порядку задач на сервері
    function updateTaskOrder() {
        const taskElements = document.querySelectorAll('.draggable-task');
        const taskIds = Array.from(taskElements).map(el => el.dataset.taskId);
        const projectId = window.location.pathname.split('/')[2]; // Отримуємо ID проєкту з URL
        
        // Відправляємо до Django через HTMX
        const formData = new FormData();
        taskIds.forEach(id => formData.append('task_ids[]', id));
        
        fetch(`/htmx/project/${projectId}/tasks/reorder/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        });
    }

});