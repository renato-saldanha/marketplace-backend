import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.database import obter_sessao, Base
from app.core.seguranca import criar_token_acesso

# Configuração do banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def event_loop():
    """Cria um event loop para toda a sessão de testes."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def db_session():
    """Cria uma sessão de banco de dados para cada teste."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Cria um cliente de teste FastAPI."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[obter_sessao] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def usuario_teste():
    """Dados de usuário para testes."""
    return {
        "email": "teste@exemplo.com",
        "senha": "senha123",
        "nome": "Usuário Teste",
        "telefone": "11999999999"
    }

@pytest.fixture
def token_acesso(usuario_teste):
    """Cria um token de acesso para testes."""
    return criar_token_acesso({"sub": usuario_teste["email"]})

@pytest.fixture
def headers_autenticacao(token_acesso):
    """Headers com token de autenticação."""
    return {"Authorization": f"Bearer {token_acesso}"}

@pytest.fixture
def produto_teste():
    """Dados de produto para testes."""
    return {
        "titulo": "Produto Teste",
        "descricao": "Descrição do produto teste",
        "preco": 99.99,
        "categoria": "Eletrônicos",
        "status": "ativo"
    }
