import pytest
from fastapi.testclient import TestClient
from app.models.usuario import Usuario
from app.core.seguranca import verificar_senha

class TestAutenticacao:
    """Testes de integração para autenticação."""
    
    def test_registro_usuario_sucesso(self, client: TestClient, db_session):
        """Testa registro de usuário com sucesso."""
        dados_usuario = {
            "email": "novo@exemplo.com",
            "senha": "senha123",
            "nome": "Novo Usuário",
            "telefone": "11999999999"
        }
        
        response = client.post("/api/auth/registrar", json=dados_usuario)
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["email"] == dados_usuario["email"]
        assert data["nome"] == dados_usuario["nome"]
        assert "senha" not in data  # Senha não deve ser retornada
        
        # Verifica se o usuário foi criado no banco
        usuario_db = db_session.query(Usuario).filter(Usuario.email == dados_usuario["email"]).first()
        assert usuario_db is not None
        assert verificar_senha(dados_usuario["senha"], usuario_db.senha_hash)
    
    def test_registro_email_duplicado(self, client: TestClient, db_session, usuario_teste):
        """Testa registro com email duplicado."""
        # Primeiro registro
        client.post("/api/auth/registrar", json=usuario_teste)
        
        # Segundo registro com mesmo email
        response = client.post("/api/auth/registrar", json=usuario_teste)
        
        assert response.status_code == 400
        assert "Email já cadastrado" in response.json()["detail"]
    
    def test_login_sucesso(self, client: TestClient, usuario_teste):
        """Testa login com credenciais válidas."""
        # Registra usuário
        client.post("/api/auth/registrar", json=usuario_teste)
        
        # Faz login
        dados_login = {
            "email": usuario_teste["email"],
            "senha": usuario_teste["senha"]
        }
        
        response = client.post("/api/auth/login", data=dados_login)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        assert "usuario" in data
        assert data["usuario"]["email"] == usuario_teste["email"]
    
    def test_login_credenciais_invalidas(self, client: TestClient, usuario_teste):
        """Testa login com credenciais inválidas."""
        # Registra usuário
        client.post("/api/auth/registrar", json=usuario_teste)
        
        # Tenta login com senha errada
        dados_login = {
            "email": usuario_teste["email"],
            "senha": "senha_errada"
        }
        
        response = client.post("/api/auth/login", data=dados_login)
        
        assert response.status_code == 422
    
    def test_obter_usuario_autenticado(self, client: TestClient, usuario_teste, headers_autenticacao):
        """Testa obtenção de dados do usuário autenticado."""
        # Registra usuário
        client.post("/api/auth/registrar", json=usuario_teste)
        
        # Obtém dados do usuário
        response = client.get("/api/auth/me", headers=headers_autenticacao)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == usuario_teste["email"]
        assert data["nome"] == usuario_teste["nome"]
    
    def test_obter_usuario_nao_autenticado(self, client: TestClient):
        """Testa obtenção de dados sem autenticação."""
        response = client.get("/api/auth/me")
        
        assert response.status_code == 403
    
    def test_alterar_senha_sucesso(self, client: TestClient, usuario_teste, headers_autenticacao):
        """Testa alteração de senha com sucesso."""
        # Registra usuário
        client.post("/api/auth/registrar", json=usuario_teste)
        
        # Altera senha
        dados_alteracao = {
            "senha_atual": usuario_teste["senha"],
            "nova_senha": "nova_senha123"
        }
        
        response = client.put("/api/auth/me/alterar-senha", json=dados_alteracao, headers=headers_autenticacao)
        
        assert response.status_code == 200
        assert "Senha alterada com sucesso" in response.json()["mensagem"]
    
    def test_alterar_senha_senha_atual_errada(self, client: TestClient, usuario_teste, headers_autenticacao):
        """Testa alteração de senha com senha atual incorreta."""
        # Registra usuário
        client.post("/api/auth/registrar", json=usuario_teste)
        
        # Tenta alterar senha com senha atual errada
        dados_alteracao = {
            "senha_atual": "senha_errada",
            "nova_senha": "nova_senha123"
        }
        
        response = client.put("/api/auth/me/alterar-senha", json=dados_alteracao, headers=headers_autenticacao)
        
        assert response.status_code == 400
        assert "Senha atual incorreta" in response.json()["detail"]
