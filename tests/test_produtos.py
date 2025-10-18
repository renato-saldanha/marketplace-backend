import pytest
from fastapi.testclient import TestClient
from app.models.produto import Produto
from app.models.usuario import Usuario

class TestProdutos:
    """Testes de integração para produtos."""
    
    def test_criar_produto_sucesso(self, client: TestClient, usuario_teste, produto_teste, headers_autenticacao):
        """Testa criação de produto com sucesso."""
        # Registra usuário
        client.post("/api/auth/registrar", json=usuario_teste)
        
        # Cria produto
        response = client.post("/api/produtos/", json=produto_teste, headers=headers_autenticacao)
        
        assert response.status_code == 200
        data = response.json()
        assert data["titulo"] == produto_teste["titulo"]
        assert data["descricao"] == produto_teste["descricao"]
        assert data["preco"] == produto_teste["preco"]
        assert data["categoria"] == produto_teste["categoria"]
        assert data["status"] == produto_teste["status"]
        assert "id" in data
        assert "data_criacao" in data
    
    def test_criar_produto_sem_autenticacao(self, client: TestClient, produto_teste):
        """Testa criação de produto sem autenticação."""
        response = client.post("/api/produtos/", json=produto_teste)
        
        assert response.status_code == 403
    
    def test_listar_produtos_usuario(self, client: TestClient, usuario_teste, produto_teste, headers_autenticacao):
        """Testa listagem de produtos do usuário."""
        # Registra usuário
        client.post("/api/auth/registrar", json=usuario_teste)
        
        # Cria produto
        client.post("/api/produtos/", json=produto_teste, headers=headers_autenticacao)
        
        # Lista produtos
        response = client.get("/api/produtos/meus", headers=headers_autenticacao)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["titulo"] == produto_teste["titulo"]
    
    def test_atualizar_produto_sucesso(self, client: TestClient, usuario_teste, produto_teste, headers_autenticacao):
        """Testa atualização de produto com sucesso."""
        # Registra usuário
        client.post("/api/auth/registrar", json=usuario_teste)
        
        # Cria produto
        response = client.post("/api/produtos/", json=produto_teste, headers=headers_autenticacao)
        produto_id = response.json()["id"]
        
        # Atualiza produto
        dados_atualizacao = {
            "titulo": "Produto Atualizado",
            "preco": 199.99
        }
        
        response = client.put(f"/api/produtos/{produto_id}", json=dados_atualizacao, headers=headers_autenticacao)
        
        assert response.status_code == 200
        data = response.json()
        assert data["titulo"] == "Produto Atualizado"
        assert data["preco"] == 199.99
    
    def test_excluir_produto_sucesso(self, client: TestClient, usuario_teste, produto_teste, headers_autenticacao):
        """Testa exclusão de produto com sucesso."""
        # Registra usuário
        client.post("/api/auth/registrar", json=usuario_teste)
        
        # Cria produto
        response = client.post("/api/produtos/", json=produto_teste, headers=headers_autenticacao)
        produto_id = response.json()["id"]
        
        # Exclui produto
        response = client.delete(f"/api/produtos/{produto_id}", headers=headers_autenticacao)
        
        assert response.status_code == 200
        
        # Verifica se produto foi excluído
        response = client.get("/api/produtos/meus", headers=headers_autenticacao)
        assert len(response.json()) == 0
    
    def test_obter_produto_por_id(self, client: TestClient, usuario_teste, produto_teste, headers_autenticacao):
        """Testa obtenção de produto por ID."""
        # Registra usuário
        client.post("/api/auth/registrar", json=usuario_teste)
        
        # Cria produto
        response = client.post("/api/produtos/", json=produto_teste, headers=headers_autenticacao)
        produto_id = response.json()["id"]
        
        # Obtém produto por ID
        response = client.get(f"/api/produtos/{produto_id}", headers=headers_autenticacao)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == produto_id
        assert data["titulo"] == produto_teste["titulo"]
    
    def test_obter_produto_inexistente(self, client: TestClient, headers_autenticacao):
        """Testa obtenção de produto inexistente."""
        response = client.get("/api/produtos/99999999-9999-9999-9999-999999999999", headers=headers_autenticacao)
        
        assert response.status_code == 404
    
    def test_listar_produtos_com_filtros(self, client: TestClient, usuario_teste, headers_autenticacao):
        """Testa listagem de produtos com filtros."""
        # Registra usuário
        client.post("/api/auth/registrar", json=usuario_teste)
        
        # Cria produtos com diferentes categorias
        produtos = [
            {"titulo": "Produto 1", "descricao": "Desc 1", "preco": 100, "categoria": "Eletrônicos", "status": "ativo"},
            {"titulo": "Produto 2", "descricao": "Desc 2", "preco": 200, "categoria": "Roupas", "status": "ativo"},
            {"titulo": "Produto 3", "descricao": "Desc 3", "preco": 50, "categoria": "Eletrônicos", "status": "ativo"}
        ]
        
        for produto in produtos:
            client.post("/api/produtos/", json=produto, headers=headers_autenticacao)
        
        # Filtra por categoria
        response = client.get("/api/produtos/?categoria=Eletrônicos", headers=headers_autenticacao)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(produto["categoria"] == "Eletrônicos" for produto in data)
        
        # Filtra por preço mínimo
        response = client.get("/api/produtos/?preco_min=150", headers=headers_autenticacao)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["preco"] >= 150
