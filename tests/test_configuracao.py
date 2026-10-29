import pytest
from fastapi.testclient import TestClient
from app.models.configuracao import ConfiguracaoUsuario

class TestConfiguracao:
    """Testes de integração para configurações."""
    
    def test_obter_configuracao_padrao(self, client: TestClient, usuario_teste, headers_autenticacao):
        """Testa obtenção de configuração padrão."""
        # Registra usuário
        client.post("/api/auth/registrar", json=usuario_teste)
        
        # Obtém configuração
        response = client.get("/api/configuracao/me", headers=headers_autenticacao)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verifica configurações padrão
        assert data["notificacoes_email"] == True
        assert data["notificacoes_push"] == True
        assert data["tema_preferido"] == "claro"
        assert data["idioma_preferido"] == "pt-BR"
        assert data["perfil_publico"] == False
    
    def test_atualizar_configuracao_sucesso(self, client: TestClient, usuario_teste, headers_autenticacao):
        """Testa atualização de configuração com sucesso."""
        # Registra usuário
        client.post("/api/auth/registrar", json=usuario_teste)
        
        # Atualiza configuração
        dados_atualizacao = {
            "notificacoes_email": False,
            "tema_preferido": "escuro",
            "idioma_preferido": "en-US"
        }
        
        response = client.put("/api/configuracao/me", json=dados_atualizacao, headers=headers_autenticacao)
        
        assert response.status_code == 200
        data = response.json()
        assert data["notificacoes_email"] == False
        assert data["tema_preferido"] == "escuro"
        assert data["idioma_preferido"] == "en-US"
    
    def test_resetar_configuracao(self, client: TestClient, usuario_teste, headers_autenticacao):
        """Testa reset de configuração para padrões."""
        # Registra usuário
        client.post("/api/auth/registrar", json=usuario_teste)
        
        # Atualiza configuração
        dados_atualizacao = {
            "notificacoes_email": False,
            "tema_preferido": "escuro"
        }
        client.put("/api/configuracao/me", json=dados_atualizacao, headers=headers_autenticacao)
        
        # Reseta configuração
        response = client.post("/api/configuracao/me/reset", headers=headers_autenticacao)
        
        assert response.status_code == 200
        
        # Verifica se voltou ao padrão
        response = client.get("/api/configuracao/me", headers=headers_autenticacao)
        data = response.json()
        assert data["notificacoes_email"] == True
        assert data["tema_preferido"] == "claro"
    
    def test_exportar_dados_usuario(self, client: TestClient, usuario_teste, produto_teste, headers_autenticacao):
        """Testa exportação de dados do usuário."""
        # Registra usuário
        client.post("/api/auth/registrar", json=usuario_teste)
        
        # Cria produto
        client.post("/api/produtos/", json=produto_teste, headers=headers_autenticacao)
        
        # Exporta dados
        response = client.get("/api/auth/me/exportar-dados", headers=headers_autenticacao)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verifica estrutura dos dados exportados
        assert "usuario" in data
        assert "produtos" in data
        assert data["usuario"]["email"] == usuario_teste["email"]
        assert len(data["produtos"]) == 1
        assert data["produtos"][0]["titulo"] == produto_teste["titulo"]
    
    def test_excluir_conta_usuario(self, client: TestClient, usuario_teste, produto_teste, headers_autenticacao):
        """Testa exclusão de conta do usuário."""
        # Registra usuário
        client.post("/api/auth/registrar", json=usuario_teste)
        
        # Cria produto
        client.post("/api/produtos/", json=produto_teste, headers=headers_autenticacao)
        
        # Exclui conta
        response = client.delete("/api/auth/me", headers=headers_autenticacao)
        
        assert response.status_code == 200
        assert "Conta excluída com sucesso" in response.json()["mensagem"]
        
        # Verifica se não consegue mais acessar dados
        response = client.get("/api/auth/me", headers=headers_autenticacao)
        assert response.status_code == 401
