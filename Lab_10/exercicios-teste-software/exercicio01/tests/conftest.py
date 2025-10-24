"""
Fixtures compartilhadas para todos os testes
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import requests
import shutil


def tem_chrome_instalado():
    """Verifica se Chrome está instalado"""
    return shutil.which("google-chrome") is not None or shutil.which("chromium") is not None


@pytest.fixture
def chrome_driver():
    """Fixture que retorna uma instância do Chrome WebDriver"""
    if not tem_chrome_instalado():
        pytest.skip("Chrome não está instalado neste ambiente")
    
    options = Options()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    yield driver
    
    driver.quit()


@pytest.fixture
def headless_chrome_driver():
    """Fixture para Chrome em modo headless (sem interface gráfica)"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    yield driver
    
    driver.quit()


@pytest.fixture
def api_base_url():
    """URL base da API de testes"""
    return "https://jsonplaceholder.typicode.com"


@pytest.fixture
def api_session():
    """Sessão HTTP reutilizável para testes de API"""
    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/json',
        'User-Agent': 'Python-Test-Client/1.0'
    })
    
    yield session
    
    session.close()


@pytest.fixture
def auth_token():
    """
    Fixture que simula obtenção de token de autenticação
    Em produção, faria login real em uma API
    """
    # Simulação - em produção seria uma chamada real
    return "fake-jwt-token-for-testing"


def pytest_addoption(parser):
    """Adiciona opções customizadas ao pytest"""
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Executar testes web em modo headless"
    )


@pytest.fixture
def browser_option(request):
    """Retorna se deve usar modo headless"""
    return request.config.getoption("--headless")
