"""
Testes de Interface Web com Selenium
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.google_page import GooglePage


@pytest.mark.web
def test_titulo_google(chrome_driver):
    """Verifica título da página do Google"""
    chrome_driver.get("https://www.google.com")
    assert "Google" in chrome_driver.title


@pytest.mark.web
def test_busca_google(chrome_driver):
    """Testa funcionalidade de busca do Google"""
    chrome_driver.get("https://www.google.com")
    
    # Localizar campo de busca
    search_box = chrome_driver.find_element(By.NAME, "q")
    search_box.send_keys("Python testing")
    search_box.submit()
    
    # Aguardar resultados
    WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, "search"))
    )
    
    # Verificar resultados
    assert "Python" in chrome_driver.page_source


@pytest.mark.web
def test_busca_com_page_object(chrome_driver):
    """Teste usando Page Object Model"""
    google_page = GooglePage(chrome_driver)
    google_page.abrir()
    google_page.buscar("Selenium Python")
    
    assert google_page.tem_resultados()
    assert "Selenium" in google_page.get_texto_resultados()


@pytest.mark.web
@pytest.mark.parametrize("termo_busca", [
    "Python",
    "Selenium",
    "Pytest"
])
def test_busca_multiplos_termos(chrome_driver, termo_busca):
    """Testa busca com múltiplos termos"""
    google_page = GooglePage(chrome_driver)
    google_page.abrir()
    google_page.buscar(termo_busca)
    
    assert google_page.tem_resultados()


@pytest.mark.web
@pytest.mark.slow
def test_responsividade(chrome_driver):
    """Testa layout em diferentes resoluções"""
    viewports = [
        (1920, 1080),  # Desktop
        (768, 1024),   # Tablet
        (375, 667)     # Mobile
    ]
    
    for width, height in viewports:
        chrome_driver.set_window_size(width, height)
        chrome_driver.get("https://www.google.com")
        
        # Verificar que elementos principais estão visíveis
        search_box = chrome_driver.find_element(By.NAME, "q")
        assert search_box.is_displayed()
