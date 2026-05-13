import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

@pytest.fixture(scope="function")
def driver():
    """Фикстура: драйвер Chrome для тестов"""
    
    options = Options()
    
    # Настройки для headless режима (важно для CI)
    if os.getenv('CI') == 'true':
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
    
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    # ИСПОЛЬЗУЕМ СИСТЕМНЫЙ CHROMEDRIVER (вместо webdriver-manager)
    service = Service('/usr/bin/chromedriver')
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture
def form_url():
    """URL формы для тестирования"""
    return "file:///" + os.path.abspath("index.html").replace("\\", "/")