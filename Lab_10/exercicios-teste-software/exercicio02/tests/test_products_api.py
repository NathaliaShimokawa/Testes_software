"""
Testes automatizados para a API Fake Store
API Base: https://fakestoreapi.com/
"""
import pytest
import requests
import jsonschema
from jsonschema import validate
import json


class TestProductsAPI:
    """Classe de testes para a API de produtos da Fake Store"""
    
    BASE_URL = "https://fakestoreapi.com"
    PRODUCTS_ENDPOINT = f"{BASE_URL}/products"
    CATEGORIES_ENDPOINT = f"{BASE_URL}/products/categories"
    
    # Categorias esperadas conforme documentação
    EXPECTED_CATEGORIES = ["electronics", "jewelery", "men's clothing", "women's clothing"]
    
    # Schema JSON para validação dos produtos
    PRODUCT_SCHEMA = {
        "type": "object",
        "required": ["id", "title", "price", "description", "category", "image", "rating"],
        "properties": {
            "id": {"type": "integer", "minimum": 1},
            "title": {"type": "string", "minLength": 1},
            "price": {"type": "number", "minimum": 0},
            "description": {"type": "string", "minLength": 1},
            "category": {"type": "string", "enum": EXPECTED_CATEGORIES},
            "image": {"type": "string", "format": "uri"},
            "rating": {
                "type": "object",
                "required": ["rate", "count"],
                "properties": {
                    "rate": {"type": "number", "minimum": 0, "maximum": 5},
                    "count": {"type": "integer", "minimum": 0}
                }
            }
        }
    }
    
    def test_listar_todos_produtos(self, api_session):
        """
        Teste: Listar todos os produtos
        Cenário: Requisição GET para /products
        Resultado esperado: Lista com todos os produtos (20 itens)
        """
        response = api_session.get(self.PRODUCTS_ENDPOINT)
        
        # Verificar status code
        assert response.status_code == 200, f"Status code esperado: 200, obtido: {response.status_code}"
        
        # Verificar se retorna lista
        products = response.json()
        assert isinstance(products, list), "A resposta deve ser uma lista"
        
        # Verificar quantidade de produtos (API retorna 20 produtos)
        assert len(products) == 20, f"Esperado 20 produtos, obtido: {len(products)}"
        
        # Verificar se todos os produtos têm campos obrigatórios
        for product in products:
            assert "id" in product, "Produto deve ter campo 'id'"
            assert "title" in product, "Produto deve ter campo 'title'"
            assert "price" in product, "Produto deve ter campo 'price'"
            assert "category" in product, "Produto deve ter campo 'category'"
            
        # Verificar se o primeiro produto tem estrutura correta
        first_product = products[0]
        assert "title" in first_product
        assert isinstance(first_product["id"], int)
        assert isinstance(first_product["price"], (int, float))
    
    def test_buscar_produto_por_id_valido(self, api_session):
        """
        Teste: Buscar produto por ID válido
        Cenário: Requisição GET para /products/{id} com ID existente
        Resultado esperado: Retorna produto específico
        """
        product_id = 1
        response = api_session.get(f"{self.PRODUCTS_ENDPOINT}/{product_id}")
        
        # Verificar status code
        assert response.status_code == 200, f"Status code esperado: 200, obtido: {response.status_code}"
        
        # Verificar se retorna um produto
        product = response.json()
        assert isinstance(product, dict), "A resposta deve ser um objeto"
        
        # Verificar se o ID corresponde
        assert product["id"] == product_id, f"ID esperado: {product_id}, obtido: {product['id']}"
        
        # Verificar campos obrigatórios
        required_fields = ["id", "title", "price", "description", "category", "image", "rating"]
        for field in required_fields:
            assert field in product, f"Campo obrigatório '{field}' não encontrado"
    
    def test_buscar_produto_por_id_invalido(self, api_session):
        """
        Teste: Buscar produto por ID inválido
        Cenário: Requisição GET para /products/{id} com ID inexistente
        Resultado esperado: Retorna erro ou produto vazio
        """
        invalid_id = 999999
        response = api_session.get(f"{self.PRODUCTS_ENDPOINT}/{invalid_id}")
        
        # Para esta API, ID inválido pode retornar diferentes respostas
        if response.status_code == 200:
            # Se retornou 200, verificar se consegue fazer parse do JSON
            try:
                product = response.json()
                # Se retornou 200 e conseguiu fazer parse, deve ser null ou objeto vazio
                assert product is None or product == {}, f"Para ID inválido, esperado null ou vazio, obtido: {product}"
            except ValueError:
                # Se não conseguiu fazer parse do JSON, pode ser resposta vazia
                assert response.text.strip() == "", f"Para ID inválido, resposta deve estar vazia, obtido: '{response.text}'"
        else:
            # Ou retorna status de erro
            assert response.status_code in [404, 400], f"Status code para ID inválido deve ser 404 ou 400, obtido: {response.status_code}"
    
    @pytest.mark.parametrize("category", EXPECTED_CATEGORIES)
    def test_filtrar_produtos_por_categoria(self, api_session, category):
        """
        Teste parametrizado: Filtrar produtos por categoria
        Cenário: Requisição GET para /products/category/{category}
        Resultado esperado: Lista de produtos da categoria específica
        """
        response = api_session.get(f"{self.PRODUCTS_ENDPOINT}/category/{category}")
        
        # Verificar status code
        assert response.status_code == 200, f"Status code esperado: 200, obtido: {response.status_code}"
        
        # Verificar se retorna lista
        products = response.json()
        assert isinstance(products, list), "A resposta deve ser uma lista"
        
        # Verificar se não está vazia (todas as categorias têm produtos)
        assert len(products) > 0, f"Categoria '{category}' deve ter produtos"
        
        # Verificar se todos os produtos são da categoria solicitada
        for product in products:
            assert product["category"] == category, f"Produto com categoria '{product['category']}' em filtro de '{category}'"
    
    def test_listar_categorias_disponiveis(self, api_session):
        """
        Teste: Listar todas as categorias disponíveis
        Cenário: Requisição GET para /products/categories
        Resultado esperado: Lista com categorias válidas
        """
        response = api_session.get(self.CATEGORIES_ENDPOINT)
        
        # Verificar status code
        assert response.status_code == 200, f"Status code esperado: 200, obtido: {response.status_code}"
        
        # Verificar se retorna lista
        categories = response.json()
        assert isinstance(categories, list), "A resposta deve ser uma lista"
        
        # Verificar se contém as categorias esperadas
        for expected_category in self.EXPECTED_CATEGORIES:
            assert expected_category in categories, f"Categoria '{expected_category}' não encontrada"
        
        # Verificar se não há categorias extras inesperadas
        assert len(categories) == len(self.EXPECTED_CATEGORIES), f"Número de categorias inesperado: {categories}"
    
    def test_validar_schema_produto(self, api_session):
        """
        Teste: Validar schema da resposta de produto
        Cenário: Buscar um produto e validar estrutura JSON
        Resultado esperado: Produto segue schema definido
        """
        response = api_session.get(f"{self.PRODUCTS_ENDPOINT}/1")
        
        assert response.status_code == 200
        product = response.json()
        
        # Validar schema usando jsonschema
        try:
            validate(instance=product, schema=self.PRODUCT_SCHEMA)
        except jsonschema.exceptions.ValidationError as e:
            pytest.fail(f"Produto não segue o schema esperado: {e.message}")
    
    def test_validar_schema_lista_produtos(self, api_session):
        """
        Teste: Validar schema da lista de produtos
        Cenário: Listar produtos e validar estrutura de cada item
        Resultado esperado: Todos os produtos seguem schema definido
        """
        response = api_session.get(self.PRODUCTS_ENDPOINT)
        
        assert response.status_code == 200
        products = response.json()
        
        # Validar schema de cada produto
        for i, product in enumerate(products):
            try:
                validate(instance=product, schema=self.PRODUCT_SCHEMA)
            except jsonschema.exceptions.ValidationError as e:
                pytest.fail(f"Produto {i+1} (ID: {product.get('id', 'N/A')}) não segue o schema: {e.message}")
    
    @pytest.mark.parametrize("limit", [1, 5, 10, 20])
    def test_limite_produtos_retornados(self, api_session, limit):
        """
        Teste parametrizado: Testar limite de produtos retornados
        Cenário: Requisição GET para /products?limit={limit}
        Resultado esperado: Número correto de produtos retornados
        """
        response = api_session.get(f"{self.PRODUCTS_ENDPOINT}?limit={limit}")
        
        # Verificar status code
        assert response.status_code == 200, f"Status code esperado: 200, obtido: {response.status_code}"
        
        # Verificar se retorna lista
        products = response.json()
        assert isinstance(products, list), "A resposta deve ser uma lista"
        
        # Verificar se o número de produtos retornados está correto
        assert len(products) == limit, f"Esperado {limit} produtos, obtido: {len(products)}"
        
        # Verificar se os produtos são válidos
        for product in products:
            assert "id" in product
            assert "title" in product
    
    def test_limite_maximo_produtos(self, api_session):
        """
        Teste: Verificar comportamento com limite maior que total disponível
        Cenário: Requisição GET para /products?limit=100
        Resultado esperado: Retorna todos os produtos disponíveis (máximo 20)
        """
        large_limit = 100
        response = api_session.get(f"{self.PRODUCTS_ENDPOINT}?limit={large_limit}")
        
        assert response.status_code == 200
        products = response.json()
        
        # Não deve retornar mais que o total disponível
        assert len(products) <= 20, f"Não deve retornar mais que 20 produtos, obtido: {len(products)}"
    
    def test_limite_zero_ou_negativo(self, api_session):
        """
        Teste: Verificar comportamento com limite zero ou negativo
        Cenário: Requisição GET para /products?limit=0
        Resultado esperado: Retorna lista vazia ou todos os produtos
        """
        response = api_session.get(f"{self.PRODUCTS_ENDPOINT}?limit=0")
        
        assert response.status_code == 200
        products = response.json()
        
        # Comportamento pode variar, mas deve ser uma lista válida
        assert isinstance(products, list)
    
    def test_ordenacao_produtos(self, api_session):
        """
        Teste: Verificar ordenação de produtos
        Cenário: Requisição GET para /products?sort=desc
        Resultado esperado: Produtos ordenados por ID decrescente
        """
        # Testar ordenação crescente (padrão)
        response_asc = api_session.get(f"{self.PRODUCTS_ENDPOINT}?sort=asc")
        assert response_asc.status_code == 200
        products_asc = response_asc.json()
        
        # Testar ordenação decrescente
        response_desc = api_session.get(f"{self.PRODUCTS_ENDPOINT}?sort=desc")
        assert response_desc.status_code == 200
        products_desc = response_desc.json()
        
        # Verificar se as ordenações são diferentes
        if len(products_asc) > 1 and len(products_desc) > 1:
            assert products_asc[0]["id"] != products_desc[0]["id"], "Ordenação ascendente e descendente devem ser diferentes"
    
    def test_combinacao_filtros(self, api_session):
        """
        Teste: Combinação de filtros (categoria + limite)
        Cenário: Requisição GET para /products/category/electronics?limit=2
        Resultado esperado: Máximo 2 produtos da categoria electronics
        """
        category = "electronics"
        limit = 2
        
        response = api_session.get(f"{self.PRODUCTS_ENDPOINT}/category/{category}?limit={limit}")
        
        assert response.status_code == 200
        products = response.json()
        
        # Verificar limite
        assert len(products) <= limit, f"Não deve retornar mais que {limit} produtos"
        
        # Verificar categoria (se houver produtos)
        if products:
            for product in products:
                assert product["category"] == category
    
    def test_headers_response(self, api_session):
        """
        Teste: Verificar headers da resposta
        Cenário: Requisição GET para /products
        Resultado esperado: Headers apropriados (Content-Type, etc.)
        """
        response = api_session.get(self.PRODUCTS_ENDPOINT)
        
        assert response.status_code == 200
        
        # Verificar Content-Type
        content_type = response.headers.get('content-type', '')
        assert 'application/json' in content_type.lower(), f"Content-Type esperado: application/json, obtido: {content_type}"
        
        # Verificar se há headers de cache (opcional)
        # APIs REST geralmente têm políticas de cache
        assert 'cache-control' in [h.lower() for h in response.headers.keys()] or \
               'etag' in [h.lower() for h in response.headers.keys()], "Headers de cache esperados"
    
    def test_performance_api(self, api_session):
        """
        Teste: Verificar performance básica da API
        Cenário: Medir tempo de resposta da API
        Resultado esperado: Resposta em tempo razoável (< 5 segundos)
        """
        import time
        
        start_time = time.time()
        response = api_session.get(self.PRODUCTS_ENDPOINT)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 5.0, f"API muito lenta. Tempo de resposta: {response_time:.2f}s"
    
    def test_encoding_unicode(self, api_session):
        """
        Teste: Verificar suporte a caracteres especiais
        Cenário: Verificar se produtos com caracteres especiais são tratados corretamente
        Resultado esperado: Strings decodificadas corretamente
        """
        response = api_session.get(self.PRODUCTS_ENDPOINT)
        
        assert response.status_code == 200
        products = response.json()
        
        # Verificar se strings são válidas e não têm problemas de encoding
        for product in products:
            title = product.get("title", "")
            description = product.get("description", "")
            
            # Verificar se são strings válidas (não None)
            assert isinstance(title, str), f"Título deve ser string: {title}"
            assert isinstance(description, str), f"Descrição deve ser string: {description}"
            
            # Verificar se não há caracteres de encoding quebrados
            assert "�" not in title, f"Problema de encoding no título: {title}"
            assert "�" not in description, f"Problema de encoding na descrição: {description}"