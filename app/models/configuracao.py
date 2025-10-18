"""
Modelo para configurações do usuário
"""
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import ModeloBase


class ConfiguracaoUsuario(ModeloBase):
    """Modelo para configurações do usuário"""
    __tablename__ = "configuracoes_usuario"

    usuario_id = Column(String, ForeignKey("usuarios.id"), nullable=False, unique=True)
    
    # Configurações de notificações
    notificacoes_email = Column(Boolean, default=True, nullable=False)
    notificacoes_push = Column(Boolean, default=True, nullable=False)
    notificacoes_vendas = Column(Boolean, default=True, nullable=False)
    notificacoes_mensagens = Column(Boolean, default=True, nullable=False)
    notificacoes_promocoes = Column(Boolean, default=True, nullable=False)
    
    # Configurações de privacidade
    perfil_publico = Column(Boolean, default=False, nullable=False)
    mostrar_contato = Column(Boolean, default=True, nullable=False)
    mostrar_email = Column(Boolean, default=False, nullable=False)
    
    # Configurações de exibição
    tema_preferido = Column(String, default="claro", nullable=False)  # claro, escuro, auto
    idioma_preferido = Column(String, default="pt-BR", nullable=False)
    
    # Configurações de dados
    compartilhar_analytics = Column(Boolean, default=True, nullable=False)
    receber_newsletter = Column(Boolean, default=False, nullable=False)
    
    # Relacionamento
    usuario = relationship("Usuario", back_populates="configuracao")

    def __repr__(self):
        return f"<ConfiguracaoUsuario(usuario_id={self.usuario_id})>"
