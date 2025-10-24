# Exercício 04 - Page Object Model (POM) para Testes Web

## Arquitetura das Pages

### 1. **BasePage (base_page.py)**
Classe base com funcionalidades comuns:
- Inicialização do WebDriver
- Métodos genéricos (wait, click, type, etc.)
- Tratamento de exceções
- Utilidades de navegação

```python
class BasePage:
    def __init__(self, driver):
        self.driver = driver
    
    def wait_for_element(self, locator, timeout=10):
        # Implementação de espera
    
    def click(self, locator):
        # Click com tratamento de erros
    
    def type_text(self, locator, text):
        # Digitação com limpeza prévia
```

### 2. **GooglePage (google_page.py)**
Page Object específica para o Google:
- Localizadores dos elementos (search box, buttons, results)
- Métodos de ação (search, get_results, etc.)
- Validações específicas da página

```python
class GooglePage(BasePage):
    # Localizadores
    SEARCH_BOX = (By.NAME, "q")
    SEARCH_BUTTON = (By.NAME, "btnK")
    
    # Ações
    def search(self, term):
        # Implementa busca no Google
    
    def get_results_count(self):
        # Retorna número de resultados
```

## Cenários de Teste

### 1. **Testes de Busca no Google**
```python
def test_busca_simples(chrome_driver):
    google_page = GooglePage(chrome_driver)
    google_page.navigate()
    google_page.search("selenium python")
    
    assert google_page.has_results()
    assert "selenium" in google_page.get_page_title()
```

### 2. **Validações da Interface**
- Presença de elementos essenciais
- Funcionalidade da caixa de busca
- Exibição de resultados
- Links de navegação

### 3. **Testes de Fluxo**
- Navegação completa (busca → resultados → navegação)
- Múltiplas buscas em sequência
- Validação de state entre páginas
