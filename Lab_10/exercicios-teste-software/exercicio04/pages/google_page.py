"""
Page Object para a página do Google
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage


class GooglePage(BasePage):
    """Page Object da página do Google"""
    
    # Locators
    CAMPO_BUSCA = (By.NAME, "q")
    RESULTADOS = (By.ID, "search")
    PRIMEIRO_RESULTADO = (By.CSS_SELECTOR, "div.g")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.google.com"
    
    def abrir(self):
        """Abre a página do Google"""
        self.abrir_url(self.url)
    
    def buscar(self, termo):
        """Realiza uma busca"""
        campo = self.encontrar_elemento(self.CAMPO_BUSCA)
        campo.clear()
        campo.send_keys(termo)
        campo.send_keys(Keys.RETURN)
    
    def tem_resultados(self):
        """Verifica se há resultados de busca"""
        return self.elemento_visivel(self.RESULTADOS)
    
    def get_texto_resultados(self):
        """Obtém texto dos resultados"""
        if self.tem_resultados():
            return self.obter_texto(self.RESULTADOS)
        return ""
    
    def contar_resultados(self):
        """Conta número de resultados na primeira página"""
        if self.tem_resultados():
            return len(self.encontrar_elementos(self.PRIMEIRO_RESULTADO))
        return 0
