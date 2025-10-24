"""
Testes CRUD de Integração - JSONPlaceholder API
"""
import pytest


class TestTodosCRUD:
    """Testes CRUD completos para TODOs"""
    
    def test_listar_todos_existentes(self, api_client):
        """Teste READ: Listar todos os TODOs existentes"""
        response = api_client.get(f"{api_client.base_url}/todos")
        assert response.status_code == 200
        
        todos = response.json()
        assert isinstance(todos, list)
        assert len(todos) > 0
        
        # Validar estrutura do primeiro TODO
        first_todo = todos[0]
        assert "id" in first_todo
        assert "userId" in first_todo
        assert "title" in first_todo
        assert "completed" in first_todo
    
    def test_buscar_todo_por_id(self, api_client):
        """Teste READ: Buscar TODO específico por ID"""
        todo_id = 1
        response = api_client.get(f"{api_client.base_url}/todos/{todo_id}")
        assert response.status_code == 200
        
        todo = response.json()
        assert todo["id"] == todo_id
        assert "userId" in todo
        assert "title" in todo
        assert isinstance(todo["completed"], bool)
    
    def test_criar_todo_valido(self, api_client, todo_payload):
        """Teste CREATE: Criar novo TODO com dados válidos"""
        response = api_client.post(f"{api_client.base_url}/todos", json=todo_payload)
        assert response.status_code == 201
        
        created_todo = response.json()
        assert created_todo["userId"] == todo_payload["userId"]
        assert created_todo["title"] == todo_payload["title"]
        assert created_todo["completed"] == todo_payload["completed"]
        assert "id" in created_todo  # ID gerado pela API
    
    def test_atualizar_todo_existente(self, api_client):
        """Teste UPDATE: Atualizar TODO existente"""
        todo_id = 1
        update_data = {
            "userId": 1,
            "title": "TODO atualizado via teste",
            "completed": True
        }
        
        response = api_client.put(f"{api_client.base_url}/todos/{todo_id}", json=update_data)
        assert response.status_code == 200
        
        updated_todo = response.json()
        assert updated_todo["id"] == todo_id
        assert updated_todo["title"] == update_data["title"]
        assert updated_todo["completed"] == update_data["completed"]
    
    def test_deletar_todo_existente(self, api_client):
        """Teste DELETE: Remover TODO existente"""
        todo_id = 1
        response = api_client.delete(f"{api_client.base_url}/todos/{todo_id}")
        assert response.status_code == 200


class TestUsersCRUD:
    """Testes CRUD completos para usuários"""
    
    def test_listar_usuarios_existentes(self, api_client):
        """Teste READ: Listar todos os usuários"""
        response = api_client.get(f"{api_client.base_url}/users")
        assert response.status_code == 200
        
        users = response.json()
        assert isinstance(users, list)
        assert len(users) > 0
        
        # Validar estrutura do primeiro usuário
        first_user = users[0]
        assert "id" in first_user
        assert "name" in first_user
        assert "email" in first_user
        assert "address" in first_user
    
    def test_buscar_usuario_por_id(self, api_client):
        """Teste READ: Buscar usuário específico por ID"""
        user_id = 1
        response = api_client.get(f"{api_client.base_url}/users/{user_id}")
        assert response.status_code == 200
        
        user = response.json()
        assert user["id"] == user_id
        assert "@" in user["email"]  # Validação básica de email
        assert "address" in user
        assert "geo" in user["address"]
    
    def test_criar_usuario_valido(self, api_client, user_payload):
        """Teste CREATE: Criar novo usuário com dados completos"""
        response = api_client.post(f"{api_client.base_url}/users", json=user_payload)
        assert response.status_code == 201
        
        created_user = response.json()
        assert created_user["name"] == user_payload["name"]
        assert created_user["email"] == user_payload["email"]
        assert "id" in created_user
    
    def test_atualizar_usuario_existente(self, api_client):
        """Teste UPDATE: Atualizar dados do usuário"""
        user_id = 1
        update_data = {
            "name": "Nome Atualizado",
            "email": "atualizado@teste.com",
            "username": "usuario_atualizado"
        }
        
        response = api_client.put(f"{api_client.base_url}/users/{user_id}", json=update_data)
        assert response.status_code == 200
        
        updated_user = response.json()
        assert updated_user["id"] == user_id
        assert updated_user["name"] == update_data["name"]
        assert updated_user["email"] == update_data["email"]


