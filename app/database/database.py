"""
Configuração do banco de dados
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from ..core.config import configuracoes
from ..models import Base

# Criar engine do banco de dados
engine = create_engine(
    configuracoes.database_url,
    pool_pre_ping=True,
    echo=configuracoes.debug
)

# Criar sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def criar_tabelas():
    """Criar todas as tabelas no banco de dados"""
    Base.metadata.create_all(bind=engine)


def obter_sessao() -> Session:
    """
    Obter sessão do banco de dados
    """
    sessao = SessionLocal()
    try:
        yield sessao
    finally:
        sessao.close()


# Alias para compatibilidade
get_db = obter_sessao
