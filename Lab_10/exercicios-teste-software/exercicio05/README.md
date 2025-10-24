# Exercício 05 - Testes Parametrizados Avançados

## Tipos de Testes Implementados

### 1. **Testes de Validação de API (37 testes)**
**Arquivo**: `test_validacoes_parametrizadas.py`

#### Validação de Email (8 cenários)
```python
@pytest.mark.parametrize("email,esperado", [
    ("user@example.com", True),      # Email válido básico
    ("test+tag@domain.co.uk", True), # Email com tag e domínio complexo
    ("invalid-email", False),         # Sem @ e domínio
    ("@domain.com", False),          # Sem parte local
    ("user@", False),                # Sem domínio
    ("", False),                     # String vazia
    ("spaces @domain.com", False),   # Espaços inválidos
    ("user@domain", False)           # Sem TLD
])
```

#### Validação de Senha (5 cenários)
```python
@pytest.mark.parametrize("senha,esperado", [
    ("MinhaSenh@123", True),         # Senha forte completa
    ("weakpass", False),             # Muito simples
    ("NoNumber!", False),            # Sem números
    ("nonumber123", False),          # Sem caracteres especiais
    ("", False)                      # Senha vazia
])
```

#### Testes de API REST (24 cenários adicionais)
- Criação de posts com diferentes payloads
- Validação de responses de APIs externas
- Tratamento de códigos de status HTTP
- Validação de schemas JSON

### 2. **Testes de Busca Web (18 testes)**
**Arquivo**: `test_busca_parametrizada.py`

#### 🔍 Busca Parametrizada no Google (5 termos + variações)
```python
@pytest.mark.parametrize("termo_busca", [
    "Python programming",            # Termo técnico
    "pytest tutorial",              # Tutorial específico
    "selenium automation",          # Ferramentas de automação
    "GitHub Copilot",              # Produto específico
    "machine learning"             # Área de conhecimento
])
```

#### Testes de Performance e Contexto (13 cenários adicionais)
- Validação de tempo de resposta
- Verificação de elementos da página
- Testes de responsividade
- Validação de encoding e caracteres especiais

### Pytest Parametrize Features
```python
# Parametrização simples
@pytest.mark.parametrize("input,expected", [(1, 2), (2, 3)])

# Parametrização múltipla
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [3, 4])  # Produto cartesiano: 4 testes

# Parametrização com IDs personalizados
@pytest.mark.parametrize("email,valid", [
    ("user@domain.com", True, id="email_valido"),
    ("invalid", False, id="email_invalido")
])

# Parametrização indireta (usando fixtures)
@pytest.mark.parametrize("api_client", ["json", "xml"], indirect=True)
```