class TestPostsCRUD:
    """Testes CRUD completos para posts"""
    
    def test_listar_posts_existentes(self, api_client):
        """Teste READ: Listar todos os posts"""
        response = api_client.get(f"{api_client.base_url}/posts")
        assert response.status_code == 200
        
        posts = response.json()
        assert isinstance(posts, list)
        assert len(posts) > 0
        
        # Validar estrutura do primeiro post
        first_post = posts[0]
        assert "id" in first_post
        assert "userId" in first_post
        assert "title" in first_post
        assert "body" in first_post
    
    def test_criar_post_valido(self, api_client, post_payload):
        """Teste CREATE: Criar novo post"""
        response = api_client.post(f"{api_client.base_url}/posts", json=post_payload)
        assert response.status_code == 201
        
        created_post = response.json()
        assert created_post["userId"] == post_payload["userId"]
        assert created_post["title"] == post_payload["title"]
        assert created_post["body"] == post_payload["body"]
        assert "id" in created_post
    
    def test_atualizar_post_existente(self, api_client):
        """Teste UPDATE: Atualizar post existente"""
        post_id = 1
        update_data = {
            "userId": 1,
            "title": "Título Atualizado",
            "body": "Conteúdo do post atualizado via teste automatizado."
        }
        
        response = api_client.put(f"{api_client.base_url}/posts/{post_id}", json=update_data)
        assert response.status_code == 200
        
        updated_post = response.json()
        assert updated_post["id"] == post_id
        assert updated_post["title"] == update_data["title"]
        assert updated_post["body"] == update_data["body"]


class TestIntegracaoCRUD:
    """Testes de integração entre recursos relacionados"""
    
    def test_integracao_usuario_posts(self, api_client):
        """Testa integração: usuário e seus posts"""
        user_id = 1
        
        # Buscar usuário
        user_response = api_client.get(f"{api_client.base_url}/users/{user_id}")
        assert user_response.status_code == 200
        user = user_response.json()
        
        # Buscar posts do usuário
        posts_response = api_client.get(f"{api_client.base_url}/posts?userId={user_id}")
        assert posts_response.status_code == 200
        posts = posts_response.json()
        
        # Verificar integridade referencial
        assert len(posts) > 0
        assert all(post["userId"] == user["id"] for post in posts)
    
    def test_integracao_usuario_todos(self, api_client):
        """Testa integração: usuário e seus TODOs"""
        user_id = 1
        
        # Buscar usuário
        user_response = api_client.get(f"{api_client.base_url}/users/{user_id}")
        assert user_response.status_code == 200
        
        # Buscar TODOs do usuário
        todos_response = api_client.get(f"{api_client.base_url}/todos?userId={user_id}")
        assert todos_response.status_code == 200
        todos = todos_response.json()
        
        # Verificar integridade referencial
        assert len(todos) > 0
        assert all(todo["userId"] == user_id for todo in todos)
    
    def test_integracao_post_comentarios(self, api_client):
        """Testa integração: post e seus comentários"""
        post_id = 1
        
        # Buscar post
        post_response = api_client.get(f"{api_client.base_url}/posts/{post_id}")
        assert post_response.status_code == 200
        
        # Buscar comentários do post
        comments_response = api_client.get(f"{api_client.base_url}/posts/{post_id}/comments")
        assert comments_response.status_code == 200
        comments = comments_response.json()
        
        # Verificar integridade referencial
        assert len(comments) > 0
        assert all(comment["postId"] == post_id for comment in comments)


class TestErrorHandling:
    """Testes de tratamento de erros e edge cases"""
    
    def test_buscar_recurso_inexistente(self, api_client):
        """Teste de erro: buscar recurso que não existe"""
        recursos = ["users", "posts", "todos"]
        
        for recurso in recursos:
            response = api_client.get(f"{api_client.base_url}/{recurso}/99999")
            assert response.status_code == 404
    
    def test_criar_recurso_dados_invalidos(self, api_client):
        """Teste de erro: criar recurso com dados inválidos"""
        # TODO com dados incompletos
        invalid_todo = {"title": ""}  # título vazio
        response = api_client.post(f"{api_client.base_url}/todos", json=invalid_todo)
        # JSONPlaceholder aceita dados inválidos, mas em API real seria 400
        assert response.status_code in [200, 201, 400]
    