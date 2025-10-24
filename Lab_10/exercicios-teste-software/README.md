# Exercícios de Teste de Software 

---

## **Estrutura do Projeto**

```
exercicios-teste-software/
├── README.md                   
├── requirements.txt            
├── pytest.ini                 
├── exercicio01/                # Testes Selenium - Login Form
│   ├── README.md
│   └── tests/
│       ├── test_login.py
│       ├── conftest.py
│       └── relatorio_execucao.html
├── exercicio02/                # Testes REST API - Products
│   ├── README.md
│   └── tests/
│       ├── test_products_api.py
│       └── relatorio_execucao.html
├── exercicio03/                # Testes CRUD - JSONPlaceholder
│   ├── README.md
│   └── tests/
│       ├── test_todos_crud.py
│       └── relatorio_execucao.html
├── exercicio04/                # Page Object Model  
│   ├── README.md
│   ├── tests/
│   │   ├── test_login_pom.py
│   │   └── relatorio_execucao.html
│   └── pages/
│       ├──  base_page.py
│       ├──  login_page.py
│       └──  dashboard_page.py
└── exercicio05/                # Testes Parametrizados
    ├── README.md
    └── tests/
        ├── test_validacoes_parametrizadas.py
        ├── test_busca_parametrizada.py
        └── relatorio_execucao.html
```

---

## **Como Executar**

### **Execução Individual**
```bash
# Exercício 1 - Testes de Login
cd exercicio01
pytest tests/ -v --html=tests/relatorio_execucao.html

# Exercício 2 - API REST  
cd exercicio02
pytest tests/ -v --html=tests/relatorio_execucao.html

# Exercício 3 - CRUD
cd exercicio03
pytest tests/ -v --html=tests/relatorio_execucao.html

# Exercício 4 - Page Object Model
cd exercicio04
pytest tests/ -v --html=tests/relatorio_execucao.html

# Exercício 5 - Testes Parametrizados
cd exercicio05
pytest tests/ -v --html=tests/relatorio_execucao.html
```

### **Execução Global**
```bash
# Todos os exercícios
pytest -v --html=relatorio_geral.html

# Por marcador
pytest -m "login" -v        # Apenas testes de login
pytest -m "api" -v          # Apenas testes de API
pytest -m "parametrize" -v  # Apenas testes parametrizados
```
