"""
Exercício 5 - Testes Parametrizados: Validações REST API
=========================================================

Este módulo implementa testes parametrizados para validar múltiplos cenários de entrada 
através de APIs públicas, focando em:

Parte A: Validação de Dados de Usuário (JSONPlaceholder)
Parte B: Validação de Posts e Comentários (JSONPlaceholder)

Sites de teste: 
- https://jsonplaceholder.typicode.com/ (CRUD operations)
- https://httpbin.org/ (HTTP testing)
"""

import pytest
import requests
import time
import re
from typing import List, Tuple


class TestValidacoesParametrizadas:
    """
    Classe de testes para validações parametrizadas usando REST API
    
    Testa diferentes cenários de entrada inválida e válida usando APIs públicas
    que simulam comportamentos de validação reais.
    """
    
    # Base URLs para os testes de API
    JSONPLACEHOLDER_URL = "https://jsonplaceholder.typicode.com"
    HTTPBIN_URL = "https://httpbin.org"
    
    # ===============================
    # PARTE A: VALIDAÇÃO DE EMAILS
    # ===============================
    
    # Lista de emails inválidos conforme especificação
    emails_invalidos = [
        "sem-arroba.com",              # Sem símbolo @
        "@sem-usuario.com",            # Sem parte local (usuário)
        "sem-dominio@",                # Sem domínio
        "espacos no meio@teste.com",   # Espaços no meio
        "caracteres!especiais@teste.com", # Caracteres especiais não permitidos
        "..pontos@teste.com",          # Pontos consecutivos
        "teste@",                      # Só @ sem domínio
        "@teste.com"                   # Só @ sem usuário
    ]
    
    @pytest.mark.parametrize("email_invalido", emails_invalidos)
    def test_validacao_email_formato(self, email_invalido):
        """
        Teste parametrizado: Validação local de formatos de email inválidos
        
        Cenário: Usar regex para validar formatos de email
        Resultado esperado: Emails malformados devem falhar na validação
        
        Args:
            email_invalido (str): Email malformado para testar
        """
        # Arrange - Pattern regex para email válido (mais rigoroso)
        # Não permite pontos consecutivos, espaços, ou caracteres especiais problemáticos
        email_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._-]*[a-zA-Z0-9]@[a-zA-Z0-9][a-zA-Z0-9.-]*[a-zA-Z0-9]\.[a-zA-Z]{2,}$'
        
        # Act - Testar email com regex
        is_valid = re.match(email_pattern, email_invalido) is not None
        
        # Assert - Email inválido não deve passar no regex
        assert not is_valid, (
            f"Email '{email_invalido}' deveria ser inválido pela regex, "
            f"mas passou na validação"
        )
        
        print(f"Email inválido rejeitado pela regex: {email_invalido}")
    
    @pytest.mark.parametrize("email_invalido", emails_invalidos)
    def test_validacao_email_via_httpbin(self, email_invalido):
        """
        Teste parametrizado: Enviar emails inválidos para httpbin e validar estrutura
        
        Cenário: Usar httpbin.org para simular validação de payload
        Resultado esperado: Conseguir enviar e validar estrutura da resposta
        
        Args:
            email_invalido (str): Email malformado para testar
        """
        # Arrange - Preparar dados de requisição para httpbin
        payload = {
            "email": email_invalido,
            "action": "register"
        }
        
        # Act - Enviar para httpbin que ecoa a requisição
        response = requests.post(f"{self.HTTPBIN_URL}/post", json=payload)
        
        # Assert - Httpbin deve sempre retornar 200 e ecoar os dados
        assert response.status_code == 200, (
            f"Httpbin deveria retornar 200, mas retornou {response.status_code}"
        )
        
        # Verificar estrutura da resposta
        response_data = response.json()
        assert "json" in response_data, "Resposta deveria conter campo 'json'"
        assert response_data["json"]["email"] == email_invalido, (
            f"Email na resposta deveria ser '{email_invalido}'"
        )
        
        print(f"Email inválido processado via httpbin: {email_invalido}")
    
    def test_emails_validos_para_comparacao(self):
        """
        Teste de controle: Verificar que emails válidos passam na validação
        
        Este teste garante que nossa validação funciona corretamente com emails válidos.
        """
        # Arrange - Lista de emails válidos
        emails_validos = [
            "usuario@teste.com",
            "test.email@exemplo.org", 
            "valido123@dominio.com.br",
            "nome+sobrenome@teste.co.uk"
        ]
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # Act & Assert - Todos os emails válidos devem passar
        for email_valido in emails_validos:
            is_valid = re.match(email_pattern, email_valido) is not None
            assert is_valid, f"Email válido '{email_valido}' deveria passar na validação"
        
        print(f"{len(emails_validos)} emails válidos passaram na validação")
    
    # ===============================
    # PARTE B: VALIDAÇÃO DE SENHAS
    # ===============================
    
    # Lista de senhas inválidas com motivos específicos
    senhas_invalidas = [
        ("123", "muito curta"),          # Menos de 6 caracteres
        ("semNumero", "sem número"),     # Sem dígitos
        ("semmaiuscula123", "sem maiúscula"),  # Sem letras maiúsculas
        ("12345678", "só números"),      # Apenas números
        ("ab", "muito curta")            # Extremamente curta
    ]
    
    @pytest.mark.parametrize("senha,motivo", senhas_invalidas)
    def test_validacao_senha_criterios(self, senha, motivo):
        """
        Teste parametrizado: Validação de critérios de senha
        
        Cenário: Validar senhas usando critérios de segurança
        Resultado esperado: Senhas que não atendem critérios devem ser rejeitadas
        
        Args:
            senha (str): Senha inválida para testar
            motivo (str): Razão pela qual a senha é inválida
        """
        # Arrange - Definir critérios de validação de senha
        def validar_senha(password):
            """Valida senha usando critérios de segurança"""
            if len(password) < 6:
                return False, "muito curta"
            # Verificar "só números" antes das outras validações
            if password.isdigit():
                return False, "só números"
            if not re.search(r'\d', password):
                return False, "sem número"
            if not re.search(r'[A-Z]', password):
                return False, "sem maiúscula"
            return True, "válida"
        
        # Act - Validar senha
        is_valid, motivo_detectado = validar_senha(senha)
        
        # Assert - Senha deve ser inválida pelo motivo esperado
        assert not is_valid, (
            f"Senha '{senha}' deveria ser inválida, mas foi considerada válida"
        )
        
        # Verificar se o motivo está correto (flexível para diferentes critérios)
        assert motivo in motivo_detectado or motivo_detectado in motivo, (
            f"Motivo esperado '{motivo}' não corresponde ao detectado '{motivo_detectado}'"
        )
        
        print(f"Senha inválida rejeitada: '{senha}' (motivo: {motivo_detectado})")
    
    @pytest.mark.parametrize("senha,motivo", senhas_invalidas)
    def test_validacao_senha_via_jsonplaceholder(self, senha, motivo):
        """
        Teste parametrizado: Enviar senhas para JSONPlaceholder simulando validação
        
        Cenário: Usar JSONPlaceholder para simular criação de usuário com senha
        Resultado esperado: Validar estrutura e processamento da requisição
        
        Args:
            senha (str): Senha para testar
            motivo (str): Razão da invalidade
        """
        # Arrange - Criar payload para usuário com senha
        payload = {
            "name": "Test User",
            "username": "testuser",
            "email": "test@test.com",
            "password": senha,
            "password_strength": motivo
        }
        
        # Act - Enviar para JSONPlaceholder (sempre aceita)
        response = requests.post(f"{self.JSONPLACEHOLDER_URL}/users", json=payload)
        
        # Assert - JSONPlaceholder sempre aceita, mas podemos validar estrutura
        assert response.status_code == 201, (
            f"JSONPlaceholder deveria aceitar POST, mas retornou {response.status_code}"
        )
        
        # Verificar que os dados foram ecoados
        response_data = response.json()
        assert "id" in response_data, "Resposta deveria conter ID gerado"
        assert response_data.get("password") == senha, (
            f"Senha na resposta deveria ser '{senha}'"
        )
        
        print(f"Senha processada via JSONPlaceholder: '{senha}' (motivo: {motivo})")
    
    def test_senhas_validas_para_comparacao(self):
        """
        Teste de controle: Verificar que senhas válidas passam na validação
        
        Garante que nossa validação funciona corretamente com senhas seguras.
        """
        # Arrange - Lista de senhas válidas
        senhas_validas = [
            "MinhaSenh@123",
            "Password123!",
            "Segura456",
            "ValidPass789"
        ]
        
        def validar_senha(password):
            """Valida senha usando critérios de segurança"""
            if len(password) < 6:
                return False, "muito curta"
            # Verificar "só números" antes das outras validações
            if password.isdigit():
                return False, "só números"
            if not re.search(r'\d', password):
                return False, "sem número"
            if not re.search(r'[A-Z]', password):
                return False, "sem maiúscula"
            return True, "válida"
        
        # Act & Assert - Todas as senhas válidas devem passar
        for senha_valida in senhas_validas:
            is_valid, motivo = validar_senha(senha_valida)
            assert is_valid, f"Senha válida '{senha_valida}' deveria passar na validação: {motivo}"
        
        print(f"{len(senhas_validas)} senhas válidas passaram na validação")
    
    # ===============================
    # TESTES COMBINADOS
    # ===============================
    
    @pytest.mark.parametrize("email,senha", [
        ("invalid@", "123"),                    # Email e senha inválidos
        ("sem-arroba.com", "semNumero"),        # Ambos inválidos por motivos diferentes
        ("@teste.com", "ab"),                   # Casos extremos
    ])
    def test_validacao_combinada_email_senha_invalidos(self, email, senha):
        """
        Teste parametrizado: Combinações de email e senha inválidos
        
        Cenário: Testar casos onde tanto email quanto senha são inválidos
        Resultado esperado: Ambas validações devem falhar
        """
        # Arrange - Patterns de validação
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        def validar_senha(password):
            if len(password) < 6:
                return False, "muito curta"
            if not re.search(r'\d', password):
                return False, "sem número"
            if not re.search(r'[A-Z]', password):
                return False, "sem maiúscula"
            return True, "válida"
        
        # Act - Validar email e senha
        email_valido = re.match(email_pattern, email) is not None
        senha_valida, motivo_senha = validar_senha(senha)
        
        # Assert - Ambos devem ser inválidos
        assert not email_valido, f"Email '{email}' deveria ser inválido"
        assert not senha_valida, f"Senha '{senha}' deveria ser inválida: {motivo_senha}"
        
        print(f"Combinação inválida rejeitada: {email} + {senha}")
    
    # ===============================
    # TESTES DE PERFORMANCE
    # ===============================
    
    @pytest.mark.parametrize("email_invalido", emails_invalidos[:3])  # Subset para performance
    def test_tempo_resposta_validacao_email(self, email_invalido):
        """
        Teste de performance: Tempo de resposta da validação de email
        
        Verifica se a validação responde dentro de um tempo aceitável.
        """
        # Arrange - Preparar pattern de validação
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # Act - Medir tempo de validação
        start_time = time.time()
        is_valid = re.match(email_pattern, email_invalido) is not None
        validation_time = time.time() - start_time
        
        # Assert - Verificar tempo de resposta (validação local deve ser muito rápida)
        assert validation_time < 0.1, (
            f"Validação demorou {validation_time:.4f}s para email inválido. "
            "Deveria ser menor que 0.1s."
        )
        
        # Verificar que ainda rejeita corretamente
        assert not is_valid, f"Email '{email_invalido}' deveria ser inválido"
        
        print(f"Validação rápida ({validation_time:.4f}s): {email_invalido}")
    
    @pytest.mark.parametrize("user_data", [
        {"name": "João Silva", "email": "joao@teste.com", "website": "joao.com.br"},
        {"name": "Maria Santos", "email": "maria@exemplo.org", "website": "maria.net"},
        {"name": "Pedro Costa", "email": "pedro@site.com", "website": "pedro.io"}
    ])
    def test_criacao_usuarios_jsonplaceholder(self, user_data):
        """
        Teste parametrizado: Criação de usuários via JSONPlaceholder
        
        Cenário: Testar criação de diferentes usuários
        Resultado esperado: Todos devem ser criados com sucesso
        """
        # Arrange - Dados já preparados no parâmetro
        
        # Act - Criar usuário via JSONPlaceholder
        start_time = time.time()
        response = requests.post(f"{self.JSONPLACEHOLDER_URL}/users", json=user_data)
        response_time = time.time() - start_time
        
        # Assert - Verificar criação bem-sucedida
        assert response.status_code == 201, (
            f"Criação de usuário deveria retornar 201, mas retornou {response.status_code}"
        )
        
        # Verificar estrutura da resposta
        response_data = response.json()
        assert "id" in response_data, "Resposta deveria conter ID gerado"
        assert response_data["name"] == user_data["name"], (
            f"Nome na resposta deveria ser '{user_data['name']}'"
        )
        
        # Verificar performance
        assert response_time < 5.0, (
            f"Criação demorou {response_time:.2f}s, deveria ser < 5s"
        )
        
        print(f"Usuário criado em {response_time:.2f}s: {user_data['name']}")


# ===============================
# FIXTURES AUXILIARES
# ===============================

@pytest.fixture(scope="session")
def api_session():
    """
    Fixture: Sessão HTTP reutilizável para os testes de API
    
    Cria uma sessão requests que pode ser reutilizada entre testes,
    melhorando a performance ao reusar conexões TCP.
    """
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json"
    })
    
    yield session
    
    session.close()


@pytest.fixture(autouse=True)
def delay_between_tests():
    """
    Fixture: Delay automático entre testes para evitar rate limiting
    
    Adiciona uma pequena pausa entre os testes para evitar que a API
    do reqres.in bloqueie requisições por excesso de chamadas.
    """
    yield
    time.sleep(0.1)  # 100ms entre testes