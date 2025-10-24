# Exercício 03 - Testes CRUD de Integração

## Objetivo
Implementar e exercitar testes de integração completos usando operações CRUD (Create, Read, Update, Delete) em APIs REST, validando o ciclo completo de vida dos dados.

## Conceitos Abordados

### 1. **Testes CRUD Completos**
- **CREATE**: POST para criação de recursos
- **READ**: GET para leitura/consulta de dados  
- **UPDATE**: PUT/PATCH para atualização de recursos
- **DELETE**: DELETE para remoção de recursos

### 2. **Testes de Integração**
- Validação de fluxos end-to-end
- Interdependência entre operações
- Consistência de dados entre requests
- Simulação de cenários reais de uso

## Recursos Testados

### 1. **TODOs Management**
- Criar novo TODO
- Listar TODOs existentes
- Atualizar status de TODO (completed/pending)
- Remover TODO
- Validar estrutura de dados

### 2. **Users Management** 
- Criar usuário completo com endereço
- Buscar usuário por ID
- Atualizar dados do usuário
- Validar relacionamentos (user → todos)

### 3. **Posts Management**
- Criar post associado a usuário
- Listar posts por usuário
- Atualizar conteúdo do post
- Remover post


## Cenários de Teste

### 1. **Fluxo CRUD Básico**
```python
def test_crud_completo():
    # CREATE: Criar recurso
    response_post = client.post("/todos", json=payload)
    assert response_post.status_code == 201
    
    # READ: Ler recurso criado  
    todo_id = response_post.json()["id"]
    response_get = client.get(f"/todos/{todo_id}")
    assert response_get.status_code == 200
    
    # UPDATE: Atualizar recurso
    update_payload = {"completed": True}
    response_put = client.put(f"/todos/{todo_id}", json=update_payload)
    assert response_put.status_code == 200
    
    # DELETE: Remover recurso
    response_delete = client.delete(f"/todos/{todo_id}")
    assert response_delete.status_code == 200
```
