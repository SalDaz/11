"""
UI тесты для формы регистрации
Требование: 3-4 автоматизированных теста с Selenium
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestRegistrationForm:
    """Тесты формы регистрации"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, form_url):
        """Открываем форму перед каждым тестом"""
        driver.get(form_url)
        # Ждём загрузки формы
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "registration-form"))
        )
    
    def test_form_elements_present(self, driver):
        """
        Тест 1: Проверка наличия всех элементов формы
        Ожидаемый результат: все поля и кнопка отображаются
        """
        # Проверяем наличие заголовка
        title = driver.find_element(By.ID, "page-title")
        assert title.text == "Регистрация пользователя", "Неверный заголовок"
        
        # Проверяем наличие полей ввода
        assert driver.find_element(By.ID, "username").is_displayed()
        assert driver.find_element(By.ID, "email").is_displayed()
        assert driver.find_element(By.ID, "password").is_displayed()
        
        # Проверяем наличие кнопки
        submit_btn = driver.find_element(By.ID, "submit-btn")
        assert submit_btn.is_displayed()
        assert submit_btn.text == "Зарегистрироваться"
    
    def test_successful_registration(self, driver):
        """
        Тест 2: Успешная регистрация с валидными данными
        Ожидаемый результат: форма очищается или показывается успех
        """
        # Заполняем форму валидными данными
        driver.find_element(By.ID, "username").send_keys("testuser")
        driver.find_element(By.ID, "email").send_keys("test@example.com")
        driver.find_element(By.ID, "password").send_keys("password123")
        
        # Отправляем форму
        driver.find_element(By.ID, "submit-btn").click()
        
        # Проверяем что форма очистилась (признак успешной отправки)
        # Или ждём появление сообщения об успехе (если реализовано)
        try:
            # Вариант 1: Ждём сообщение об успехе (если есть в HTML)
            success_msg = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "success-message"))
            )
            assert success_msg.is_displayed()
        except:
            # Вариант 2: Проверяем что поля очистились (альтернативный признак успеха)
            username = driver.find_element(By.ID, "username").get_attribute("value")
            email = driver.find_element(By.ID, "email").get_attribute("value")
            password = driver.find_element(By.ID, "password").get_attribute("value")
            assert username == "" and email == "" and password == "", "Form should be cleared on success"
    
    def test_validation_username_too_short(self, driver):
        """
        Тест 3: Валидация - имя слишком короткое
        Ожидаемый результат: браузер показывает ошибку валидации
        """
        # Вводим слишком короткое имя (менее 3 символов)
        username_field = driver.find_element(By.ID, "username")
        username_field.send_keys("ab")  # 2 символа, минимум 3
        
        # Вводим остальные валидные данные
        driver.find_element(By.ID, "email").send_keys("test@example.com")
        driver.find_element(By.ID, "password").send_keys("password123")
        
        # Пытаемся отправить форму
        driver.find_element(By.ID, "submit-btn").click()
        
        # Проверяем что поле имеет класс ошибки ИЛИ браузерная валидация сработала
        # Для HTML5 валидации проверяем validity API через JavaScript
        is_invalid = driver.execute_script(
            "return document.getElementById('username').validity.tooShort || "
            "document.getElementById('username').validity.valueMissing;"
        )
        assert is_invalid, "Username validation should fail for short input"
    
    def test_validation_invalid_email(self, driver):
        """
        Тест 4: Валидация - некорректный email
        Ожидаемый результат: браузер показывает ошибку валидации
        """
        # Вводим валидное имя и пароль
        driver.find_element(By.ID, "username").send_keys("testuser")
        
        # Вводим некорректный email (без @)
        email_field = driver.find_element(By.ID, "email")
        email_field.send_keys("invalid-email")
        
        driver.find_element(By.ID, "password").send_keys("password123")
        
        # Пытаемся отправить форму
        driver.find_element(By.ID, "submit-btn").click()
        
        # Проверяем что поле email не прошло валидацию через JavaScript validity API
        is_invalid = driver.execute_script(
            "return document.getElementById('email').validity.typeMismatch;"
        )
        assert is_invalid, "Email validation should fail for invalid format"