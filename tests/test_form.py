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
        Ожидаемый результат: показывается сообщение об успехе
        """
        # Заполняем форму валидными данными
        driver.find_element(By.ID, "username").send_keys("testuser")
        driver.find_element(By.ID, "email").send_keys("test@example.com")
        driver.find_element(By.ID, "password").send_keys("password123")
        
        # Отправляем форму
        driver.find_element(By.ID, "submit-btn").click()
        
        # Проверяем сообщение об успехе
        success_msg = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "success-message"))
        )
        assert success_msg.is_displayed()
        assert "Регистрация успешна" in success_msg.text
    
    def test_validation_username_too_short(self, driver):
        """
        Тест 3: Валидация - имя слишком короткое
        Ожидаемый результат: показывается ошибка, форма не отправляется
        """
        # Вводим слишком короткое имя
        driver.find_element(By.ID, "username").send_keys("ab")
        driver.find_element(By.ID, "email").send_keys("test@example.com")
        driver.find_element(By.ID, "password").send_keys("password123")
        
        # Пытаемся отправить форму
        driver.find_element(By.ID, "submit-btn").click()
        
        # Проверяем что показана ошибка
        username_error = driver.find_element(By.ID, "username-error")
        assert username_error.text != "", "Ошибка не показана"
        assert "минимум 3 символа" in username_error.text.lower()
        
        # Проверяем что сообщение об успехе НЕ показано
        success_msg = driver.find_elements(By.ID, "success-message")
        assert len(success_msg) == 0 or "hidden" in success_msg[0].get_attribute("class")
    
    def test_validation_invalid_email(self, driver):
        """
        Тест 4: Валидация - некорректный email
        Ожидаемый результат: показывается ошибка для email
        """
        # Вводим некорректный email
        driver.find_element(By.ID, "username").send_keys("testuser")
        driver.find_element(By.ID, "email").send_keys("invalid-email")
        driver.find_element(By.ID, "password").send_keys("password123")
        
        # Пытаемся отправить форму
        driver.find_element(By.ID, "submit-btn").click()
        
        # Проверяем ошибку email
        email_error = driver.find_element(By.ID, "email-error")
        assert email_error.text != "", "Ошибка email не показана"
        assert "корректный" in email_error.text.lower() or "email" in email_error.text.lower()