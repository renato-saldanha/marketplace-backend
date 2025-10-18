"""
Modelo base para todos os modelos do banco de dados
"""
from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()


class ModeloBase(Base):
    """Modelo base com campos comuns"""
    __abstract__ = True
    
    def __init__(self, **kwargs):
        if 'id' not in kwargs:
            kwargs['id'] = str(uuid.uuid4())
        super().__init__(**kwargs)
    
    id = Column(String, primary_key=True, index=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())
