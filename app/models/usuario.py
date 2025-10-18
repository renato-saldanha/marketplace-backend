"""
Modelo de usuário
"""
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from .base import ModeloBase


class Usuario(ModeloBase):
    """Modelo de usuário do sistema"""
    __tablename__ = "usuarios"
    
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    ativo = Column(Boolean, default=True)
    foto_perfil_url = Column(String, nullable=True)
    
    # Relacionamentos
    produtos = relationship("Produto", back_populates="vendedor")
    configuracao = relationship("ConfiguracaoUsuario", back_populates="usuario", uselist=False)
