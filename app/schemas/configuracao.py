"""
Schemas para configurações do usuário
"""
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class ConfiguracaoBase(BaseModel):
    """Schema base para configurações"""
    # Configurações de notificações
    notificacoes_email: bool = True
    notificacoes_push: bool = True
    notificacoes_vendas: bool = True
    notificacoes_mensagens: bool = True
    notificacoes_promocoes: bool = True
    
    # Configurações de privacidade
    perfil_publico: bool = False
    mostrar_contato: bool = True
    mostrar_email: bool = False
    
    # Configurações de exibição
    tema_preferido: str = "claro"  # claro, escuro, auto
    idioma_preferido: str = "pt-BR"
    
    # Configurações de dados
    compartilhar_analytics: bool = True
    receber_newsletter: bool = False


class ConfiguracaoAtualizar(BaseModel):
    """Schema para atualizar configurações"""
    # Configurações de notificações
    notificacoes_email: Optional[bool] = None
    notificacoes_push: Optional[bool] = None
    notificacoes_vendas: Optional[bool] = None
    notificacoes_mensagens: Optional[bool] = None
    notificacoes_promocoes: Optional[bool] = None
    
    # Configurações de privacidade
    perfil_publico: Optional[bool] = None
    mostrar_contato: Optional[bool] = None
    mostrar_email: Optional[bool] = None
    
    # Configurações de exibição
    tema_preferido: Optional[str] = None
    idioma_preferido: Optional[str] = None
    
    # Configurações de dados
    compartilhar_analytics: Optional[bool] = None
    receber_newsletter: Optional[bool] = None


class ConfiguracaoResposta(ConfiguracaoBase):
    """Schema de resposta das configurações"""
    id: str
    usuario_id: str
    data_criacao: datetime
    data_atualizacao: Optional[datetime] = None
    
    # Configuração do modelo (Pydantic v2)
    model_config = ConfigDict(
        from_attributes=True
    )
