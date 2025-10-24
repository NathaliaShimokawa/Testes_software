"""
Testes automatizados para formulário de login
Site de teste: https://practicetestautomation.com/practice-test-login/
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class TestLogin:
    """Classe de testes para funcionalidade de login"""
    
    LOGIN_URL = "https://practicetestautomation.com/practice-test-login/"
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    SUBMIT_BUTTON = (By.ID, "submit")
    ERROR_MESSAGE = (By.ID, "error")
    SUCCESS_MESSAGE = "Logged In Successfully"
    LOGOUT_BUTTON = (By.LINK_TEXT, "Log out")
    
    # Credenciais válidas
    VALID_USERNAME = "student"
    VALID_PASSWORD = "Password123"
    
    def setup_method(self):
        """Executado antes de cada teste"""
        pass
    
    def teardown_method(self):
        """Executado após cada teste"""
        pass
    
    def test_login_sucesso(self, chrome_driver):
        """
        Teste: Login com credenciais válidas
        Cenário: Usuário insere username e password corretos
        Resultado esperado: Login realizado com sucesso
        """
        driver = chrome_driver
        wait = WebDriverWait(driver, 10)
        
        # Navegar para a página de login
        driver.get(self.LOGIN_URL)
        
        # Verificar se a página carregou corretamente
        assert "Test Login" in driver.title
        
        # Preencher formulário com credenciais válidas
        username_field = wait.until(EC.presence_of_element_located(self.USERNAME_FIELD))
        password_field = driver.find_element(*self.PASSWORD_FIELD)
        submit_button = driver.find_element(*self.SUBMIT_BUTTON)
        
        username_field.clear()
        username_field.send_keys(self.VALID_USERNAME)
        
        password_field.clear()
        password_field.send_keys(self.VALID_PASSWORD)
        
        # Clicar no botão de submit
        submit_button.click()
        
        # Verificar sucesso do login
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert self.SUCCESS_MESSAGE in driver.page_source
        
        # Verificar se o botão de logout está presente
        logout_button = wait.until(EC.presence_of_element_located(self.LOGOUT_BUTTON))
        assert logout_button.is_displayed()
    
    def test_login_username_invalido(self, chrome_driver):
        """
        Teste: Login com username inválido
        Cenário: Usuário insere username incorreto com password correto
        Resultado esperado: Mensagem de erro exibida
        """
        driver = chrome_driver
        wait = WebDriverWait(driver, 10)
        
        # Navegar para a página de login
        driver.get(self.LOGIN_URL)
        
        # Preencher formulário com username inválido
        username_field = wait.until(EC.presence_of_element_located(self.USERNAME_FIELD))
        password_field = driver.find_element(*self.PASSWORD_FIELD)
        submit_button = driver.find_element(*self.SUBMIT_BUTTON)
        
        username_field.clear()
        username_field.send_keys("usuario_invalido")
        
        password_field.clear()
        password_field.send_keys(self.VALID_PASSWORD)
        
        # Clicar no botão de submit
        submit_button.click()
        
        # Verificar mensagem de erro
        error_element = wait.until(EC.presence_of_element_located(self.ERROR_MESSAGE))
        assert error_element.is_displayed()
        error_text = error_element.text
        assert "Your username is invalid!" in error_text
    
    def test_login_senha_incorreta(self, chrome_driver):
        """
        Teste: Login com senha incorreta
        Cenário: Usuário insere username correto com password incorreto
        Resultado esperado: Mensagem de erro exibida
        """
        driver = chrome_driver
        wait = WebDriverWait(driver, 10)
        
        # Navegar para a página de login
        driver.get(self.LOGIN_URL)
        
        # Preencher formulário com senha incorreta
        username_field = wait.until(EC.presence_of_element_located(self.USERNAME_FIELD))
        password_field = driver.find_element(*self.PASSWORD_FIELD)
        submit_button = driver.find_element(*self.SUBMIT_BUTTON)
        
        username_field.clear()
        username_field.send_keys(self.VALID_USERNAME)
        
        password_field.clear()
        password_field.send_keys("senha_incorreta")
        
        # Clicar no botão de submit
        submit_button.click()
        
        # Verificar mensagem de erro
        error_element = wait.until(EC.presence_of_element_located(self.ERROR_MESSAGE))
        assert error_element.is_displayed()
        error_text = error_element.text
        assert "Your password is invalid!" in error_text
    
    def test_login_campos_vazios(self, chrome_driver):
        """
        Teste: Tentativa de login sem preencher campos
        Cenário: Usuário clica em submit sem preencher username e password
        Resultado esperado: Mensagem de erro exibida
        """
        driver = chrome_driver
        wait = WebDriverWait(driver, 10)
        
        # Navegar para a página de login
        driver.get(self.LOGIN_URL)
        
        # Garantir que os campos estão vazios e clicar em submit
        username_field = wait.until(EC.presence_of_element_located(self.USERNAME_FIELD))
        password_field = driver.find_element(*self.PASSWORD_FIELD)
        submit_button = driver.find_element(*self.SUBMIT_BUTTON)
        
        username_field.clear()
        password_field.clear()
        
        # Clicar no botão de submit
        submit_button.click()
        
        # Verificar mensagem de erro
        error_element = wait.until(EC.presence_of_element_located(self.ERROR_MESSAGE))
        assert error_element.is_displayed()
        error_text = error_element.text
        assert "Your username is invalid!" in error_text
    
    def test_login_apenas_username(self, chrome_driver):
        """
        Teste: Login apenas com username preenchido
        Cenário: Usuário preenche apenas o campo username
        Resultado esperado: Mensagem de erro exibida
        """
        driver = chrome_driver
        wait = WebDriverWait(driver, 10)
        
        # Navegar para a página de login
        driver.get(self.LOGIN_URL)
        
        # Preencher apenas o username
        username_field = wait.until(EC.presence_of_element_located(self.USERNAME_FIELD))
        password_field = driver.find_element(*self.PASSWORD_FIELD)
        submit_button = driver.find_element(*self.SUBMIT_BUTTON)
        
        username_field.clear()
        username_field.send_keys(self.VALID_USERNAME)
        
        password_field.clear()  # Garantir que está vazio
        
        # Clicar no botão de submit
        submit_button.click()
        
        # Verificar mensagem de erro
        error_element = wait.until(EC.presence_of_element_located(self.ERROR_MESSAGE))
        assert error_element.is_displayed()
        error_text = error_element.text
        assert "Your password is invalid!" in error_text
    
    def test_login_apenas_password(self, chrome_driver):
        """
        Teste: Login apenas com password preenchido
        Cenário: Usuário preenche apenas o campo password
        Resultado esperado: Mensagem de erro exibida
        """
        driver = chrome_driver
        wait = WebDriverWait(driver, 10)
        
        # Navegar para a página de login
        driver.get(self.LOGIN_URL)
        
        # Preencher apenas o password
        username_field = wait.until(EC.presence_of_element_located(self.USERNAME_FIELD))
        password_field = driver.find_element(*self.PASSWORD_FIELD)
        submit_button = driver.find_element(*self.SUBMIT_BUTTON)
        
        username_field.clear()  # Garantir que está vazio
        
        password_field.clear()
        password_field.send_keys(self.VALID_PASSWORD)
        
        # Clicar no botão de submit
        submit_button.click()
        
        # Verificar mensagem de erro
        error_element = wait.until(EC.presence_of_element_located(self.ERROR_MESSAGE))
        assert error_element.is_displayed()
        error_text = error_element.text
        assert "Your username is invalid!" in error_text
    
    def test_verificar_elementos_da_pagina(self, chrome_driver):
        """
        Teste: Verificar se todos os elementos necessários estão presentes na página
        Cenário: Carregar página de login
        Resultado esperado: Todos os elementos do formulário estão presentes
        """
        driver = chrome_driver
        wait = WebDriverWait(driver, 10)
        
        # Navegar para a página de login
        driver.get(self.LOGIN_URL)
        
        # Verificar presença dos elementos
        username_field = wait.until(EC.presence_of_element_located(self.USERNAME_FIELD))
        password_field = driver.find_element(*self.PASSWORD_FIELD)
        submit_button = driver.find_element(*self.SUBMIT_BUTTON)
        
        # Verificar se os elementos estão visíveis e habilitados
        assert username_field.is_displayed()
        assert username_field.is_enabled()
        
        assert password_field.is_displayed()
        assert password_field.is_enabled()
        
        assert submit_button.is_displayed()
        assert submit_button.is_enabled()
        
        # Verificar placeholders ou labels se existirem
        assert username_field.get_attribute("placeholder") or username_field.get_attribute("name")
        assert password_field.get_attribute("type") == "password"
    
    @pytest.mark.parametrize("username,password,expected_error", [
        ("", "", "Your username is invalid!"),
        ("student", "", "Your password is invalid!"),
        ("", "Password123", "Your username is invalid!"),
        ("invalid_user", "Password123", "Your username is invalid!"),
        ("student", "wrong_password", "Your password is invalid!"),
        ("STUDENT", "Password123", "Your username is invalid!"),  # Case sensitive
        ("student", "password123", "Your password is invalid!"),  # Case sensitive
    ])
    def test_login_cenarios_invalidos(self, chrome_driver, username, password, expected_error):
        """
        Teste parametrizado: Diferentes cenários de login inválido
        Cenário: Testar vários casos de entrada inválida
        Resultado esperado: Mensagens de erro apropriadas para cada caso
        """
        driver = chrome_driver
        wait = WebDriverWait(driver, 10)
        
        # Navegar para a página de login
        driver.get(self.LOGIN_URL)
        
        # Preencher formulário
        username_field = wait.until(EC.presence_of_element_located(self.USERNAME_FIELD))
        password_field = driver.find_element(*self.PASSWORD_FIELD)
        submit_button = driver.find_element(*self.SUBMIT_BUTTON)
        
        username_field.clear()
        if username:
            username_field.send_keys(username)
        
        password_field.clear()
        if password:
            password_field.send_keys(password)
        
        # Clicar no botão de submit
        submit_button.click()
        
        # Verificar mensagem de erro esperada
        error_element = wait.until(EC.presence_of_element_located(self.ERROR_MESSAGE))
        assert error_element.is_displayed()
        error_text = error_element.text
        assert expected_error in error_text