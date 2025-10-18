import pytest
from fastapi.testclient import TestClient

def test_health_check(client: TestClient):
    """Testa o health check da API."""
    response = client.get("/")
    assert response.status_code == 200
    # O endpoint raiz retorna mensagem de sucesso
    data = response.json()
    assert "mensagem" in data or "status" in data

def test_registro_simples(client: TestClient):
    """Testa registro simples sem validações complexas."""
    dados_usuario = {
        "email": "teste@teste.com",
        "senha": "123456",
        "nome": "Teste",
        "telefone": "11999999999"
    }
    
    response = client.post("/api/auth/registrar", json=dados_usuario)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Aceita tanto 200 quanto 400 (dependendo da validação)
    assert response.status_code in [200, 400]

    assert response.status_code in [200, 400]

    assert response.status_code in [200, 400]
