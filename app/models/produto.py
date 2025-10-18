"""
Modelo de produto
"""
from sqlalchemy import Column, String, Text, Numeric, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import ModeloBase
import enum


class StatusProduto(enum.Enum):
    """Enum para status do produto"""
    ATIVO = "ativo"
    INATIVO = "inativo"
    VENDIDO = "vendido"
    RASCUNHO = "rascunho"


class Produto(ModeloBase):
    """Modelo de produto do marketplace"""
    __tablename__ = "produtos"
    
    titulo = Column(String, nullable=False, index=True)
    descricao = Column(Text, nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    imagem_url = Column(String, nullable=True)
    categoria = Column(String, nullable=False, index=True)
    status = Column(Enum(StatusProduto), default=StatusProduto.RASCUNHO, nullable=False)
    
    # Chave estrangeira
    vendedor_id = Column(String, ForeignKey("usuarios.id"), nullable=False)
    
    # Relacionamentos
    vendedor = relationship("Usuario", back_populates="produtos")
