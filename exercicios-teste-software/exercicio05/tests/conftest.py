"""
Configurações para testes parametrizados (API + Web)
"""
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# ===== FIXTURES PARA TESTES DE API =====

@pytest.fixture(scope="session")
def api_session():
    """
    Fixture: Sessão HTTP reutilizável para testes de API parametrizados
    """
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json"
    })
    
    yield session
    
    session.close()


@pytest.fixture
def api_base_urls():
    """URLs base para testes de API parametrizados"""
    return {
        "jsonplaceholder": "https://jsonplaceholder.typicode.com",
        "httpbin": "https://httpbin.org",
        "reqres": "https://reqres.in/api"
    }


# ===== FIXTURES PARA TESTES WEB =====

@pytest.fixture
def chrome_options_busca():
    """
    Configurações Chrome específicas para testes de busca parametrizados
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-images")  # Performance
    
    return options


@pytest.fixture
def chrome_driver_busca(chrome_options_busca):
    """
    WebDriver Chrome específico para testes de busca parametrizada
    
    Separado da fixture do exercício 04 para evitar conflitos
    """
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options_busca)
    
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(30)
    
    yield driver
    
    driver.quit()


# ===== FIXTURES COMPARTILHADAS =====

@pytest.fixture(autouse=True)
def delay_between_tests():
    """
    Delay automático entre todos os testes parametrizados
    """
    import time
    yield
    time.sleep(0.2)  # 200ms entre testes


@pytest.fixture
def timeout_config():
    """Configurações de timeout para testes parametrizados"""
    return {
        "api_timeout": 10,  # segundos para requisições API
        "web_timeout": 30,  # segundos para carregamento de páginas
        "element_timeout": 10  # segundos para encontrar elementos
    }