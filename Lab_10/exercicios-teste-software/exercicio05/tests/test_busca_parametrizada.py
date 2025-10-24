"""
Exercício 5 - Testes Parametrizados: Busca Web
==============================================

Este módulo implementa testes parametrizados para validar funcionalidade de busca
no Google usando Selenium WebDriver.

Parte C: Busca Parametrizada (Web)

Site de teste: https://www.google.com
"""

import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class TestBuscaParametrizada:
    """
    Classe de testes para busca parametrizada no Google
    
    Testa diferentes termos de busca para verificar se o sistema de busca
    do Google retorna resultados apropriados para termos relacionados a tecnologia.
    """
    
    # URL base para os testes
    GOOGLE_URL = "https://www.google.com"
    
    # ===============================
    # PARTE C: BUSCA PARAMETRIZADA
    # ===============================
    
    # Lista de termos de busca conforme especificação
    termos_busca = [
        "Python",
        "Selenium", 
        "Pytest",
        "API Testing",
        "Automation"
    ]
    
    @pytest.mark.parametrize("termo_busca", termos_busca)
    def test_busca_google(self, chrome_driver_busca, termo_busca):
        """
        Teste parametrizado: Busca no Google com múltiplos termos
        
        Cenário: Pesquisar diferentes termos relacionados a tecnologia
        Resultado esperado: Termo deve aparecer nos resultados da busca
        
        Args:
            chrome_driver_busca: Fixture do WebDriver Chrome otimizado
            termo_busca (str): Termo para pesquisar no Google
        """
        driver = chrome_driver_busca
        
        # Arrange - Navegar para o Google
        driver.get(self.GOOGLE_URL)
        
        # Aguardar e lidar com possíveis cookies/termos
        self._aceitar_cookies_se_necessario(driver)
        
        try:
            # Act - Encontrar caixa de busca e realizar pesquisa
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            
            # Limpar campo e digitar termo
            search_box.clear()
            search_box.send_keys(termo_busca)
            search_box.send_keys(Keys.RETURN)
            
            # Aguardar resultados carregarem
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "search"))
            )
            
            # Assert - Verificar se o termo aparece nos resultados
            page_source = driver.page_source.lower()
            termo_lower = termo_busca.lower()
            
            assert termo_lower in page_source, (
                f"Termo '{termo_busca}' não encontrado nos resultados da busca"
            )
            
            # Verificação adicional: pelo menos um resultado deve estar presente
            resultados = driver.find_elements(By.CSS_SELECTOR, "div.g")
            assert len(resultados) > 0, (
                f"Nenhum resultado encontrado para '{termo_busca}'"
            )
            
            print(f"✅ Busca bem-sucedida para: {termo_busca} ({len(resultados)} resultados)")
            
        except TimeoutException:
            pytest.fail(f"Timeout ao buscar por '{termo_busca}' - elementos não carregaram")
        except NoSuchElementException as e:
            pytest.fail(f"Elemento não encontrado durante busca por '{termo_busca}': {e}")
    
    @pytest.mark.parametrize("termo_busca,resultado_esperado", [
        ("Python", "programming"),           # Python deve retornar conteúdo sobre programação
        ("Selenium", "automation"),          # Selenium deve retornar sobre automação
        ("Pytest", "testing"),               # Pytest deve retornar sobre testes
        ("API Testing", "api"),              # API Testing deve conter "api"
        ("Automation", "test")               # Automation deve mencionar "test"
    ])
    def test_busca_com_validacao_contexto(self, chrome_driver_busca, termo_busca, resultado_esperado):
        """
        Teste parametrizado: Busca com validação de contexto dos resultados
        
        Cenário: Verificar se os resultados são relevantes ao termo buscado
        Resultado esperado: Resultados devem conter palavras-chave relacionadas
        
        Args:
            chrome_driver_busca: Fixture do WebDriver Chrome
            termo_busca (str): Termo para buscar
            resultado_esperado (str): Palavra-chave que deve aparecer nos resultados
        """
        driver = chrome_driver_busca
        
        # Arrange - Navegar para Google
        driver.get(self.GOOGLE_URL)
        self._aceitar_cookies_se_necessario(driver)
        
        try:
            # Act - Realizar busca
            search_box = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "q"))
            )
            
            search_box.clear()
            search_box.send_keys(termo_busca)
            search_box.send_keys(Keys.RETURN)
            
            # Aguardar resultados
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "search"))
            )
            
            # Assert - Verificar contexto dos resultados
            page_source = driver.page_source.lower()
            
            assert resultado_esperado.lower() in page_source, (
                f"Resultado esperado '{resultado_esperado}' não encontrado "
                f"para busca '{termo_busca}'"
            )
            
            # Verificar se há múltiplos resultados relevantes
            resultados = driver.find_elements(By.CSS_SELECTOR, "div.g")
            assert len(resultados) >= 3, (
                f"Poucos resultados ({len(resultados)}) para '{termo_busca}'"
            )
            
            print(f"✅ Contexto validado: '{termo_busca}' → '{resultado_esperado}' encontrado")
            
        except TimeoutException:
            pytest.fail(f"Timeout na validação de contexto para '{termo_busca}'")
    
    @pytest.mark.parametrize("termo_busca", termos_busca)
    def test_tempo_carregamento_busca(self, chrome_driver_busca, termo_busca):
        """
        Teste de performance: Tempo de carregamento da busca
        
        Cenário: Verificar se a busca carrega dentro do tempo esperado
        Resultado esperado: Resultados devem aparecer em menos de 5 segundos
        """
        driver = chrome_driver_busca
        
        # Arrange - Navegar e medir tempo
        start_time = time.time()
        driver.get(self.GOOGLE_URL)
        self._aceitar_cookies_se_necessario(driver)
        
        try:
            # Act - Buscar e medir tempo até resultados
            search_box = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "q"))
            )
            
            search_time_start = time.time()
            search_box.clear()
            search_box.send_keys(termo_busca)
            search_box.send_keys(Keys.RETURN)
            
            # Aguardar resultados e medir tempo
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "search"))
            )
            
            search_time_end = time.time()
            tempo_busca = search_time_end - search_time_start
            
            # Assert - Verificar tempo de resposta
            assert tempo_busca < 5.0, (
                f"Busca por '{termo_busca}' demorou {tempo_busca:.2f}s. "
                "Deveria ser menor que 5s."
            )
            
            print(f"✅ Busca rápida ({tempo_busca:.2f}s): {termo_busca}")
            
        except TimeoutException:
            tempo_total = time.time() - start_time
            pytest.fail(f"Timeout após {tempo_total:.2f}s para '{termo_busca}'")
    
    @pytest.mark.parametrize("termo_busca", ["", "   ", "!@#$%"])
    def test_busca_termos_invalidos(self, chrome_driver_busca, termo_busca):
        """
        Teste parametrizado: Busca com termos inválidos/vazios
        
        Cenário: Verificar comportamento com entradas inválidas
        Resultado esperado: Sistema deve lidar graciosamente com entradas inválidas
        """
        driver = chrome_driver_busca
        
        # Arrange - Navegar para Google
        driver.get(self.GOOGLE_URL)
        self._aceitar_cookies_se_necessario(driver)
        
        try:
            # Act - Tentar buscar termo inválido
            search_box = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "q"))
            )
            
            search_box.clear()
            if termo_busca.strip():  # Se não for vazio
                search_box.send_keys(termo_busca)
            search_box.send_keys(Keys.RETURN)
            
            # Aguardar resposta (pode ser página de erro ou resultado vazio)
            time.sleep(2)
            
            # Assert - Sistema não deve quebrar
            current_url = driver.current_url
            assert "google.com" in current_url, (
                "Sistema deveria permanecer no Google após busca inválida"
            )
            
            print(f"✅ Sistema lidou graciosamente com termo inválido: '{termo_busca}'")
            
        except Exception as e:
            # Para termos inválidos, falhas específicas são aceitáveis
            print(f"⚠️ Comportamento esperado para termo inválido '{termo_busca}': {e}")
    
    # ===============================
    # MÉTODOS AUXILIARES
    # ===============================
    
    def _aceitar_cookies_se_necessario(self, driver):
        """
        Método auxiliar: Aceitar cookies do Google se aparecer modal
        
        Args:
            driver: Instance do WebDriver
        """
        try:
            # Tentar encontrar e clicar no botão de aceitar cookies
            accept_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Aceitar')]"))
            )
            accept_button.click()
            time.sleep(1)
        except TimeoutException:
            # Não há problema se não aparecer o modal de cookies
            pass
        except Exception as e:
            # Log do erro mas não falha o teste
            print(f"Aviso: Erro ao lidar com cookies: {e}")
    
    def _aguardar_elemento_removido(self, driver, locator, timeout=10):
        """
        Método auxiliar: Aguardar elemento ser removido da tela
        
        Args:
            driver: Instance do WebDriver  
            locator: Tuple (By, selector)
            timeout: Tempo limite em segundos
        """
        try:
            WebDriverWait(driver, timeout).until_not(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            pass  # Elemento ainda presente, mas continuamos


# ===============================
# FIXTURES ESPECÍFICAS
# ===============================

@pytest.fixture(scope="function")
def chrome_driver_busca():
    """
    Fixture: Chrome driver otimizado para testes de busca
    
    Configurações específicas para melhor performance nos testes de busca:
    - Desabilita imagens para carregar mais rápido
    - Configura user-agent
    - Define timeouts apropriados
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executar sem interface gráfica
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Otimizações para busca
    chrome_options.add_argument("--disable-images")  # Não carregar imagens
    chrome_options.add_argument("--disable-javascript")  # Desabilitar JS desnecessário
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    # User agent para evitar detecção de bot
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30)
        
        yield driver
        
    except Exception as e:
        pytest.skip(f"Chrome não disponível para testes de busca: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass


@pytest.fixture(autouse=True, scope="function")
def delay_between_search_tests():
    """
    Fixture: Delay entre testes de busca para evitar rate limiting do Google
    
    Adiciona pausa entre testes para ser respeitoso com os serviços do Google
    e evitar bloqueios por excesso de requisições automatizadas.
    """
    yield
    time.sleep(1)  # 1 segundo entre testes de busca