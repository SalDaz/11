document.getElementById('registration-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Получаем значения полей
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    // Сбрасываем ошибки
    clearErrors();
    
    // Валидация
    let isValid = true;
    
    if (username.length < 3) {
        showError('username', 'Имя должно содержать минимум 3 символа');
        isValid = false;
    }
    
    if (!isValidEmail(email)) {
        showError('email', 'Введите корректный email');
        isValid = false;
    }
    
    if (password.length < 6) {
        showError('password', 'Пароль должен содержать минимум 6 символов');
        isValid = false;
    }
    
    // Если валидация прошла успешно
    if (isValid) {
        // Показываем сообщение об успехе
        document.getElementById('success-message').classList.remove('hidden');
        
        // Очищаем форму
        this.reset();
        
        // Скрываем сообщение через 3 секунды
        setTimeout(() => {
            document.getElementById('success-message').classList.add('hidden');
        }, 3000);
    }
});

function showError(fieldId, message) {
    const field = document.getElementById(fieldId);
    const error = document.getElementById(fieldId + '-error');
    
    field.classList.add('error');
    error.textContent = message;
}

function clearErrors() {
    document.querySelectorAll('.error').forEach(el => {
        el.textContent = '';
    });
    document.querySelectorAll('input').forEach(el => {
        el.classList.remove('error');
    });
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}