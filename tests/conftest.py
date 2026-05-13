import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

@pytest.fixture(scope="function")
def driver():
    """Фикстура: драйвер Chrome для тестов"""
    
    # Настройки для headless режима (важно для CI)
    options = Options()
    
    # Определяем, запущены ли тесты в CI
    if os.getenv('CI') == 'true':
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
    
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    driver.implicitly_wait(10)
    
    yield driver
    
    driver.quit()

@pytest.fixture
def form_url():
    """URL формы для тестирования"""
    # Для локальных тестов
    return "file:///" + os.path.abspath("index.html").replace("\\", "/")