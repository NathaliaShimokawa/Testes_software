"""
Classe base para Page Objects - Page Object Model (POM)
Contém métodos comuns que serão herdados por todas as páginas
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


class BasePage:
    """Classe base com métodos comuns para todas as páginas"""
    
    def __init__(self, driver, timeout=10):
        """
        Inicializa a página base
        
        Args:
            driver: Instância do WebDriver
            timeout: Tempo limite padrão para esperas (default: 10s)
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def abrir_url(self, url):
        """Abre uma URL"""
        self.driver.get(url)
    
    def encontrar_elemento(self, locator):
        """Encontra um elemento na página"""
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def encontrar_elementos(self, locator):
        """Encontra múltiplos elementos na página"""
        return self.wait.until(EC.presence_of_all_elements_located(locator))
    
    def clicar(self, locator):
        """Clica em um elemento"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def digitar(self, locator, texto):
        """Digita texto em um campo"""
        element = self.encontrar_elemento(locator)
        element.clear()
        element.send_keys(texto)
    
    def obter_texto(self, locator):
        """Obtém texto de um elemento"""
        element = self.encontrar_elemento(locator)
        return element.text
    
    def elemento_visivel(self, locator):
        """Verifica se elemento está visível"""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def elemento_presente(self, locator):
        """
        Verifica se um elemento está presente na página (pode não estar visível)
        
        Args:
            locator: Tupla (By.TYPE, "value") do elemento
            
        Returns:
            bool: True se elemento está presente, False caso contrário
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def obter_atributo(self, locator, atributo):
        """
        Obtém o valor de um atributo de um elemento
        
        Args:
            locator: Tupla (By.TYPE, "value") do elemento
            atributo: Nome do atributo
            
        Returns:
            str: Valor do atributo
        """
        element = self.encontrar_elemento(locator)
        return element.get_attribute(atributo)
    
    def aguardar_texto_presente(self, locator, texto):
        """
        Aguarda até que um texto específico esteja presente em um elemento
        
        Args:
            locator: Tupla (By.TYPE, "value") do elemento
            texto: Texto a ser aguardado
            
        Returns:
            bool: True se texto foi encontrado
        """
        return self.wait.until(EC.text_to_be_present_in_element(locator, texto))
    
    def aguardar_url_conter(self, texto):
        """
        Aguarda até que a URL contenha um texto específico
        
        Args:
            texto: Texto que deve estar presente na URL
            
        Returns:
            bool: True se URL contém o texto
        """
        return self.wait.until(EC.url_contains(texto))
    
    def obter_titulo_pagina(self):
        """Obtém o título da página atual"""
        return self.driver.title
    
    def obter_url_atual(self):
        """Obtém a URL atual da página"""
        return self.driver.current_url
    
    def aguardar_pagina_carregar(self, timeout=30):
        """
        Aguarda a página carregar completamente
        
        Args:
            timeout: Tempo limite para carregamento
        """
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
