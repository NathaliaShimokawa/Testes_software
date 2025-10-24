"""
Configurações para testes web com Selenium e Page Object Model
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def chrome_options():
    """
    Configurações otimizadas do Chrome para testes automatizados
    """
    options = Options()
    options.add_argument("--headless")  # Execução em background
    options.add_argument("--no-sandbox")  # Necessário em alguns ambientes
    options.add_argument("--disable-dev-shm-usage")  # Evita problemas de memória
    options.add_argument("--disable-gpu")  # Desabilita GPU para headless
    options.add_argument("--window-size=1920,1080")  # Resolução fixa
    options.add_argument("--disable-web-security")  # Para testes locais
    options.add_argument("--disable-extensions")  # Desabilita extensões
    options.add_argument("--disable-plugins")  # Desabilita plugins
    options.add_argument("--disable-images")  # Não carrega imagens (performance)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    return options


@pytest.fixture
def chrome_driver(chrome_options):
    """
    Fixture principal: WebDriver Chrome configurado para Page Object Model
    
    Automaticamente gerencia instalação do ChromeDriver,
    inicializa o navegador com configurações otimizadas,
    e garante cleanup após cada teste.
    """
    # Instalação automática do ChromeDriver
    service = Service(ChromeDriverManager().install())
    
    # Inicializar WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Configurações adicionais
    driver.implicitly_wait(10)  # Espera implícita de 10s
    driver.set_page_load_timeout(30)  # Timeout de carregamento de página
    
    yield driver
    
    # Cleanup: fechar navegador
    driver.quit()


@pytest.fixture(autouse=True)
def delay_between_web_tests():
    """
    Fixture: Delay automático entre testes web para estabilidade
    
    Adiciona uma pequena pausa entre os testes para evitar
    problemas de timing e garantir que o navegador seja
    completamente reinicializado.
    """
    import time
    yield
    time.sleep(0.5)  # 500ms entre testes web


# Configurações específicas para Page Object Model
@pytest.fixture
def google_url():
    """URL base do Google para testes de busca"""
    return "https://www.google.com"


@pytest.fixture  
def search_terms():
    """Termos de busca padrão para testes"""
    return [
        "selenium python",
        "pytest tutorial", 
        "page object model",
        "web automation testing",
        "github copilot"
    ]