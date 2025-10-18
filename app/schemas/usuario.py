"""
Schemas para usuário
"""
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime


class UsuarioBase(BaseModel):
    """Schema base para usuário"""
    email: EmailStr
    nome: str
    foto_perfil_url: Optional[str] = None
    foto_perfil_data: Optional[str] = None


class UsuarioCriar(UsuarioBase):
    """Schema para criar usuário"""
    senha: str


class UsuarioAtualizar(BaseModel):
    """Schema para atualizar usuário"""
    nome: Optional[str] = None
    ativo: Optional[bool] = None
    foto_perfil_url: Optional[str] = None
    foto_perfil_data: Optional[str] = None


class AlterarSenha(BaseModel):
    """Schema para alteração de senha"""
    senha_atual: str
    nova_senha: str


class UsuarioResposta(UsuarioBase):
    """Schema de resposta do usuário"""
    id: str
    ativo: bool
    data_criacao: datetime
    data_atualizacao: Optional[datetime] = None
    foto_perfil_thumb: Optional[str] = None
    foto_perfil_medium: Optional[str] = None
    
    # Configuração do modelo (Pydantic v2)
    model_config = ConfigDict(
        from_attributes=True
    )


class UsuarioLogin(BaseModel):
    """Schema para login"""
    email: EmailStr
    senha: str


class Token(BaseModel):
    """Schema para token de acesso"""
    access_token: str
    token_type: str
    usuario: UsuarioResposta


class MensagemResposta(BaseModel):
    """Schema para resposta simples com mensagem"""
    mensagem: str
