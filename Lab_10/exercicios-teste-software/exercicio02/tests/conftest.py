"""
Configurações globais para testes de API REST
"""
import pytest
import requests


@pytest.fixture(scope="session")
def api_session():
    """
    Fixture: Sessão HTTP reutilizável para testes de API
    
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
def delay_between_api_tests():
    """
    Fixture: Delay automático entre testes de API para evitar rate limiting
    
    Adiciona uma pequena pausa entre os testes para evitar que APIs
    externas bloqueiem requisições por excesso de chamadas.
    """
    import time
    yield
    time.sleep(0.1)  # 100ms entre testes de API