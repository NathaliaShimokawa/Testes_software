"""
Configurações para testes CRUD de integração
"""
import pytest
import requests


@pytest.fixture(scope="session")
def base_url():
    """URL base da API JSONPlaceholder para testes CRUD"""
    return "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="function")
def api_client(base_url):
    """
    Cliente HTTP configurado para testes CRUD
    
    Cria uma nova sessão para cada teste, garantindo isolamento
    entre os testes CRUD.
    """
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json"
    })
    
    # Adiciona a URL base como atributo da sessão
    session.base_url = base_url
    
    yield session
    
    session.close()


@pytest.fixture
def todo_payload():
    """
    Payload padrão para criação de TODOs nos testes
    """
    return {
        "userId": 1,
        "title": "Test TODO from pytest",
        "completed": False
    }


@pytest.fixture
def user_payload():
    """
    Payload padrão para criação de usuários nos testes  
    """
    return {
        "name": "Test User",
        "username": "testuser",
        "email": "test@example.com",
        "address": {
            "street": "Test Street",
            "suite": "Apt. 123",
            "city": "Test City",
            "zipcode": "12345-678",
            "geo": {
                "lat": "-37.3159",
                "lng": "81.1496"
            }
        },
        "phone": "1-770-736-8031 x56442",
        "website": "test.org",
        "company": {
            "name": "Test Company",
            "catchPhrase": "Testing is everything",
            "bs": "harness real-time e-markets"
        }
    }


@pytest.fixture
def post_payload():
    """
    Payload padrão para criação de posts nos testes
    """
    return {
        "userId": 1,
        "title": "Test Post Title",
        "body": "This is a test post body created during automated testing."
    }